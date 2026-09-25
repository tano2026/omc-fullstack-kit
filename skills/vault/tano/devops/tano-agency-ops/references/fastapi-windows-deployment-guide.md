---
name: fastapi-windows-deploy
description: "Deploy và troubleshoot FastAPI app trên Windows (Python 3.14+), bao gồm template engine workaround, port management, background process."
category: devops
---

# FastAPI Windows Deploy

Trigger: user muốn chạy FastAPI app trên Windows, template error, port conflict, background process.

## Steps

### 1. Start server
```bash
cd /d/path/to/project
python backend/main.py
```
Or double-click `.bat` file.

### 2. Test
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT/
```

## Python 3.14 + Jinja2/Starlette Bug Workaround

**Symptom:** `TypeError: cannot use 'tuple' as a dict key (unhashable type: 'dict')` khi gọi `TemplateResponse()`.

**Root cause:** Jinja2 >= 3.2 + Python 3.14 conflict trong `jinja2.utils.py:515` — `cache.get()` dùng `dict` key không hash được.

**Fix:** Bỏ `Jinja2Templates` hoàn toàn, đọc file HTML thay thế:

```python
from fastapi.responses import HTMLResponse

TEMPLATES_DIR = SAAS_DIR / "templates"

def render(name: str, request: Request = None, **extra) -> HTMLResponse:
    path = TEMPLATES_DIR / name
    html = path.read_text(encoding="utf-8") if path.exists() else f"<h1>Template '{name}' not found</h1>"
    return HTMLResponse(content=html)

# Use in routes:
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return render("index.html", request=request)
```

**Note:** `cache_size=0` trong `Jinja2Templates` không được support. Override `get_template()` cũng không fix được.

## Port Management on Windows

**Kill process on port:**
```bash
# Find PID
netstat -ano | grep ":PORT" | grep LISTEN

# Kill (git-bash/MSYS — dùng cmd //c)
cmd //c "taskkill /F /PID XXXX"

# Verify freed
netstat -ano | grep ":PORT" | grep LISTEN || echo "FREE"
```

**Note:** `kill -9 PID` không work trên MSYS/git-bash Windows — luôn dùng `taskkill /F`.

### Port TIME_WAIT trap

After killing a process, the port may stay in `TIME_WAIT` state for 2+ minutes:
```
TCP    127.0.0.1:8137   127.0.0.1:52912   TIME_WAIT       0
```
Your new process will fail with `[Errno 10048] error while attempting to bind on address`.

**Solutions (in order of preference):**
1. **Wait** — 2 minutes, then start again
2. **Change port** — if you can, just use a different port immediately
3. **Reuse address** — in uvicorn: `uvicorn.run(app, host="0.0.0.0", port=PORT, reuse_address=True)` (may not work on Windows)

**Kill sequence that WORKS in git-bash:**
```bash
# 1. Find the LISTENING PID
netstat -ano | grep ":8137 " | grep LISTEN

# 2. Kill via cmd.exe (git-bash's taskkill often fails)
cmd.exe /c "taskkill /F /PID <PID>"

# 3. Or via PowerShell
powershell -NoProfile -Command "Stop-Process -Id <PID> -Force"

# 4. After kill, TIME_WAIT remains — either wait or change port
```

### __pycache__ stale code trap

On Windows, after editing a FastAPI app file (`app.py`), the running process may continue serving old code because `__pycache__` holds `.pyc` files compiled before the edit. Even killing and restarting doesn't help if you're running from a different shell that creates a new cache.

**Fix:**
```python
import shutil, os
root = "D:/path/to/project"
for dirpath, dirs, _ in os.walk(root):
    if '__pycache__' in dirs:
        shutil.rmtree(os.path.join(dirpath, '__pycache__'))
