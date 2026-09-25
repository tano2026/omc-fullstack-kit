# Project Sidebar & Modal with Memory (19/07/2026)

## Pattern: Project list in sidebar + modal with facts/decisions/chat

### Sidebar addition (JS in dashboard.html)

```javascript
function buildSidebar(){
  // ... agents section ...
  html += `<div class="sidebar-divider"></div><div class="sidebar-title">Dự án</div>`;
  html += `<div id="sidebar-projects"></div>`;
  sb.innerHTML = html;
}

function updateProjectsSidebar(){
  const el = document.getElementById('sidebar-projects');
  let html = '';
  projectsData.forEach(p => {
    const statusClass = p.status === 'active' ? 'green' : 'red';
    html += `<button class="sidebar-btn" onclick="openProjectModal('${p.name}')">
      ${p.icon}<span class="sb-label">${p.name}</span>
      <span class="status-dot ${statusClass}" style="margin-left:auto;flex-shrink:0"></span>
    </button>`;
  });
  el.innerHTML = html;
}
```

Called from `loadAll()` after projects load: `updateProjectsSidebar()`

### Project Modal (`openProjectModal`)

Shows 5 sections:
1. **Project info** — icon + name + status (✅/❌) + filesystem path
2. **🧠 Kiến thức đã lưu** — facts from `/api/memory/facts?project=X`
3. **📋 Quyết định đã ghi** — decisions from `/api/memory/decisions?project=X`
4. **Buttons**: 💬 Hỏi CEO về dự án / 🧠 Thêm kiến thức (prompt-based)
5. **💬 Chat riêng dự án** — inline chat box using `session_type: projectName`

```javascript
function openProjectModal(projectName){
  closeModal();
  // ... render modal HTML with #pm-facts and #pm-decisions ...
  modalChatSessionId = 'proj_' + projectName;

  // Load facts + decisions
  Promise.all([
    API.get('/api/memory/facts?project=' + encodeURIComponent(projectName)),
    API.get('/api/memory/decisions?project=' + encodeURIComponent(projectName)),
  ]).then(([factsData, decData]) => {
    // render facts list + decisions list
    // if empty: show "Chưa có kiến thức nào"
  });
}
```

### Project Chat (`sendProjectChat`)

Key difference from global chat: sends `session_type` parameter so CEO knows which project context to load.

```javascript
function sendProjectChat(projectName){
  const text = input.value.trim();
  API.post('/api/chat', {
    message: text, 
    session_type: projectName,  // ← THIS is critical
    session_id: 'proj_' + projectName
  }).then(data => {
    // render CEO response in modal chat bubble
  });
}
```

### Manual Fact Entry (`projectAddFact`)

User types in a fact via `prompt()`, posts to `/api/memory/facts`, then re-opens modal.

```javascript
function projectAddFact(projectName){
  const fact = prompt('Nhập kiến thức mới về dự án ' + projectName + ':');
  if(!fact) return;
  API.post('/api/memory/facts', {
    project: projectName,
    fact: fact,
    category: 'note',
    source: 'manual'
  }).then(data => {
    if(data.ok) openProjectModal(projectName); // refresh modal
  });
}
```

### API: `/api/memory/projects` — list projects with memory

**Note:** This endpoint had a 500 error. The query joins across 3 tables `(facts, decisions, project_chat)` using `DISTINCT project`. Fix: ensure the `project` column exists and has correct values in all 3 tables, and that `MEMORY_DB` path resolves correctly in the import context.

### Integration points

| File | Change |
|------|--------|
| `dashboard/app.py` | Import `project_memory` module, add `/api/memory/facts`, `/api/memory/decisions`, `/api/memory/projects`, `/api/preferences`, `/api/skills` endpoints |
| `dashboard/project_memory.py` | All memory logic (new file) |
| `dashboard/templates/dashboard.html` | `buildSidebar()` + `updateProjectsSidebar()` + `openProjectModal()` + `sendProjectChat()` + `projectAddFact()` + `projectChat()` |
