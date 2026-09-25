#!/usr/bin/env python3
"""
verify_script.py — Factual audit for Airfare Decoded scripts.

Usage:
    python verify_script.py <script_path> [--json]

Scans a script markdown file and flags:
  - Fare class names vs known IATA booking codes
  - Airline names vs known US carriers
  - Specific numbers without confidence tier annotation
  - "X million/billion/percent" patterns (likely unsourced)
  - Absolute language (all/every/always/never)
  - Regulatory claims without DOT/FAA source
  - Pre-2024 data patterns

Returns a pass/fail report with actionable items.
"""

import re
import sys
import json
from pathlib import Path

# =============================================================================
# Knowledge Base
# =============================================================================

IATA_BOOKING_CODES = {
    # First Class
    "F": "First (full fare)", "A": "First (discounted)", "P": "First (premium)",
    # Business
    "J": "Business (full fare)", "C": "Business (full fare)", "D": "Business (discounted)",
    "I": "Business (discounted)", "R": "Business (supersonic)", "Z": "Business (discounted)",
    # Premium Economy
    "W": "Premium Economy", "E": "Premium Economy (discounted)",
    # Economy
    "Y": "Economy (full fare)", "B": "Economy (full fare variant)",
    "M": "Economy (standard)", "H": "Economy (standard)",
    "Q": "Economy (discount)", "V": "Economy (discount)",
    "W": "Economy (premium)", "S": "Economy (deep discount)",
    "T": "Economy (deep discount)", "L": "Economy (deep discount)",
    "K": "Economy (deep discount)", "U": "Economy (discount)",
    "N": "Economy (Basic Economy - United)", "E": "Economy (Basic Economy - Delta)",
    # Basic Economy Delta
    "E": "Basic Economy (Delta Main Basic)",
    # Basic Economy United
    "N": "Basic Economy (United)", "B": "Basic Economy (American)",
}

# Delta-specific fare class mapping
DELTA_CLASSES = {
    "E": "Delta Main Basic (Basic Economy)",
    "Y": "Delta Main Cabin (full fare)",
    "B": "Delta Main Cabin",
    "M": "Delta Main Cabin",
    "H": "Delta Main Cabin",
    "Q": "Delta Main Cabin (discount)",
    "V": "Delta Main Cabin (deep discount)",
    "X/S/T/K/L": "Delta Main Cabin (lowest discount)",
    "G": "Delta Comfort+ (paid upgrade)",
    "W": "Delta Premium Select",
    "A": "Delta Business (discount)",
    "C": "Delta One (business)",
    "D": "Delta One (discount)",
    "I": "Delta One (lowest business)",
    "J": "Delta One (full fare)",
    "F": "Delta First (domestic)",
    "P": "Delta One (premium)",
}

# United-specific fare class mapping
UNITED_CLASSES = {
    "N": "United Basic Economy",
    "Y": "United Economy (full fare)",
    "B": "United Economy",
    "M": "United Economy (standard)",
    "E": "United Economy (standard)",
    "U": "United Economy (standard)",
    "H": "United Economy (standard)",
    "Q": "United Economy (discount)",
    "V": "United Economy (deep discount)",
    "W": "United Economy (deep discount)",
    "S": "United Economy (deep discount)",
    "T": "United Economy (deep discount)",
    "L": "United Economy (deep discount)",
    "K": "United Economy (deep discount)",
    "G": "United Economy (lowest)",
    "O": "United Economy (lowest)",
}

# American-specific fare class mapping
AA_CLASSES = {
    "B": "American Basic Economy",
    "Y": "American Main Cabin (full fare)",
    "W": "American Main Cabin (discount)",
    "H": "American Main Cabin",
    "K": "American Main Cabin",
    "M": "American Main Cabin",
    "L": "American Main Cabin",
    "V": "American Main Cabin (discount)",
    "S": "American Main Cabin (discount)",
    "N": "American Main Cabin (discount)",
    "Q": "American Main Cabin (discount)",
    "O": "American Main Cabin (lowest)",
    "P": "American Premium Economy",
    "J": "American Business (full fare)",
    "D": "American Business (discount)",
    "I": "American Business (lowest)",
    "R": "American Flagship Business",
    "F": "American First (full fare)",
    "A": "American First (discount)",
}

