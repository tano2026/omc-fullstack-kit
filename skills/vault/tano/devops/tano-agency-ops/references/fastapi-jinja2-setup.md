# FastAPI + Jinja2 Setup Boilerplate

## Minimal FastAPI app with template serving

```python
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

BASE_DIR = Path("D:/MMO Du an/GMSP-SAAS")

app = FastAPI(title="My App")

# ─── API Routes (declare FIRST) ───
@app.get("/api/health")
def health():
    return {"status": "ok"}

# ─── Static files (AFTER API routes) ───
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# ─── Web Routes (AFTER static mount) ───
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return TEMPLATES.TemplateResponse("index.html", {"request": request})
```

## File structure

```
project/
├── backend/
│   └── main.py
├── templates/
│   └── index.html
├── static/
│   └── css/
│       └── style.css
└── start.bat
```

## Key rules
1. **Import order:** `StaticFiles` and `TemplatesResponse` from `fastapi.staticfiles`, `fastapi.templating`, `fastapi.responses`
2. **Mount order:** API routes → StaticFiles mount → Web routes
3. **Don't use `Project` from `jinja2`** — use `Jinja2Templates(directory=...)` from FastAPI
4. **TemplateResponse signature:** `TEMPLATES.TemplateResponse("file.html", {"request": request})`
5. **Pass `request`** — it's required by Jinja2 for URL generation
