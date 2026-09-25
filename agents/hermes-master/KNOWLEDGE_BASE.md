# 🗺️ KNOWLEDGE BASE: Bản Đồ Toàn Tri Hệ Thống OMC

> Tài liệu nội bộ nạp vào nhận thức của **Hermes Master Copilot** để nắm bắt 100% cấu trúc và tài nguyên của hệ thống.

---

## 1. CẤU TRÚC THƯ MỤC HỆ THỐNG (DIRECTORY SITEMAP)

- **`engines/`**:
  - `jev_gateway/ingress_router.py`: Bắt ý định System 1 trong 10ms từ Telegram/Webhook.
  - `jev_gateway/safety_guard.py`: Rào chắn phòng thủ an toàn Zero-Damage (chặn lệnh phá hoại).
  - `dsh_planner/goal_planner.py`: Bẻ mục tiêu lớn thành các task con DAG phi chu trình.
  - `trio_orchestrator.py`: Pipeline 5 pha phối hợp tự động giữa 4 động cơ.
- **`agents/`**:
  - `main`: Gateway router & dispatcher.
  - `dsh-commander`: Lập kế hoạch cấp cao.
  - `hermes-architect`: Thiết kế kiến trúc & code phức tạp.
  - `dev-automation`: Kỹ sư Full-Stack & Bot RPA.
  - `media-producer`: Kịch bản video viral & media AI.
  - `openclaw-executor`: DevOps & Execution 24/7.
  - `jev-sentinel`: Rào chắn an toàn dữ liệu.
  - `research-intel`: SEO / AEO & Nghiên cứu đối thủ.
  - `domain-ops`: Nghiên cứu & Vận hành nghiệp vụ công ty.
  - `hermes-master`: Tổng quản & Cố vấn tối cao (Chính tôi).
- **`skills/`**:
  - `core/`: 20 Kỹ năng nền tảng (`spec-driven`, `test-driven`, `task-breakdown`, `debugging`, `a11y`, `security-hardening`...).
  - `vault/`: 702 Kỹ năng chuyên sâu (ECC architecture, Tano marketing/agency, Video AI, Automation).
  - `manager.py`: Bộ CLI tra cứu, tìm kiếm và trang bị skill cho Agent.
- **`obsidian-vault/`**:
  - `01 - Org/`: Hồ sơ công ty, sơ đồ tổ chức, OKRs.
  - `02 - Projects/`: Quản lý Kanban và phân rã DAG.
  - `03 - Agents/`: Profile của 9 Agent.
  - `04 - Knowledge/`: Nguyên lý Quad-Engine & Cẩm nang AI model.
  - `05 - Templates/`: Mẫu Daily Note, ADR, Project Spec.
  - `06 - Inbox/`: Nơi tiếp nhận ý tưởng từ Telegram.
  - `07 - Decisions-ADR/`: Sổ cái quyết định kiến trúc được CEO duyệt.
  - `vault_sync.py`: Đồng bộ tự động 2 chiều Agent ⇄ Obsidian.
- **`gateway/`**:
  - `model_config.json`: Cấu hình OpenRouter Free + Failover 5 tầng.
  - `telegram_gateway.py`: Bot Telegram 24/7 bắt ý định tự động.
  - `webhook_server.py`: REST API Webhook cho Zalo/CRM/n8n.
- **`clone_company.py`**:
  - Script nhân bản 1-click tạo công ty OMC mới trong 8 giây: `python clone_company.py --name "<Ten>" --domain "<Nganh>"`.

---

## 2. NGUYÊN TẮC ĐIỀU PHỐI CỦA HERMES MASTER

Khi Chủ tịch giao một công việc bất kỳ:
1. **Phân tích:** Đánh giá xem thuộc phòng ban nào (Code, Media, SEO, Ops hay Kế hoạch lớn).
2. **Khảo sát Kỹ năng:** Kiểm tra xem Agent phụ trách đã có đủ skill chưa. Nếu thiếu, dùng `python skills/manager.py search <kw>` để tìm và trang bị bằng `assign`.
3. **Kích hoạt Pipeline:** Gọi `trio_orchestrator.py` hoặc chuyển tiếp cho đúng Agent.
4. **Ghi nhận Second Brain:** Đảm bảo mọi kết quả quan trọng đều được ghi vào `obsidian-vault/` thông qua `vault_sync.py`.
5. **Tự Học & Tối Ưu:** Nếu phát hiện ra phương pháp mới hoặc giải pháp đột phá, tạo ngay file `SKILL.md` mới lưu vào `skills/vault/` để công ty tự động nâng cấp trình độ.
