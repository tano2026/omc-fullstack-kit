# Dev Agent Budget Cap

## Overview

Giới hạn tài nguyên cho Dev agent để tránh loop vô hạn, spam terminal, hoặc LLM over-generation.

## Budget limits

```python
_DEV_BUDGET = {
    "terminal_calls": 0,          # Counter: số lần gọi _tool_terminal
    "max_terminal_calls": 10,     # Max: 10 lần terminal
    "files_created": 0,           # Counter: số file đã tạo
    "max_files_created": 8,       # Max: 8 files
    "total_read_chars": 0,        # Counter: tổng chars đã đọc từ file
    "max_read_chars": 30000,      # Max: 30KB
    "started_at": None,           # Thời điểm bắt đầu (time.monotonic)
    "max_duration_seconds": 120,  # Max: 2 phút
}
```

## Functions

### `_budget_check(name) -> (ok: bool, reason: str)`
- Kiểm tra tất cả counters trước khi cho phép thao tác
- Init `started_at` ở lần gọi đầu tiên
- Nếu bất kỳ budget nào hết → return False + reason

### `_budget_tick(name)`
- Tăng counter tương ứng:
  - `"terminal"` → `terminal_calls += 1`
  - `"file_write"` → `files_created += 1`

### `_budget_reset()`
- Reset tất cả counters về 0
- Reset `started_at` về None
- Gọi khi chuẩn bị chạy task mới

## Where injected

| Function | Hook location | Budget check |
|----------|--------------|--------------|
| `_tool_terminal()` | First line | `_budget_check("terminal")` then `_budget_tick("terminal")` |
| `_tool_write_file()` | First line | `_budget_check("file_write")` then `_budget_tick("file_write")` |
| `_tool_read_file()` | First line | `_budget_check("file_read")` (no tick — chars counted via content length) |

**Note:** `_tool_read_file` doesn't call `_budget_tick` because read limit is tracked by `total_read_chars` (chars consumed). The `_budget_check` already verifies this cap.

## File

`agents/dev/adapters.py` — ≈50 lines after guard definitions, before tool function definitions.

## Design decisions

- Budget is **per-session** (reset between tasks, not persistent across reboots)
- Budget is **global to Dev agent**, not per-invocation — prevents infinite loops within one `brain.run()`
- Blocked requests return same shape as errors: `{"output": reason, "exit_code": -1}` for terminal, `{"status": "blocked", "error": reason}` for file ops
- **No budget for read-only tool search** (`_tool_search_files`, `_real_repo`, `_real_logs`) — only file create/read/write + terminal
- **No budget for LLM analyzers** — those are just string operations, cost is negligible

## Test commands

```python
from agents.dev.adapters import _tool_write_file, _tool_terminal, _budget_reset, _DEV_BUDGET

# Reset
_budget_reset()

# Use tools
_tool_terminal('pip list')  # count: 1
_tool_write_file('D:/MMO Du an/test.txt', 'a')  # count: 1

# Check state
print(_DEV_BUDGET['terminal_calls'])  # 1
print(_DEV_BUDGET['files_created'])   # 1

# Reset again
_budget_reset()
print(_DEV_BUDGET['terminal_calls'])  # 0
```
