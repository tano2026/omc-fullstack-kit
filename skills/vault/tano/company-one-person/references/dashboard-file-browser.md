# Dashboard File Browser (20/07/2026)

## Purpose
Allow the CEO agent (chat on dashboard) to read files from `D:\MMO Du an` — solve "CEO không vào được ổ D" problem.

## Endpoints

| Endpoint | Method | Params | Description |
|----------|--------|--------|-------------|
| `/api/file/ls` | GET | `?path=D:/MMO Du an` | List directory contents (sorted: dirs first, then files, alphabetical) |
| `/api/file/read` | GET | `?path=...&offset=1&limit=200` | Read text file with line numbers |
| `/api/file/search` | GET | `?path=...&pattern=...&ext=.md` | Find files by name pattern (max 50 results) |

## Security

```python
ALLOWED_BASE = Path("D:/MMO Du an").resolve()

def _safe_path(user_path: str) -> Path | None:
    try:
        p = Path(user_path).resolve()
        if p == ALLOWED_BASE or ALLOWED_BASE in p.parents or p.parent == ALLOWED_BASE:
            if p.exists():
                return p
    except Exception:
        pass
    return None
```

File read whitelisted extensions: `.txt`, `.md`, `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.cfg`, `.ini`, `.conf`, `.log`, `.csv`, `.xml`, `.html`, `.css`, `.bat`, `.sh`, `.ps1`, `.env`, `.sql`, `.db`, `.sample`

## Pitfall — 404 after rewrite

After rewriting `app.py`, 3 file endpoints may return 404 despite `len(app.routes)` showing 52 routes with all 3 present.

**Fix sequence:**
1. `cd "/d/MMO Du an/TANO-AGENCY/PLATFORM/agent-core" && python -c "import shutil,os; [shutil.rmtree(os.path.join(d,'__pycache__')) for d,dirs,_ in os.walk('.') if '__pycache__' in dirs]"`
2. `netstat -ano | grep 8138` — find LISTENING PID
3. `taskkill /F /PID <PID>` — kill exactly that PID
4. Restart `python dashboard/app.py`
5. `python -c "import urllib.request, json; r=urllib.request.urlopen('http://localhost:8138/api/file/ls?path='+urllib.parse.quote('D:/MMO Du an')); print(json.loads(r.read())['ok'])"` — verify
