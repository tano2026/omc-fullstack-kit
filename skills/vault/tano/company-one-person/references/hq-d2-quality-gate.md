# HQ Module — D2 Quality Gate + Event Queue + Tick Claim

**⚠️ SUPERSEDED by `references/quality-gate-v2.md`**

The old `_d2_eval_quality` inline function (6 layers) has been replaced by the full `dashboard/quality_gate.py` module (11 layers). See `references/quality-gate-v2.md` for the current version.

## D2 Quality Gate — `_d2_eval_quality(text) -> dict`

6 mechanical layers that check eval quality with **no LLM judgment**:

| Layer | Check | Fail if |
|-------|-------|---------|
| `thinEval` | Text length | < 100 chars |
| `noCodeRefs` | `file:line` patterns | No matches found |
| `lowUniqueContent` | Unique word ratio | < 40% |
| `lineLengthVarianceLow` | Line length std_dev | < 5 (output too uniform — LLM boilerplate pattern) |
| `aspirationalClaims` | Hedging patterns | "could", "might", "perhaps", "I think", "it seems" present |
| `invalidRefCount` | Links/citations count | 0 or > 20 references |

Returns `{pass: bool, layers: [str,...], score: int}` — score >= 50 passes.

### Integrated into `approve()`

Before approving a job, `approve()` now calls `_d2_eval_quality(action)`. If quality fails, logs `[HQ WARN] D2 quality gate FAIL` with score + layers to activity_log.

### Python API

```python
from dashboard.hq import _d2_eval_quality

result = _d2_eval_quality("This code review found 3 issues in src/main.py:42, src/auth.py:15...")
if not result["pass"]:
    print(f"Quality score {result['score']}, failed layers: {result['layers']}")
```

## Event Queue — `add_event(task, data) -> int` + `pop_event() -> dict|None`

SQLite-backed event queue replaces cron polling. Table `events`:

| Field | Type | Purpose |
|-------|------|---------|
| `id` | INTEGER PK | Auto-increment |
| `task` | TEXT | Event type (e.g. "dispatch", "brief", "alert") |
| `data` | TEXT (JSON) | Payload |
| `status` | TEXT | queued → processing → done |
| `created` | TEXT | ISO timestamp |

**`add_event(task, data)`** — inserts with status `queued`, returns event ID.

**`pop_event()`** — atomically claims oldest `queued` event (BEGIN IMMEDIATE → SELECT FOR UPDATE pattern), sets to `processing`, returns dict. Returns `None` if queue empty.

**`mark_event_done(event_id)`** — sets status to `done`.

## Tick Claim — `_claim_tick(timeout_seconds=300) -> bool`

Atomic DB-based tick claim for dispatch loop concurrency. Table `ticks`:

| Field | Type | Purpose |
|-------|------|---------|
| `id` | INTEGER PK | Auto-increment |
| `claimed_by` | TEXT | Worker identifier |
| `expires_at` | TEXT | ISO timestamp of auto-expiry |
| `active` | INTEGER | 1=active, 0=expired |
| `created` | TEXT | ISO timestamp |

Returns `True` on successful claim, `False` if another worker holds the active tick. Auto-expires stale ticks after `timeout_seconds`. Ensures only one dispatch runs at a time even with overlapping cron schedules.

## Test Coverage

`dashboard/test_hq_d2.py` — 25 tests covering:
- D2 gate: empty, short, good, hedging, uniform, boilerplate, too-many-refs texts
- Tick claim: success, re-claim blocked, expiry reclaim
- Event queue: add, pop, FIFO order, mark done, empty queue
- Approval quality warning integration
