---
name: youtube-script-production
title: YouTube Script Production
description: Class-level workflow for producing YouTube scripts with AI (DeepSeek R1, etc.) — from prompt to final verified deliverable. Covers Airfare Decoded (English) and general script pipelines.
---

# YouTube Script Production

## When to Load
- User says "viết script", "gen script", "draft video script", "sản xuất script"
- User refers to "script" + video/channel name
- User mentions "R1" or "DeepSeek R1" for content

## Pipeline

### Phase 1: Research & Prompt
1. Confirm channel name, target audience, video topic, tone
2. Gather reference material (competing videos, sources, regulations)
3. Build prompt with: hook structure, case study format, CTA, length, sources to cite
4. **CRITICAL**: Instruct the model to cite only VERIFIABLE data. Ban fake stats, fake fines, fake case studies — the AI WILL fabricate convincing-sounding numbers

### Phase 2: Generation
1. Use model specified by user (prefer DeepSeek R1 for Airfare Decoded, deepseek-chat for Vietnamese)
2. Set max_tokens high enough (8K+ for full script)
3. Write output to structured file `script_r1.md` (or `script_v{N}.md`)

### Phase 3: Delivery & Review
1. Present script to user for review with scene summary
2. User will fact-check — expect corrections
3. **DO NOT argue** — user knows the domain better than any AI
4. Patch script per corrections immediately

### Phase 4: Correction Loop
1. Read full script file
2. For each user correction: `patch()` targeted replacements
3. Re-read full file to verify consistency
4. Check for stale references (names, sources, stats that should have been renamed)
5. Present diff summary to user

## Verified Sources (Airfare Decoded)

| Topic | Real Source | Don't Use |
|-------|-------------|-----------|
| Senate airline investigation | PSI Report Nov 2024 — $12.4B seat fees 2018-2023, $26M gate agent bonuses | "Fined $200M" (never happened) |
| DOT cancellation rule | CFR 14 Part 259 — 24h free cancellation if flight >= 7 days away | Medical exemption loopholes |
| DOT refund rule | Oct 2024 mandate — automatic refunds on cancel/significant change within 7 business days | Doctor's note hacks |
| Fare class charts | Pick ONE airline. Delta: E (BE) / Q,S (MC) / W (PS) / J,D (Biz) / P,F (First) | Mixed airline codes |
| Ancillary revenue | IdeaWorksCompany 2023 — $33B global, ~50% for ULCC | — |

## Critical Pitfalls

### DO NOT fabricate:
- **Fake fines**: Senate PSI didn't fine anyone. Never say "fined $X" without verifying
- **Fake case studies**: If using a named person, it must be "composite story" disclaimer or "imagine this"
- **Fake loopholes**: Credit card status match, medical exemption hacks are often wrong
- **Mixed fare codes**: Pick ONE airline and get their specific codes right — Delta's N is NOT Basic Economy (United uses N for BE)

### DO verify:
- Every dollar figure — Google the exact number
- Every regulation citation — check CFR / DOT title number
- Loopholes must be tested by user or documented as real

### Consistency checks:
- After patching, check ALL scenes for stale names (e.g. old character names, old stats)
- Scene numbering must remain sequential after insert/delete
- Scene title must match its content after renames

### General writing:
- No named real people without disclaimer
- Pick ONE airline for fare examples and stay consistent throughout
- Prefer "imagine this" / "one traveler" / "a passenger" over fake characters
