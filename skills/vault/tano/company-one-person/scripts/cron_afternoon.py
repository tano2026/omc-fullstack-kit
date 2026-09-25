"""Cron afternoon briefing: CEO tổng kết buổi chiều + ghi outbox."""
import sys, json, time
from pathlib import Path

AGENT_DIR = Path.home() / "AppData" / "Local" / "hermes" / "scripts"
AGENT_CORE = AGENT_DIR.parent / "skills" / "tano" / "company-one-person" / "references" / "TANO-AGENCY" / "PLATFORM" / "agent-core"
if not AGENT_CORE.exists():
    AGENT_CORE = Path("D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core")
sys.path.insert(0, str(AGENT_CORE))

PROJECTS = {
    "gmsp": {"name": "GMSP Content Pipeline", "icon": "🎬"},
    "fast_track": {"name": "An Binh Fast Track", "icon": "🛬"},
    "abtrip": {"name": "ABTrip Ticketing", "icon": "✈️"},
    "tuvi": {"name": "Tu Vi AI Engine", "icon": "🔮"},
}

def run():
    try:
        from core.memory import AgentMemory
        mem = AgentMemory(agent="ceo")
        board = mem.kv_get("assignments", [])

        running = [a for a in board if a.get("status") == "running"]
        done_today = [a for a in board if a.get("status") == "done"]
        blocked = [a for a in board if a.get("status") == "blocked"]
        pending = [a for a in board if a.get("status") == "pending"]

        lines = [f"🌅 Bao chieu — {time.strftime('%d/%m/%Y %H:%M')}", ""]
        lines.append(f"Hom nay: {len(done_today)} viec xong, {len(running)} dang lam")
        lines.append("")

        if done_today:
            lines.append("Da hoan thanh:")
            for t in done_today[-5:]:
                lines.append(f"  ✅ {t.get('dept','?')}: {t.get('task','')[:60]}")
            lines.append("")

        if running:
            lines.append("Dang lam:")
            for t in running[:5]:
                lines.append(f"  🔄 {t.get('dept','?')}: {t.get('task','')[:60]}")
            lines.append("")

        if blocked:
            lines.append(f"Bi chan ({len(blocked)}):")
            for t in blocked[:3]:
                lines.append(f"  ❌ {t.get('dept','?')}: {t.get('task','')[:50]}")
            lines.append("")

        if pending:
            lines.append(f"{len(pending)} viec cho ngay mai")
            lines.append("")

        lines.append("Checklist cuoi ngay:")
        lines.append("  [ ] Dashboard http://localhost:8137 con chay?")
        lines.append("  [ ] 9 agent OK?")
        lines.append("  [ ] Code da commit?")
        lines.append(f"\n🤖 CEO TANO-AGENCY · {time.strftime('%H:%M')}")
        return "\n".join(lines)
    except Exception as e:
        return f"Loi afternoon briefing: {e}"

if __name__ == "__main__":
    report = run()
    try:
        op = Path.home() / ".hermes" / "outbox"
        op.mkdir(parents=True, exist_ok=True)
        with open(op / "afternoon_report.json", "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "target": "telegram",
                "message": report,
                "from": "ceo_afternoon",
                "ts": str(time.time())
            }, ensure_ascii=False) + "\n")
        print(report)
    except Exception as e:
        print(report)
        print(f"\n(ko ghi dc outbox: {e})")
