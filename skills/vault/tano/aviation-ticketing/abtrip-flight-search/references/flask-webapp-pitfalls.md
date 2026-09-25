# Flask Webapp Pitfalls (flight-booking-webapp)

Kiến trúc và lỗi thường gặp khi chạy Flask webapp kết hợp Playwright Booking + Watcher API.

## Server Location

```
http://192.168.1.253:5000
```

## Import Rules

`app.py` nằm trong `flight-booking-webapp/` cùng cấp với `watcher_api/` và `watcher_scraper/`:

```python
# ✅ Đúng — import trực tiếp, không prefix
from checker_manager import create_watcher, list_watchers, run_check, WatcherScheduler
from api_checker import check_route as api_check_route, check_flight_condition
from scraper_manager import execute_booking_sync, list_previous_bookings

# ❌ Sai — ModuleNotFoundError
from watcher_api.checker_manager import create_watcher
```

Lý do: `app.py` không chạy từ package context, Python không tìm thấy đường dẫn `watcher_api.*`.

## Debug Mode + Playwright = Crash

**Triệu chứng:** Server đang chạy debug mode, gọi `/api/book` → Playwright khởi tạo browser → Flask reloader restart process → Playwright session bị kill → crash.

**Fix:** 
- Chạy `python app.py` (không `--debug`) khi cần dùng Playwright booking
- Hoặc set `app.run(debug=True, use_reloader=False)` — không lý tưởng
- Recommended: dùng 2 instance — 1 dev (debug) + 1 production (no debug)

## Duplicate Endpoint Error

**Error:**
```
AssertionError: View function mapping is overwriting an existing endpoint function: api_watcher_worker_stop
```

**Cause:** Copy-paste route decorator tạo ra 2 function cùng tên. Flask tự động đặt endpoint name = function name, không cho phép overwrite.

**Fix:**
```bash
# Kiểm tra trên disk (không chỉ session cache)
grep -n "def api_watcher_" app.py
# Nếu thấy 2 dòng giống nhau, xóa 1
```

**Context compaction trap:** Khi làm việc với context compaction, file hiển thị trong session có thể KHÁC file thật trên disk. Nếu `grep` chỉ thấy 1 dòng mà Flask vẫn báo lỗi → đã có thay đổi file giữa session cache và disk. **Luôn chạy grep trực tiếp trên file để verify.**

## Watcher Field Mapping

App có 2 "view" của watcher data:

| Layer | Field Names |
|-------|-------------|
| Frontend (UI form) | `start`, `end`, `type` |
| Backend (backend API) | `from`, `to`, `monitor_type` |
| Backend (create_watcher) | `from`, `to`, `monitor_type` |

Route `/api/watcher/create` trong `app.py` phải map thủ công:
```python
@app.route('/api/watcher/create', methods=['POST'])
def api_watcher_create():
    data = request.json
    # Map frontend fields to backend
    if 'start' in data and 'from' not in data:
        data['from'] = data.pop('start')
    if 'end' in data and 'to' not in data:
        data['to'] = data.pop('end')
    if 'type' in data and 'monitor_type' not in data:
        data['monitor_type'] = data.pop('type')
    return create_watcher(data)
```

## WatcherScheduler API

```python
from checker_manager import WatcherScheduler

scheduler = WatcherScheduler()
scheduler.start()           # ✅ start worker (mặc định 600s interval)
# scheduler.start(interval_seconds=600)  # ❌ KHÔNG hỗ trợ args

scheduler.running           # ✅ property bool
scheduler.stop()            # ✅ stop worker
```

Lưu ý: `start()` không nhận `interval_seconds` argument. Interval mặc định là 600s (10 phút). Nếu cần custom interval, sửa trong `WatcherScheduler.__init__` hoặc set attribute trước khi start.

## Worker Start/Stop Routes

```python
# ✅ Working — 2 routes riêng biệt
@app.route('/api/watcher/worker/start', methods=['POST'])
def api_watcher_worker_start():
    scheduler.start()
    return jsonify({"success": True, "message": "Worker started"})

@app.route('/api/watcher/worker/stop', methods=['POST'])
def api_watcher_worker_stop():         # ← function name must be UNIQUE
    scheduler.stop()
    return jsonify({"success": True, "message": "Worker stopped"})
```

Không copy-paste function name. Mỗi route 1 function name riêng.

## Natural Language Search

Route `/api/search` dùng Playwright (`abtrip_browser.py`) để search thật.
Route `/api/tim-chuyen` dùng API B2B để search test.

```python
# Playwright search — nhận query tự nhiên
POST /api/search
{"query": "Sài Gòn đi Hà Nội 12/6"}

# API B2B search — nhận từng field
POST /api/tim-chuyen
{"from": "SGN", "to": "HAN", "date": "12062026"}
```

Natural language query được parse bởi `parse_search_query()` trong `app.py` (không phải NLP — chỉ regex đơn giản tìm 3 airport codes + date).

## Watcher Persistence

- JSON files in `watchers/` directory at project root
- Each watcher = 1 file named `{watcher_id}.json`
- **Survives server crash + restart** — verified: 4 watchers persisted after process crash
- Trigger files saved by `scraper_manager` in `triggers/`
- Booking results saved in `bookings/`

## Route /api/watcher/get/<id> — Method

The route is defined as:
```python
@app.route('/api/watcher/get/<watcher_id>', methods=['GET'])
```
Test with:
```bash
curl "http://localhost:5000/api/watcher/get/watcher_xxx"
```

## Quick Start After Crash

```bash
cd D:/AI Store/Hermes Agent/flight-booking-webapp
# Check port
netstat -ano | findstr :5000
# Kill if needed
taskkill /F /PID <pid>
# Start — NO debug mode
python app.py
# Verify
curl http://localhost:5000/api/status
# → {"status": "ok", "watcher_worker": true}
# Start worker
curl -X POST http://localhost:5000/api/watcher/worker/start
```
