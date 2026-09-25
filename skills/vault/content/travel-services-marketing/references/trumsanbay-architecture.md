# Trùm Sân Bay — Architecture Reference

> Extracted from standalone repo at `D:\MMO Du an\Trum Du Lich\`
> Cập nhật: 19/07/2026

## Kiến trúc Tổng Quan

```
Nobitano → Telegram → OpenClaw
                         ↓
             Content Orchestrator (Hermes)
             ├── Ideation Agent     → lên ý tưởng theo pillar + lịch
             ├── Writer Agent       → viết caption đúng tone + fact-check
             ├── Visual Agent       → gen ảnh/video (Gemini free tier / HyperFrames)
             ├── Adapter Agent      → adapt format từng platform
             ├── Review Queue       → đẩy vào Airtable, notify Telegram
             └── Publisher Agent    → post qua API từng platform
                         ↓
             Comment Monitor (định kỳ)
             └── Reply Agent        → draft reply, queue chờ approve
```

## Funnel Content
- **TOFU** (60%) — Tips miễn phí, cảnh báo, hướng dẫn
- **MOFU** (25%) — So sánh dịch vụ, case study, review
- **BOFU** (15%) — Promote Fast Track / SIM / đổi tiền

## Key Files in Repo

| File | Kích thước | Vai trò |
|------|-----------|---------|
| `agent.py` | 28.8 KB (710 dòng) | Pipeline agent — API call, Airtable, LLM, publish |
| `orchestrator.py` | 32.6 KB (651 dòng) | NÃO THẬT — ghép 9 agent thành pipeline |
| `system-prompt.md` | 4.7 KB | Persona prompt — nhân viên sân bay kỳ cựu |
| `ARCHITECTURE.md` | 6.1 KB | Sub-agent chi tiết + platform format |
| `HARNESS.md` | 13.8 KB | 3 trụ: context, constraints, entropy |
| `DEV-SKILLS.md` | 2.8 KB | Dev skills guide cho repo này |

## Pipeline Commands

```bash
python3 orchestrator.py weekly       # Full pipeline: research → ideation → writer → visual → brand check
python3 orchestrator.py comments     # Fetch + classify + draft reply comment mới
python3 orchestrator.py token_check  # Health check token, tự refresh nếu cần
```

## Trạng Thái Thật (đã cập nhật)

- ✅ `run_visual_agent_image()` gọi Gemini image gen thật (`gemini-2.5-flash-image`, free tier)
- ✅ `fetch_all_comments()` đã code đủ 4 platform
- ⚠️ Brand Check chạy nhưng ảnh chưa có logo/watermark tự động
- ⚠️ Gemini free tier rate limit ~15 req/phút
- ⚠️ Toàn bộ code compile sạch nhưng CHƯA chạy với credential thật

## Tek Stack

| Component | Công nghệ |
|-----------|----------|
| Orchestrator | Hermes (Python, urllib) |
| Gateway | OpenClaw (Node.js, Telegram bot) |
| Workflow | n8n (port 5678) |
| Queue/CMS | Airtable |
| Visual gen | Gemini 2.5 Flash Image / HyperFrames |
| Video render | ffmpeg |
| Storage | Local VPS /opt/trum-san-bay/assets/ |

## Import Status

Repo đã import vào TANO-AGENCY CLIENTS structure:
- `D:\MMO Du an\TANO-AGENCY\CLIENTS\TRUM-DU-LICH\` — README.md (pending strategy decision)
- Cần quyết định: standalone brand hay gộp sub-brand dưới ABTrip?
