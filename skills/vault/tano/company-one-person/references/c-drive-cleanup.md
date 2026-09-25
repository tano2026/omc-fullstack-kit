# C: Drive Cleanup — Safe Deletions (July 2026)

Ổ C (171GB NVMe) thường gần đầy (0-14GB free). Các thư mục **xoá an toàn**:

## Top offenders

| Item | Size (Jul 2026) | Action | Recovery |
|------|-----------------|--------|----------|
| `~\.gemini\` | 6.8 GB | Delete | Cache Gemini CLI — tự tạo lại |
| `~\.cursor\Cache\` | 2.1 GB | Delete | Cache Cursor IDE |
| `~\.vscode\extensions\` | 1.9 GB | Delete | Cài lại được từ IDE |
| `~\.cache\` | 1.0 GB | Delete | pip/hermes/uv cache |
| `C:\Windows\SoftwareDistribution\Download\` | ~1.6 MB | Delete | Windows Update cache |
| `%TEMP%\` | ~2.6 GB | Delete | Windows temp files |

## Clean script

```
C:\Users\<user>\deep_clean.ps1
```

```powershell
Remove-Item "$env:USERPROFILE\.gemini" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\.cursor\Cache" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\.vscode\extensions\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\.cache\" -Recurse -Force -ErrorAction SilentlyContinue
npm cache clean --force 2>$null
Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
```

Sau clean: 0 → ~14GB free.

## DO NOT delete (important data)
- `C:\Windows\WinSxS\` — System files
- `~\.ollama\` (3GB) — AI models if user still uses Ollama
- `~\.hermes\` — Hermes config + skills

## Preventive
- Set `pip config set global.cache-dir D:/pip-cache`
- Consider `set TEMP=D:\Temp` environment variable
- Monitor free space weekly
