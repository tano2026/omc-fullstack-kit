# OPC Repo Research — 4 One-Person Company Projects (19/07/2026)

## 1. iamtouchskyer/opc (~1k⭐)
**Architecture:** Digraph pipeline for Claude Code. 16 agents (PM, designer, security, devil's advocate...). File-based state in `~/.opc/sessions/`.

**Key innovations:**
- **D2 compound eval gate** — 11 mechanical layers to detect hallucinated/boilerplate evaluations
- **Zero-trust review** — agent that does work never evaluates it
- **Review independence** — byte-identical = hard error, >70% overlap = warning
- **Mechanical gates** — verdict from data (🔴 count≥3=Fail), never LLM judgment
- **Extension system** — capability-routed hooks with circuit breakers

**Weaknesses:** Single orchestrator (Claude Code), no dashboard, expensive for simple tasks (30-50 LLM calls per full run)

## 2. paperclipai/paperclip (~3k⭐)
**Architecture:** Node.js + React + PostgreSQL monorepo. 14 agent adapters (incl. Hermes adapter built-in). DB-first orchestration with heartbeat scheduling.

**Key innovations:**
- **Atomic checkout** — task claim + budget enforcement = atomic transaction
- **DB-backed wakeup queue** — no Kafka/RabbitMQ needed
- **Governance gates** — approval workflow, budget hard-stop, audit log
- **Hermes adapter** — `hermes_local` and `hermes_gateway` built-in adapters
- **Adapter plugin system** — ESM dynamic import, hot-reload

**Weaknesses:** 192 services, 260 UI components, 14 adapters = steep learning curve. Single-process scheduler. Needs Node 22+.

## 3. 1mancompany/OneManCompany (~2k⭐)
**Architecture:** Python + FastAPI + WebSocket + Canvas 2D pixel-art office. LangChain agents. YAML/MD/JSON persistence (zero database).

**Key innovations:**
- **Pixel-art office visualization** — real-time agent activity
- **Talent Market** — ecosystem for AI employees
- **Vessel+Talent modular pattern** — separate execution container from capability
- **EventBus + async pub/sub** — simple in-process event system

**Weaknesses:** Vanilla JS monolithic (154K CSS), single-user, not production-grade.

## 4. lulin70/OPC-Agents (~500⭐)
**Architecture:** Python + Streamlit. 99 modules, 4164 tests, three sages parallel voting (strategist/executor/reflector).

**Key innovations:**
- **Three Sages Parallel Voting** — 1×RTT instead of 3×RTT, upfront consensus
- **CI quality gates** — mypy, ruff, Black, Bandit, radon, coverage
- **Skill marketplace** — 21 built-in skills + external MCP discovery
- **Memory bridge** — persistent cross-session memory + flywheel

**Weaknesses:** Streamlit (not mobile-first), code heavy (99 modules), focuses on task execution not dashboard.

## What to Apply to Hermes

| Pattern | From | Priority | Effort |
|---------|------|----------|--------|
| D2 compound eval gate | OPC | HIGH | Low — done (quality_gate.py) |
| Atomic checkout + loop locks | Paperclip | HIGH | Low — done (loop_mode.py) |
| Verdict from data (no LLM) | OPC | HIGH | Low — enforce in hq.py approve() |
| Review independence check | OPC | MEDIUM | Low — quality_gate.py has it |
| Hermes adapter as Paperclip plugin | Paperclip | LOW | Paperclip already has it |
| Canvas office visualization | OMC | LOW | Nice-to-have for dashboard |
| Three sages voting | OPC-Agents | MEDIUM | Medium — pattern for hq.py dispatch |
