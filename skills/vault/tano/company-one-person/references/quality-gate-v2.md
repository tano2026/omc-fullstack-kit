# Quality Gate v2 — Full D2 Compound Defense (19/07/2026)

Replaces the limited `_d2_eval_quality` inline function. Full 11-layer module adapted from OPC (iamtouchskyer/opc).

## Module: `dashboard/quality_gate.py`

### 11-Layer D2 Compound Defense

| Layer | Function | Check | Fail Condition | 
|-------|----------|-------|---------------|
| L1 | `check_thin_eval()` | Text length | < 200 chars |
| L2 | `check_no_code_refs()` | `file:line` references | < 2 refs |
| L3 | `check_low_unique_content()` | Unique word ratio | < 40% (boilerplate) |
| L4 | `check_single_heading()` | Markdown headings | < 2 headings (flat structure) |
| L5 | `check_finding_density_low()` | Finding/keyword markers | < 2 findings in long text |
| L6 | `check_fabricated_refs()` | Reference exists? | > 3 refs to non-existent files |
| L7 | `check_line_length_variance()` | Line std deviation | < 8 (LLM output pattern) |
| L8 | `check_aspirational_claims()` | Hedging words | > 5 hits (could, might, should, consider) |
| L9 | `check_missing_reasoning()` | Reasoning markers | < 3 (because, since, therefore) |
| L10 | `check_missing_fix()` | Issue described but fix? | Has issue but no fix recommendation |
| L11 | `check_invalid_ref_count()` | Refs vs text length | < 2 refs or < 1 ref per 200 words |

### Verdict Rules (code-enforced, no LLM)

- ≥ 3 layers fail → **FAIL**
- 1-2 layers fail → **ITERATE**
- 0 fails → **PASS**

### Review Independence Enforcement

`check_review_independence(eval_texts: list[str]) -> dict`

- Byte-identical evals → `ERROR` (hard fail)
- > 70% line overlap → `WARNING`
- Otherwise → `PASS`

### Usage

```python
from dashboard.quality_gate import run_d2_gate, check_review_independence

result = run_d2_gate(eval_text, existing_files=["src/main.py", "src/auth.py"])
print(result.summary())  # "D2 Gate: FAIL (4 fail / 11 checks)"
for layer in result.layers:
    if layer["failed"]:
        print(f'  {layer["severity"]} {layer["name"]}: {layer["detail"]}')

ri = check_review_independence([eval1, eval2, eval3])
if ri["status"] == "FAIL":
    print("Reviews are colluding!")
```

## Loop Mode: `dashboard/loop_mode.py`

Atomic checkout pattern from Paperclip heartbeat + OPC loop ownership.

### Atomic Checkout

```python
from dashboard.loop_mode import atomic_checkout, release, heartbeat, dispatch_tick

if atomic_checkout("slot-09", owner="dispatch"):
    try:
        heartbeat("slot-09")  # Keep lock alive
    finally:
        release("slot-09")
```

### Dispatch Tick (full workflow)

```python
result = dispatch_tick("slot-09", limit=5)
# Returns: {"claimed": True, "dispatched": 2, "jobs": [...]}
```

### Integration in cron scripts

```python
from loop_mode import dispatch_tick, clean_stale_locks
slot = os.environ.get("DISPATCH_SLOT", "slot-09")
clean_stale_locks(max_age_minutes=60)
result = dispatch_tick(slot, limit=10)
```
