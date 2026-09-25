# Backup System for TANO-AGENCY (Jul 2026)

## Kiến trúc

```
Daily backup -> D:\Backups\TANO-AGENCY\YYYYMMDD_HHMMSS\
  - main.py, real_adapters.py, skill_loader.py, .env
  - core/, agents/, dashboard/, data/ (SQLite DBs), skills/
  - _manifest.json (metadata)
```

## Script path rule
Hermes cron yêu cầu script path RELATIVE tới ~/.hermes/scripts/.
Copy bang: cp <src> $HOME/AppData/Local/hermes/scripts/backup.py

## Cron
- Schedule: 0 3 * * * (3h sang)
- Script: backup.py (no_agent=True)
- Delivery: local
- Giu 7 ngay, tu cleanup
