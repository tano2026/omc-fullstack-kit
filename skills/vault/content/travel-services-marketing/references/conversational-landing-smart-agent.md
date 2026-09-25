# Conversational Landing Page — Smart Agent (Tham Khảo)

> Xây dựng cho dự án **Smart Agent** (ABTrip Platform), tháng 7/2026.
> Server live port 6969, route `/` serve `main.html`.

## Ngữ Cảnh

User yêu cầu: "trang chủ đặt vé thiết kế dạng kiểu một trang như ChatGPT và đặt dịch vụ theo kiểu ngôn ngữ tự nhiên thay vì phải chọt chọt"

## Kiến Trúc

```
HTML single-file (26KB)
├── Header (sticky, blur) — logo + nút "Đặt ngay" scroll to chat
├── Chat Messages (flex-1, scrollable)
│   ├── Welcome Screen (ẩn khi có message)
│   │   ├── Icon + h1 "Nói 1 câu, AI lo hết"
│   │   └── 5 Suggestion Pills
│   └── Message Bubbles
│       ├── user — avatar T + bubble inverted
│       └── assistant — avatar S + bubble white + border
│           └── Result Cards (flight search / Fast Track / eSIM)
├── Chat Input
│   ├── Quick Tools bar (4 nút: vé/FT/eSIM/Visa)
│   ├── Textarea + Send button
│   └── Footer note
```

## Server Integration

- FastAPI route `/` → `templates/main.html`
- SSE streaming: `POST /api/smart-agent/chat` → stream events `{type, content, step, data, session_id}`
- Result cards render từ event data (phải có `step` + `data` payload)

## Taste-Frontend Applied

| Rule | Implementation |
|------|---------------|
| Font | Plus Jakarta Sans (Google Fonts) |
| Background | #FAF8F5 (warm beige, ko pure white) |
| Surfaces | #FFFFFF + border #E8E2D8 |
| Shadows | 0 1px 3px rgba(0,0,0,0.04) [ultra-light] |
| Gold accent | #D4A843 primary, #B8860B dark |
| No rounded-full | radius 14px (chat bubble), 50% (avatar) |
| No gradients | flat colors (trừ gold btn) |
| No glassmorphism nặng | 8px blur on header only |

## Code Hay

### Welcome + Messages mutual exclusion
```css
.chat-messages:empty + .welcome { display: flex; }
.chat-messages:not(:empty) + .welcome { display: none; }
```

### Typing indicator (pure CSS)
```css
.typing-indicator span {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--text-muted);
  animation: pulse 1.2s infinite;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
```

### Suggestion pills trigger
```javascript
function sendSuggestion(text) {
  chatInput.value = text
  sendBtn.disabled = false
  sendMessage()
}
```

## Lessons Learned

1. **User prefers chat over forms** — even for complex travel booking. Don't default to input fields + submit buttons. Start with "nói 1 câu" mental model.
2. **Suggestion pills are critical** — they teach the user HOW to talk to the AI. Bad pills = user stuck.
3. **Quick tools bar > navigation** — 4 buttons above input beats 5 menu items in header. Lower friction.
4. **Card rendering in chat** — flight lists, Fast Track packages, eSIM plans all inline. No page navigation needed.
5. **SEO sacrifice** — conversational UI is JS-rendered, harder to crawl. Accept this trade-off for conversion speed.
