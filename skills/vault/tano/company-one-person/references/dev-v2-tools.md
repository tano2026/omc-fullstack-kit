# Dev Agent v2 — Real Tools Implementation

## Kiến trúc

Dev agent có 2 layer:
1. **Collect phase**: `_real_repo()`, `_real_logs()`, `_real_infra()`, `_real_search()` — tìm dữ liệu thật
2. **Build phase**: `_real_build()` — **tạo file code thật trên ổ cứng**

## _real_repo() — keyword project map

```python
project_map = {
    "abtrip": ["AI Agent Future", "agent.tkt"],
    "fast track": ["TANO-AGENCY"],
    "gmsp": ["GMSP"],
    "tuvi": ["Giai ma so phan", "GMSP"],
    "tano": ["TANO-AGENCY"],
}
```

Fallback: dùng `rg` (ripgrep) tìm file .py chứa keyword.

## _real_infra() — PowerShell health commands

| Command | What it checks |
|---------|---------------|
| `netstat -ano \| findstr :8137 \| findstr LISTENING` | Dashboard đang chạy? |
| `tasklist /FI "IMAGENAME eq python.exe"` | Python processes |
| `wmic logicaldisk get size,freespace,caption` | Disk usage |

## _real_build() — LLM Code Generator

Flow:
1. LLM nhận task + repo context → trả JSON:
```json
{
  "files_to_create": [{"path": "D:/.../file.py", "content": "...", "type": "python"}],
  "commands_to_run": ["pip install requests"],
  "summary": "Created test file for API health check"
}
```
2. `_tool_write_file()` — tạo file thật (mkdir -p + write)
3. `_tool_terminal()` — chạy commands (pip, python file.py, etc.)

### Pitfalls

| Vấn đề | Fix |
|--------|-----|
| LLM trả JSON bị lỗi | Regex extract `\{.*\}` với re.DOTALL, fallback json.loads |
| File path không absolute | LLM được prompt "path must be absolute in D:/MMO Du an/" |
| LLM sinh code sai | Chưa có auto-run test — file được tạo nhưng chưa verify run được |
| _real_build chỉ dùng cho build | review/fix/deploy vẫn dùng LLM analyze (không tạo file) |
| _real_build có timeout | subprocess.run(timeout=60) trên terminal commands |

## _tool_terminal() — subprocess runner

```python
def _tool_terminal(cmd: str, workdir: str = None, timeout: int = 60) -> dict:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       cwd=workdir, timeout=timeout)
    return {"output": (r.stdout + r.stderr)[:2000], "exit_code": r.returncode}
```

- Timeout 60s mặc định
- Output truncated 2000 chars
- Exit code giúp detect lỗi

## _real_search() — Hermes tool hoặc ddgs fallback

```python
try:
    from hermes_tools import web_search
    res = web_search(query=query, limit=max_results)
    # Parse dict result
except ImportError:
    from ddgs import DDGS  # fallback
```

## Files

| File | Description |
|------|-------------|
| `PLATFORM/agent-core/agents/dev/adapters.py` | v2 — all stubs replaced with real tools |
| `PLATFORM/agent-core/agents/dev/spec.py` | Dev spec (build/review/fix/deploy/infra/handover) |
