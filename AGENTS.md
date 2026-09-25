# 🤖 Project Universal Agent Contract & Skill Matrix

> Tệp chỉ dẫn và quy chuẩn vận hành chung cho **Hermes Agent**, **Agent Harness (Claude Code)**, và **OpenClaw**.
> Mọi Agent khi tham gia vào dự án này **BẮT BUỘC** đọc và tuân thủ các quy định dưới đây.

---

## 1. PHÂN CHIA VAI TRÒ (OMC 9 SPECIALIZED AGENTS & QUAD-ENGINE)

Hệ thống vận hành theo mô hình **One-Man Company (OMC)** trên nền tảng **Quad-Engine: DSH (Planning) + Hermes (Reasoning) + OpenClaw (Execution) + JEV (Safety & Ingress Reflex)**:

1. **🌐 `main` (OMC JEV Gateway - System 1 Ingress Router):**
   - **Model:** `openrouter/free` (OpenRouter Auto-Free Router, $0 Free Tier).
   - **Chức năng:** Cổng đón tin nhắn đa kênh (Telegram, Webhook, CLI), nhận diện ý định và định tuyến tự động đến đúng Agent chuyên môn.
2. **🎯 `dsh-commander` (Chief Orchestrator & Goal Engine):**
   - **Model:** `deepseek/deepseek-chat` (DeepSeek-V3).
   - **Chức năng:** Lập kế hoạch cấp cao (DAG Task Breakdown), theo dõi tiến độ các mục tiêu lớn, điều phối phối hợp giữa các Agent.
3. **🏛️ `hermes-architect` (Senior Software & Systems Architect):**
   - **Model:** `deepseek/deepseek-reasoner` (DeepSeek-R1 CoT).
   - **Chức năng:** Phân tích tư duy chiều sâu, thiết kế kiến trúc hệ thống, audit thuật toán, refactor các module code phức tạp.
4. **💻 `dev-automation` (Senior Full-Stack & RPA/Bot Automation Engineer):**
   - **Model:** `deepseek/deepseek-chat` (DeepSeek-V3).
   - **Chức năng:** Code tính năng frontend/backend, automation script, RPA web crawler, bot webhook/Zalo/Telegram, tích hợp API.
5. **🎬 `media-producer` (Creative Director & AI Video Production):**
   - **Model:** `openrouter/free` (Free Tier).
   - **Chức năng:** Biên kịch video viral, short-form Reels/TikTok/YouTube Shorts, prompt visual AI (Midjourney/Runway), kịch bản quảng cáo.
6. **⚡ `openclaw-executor` (24/7 DevOps & Execution Commander):**
   - **Model:** `deepseek/deepseek-chat` (DeepSeek-V3).
   - **Chức năng:** Chạy lệnh terminal, build test, git commit, deploy server, kiểm thử trình duyệt, giám sát hạ tầng.
7. **🛡️ `jev-sentinel` (Safety & Quality Gatekeeper):**
   - **Model:** `openrouter/free`.
   - **Chức năng:** Rào chắn phòng thủ Zero-Damage. Kiểm duyệt bảo mật trước các lệnh nhạy cảm (xóa file, drop db, ghi đè config).
8. **📊 `research-intel` (Market Research & SEO/AEO/GEO Specialist):**
   - **Model:** `deepseek/deepseek-chat`.
   - **Chức năng:** Social listening, nghiên cứu đối thủ 30 ngày qua, crawl dữ liệu thị trường, audit và tối ưu thứ hạng SEO/AEO/GEO.
9. **✈️ `airport-ops` (An Binh Air Services Specialist):**
   - **Model:** `openrouter/free`.
   - **Chức năng:** Chuyên gia nghiệp vụ đón tiễn sân bay Nội Bài, Tân Sơn Nhất, Đà Nẵng, xử lý yêu cầu đặt dịch vụ Fast Track, VIP Lounge, xe đưa đón.

---

## 2. 6 NGUYÊN TẮC BẤT DI BẤT DỊCH (CORE OPERATING BEHAVIORS)

1. **Surface Assumptions:** Nêu rõ các giả định trước khi làm tính năng phức tạp:
   > *"Tôi đang giả định: [1. Yêu cầu... 2. Kiến trúc... 3. Phạm vi...] — Xác nhận để tôi tiếp tục."*
