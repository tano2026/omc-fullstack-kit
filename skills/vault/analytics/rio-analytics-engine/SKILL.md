---
title: RIO Analytics Engine v2.0
name: rio-analytics-engine
description: Full analytics module — Market Analysis, SWOT, Sentiment Mining, Trend Forecasting, KPI Dashboarding với fact-checker rating system + verification loop.
author: Tano Agency
---

# RIO Analytics Engine v2.0

## Overview
Module phân tích dữ liệu chuyên nghiệp, chạy không cần API key — chỉ dùng web search (DuckDuckGo). Được thiết kế cho RIO bot (Research & Intelligence Officer), có thể dùng lại cho bất kỳ agent research nào.

**Dependencies:** pandas, numpy, requests (standard Python libs)
**Zero API keys required:** Chỉ dùng DDG web search free.

## Architecture — 8 Classes

```
Analytics (wrapper)
 ├── MarketAnalyzer
 │   ├── analyze_market()     — Market overview with sub-question workflow
 │   └── swot_analysis()      — SWOT with source-attributed evidence
 ├── SentimentMiner
 │   └── analyze()            — Keyword-based sentiment + fact-checker ratings
 ├── TrendForecaster
 │   └── forecast()           — Signal extraction with confidence levels
 ├── KPIDashboard
 │   └── dashboard()          — TAM/SAM/SOM + growth + competition scorecard
 ├── VerificationLoop          — 6-8 structural checks per analysis type
 └── ProgressTracker           — Checkpoint persistence (JSON file)
```

## Design Principles (from 5 skills)

### 1. ECC-Market-Research Templates
- Output format: Executive Summary → Key Findings → Implications → Risks → Recommendation → Sources
- Phân biệt: **Fact** (có nguồn kiểm chứng) | **Inference** (suy luận từ context) | **Recommendation** (gợi ý chiến lược)
- Mọi số liệu đều có source link hoặc label `[inference]`

### 2. Fact-Checker Rating System
| Rating | Meaning | When |
|--------|---------|------|
| ✅ | Verified | Source từ .gov, .org, statista, gartner, worldbank |
| 🟡 | Partial | Từ .edu, forbes, bloomberg, reuters, consulting |
| 🔄 | Unverified | Blog, news, generic — không verify được |
| 🟠 | Likely wrong | Mâu thuẫn với các nguồn khác |
| ❌ | False | Bị bác bỏ |
| ❓ | Uncertain | Không đủ context |

### 3. ECC-Deep-Research Sub-Question Workflow
- Break 1 topic → 3-5 sub-questions
- Research từng sub-question riêng
- Synthesize từ multi-source
- Ghi rõ confidence level per signal

### 4. Harness Engineering — Verification Loop
- auto-detect AI hallucination red flags: "pioneering", "game-changing", "revolutionary", "disruptive"
- Kiểm tra cấu trúc output (exec summary, sources, recommendations...)
- Tự động phát hiện generic content "mở rộng thị trường", "tích hợp AI"

### 5. Data Quality Methodology
- Mỗi metric có flag: 🟢 Verified | 🟡 Estimated | 🟠 Unverified
- TAM/SAM/SOM: ghi rõ "top-down from public data" — không tự sinh số
- Growth rates: average, min, max, source quality distribution

## Class Details

### MarketAnalyzer.analyze_market(topic, industry)
Sub-questions (5): market size, growth CAGR, competitors, trends 2026, challenges
Output sections: Executive Summary → Key Findings → Implications → Risks → Recommendation → Sources

### MarketAnalyzer.swot_analysis(entity)
5 search angles: about, reviews, competitors, news, problems
SO-WO-ST-WT strategy recommendation từ evidence

### SentimentMiner.analyze(keyword, limit=20)
Sentiment bar visualization + fact-checker ratings (3 claims)
Verdict: 🟢/🟡/⚪/🟠/🔴

### TrendForecaster.forecast(topic, horizon="3-6 months")
5 sub-questions: Past → Present → Future → Related → Risks
4 signal types + confidence scoring (source count × diversity)

### KPIDashboard.dashboard(domain)
TAM/SAM/SOM top-down, CAGR extraction, competition detection
KPI Scorecard: 5 metrics with quality flags

### VerificationLoop
verify_report(type, text) → {"all_passed": bool, "checks": [...]}
- market: 6 checks
- swot: 5 checks
- sentiment: 2 checks
- forecast: 3 checks
- kpi: 3 checks

### ProgressTracker
JSON checkpoint persistence, resume support.
Phases: research → analyze → verify → deliver

## Integration
```python
from modules.analytics import Analytics
engine = Analytics()
report = engine.run("market", "AI agents Vietnam")
```
