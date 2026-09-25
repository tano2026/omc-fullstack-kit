# FastAPI Dashboard — Công ty 1 người

## Cấu trúc
```
web/
  dashboard.py          # FastAPI app (6KB)
  templates/
    index.html          # Mobile-first SPA (23KB)
  static/               # (trống, CSS inline trong HTML)
```

## API endpoints

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| `/` | GET | — | HTML dashboard |
| `/api/health` | GET | — | {status, data: [{title, snippet}], ts} |
| `/api/kanban` | GET | — | {status, data: [list items], ts} |
| `/api/tickets` | GET | ?status=open/in_progress/closed | {status, data, ts} |
| `/api/outbox` | GET | — | {status, data, ts} |
| `/api/agents` | GET | — | {status, data: [{name, label, types}], ts} |
| `/api/chat` | POST | message=Form | {status, intake, plan, track, dispatch, ts} |
| `/api/ceo/command` | POST | message=Form | {status, intake, plan, ts} |
| `/api/run/{agent}/{ttype}` | GET | ?topic= | {status, result, progress, ts} |

## Văn Phòng tab (Situation Room) — CSS animation + realtime status

Bottom nav 7 items (thêm 🏢 Văn Phòng). HTML/CSS/JS inline trong index.html.

### Cấu trúc template
```
<!-- Bàn họp phát sáng -->
<div class="meeting-table">
  <div class="table-glow"></div>        <!-- radial-gradient pulse glow -->
  <div class="table-text">🏢 TANO AGENCY</div>
  <div class="table-text-sub">Situation Room</div>
</div>

<!-- CEO head — bấm vào chuyển sang tab Chat -->
<div class="ceo-spot">
  <div class="agent-btn" id="ceo-btn" onclick="switchPage('chat')">
    <div class="agent-ring" id="ceo-ring"></div>  <!-- ring quay khi có agent running -->
    👔
  </div>
  <div class="ceo-label">CEO Trợ lý</div>
</div>

<!-- 8 agent cards — 2 cột grid -->
<div class="agent-grid" id="office-agents">
  <div class="agent-card" data-agent="dev">      <!-- CSS class quyết định animation -->
    <div class="agent-avatar"><div class="agent-ring"></div><span class="agent-emoji">💻</span></div>
    <div class="agent-body">
      <div class="agent-title">Dev</div>
      <div class="agent-status" id="st-dev">✅ ready</div>
      <div class="agent-meta" id="meta-dev">0 tasks</div>
    </div>
  </div>
  ... (8 agents)
</div>

<!-- Stats bar -->
<div class="office-stats">
  <span>📊 <span id="office-gen-status">9 agents · 2 tasks · 0 done · 0 blocked · 0 running</span></span>
</div>
```

### Agent trạng thái → CSS class mapping

| Trạng thái | CSS class | Animation | Màu |
|-----------|-----------|-----------|-----|
| ✅ ready (0 tasks) | `.done` | — | Xanh lá (green glow) |
| ⏳ idle (có task nhưng ko chạy) | _none_ | — | Mặc định |
| 🔄 running | `.running` | ring rotate + avatar shake + card pulse | Vàng (accent glow) |
| 🔴 blocked | `.blocked` | — | Đỏ (red glow) |

### CSS animations
```css
@keyframes pulse-glow {         /* Bàn họp */
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.2); }
}
@keyframes ring-rotate {        /* Ring CEO/agent khi running */
  0% { transform: rotate(0deg); border-color: var(--accent); }
  50% { border-color: var(--yellow); }
  100% { transform: rotate(360deg); border-color: var(--accent); }
}
@keyframes avatar-shake {       /* Agent avatar khi đang chạy */
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(8deg); }
  75% { transform: rotate(-8deg); }
}
@keyframes card-pulse {         /* Card border glow khi running */
  0%, 100% { box-shadow: 0 0 5px rgba(255,215,0,0.2); }
  50% { box-shadow: 0 0 15px rgba(255,215,0,0.4); }
}
```

### JS: loadOffice() — fetch Kanban + Agents API
```javascript
const OFFICE_AGENTS = ['dev','sales','marketing','operations','support','analytics','media','research'];

function loadOffice() {
  Promise.all([
    fetch('/api/kanban').then(r=>r.json()),
    fetch('/api/agents').then(r=>r.json())
  ]).then(([kanban, agents]) => {
    const cards = kanban.data || [];
    // Count tasks per agent: total, running, blocked
    cards.forEach(c => {
      const owner = (c.owner || '').toLowerCase();
      if (OFFICE_AGENTS.includes(owner)) {
        agentTasks[owner]++;
        if (c.state === 'running') agentRunning[owner] = true;
        if (c.state === 'blocked') agentBlocked[owner] = true;
      }
    });
    // Update each agent-card: remove all states, add matching class
    OFFICE_AGENTS.forEach(name => {
      const card = document.querySelector(`.agent-card[data-agent="${name}"]`);
      card.classList.remove('running', 'done', 'blocked');
      if (agentBlocked[name]) statusClass = 'blocked';
      else if (agentRunning[name]) statusClass = 'running';
      else if (agentTasks[name] == 0) statusClass = 'done';
      if (statusClass) card.classList.add(statusClass);
    });
    // CEO ring animation khi có bất kỳ agent nào running
    const ceoRing = document.getElementById('ceo-ring');
    if (runningCount > 0) ceoRing.classList.add('running');
    else ceoRing.classList.remove('running');
  });
}

// Auto refresh 15s
setInterval(() => {
  const page = document.getElementById('page-office');
  if (page && page.classList.contains('active')) loadOffice();
}, 15000);
```

### Pitfalls
- Mỗi agent-card phải có `data-agent="${name}"` để JS querySelector
- `id` cho status/meta: `st-${name}`, `meta-${name}`
- CEO cần `id="ceo-ring"` riêng để toggle class (không dùng data-agent)
- Auto-refresh 15s — không gọi khi tab không active (kiểm tra class)

## Template pattern (mobile-first)
- Bottom nav: fixed 6 items, icon + label, active state
- Header: centered title + subtitle
- Cards: single column, dark theme (--bg: #0F0F1A, --card: #1A1A2E, --accent: #FFD700)
- Chat: user right (accent), assistant left (card), loading dots
- Health: 2-column grid with emoji status
- Auto-refresh: 30s interval on health/kanban/outbox tabs
- Safe area: `env(safe-area-inset-bottom)` cho notch phones

## Jinja2 cache fix (Python 3.14)
```python
from jinja2 import FileSystemLoader
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader("templates")  # REQUIRED fix
```

## Chạy
```bash
cd web
uvicorn dashboard:app --host 0.0.0.0 --port 8137
```
