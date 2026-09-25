#!/usr/bin/env python
"""Batch test harness for ABTrip smart_agent_router booking + ops queries.
Runs 7 test cases against POST /api/smart-agent/chat and reports results.
Usage: python test_batch.py [--base http://localhost:8765]
"""
import httpx, json, time, sys, re

BASE = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--base" else "http://localhost:8765"
ENDPOINT = f"{BASE}/api/smart-agent/chat"

TESTS = [
    ("1-VeSG-HN", "vé SG đi Hà Nội mai, 1 người"),
    ("2-Alias-DN", "vé sài gòn đến đà nẵng thứ 7, 2 người"),
    ("3-DateNum", "vé Hà Nội đi Đà Nẵng 15/8, 3 người"),
    ("4-OpsRefund", "chính sách hoàn vé Vietjet thế nào?"),
    ("5-MissingOrigin", "vé đi Nha Trang mai"),
    ("6-Short", "vé SG HN"),
    ("7-HCM-NT", "vé Hồ Chí Minh đi Nha Trang 20/8"),
]

MARKERS = {
    "flight": "✈️",
    "price": "💰",
    "cheapest": "🏷",
    "rag": "📚",
    "clarify": "❓",
    "error": "❌",
}

results = []

for name, msg in TESTS:
    t0 = time.time()
    try:
        r = httpx.post(ENDPOINT, json={"message": msg, "session_id": f"test_{name}"}, timeout=45)
        # Parse SSE stream for final content
        full = ""
        for line in r.text.split("\n"):
            if line.startswith("data: ") and line != "data: [DONE]":
                try:
                    ev = json.loads(line[6:])
                    if ev.get("type") == "done":
                        full = ev.get("content", "")
                except json.JSONDecodeError:
                    pass
        if not full:
            full = "(empty)"
        elapsed = f"{time.time() - t0:.1f}s"

        # Detect markers
        flags = {k: bool(re.search(v, full, re.IGNORECASE)) if isinstance(v, str) else v(full)
                 for k, v in {
                     "flight": r"(?i)(chuyến|flight|SGN|HAN|CXR|DAD|\bBL\d|\bVJ\d|\bVN\d|\bQH\d|\bVU\d)",
                     "price": r"\d[\d,]*[₫Vv]",
                     "cheapest": r"(?i)(rẻ nhất|cheapest)",
                     "rag": r"(?i)(THÔNG TIN TRA CỨU|chính sách|hành lý)",
                     "clarify": r"(?i)(bạn chưa|vui lòng|cho tôi biết)",
                     "error": r"(?i)(lỗi|sự cố|không nhận được)",
                 }.items()}
        flags["rag"] = flags["rag"] and not flags["flight"]  # Only mark rag for ops queries

        results.append({
            "test": name,
            "s": r.status_code,
            "t": elapsed,
            "L": len(full),
            **{k: v for k, v in flags.items()},
            "pv": full[:300],
        })
    except Exception as e:
        results.append({
            "test": name, "s": 0, "t": f"{time.time()-t0:.1f}s",
            "L": 0, "✈️": False, "💰": False, "🏷": False, "📚": False, "❓": False, "❌": True,
            "pv": str(e)[:200],
        })

print(json.dumps(results, ensure_ascii=False, indent=2))

# Summary
passed = sum(1 for r in results if r["✈️"] or r["📚"] or r["❓"])
failed = sum(1 for r in results if r["❌"] and not (r["✈️"] or r["📚"] or r["❓"]))
partial = len(results) - passed - failed
print(f"\n{'='*50}")
print(f"  {passed}/{len(TESTS)} pass  |  {failed} fail  |  {partial} partial")
for r in results:
    status = "✅" if r["✈️"] or r["📚"] else ("⚠️" if r["❓"] else "❌")
    print(f"  {status} {r['test']}: {r['t']}s — {r['pv'][:80]}...")
