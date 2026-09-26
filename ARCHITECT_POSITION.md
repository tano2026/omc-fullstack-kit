# Council — Architect Position: agent-manager-skill → omc-fullstack-kit

**Position (Architect — 2 câu):**
Tích hợp `agent-manager-skill` vào `omc-fullstack-kit` không phải như một module frontend/backend, mà như một **OpenClaw Execution Adapter / agent-scheduling plug-in** cho lớp thực thi 24/7. Skill này chạy 9 agent chuyên biệt (main / dsh-commander / hermes-architect / dev-automation / media-producer / openclaw-executor / jev-sentinel / research-intel / airport-ops) qua tmux session + cron — đúng với vai trò `openclaw-executor` trong pipeline 6 giai đoạn và Quad-Engine (DSH → Hermes → OpenClaw → JEV).

**Reasoning (3 bullet — không hedging):**
- Scope của skill là quản lý CLI tmux (start/stop/monitor/assign/cron) — đúng 1:1 với `openclaw-executor` (thực thi 24/7, build/test/git/deploy) trong AGENTS.md, chứ không thuộc tầng web stack.
- `omc-fullstack-kit` đã định nghĩa 9 specialized agents (AGENTS.md §1); `agent-manager-skill` cung cấp cơ chế chạy song song + ghi log + gán task — hoàn thiện phần thiếu của pipeline [Plan → Build → Verify → Exec].
- Điểm tích hợp chính xác là **giai đoạn 3 (OpenClaw Execution)** và cổng JEV Safety Gate trước khi chạy lệnh nhạy cảm — không chạm vào database / frontend / API schema, giảm rủi ro phụ thuộc.

**Risk (lớn nhất):**
Dependency môi trường bất ổn định (tmux + python3; cấu hình agent nằm trong `agents/` riêng; repo `agent-manager-skill` phải `git clone` bên ngoài). Nếu `tmux` không có (Windows bare) hoặc thư mục cấu hình sai, `start/assign` thất bại im lặng và cả 9 agent ngừng lập lịch — không có gate tự động phát hiện (skill KHÔNG có health-check endpoint).

**Surprise (điều người khác có thể bỏ sót):**
Skill bắt buộc `git clone https://github.com/fractalmind-ai/agent-manager-skill.git` — đây là **supply-chain dependency ngoài**, không có trong `omc-fullstack-kit`. Một lỗi pull / xóa repo / thay đổi branch sẽ phá vỡ toàn bộ scheduling cho tất cả các agent lại, nhưng README không đề cập pin version, checksum, hay fallback offline. Đặc biệt: skill không tích hợp JEV Safety Gate tự nhiên — phải tự bọc `agent-manager/scripts/main.py` bên trong JEV pre-execution check (AGENTS.md §1, `jev-sentinel`) trước khi chạy `start/assign`.

---
*Architect voice — vị trí được hình thành TRƯỚC khi biểu quyết 4-voice (Skeptic / Pragmatist / Critic chưa phát). Format: <300 words, direct, no hedging. Ngôn ngữ phản hồi: tiếng Việt thân thiện cho Chủ tịch; nội dung kỹ thuật theo spec gốc (Position / Reasoning / Risk / Surprise, English).*
*Workspace: D:\TanoAgencyStorage\platform\omc-fullstack-kit | Skill sources: agent-manager-skill (C:\Users\...\.agents\skills), AGENTS.md, dsh-hermes-openclaw-trio (§JEV Gate 2 — pre-execution safety brake).*
