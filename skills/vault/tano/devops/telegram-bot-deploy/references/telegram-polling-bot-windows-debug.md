# Telegram Polling Bot — Windows Silent Killers Debug Guide

Dựa trên session thực tế 2026-07-18: debug một CEO bot Telegram chạy polling loop, không bao giờ nhận được message từ user.

## Các silent killer đã gặp

### 1. emoji trong print() crash trên Windows cp1252

**Triệu chứng:** Bot chạy 2-3 giây rồi tắt, không có log lỗi rõ ràng. Chạy với `PYTHONUNBUFFERED=1` mới thấy `UnicodeEncodeError` về codec cp1252.

**Nguyên nhân:** Windows console mặc định dùng cp1252 encoding. Emoji (🧠, 🎯, ✅, etc.) trong `print()` không encode được → crash Python.

**Fix:**
```python
# Option A: reconfigure stdout
import sys, io
sys.stdout.reconfigure(encoding='utf-8')  # Python 3.7+

# Option B: Remove emoji from ALL print() statements
print("[CEO] Bot dang chay...")         # ✅
print("🧠 Bot chay...")                   # ❌ crash

# Option C: Environment variable
# set PYTHONIOENCODING=utf-8
# set PYTHONUNBUFFERED=1
```

**Quan trọng:** Emoji trong Telegram API message text (qua wire) vẫn hoạt động bình thường. Chỉ `print()` ra terminal mới crash.

### 2. 401 Unauthorized — token hết hạn

**Triệu chứng:** Bot vẫn chạy (process alive) nhưng không nhận message. Error trong log nếu PYTHONUNBUFFERED=1: `telegram.error.Unauthorized: 401`.

**Debug:**
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getMe" | python -c "import json,sys; d=json.load(sys.stdin); print('OK' if d.get('ok') else d.get('description','FAIL'))"
```

**Fix:** Tạo token mới từ @BotFather → `/mybots` → chọn bot → `/revoke`

### 3. 409 Conflict — duplicate polling instance

**Triệu chứng:** Khi dùng `getUpdates`, trả về 409 Conflict. Bot process cũ vẫn đang poll với cùng token.

**Nguyên nhân:** Telegram chỉ cho phép 1 polling connection/token. Process cũ (zombie từ terminal background) vẫn giữ kết nối.

**Fix:** Kill stale Python processes:
```bash
# Liệt kê tất cả python.exe
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select-Object ProcessId, CommandLine"

# Kill những process liên quan (double slash cho MSYS)
taskkill //F //PID <PID>
# Hoặc từ MSYS:
kill -9 <PID>
```

**Nguyên nhân root:** MSYS/bash wrapper (từ terminal(background=true)) chết (exit code -15) nhưng python.exe con vẫn sống → zombie bot.

### 4. Timeout silent drop — urllib timeout ≤ poll timeout

**Triệu chứng:** Bot process chạy ổn (không crash), không lỗi gì, process alive — nhưng không bao giờ nhận message từ user.

**Nguyên nhân:** Telegram long-poll giữ kết nối 30s. Nếu `urllib.urlopen(timeout=35)` timeout cũng ~30s, request đóng đúng lúc Telegram trả response → mất message. **Lỗi này silent — không có exception, không có log.**

**Fix:**
```python
# ❌ Gây mất message:
urllib.request.urlopen(req, timeout=35)

# ✅ Luôn dùng timeout lớn hơn poll timeout (tối thiểu 60, khuyến nghị 180):
urllib.request.urlopen(req, timeout=180)
```

**Debug:** Thêm `print(f"[tg] {method} -> ok={r.get('ok')} results=...")` trong hàm tg() — nếu có log `getUpdates -> ok=True results=0` hoặc `results=1` là loop hoạt động. Nếu không có log nào → timeout silent drop.

## Startup Verification Checklist

Sau mỗi lần restart bot, verify theo thứ tự:

### Step 1: Check process alive
```bash
process(action="poll", session_id="proc_xxx")  # nếu từ Hermes
# hoặc
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select-Object ProcessId, CommandLine" | grep bot_name
```

### Step 2: Check token validity
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getMe" | python -c "import json,sys; d=json.load(sys.stdin); print('OK' if d.get('ok') else d.get('description'))"
```

### Step 3: Check polling (no conflict)
```bash
# Dùng short timeout request riêng (process đang poll sẽ ko ảnh hưởng nếu dùng getMe trước)
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates?offset=0&timeout=2" | python -c "import json,sys; d=json.load(sys.stdin); print('Polling OK' if d.get('ok') else 'Conflict: ' + d.get('description','?'))"
```

### Step 4: Send test message + watch log
```bash
tail -f bot.log | head -20
# Gửi 1 tin nhắn từ Telegram vào bot → kiểm tra log có receive không
```

### Step 5: Verify no emoji in print()
```bash
grep -n "print.*["'"'"'🧠🎯✅🔒🟢🔴⭐💡📊📋🪐🏆]" bot.py
# Nếu có match → fix trước khi chạy tiếp
```

## Background Process Architecture on Windows

```
Hermes process(action="poll")
  │
  ▼
bash.exe (MSYS) ─── PID 12345  ← Hermes tracks this as "process"
  │
  ▼
python.exe bot.py ── PID 67890  ← Actual bot process (real PID)
  │
  ▼
urllib HTTPS ─── Telegram API (holds polling connection)

Tình huống chết khó phát hiện (đã xảy ra thực tế):
1. bash.exe chết (exit -15/SIGTERM) → Hermes process(action="poll") báo "dead"
2. python.exe bot.py VẪN SỐNG → tiếp tục poll Telegram
3. Muốn chạy bản mới → 409 Conflict vì python.exe zombie

Fix: Luôn kill python.exe riêng, không chỉ dựa vào Hermes process tool.
```

## Self-Learning Hook Points

Khi tích hợp learning vào polling bot, hook 3 chỗ:
1. `run_agent()` — sau Harness kết thúc, ghi observation
2. `cmd_natural()` — sau CEO dispatch, ghi observation
3. `handle()` — trước khi xử lý, detect correction keywords

Detail: xem `multi-agent-platform` skill, section "Self-Learning Engine".
