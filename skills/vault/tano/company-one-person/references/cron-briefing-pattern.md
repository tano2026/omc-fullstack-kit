# Cron Briefing Pattern — Morning + Afternoon

## Overview

2 cron scripts that read the taskboard and write reports to the Hermes outbox,
where `cron_telegram.py` picks them up and delivers to Telegram.

| Cron | Time | File | Content |
|------|------|------|---------|
| ☀️ Morning | 08:00 daily | `cron_morning.py` | Taskboard overview, pending/blocked per project, gợi ý dự án chưa có task |
| 🌅 Afternoon | 17:00 daily | `cron_afternoon.py` | Today completions, still running, blocked items, checklist cuối ngày |

## Where files live

Scripts: `~/.hermes/scripts/cron_morning.py` and `cron_afternoon.py`
Registered via `cronjob` Hermes tool with `no_agent=True`, `script` = filename only.

## Script template

```python
import sys, json, time
from pathlib import Path

# Resolve AGENT_CORE — works when Hermes runs script from ~/.hermes/scripts/
AGENT_DIR = Path.home() / "AppData" / "Local" / "hermes" / "scripts"
AGENT_CORE = AGENT_DIR.parent / "skills" / "tano" / "company-one-person" / "references" / "TANO-AGENCY" / "PLATFORM" / "agent-core"
if not AGENT_CORE.exists():
    AGENT_CORE = Path("D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core")
sys.path.insert(0, str(AGENT_CORE))

def run():
    from agents import get_brain
    from core.memory import AgentMemory
    mem = AgentMemory(agent="ceo")
    board = mem.kv_get("assignments", [])

    lines = ["☀️ Báo — ..."]
    # ... build report ...
    return "\n".join(lines)

if __name__ == "__main__":
    report = run()
    # Write to outbox for Telegram delivery
    try:
        op = Path.home() / ".hermes" / "outbox"
        op.mkdir(parents=True, exist_ok=True)
        with open(op / "briefing.json", "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "target": "telegram",
                "message": report,
                "from": "ceo_briefing",
                "ts": str(time.time())
            }, ensure_ascii=False) + "\n")
        print(report)
    except Exception as e:
        print(report)
        print(f"\n(outbox error: {e})")
```

## Separate files per report type

Each cron writes to its own outbox file to avoid mixing payloads:

| Cron | Outbox file | `from` field |
|------|------------|--------------|
| Morning | `morning_report.json` | `ceo_morning` |
| Afternoon | `afternoon_report.json` | `ceo_afternoon` |

The Telegram cron (`cron_telegram.py`, every 15m) reads ALL `.json` files from `~/.hermes/outbox/` and sends them, then clears.

## Key design decisions

- **no_agent=True** — zero token cost, pure script execution. Scripts CANNOT use `hermes_tools.send_message` because they don't have Hermes tool context. Must write to outbox file.
- **File outbox** — not direct Telegram API. Hermes cron `cron_telegram.py` does the actual API call. Two-step: script writes JSON → cron reads+delivers.
- **AGENT_CORE path** must work from `~/.hermes/scripts/` context — use the fallback chain above. `Path(__file__).parent` is UNRELIABLE in cron context — Hermes may run from a different cwd.
- **agent-core can import directly** because it's in sys.path — no subprocess needed.
- **`os.environ` is NOT available** in `no_agent=True` scripts unless explicitly set by the Hermes cron scheduler. Don't rely on env vars in scripts — hardcode any needed paths.
- **Telegram delivery cron (`cron_telegram.py`) NEEDS `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `agent-core/.env`** — it reads `.env` directly, not via `os.environ`. This means .env must be manually updated when token changes.
- **After outbox delivery, files are deleted** — if delivery fails (empty chat_id, wrong token), the message is lost. Monitor Telegram logs. If no delivery, check `TELEGRAM_CHAT_ID` first.

## Pitfalls

| Problem | Fix |
|---------|-----|
| `__file__` resolution fails in Hermes cron context | Hardcode `AGENT_CORE = Path("D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core")` as fallback |
| Cron produces output but Telegram doesn't receive it | Check `TELEGRAM_CHAT_ID` in .env (was empty Jul 2026 → user provided `762010475`). Check token is not revoked. |
| Running twice = duplicate delivery | Each cron writes append to outbox file. Telegram delivery cron reads AND clears. If delivery cron fails mid-way, some items may re-deliver next tick. Acceptable for status reports. |
| `cron_afternoon.py` was created AFTER `cron_morning.py` — both needed same path resolution fix | See script template — always use the fallback chain, don't assume `__file__` works. |
| Dashboard PID 2572 from `dashboard/app.py` was restarted this session | When dashboard.py path changed (`web/dashboard.py` → `dashboard/app.py`), old process kept failing silently. Check `dashboard.log` if dashboard stops responding. |
| **Telegram bot responding very slowly (240s)** | Not a cron issue per se, but affects all Telegram interaction. See `references/telegram-bot-ops.md` → Budget Tuning section. Fix: reduce `PER_COMMAND_BUDGET` to `max_iterations=1, max_seconds=15`. |
