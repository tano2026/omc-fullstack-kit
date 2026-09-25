# Dashboard Inline Chat Pattern (v4, 19/07/2026)

User complained that clicking "Giao CEO xử lý" kicked them to the chat tab instead of executing silently. Also wanted to chat CEO directly inside modals without navigating away.

## Mini chat inside task/project modals

Every task detail modal (from Bảng Tin) and project detail modal (from Phòng Họp) has an inline chat box at the bottom:

```html
<div class="modal-section">
  <div class="modal-section-title">💬 Chat CEO</div>
  <div id="modal-chat-msgs" style="max-height:120px;overflow-y:auto;..."></div>
  <div style="display:flex;gap:6px;">
    <input type="text" id="modal-chat-input" placeholder="Nhắn CEO..." 
           onkeydown="if(event.key==='Enter')sendModalChat()">
    <button onclick="sendModalChat()">Gửi</button>
  </div>
</div>
```

Since both task and project modals use the same container (`#modal-full-inner`), the chat input IDs (`#modal-chat-input`, `#modal-chat-msgs`) can be reused — only one modal is open at a time.

Session ID: `'modal_' + Date.now()` — unique per modal open, so chat history is per-modal-view.

## "Giao CEO xử lý" — API direct call

No tab switch. Calls `/api/chat` directly, shows a toast with CEO's response:

```javascript
async function assignToCEO(title) {
  closeModal(null);
  const msg = '/ceo Giao nhiệm vụ: ' + title + '. Báo cáo tiến độ và kết quả.';
  const data = await API.post('/api/chat', {message: msg, session_id: 'dashboard_assign'});
  if (data.ok && data.response) {
    // Toast notification
    const toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;bottom:90px;left:16px;right:16px;max-width:400px;margin:0 auto;background:#16161F;border:1px solid var(--gold);border-radius:12px;padding:14px 18px;color:var(--text);font-size:13px;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,0.5);animation:fadeIn 0.3s ease';
    toast.innerHTML = '✅ Đã giao CEO xử lý: <strong>' + escapeHtml(title) + '</strong><br><span style="color:var(--text-muted);font-size:11px;">' + escapeHtml(data.response.substring(0, 150)) + '</span>';
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.3s'; setTimeout(() => toast.remove(), 300); }, 4000);
  } else {
    // Fallback: navigate to chat tab
    switchTab('chat');
    document.getElementById('chat-input').value = msg;
  }
}
```

## "Chỉ đạo trực tiếp" — stays old flow

Just navigates to chat tab with pre-filled `/agent_name task_title`:

```javascript
function directChatTask(owner, title) {
  closeModal(null);
  switchTab('chat');
  document.getElementById('chat-input').value = '/' + owner + ' ' + title;
  document.getElementById('chat-input').focus();
}
```

## JS template string escaping

When constructing onclick attributes inside template literals, `escapeHtml()` would double-encode. Instead use `c.title.replace(/'/g, "\\'")` to prevent single-quote breakage:

```javascript
// Instead of:
onclick="assignToCEO('${escapeHtml(c.title)}')"
// Use:
onclick="assignToCEO('${c.title.replace(/'/g,"\\'")}')"
```