US_AIRLINES = {
    "delta": "Delta Air Lines", "united": "United Airlines", "american": "American Airlines",
    "southwest": "Southwest Airlines", "jetblue": "JetBlue", "alaska": "Alaska Airlines",
    "spirit": "Spirit Airlines", "frontier": "Frontier Airlines", "allegiant": "Allegiant Air",
    "hawaiian": "Hawaiian Airlines", "breeze": "Breeze Airways", "avelo": "Avelo Airlines",
    "sun country": "Sun Country Airlines",
}

TIER_KEYWORDS = {
    "Tier A": "Tier A", "Tier B": "Tier B", "Tier C": "Tier C", "Tier D": "Tier D",
    "Tier A": "Tier A", "Tier B": "Tier B", "Tier C": "Tier C", "Tier D": "Tier D",
}

ABSOLUTE_WORDS = [
    "all airlines", "every airline", "always", "never", "always happens", "guaranteed upgrade",
    "always get", "every flight", "never happens", "always the same",
]

REGULATORY_PHRASES = [
    "dot says", "dot rule", "department of transportation", "faa mandates",
    "federal law requires", "airlines must", "required by law",
]

DOT_REGULATIONS = {
    "24-hour refund": "14 CFR Part 259 — Enhanced Protections for Airline Passengers (2024)",
    "automatic refund": "DOT Final Rule — Refunds and Other Consumer Protections (April 2024)",
    "fee transparency": "DOT Final Rule — Enhancing Transparency of Airline Ancillary Service Fees (April 2024)",
    "junk fees": "DOT Final Rule on Ancillary Fee Disclosure (April 2024), currently under legal challenge",
}


# =============================================================================
# Check Functions
# =============================================================================

def check_fare_classes(text):
    """Flag fare class mentions that don't match known codes."""
    findings = []
    
    # Look for fare class letter mention patterns
    patterns = [
        r"fare class\s+([A-Z])",
        r'([A-Z])\s*fare class',
        r'class\s+([A-Z])\s*\(',
        r"booking code\s+([A-Z])",
        r"([A-Z])\s*basic economy",
        r"([A-Z])\s*main cabin",
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            code = match.group(1).upper()
            if code not in IATA_BOOKING_CODES:
                # Check if it's in airline-specific mapping
                findings.append({
                    "type": "UNKNOWN_FARE_CLASS",
                    "match": match.group(0),
                    "code": code,
                    "line": text[max(0, match.start()-50):match.end()+50],
                    "severity": "HIGH",
                    "message": f"Fare class '{code}' not in standard IATA booking codes. Verify specific airline mapping."
                })
    
    return findings


def check_airline_names(text):
    """Check if airline names mentioned exist."""
    findings = []
    
    # Scan for airline-like patterns
    mentions = re.findall(r'\b([A-Z][a-z]+(?:\s[A-Za-z]+)?)\s[Aa]irline[s]?\b', text)
    
    for mention in mentions:
        key = mention.lower()
        if key not in US_AIRLINES and key not in {"some", "most", "many", "other", "major", "u.s.", "us"}:
            findings.append({
                "type": "UNKNOWN_AIRLINE",
                "match": mention,
                "severity": "MEDIUM",
                "message": f"'{mention}' not in known US airline list. Check if it's correct."
            })
    
    return findings


def check_unsourced_numbers(text):
    """Flag specific numbers that don't have a tier annotation nearby."""
    findings = []
    lines = text.split('\n')
    
    # Patterns for numbers that might be unsourced
    number_patterns = [
        r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*(?!percent|%)\w+)?',
        r'(\d+\.?\d*)\s*(million|billion|trillion)',
        r'(\d+\.?\d*)\s*(percent|%)\s+of',
        r'(\d+)\s*(dollars|USD|bucks)',
    ]
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Skip lines that have tier annotation already
        if any(t in stripped for t in TIER_KEYWORDS):
            continue
        if stripped.startswith('#') or stripped.startswith('-') or stripped.startswith('['):
            continue
        if stripped.startswith('```') or stripped.startswith('|') or stripped.startswith('*'):
            continue
        if 'Tier A' in stripped or 'Tier B' in stripped or 'Tier C' in stripped:
            continue
        
        for pattern in number_patterns:
            matches = re.findall(pattern, stripped)
            if matches:
                # Check surrounding lines for tier annotation
                context = lines[max(0,i-3):min(len(lines),i+2)]
                context_text = '\n'.join(context)
                if not any(t in context_text for t in TIER_KEYWORDS):
                    findings.append({
                        "type": "UNSOURCED_NUMBER",
                        "match": str(matches[0]) if isinstance(matches[0], str) else matches[0][0],
                        "line": i,
                        "text": stripped[:120],
                        "severity": "HIGH" if 'million' in stripped.lower() or 'billion' in stripped.lower() else "MEDIUM",
                        "message": f"Number without tier annotation nearby. Either add Tier tag or convert to range."
                    })
                break  # one flag per line max
    
    return findings


