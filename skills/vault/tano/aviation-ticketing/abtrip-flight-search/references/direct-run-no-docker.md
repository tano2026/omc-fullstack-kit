# Chạy agent.tkt trực tiếp không cần Docker

> Last verified: 2026-07-06

## Khi nào dùng

Khi Docker Desktop không có sẵn trên Windows (chưa cài, không trong PATH git-bash, hoặc Docker service không chạy).

## Port mapping (không Docker)

| Service | Docker port | Direct port | Ghi chú |
|---------|------------|-------------|---------|
| Backend (FastAPI) | 8765 (map 8000) | **8138** | Từ `.env` `BACKEND_PORT=8138`. `run.py` default=8137 nhưng .env override. |
| Frontend (Next.js) | 4321 (map 3000) | **4321** | `npx next dev -p 4321` |
| PostgreSQL | 5987 | ❌ Không cần | Backend không dùng DB trực tiếp |
| Redis | 7103 | ❌ Không cần | Optional, backend config `redis_url=""` |

## Các bước khởi động

### 1. Backend

```bash
cd ~/agent.tkt/backend
PORT=8138 python run.py
```

Backend tự load `.env` qua pydantic-settings. Health check:
```bash
curl http://localhost:8138/docs   # Swagger UI
```

### 2. Frontend

```bash
cd ~/agent.tkt/frontend
npx next dev -p 4321
```

### 3. Verify

```bash
curl -s http://localhost:4321 | head -5   # HTML response = OK
curl -s http://localhost:8138/docs | head -5   # Swagger = OK
```

## Pitfalls

### `close_llm` ImportError

```
ImportError: cannot import name 'close_llm' from 'app.services.llm_gateway'
```

**Nguyên nhân:** `main.py` line 25 import `close_llm` nhưng `llm_gateway.py` chưa định nghĩa hàm này.

**Fix:** Thêm stub vào cuối `backend/app/services/llm_gateway.py`:

```python
async def close_llm() -> None:
    """Close the LLM gateway (no-op for now)."""
    pass
```

### Port không khớp với docker-compose

Docker Compose map `8765:8000` (backend container port 8000 → host 8765).
Khi chạy trực tiếp, backend dùng `BACKEND_PORT` từ `.env` (8138), không phải 8765.
Frontend vẫn dùng 4321 như docker-compose.

### Docker không trong PATH git-bash

Trên Windows, Docker Desktop có thể không tự động thêm vào PATH của git-bash/MSYS.
Paths thường gặp: `C:\Program Files\Docker\Docker\resources\bin\docker.exe`.
Nếu không tìm thấy → chạy direct mode.
