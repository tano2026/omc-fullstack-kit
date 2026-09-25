# Smart Agent Backend Architecture (July 2026)

## 5-Service Router

```
User Message → classify_service() → Route to handler
  ├── "flight"       → _handle_ticketing (existing intent parser + AGT/mock)
  ├── "fasttrack"    → _handle_smart_service → smart_fasttrack.py
  ├── "esim"         → _handle_smart_service → smart_esim.py
  ├── "visa"         → _handle_smart_service → smart_visa.py
  └── "passport"     → _handle_smart_service → smart_passport.py
```

Service routing happens in `chat.py` STEP 0 — BEFORE pending action checks. But service routing is ONLY active when there's no pending action (confirm flow), so `"OK"` after confirm works.

## Flight Results: Structured JSON + Frontend Render (User Preference)

User found code-block tables "khó nhìn". **The solution is NOT to prettify text formatting — the solution is architecture change:**

1. **Backend** returns `data.flights[]` as structured JSON array with `{airline, flight_code, depart, arrive, price, duration, cheapest}` per item
2. **Frontend HTML** renders each flight as a card/row with:
   - Airline emoji + flight code left
   - Depart→arrive time in middle  
   - Price right (big, bold, standout color for cheapest)
   - Duration as subtitle

This avoids monospace tables entirely and gives proper visual hierarchy.

## Nginx Config Pitfall

When `sites-enabled/` has MULTIPLE configs listening on `server_name _` port 80, nginx uses the LAST-enabled one (alphabetical or link order). This caused `hermes` config to override `abtrip` config for API proxy.

**Fix:** Only keep ONE config per port. Disable conflicting ones:
```bash
sudo rm /etc/nginx/sites-enabled/hermes
sudo systemctl reload nginx
```

## Session Persistence & Workers

uvicorn with `--workers 2` splits sessions between workers — a confirm from worker 1 won't be seen by worker 2. **Fix:** use `--workers 1` for in-memory session apps.

For production multi-worker, use Redis or shared session store.
