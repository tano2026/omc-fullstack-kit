# Research & Analytics Integration — Skill Patterns cho RIO Bot

> This file documents research/analytics skill patterns discovered from the AI-Vibe-Toolkit library that can be reused in RIO bot and similar research bots. Created 2026-07-17.

## 1. Skill → Use Case Mapping

### Core Research Skills

| Skill | What it provides | RIO integration |
|-------|-----------------|-----------------|
| `ecc-market-research` | Output template: Executive Summary → Findings → Implications → Risks → Rec → Sources | `/analyze`, `/kpi` output formatting |
| `ecc-deep-research` | Sub-question workflow: decompose → multi-source → deep-read → synthesize | `/research deep` logic, `/research` multi-step |
| `fact-checker` | Rating system: ✅/🟡/🔄/🟠/❌/❓ + claim extraction → verify → verdict | Data quality labels in all analytics output |
| `research-agent` | Prompt template for structured research | Fallback prompt structure for `/research quick` |
| `deep-researchs` | L0-L5 research ladder | Tier selection in research command |

### Data Collection Skills

| Skill | What it provides | RIO integration |
|-------|-----------------|-----------------|
| `auto-research-trending` | Chinese platform sources (Douyin, Weibo, Xiaohongshu, Bilibili, Baidu, Zhihu) + GitHub/Reddit/PH | Overlap with `cn_trends.py` — merge methodology |
| `ecc-data-scraper-agent` | COLLECT → ENRICH → STORE architecture, batch AI calls, retry, dedup, feedback learning | Data pipeline design for `/watch` + `/kpi` |
| `x-research` | X/Twitter API research: search, thread, monitor | X research if X API available |
| `company-due-diligence` | 6-step VN company cross-ref: registry → VPĐD → website → social → director → red flags | `/swot` VN company analysis |

### Competitive Intelligence Skills

| Skill | What it provides | RIO integration |
|-------|-----------------|-----------------|
| `ecc-lead-intelligence` | Signal scoring → mutual ranking → warm path discovery → enrichment → outreach | `/swot` competitor pipeline |
| `youtube-research-agent` | YouTube channel analysis, topic pattern extraction, content mapping | `/research` YouTube content research |
| `ecc-search-first` | "Research before code" methodology: repo → npm → MCP → skills → GitHub → decide | Research methodology reference |

### Content & Output Skills

| Skill | What it provides | RIO integration |
|-------|-----------------|-----------------|
| `ecc-content-engine` | Source-First workflow, platform adaptation, hard bans on slop | `/brief` tone, `/trend` style |
| `ecc-marketing-campaign` | Campaign planning: positioning → audience → copy → calendar | Marketing analytics output |
| `ecc-brand-voice` | Voice profile from real sources | Consistent bot tone across outputs |
| `ecc-crosspost` | Multi-platform adaptation | Cross-platform trending report format |

## 2. Integration Priority

### P0 — MUST adopt now (already in analytics.py)
- Output template from `ecc-market-research`
- Quality gate rules from `ecc-market-research`
- Sub-question workflow from `ecc-deep-research`
- Fact-checker rating from `fact-checker`
- L0-L5 tier from `deep-researchs`

### P1 — Should merge next
- Auto-retry + batch AI patterns from `ecc-data-scraper-agent`
- Chinese platform source list from `auto-research-trending`
- Company due diligence 6-step from `company-due-diligence`

### P2 — Future enhancement
- Signal scoring model from `ecc-lead-intelligence`
- YouTube channel analysis from `youtube-research-agent`
- Hardware bans from `ecc-content-engine`

## 3. Code Pattern: Merged Analytics Class

```python
# Pattern for analytics.py — combining multiple skill patterns
from modules import web_research

class SmartAnalyzer:
    """Merges ecc-market-research + ecc-deep-research + fact-checker patterns"""
    
    CONFIDENCE_LABELS = {
        90: "Cao",   # Multiple reliable sources, recent data
        70: "Trung bình",  # Limited sources, some estimates
        50: "Thấp",  # Single source, old data, speculation
    }
    
    QUALITY_LABELS = {
        "confirmed": "✅ Đúng",
        "partial": "🟡 Phần lớn đúng",
        "disputed": "🔄 Có tranh cãi",
        "misleading": "🟠 Phần lớn sai",
        "false": "❌ Sai",
        "unknown": "❓ Ko verify được",
    }
    
    def report_template(self, topic, analysis_type, sources_count, confidence):
        return f"""📊 {topic}: {analysis_type}
Generated: {datetime.now().strftime('%Y-%m-%d')} | Sources: {sources_count} | Confidence: {confidence}

## Executive Summary
{{exec_summary}}

## Key Findings
{{findings}}

## Implications
{{implications}}

## Risks & Caveats
{{risks}}

## Recommendation
{{recommendation}}

## Sources
{{sources}}
"""
    
    def decompose_topic(self, query):
        """Sub-question strategy from ecc-deep-research"""
        return [
            f"{query} market size growth 2025 2026",
            f"{query} top companies competitors",
            f"{query} technology trends innovation",
            f"{query} challenges problems",
            f"{query} future outlook prediction"
        ]
    
    def rate_claim(self, claim_text, sources_count, data_age_months):
        """Fact-checker style rating"""
        if sources_count >= 2 and data_age_months <= 6:
            return "confirmed", 95
        elif sources_count >= 1 and data_age_months <= 12:
            return "partial", 75
        elif data_age_months > 24:
            return "unknown", 50
        else:
            return "unknown", 40

    def quality_gate(self, report: str) -> bool:
        """ecc-market-research quality checks"""
        checks = {
            "Has sources": "Source" in report or "source" in report.lower(),
            "No unsourced numbers": not bool(re.search(r'\$\d+[BMK]', report)) or "estimate" in report.lower(),
            "Has risks": "Risks" in report or "risk" in report.lower() or "Caveats" in report,
            "Has recommendation": "Recommendation" in report,
        }
        return all(checks.values())
```
