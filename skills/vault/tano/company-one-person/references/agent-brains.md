# Agent Brains — Full Audit & Upgrade Guide

## 3 Levels of Agent Intelligence

| Level | What | When | Cost |
|-------|------|------|------|
| Brain prompt | Edit `system_prompt=` string | Agent gives wrong answers/tone/format | 0 code, edit string + restart |
| Code logic | Add Python validation/parsing/fallback | Agent hallucinates or ignores data | 10-50 lines |
| Real tools | Add terminal/file/web/DB access | Agent knows what to do but can't do it | 50-200 lines |

## Pitfall: Adapter registry ≠ spec task_types

**Problem:** Adding a function to the adapter registry (`reg.register("initiative", ...)`) does NOT make it callable via `brain.run("initiative", ...)`. The brain reads `spec.task_types` first — it only dispatches to task types declared there.

**Fix:** Both steps required:
1. Register the function in `build_registry()` — `reg.register("initiative", live.get("initiative", _ceo_initiative))`
2. Add the task type in spec.py — `SPEC.task_types["initiative"] = {...}`
3. The `"analyze"` field in spec must match the registry name (e.g. `"analyze": "initiative"`)

Without step 2 → `brain.run('initiative', ...)` returns `"không hỗ trợ task type 'initiative'. Có: ['delegate', 'intake', 'report', 'track']"`

## Before/After: Jul 2026 Upgrade

### 👔 CEO — project-aware
**Before:**
```python
"Mày là CEO trợ lý của TANO-AGENCY. Phân tích mệnh lệnh của Chủ tịch..."
```
**After:**
```python
"...=== DỰ ÁN HIỆN TẠI ===
1. GMSP — Content Pipeline (Tử Vi + PTBT + Cổ Kim)
2. An Bình Fast Track — Fast Track & Lounge Nội Bài
3. ABTrip — Ticketing máy bay nội địa
4. Tử Vi — AI Engine xem bói

Khi Chủ tịch hỏi thăm, kiểm tra COMPANY_PROJECTS và gợi ý dự án cần kickstart."
```
**Plus in planner:**
```python
"...LƯU Ý: Nếu liên quan tới 4 dự án chính (GMSP, Fast Track, ABTrip, Tử Vi),
ưu tiên Dev (code) + Media (ảnh/video) + Research (thị trường)."
```

### 💻 DEV — tool-aware
**Before:**
```python
"Mày là software architect. Từ yêu cầu, đưa: kiến trúc module + file layout..."
```
**After:**
```python
"...=== TOOL CỦA MÀY ===
- _real_repo(): tìm code cũ trong D:/MMO Du an/ trước khi viết mới
- _tool_terminal(): chạy terminal thật — dùng pip install, git, py_compile, pytest
- _tool_write_file(): ghi file thật — LUÔN validate path tồn tại trước khi ghi
- _real_build(): tạo file code + test — viết test/test_*.py TRƯỚC, code thật SAU
- TDD: tạo file test trước, code sau. Chạy pytest để verify."
```

### 🛒 SALES — new lead_analyzer
**Before:** only copywriter brain
**After (added new brain):**
```python
reg.register("lead_analyzer", live.get("lead_analyzer") or llm.make_analyzer(
    "Mày là sales analyst. Từ kết quả search lead, đánh giá từng lead: "
    "ngành nghề có phù hợp không, quy mô, nhu cầu khả năng cao/thấp, "
    "recommend action (call/email/skip). "
    "Output bảng: | Lead | Ngành | Fit | Nhu cầu | Action |
    ...
    === DỰ ÁN MỤC TIÊU ===
    - An Bình Fast Track: B2B travel, hotel/DMC partnership
    - GMSP: đối tác content, KOL, platform
    - ABTrip: travel agency, đại lý bán vé máy bay"
))
```

### 📢 MARKETING — brand-embedded
**Before:**
```python
"Mày là content writer Việt Nam. Viết content theo brief..."
```
**After:**
```python
"...=== BRAND VOICE ===
- Brand chính: Giải Mã Số Phận — đen #0D0D12 + vàng #FFD700 + đỏ #8B0000
- Giọng điệu: gai góc, từng trải, brutal truth, dễ hiểu
- Công thức: truth opening → hidden system → urgency → giải pháp
- 3 domain dùng chung brand, chỉ khác accent: Tử Vi=vàng+đỏ, PTBT=xanh lá, Cổ Kim=nâu đất"
```

### 🎬 MEDIA — pipeline-embedded
**Before:**
```python
"Mày là video producer. Từ brief: kịch bản timeline, voice-over tiếng Việt, gợi ý footage, format, nhạc."
```
**After:**
```python
"...=== PIPELINE GMSP ===
Pipeline chuẩn: Research → Script → TTS → Media → Render → Publish → Social
7 bước, mỗi bước độc lập, input/output qua file.

=== QUY TẮC ===
- Hook 3s đầu — shock, curiosity, hoặc brutal truth
- 1 giọng duy nhất xuyên suốt (ko trộn TTS voices)
- Ko BGM — chỉ voiceover
- Mỗi scene 1 ảnh AI riêng (dark academia style)
- Ko có hiệu ứng zoompan — dùng scale+crop thay thế
- SRT phụ đề tiếng Việt"
```

## Anatomy of a Good Agent Prompt

```
[ROLE — who they are] "Mày là CEO trợ lý / software architect / sales analyst..."
[CONSTRAINTS — hard rules] "TUYỆT ĐỐI không bịa số", "Không tự động dispatch"
[OUTPUT FORMAT — parseable] "Trả về bảng: | STT | phòng ban | việc | P1/P2/P3 |"
[TOOL AWARENESS — what they can do] "=== TOOL CỦA MÀY ==="
[DOMAIN KNOWLEDGE — what they must know] "=== DỰ ÁN HIỆN TẠI ===" / "=== BRAND VOICE ===" / "=== PIPELINE GMSP ==="
[FALLBACK — what to do when stuck] "Nếu không xử lý được → escalate"
```

## When to Upgrade Which Level

**User says "thằng này ngu":**
1. Check brain prompt first (easiest, 0 code)
2. If prompt is fine but agent ignores it → add code logic (parsing, validation, guards)
3. If agent knows what to do but can't → add real tools (terminal, write_file, web search)

**User says "ko biết dự án của tao":**
→ Pattern 1 — embed project context into prompt (CEO, Sales)

**User says "nó cứ tạo file sai chỗ":**
→ Pattern 2 — tell Dev its available tools + validate path in prompt

**User says "content ko đúng giọng":**
→ Pattern 3 — embed brand voice into prompt (Marketing)

**User says "ko biết pipeline video":**
→ Pattern 4 — embed pipeline knowledge into prompt (Media)

## Session Link

Full prompt upgrade session Jul 2026: https://hermes.nousresearch.com/chat/session-20260718-brain-upgrades
