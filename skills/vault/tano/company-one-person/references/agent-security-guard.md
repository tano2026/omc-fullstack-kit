# Guard System — Dev Agent Security Layers

## 3-Layer Guard Architecture

```
User input → Layer 1: BUDGET CAP → Layer 2: FILE I/O GUARD → Layer 3: TERMINAL GUARD → Execution
```

### Layer 1: Budget Cap (`_budget_check`)
```
terminal_calls ≤ 10 | files_created ≤ 8 | read_chars ≤ 30000 | duration ≤ 120s
```

### Layer 2: File I/O Guard (`_is_allowed_path`)
```
ALLOWED: D:/MMO Du an/, Desktop/, Documents/, $HOME/
BLOCKED: C:\Windows, Program Files, System32, AppData\Roaming
```

### Layer 3: Terminal Guard (`_is_safe_command`)
```
BLOCKED: del, rm -rf, format, shutdown, curl -o, powershell -enc
ALLOWED: pip, python, git, pytest, node, npm, cd, cat, cp, mkdir
```

## Security Review Checklist (from ecc-security-review skill)

After embedding the ecc-security-review skill pattern into Dev agent prompts, the following security concerns are checked at each code operation:

| Concern | Check | Where |
|---------|-------|-------|
| Secrets exposure | _tool_write_file scans for API_KEY, TOKEN, password patterns via regex | `_real_build()` prompt |
| Input validation | _tool_terminal validates via command whitelist, not just blacklist | `_is_safe_command()` |
| Path traversal | _tool_read_file/_tool_write_file resolve() and check allowed roots | `_is_allowed_path()` |
| Resource exhaustion | _budget_check prevents infinite loops | `_tool_terminal/write_file/read_file` |
| SQL injection | _analytics_query blocks DROP/INSERT/UPDATE/DELETE/ALTER | `real_adapters.py` (Analytics agent) |

## File

- `agents/dev/adapters.py`: `_is_allowed_path()`, `_is_safe_command()`, `_budget_check()/_budget_tick()/_budget_reset()`
