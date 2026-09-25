# CEO Response Format — Dashboard Chat

## Vấn đề
CEO trả lời dài không có cấu trúc → user khó đọc, khó theo dõi.

## Giải pháp

### Phía backend (Python)
CEO adapters trả về 4 section riêng qua dict:
```python
{
  "intake": "phân tích...",      # 👔
  "plan": "kế hoạch...",         # 🧭
  "track": "taskboard...",        # 📋
  "dispatch": [{"dept", "status"}] # 🚀
}
```

Không trộn lẫn text. Mỗi section độc lập, JS render riêng.

### Phía frontend (JavaScript)
Dùng `formatCeoResponse()` — line-by-line parser (không regex dump):

| Loại dòng | Format | HTML output |
|-----------|--------|-------------|
| `## Title` | H2 | `<h2>` với border-left accent vàng |
| `### Title` | H3 | `<h3>` vàng |
| `• item` | Bullet | `<li>• text</li>` |
| `| col1 \| col2 \|` | Table row | `<table>` header=th, rest=td |
| `| --- \| --- \|` | Skip | Bỏ qua |
| `✅ text` / `❌ text` | Status | `<div>` inline |
| `------` | HR | `<hr>` |
| `**bold**` | Inline bold | `<strong>` |
| `*italic*` | Inline italic | `<em>` |
| `` `code` `` | Inline code | `<code>` nền #2a2a40 |
| Dòng trống | Spacer | `<br>` |
| Dòng thường | Paragraph | `<p>` margin 4px |

### CSS classes cho chat messages
```css
.msg.assistant .block     # Section header: nền #15152a, border-left 3px accent
.msg.assistant h2          # border-left 3px solid accent, padding-left 8px
.msg.assistant h4          # Muted, uppercase, letter-spacing (dùng cho meta)
.msg.assistant .tag        # Inline badge: font 10px, bg #2a2a40, border-radius 8px
.msg.assistant code        # Inline code: bg #2a2a40, padding 1px 5px, radius 4px
```

### Layout fixes
| Vấn đề | Fix |
|--------|-----|
| Input bị nav che | `.chat-input-wrap` fixed `bottom: var(--nav-height)`, z-index 999 |
| Body padding cứng 70px | CSS var `--nav-height: 64px`, calc() |
| Chat text chui xuống input | `.chat-area` margin-bottom 80px |
| Nav icon không căn giữa | flex column + align-items center + justify-content center |
| Nav desktop xấu | max-width 450px + border-left + border-right + border-radius 12px |
| Office grid mobile | `.agent-grid` grid-template-columns 1fr, desktop 1fr 1fr |

## File cần sửa
- `web/templates/index.html` — toàn bộ CSS + JS + HTML layout
- `agents/ceo/adapters.py` — CEO trả về section riêng, không text trộn
