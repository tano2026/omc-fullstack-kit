# pydantic-settings .env Gotchas

Các lỗi thường gặp khi dùng `pydantic-settings` (v2+) + `.env` trên Windows.

## 1. Quotes trong .env thành literal value

**Vấn đề:** pydantic-settings đọc `.env` literal — KHÔNG strip quotes.

```env
# ❌ SAI — AGT_API_HOST sẽ là '"https://api..."' (có quotes)
AGT_API_HOST="https://api-abtrip.timtrungtam.com/v1"

# ✅ ĐÚNG
AGT_API_HOST=https://api-abtrip.timtrungtam.com/v1
```

Triệu chứng: `getaddrinfo failed` vì URL có dấu `"` ở đầu/cuối.

## 2. lru_cache trên get_settings()

pydantic-settings dùng `@lru_cache()` trên `get_settings()` — settings chỉ load **1 lần** mỗi process.

```python
@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

Triệu chứng: sửa `.env` xong restart backend, vẫn dùng giá trị cũ → kill process cũ hoàn toàn (taskkill /F) trước khi chạy lại.

## 3. async close functions trong lifespan

Khi viết `lifespan` context manager trong FastAPI, shutdown handler await tất cả close functions. Nếu một function không phải async, lỗi `'NoneType' object can't be awaited`:

```python
# ❌ SAI — không await được
def close_llm():
    global _gateway; _gateway = None

# ✅ ĐÚNG
async def close_llm():
    global _gateway; _gateway = None
```

## 4. Backend chết nhưng health check vẫn OK

Port bị process cũ giữ → uvicorn mới crash, nhưng health check (`/api/health`) vẫn 200 vì hit vào process cũ.
Fix: luôn check netstat + kill hết PID trước khi start.

```bash
netstat -ano | grep ":8137 " | grep LISTENING
taskkill //F //PID <PID>
```
