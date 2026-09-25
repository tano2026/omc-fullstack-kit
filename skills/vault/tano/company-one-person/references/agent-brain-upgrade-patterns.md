# Agent Brain Upgrade Patterns (Jul 2026)

4 patterns discovered during session where user asked "đánh giá bộ não của bọn nó" and 6 agents got prompt upgrades.

## Pattern 1 — Embed project context into prompts

**When:** Agent needs to know what projects the user runs
**Applies to:** CEO, Sales

**Before:** generic
```
"Phân tích mệnh lệnh của Chủ tịch."
```

**After:** project-aware
```
"Phân tích mệnh lệnh của Chủ tịch.
=== DỰ ÁN HIỆN TẠI ===
1. GMSP — Content Pipeline (Tử Vi + PTBT + Cổ Kim)
2. An Bình Fast Track — Fast Track & Lounge Nội Bài
3. ABTrip — Ticketing máy bay nội địa
4. Tử Vi — AI Engine xem bói Tử Vi

Khi Chủ tịch hỏi thăm, kiểm tra COMPANY_PROJECTS và gợi ý."
```

## Pattern 2 — Tell agents their available tools

**When:** Agent has real tools (terminal, file I/O) but prompt doesn't mention them → agent won't use them
**Applies to:** Dev

**Before:** tool-blind
```
"Mày là software architect. Từ yêu cầu, đưa: kiến trúc module..."
```

**After:** tool-aware
```
"Mày là software architect. ...
=== TOOL CỦA MÀY ===
- _real_repo(): tìm code cũ trong D:/MMO Du an/ trước khi viết mới
- _tool_terminal(): chạy terminal thật — pip install, git, py_compile, pytest
- _tool_write_file(): ghi file thật — LUÔN validate path tồn tại trước khi ghi
- _real_build(): tạo file code + test — viết test/test_*.py TRƯỚC, code thật SAU
- TDD: tạo file test trước, code sau. Chạy pytest để verify."
```

## Pattern 3 — Embed brand/system rules

**When:** Agent writes content that needs consistent brand voice
**Applies to:** Marketing, Sales

**Before:** generic
```
"Mày là content writer Việt Nam. Viết content theo brief..."
```

**After:** brand-embedded
```
"Mày là content writer Việt Nam. ...
=== BRAND VOICE ===
- Brand chính: Giải Mã Số Phận — đen #0D0D12 + vàng #FFD700 + đỏ #8B0000
- Giọng điệu: gai góc, từng trải, brutal truth, dễ hiểu
- Công thức: truth opening → hidden system → urgency → giải pháp
- 3 domain dùng chung brand, chỉ khác accent: Tử Vi=vàng+đỏ, PTBT=xanh lá, Cổ Kim=nâu đất"
```

## Pattern 4 — Embed pipeline knowledge

**When:** Agent needs to understand a multi-step pipeline to give useful advice
**Applies to:** Media video_pipeline

**Before:** too vague
```
"Mày là video producer. Từ brief: kịch bản timeline..."
```

**After:** pipeline-embedded
```
"Mày là video producer. ...
=== PIPELINE GMSP ===
Pipeline: Research → Script → TTS → Media → Render → Publish → Social
7 bước, mỗi bước độc lập, input/output qua file.
=== QUY TẮC ===
- Hook 3s đầu — shock, curiosity, hoặc brutal truth
- 1 giọng duy nhất xuyên suốt (ko trộn TTS voices)
- Ko BGM — chỉ voiceover
- Mỗi scene 1 ảnh AI riêng (dark academia style)
- Ko có hiệu ứng zoompan — dùng scale+crop thay thế
- SRT phụ đề tiếng Việt"
```

## Pattern 5 — Sales target context

**When:** Sales agent needs to know what the company sells to who
**Applies to:** Sales lead_analyzer

```
=== DỰ ÁN MỤC TIÊU ===
- An Bình Fast Track: B2B travel, hotel/DMC partnership
- GMSP: đối tác content, KOL, platform
- ABTrip: travel agency, đại lý bán vé máy bay
```

## Implementation

All patterns go into `llm.make_analyzer(system_prompt=...)` in the agent's `adapters.py` `build_registry()` function.

Python code strategy:
```python
reg.register("adapter_name", live.get("adapter_name") or llm.make_analyzer(
    system_prompt=(
        "Role description..."
        "=== SECTION ===\n"
        "- Key fact 1\n"
        "- Key fact 2\n"
    ),
    fallback=_fallback_function
))
```

## Guard: File I/O Safety (Dev)

`_is_allowed_path(path)` — 2-tier guard:

1. **Block list check** — starts with Windows/Program Files/System32/etc → 🚫
2. **Allow list check** — resolved path under D:/MMO Du an, Desktop, Documents, home → ✅

```python
_ALLOWED_ROOTS = [
    Path("D:/MMO Du an"),
    Path("C:/Users/Nguyen Ngoc Tan/Desktop"),
    Path("C:/Users/Nguyen Ngoc Tan/Documents"),
    Path.home(),
]
_BLOCKED_PREFIXES = [
    "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
    "System32", "C:\\$Recycle.Bin", "C:\\System Volume Information",
    "C:\\ProgramData",
]

def _is_allowed_path(path: str) -> tuple:
    p = Path(path).resolve()
    p_str = str(p).lower()
    for blocked in _BLOCKED_PREFIXES:
        if p_str.startswith(blocked.lower()):
            return False, f"🚫 Path bị chặn: {blocked}"
    for root in _ALLOWED_ROOTS:
        try:
            p.relative_to(root)
            return True, ""
        except ValueError:
            continue
    return False, f"🚫 Path không nằm trong vùng an toàn"
```

`_tool_write_file()` và `_tool_read_file()` gọi `_is_allowed_path()` đầu function. `_tool_terminal()` không guard — vẫn chạy cmd shell tự do.

## Rule of thumb

If you can remove the prompt and the agent still knows what to do because of the code, the prompt is redundant.
If you can remove the code and the prompt still tells the agent what to do, the code is redundant.
The prompt should carry KNOWLEDGE the agent can't derive from its training or from code logic alone.
