# CEO Confirm Flow — Dashboard Implementation + Telegram Report Tool

## Vấn đề
CEO dispatch tự động ngay sau khi lập kế hoạch → Chủ tịch không kịp review → agent chạy sai hướng.

## Giải pháp
CEO chỉ intake + plan + track → DỪNG lại hỏi Chủ tịch → Chủ tịch confirm → dispatch.

## Backend (web/dashboard.py)

### API endpoint POST /api/chat

```
1. brain.run("intake", message)   → intake_text
2. brain.run("delegate", message)  → plan_text (ghi taskboard)
3. brain.run("track", message)     → track_text
4. Kiểm tra message có phải confirm không:
   confirm_keywords = [
     "ok", "ok ", "ok.", "làm", "làm đi", "làm luôn",
     "triển khai", "triển khai đi", "đồng ý", "ừ", "ừ ",
     "go", "go ahead", "được", "được rồi", "duyệt",
     "chạy", "chạy đi", "chạy luôn", "cho chạy", "dispatch"
   ]
   msg_lower = message.lower().strip()
   is_confirm = any(
     msg_lower == kw or
     msg_lower.startswith(kw + " ") or
     msg_lower.startswith(kw + ",")
     for kw in confirm_keywords
   )
5. CHỈ dispatch nếu is_confirm=True
6. Trả về {intake, plan, track, dispatch, needs_confirm: !is_confirm}
```

### Dispatch mission parsing
```python
if msg_lower.startswith("dispatch "):
    actual_mission = message[len("dispatch "):].strip()
else:
    actual_mission = message
```

Điều này xử lý trường hợp user bấm nút "Duyệt" → frontend gửi "dispatch <lệnh gốc>".

## Frontend (web/templates/index.html)

### confirmAndRun()
```javascript
async function confirmAndRun() {
  const area = document.getElementById('chat-area');
  const msgs = area.querySelectorAll('.msg.user');
  const lastMsg = msgs.length > 0 ? msgs[msgs.length - 1].textContent : '';
  
  document.getElementById('chat-input').value = `dispatch ${lastMsg.substring(0, 150)}`;
  sendChat();
}
```

### Confirm UI
Khi `data.needs_confirm === true`, render:
```html
<div style="background:#2a2a10;border:1px solid var(--accent);border-radius:12px;padding:14px;text-align:center">
  <div>🤔 CEO chờ lệnh Chủ tịch</div>
  <div style="color:var(--muted)">Đã lên kế hoạch và ghi taskboard. Duyệt để triển khai?</div>
  <button onclick="confirmAndRun()">✅ Duyệt — Triển khai</button>
</div>
```

## Test

1. Gõ "làm landing page Fast Track" → CEO trả về intake + plan + track + needs_confirm
2. Nhìn thấy nút vàng "✅ Duyệt — Triển khai"
3. Bấm nút hoặc gõ "ok" → CEO dispatch chạy
4. Gõ "khoan" → CEO chỉ trả về plan, không dispatch
5. Gõ "gửi báo cáo telegram" → CEO gọi telegram_report tool

## Telegram Report Tool

```python
def _ceo_telegram_report(spec, task, sources, adapters, memory):
    """CEO gửi báo cáo qua Telegram."""
    msg = f"👔 *Báo cáo CEO*\n\n{task.topic}"
    
    try:
        from hermes_tools import send_message
        result = send_message(target="telegram", message=msg)
    except ImportError:
        # Hermes tool not available — return text
```

Đăng ký: `reg.register("telegram_report", live.get("telegram_report", _ceo_telegram_report))`

Note: Chỉ hoạt động trong Hermes context (có `hermes_tools` module). Nếu không, trả text nội dung báo cáo.
