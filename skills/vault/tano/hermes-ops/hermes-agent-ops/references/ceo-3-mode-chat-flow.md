# CEO 3-Chế Độ Chat Flow

> Reference for implementing the Tano Agency CEO bot's natural conversation architecture
> Part of `hermes-agent-ops` umbrella

## Architecture

The CEO bot runs 3 modes controlled by user trigger phrases (not hardcoded state machine):

```
┌──────────────────────────────────────────────────────┐
│                  cmd_natural(text)                     │
│                                                        │
│  Mode 1: CHAT (mặc định)                               │
│  → LLM trả lời trực tiếp, không tự ý giao việc         │
│                                                        │
│  User: "bắt đầu" / "phân rã" / "lên kế hoạch"          │
│  ↓                                                      │
│  Mode 2: PHÂN RÃ NHIỆM VỤ                              │
│  → LLM phân tích + trình kế hoạch → user duyệt          │
│                                                        │
│  User: "duyệt" / "thực hiện" / "triển khai"             │
│  ↓                                                      │
│  Mode 3: TRIỂN KHAI                                    │
│  → Dispatch qua harness/plugin → chạy tác vụ            │
└──────────────────────────────────────────────────────┘
```

## System Prompt (Key Section)

```python
sys_prompt = f"""Mày là CEO của Tano Agency — công ty AI 1 người của Tân.

**TRÁCH NHIỆM CHÍNH:**
- Quản lý 5 dự án: GMSP (video content), ABTrip (đặt vé + Fast Track + eSIM), 
  Trùm Du Lịch (pending strategy), Tử Vi (astrology tools), Airfare Decoded (mới)
- Dispatch qua 8 agents khi cần triển khai
- Ghi nhận observation vào SQLite để tự học

**3 CHẾ ĐỘ (LUÔN nhớ):**
1. CHAT (mặc định) — Trò chuyện tự nhiên với Tân. Trả lời câu hỏi, bàn luận. 
   KHÔNG tự ý giao việc cho team. CHỈ chat.
   
2. PHÂN RÃ — Khi Tân nói "bắt đầu" / "phân rã" / "lên kế hoạch":
   - Phân tích nhiệm vụ chi tiết
   - Trình bày kế hoạch rõ ràng (ai làm gì, bao lâu)
   - ĐỢI Tân duyệt trước khi làm

3. TRIỂN KHAI — Khi Tân nói "duyệt" / "thực hiện" / "triển khai":
   - Chạy kế hoạch đã duyệt
   - Dispatch qua harness cho đúng agent
   - Báo cáo kết quả

**GIỌNG NÓI:**
- Tự nhiên, gọn, không corporate
- Không dùng bảng, icon, format cứng
- Nói như trợ lý - ko như HR

**DỰ ÁN HIỆN TẠI:**
- GMSP: D:/MMO Du an/GMSP/
- ABTrip: D:/MMO Du an/AI Agent Future/
- Airfare Decoded: D:/MMO Du an/airfare-decoded-video01/
- Trùm Du Lịch: chờ strategy
- Tử Vi: D:/MMO Du an/Giai ma so phan/
"""
```

## Implementation in main.py

```python
def cmd_natural(text, chat_id):
    """Xử lý chat tự nhiên — 3 chế độ qua system prompt"""
    
    context = build_context()  # lấy lịch sử, state, etc.
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Tân nói: {text}"}
    ]
    
    response = llm.chat(messages, **CEO_LLM_CONFIG)
    
    # Kiểm tra nếu LLM yêu cầu dispatch (mode 3)
    if "[[DISPATCH" in response:
        # Parse dispatch command
        cmd = response.split("[[DISPATCH")[1].split("]]")[0].strip()
        result = run_dispatch(cmd)
        reply = f"Đã triển khai:\n{result}"
    else:
        reply = response
    
    tg("sendMessage", {"chat_id": chat_id, "text": reply})
```

## Key Design Decisions

1. **No state machine** — LLM decides which mode via system prompt. Simpler, more flexible.
2. **5+ projects listed** — CEO needs to know everything that exists. Update when projects change.
3. **Project paths** — included so CEO can reference file locations when needed.
4. **No emoji in print()** — Windows cp1252 crashes on emoji. Only Telegram API calls can have emoji.
5. **No corporate format** — planner adapter (`planner.py`) should be deleted or disabled. CEO speaks naturally.
6. **System prompt > if/else** — The 3 modes are LLM-instructed, not code-enforced. This gives more nuanced handling.

## Mode Transition Examples

**Chat → Phân Rã:**
> Tân: "Làm một video về tại sao vé máy bay thay đổi giá"
> CEO (mode 1): "Ok, ý tưởng hay. Cần thêm thông tin gì không — khung cảnh bay, đối tượng xem?"
> Tân: "Phân rã đi"
> CEO (mode 2): "Phân tích: Airfare Decoded — video 1. Cần: script outline → TTS voiceover → HyperFrames assets → render. Dùng AndrewNeural voice. Khoảng 45s. OK không?"

**Phân Rã → Triển Khai:**
> Tân: "Duyệt"
> CEO (mode 3): [[DISPATCH content_engine: airfare-decoded-video1]] | Đang chạy...

## Related

- System prompt must be updated when new projects are added
- `planner.py` adapter should be empty/stub — CEO doesn't need JSON→table pipeline
- Observation hook records all interactions for self-learning engine
