# 🏢 OMC Fullstack Kit (One-Man Company Master Blueprint)

> **Bản đóng gói hoàn chỉnh Fullstack Master cho mô hình One-Man Company (OMC)**  
> Kết hợp hoàn hảo giữa **Quad-Engine Trio + JEV** và **Obsidian Second Brain**.  
> Thiết lập công ty tự hành 24/7 và hỗ trợ **Nhân bản (Clone) ra công ty mới chỉ trong 30 giây**.

---

## 🌟 TỔNG QUAN KIẾN TRÚC

```
[Người dùng / Khách hàng / Webhook]
                 │
                 ▼
     [🌐 Cổng Ingress Đa Kênh (Telegram / Webhook)]
                 │
                 ▼
       [⚡ JEV Ingress Router (~10ms Reflex)]
                 │
                 ├── 🛡️ JEV Sentinel (Zero-Damage Safety Gate)
                 │
                 ├── 🎯 DSH Commander (DAG Task Breakdown & Goals)
                 │
                 ├── 🏛️ Hermes Architect (Deep Systems Reasoning & Spec)
                 │
                 ├── 💻 Dev Automation (Full-Stack & RPA Bots)
                 │
                 ├── 🎬 Media Producer (Video AI & Viral Content)
                 │
                 ├── 📊 Research Intel (SEO / AEO / Market Research)
                 │
                 ├── 💼 Domain Ops (Vận Hành Nghiệp Vụ Công Ty)
                 │
                 └── ⚡ OpenClaw Executor (Thực Thi Terminal & DevOps 24/7)
                                 │
                                 ▼
                 [📓 Obsidian Second Brain (Persistent Memory)]
```

---

## 📁 CẤU TRÚC BỘ FULLSTACK MASTER

| Thư mục / File | Chức năng chi tiết |
| :--- | :--- |
| **`install.bat` / `install.sh`** | **Bộ Cài Đặt Tự Động 1-Click**: Tự động cài Python deps, Node.js, OpenClaw 2.0, Hermes, DSH, JEV trên máy mới. |
| **`copilot.bat` / `copilot.sh`** | **Trợ Lý Ruột & Cố Vấn Tối Cao Hermes Master**: Hướng dẫn, onboard, điều phối và tự học kỹ năng mới. |
| **`engines/`** | **Bộ Lõi Quad-Engine Trio + JEV** (DSH Planning + Hermes Reasoner + OpenClaw Runner + JEV Gateway & Safety Guard). |
| **`agents/`** | **9 Phòng Ban Chuyên Môn** (`main`, `dsh-commander`, `hermes-architect`, `dev-automation`, `media-producer`, `openclaw-executor`, `jev-sentinel`, `research-intel`, `domain-ops`). |
| **`obsidian-vault/`** | **Bộ Não Thứ Hai (Second Brain)**: Quản trị mục tiêu, dự án, nhật ký, quyết định ADR và tự động đồng bộ 2 chiều với Agent qua `vault_sync.py`. |
| **`skills/`** | **Kho Tổng 700+ Skills**: Gồm 20 Foundation Skills cốt lõi và hơn 700 skills chuyên ngành (ECC, Tano Agency, Video AI, Automation) quản lý qua `manager.py`. |
| **`gateway/`** | **Cổng Kết Nối Đa Kênh**: Telegram Bot Bridge tự động định tuyến + Webhook REST API Server + Cấu hình OpenRouter Free Tier & Failover 5 tầng. |
| **`clone_company.py`** | **Tool Nhân Bản 1-Click**: Tạo mới 1 công ty OMC hoàn chỉnh độc lập chỉ trong 30 giây. |
| **`start.bat` / `start.sh`** | File chạy 1-click kích hoạt toàn bộ công ty trên Windows hoặc Linux. |

---

## 🚀 HƯỚNG DẪN BẮT ĐẦU NHANH

### 0. Cài Đặt Môi Trường (Lần đầu trên máy mới)
- **Windows:** Click đúp **`install.bat`** (Tự động cài OpenClaw 2.0, requirements, config).
- **Linux/VPS:** Chạy `./install.sh`.
- Chi tiết xem tại [INSTALL_GUIDE.md](file:///d:/TanoAgencyStorage/platform/omc-fullstack-kit/INSTALL_GUIDE.md).

### 1. Trò Chuyện & Làm Việc Cùng Cố Vấn Hermes Master
- Click đúp **`copilot.bat`** (Windows) hoặc `./copilot.sh` (Linux).
- Hermes Master am hiểu toàn bộ hệ sinh thái, hướng dẫn và điều phối các phòng ban cho bạn.

### 2. Khởi Động Telegram Ingress Gateway 24/7
- **Trên Windows:** Click đúp vào `start.bat`
- **Trên Linux / VPS:** Chạy `./start.sh`

### 2. Nhân Bản Công Ty Mới (1-Click Cloning)
Muốn tạo một công ty mới (Ví dụ: Công ty Dịch Vụ Sân Bay `AnBinhAir` hoặc Agency Marketing `TanoAgency`):
```bash
python clone_company.py --name "AnBinhAir" --domain "Airport VIP Services" --bot-token "YOUR_TELEGRAM_BOT_TOKEN"
```
Hệ thống sẽ tự động:
1. Tạo thư mục `platform/companies/AnBinhAir` độc lập.
2. Sinh Obsidian Vault riêng gắn thương hiệu và thông số công ty.
3. Tạo sẵn 9 Agent chuyên môn được tùy biến riêng cho lĩnh vực `Airport VIP Services`.
4. Cấu hình Telegram Gateway và script khởi chạy riêng `start.bat` / `start.sh`.

---

## 🧰 QUẢN LÝ KHO 700+ SKILLS

Trong thư mục `skills/`:
- **Xem danh sách 20 core skills:**
  ```bash
  python skills/manager.py list
  ```
- **Tìm kiếm skill bất kỳ trong kho 700+ skills:**
  ```bash
  python skills/manager.py search "video"
  python skills/manager.py search "docker"
  python skills/manager.py search "seo"
  ```
- **Trang bị thêm skill cho một Agent:**
  ```bash
  python skills/manager.py assign --agent media-producer --skill viral-hooks
  python skills/manager.py assign --agent dev-automation --skill fastapi-patterns
  ```

---

## 📓 KẾT NỐI OBSIDIAN SECOND BRAIN

1. Mở ứng dụng **Obsidian**.
2. Chọn **Open folder as vault** ➔ Trỏ đến thư mục `obsidian-vault/`.
3. Toàn bộ tiến độ dự án, ý tưởng từ Telegram, và các quyết định kiến trúc (ADR) sẽ được hiển thị trực quan dạng đồ thị (Graph View) và Kanban.

---

## 🛡️ NGUYÊN TẮC BẢO VỆ ZERO-DAMAGE

Mọi lệnh terminal và thao tác code do Agent thực hiện đều phải đi qua **JEV Sentinel**:
- Tự động chặn các lệnh phá hoại: `rm -rf /`, `del /f /s /q`, `drop database`, `truncate`.
- Tự động che giấu (Redact) các Secret Key và API Tokens.
- Báo cáo và yêu cầu phê duyệt khi thao tác chạm vào file cấu hình trọng yếu.
