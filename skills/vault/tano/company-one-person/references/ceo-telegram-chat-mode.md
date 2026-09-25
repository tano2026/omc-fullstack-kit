# CEO Telegram Chat Mode

## Kiến trúc chat (chốt 18/07/2026)

User chat with @Tano_CEO_bot → `main.py/handle()` → `cmd_natural()` → 1 LLM call.

**KHÔNG còn Harness loop.** Không còn pipeline 6 bước. Không còn dispatch.

## Code pattern

```python
def cmd_natural(chat_id, text):
    t0 = time.time()
    send(chat_id, "CEO dang nghi...")
    
    system = (
        "Mày là CEO TANO-AGENCY — trợ lý AI của chủ tịch Nguyễn Ngọc Tân. "
        "CHỈ TRẢ LỜI CÂU HỎI. "
        "KHÔNG tự ý giao việc, KHÔNG dispatch, KHÔNG ra lệnh cho ai. "
        "Khi chủ tịch nói \"bắt đầu\" hoặc \"triển khai\" hoặc \"giao\" "
        "thì mới viết: 📋 Giao: <phòng ban>: <việc>"
    )
    
    out = llm.chat(text, system=system, task_type="chat", max_tokens=1000, timeout=30)
    if out:
        send(chat_id, out)
    else:
        send(chat_id, "CEO ko tra loi duoc. Thu /agents")
```

## Budget history

| Version | Budget | Time/msg | Ghi chú |
|---------|--------|----------|---------|
| v1 (old) | `Harness(Budget(max_iters=2, max_tokens=12000, max_sec=180))` + `run_all_pending()` | ~240s | LLM 6-pipeline + dispatch xuống agent khác |
| v2 (fix chậm) | `Harness(Budget(max_iters=1, max_tokens=2000, max_sec=15))` + try/except | ~12s | Vẫn còn Harness, vẫn còn dispatch |
| v3 (final) | `llm.chat()` 1 call, ko Harness, ko dispatch | ~3s | Chat thuần, ko pipeline, ko giao việc |

## Rules

1. **1 LLM call** — `llm.chat(text, system=...)`. Ko Harness, ko brain.run, ko pipeline.
2. **System prompt** — được set inline trong `cmd_natural()`, không lấy từ agent spec.
3. **No dispatch** — KHÔNG có `run_all_pending()` hay bất kỳ code nào gọi agent khác sau chat.
4. **User must say "bắt đầu" / "triển khai" / "giao"** để CEO mới output `📋 Giao: <agent>: <task>` — chỉ là text, ko thực thi.

## File modified

`main.py` — function `cmd_natural()`. Toàn bộ logic chat nằm trong 1 function.
