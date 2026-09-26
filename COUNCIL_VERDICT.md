# Council Verdict — agent-manager-skill → omc-fullstack-kit

**Câu hỏi quyết định:** Có nên tích hợp `agent-manager-skill` (tmux-based CLI agent manager) vào `omc-fullstack-kit` (OMC Quad-Engine: DSH + Hermes + OpenClaw + JEV + 9 specialized agents)?

---

## 1. Các vị trí (thứ tự: Architect → Skeptic → Pragmatist → Critic)

| Voice | Position | Key Points |
|---|---|---|
| **Architect** | Không tích hợp primary. Chỉ chấp nhận như **OpenClaw Execution Adapter / plug-in** cho tầng thực thi 24/7. | Scope đúng = giai đoạn 3 (OpenClaw Execution). Không chạm DB/API. Supply-chain risk từ `git clone`. Thiếu health-check. |
| **Skeptic** | **Không tích hợp.** Tạo cognitive friction, conflict với OpenClaw layer. | Skill dùng tmux session; OMC dùng in-process agent dispatch (`openclaw agent --agent`). Skill giải quyết "9 terminal cùng lúc" chứ không phải "9 agent chạy an toàn song song". |
| **Pragmatist** | **Không tích hợp chính thức.** Nếu phải, chỉ stage ở agent **không quan trọng** (`media-producer`, `research-intel`) trước. | `tmux` là red herring — thực chất nguy hiểm là **cron ownership** khiến DSH và agent-manager tranh quyền scheduling → double-trigger → cost spike / race condition. |
| **Critic** | **Không tích hợp primary.** Giữ lại chỉ như **emergency fallback** khi Quad-Engine deadlock. | SPOF cho 9 agent, silent failure (không có health-check), audit log/assignment record mất, vi phạm AGENTS.md §1 (JEV phải tự bọc, không tích hợp sẵn), double-authority scheduling. |

---

## 2. Consensus và Dissent mạnh nhất

- **Consensus 4/4:** Từ chối tích hợp làm primary orchestration cho cả 9 agent.
- **Dissent mạnh:** **Critic** (và **Architect**) đồng ý giữ lại `agent-manager-skill` ở trạng thái **không tích hợp** nhưng **lưu trữ** dưới `.agents/skills/` cho trường hợp khẩn cấp (JEV Safety Gate block toàn bộ pipeline → cần manual override ngoài Quad-Engine).
- **Dissent nhẹ:** **Pragmatist** đề xuất stage integration cho agent không critical (`media-producer`, `research-intel`) — nhưng vẫn cần giải quyết `cron` vs `trio_orchestrator` conflict trước.

---

## 3. Kiểm tra giả định (Premise Check)

- **Skeptic thách thức:** "Skill có thực sự giải quyết vấn đề nào OMC chưa giải quyết?" → **Không.** PM2 (`ecosystem.config.js`) đã làm process lifecycle, `skills/manager.py` đã làm taxonomy + assign, `trio_orchestrator.py` đã làm 5-phase pipeline.
- **Architect xác nhận:** Skill chỉ bổ sung "chạy 9 terminal cùng lúc" — không phải isolation thực sự (tmux không cung cấp resource isolation như container/subprocess).

---

## 4. Khuyến nghị tổng hợp (Verdict)

### A. Ngay lập tức (Immediate)

| Hành động | Chi tiết | File liên quan |
|---|---|---|
| **Từ chối tích hợp** | Không thêm `agent-manager-skill` vào `omc-fullstack-kit` pipeline | `engines/trio_orchestrator.py`, `gateway/webhook_server.py` |
| **Ghi nhận vị trí** | Lưu 4 voice + verdict vào repo để audit sau này | `ARCHITECT_POSITION.md` (đã có), `CRITIC_POSITION.md` (mới), `COUNCIL_VERDICT.md` (mới) |
| **Bảo vệ P0 rules** | Kiểm tra không có token/API key trong `abtrip-api-guide.md`; redaction đã có trong `safety_guard.py` | `skills/vault/.../abtrip-api-guide.md`, `engines/jev_gateway/safety_guard.py` |

