# Dashboard: Agent Profile Modal Pattern (v4, 19/07/2026)

## Kiến trúc 4-tab "Văn Phòng Đại Lý"

| Tab | Content | API | Notes |
|-----|---------|-----|-------|
| 🏢 **VP** | 9 agent cards grid (2-col mobile, 3-col desktop) | /api/kanban filter by owner | Agent accent colors per role |
| 📋 **Bảng Tin** | Live feed of all non-idle kanban tasks | /api/kanban | auto-refresh 30s |
| 🏛️ **Phòng Họp** | 5 project cards + weekly plan + health alerts | /api/projects, /api/health | |
| 💬 **Chat** | CEO chat with SQLite persistence | /api/chat | session_id grouping |

## Agent Profile Modal — 5 mandatory sections

When user clicks any agent card, show a FULL-PAGE scrollable modal (position:fixed, overflow-y:auto, max-height:100vh, overscroll-behavior:contain):

1. **👤 Tôi là ai** — Vietnamese introduction
2. **🎯 Nhiệm vụ của tôi** — mission
3. **🛠️ Tôi có gì** — tools (tag chips) + skills
4. **📋 Tôi đang làm gì** — fetch /api/kanban, filter by owner
5. **💬 Chat trực tiếp** — button: closeModal(), switchTab('chat'), pre-fill "/agent_name "

### CRITICAL: Scrollability
- `position:fixed` modal with `overflow-y:auto; max-height:100vh; overscroll-behavior:contain`
- User MUST be able to scroll to the bottom (Chat button)
- First version failed because modal wasn't scrollable → user complained

## Task Click Modal (Bảng Tin) — 2 action buttons

When user clicks a task card in Bảng Tin:

### Section 1: Details
- Agent icon + name + task title (colored by agent accent)
- Title, owner, state, created_at timestamp

### Section 2: State change
- `<select>` dropdown with all states (ready/running/review/blocked/done)
- "✅ Cập nhật" button → POST /api/kanban/move

### Section 3: Action buttons

**"💬 Chỉ đạo trực tiếp"**
- Closes modal, switches to Chat tab
- Pre-fills input with "/<owner> <task title>"
- User types their message and sends manually

**"🤝 Giao CEO xử lý"**
- Sends command via POST /api/chat DIRECTLY (no tab switch)
- Shows toast notification with CEO response preview
- Toast auto-dismisses after 4 seconds
- Fallback: if API fails, switch to Chat tab

```javascript
async function assignToCEO(title) {
  closeModal(null);
  const msg = '/ceo Giao nhiệm vụ: ' + title + '. Báo cáo tiến độ và kết quả.';
  const data = await API.post('/api/chat', {message: msg, session_id: 'dashboard_assign'});
  if (data.ok && data.response) {
    // Show toast
    const toast = document.createElement('div');
    toast.style.cssText = '...';
    toast.innerHTML = '✅ Đã giao CEO xử lý: <strong>' + title + '</strong><br>...';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  } else {
    // Fallback: switch to chat
    switchTab('chat');
    document.getElementById('chat-input').value = msg;
  }
}
```

## Project Click Modal (Phòng Họp) — 2 action buttons

When user clicks a project card:

### Section 1: Details
- Project name + icon + status badge
- Path (monospace)
- Related tasks (filter /api/kanban cards whose title contains project name)

### Section 2: Action buttons

**"💬 Yêu cầu CEO"**
- Pre-fills chat with "/ceo báo cáo tiến độ <project>"
- Auto-sends after 300ms

**"📋 Thêm nhiệm vụ"**
- prompt() for task title
- POST /api/kanban/add with owner="ceo", state="ready"
- Refreshes kanban + modal
