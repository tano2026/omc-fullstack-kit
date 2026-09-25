# Skill → Adapter Mapping (Full)

> Hermes Skill Library → `real_adapters.py` function cho Tano Agency

## Cách dùng

Mỗi dòng = 1 adapter có thể code cho agent. Ưu tiên theo thứ tự:
1. **P0** = cần để agent hoạt động thực tế
2. **P1** = nâng cao chất lượng output
3. **P2** = nice-to-have

## Sales 🎯

| Adapter | P | Skill | Chi tiết | API/Key? |
|---------|---|-------|---------|----------|
| `lead_search` | P0 | `ecc-lead-intelligence` | Tìm công ty theo ngành, tách contact info từ snippet. Lead scoring: email=2, sđt=1, linkedin=3 | ❌ $0 |
| `affiliate_check` | P0 | `affiliate-check` | Tra cứu chương trình affiliate — commission, cookie, rating. `openaffiliate.dev` API | ❌ $0 (cached daemon) |
| `search` | P0 | `api-mega-list` | Tìm API miễn phí cho bất kỳ ngành nào | ❌ $0 |
| `crm` | P1 | `ecc-github-ops` | Dùng SQLite + GitHub issue tracker làm CRM mini | ❌ $0 |
| `copywriter` | P1 | `ecc-marketing-campaign` | Viết outreach email theo template + A/B test | ❌ LLM |
| `objection` | P2 | `ecc-safety-guard` | Phản hồi objection phổ biến từ training data | ❌ $0 |

## Marketing 📢

| Adapter | P | Skill | Chi tiết | Key? |
|---------|---|-------|---------|------|
| `seo` | P0 | `ecc-seo` | Keyword research, density check, competitor analysis | ❌ $0 |
| `content` | P0 | `ai-content-writing` | 6 prompt formula cho content ngắn (blog, caption, email) | ❌ LLM |
| `viral_hooks` | P0 | `viral-hooks` | 100 hook formula cho TikTok/Reels/Shorts | ❌ $0 |
| `trends` | P1 | `auto-research-trending` | Scan GitHub Trending, Reddit, Product Hunt, Weibo | ❌ $0 |
| `social` | P1 | `ecc-social-publisher` | Format + post đa nền tảng | ❌ $0 |
| `youtube` | P1 | `youtube-marketings` | 21 command: SEO, script, thumb, analytics, calendar | ❌ $0 |
| `crosspost` | P2 | `ecc-crosspost` | Cross-publish giữa các nền tảng | ❌ $0 |

## Dev 💻

| Adapter | P | Skill | Chi tiết | Key? |
|---------|---|-------|---------|------|
| `review` | P0 | `ecc-verification-loop` | Đã có 6 phase: build→type→lint→test→security→diff | ❌ $0 |
| `repo` | P0 | `ecc-github-ops` | Clone, branch, PR, merge auto | 🟡 GitHub token |
| `deploy` | P1 | `ecc-deployment-patterns` | Dockerfile, docker-compose, CI config | ❌ $0 |
| `debug` | P1 | `ecc-error-handling` | Root cause triage từ log | ❌ $0 |
| `architect` | P1 | `ecc-blueprint` | Thiết kế kiến trúc từ spec | ❌ LLM |
| `docker` | P2 | `ecc-docker-patterns` | Dockerfile patterns cho Python/Node | ❌ $0 |

## Media 🎨

| Adapter | P | Skill | Chi tiết | Key? |
|---------|---|-------|---------|------|
| `render` | P0 | `hyperframes` (+10 sub) | Pipeline video hoàn chỉnh: init→add→capture→render | ❌ $0 |
| `image_gen` | P1 | `ecc-fal-ai-media` | Tạo ảnh AI qua FAL (Flux/Imagen) | 🟡 FAL key |
| `captions` | P1 | `embedded-captions` | 36-style catalog, subject matting, VFX | ❌ $0 |
| `tts` | P1 | `faceless-explainer` (TTS) | Edge TTS fallback: giọng vi-VN | ❌ $0 |
| `design` | P2 | `ecc-design-system` | Design token, component, responsive grid | ❌ $0 |
| `slides` | P2 | `slideshow` | HyperFrames slideshow: presentation, pitch deck | ❌ $0 |

## Support 🎧

| Adapter | P | Skill | Chi tiết | Key? |
|---------|---|-------|---------|------|
| `invoice` | P0 | `invoice-extractor` | PDF hóa đơn → JSON → Misa format | ❌ $0 |
| `kb` | P0 | `ecc-knowledge-ops` | 6-layer knowledge: 1.GitHub→2.Memory→3.MCP Graph→4.KB repo→5.External→6.Archive | ❌ $0 |
| `ticket` | P1 | `ecc-customer-billing-ops` | Phân loại + priority + route billing ticket | ❌ $0 |
| `billing` | P1 | `ecc-finance-billing-ops` | Billing ops: invoice, payment, subscription | ❌ $0 |

## Analytics 📊

| Adapter | P | Skill | Chi tiết | Key? |
|---------|---|-------|---------|------|
| `market_report` | P0 | `ecc-market-research` | TAM/SAM/SOM, competitive map, unit economics, risks, verdict | ❌ $0 |
| `dashboard` | P1 | `sc-datav` | 3D sci-fi dashboard từ data CSV/JSON | ❌ $0 |
| `lead_intel` | P1 | `ecc-lead-intelligence` | Score + segment lead list | ❌ $0 |

## Operations ⚙️

| Adapter | P | Skill | Chi tiết | Key? |
|---------|---|-------|---------|------|
| `incident` | P1 | `ecc-canary-watch` | Canary release + rollback health check | ❌ $0 |
| `decision` | P2 | `ecc-recursive-decision-ledger` | Decision tree + audit trail | ❌ $0 |

## CEO 👔

| Adapter | P | Skill | Chi tiết | Key? |
|---------|---|-------|---------|------|
| `plan` | P0 | `ecc-plan-orchestrate` | Sprint planning, task decomposition, estimation | ❌ LLM |
| `orchestrate` | P0 | `ecc-team-agent-orchestration` | Multi-agent kanban, handoff protocol, gate check | ❌ $0 |
| `stocktake` | P1 | `ecc-skill-stocktake` | Rà soát skills + agents + việc tồn | ❌ $0 |

## Lưu ý key

- **❌ $0** = chạy được ngay, không cần API key
- **🟡 có thể cần key** = nếu muốn gọi API thật (có fallback rule-based)
- **❌ LLM** = cần LLM key (DeepSeek hoặc OpenRouter) — nếu thiếu, dùng fallback markdown template