```

### Which Python to use (Hermes venv vs system)

On Windows with Hermes installed:
- **System `python`** (e.g. C:\\Python314\\python.exe) — may or may NOT have fastapi/uvicorn
- **Hermes venv** (`C:\\Users\\<user>\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe`) — HAS fastapi installed

**Prefer Hermes venv for most cases:**
```python
HERMES_PY = r"C:\\Users\\Nguyen Ngoc Tan\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe"
p = subprocess.Popen([HERMES_PY, 'dashboard/app.py'], cwd=root)
```

**But global Python is OK when Hermes venv uvicorn fails** (module import errors). Tested on ABTrip Phase 1 (July 2026): `python -m uvicorn app.main:app --host 0.0.0.0 --port 6969` works fine with global Python because all ABTrip deps are installed globally. Choose the Python that can `import fastapi` — not forced to Hermes venv.

To find which Python has fastapi:
```bash
python -c "import fastapi; print(fastapi.__file__)"  # if found → use this python
# Or check known venv paths
```

## Background Process

```bash
# Start in background
cd /d/path && python backend/main.py &
disown
```

## Static Files

Mount AFTER web routes để tránh catch-all:
```python
app.mount("/static", StaticFiles(directory=str(PROJECT_DIR / "static")), name="static")
```

## Pitfalls

- **`uvicorn` lỗi `Could not import module` (chạy sai thư mục):** Xảy ra khi chạy `uvicorn main:app` từ thư mục cha hoặc thư mục khác mà không phải thư mục chứa `main.py`.
  **Fix:** Luôn `cd` vào thư mục chứa `main.py` (ví dụ: `cd D:\path\to\project\backend\app`) trước khi chạy `uvicorn main:app --reload --port <PORT>`.

- **Lệnh `cd` với đường dẫn có khoảng trắng trong PowerShell:** `Set-Location : A positional parameter cannot be found that accepts argument 'Du'.`
  **Fix:** Luôn đặt đường dẫn trong dấu ngoặc kép: `cd "D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip\backend\app"`.

- **`read_file` không trả `content` khi file `unchanged`:** Khi `read_file` trả về `{"status": "unchanged", ...}` thay vì `{"content": "...", ...}`, việc truy cập `response["content"]` sẽ gây `KeyError`.
  **Fix:** Kiểm tra sự tồn tại của key `content` trực tiếp: `if "content" in response: content = response["content"]`.

## Advanced HTML/CSS Refactoring with `execute_code`

Khi `patch` tool gặp khó khăn với các thay đổi lớn, phức tạp, hoặc `old_string` không duy nhất (do bị trùng lặp, hoặc các thay đổi liên tiếp làm lệch match), `execute_code` kết hợp với `re.sub` (Python regex) là một giải pháp mạnh mẽ để thực hiện các chuyển đổi HTML/CSS quy mô lớn.

### Workflow:

1.  **Đọc toàn bộ file:** Dùng `read_file` để lấy toàn bộ nội dung HTML/CSS.
2.  **Sử dụng `re.sub` với `re.DOTALL`:** Để thay thế các khối HTML/CSS lớn. `re.DOTALL` cho phép `.` khớp với cả ký tự xuống dòng, rất hữu ích cho các khối đa dòng.
    *   **Cẩn thận với Regex:** Luôn kiểm tra regex của bạn.
    *   **Thoát ký tự đặc biệt:** Cẩn thận thoát các dấu ngoặc kép (`"`), dấu gạch chéo ngược (`\\`), và các ký tự regex đặc biệt khác trong chuỗi Python của bạn.
3.  **Tái cấu trúc HTML/CSS trong Python:** Xây dựng các chuỗi HTML/CSS mới và sử dụng `replace` hoặc `re.sub` để chèn/thay thế chúng.
4.  **Ghi lại toàn bộ file:** Dùng `write_file` để lưu nội dung đã chỉnh sửa trở lại.

**Ví dụ:** Thay thế toàn bộ khối `<style>`:
```python
style_block_match = re.search(r'(<style>.*?<\/style>)', content, re.DOTALL)
if style_block_match:
    old_style_block = style_block_match.group(0)
    new_style_css = """
    /* Your new CSS here */
    """
    content = content.replace(old_style_block, f"<style>{new_style_css}</style>")
```

**Ví dụ:** Di chuyển và thay thế khối HTML lớn:
```python
# Extract the block to move
services_grid_match = re.search(r'(<div class="services-grid">.*?<\/div>)', content, re.DOTALL)
if services_grid_match:
    services_html = services_grid_match.group(0)
    content = content.replace(services_html, "") # Remove from original location

# Insert into new location (e.g., inside header)
header_end_tag_match = re.search(r'(<\/header>)', content, re.DOTALL)
if header_end_tag_match:
    new_header_content = f"{header_end_tag_match.group(0)}\n<!-- New services here -->\n{services_html}"
    content = content.replace(header_end_tag_match.group(0), new_header_content)
```


- `Jinja2Templates` + `HTMLResponse`: routes cần `response_class=HTMLResponse`.
- Static mount sau route là mandatory.
- `uvicorn --reload` không detect template changes với `read_text()` — restart manual.
- `kill -9` không chạy trên Windows/msys — dùng `taskkill /F`.
- **`uv pip install` false positive:** On Windows, `uv pip install` with piped output (`| tail`) triggers "long-lived server" detection. Use `python -m uv pip install` or pip directly. For `| tail` style, leave pipe out or use 2>&1 first.
- **Missing `aiosqlite`:** Not in stdlib. Install with `pip install aiosqlite` when adding async SQLAlchemy with SQLite.
- **`Settings.db_path` missing:** When adding a new async SQLite service, don't reference `settings.db_path` — ABTrip doesn't have it. Create `data/` dir with `os.makedirs()` and store DB there.
