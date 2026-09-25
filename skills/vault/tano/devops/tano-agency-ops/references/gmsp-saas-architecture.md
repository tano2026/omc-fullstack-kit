# GMSP-SAAS Full Architecture

## Overview
Wrap 7-stage GMSP pipeline into a web dashboard. MVP: single-user (Tân nội bộ). Future: auth → multi-user → billing.

## API Endpoints

```
GET  /api/health                    — Health check
POST /api/projects                  — Create project {name, topic, domain, voice}
GET  /api/projects                  — List projects (name, domain, voice, progress, status)
GET  /api/projects/{id}             — Project detail (steps_data JSON)
POST /api/projects/{id}/run/{step}  — Run pipeline step (background task)
GET  /api/projects/{id}/steps/{step}— Step status
GET  /api/knowledge                 — Knowledge base (parsed sections)
```

## DB Schema (SQLite)

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    topic TEXT DEFAULT '',
    domain TEXT DEFAULT 'tu-vi',
    voice TEXT DEFAULT 'trung-thanh',
    status TEXT DEFAULT 'draft',
    steps_data TEXT DEFAULT '{}',   -- JSON: {"research":{"status":"done",...}}
    created_at FLOAT,
    updated_at FLOAT
);
```

## Pipeline Steps

| # | Step | Script | Description |
|---|------|--------|-------------|
| 1 | research | `pipeline/01_research.py` | Research topic |
| 2 | script | `pipeline/02_content.py` | Write script |
| 3 | tts | `pipeline/03_tts.py` | Generate TTS |
| 4 | media | `pipeline/04_media.py` | Create media |
| 5 | render | `pipeline/05_render.py` | Render video |
| 6 | publish | `pipeline/06_publish.py` | Deploy/publish |

Each script called via: `subprocess.run(["python", script, "--project", str(pid)], cwd=BASE_DIR)`

## Migration Path

| Phase | Content | Time |
|-------|---------|------|
| 1 | MVP Streamlit/Jinja2: create project, run pipeline, logs | 2 days |
| 2 | Frontend Next.js: beautiful dashboard + script editor | 5 days |
| 3 | Knowledge base + AI script generation from topic | 3 days |
| 4 | TTS + media preview before render | 2 days |
| 5 | Auth + multi-user | 3 days |
| 6 | Stripe billing + white label | 5 days |
