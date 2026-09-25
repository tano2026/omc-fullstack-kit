# Hermes AppData Disk Cleanup

`AppData\Local\hermes\` can silently grow to 100+ GB. On a 172GB drive, one session found it consuming 182GB (likely including session history, audio cache, and plugin artifacts).

## What's inside

| Subdirectory | Typical Size | Safe to delete? |
|---|---|---|
| `sessions/` | 50-150 GB | ⚠️ Session history DB. Can be pruned but user loses history. |
| `audio_cache/` | 1-10 GB | ✅ Regenerates on TTS use |
| `skills/` | 0.1-2 GB | ⚠️ Knowledge base — should NOT delete |
| `plugins/` | 0.1-1 GB | ⚠️ Active plugins |
| `cron/` | 0.01-0.1 GB | ⚠️ Cron job state |
| `memories/` | 0.01-0.1 GB | ⚠️ Persistent memory |
| `venvs/` or virtualenvs | 1-5 GB | ✅ Recreatable |

## Investigation commands

Check session DB size:
```bash
du -sh /c/Users/"Nguyen Ngoc Tan"/AppData/Local/hermes/sessions/
ls -lh /c/Users/"Nguyen Ngoc Tan"/AppData/Local/hermes/sessions/*.db 2>/dev/null
```

Check audio cache:
```bash
du -sh /c/Users/"Nguyen Ngoc Tan"/AppData/Local/hermes/audio_cache/
```

Full breakdown:
```bash
du -sh /c/Users/"Nguyen Ngoc Tan"/AppData/Local/hermes/*/ 2>/dev/null | sort -rh
```

## Note on symlink

`~/.hermes` is a symlink to `D:\AI Store\AgentConfigs\.hermes` (config files).
This is DIFFERENT from `AppData\Local\hermes\` which is the actual AppData storage
(not symlinked). Both can exist simultaneously.

## Cleanup strategy

1. **Always run a breakdown first** — know what's big before deleting
2. **audio_cache/** — safe to clear entirely
3. **sessions/** — ask user before pruning (they lose conversation history)
4. **Never delete skills/, plugins/, cron/, memories/** without user confirmation
