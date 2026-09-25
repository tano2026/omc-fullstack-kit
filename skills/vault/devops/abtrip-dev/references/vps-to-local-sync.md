# VPS-to-Local Sync Workflow (added 24 Jul 2026, fixed 24 Jul 2026)

## When to use this

- User says local code is "cũ quá" (outdated)
- Local Docker containers show different UI than VPS at `http://100.64.173.75:8138/`
- You discovered local files differ from VPS versions

## The rule

**The VPS is the source of truth for production code.** Sync FROM it when local is stale, TO it when local has new changes. Never modify local code based on assumptions — verify against VPS first.

## ⛔ DO NOT USE `scp -r` (creates nested dirs on Windows Git Bash)

`scp -r ubuntu@vps:/opt/abtrip-backend/backend/app/services/ "D:/.../services/"` silently creates `services/services/` inside the target — ALL your actual services/ files remain untouched. The old `chat.html` / `chat.py` keeps serving while you think you've updated them. This is silent data corruption.

## ✅ Correct method: tar pipe (one-shot, never creates nested dirs)

```bash
# Sync entire backend app/ directory from VPS to local (overwrites in-place)
ssh -o ConnectTimeout=10 ubuntu@43.156.72.127 "cd /opt/abtrip-backend/backend && tar czf - app/" | tar xzf - -C "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/backend/"
```

**Why this works while scp -r doesn't:**
- `tar` on VPS flattens the directory tree into a stream — no trailing-slash ambiguity
- `tar xzf -` on local extracts exactly the same tree, overwriting files in-place
- No nested directories, no duplicated subfolders

**After syncing — verify line counts match VPS:**
```bash
# Check key files are the same size as VPS
echo "VPS: $(ssh ubuntu@43.156.72.127 'wc -l < /opt/abtrip-backend/backend/app/services/rag_service.py')"
echo "LOCAL: $(wc -l < 'D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/backend/app/services/rag_service.py')"
```

## After syncing — rebuild Docker

```bash
"C:/Users/Nguyen Ngoc Tan/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe" compose -f "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/docker-compose.local.yml" up -d --build --force-recreate --no-deps abtrip-backend
```

Wait 3-5 seconds for Uvicorn startup, then verify:
```bash
curl -s http://localhost:8765/api/health  # should return 200
curl -s http://localhost:8765/ | head -3   # should show <html lang="vi"> — the Smart Agent landing
```

## Verify

- Check `main.py` still points to `TEMPLATES_DIR / "main.html"` (NOT `landing_page_sanhoo.html`)
- `docker compose logs abtrip-backend --tail=5` should show "Application startup complete"
- Open `http://localhost:8765` — should show Smart Agent landing page matching VPS at `http://100.64.173.75:8138/`

## Key distinction from deploy.sh

- **deploy.sh** pushes local → VPS (when local has new code)
- **This workflow** pulls VPS → local (when VPS is ahead, or local is stale/corrupt)
- The VPS is the canonical environment — always verify direction before transferring files

## Related pitfalls

- Pitfall #22: uvicorn 0.51.0+ breaking change — pin to `<0.51.0`
- Pitfall #23: missing `from pathlib import Path` in main.py
- Pitfall #24: scp -r trailing slash creates nested dirs on Windows Git Bash — use tar pipe instead
- After any VPS sync, `main.html` serves the "Smart Agent — Phòng Vé AI" page, NOT the old Next.js frontend
