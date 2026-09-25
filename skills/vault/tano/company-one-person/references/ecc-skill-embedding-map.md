# ECC Skill Embedding Map — What Was Loaded, What Was Applied, What Was Skipped

## Embedded into agent code/prompts (8 skills)

| ECC Skill | Agent | Method | Detail |
|-----------|-------|--------|--------|
| **ecc-brand-voice** | Marketing | Prompt | Màu đen/vàng/đỏ, tone gai góc, AIDA + domain accent |
| **ecc-content-engine** | Marketing | Code | 1 source → multi-platform + quality gate |
| **ecc-knowledge-ops** | Support, Analytics | Code | 6-layer KB: Memory→File→MCP→External→Archive |
| **ecc-verification-loop** | Dev | Code | 6 phase: build→type→lint→test→security→diff |
| **ecc-team-orchestration** | CEO | Code | SQLite Kanban: backlog→ready→running→review→blocked→merged→archived |
| **ecc-python-testing** | Dev | Prompt | TDD: test trước code, mock deps, edge cases |
| **ecc-fal-ai-media** | Media | Prompt | Image prompt tiếng Anh chuẩn FAL format |
| **ecc-git-workflow** | Dev | Prompt | Conventional commits, branch naming feat/fix |

## Reviewed but NOT embedded (with reason)

| Skill | Reason Skipped |
|-------|---------------|
| **ecc-security-review** | **Now embedded** (2026-07-18) — checklist: secrets exposure, input validation, path traversal, SQL injection, resource exhaustion. Applied as validation rules in Dev agent guards and Analytics query safety check. |
| **ecc-security-scan** | Claude Code config scanner — không áp dụng cho TANO-AGENCY Python agents |
| **ecc-autonomous-loops** | TANO-AGENCY đã có brain.run pipeline + budget cap — loop pattern đã built-in |
| **ecc-token-budget-advisor** | Token advisor cho Hermes, không phải agent Python |
| **ecc-continuous-agent-loop** | Liên quan Claude Code continuous execution — ko liên quan TANO-AGENCY |
| **ecc-deep-research** | Cần Exa + Firecrawl (paid) — skip. Dùng ddgs thay thế |
| **ecc-lead-intelligence** | Cần X API (paid) — skip. Dùng DuckDuckGo thay thế |
| **ecc-social-publisher** | Cần SocialClaw (paid) — skip |
| **ecc-email-ops** | Apple Mail (macOS-only) — skip |
| **ecc-dashboard-builder** | Grafana — TANO-AGENCY dùng FastAPI + Jinja2 HTML |
| **ecc-mcp-server-patterns** | Chưa deploy MCP server — để sau |

## Embedding method

- **Prompt**: pattern text → `llm.make_analyzer(system_prompt=...)` string
- **Code**: workflow steps → Python function + validation rules
- **Hybrid**: prompt tells agent about tool, code implements tool

### Pitfalls encountered

| Pitfall | Fix in code |
|---------|-------------|
| Skill là markdown, không phải code | Viết function map thủ công |
| Skill trả phí nhưng tưởng free | Check `required_credentials` trước |
| Nhiều skill overlap | brand-voice x content-engine: brand-voice làm voice layer, content-engine làm pipeline |
| Agent không nhận adapter mới | Thêm tên vào `SEARCH_LIKE` set trong brain.py |
