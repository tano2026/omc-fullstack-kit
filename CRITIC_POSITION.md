# Council — Critic Position: agent-manager-skill → omc-fullstack-kit

**Position (Critic — 2 câu):**
Tích hợp `agent-manager-skill` làm primary orchestration là **SPOF cho cả 9 agent + silent failure + vi phạm AGENTS.md §1** — JEV phải tự bọc chứ không tích hợp sẵn. Nếu dùng duy nhất như fallback khẩn cấp (emergency override khi Quad-Engine deadlock), mới chấp nhận được.

**Reasoning (3 bullet — không hedging):**
- **OS + dependency rủi ro**: Skill cần `tmux` (không có trên Windows native) và `git clone` repo ngoài — nếu fetch thất bại hoặc `tmux` không khởi động, **9 agent ngừng lập lịch đồng loạt** mà `jev-sentinel` không phát hiện vì skill không có health-check endpoint (đã ghi trong ARCHITECT_POSITION.md).
- **Audit trail mất**: `agent-manager-skill` dùng `cron` + `tmux` ghi log riêng, không đồng bộ với `VaultSync` (Obsidian Second Brain) hay `skills/manager.py`. Quality Gate (§5) yêu cầu `Obsidian sync + Sprint_Backlog [x]`; nếu agent chạy qua tmux mà không ghi vào vault → **audit log biến mất**, vi phạm Rule ① (Verify, Don't Assume).
- **JEV Safety Gate bị bypass**: AGENTS.md §1 nói `jev-sentinel` phải bảo vệ trước mọi lệnh nhạy cảm. Skill không tích hợp JEV tự nhiên — phải tự bọc `main.py` bên trong `safety_guard.py`. Nếu dev quên bọc, lệnh `rm -rf` hoặc `drop table` có thể chạy qua cron mà không qua Gate 2 (15ms pre-execution brake).

**Risk (lớn nhất):**
Silent failure + double-authority scheduling. `DSH Planning` (dsh-planner) và `agent-manager-skill` (cron) cùng điều khiển cùng 9 agent → **race condition / double-trigger** khi cả 2 hệ thống cùng gán công việc cho `dev-automation` hoặc `openclaw-executor`. Không có mechanism đồng bộ trạng thái giữa `trio_orchestrator.py` và tmux session → process divergence, resource conflict (port, file lock), và debugging black hole.

**Surprise (điều người khác có thể bỏ sót):**
Không chỉ repo git chết — **log/cron/assignment record cũng biến mất**. Skill không cung cấp cấu trúc `session_id`, `tenant_id`, `pendingAction` như `ChatSession` trong `agent-tkt-llm-chat-backend-aug2026.md`. Nếu dùng tmux cho `airport-ops` xử lý khách hàng sân bay, không có log cấu trúc để audit lại chuỗi hành động → **Quality Gate 5/5 không thể đạt** (cần Playwright screenshot + Obsidian sync + brand check).

---
*Critic voice — vị trí adversarial / failure-mode, được viết SAU khi Architect đã ghi trước. Format: <300 words, direct, no hedging. Tiếng Việt thân thiện cho Chủ tịch; nội dung kỹ thuật theo spec gốc (Position / Reasoning / Risk / Surprise, English).*
*Workspace: D:\TanoAgencyStorage\platform\omc-fullstack-kit | Skill sources: agent-manager-skill (C:\Users\...\.agents\skills), AGENTS.md §1 (JEV Gate), dsh-hermes-openclaw-trio (§JEV Safety Gate 2), skills/manager.py (agent assignment).*
