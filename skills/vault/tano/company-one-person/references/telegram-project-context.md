# Telegram CEO Bot — Per-Project Context Detection

**Critical fix (19/07/2026):** CEO bot on Telegram confused projects — talking about Airfare would veer into GMSP because it used a single generic system prompt.

## Solution: Detect project from message text + inject per-project context

### Step 1 — Project keyword map

In `main.py`, define `PROJECT_NAMES`:

```python
PROJECT_NAMES = {
    "gmsp": "GMSP", "giải mã": "GMSP", "giai ma": "GMSP",
    "abtrip": "ABTrip", "ab trip": "ABTrip",
    "tử vi": "Tử Vi", "tu vi": "Tử Vi", "bói": "Tử Vi",
    "airfare": "AirFares Decoded", "airfare decoded": "AirFares Decoded", "airfares": "AirFares Decoded",
    "fast track": "Fast Track", "nội bài": "Fast Track", "noi bai": "Fast Track",
    "trùm du lịch": "ABTrip", "trùm sân bay": "Fast Track",
}
```

### Step 2 — Detect function

```python
def _detect_project(text: str) -> str | None:
    lower = text.lower()
    for kw, proj in PROJECT_NAMES.items():
        if kw in lower:
            return proj
    return None
```

### Step 3 — Inject project context into system prompt

```python
def cmd_natural(chat_id, text):
    project = _detect_project(text)
    project_context = ""
    if project:
        project_context = build_project_context(project)
    
    base_system = "...standard CEO system..."
    
    if project:
        base_system += f"=== DỰ ÁN HIỆN TẠI: {project} ===\n"
        if project_context:
            base_system += project_context + "\n\n"
        base_system += (
            "QUY TẮC RIÊNG CHO DỰ ÁN NÀY:\n"
            "1. Chỉ trả lời về dự án được hỏi, KO lẫn sang dự án khác.\n"
            "2. Khi biết thông tin mới, viết: [LƯU FACT: nội dung] [CATEGORY: contact/note/link]\n"
            "3. Khi có quyết định, viết: [QUYẾT ĐỊNH: nội dung]\n"
        )
    else:
        base_system += "...list all 5 projects..."
    
    # Also include skills
    if skills_str:
        base_system += f"\n=== KỸ NĂNG CÓ THỂ DÙNG ===\n{skills_str}\n"
```

### Step 4 — Save chat + auto-extract facts

```python
save_chat(project, "user", text)
save_chat(project, "assistant", out or "")

if project:
    extract_facts_from_message(project, text)
    for line in (out or "").split("\n"):
        if "[LƯU FACT:" in line:
            # Parse and save
            ...
        if "[QUYẾT ĐỊNH:" in line:
            # Parse and save
            ...
```

### Step 5 — Import project_memory

```python
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard"))
from project_memory import (
    save_chat, load_chat_history,
    add_fact, get_facts, search_facts,
    add_decision, get_decisions,
    build_project_context, extract_facts_from_message,
)
```

### Key principles

1. **Detect earliest** — check project before LLM call, not after
2. **Isolate context** — each project gets its OWN system prompt with ONLY its facts
3. **Same DB** — Telegram bot and web dashboard share `project_memory.db` at `PLATFORM/agent-core/data/project_memory.db`
4. **Auto-save** — facts from both user (email/phone/URL regex) and CEO (`[LƯU FACT]` bracket syntax)
5. **No project mentioned → use global_chat** — don't assume context

### Pitfalls

- **`'\"` string escaping** — when patching `cmd_natural` via `patch` tool, double-backslash escaping is fragile. Always verify by reading the file after patch.
- **`base_system += f"...{variable}..."`** — f-strings work inside `+` concatenation. Don't mix with `\\\\n` legacy patterns.
- **`build_project_context()` can be empty** — if no facts/decisions stored yet, returns "Chưa có thông tin về dự án này." — still valid context.
