# TANO-AGENCY Dashboard v3.0 — Single-Screen SAAS Design

## Architecture Overview

Single HTML page served by FastAPI, no SPA framework. JS manages state + fetch from API.

## Layout: 4 Zones

### 1. Header (sticky top)
```
TANO.AGENCY          📁 5/5  📋 3/10  🟢 OK
```
- Project count: active/total
- Task count: running/total
- Health dot: green/yellow/red

### 2. Sidebar (left, 180px on desktop)
```
Phòng ban
👔 CEO
💻 Developer
🎯 Sales
📢 Marketing
⚙️ Operations
🎧 Support
📊 Analytics
🎨 Media
🔬 Research
──────────────
Chung
🏠 Tất cả
```
- Click = filter task feed by agent
- Active state = gold background
- Mobile (≤480px): collapses to 50px, labels hidden

### 3. Task Feed (center, scrollable)
```
📋 Công việc

[💻 icon] Landing Page GMSP
          Developer · 2h ago          [🟢 Đang chạy]

[🎯 icon] KPI tháng 7
          Sales · 1ng ago             [🟡 Review]
```
- Cards sorted by priority: running > ready > review > blocked > backlog > done
- Each card: agent avatar (36px, colored bg) + title + meta (name + time ago) + state badge
- Click = opens bottom-sheet modal

### 4. Chat Bar (fixed bottom)
```
┌─────────────────────────────────────┐
│ 💬 Nhắn CEO...                [➤]  │
└─────────────────────────────────────┘
```
- Always visible on every screen
- Enter to send, loading indicator during response
- Toast notification for CEO reply

## Modal (bottom-sheet)

Triggered by clicking any task card:

```
┌─────────────────────────────────────┐
│ ─── (handle bar)                     │
│                                      │
│ [💻 icon] Landing Page GMSP          │
│           Developer                  │
│                                      │
│ TRẠNG THÁI                           │
│ [🟢 Đang chạy ▼]                     │
│ [✅ Cập nhật]                        │
│                                      │
│ THÔNG TIN                            │
│ Tạo lúc: 19/07/2026 14:30            │
│                                      │
│ [🤝 Giao CEO]  [💬 Chỉ đạo]          │
│                                      │
│ 💬 Chat CEO                          │
│ ┌─────────────────────────────────┐  │
│ │ CEO đang nghĩ...                │  │
│ └─────────────────────────────────┘  │
│ ┌────────────────────┐ [Gửi]         │
│ │                    │                │
│ └────────────────────┘                │
└─────────────────────────────────────┘
```

- 85vh max height, scrollable
- State selector + update button calls POST /api/kanban/move
- "🤝 Giao CEO" → calls API directly, shows toast, stays on page
- "💬 Chỉ đạo" → fills chat bar with /agent prefix, switches focus
- Inline chat → separate session per modal, bubble layout

## Quick Tools (floating buttons, bottom-right)

3 buttons stacked:

| Icon | Action | Result |
|------|--------|--------|
| 📋 | showNewTaskModal() | Modal với form: title + phòng ban + ưu tiên → POST /api/kanban/add |
| 📊 | showReportModal() | Modal: system health + task stats + project status + "Yêu cầu CEO" |
| 🏛️ | sendChat('/ceo họp khẩn') | Gửi lệnh họp CEO qua API chat |

## Theme

User explicitly chose and praised **light theme**:

```css
:root {
  --bg: #F5F5F7;
  --card: #FFFFFF;
  --card-hover: #EBEBF0;
  --border: #D4D4D8;
  --text: #1A1A2E;
  --text-muted: #6B6B80;
  --gold: #B8860B;
  --green: #16A34A;
  --red: #DC2626;
  --yellow: #CA8A04;
}
```

## Mobile Adaptation

| Viewport | Sidebar | Feed | Font |
|----------|---------|------|------|
| ≥768px | 180px, full labels | 800px max-width center | Default |
| <480px | 50px, icons only | Full width | Slightly smaller |

## State Management (JS)

```javascript
let projectsData = [];   // Loaded once from /api/projects
let kanbanCards = [];    // Reloaded every 30s from /api/kanban
let chatSessionId = 'main_' + Date.now();
let modalChatSessionId = 'modal_' + Date.now();

// API helper
const API = {
  get: async (url) => { const r=await fetch(url); return r.json(); },
  post: async (url, body) => {
    const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    return r.json();
  }
};

// Auto-refresh
setInterval(loadAll, 30000);
```

## Agent Color Map

```javascript
const AGENTS = [
  {id:'ceo',   icon:'👔', name:'CEO',         color:'#D4A843'},
  {id:'dev',   icon:'💻', name:'Developer',   color:'#22C55E'},
  {id:'sales', icon:'🎯', name:'Sales',       color:'#3B82F6'},
  {id:'marketing', icon:'📢', name:'Marketing', color:'#A855F7'},
  {id:'operations',icon:'⚙️', name:'Operations',color:'#F97316'},
  {id:'support',icon:'🎧', name:'Support',    color:'#06B6D4'},
  {id:'analytics',icon:'📊',name:'Analytics', color:'#EC4899'},
  {id:'media',  icon:'🎨', name:'Media',      color:'#D946EF'},
  {id:'research',icon:'🔬',name:'Research',  color:'#14B8A6'},
];
```

## Lessons Learned (Jul 2026)

1. **User prefers single screen over tabs** — "phải thế chứ. khác bọt hẳn" (direct praise)
2. **User prefers light theme** — dark was rejected after trying both
3. **User wants wide sidebar with full names** — not compact icon-only
4. **Dead process problem** — process cũ giữ port với code cũ. Kill all Python procs + clear __pycache__ before restart
5. **SQLite "database is locked"** — fix with WAL mode + timeout=10 on all kanban write endpoints
6. **Modal scroll** — must set max-height and body overflow-y; mobile users need to scroll after opening modal
7. **Inline chat session** — each modal needs its own session_id to maintain conversation context
8. **"CEO đang nghĩ..." double message** — user hated this. Replace with `sendChatAction(action="typing")` — chỉ 1 message duy nhất khi response ready
9. **Project sidebar** — dự án trong sidebar với status dot. Bấm → modal: facts + decisions + inline chat riêng. Auto-load từ `/api/memory/facts` + `/api/memory/decisions`
10. **F5-proof chat** — lưu vào SQLite `project_memory.db` thay vì RAM dict
