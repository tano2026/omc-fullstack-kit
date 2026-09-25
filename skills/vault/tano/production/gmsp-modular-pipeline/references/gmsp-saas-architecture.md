# GMSP SaaS Architecture

## Khi nào dùng
Cần gói pipeline GMSP thành web dashboard để quản lý sản xuất nội bộ, hoặc chuẩn bị thương mại hoá (SaaS).

## Triết lý
- **MVP nội bộ trước, bán sau** — dựng cái xài được trong 2 ngày, không over-engineer
- **Tận dụng pipeline có sẵn** — backend gọi script Python, ko viết lại pipeline
- **Kiến trúc đủ lỏng để mở rộng** — Streamlight → Next.js, SQLite → PostgreSQL, single user → multi-user

## Stack

| Layer | Công nghệ | $ | Ghi chú |
|-------|-----------|:-:|---------|
| Backend API | FastAPI (Python) | $0 | Tận dụng pipeline script |
| Frontend | Streamlit (MVP) → Next.js (sau) | $0 | Streamlit nhanh, Next.js đẹp |
| Queue | FastAPI BackgroundTasks hoặc Celery | $0 | BackgroundTasks cho MVP |
| DB | SQLite (SQLAlchemy) | $0 | Lên PostgreSQL sau |
| Storage | Local + Google Drive backup | $0 | |
| Host | VPS Ubuntu (Docker Compose) hoặc local | $0 | Dùng VPS có sẵn |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/projects` | Tạo project mới |
| GET | `/api/projects` | Danh sách project |
| GET | `/api/projects/{id}` | Chi tiết project + steps |
| POST | `/api/projects/{id}/run/{step}` | Chạy 1 step trong pipeline |
| GET | `/api/projects/{id}/steps/{step}` | Trạng thái step |
| GET | `/api/knowledge` | Kho kiến thức (từ kho-thuat-dinhluat-tamly.md) |

## Pipeline Engine

Mỗi step là 1 script Python riêng, gọi qua subprocess:

```python
STEPS_MAP = {
    "research": "pipeline/01_research.py",
    "script":   "pipeline/02_content.py",
    "tts":      "pipeline/03_tts.py",
    "media":    "pipeline/04_media.py",
    "render":   "pipeline/05_render.py",
    "publish":  "pipeline/06_publish.py",
}
subprocess.run(["python", script_path, "--project", str(project_id)], cwd=BASE_DIR)
```

Chạy async (BackgroundTasks hoặc Celery) — không block UI.

## Cấu trúc thư mục

```
GMSP-SAAS/
├── backend/
│   ├── main.py          # FastAPI app
│   └── (models, routers)
├── frontend/
│   └── app.py           # Streamlit app
├── ARCHITECTURE.md      # Full thiết kế
└── start.bat            # Bấm đúp chạy cả 2
```

## Lộ trình mở rộng

| Phase | Nội dung | Thời gian |
|-------|----------|-----------|
| **1** MVP | Streamlit + FastAPI: tạo project, chạy pipeline, xem log | 2 ngày ✅ |
| **2** Đẹp | Next.js frontend + script editor + kho kiến thức visual | 5 ngày |
| **3** Preview | Nghe TTS trước render, xem media trước ghép | 2 ngày |
| **4** Auth | Multi-user + phân quyền | 3 ngày |
| **5** Billing | Stripe + gói $29/tháng, $5/video | 5 ngày |

## Files
- `D:\MMO Du an\GMSP-SAAS\backend\main.py` — FastAPI app (port 8137)
- `D:\MMO Du an\GMSP-SAAS\frontend\app.py` — Streamlit frontend (port 8138)
- `D:\MMO Du an\GMSP-SAAS\start.bat` — launch cả 2