2. **Manage Confusion Actively:** Gặp mâu thuẫn yêu cầu hoặc code cũ khó hiểu ➔ **DỪNG LẠI** và hỏi rõ, tuyệt đối KHÔNG đoán mò.
3. **Push Back When Warranted:** Phản biện thẳng thắn khi giải pháp có vấn đề (chi phí cao, thêm độ trễ, rủi ro bảo mật).
4. **Enforce Simplicity:** Ưu tiên code ngắn gọn, đơn giản, ít trừu tượng thừa (*"Cleverness is expensive"*).
5. **Maintain Scope Discipline:** Chỉ sửa đúng phạm vi yêu cầu, không tự ý refactor lan man hoặc xóa code/comment ngoài phạm vi.
6. **Verify, Don't Assume:** Nhiệm vụ chỉ xong khi có bằng chứng chạy thực tế (test pass, build pass, output đúng).

---

## 3. KHO SKILL TỔNG & CƠ CHẾ LẤY SKILL THEO YÊU CẦU (CENTRAL SKILLS HUB)

Ngoài 20 skill cốt lõi đã có sẵn trong project, hệ thống sở hữu **Kho lưu trữ hơn 300+ Skills nội bộ và 90,000+ Skills toàn cầu**. Mọi Agent khi cần giải quyết các bài toán chuyên biệt đều phải truy xuất theo quy trình dưới đây:

