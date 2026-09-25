# CEO Chat Rules — Corrected Behaviors

## Rule 1: CHỈ trả lời, KHÔNG tự dispatch

**Correction source:** User multiple times said bot "cứ nói 1 câu là lại chạy đi giao việc 1 loạt".

**Trigger:** User sent a normal message (no slash command, no "bắt đầu").

**Old behavior:** `cmd_natural()` → Harness(brain=ceo) → pipeline → `run_all_pending()` — CEO auto-dispatched to all agents.

**Correct behavior:** `cmd_natural()` → `llm.chat(text, system=CEO_SYSTEM)` — 1 LLM call, no dispatch, no pipeline.

**System prompt must contain:**
```
CHỈ TRẢ LỜI CÂU HỎI.
KHÔNG tự ý giao việc, KHÔNG dispatch, KHÔNG ra lệnh cho ai.
Khi chủ tịch nói "bắt đầu" hoặc "triển khai" hoặc "giao"
thì mới viết: 📋 Giao: <phòng ban>: <việc>
```

## Rule 2: 1 LLM call, không Harness

**Trigger:** Any normal chat message.

**Pattern:**
- ❌ `Harness(brain).run("delegate", text)` + `run_all_pending()` → 240s
- ❌ `Harness(brain).run("delegate", text)` (1 iteration, no dispatch) → 12s
- ✅ `llm.chat(text, system=..., task_type="chat")` → 3s

## Rule 3: Token cost là không đáng kể

Mỗi message: ~500 input tokens + ~300 output tokens × $0.14/1M ≈ $0.0001/msg.

## File: `main.py` → function `cmd_natural()`
