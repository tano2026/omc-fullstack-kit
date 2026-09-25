# CEO 3-Mode Chat Flow (Jul 2026)

## Origin

User phản hồi "Nó bị hâm mịe rồi. Mày cho nó như một trợ lý đi. Đừng format cứng" — CEO bot trả lời "Alo" bằng bảng delegate có icon. Cần sửa để chat tự nhiên, chỉ phân rã khi được yêu cầu.

## The 3 Modes

Embedded in `main.py` `cmd_natural` system prompt:

**Mode 1 — Chat tự nhiên (mặc định)**
- Trò chuyện như Hermes — hỏi đáp, tư vấn, hỏi lại để làm rõ
- KHÔNG tự ý giao việc, KHÔNG dispatch agent
- Có thể gợi ý nhưng không hành động

**Mode 2 — Phân rã nhiệm vụ** (trigger: "bắt đầu" / "phân rã" / "lên kế hoạch")
- Phân tích nhiệm vụ → đầu việc + gán agent
- TRÌNH LẠI để duyệt — chưa thực hiện

**Mode 3 — Triển khai** (trigger: "duyệt" / "triển khai" / "thực hiện")
- Chạy tác vụ đã duyệt
- Báo cáo kết quả

## System prompt history

| Version | Content | Date |
|---------|---------|------|
| v1 | Bảng delegate với icon | Jul 18 (morning) |
| v2 | 3 chế độ nhưng `\\n` escape sai → `\\\\\\\\n` | Jul 18 (afternoon) |
| v3 | Clean: sạch `\\\\n`, thêm 5 dự án, dùng `---` separator | Jul 18 (evening) |

## Pitfall: `\\n` escaping in Python string concatenation

`main.py` dùng:
```python
system = (
    "Mày là CEO... "
    "\\n\\n"          # -> literal \n\n -> LLM sees "newline newline"
)
```

Trong file Python, `\\n` = 2 ký tự `\` + `n` = LLM hiểu là `\n` (newline).
`\\\\n` = 4 ký tự `\` `\` `\` `n` = LLM thấy `\\n` = text, không xuống dòng.

Đây là trap dễ mắc nhất khi dùng `patch` tool — nếu old_string/new_string chứa `\\`, tool thêm layer khác → `\\\\`. Luôn verify bằng `read_file` dòng 111-132 sau patch.

## File chứa code

`D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core/main.py` — `cmd_natural()` function, dòng 106-141.