### 📍 ĐỊA CHỈ KHO SKILL TRÊN MÁY (LOCAL CENTRAL REPOSITORIES)
1. **Kho tổng Master (Chứa 300+ Skills mọi lĩnh vực):**
   `D:\AI Store\AgentConfigs\hermes-local-appdata\skills\`
   - `ecc-*` (Hơn 150 skill chuyên sâu về Architecture, DevOps, Backend, Frontend, Testing, Security).
   - `tano/*` (30+ skill thực chiến Agency, Affiliate, SEO, Marketing, Automation).
   - `google-skills/*`, `devops/*`, `media/*`, `data-science/*`, `content/*`, `tuvi/*`.
2. **Kho User Global Skills:**
   `C:\Users\Nguyen Ngoc Tan\.agents\skills\`
3. **Kho Bundled của OpenClaw 2.0:**
   `D:\AI Store\OpenClaw\skills\`
4. **Kho Index Toàn cầu (91,400+ Skills):**
   `D:\AI Store\AgentConfigs\hermes-local-appdata\skills\.hub\index-cache\hermes-index.json`

---

### 🔍 CÁCH TỪNG AGENT TÌM KIẾM & LẤY SKILL TỪ KHO

#### A. Đọc trực tiếp không cần copy (On-Demand Direct Read):
Khi gặp bài toán chuyên ngành (ví dụ: cần cấu hình FastAPI, Docker, tối ưu Prompt, dựng Video, phân tích Tài chính):
- Agent quét thư mục `D:\AI Store\AgentConfigs\hermes-local-appdata\skills\` để tìm folder phù hợp.
- Đọc trực tiếp file `SKILL.md` (hoặc `.md`) trong folder đó để nạp tri thức và prompt mẫu.

#### B. Tự động nạp vào Project (Auto-Import to Project):
Nếu skill đó cần dùng thường xuyên cho project hiện tại, Agent copy thư mục skill từ kho tổng vào:
- `D:\TanoAgencyStorage\platform\omc\skills\<tên-skill>\`
- Tạo file `SKILL.md` chuẩn để toàn bộ các agent khác cùng thấy.

#### C. Lệnh tra cứu & cài đặt Online / CLI:
- **Hermes Agent:** `hermes skill search <từ-khóa>` hoặc tra cứu file `hermes-index.json`.
- **OpenClaw:** `openclaw skills search <từ-khóa>` và `openclaw skills install <tên-skill>`.
- **Agent Harness (Claude Code):** `/plugin marketplace add <tên-skill>` hoặc `npx skills add <url-github>`.

---

## 4. DANH SÁCH 20 SKILLS NỀN TẢNG BẮT BUỘC TRONG WORKSPACE

Tất cả 20 skill dưới đây đã được cài đặt sẵn tại `D:\TanoAgencyStorage\platform\omc\skills\`:

### 📌 Giai đoạn 1: DEFINE (Định nghĩa & Khai phá)
- **`interview-me`**: Phỏng vấn làm rõ nhu cầu thực sự của user trước khi lên spec hoặc code.
- **`idea-refine`**: Hoàn thiện ý tưởng thô qua tư duy phân kỳ & hội tụ (divergent & convergent).
- **`spec-driven-development`**: Viết tài liệu đặc tả và tiêu chí nghiệm thu (Acceptance Criteria) trước khi gõ code.

### 📌 Giai đoạn 2: PLAN (Lập kế hoạch)
- **`planning-and-task-breakdown`**: Bẻ nhỏ tính năng lớn thành chuỗi các task nhỏ, độc lập và kiểm chứng được.

### 📌 Giai đoạn 3: BUILD (Xây dựng & Phát triển)
- **`incremental-implementation`**: Xây dựng từng lát cắt mỏng (thin slices), test xong phần này mới mở rộng phần khác.
- **`context-engineering`**: Quản lý và nạp đúng tài liệu/ngữ cảnh vào đúng thời điểm, chống loãng context window.
- **`source-driven-development`**: Đối chiếu và xác thực code theo official docs mới nhất trước khi cài đặt.
- **`doubt-driven-development`**: Tự phản biện (adversarial review) đối với các quyết định kiến trúc phức tạp.
- **`frontend-ui-engineering`**: Xây dựng giao diện chuẩn UI/UX, responsive và đạt chuẩn tiếp cận (A11y).
- **`api-and-interface-design`** (*taste-skill / html-anything*): Thiết kế API & UI components có gu thẩm mỹ cao.

### 📌 Giai đoạn 4: VERIFY (Kiểm thử & Sửa lỗi)
- **`test-driven-dev`**: Chu trình TDD (Red-Green-Refactor): viết test lỗi trước, viết code pass test sau.
- **`browser-testing-with-devtools`**: Kiểm thử trực tiếp trên trình duyệt thật qua Chrome DevTools / Playwright MCP.
- **`debugging-and-error-recovery`**: Quy trình 4 bước: Tái hiện ➔ Khoanh vùng ➔ Sửa lỗi ➔ Tạo rào chắn chống tái phát.

### 📌 Giai đoạn 5: REVIEW (Đánh giá & Tối ưu)
- **`code-review-and-quality`**: Đánh giá code đa chiều theo 5 trục chất lượng trước khi merge.
- **`code-simplification`**: Rút gọn code, loại bỏ trừu tượng thừa, giữ code luôn dễ bảo trì nhất.
- **`security-hardening`** (*bumblebee*): Phòng ngừa lỗ hổng OWASP, kiểm tra validation đầu vào, rà soát bug logic.
- **`performance-optimization`**: Đo lường trước (Benchmark), chỉ tối ưu những điểm nghẽn thực sự ảnh hưởng hiệu năng.

### 📌 Giai đoạn 6: SHIP & OPS (Phát hành & Vận hành)
- **`git-workflow-and-versioning`**: Commit nguyên tử (Atomic commits), message chuẩn Conventional Commits, chia nhánh sạch.
- **`ci-cd-and-automation`**: Thiết lập Quality Gates và tự động hóa kiểm tra build/test trong pipeline CI/CD.
- **`documentation-and-adrs`**: Ghi lại tài liệu quyết định kiến trúc (ADR) và lý do đằng sau các giải pháp kỹ thuật.

---

## 5. QUY TRÌNH THỰC HIỆN TÁC VỤ (EXECUTION PIPELINE)

Mọi thay đổi code từ trung bình đến lớn đều phải trải qua chu trình 6 bước:
```
[1. Spec & Requirements] ➔ [2. Task Breakdown] ➔ [3. Write Tests (TDD)]
       ➔ [4. Incremental Code] ➔ [5. Verify & Bench] ➔ [6. Review & Commit]
```

---

## 6. HƯỚNG DẪN RA LỆNH VÀ ĐIỀU PHỐI (TELEGRAM & DSH CLI)

### 📱 A. Ra Lệnh Từ Telegram (Mobile & Desktop)

Bot Telegram kết nối trực tiếp với cổng `main` (JEV Ingress Gateway) 24/7. Bạn có thể tương tác theo 2 cách:

#### 1. Nhắn Tin Tự Nhiên (JEV Auto-Route - Khuyến nghị):
Chỉ cần gõ yêu cầu bằng tiếng Việt bình thường, `main` sẽ tự động phân loại trong 10ms và bàn giao cho Agent chuyên trách:
- *"Khách chuyến VN214 hạ cánh 14h30 cần 2 Fast Track T2 Nội Bài"* ➔ Tự động vào **`airport-ops`**.
- *"Nghiên cứu từ khóa và phân tích 5 đối thủ SEO dịch vụ đón tiễn sân bay"* ➔ Tự động vào **`research-intel`**.
- *"Lập kế hoạch xây dựng tính năng đặt tour tự động cho agency"* ➔ Tự động vào **`dsh-commander`**.
- *"Thiết kế kiến trúc cơ sở dữ liệu và API cho hệ thống booking mới"* ➔ Tự động vào **`hermes-architect`**.
- *"Viết script tự động đồng bộ đơn hàng từ Zalo Mini App về webhook"* ➔ Tự động vào **`dev-automation`**.
- *"Lên kịch bản 3 video ngắn TikTok/Reels viral cho dịch vụ VIP Lounge"* ➔ Tự động vào **`media-producer`**.
- *"Kiểm tra trạng thái server, PM2 và git pull bản mới nhất"* ➔ Tự động vào **`openclaw-executor`** (được duyệt bởi **`jev-sentinel`**).

#### 2. Nhắc Tên Trực Tiếp (Explicit Mention) hoặc Lệnh Điều Khiển:
- `@airport-ops <nội dung>`: Gửi việc trực tiếp cho Chuyên gia sân bay.
- `@research-intel <nội dung>`: Gửi việc trực tiếp cho Chuyên gia nghiên cứu thị trường / SEO.
- `@dsh-commander <nội dung>`: Gửi việc cho Chief Orchestrator.
- `@hermes-architect <nội dung>`: Gửi việc cho Kiến trúc sư hệ thống.
- `@dev-automation <nội dung>`: Gửi việc cho Kỹ sư Lập trình & Tự động hóa.
- `@media-producer <nội dung>`: Gửi việc cho Đạo diễn Video & Media AI.
- `@openclaw-executor <nội dung>`: Yêu cầu thực thi kỹ thuật.
- `/new` hoặc `/reset`: Khởi tạo phiên làm việc mới, xóa sạch ngữ cảnh cũ để tiết kiệm token.
- `/status`: Kiểm tra độ trễ gateway, các agent đang chạy và mức tiêu thụ token.

---

### 💻 B. Ra Lệnh Từ DSH (DeepSeek Harness / Terminal / Workspace)

Khi ngồi máy tính làm việc trực tiếp tại terminal hoặc qua DSH:

#### 1. Chạy Chuỗi Phối Hợp Trio + JEV (Tự động 5 pha):
```bash
node skills/dsh-hermes-openclaw-trio/workflow-trio.js "Xây dựng landing page cho dịch vụ VIP Lounge Nội Bài"
```
Quy trình sẽ tự động kích hoạt:
1. `JEV Ingress Gate`: Kiểm tra tính khả thi và định tuyến.
2. `DSH Planning`: Phân tách việc thành các task nhỏ (DAG).
3. `Hermes Architecture`: Thiết kế cấu trúc code và giải pháp.
4. `JEV Safety Guard`: Đánh giá rủi ro (đảm bảo không xung đột hạ tầng).
5. `OpenClaw Execution`: Tạo file, chạy test và hoàn tất.

#### 2. Gọi Trực Tiếp Từng Agent Qua CLI:
```bash
# Giao việc cho dsh-commander lập kế hoạch
openclaw agent --agent dsh-commander --prompt "Lập kế hoạch refactor hệ thống thanh toán"

# Giao việc cho research-intel quét dữ liệu
openclaw agent --agent research-intel --prompt "Cào và tổng hợp đánh giá khách hàng về Fast Track 30 ngày qua"

# Giao việc cho airport-ops tra cứu quy chuẩn
openclaw agent --agent airport-ops --prompt "Quy định hành lý và thủ tục hải quan VIP tại T2 Nội Bài"
```