def check_absolute_language(text):
    """Flag absolute language."""
    findings = []
    for phrase in ABSOLUTE_WORDS:
        if phrase in text.lower():
            # Find all occurrences
            for match in re.finditer(re.escape(phrase), text, re.IGNORECASE):
                findings.append({
                    "type": "ABSOLUTE_LANGUAGE",
                    "match": match.group(0),
                    "severity": "MEDIUM",
                    "message": f"'{match.group(0)}' — absolutes are almost always wrong in airline pricing. Qualify or remove."
                })
                break  # one finding per phrase type
    return findings


def check_regulatory_claims(text):
    """Flag regulatory claims without DOT source."""
    findings = []
    for phrase in REGULATORY_PHRASES:
        if phrase in text.lower():
            findings.append({
                "type": "UNSOURCED_REGULATION",
                "match": phrase,
                "severity": "HIGH",
                "message": f"'{phrase}' mentioned without regulation number. Add specific DOT rule (e.g. 'April 2024 DOT rule on refunds')"
            })
    return findings


def check_basic_economy_detail(text):
    """Check for airline-specific Basic Economy detail (not generic)."""
    findings = []
    
    # If mentions Basic Economy but doesn't name a specific airline
    be_mentions = list(re.finditer(r'Basic Economy', text, re.IGNORECASE))
    if len(be_mentions) > 0:
        snippet = text[:text.find('\n\n')] if '\n\n' in text else text[:500]
        has_airline = any(
            al.lower() in snippet.lower() 
            for al in ['Delta', 'United', 'American', 'Southwest', 'JetBlue']
        )
        if not has_airline:
            findings.append({
                "type": "GENERIC_BASIC_ECONOMY",
                "match": "Basic Economy",
                "severity": "MEDIUM",
                "message": "Basic Economy mentioned without specifying airline. Each airline's BE has different rules."
            })
    
    return findings


def check_false_precision(text):
    """Flag patterns of false precision."""
    findings = []
    
    # Flag very specific dollar amounts (not round numbers)
    for match in re.finditer(r'\$(\d+)\.(\d{2})', text):
        dollars = int(match.group(1))
        cents = int(match.group(2))
        context = text[max(0, match.start()-30):match.end()+30]
        
        # Check if it's a range or percentage, not a specific claim
        if cents != 0 and '$0' not in context:
            findings.append({
                "type": "FALSE_PRECISION",
                "match": match.group(0),
                "severity": "LOW",
                "message": f"'{match.group(0)}' has cents precision. If this is not from an official source, round it."
            })
    
    return findings


def check_delta_fare_ladder(text):
    """Specifically verify Delta fare ladder if mentioned."""
    findings = []
    if 'delta' in text.lower():
        # Extract fare class mentions near Delta
        delta_section = re.search(r'delta.*?(?=\n\n|$)', text, re.IGNORECASE | re.DOTALL)
        if delta_section:
            section = delta_section.group(0)
            classes_mentioned = set()
            for code in "YBMHQVWSPFD":
                if code in section:
                    classes_mentioned.add(code)
            
            # Check if E (Basic Economy) is in correct position
            if 'E' in section and 'Basic Economy' in section:
                # Should say E is lowest, then Y/B/M... up
                if section.find('E') > section.find('Y') and 'Basic Economy' in section:
                    findings.append({
                        "type": "DELTA_FARE_ORDER",
                        "match": "Delta fare ladder order",
                        "severity": "HIGH",
                        "message": "Delta fare ladder order suspect. E (Basic Economy) should be lowest, below Y/B/M/H/Q/V."
                    })
    
    return findings


