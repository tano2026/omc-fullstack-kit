# Phase 2 Multi-Agent Dispatch Example — Tử Vi "Giải Mã Số Phận"

## Context
Date: 20/07/2026
Project: Tử Vi landing page + payment system
Method: Hermes `delegate_task` — 3 parallel subagents

## Sequence

```
User: "Tu vi. Tiếp tục Phase 2"
→ Hermes dispatches 3 in parallel:
  1. Dev (started first, completed in ~4min)
  2. Media (started after Dev, ~4min)
  3. Marketing (started after Dev, ~2min)

All 3 completed within ~4 minutes total (overlapping).
```

## What Each Subagent Did

### Dev (already done in a prior session)
- `app.js` — form validation, API calls, payment modal, error handling
- `index.html` — script integration, data attributes
- `backend/main.py` — Momo + VNPay endpoints
- Tested full flow: API demo + products + payment redirects

### Media Subagent (1 call, 46 API calls, ~4min)
| File | Size | Task |
|------|------|------|
| `assets/logo.svg` | 4.2 KB | Logo "GIẢI MÃ" + "SỐ PHẬN", Bắc Đẩu 7 sao + mắt thứ 3 |
| `assets/favicon.svg` | 1 KB | Favicon SVG |
| `assets/icons.svg` | 3.9 KB | 8 SVG sprite icons |
| `assets/og-image.svg` | 3.4 KB | Social share 1200×630 |
| `frontend/style.css` | 9.4 KB | Result cards, testimonials, FAQ, scroll animations, particles |

Modified: `index.html` (OG meta, favicon, hero particles, logo), `app.js` (severity colors, icon mapping)

### Marketing Subagent (1 call, 15 API calls, ~2min)
| File | Task |
|------|------|
| `docs/BRAND_VOICE_GUIDE.md` | Tone + từ cấm + từ khuyến khích |
| `frontend/result-content.js` | 7 paint point explanations in conversational Vietnamese |
| `docs/TEASER_POSTS.md` | Facebook + TikTok + Zalo teaser scripts |

Modified: `index.html` — Hero ("Số phận của bạn không phải bí ẩn — nó là bản đồ"), Features (4 cards), Testimonials (3 case studies), FAQ (8 questions), SEO meta, CTA section

## Key Pattern

```
Hermes → delegate_task(dev_goal)          # 1st wave
Hermes → delegate_task(media_goal)        # 2nd wave (parallel with marketing)
Hermes → delegate_task(marketing_goal)    # 2nd wave (parallel with media)

After all complete:
  Hermes → verify results (ls -la, wc -l, curl test)
  Hermes → report to user
```

## Scale Stats
- 3 subagents, running in overlapping parallel
- ~60,000 input tokens total across all 3
- ~4 minutes wall-clock time
- 39 files created/modified across Phase 2
- 0 user corrections needed during dispatch
- All deliverables verified by parent after completion

## Lessons for Future Multi-Agent Dispatch

1. **Goal specificity matters** — every subagent should get: file paths, exact task list, design tokens, brand rules, and what NOT to do

2. **Media needs more context than marketing** — design tokens, SVG specs, CSS patterns, existing HTML structure. Marketing just needs brand voice + product info.

3. **Verify after dispatch** — subagent summaries are self-reports. Always re-read key files + test API endpoints.

4. **Order matters** — if agents modify the same file (e.g. index.html), parent should re-read before further edits. The note "subagent modified files the parent previously read" is a real risk.

5. **Media subagent → 46 API calls is normal** — SVG creation + CSS animations + HTML patches require many read/write cycles. Don't limit subagents too aggressively.

6. **Vietnamese content requirement** — must be explicit in context. Subagents default to English summaries. Specify language in every task's context.

7. **Severity bars color scheme** — đỏ 90%+ (danger), vàng 70-89% (warning), xanh 50-69% (ok). Match icon to paint point name via keyword mapping.
