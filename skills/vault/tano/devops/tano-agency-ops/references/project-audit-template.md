# Project Audit Template

Use during Step 4 of the Project Audit Workflow (see SKILL.md).

## Audit Header
- Date:
- Auditor:
- Source: (disk path, e.g. `D:\MMO Du an\`)

## Per-Project Checklist

```
[ ] PROJECT: <name>
[ ]   Folder exists: <path>
[ ]   Has README / docs: Y/N
[ ]   Has code (agent.py / main.py / pipeline): Y/N
[ ]   Has .env: Y/N (if yes, check TELEGRAM_BOT_TOKEN valid)
[ ]   Has Telegram bot running: Y/N
[ ]   Class: CLIENT / TOOL / LEGACY / CLARIFY
[ ]   Revenue model clear: Y/N
[ ]   Needs AI agent: Y/N (which: _____)
[ ]   Existing Hermes skills match: ___________
[ ]   Notes: ___________
```

## Gap Analysis Table

| Project | Disk Status | Doc Status | Gap | Action Needed |
|---------|-----------|-----------|-----|--------------|
| ... | OK/Missing | OK/Mapped/Stale | Planned but not executed | Create symlink / update doc |

## Multi-Source Synthesis Method (added 07/2026)

For a comprehensive portfolio audit, gather data from ALL of these sources — not just disk:

| Source | Command/Method | What It Reveals |
|--------|---------------|-----------------|
| **Disk** | `ls -la "D:/MMO Du an/"` + per-project dirs | Directory existence, code files, docs |
| **VPS** | `ssh ubuntu@43.156.72.127 "ls /opt/"` | What's deployed and running remotely |
| **Cron** | `cronjob(action='list')` | Active scheduled jobs per project |
| **Skills** | `skills_list()` | How many skills exist, which are project-specific |
| **Session DB** | `session_search(query="dự án ...")` | Recent discussions, decisions, context |
| **Memory** | (already in system prompt) | User preferences, environment facts, key decisions |

**Why multi-source matters:** Disk-only audits miss VPS deployments (ABTrip, GMSP dashboard). Cron-only misses offline projects. Skills-only misses real business status. Combine all 6 for the true picture.

## Output Format (recommended)

For the CEO (Tân), use this structure:

```
## 📊 TỔNG QUAN N DỰ ÁN

### 🏗️ 1. <Tên> — <vai trò ngắn>
**Trạng thái:** <1 dòng>
| Thành phần | Chi tiết |
|---|---|
| ... | ... |

### 📈 TỔNG KẾT
| Dự án | Trạng thái | Doanh thu |
|---|---|---|
| ... | ... | ... |
```

Keep it concise — Tân dislikes verbose explanations. One table per project, one summary table at the end. Ask "muốn đi sâu vào cái nào?" to let him steer.

When user approves import:
```
[ ] Update PROJECT-MAP.md
[ ] Create symlink in TANO-AGENCY/CLIENTS/<name>/
[ ] Add skill references to project folder
[ ] Create Telegram topic/thread
[ ] Start project TODO
[ ] Attach Hermes skills to project context
```
