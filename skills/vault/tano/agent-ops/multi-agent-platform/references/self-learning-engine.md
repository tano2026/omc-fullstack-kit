# Self-Learning Engine Architecture — Implementation Notes

**Date:** 2026-07-18
**Project:** D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core/
**Tech stack:** Python stdlib + SQLite, zero external deps

## File Layout

```
agent-core/
├── main.py              # Hooked: run_agent(), cmd_natural(), handle() mỗi interaction
├── core/
│   ├── instinct.py      # ObservationHook, PatternDetector, InstinctManager
│   ├── evolver.py       # Evolver → auto skill .md + report
│   └── harness.py       # Hooked: auto-ghi observation khi FAIL verdict
├── auto-learn.py        # Cron entry point (scan → batch upsert → evolve)
└── learning/            # Auto-created
    ├── learning.db      # SQLite (2 tables: observations, instincts)
    └── skills/auto/     # Evolved skills (.md files)
```

## Observation Schema (SQLite)

```sql
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL,
    ttype TEXT NOT NULL,
    prompt TEXT,
    response TEXT,
    outcome TEXT,        -- 'success' | 'error' | 'correction' | 'unknown'
    error_msg TEXT,
    user_feedback TEXT,
    duration_ms INTEGER,
    created_at REAL DEFAULT (julianday('now'))
);

CREATE TABLE IF NOT EXISTS instincts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL,
    pattern_type TEXT NOT NULL,  -- 'correction' | 'error' | 'repetition' | 'workflow'
    title TEXT NOT NULL,
    description TEXT,
    trigger_hint TEXT,
    action_hint TEXT,
    confidence REAL DEFAULT 0.3,
    hit_count INTEGER DEFAULT 1,
    evolved_into_skill TEXT,     -- path to SKILL.md, null if not yet
    observation_ids TEXT,        -- JSON array of related observation IDs
    created_at REAL DEFAULT (julianday('now')),
    updated_at REAL DEFAULT (julianday('now'))
);

CREATE INDEX IF NOT EXISTS idx_obs_agent ON observations(agent);
CREATE INDEX IF NOT EXISTS idx_obs_outcome ON observations(outcome);
CREATE INDEX IF NOT EXISTS idx_obs_created ON observations(created_at);
CREATE INDEX IF NOT EXISTS idx_inst_agent ON instincts(agent);
```

## Confidence Escalation

| Pattern | Initial | Per hit | Max | Trigger | 
|---------|---------|---------|-----|---------|
| correction | 0.5 | +0.1 | 0.9 | 1 occurrence |
| error | 0.4 | +0.15 | 0.9 | 2+ same error |
| repetition | 0.4 | +0.1 | 0.8 | 3+ same ttype/24h |
| workflow | 0.5 | +0.05/step | 0.7 | 3+ steps/30min |

Auto-evolve to skill when confidence ≥ 0.7 AND no `evolved_into_skill` set.

## Evolution Output

Path: `skills/auto/<agent>-<pattern_type>-<slug>.md`

Format:
```markdown
# {title}
**Pattern:** {pattern_type}  
**Agent:** {agent}  
**Confidence:** {confidence:.2f}  
**Evolved:** {timestamp}

## Trigger
{trigger_hint}

## Action
{action_hint}

## Description
{description}
```

## Key Design Decisions

1. **Synchronous SQLite** — single process, WAL mode, timeout=10s. No async, no locks.
2. **24-48h scan window** — không scan toàn bộ lịch sử. Chỉ vài trăm observations gần nhất.
3. **4 patterns, không hơn** — correction, error, repetition, workflow. Không thêm attention/novelty/complexity patterns cho v1.
4. **In-memory last_response** — `_last_responses = {}` dict per chat_id. Không persist cross-restart. Observation + instinct persist qua SQLite nên correction tracking survive restart (prev prompt đọc từ DB, không từ memory).
5. **Keywords heuristic cho correction** — list `["không", "đừng", "sai", "thay vì", "nên", "hãy", "mày sai", "làm lại", "khác đi"]`. False positive xảy ra nhưng chỉ ghi DB, không action cho tới confidence 0.7.

## Hook Location (main.py)

Khi thêm vào bot mới, tìm 3 chỗ:

```python
# 1. Sau Harness.run() trong run_agent()
h = Harness(brain, Budget(...))
result = h.run(ttype, topic)
obs_hook().record(agent=agent, ttype=ttype, prompt=topic,
    response=result["chunks"][0] if result["chunks"] else "",
    outcome="success" if result["verdict"] in ("PASS","WARN") else "error",
    duration_ms=dt_ms)

# 2. Sau Harness.run() trong cmd_natural()
obs_hook().record(agent="ceo", ttype="delegate", prompt=text,
    response=result["chunks"][0], outcome=...

# 3. Trong handle(), trước khi gửi đến cmd_natural()
# Detect correction + record
_track_correction(chat_id, text)
cmd_natural(chat_id, text)
```

## Cron Schedule

Auto-learn mỗi 30 phút:
```bash
hermes cron create --schedule "*/30 * * * *" "cd /d D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core && python auto-learn.py"
```