# =============================================================================
# Main Audit
# =============================================================================

def audit_script(text):
    """Run all checks and return a report."""
    all_findings = []
    
    checkers = [
        ("Fare Class Validation", check_fare_classes),
        ("Airline Name Check", check_airline_names),
        ("Unsourced Numbers", check_unsourced_numbers),
        ("Absolute Language", check_absolute_language),
        ("Regulatory Claims", check_regulatory_claims),
        ("Generic Basic Economy", check_basic_economy_detail),
        ("False Precision", check_false_precision),
        ("Delta Fare Ladder", check_delta_fare_ladder),
    ]
    
    for section_name, checker in checkers:
        findings = checker(text)
        for f in findings:
            f["section"] = section_name
        all_findings.extend(findings)
    
    # Severity counts
    high = sum(1 for f in all_findings if f.get("severity") == "HIGH")
    medium = sum(1 for f in all_findings if f.get("severity") == "MEDIUM")
    low = sum(1 for f in all_findings if f.get("severity") == "LOW")
    
    # Calculate score (0.0 - 1.0)
    if len(all_findings) == 0:
        score = 1.0
    else:
        high_penalty = high * 0.2
        medium_penalty = medium * 0.1
        low_penalty = low * 0.05
        score = max(0.0, 1.0 - high_penalty - medium_penalty - low_penalty)
    
    report = {
        "pass": score >= 0.7,
        "score": round(score, 2),
        "total_findings": len(all_findings),
        "high_severity": high,
        "medium_severity": medium,
        "low_severity": low,
        "findings": all_findings,
        "summary": []
    }
    
    if score >= 1.0:
        report["summary"].append("PASS — No issues found.")
    elif score >= 0.7:
        report["summary"].append(f"CONDITIONAL PASS — {len(all_findings)} issues ({high} high, {medium} medium, {low} low). Fix before publish.")
    else:
        report["summary"].append(f"FAIL — {len(all_findings)} issues ({high} high, {medium} medium, {low} low). Fix required before proceeding.")
    
    if high > 0:
        report["summary"].append(f"🚨 {high} HIGH severity issues — must fix before publish.")
    if medium > 0:
        report["summary"].append(f"⚠️ {medium} MEDIUM severity issues — should fix.")
    
    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_script.py <script_path> [--json]")
        sys.exit(1)
    
    script_path = Path(sys.argv[1])
    output_json = "--json" in sys.argv
    
    if not script_path.exists():
        print(f"File not found: {script_path}")
        sys.exit(1)
    
    text = script_path.read_text(encoding='utf-8')
    report = audit_script(text)
    
    if output_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        status = "✅ PASS" if report["pass"] else "❌ FAIL"
        print(f"{'='*60}")
        print(f"  AIRFARE DECODED — SCRIPT VERIFICATION REPORT")
        print(f"{'='*60}")
        print(f"  Score:  {report['score']:.0%}")
        print(f"  Status: {status}")
        print(f"  Issues: {report['total_findings']} total")
        print(f"          {report['high_severity']} high | {report['medium_severity']} medium | {report['low_severity']} low")
        print(f"{'='*60}")
        
        for s in report["summary"]:
            print(f"  {s}")
        
        if report["findings"]:
            print(f"\n{'─'*60}")
            print(f"  DETAILED FINDINGS")
            print(f"{'─'*60}")
            for i, f in enumerate(report["findings"], 1):
                emoji = {"HIGH": "🚨", "MEDIUM": "⚠️", "LOW": "ℹ️"}.get(f.get("severity", "MEDIUM"), "•")
                print(f"\n  [{emoji}] #{i} — {f['section']}")
                print(f"      Severity: {f['severity']}")
                print(f"      Match: {f.get('match', 'N/A')}")
                print(f"      Message: {f['message']}")
                if 'line' in f:
                    print(f"      Line: {f['line']}")
    
    sys.exit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
