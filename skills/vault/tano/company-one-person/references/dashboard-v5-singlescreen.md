# Dashboard v5 — Single-Screen SAAS Layout

Created: 19/07/2026
File: `D:\MMO Du an\TANO-AGENCY\PLATFORM\agent-core\dashboard\templates\dashboard.html`

## Layout Structure

```
┌──────────────────────────────────────────┐
│ TANO.AGENCY    📁5/5   📋3/10   🟢OK    │ ← Sticky header
├──────┬───────────────────────────────────┤
│      │  📋 Công việc                      │
│ Phòng│  ┌──────────────────────────────┐  │
│ ban   │  │ 💻 Landing Page GMSP       │  │ ← Task card: click → modal
│ 👔 CEO│  │    Developer · 2h      🟢  │  │
│ 💻 De│  ├──────────────────────────────┤  │
│ 🎯 Sa│  │ 🎯 KPI tháng 7             │  │
│ 📢 Ma│  │    Sales · 1ng        🟡  │  │
│ ⚙️ Op│  └──────────────────────────────┘  │
│ 🎧 Su│                                    │
│ 📊 An│  [Feed: sorted by priority]        │
│ 🎨 Me│                                    │
│ 🔬 Re│                                    │
│      │  ┌──────────────────────────────┐  │
│ 🏠 Tấ│  │ 💬 Input  ──────────── [➤]  │  │ ← Fixed chat bar
│      │  └──────────────────────────────┘  │
│      │         [📋] [📊] [🏛️]           │ ← Quick tools (absolute right)
└──────┴────────────────────────────────────┘
```

## CSS Framework

```css
/* Light theme tokens */
:root {
  --bg: #F5F5F7;       --card: #FFFFFF;
  --card-hover: #EBEBF0;  --border: #D4D4D8;
  --text: #1A1A2E;     --text-muted: #6B6B80;
  --gold: #B8860B;     --green: #16A34A;
  --red: #DC2626;      --yellow: #CA8A04;
  --radius: 12px;      --radius-sm: 8px;
}

/* Main layout: header + (sidebar + content) */
.header { position: sticky; top: 0; z-index: 100; }
.main { display: flex; height: calc(100vh - 52px); }
.sidebar { width: 180px; flex-shrink: 0; }
.content { flex: 1; display: flex; flex-direction: column; }
.feed { flex: 1; overflow-y: auto; }
.chat-bar { flex-shrink: 0; }

/* Task card */
.task-card {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 14px; margin-bottom: 8px;
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); cursor: pointer;
}
.task-card:hover { border-color: var(--gold); }
.tc-icon { width: 36px; height: 36px; border-radius: 50%; }
.tc-status { padding: 3px 8px; border-radius: 10px; font-size: 10px; font-weight: 700; }

/* Modal */
.modal {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 201;
  background: var(--card); border-radius: 16px 16px 0 0;
  max-height: 85vh; display: flex; flex-direction: column;
  animation: slideUp .25s ease;
}

/* Responsive */
@media(max-width: 480px) {
  .sidebar { width: 50px; }
  .sidebar-btn .sb-label { display: none; }
  .sidebar-title { display: none; }
}
```

## Key JavaScript Functions

| Function | Purpose |
|----------|---------|
| `loadAll()` | Fetch /api/projects + /api/kanban -> renderTasks() |
| `renderTasks(filter)` | Render cards sorted by priority. Filter by agent ID. |
| `filterAgent(id)` | Sidebar button -> filter tasks by owner |
| `openTaskModal(cardId)` | Build modal HTML with details + inline chat |
| `updateTaskState(cardId)` | POST /api/kanban/move, reload, close modal |
| `sendModalChat()` | Inline chat inside modal, separate session_id |
| `sendChat()` | Main chat bar -> POST /api/chat |
| `assignToCEO(title)` | POST /api/chat with "/ceo Giao nhiệm vụ:", show toast |
| `directChat(owner)` | Switch to chat bar, pre-fill "/owner " |
| `showNewTaskModal()` | Modal with title + department + priority |
| `createTask()` | POST /api/kanban/add |
| `showReportModal()` | Fetch /api/health + /api/kanban_summary -> display modal |

## Agent Colors
```
ceo:       #D4A843 (gold)
dev:       #22C55E (green)
sales:     #3B82F6 (blue)
marketing: #A855F7 (purple)
operations: #F97316 (orange)
support:   #06B6D4 (cyan)
analytics: #EC4899 (pink)
media:     #D946EF (magenta)
research:  #14B8A6 (teal)
```

## Priority Order (task sorting)
1. running (🟢 Đang chạy)
2. ready (🔵 Sẵn sàng)
3. review (🟡 Review)
4. blocked (🔴 Bị chặn)
5. backlog (⚪ Tồn)
6. done (🟣 Hoàn thành) — usually filtered out

## State Change Options
```javascript
const stateLabels = {
  'ready': '🔵 Sẵn sàng',    'running': '🟢 Đang chạy',
  'review': '🟡 Review',     'blocked': '🔴 Bị chặn',
  'done': '🟣 Hoàn thành',    'backlog': '⚪ Tồn'
};
```

## Toast Pattern
```javascript
function showToast(msg, title){
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = `<strong>${title}</strong><div class="toast-sub">${msg}</div>`;
  document.body.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transition = 'opacity 0.3s';
    setTimeout(() => t.remove(), 300);
  }, 3500);
}
```

## History
- **v1** (18/07): 5-tab SPA (Overview/Branches/Office/Tasks/Chat)
- **v2** (18/07): 2-tab redesign (Dashboard/Chat)
- **v3** (19/07): 4-tab "Văn Phòng Đại Lý" (VP/Bảng Tin/Phòng Họp/Chat)
- **v4** (19/07, mid-day): 4 tabs + inline chat in modals + toast notifications
- **v5** (19/07, evening): **Complete rewrite — single screen.** No tabs. Left sidebar + task feed + fixed chat bar + quick tools. Light theme. Per-project memory integrated.
