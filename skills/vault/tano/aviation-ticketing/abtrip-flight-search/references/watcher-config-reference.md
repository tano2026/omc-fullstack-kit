# Watcher Configuration Quick Reference

## Watcher JSON Schema

```json
{
  "watcher_id": "watcher_<unix_timestamp>_<random>",
  "name": "Tên gợi nhớ",
  "created_at": "2026-06-12T11:30:00",
  "updated_at": "2026-06-12T11:30:00",
  "active": true,
  "interval_minutes": 10,
  "monitor_type": "availability | price",
  "route": {
    "from": "HAN",
    "to": "SGN",
    "date": "30062026"
  },
  "passengers": {
    "adults": 1,
    "children": 0,
    "infants": 0
  },
  "conditions": {
    "min_availability": 1,
    "max_price": null
  },
  "target_flight": null,
  "triggered": false,
  "triggered_at": null,
  "last_check": null,
  "last_result": null,
  "history": []
}
```

## Storage

- **JSON files** in `watchers/` directory at project root
- Each watcher = 1 file named `{watcher_id}.json`
- **Trigger files** saved by scraper_manager in `triggers/`
- **Booking results** saved in `bookings/`

## API Endpoints (Flask)

**Base URL**: `http://192.168.1.253:5000`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/status` | Server health check |
| POST | `/api/search` | Search flights via API B2B |
| POST | `/api/book` | Book via Playwright scraper |
| GET | `/api/watcher/list` | List all watchers |
| POST | `/api/watcher/create` | Create watcher (JSON body) |
| GET | `/api/watcher/get/<id>` | Get watcher details |
| POST | `/api/watcher/delete/<id>` | Delete watcher |
| POST | `/api/watcher/check-now/<id>` | Force-check single watcher |
| POST | `/api/watcher/check-flights` | Check all active watchers |
| POST | `/api/watcher/worker/start` | Start background scheduler |
| POST | `/api/watcher/worker/stop` | Stop background scheduler |
| POST | `/api/trigger/book` | Trigger booking via scraper |
| GET | `/api/trigger/logs` | Get trigger history |

**Watcher create payload (required fields)**:
```json
{
  "from": "HAN", "to": "SGN", "date": "12062026",
  "monitor_type": "availability",  // or "price"
  "min_availability": 1,
  "max_price": null,
  "interval": 10
}
```

## CRUD from Python

```python
from checker_manager import (
    create_watcher,
    get_watcher,
    update_watcher,
    delete_watcher,
    list_watchers,
    run_check,
    WatcherScheduler,
)
from api_checker import check_route

# Create (note: import directly, not from watcher_api.xxx)
w = create_watcher({
    'name': 'Test route',
    'from': 'HAN', 'to': 'SGN', 'date': '30062026',
    'monitor_type': 'price',          # REQUIRED field!
    'max_price': 2000000,
    'min_availability': None,
    'interval_minutes': 10,
})

# Check
result = run_check(w['watcher_id'])

# Scheduler
scheduler = WatcherScheduler()
scheduler.start(interval_seconds=600)  # every 10 min
# scheduler.running → True/False
# scheduler.stop()

# Delete
delete_watcher(w['watcher_id'])
```

# Check
result = run_check(w['watcher_id'])

# Delete
delete_watcher(w['watcher_id'])
```

## CLI Testing

```bash
# Single search
python watcher_api/api_checker.py HAN SGN 30062026

# The file is executable — run directly:
./watcher_api/api_checker.py HAN SGN 30062026
```
