# Dashboard Situation Room — Office Simulation

## Concept
Mô phỏng văn phòng họp trên web dashboard $0 — dùng CSS animation + JavaScript fetch API. Không cần 3D, không cần library.

## Layout
```
┌──────────────────────┐
│   🏢 TANO AGENCY     │  ← Bàn họp glow vàng
│   Situation Room     │
├──────────────────────┤
│        👔 CEO        │  ← Avatar lớn, click → chat
│     CEO Trợ lý       │
├──────────────────────┤
│ ┌──────┐ ┌──────┐    │
│ │💻 Dev│ │🎯 Sal│    │  ← 2 cột grid
│ │⏳ idle│ │✅ rdy│    │
│ │2 tasks│ │0 task│    │
│ └──────┘ └──────┘    │
│ ┌──────┐ ┌──────┐    │
│ │...   │ │...   │    │
│ └──────┘ └──────┘    │
├──────────────────────┤
│ 📊 9 agents · 5 tasks│  ← Stats bar
└──────────────────────┘
```

## Agent card states (CSS classes)

| Trạng thái | CSS class | Animation | Khi nào |
|-----------|-----------|-----------|---------|
| ✅ ready | `.done` | bg xanh #0a2a1a + shadow | 0 task |
| ⏳ idle | — | mặc định | có task nhưng ko chạy |
| 🔄 running | `.running` | ring xoay 2s + avatar shake 1.5s + card pulse glow vàng | state='running' |
| 🔴 blocked | `.blocked` | bg đỏ #2a0a0a + shadow | state='blocked' |

### Key CSS animations
```css
@keyframes ring-rotate {
  0% { transform: rotate(0deg); border-color: var(--accent); }
  50% { border-color: var(--yellow); }
  100% { transform: rotate(360deg); border-color: var(--accent); }
}
@keyframes avatar-shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(8deg); }
  75% { transform: rotate(-8deg); }
}
@keyframes pulse-glow {
  0%, 100% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.2); }
}
```

## JS Logic
```javascript
const OFFICE_AGENTS = ['dev','sales','marketing','operations','support','analytics','media','research'];

function loadOffice() {
  Promise.all([fetch('/api/kanban').then(r=>r.json()), fetch('/api/agents').then(r=>r.json())])
    .then(([kanban, agents]) => {
      // Count tasks per agent from kanban cards
      // Determine state: blocked > running > idle > ready
      // Apply CSS class + text update
      // CEO ring animation if any agent running
      // Stats bar: agents · total · done · blocked · running
    });
}

// Auto refresh 15s
setInterval(() => {
  const page = document.getElementById('page-office');
  if (page && page.classList.contains('active')) loadOffice();
}, 15000);
```

## Tab count: 7
Chat → Health → Kanban → Tickets → Outbox → Agents → **Văn Phòng**

## Key files
- `web/templates/index.html` — HTML structure (lines ~500-590) + CSS (~lines 393-505) + JS (~lines 620-706)
- Web dashboard `dashboard.py` — không cần API riêng, tận dụng /api/kanban + /api/agents

## Pitfalls
- CSS selector `[data-agent="dev"]` — cần data-agent attribute trên card
- fetch error handling — nếu kanban API lỗi, office vẫn hiển thị "Error" thay vì treo trang
- Auto refresh setInterval chạy cả khi tab ko active — check `.active` class trước