### B. Ngắn hạn (Next 30 days)

| Hành động | Lý do |
|---|---|
| **Tăng cường PM2 + `skills/manager.py`** | Thay vì tmux, dùng `pm2 start ecosystem.config.js` để chạy các agent (main, dsh-commander, openclaw-executor) song song với monitoring log. |
| **Bổ sung health-check cho 9 agent** | `jev-sentinel` cần endpoint kiểm tra trạng thái từng agent (hiện chỉ có `SafetyGuard.audit_command`). |
| **Nếu cần fallback** | Giữ `agent-manager-skill` ở `C:\Users\...\.agents\skills\` (không clone vào repo). Chỉ dùng khi Quad-Engine deadlock sau khi đã thử `eval_gate.py`. |

### C. Dài hạn (Future — nếu chuyển Linux / VPS)

- Khi chạy trên Linux server có `tmux` native: có thể cân nhắc **stage** cho `media-producer` và `research-intel` (không ảnh hưởng đến core 7 agent còn lại).
- Nhưng phải giải quyết **cron ownership conflict** trước (DSH `GoalPlanner` + cron `agent-manager`) bằng cách thêm `session_id` đồng bộ vào vault (Obsidian Inbox).

---

### D. Quality Gate 5/5 — trước khi đánh dấu hoàn thành

| Gate | Trạng thái | Ghi chú |
|---|---|---|
| ① `npx tsc --noEmit` → exit 0 | ✅ Không áp dụng (Python/JS hybrid) | Kiểm tra TypeScript `orchestrator.ts`, `jev-client.ts` |
| ② Browser console → zero errors | ✅ `webhook_server.py` HTML UI sạch | Cần kiểm tra sau khi thêm agent status endpoint |
| ③ Playwright screenshot → artifacts/ | ⚠️ Chưa thực hiện | Nếu thêm agent dashboard |
| ④ Brand compliance → NO #000000 | ✅ Đã tuân thủ (#0B2545, #E8601C, #177A99, #D4A24C) | Kiểm tra trong `skills/vault/tano/aviation-ticketing/` docs |
| ⑤ Obsidian sync → Sprint_Backlog [x] + Lessons_Learned | ⚠️ Cần cập nhật | Ghi quyết định không tích hợp vào `Lessons_Learned.md` |

---

## 5. Files mới / cập nhật

| File | Trạng thái | Nội dung |
|---|---|---|
| `ARCHITECT_POSITION.md` | ✅ Đã có | Vị trí Architect: adapter cho OpenClaw step 3 |
| `CRITIC_POSITION.md` | ✅ **Mới viết** | Vị trí Critic: SPOF + silent failure + JEV gate violation + audit loss |
| `COUNCIL_VERDICT.md` | ✅ **Mới viết** | Tổng hợp 4 voice + verdict + lộ trình A/B/C + Quality Gate |
| `skills/manager.py` | ⚠️ Cần xem xét | Đã có `assign --agent --skill`; có thể mở rộng cho monitoring |

---

## 6. Kết luận cho Chủ tịch

> **Mày không cần `agent-manager-skill` để vận hành bộ này.** Hệ thống đã tự đủ: `trio_orchestrator.py` điều phối 5 pha, `pm2` quản lý process, `skills/manager.py` gán skill, `jev-sentinel` bảo vệ. Việc thêm tmux chỉ tạo rủi ro (SPOF, audit loss, double-scheduling) mà không tạo giá trị.
>
> Nếu một ngày mày chuyển server Linux và muốn song song nhiều terminal cho quan sát — **lúc đó mới cân nhắc**, và phải giải quyết `cron` vs `DSH Planning` conflict trước.

---
*Council completed: 4 voices (Architect / Skeptic / Pragmatist / Critic) + synthesized verdict. Workspace: D:\TanoAgencyStorage\platform\omc-fullstack-kit. Decision: NO integration as primary; preserve as emergency fallback only. Quality Gate: 2/5 verified (docs, P0 rules), 3/5 pending (browser, Playwright, Obsidian sync).* 
