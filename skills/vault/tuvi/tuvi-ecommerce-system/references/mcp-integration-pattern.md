# MCP Integration Pattern — v2 Singleton Process (verified 20/07/2026)

## Session Context

Session 20/07/2026 superseded the first-attempt `printf | node` pattern with a **persistent singleton process** that keeps the Node.js MCP server alive across multiple tool calls.

## Evolution: v1 → v2

| Aspect | v1 (`printf | node`) | v2 (singleton `_MCPProcess`) |
|--------|---------------------|------------------------------|
| Process | Re-spawn per call | One process, multiple calls |
| Latency | ~4-6s (includes Node.js startup) | ~1s per call (no startup) |
| Threading | None | Reader thread + threading.Event |
| Complexity | Simple shell | Python Popen + thread |
| Reliability | OK for single calls | Better for multi-call flows |

## v2 Architecture

```
FastAPI
  │
  ├─ TuviMCPClient() singleton
  │     └─ _MCPProcess._proc (subprocess.Popen, one node process)
  │           ├─ stdin  → JSON-RPC {"method":"initialize"|"tools/call", ...}
  │           ├─ stdout ← JSON-RPC response {"result":{"content":[...]}}
  │           └─ reader thread (daemon) — parses stdout, signals pending calls
  │
  └─ Calls: calculate_chart(), divination(), palace_detail(), ...
       Each: write to stdin → threading.Event.wait(timeout=30) → parse response
```

## Key Implementation Details

### Reader Thread Pattern

```python
self._pending = {}  # {call_id: {"event": threading.Event(), "result": None}}

def _reader():
    while self._running:
        line = self._proc.stdout.readline()
        if not line:
            break
        resp = json.loads(line.strip())
        rid = resp.get("id")
        if rid in self._pending:
            self._pending[rid]["result"] = resp
            self._pending[rid]["event"].set()  # wake up caller
```

### Why threading.Event instead of Queue?
- Each call produces exactly ONE response (identified by `id` field)
- `Event` is simpler and more efficient than Queue for 1:1 request/response
- Clean timeout handling: `event.wait(timeout=30)` returns False on timeout

### Cleanup on Shutdown

```python
def close(self):
    self._running = False
    self._proc.stdin.close()  # signals EOF to Node.js
    try:
        self._proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        self._proc.kill()
```

## Tools Available

All MCP tools accessible via `TuviMCPClient`:

| Method | MCP Tool | Params | Returns |
|--------|----------|--------|---------|
| `calculate_chart()` | `calculate_chart` | year, month, day, hour, gender | Chart with 12 palaces + stars |
| `divination()` | `divination` | + focus | Full reading text |
| `palace_detail()` | `palace_detail` | + palace name | Palace-specific analysis |
| `four_pillars()` | `four_pillars` | (same chart params) | Tứ trụ bát tự |
| `current_decadal_fortune()` | `current_decadal_fortune` | (same chart params) | Current đại hạn |
| `yearly_fortune()` | `yearly_fortune` | + target_year | Lưu niên analysis |

## Known Limitations

1. **Process lifetime** — If the Node.js process crashes (e.g. memory, exception), all subsequent calls fail. Auto-restart logic is NOT implemented — caller must handle `BrokenPipeError`.
2. **No concurrent calls** — Single reader thread, sequential processing. Concurrent calls would need response correlation via `id`.
3. **`reader` thread never joins** — Daemon thread exits when main process exits. Fine for web servers, not for short-lived scripts.
4. **`shlex.quote` NOT needed** — Unlike v1 which shelled out to `printf | node`, v2 passes args directly to `subprocess.Popen` with list form — no shell injection risk.
