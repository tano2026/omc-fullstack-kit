"""
dispatch_report.py — Reusable dispatch-tick reporting pattern for TANO HQ.

Reads queued/doing/review jobs from data/hq.db (already sorted P0>P1>P2 by
hq.get_jobs()), plus pending approvals + open escalations, formats a Markdown
summary, and sends it to the CEO via Telegram using real_adapters._tg_send().

This does NOT move jobs between statuses — that's scripts/cron_dispatch.py's
job (loop_mode.dispatch_tick(), atomic checkout, queued->doing only). Run this
AFTER (or instead of, if you just want a status report) that script.

Usage (from agent-core/ root, bash on Windows):
    python scripts/dispatch_report.py

Requires: sys.path must include dashboard/ for hq.py, and core.llm.load_dotenv()
must run before real_adapters._tg_send() or TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID
won't be in os.environ yet (real_adapters.py loads dotenv only at import time
in the module's own load path — calling it explicitly here is the safe,
idempotent way to guarantee it's loaded regardless of import order).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "dashboard"))

import hq
from core.llm import load_dotenv
load_dotenv()
import real_adapters as ra


def fmt(j):
    return f"[{j['id']}] {j['priority']} · {j['pack']}/{j['role']} — {j['brief'][:70]}"


def build_report():
    queued = hq.get_jobs(status="queued", limit=50)
    doing = hq.get_jobs(status="doing", limit=50)
    review = hq.get_jobs(status="review", limit=50)
    pending_approvals = hq.get_pending_approvals(20)
    esc = hq.get_open_escalations()

    lines = ["📋 *DISPATCH TICK* — TANO HQ"]

    if queued:
        lines.append("")
        lines.append(f"🟡 *Queued* ({len(queued)}) — ưu tiên P0>P1>P2:")
        for j in queued:
            lines.append("  " + fmt(j))
    else:
        lines.append("")
        lines.append("✅ Không có job nào đang *queued* — hàng đợi trống.")

    if doing:
        lines.append("")
        lines.append(f"🔵 *Đang làm (doing)* ({len(doing)}):")
        for j in doing:
            lines.append("  " + fmt(j))

    if review:
        lines.append("")
        lines.append(f"🟠 *Chờ review* ({len(review)}):")
        for j in review:
            lines.append("  " + fmt(j))

    if pending_approvals:
        lines.append("")
        lines.append(f"💰 *Chờ duyệt* ({len(pending_approvals)}):")
        for a in pending_approvals:
            lines.append(f"  [{a['job_id']}] {a['pack']} — {a['action'][:60]}")

    if esc:
        lines.append("")
        lines.append(f"🔴 *Escalation mở* ({len(esc)}):")
        for e in esc:
            lines.append(f"  [{e['id']}] {e['role']} — {e['reason'][:60]}")

    return "\n".join(lines)


if __name__ == "__main__":
    msg = build_report()
    print(msg)
    print("---SEND---")
    result = ra._tg_send(msg)
    print(result)
