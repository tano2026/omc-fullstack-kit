# Dashboard v2 — SPA Mobile-First 4 Tab (+ Chat tab thứ 5)

## Kiến trúc

```
dashboard/
  app.py          # FastAPI backend — 14 API endpoints, raw Jinja2, localStorage auth
  templates/
    dashboard.html # Single-page SPA, 5-tab bottom nav, dark theme
```

API login: POST /login (accepts JSON + form data).

## So với v1 (cũ)

| | v1 (cũ) | v2 (mới) |
|---|---------|----------|
| Auth | login.html riêng + session | localStorage token + 1 template |
| Jinja2 | `Jinja2Templates` class | Raw `Environment` + `FileSystemLoader` |
| Tabs | 7 (Chat, Health, Kanban, Tickets, Outbox, Agents, Văn Phòng) | 5 (Tổng Quan, Phòng Ban, Văn Phòng, Tasks, Chat) |
| Data source | `from real_adapters import ...` — phụ thuộc agents | SQLite trực tiếp + PowerShell + os.path — độc lập |
| API endpoints | 15+ | 14 |
| Health | `_wmic_full()` | `subprocess.run(['powershell', ...])` |

## Web Chat (tab Chat thứ 5)

Thêm năm 2026-07-18: dashboard có tab Chat thứ 5 để chat CEO trên web thay vì Telegram.

**Frontend:** `dashboard.html` — tab #tab-chat với:
- Chat bubble: user msg gold bg right-aligned, CEO reply card bg left-aligned
- Input bar fixed bottom: text input + "Gửi" button, Enter key submit
- Loading indicator 3-dot bounce animation
- Initial message: "Chào chủ tịch! Em là CEO TANO-AGENCY..."
- Tab lazy-loaded once (loadedTabs.chat flag)

**Backend:** `POST /api/chat` in `app.py`:
- Accepts JSON `{message: "..."}`
- Calls `core.llm.chat()` trực tiếp — 1 LLM call, ko Harness, ko pipeline
- System prompt: "CHỈ TRẢ LỜI. KHÔNG dispatch. Khi chủ tịch nói 'bắt đầu' thì mới giao việc"
- Returns `{ok: true, response: "...", time_ms: 123}`
- Timeout 30s, max_tokens 1000

**Khác biệt so với Telegram bot:**
- Web chat dùng API endpoint POST /api/chat, ko polling loop, ko outbox
- System prompt GIỐNG Telegram bot (main.py cmd_natural) — đồng nhất hành vi
- Web chat ko có "/" commands — chỉ chat thuần
- Web chat hiển thị thời gian response (time_ms)

## API endpoints

| Endpoint | Method | Trả về |
|----------|--------|--------|
| `/` | GET | HTML dashboard SPA |
| `/login` | POST | `{ok: true/false}` — accept Form hoặc JSON |
| `/api/health` | GET | `{cpu, ram, disk_c, disk_d, python_processes, timestamp}` — từ PowerShell |
| `/api/projects` | GET | `[name, icon, status, path]` — từ os.path.isdir |
| `/api/kanban_summary` | GET | `{states: {state: count}, total}` — từ agent_kankan.db |
| `/api/kanban` | GET | `[card, ...]` — SQLite kanban cards |
| `/api/tickets_summary` | GET | `{states: {status: count}, total}` — từ tickets.db |
| `/api/tickets` | GET | `[ticket, ...]` — SQLite tickets |
| `/api/agents` | GET | `[{name, icon, label, tasks}]` — từ memory DBs |
| `/api/learning` | GET | `{observations, instincts}` — từ learning.db |
| `/api/outbox` | GET | `{files: [name, size, modified]}` — từ ~/.hermes/outbox |
| `/api/kanban/add` | POST | `{ok: true}` — insert kanban card |
| `/api/kanban/move` | POST | `{ok: true}` — update kanban state |
| `/api/chat` | POST | `{ok: true, response: "...", time_ms: 123}` — chat với CEO gọi LLM trực tiếp |

## Data source pattern

```python
# SQLite trực tiếp — không qua agents
def query_db(path, sql):
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(sql)
        rows = [dict(r) for r in cur.fetchall()]
        return rows
    finally:
        conn.close()

# Health — PowerShell
def get_health_powershell():
    r = subprocess.run([
        "powershell", "-Command",
        "(Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average"
    ], capture_output=True, text=True, timeout=8)
    return r.stdout.strip()
```

## Template structure (dashboard.html)

```html
<!DOCTYPE html>
<html>
<head> <!-- Dark theme CSS inline --> </head>
<body>
<div id="login-screen">...</div>
<div id="app" style="display:none">
  <div id="tab-tongquan" class="tab-content active">...</div>
  <div id="tab-phongban" class="tab-content">...</div>
  <div id="tab-vanphong" class="tab-content">...</div>
  <div id="tab-tasks" class="tab-content">...</div>
  <div id="tab-chat" class="tab-content">...</div>
  <nav id="bottom-nav">
    <button data-tab="tongquan">🏠 Tổng Quan</button>
    <button data-tab="phongban">🧠 Phòng Ban</button>
    <button data-tab="vanphong">🏢 Văn Phòng</button>
    <button data-tab="tasks">📋 Tasks</button>
    <button data-tab="chat">💬 Chat</button>
  </nav>
</div>
<script>
  // localStorage auth
  // fetch API => render
  // bottom nav tab switching
  // Chat: sendChat() -> POST /api/chat -> append bubbles
</script>
</body>
</html>
```

## Auth pattern

```javascript
// Login
fetch('/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({password: pw})
}).then(r => r.json()).then(d => {
  if (d.ok) { localStorage.setItem('auth', '1'); showApp(); }
});

// No backend session — just localStorage check on load
if (localStorage.getItem('auth')) showApp();
```

**Note:** Ko có session trên backend. Login chỉ kiểm tra password, trả ok/error. Client tự nhớ qua localStorage.

## Pitfalls

1. **Login form-data vs JSON**: Frontend gửi JSON, test client gửi form-data — handler phải accept cả 2 (try JSON → fallback form)
2. **Chat response hiển thị**: Response CEO có thể dài > 4096 chars → nên truncate + "Xem thêm" nếu cần
3. **Chat API timeout**: LLM call có thể timeout 30s — frontend nên show "CEO đang suy nghĩ..." + disable input
4. **Web chat ≠ Telegram**: Web chat ko lưu history, ko outbox, ko cron — refresh page mất chat
