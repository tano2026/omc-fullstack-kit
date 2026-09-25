"""Cron morning briefing: CEO check taskboard + chủ động đề xuất."""
import sys, os, json, time
from pathlib import Path

AGENT_CORE = Path(__file__).parent.parent / "PLATFORM" / "agent-core"
sys.path.insert(0, str(AGENT_CORE))

PROJECTS = {
    "gmsp": {
        "name": "🎬 GMSP Content Pipeline",
        "depts": ["research", "marketing", "media"],
        "desc": "Sản xuất video Tử Vi / Phát Triển Bản Thân / Cổ Kim — pipeline 7 bước"
    },
    "fast_track": {
        "name": "🛬 An Bình Fast Track",
        "depts": ["dev", "marketing", "media", "sales"],
        "desc": "Fast Track + VIP B + Lounge Nội Bài — landing page + content + OTA listing"
    },
    "abtrip": {
        "name": "✈️ ABTrip Ticketing",
        "depts": ["dev", "operations", "analytics"],
        "desc": "Platform đặt vé máy bay — AGT cấp 1 API"
    },
    "tuvi": {
        "name": "🔮 Tử Vi AI Engine",
        "depts": ["dev", "research"],
        "desc": "Tử Vi Đẩu Số platform — iztro + MCP + Python engine"
    },
}

def run():
    try:
        from agents import get_brain
        from agents.ceo.adapters import DEPTS, DEFAULT_TTYPE
        from core.memory import AgentMemory
        
        mem = AgentMemory(agent="ceo")
        board = mem.kv_get("assignments", [])
        
        project_tasks = {k: [] for k in PROJECTS}
        other_tasks = []
        for a in board:
            mission = (a.get("mission", "") + " " + a.get("task", "")).lower()
            matched = False
            for pk, pv in PROJECTS.items():
                keywords = pv["name"].lower().split() + [pk]
                if any(kw in mission for kw in keywords):
                    project_tasks[pk].append(a)
                    matched = True
                    break
            if not matched:
                other_tasks.append(a)
        
        lines = [f"☀️ **Morning Briefing — {time.strftime('%d/%m/%Y %H:%M')}**", ""]
        lines.append(f"📊 **Tổng quan:** {len(board)} tasks trên taskboard")
        lines.append("")
        
        for pk, pv in PROJECTS.items():
            tasks = project_tasks[pk]
            if tasks:
                done = sum(1 for t in tasks if t.get("status") == "done")
                blocked = sum(1 for t in tasks if t.get("status") == "blocked")
                running = sum(1 for t in tasks if t.get("status") == "running")
                pending = sum(1 for t in tasks if t.get("status") == "pending")
                lines.append(f"{pv['name']}")
                lines.append(f"   {done}✅ / {running}🔄 / {pending}⏳ / {blocked}❌")
                for t in tasks[-3:]:
                    emoji = {"done": "✅", "pending": "⏳", "blocked": "❌", "running": "🔄"}
                    lines.append(f"   {emoji.get(t.get('status','?'),'•')} {t.get('dept','?')}: {t.get('task','')[:60]}")
                lines.append("")
            else:
                lines.append(f"{pv['name']} — ⚪ chưa có task")
                lines.append(f"   _Gợi ý: gọi CEO để khởi động — \"{pv['name']}\"_")
                lines.append("")
        
        if other_tasks:
            lines.append(f"📋 **Việc khác:** {len(other_tasks)} tasks")
            for t in other_tasks[-5:]:
                emoji = {"done": "✅", "pending": "⏳", "blocked": "❌", "running": "🔄"}
                lines.append(f"   {emoji.get(t.get('status','?'),'•')} {t.get('dept','?')}: {t.get('task','')[:60]}")
            lines.append("")
        
        total_pending = sum(1 for a in board if a.get("status") == "pending")
        if total_pending > 0:
            lines.append(f"⏳ **{total_pending} việc pending** — cronjob dispatch sẽ chạy tự động")
        else:
            lines.append("✅ Không có việc pending. Mọi người rảnh.")
        
        lines.append("")
        lines.append(f"> 🤖 CEO TANO-AGENCY · {time.strftime('%H:%M')}")
        return "\n".join(lines)
        
    except Exception as e:
        return f"❌ Morning briefing error: {e}"

if __name__ == "__main__":
    print(run())
