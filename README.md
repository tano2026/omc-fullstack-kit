# 🏢 OMC Fullstack Kit (One-Man Company Master Blueprint)

> **Bản đóng gói hoàn chỉnh Fullstack Master cho mô hình One-Man Company (OMC)**  
> Kết hợp hoàn hảo giữa **Quad-Engine Trio + JEV**, **Obsidian Second Brain**, và **Dev Superpowers & Harness Engineering Suite**.  
> Thiết lập công ty tự hành 24/7, tự phục hồi lỗi với vòng lặp Resilient Loop, và hỗ trợ **Nhân bản (Clone) công ty mới chỉ trong vài giây**.

---

## 🌟 TỔNG QUAN KIẾN TRÚC

```
[Người dùng / Khách hàng / Webhook / Telegram]
                 │
                 ▼
     [🌐 Cổng Ingress Đa Kênh (Telegram / Webhook / Web Chat)]
                 │
                 ▼
       [⚡ JEV Ingress Router (~10ms Reflex)]
                 │
                 ├── 🛡️ JEV Sentinel (Zero-Damage Safety Gate & Secret Sanitizer)
                 │
                 ├── 🎯 DSH Commander (DAG Task Breakdown & Goals)
                 │
                 ├── 🏛️ Hermes Architect (Deep Systems Reasoning & Spec)
                 │
                 ├── 🚀 Dev Harness & Superpowers (/spec -> /plan -> /build -> /review -> /ship)
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
                 [⚡ JEV Eval Gate 3 (Closed-Loop Delivery Gate)]
                                 │
                                 ▼
                 [📓 Obsidian Second Brain (Persistent Memory & Thread-Safe Sync)]
```

---

## 💬 CÁC KÊNH TƯƠNG TÁC ĐỂ TRÒ CHUYỆN (UI & CHAT CHANNELS)

Bộ kit cung cấp đầy đủ các kênh giao diện chat bản địa của **Hermes**, **OpenClaw**, **DSH** và **OMC Web/Telegram**:

| Kênh tương tác | Cách bật 1-Click | Nơi hiển thị & Tính năng |
| :--- | :--- | :--- |
| **🏛️ Hermes Web Dashboard** | **`hermes-dashboard.bat`** (hoặc `npm run hermes:ui`) | Web UI bản địa của Hermes tại `http://localhost:9119`, quản lý session, skill, model, memory graph. |
| **🏛️ Hermes Agent Chat (TUI)** | **`hermes-chat.bat`** (hoặc `npm run hermes:chat`) | Giao diện Terminal UI bản địa của Hermes, tương tác sâu với chuỗi tư duy (CoT). |
| **⚡ OpenClaw Control UI** | **`openclaw-dashboard.bat`** (hoặc `npm run openclaw:ui`) | Web Control Panel bản địa của OpenClaw 2.0, quản lý 24/7 nodes, agents, devices. |
| **⚡ OpenClaw Chat (TUI)** | **`openclaw-chat.bat`** (hoặc `npm run openclaw:chat`) | Giao diện Chat dòng lệnh của OpenClaw, giao tiếp trực tiếp với runtime OpenClaw. |
| **🎯 DSH & Master Copilot** | **`copilot.bat`** (hoặc `npm run copilot`) | Trợ lý Chief of Staff điều phối Quad-Engine và kho 722+ skills qua CLI. |
| **🌐 OMC Web Chat Center** | **`chat.bat`** (hoặc `npm run chat`) | Giao diện Web Chat trực quan tại `http://localhost:19888` chọn nhanh 9 phòng ban. |
| **📱 Telegram Mobile Bot** | **`start.bat`** (hoặc `npm run pm2:start`) | Chat trực tiếp từ điện thoại thông minh 24/7 qua bot Telegram. |

---

## 📁 CẤU TRÚC BỘ FULLSTACK MASTER

| Thư mục / File | Chức năng chi tiết |
| :--- | :--- |
| **`install.bat` / `install.sh`** | **Bộ Cài Đặt Tự Động 1-Click**: Cài Python deps, Node.js, OpenClaw 2.0, PM2 Supervisor, test an toàn JEV và Superpowers. |
| **`dev-superpowers.bat` / `dev-superpowers.sh`** | **Bộ Công Cụ Dev Superpowers & Harness**: Quy trình chuẩn `/spec`, `/plan`, `/build` (TDD), `/review`, `/ship` và `/eval`. |
| **`copilot.bat` / `copilot.sh`** | **Trợ Lý Ruột & Cố Vấn Tối Cao Hermes Master**: Hướng dẫn, onboard, điều phối và tự học kỹ năng mới. |
| **`engines/`** | **Bộ Lõi Quad-Engine Trio + JEV** + **Dev Harness** + **Resilient LLM Client** (Exponential Backoff + 5-Layer Failover). |
| **`agents/`** | **9 Phòng Ban Chuyên Môn** (`main`, `dsh-commander`, `hermes-architect`, `dev-automation`, `media-producer`, `openclaw-executor`, `jev-sentinel`, `research-intel`, `domain-ops`). |
| **`obsidian-vault/`** | **Bộ Não Thứ Hai (Second Brain)**: Quản trị mục tiêu, dự án, sổ cái ADR có cơ chế khóa an toàn chống xung đột đa tiến trình. |
| **`skills/`** | **Kho Tổng 720+ Skills**: Gồm 25 Foundation Core Skills (Superpowers, Harness, TDD, CI/CD...) và hơn 700 skills chuyên ngành tra cứu qua `manager.py`. |
| **`gateway/`** | **Cổng Kết Nối Đa Kênh**: Telegram Bot Bridge tự động định tuyến + Webhook REST API Server + Web Chat trực quan. |
| **`ecosystem.config.js`** | **Cấu hình PM2 Supervisor**: Đảm bảo toàn bộ hệ thống tự động khởi động lại khi crash hoặc máy tính reboot 24/7. |
| **`clone_company.py`** | **Tool Nhân Bản 1-Click**: Tạo mới 1 công ty OMC hoàn chỉnh độc lập chỉ trong vài giây. |

---

## 🚀 HƯỚNG DẪN BẮT ĐẦU NHANH

### 0. Cài Đặt Môi Trường (Lần đầu trên máy mới)
- **Windows:** Click đúp **`install.bat`**
- **Linux/Mac:** Chạy `./install.sh`

### 1. Bật Giao Diện Chat Bạn Thích
- **Mở Hermes Web Dashboard:** Click đúp **`hermes-dashboard.bat`**
- **Mở OpenClaw Control Panel:** Click đúp **`openclaw-dashboard.bat`**
- **Mở OMC Web Chat Center:** Click đúp **`chat.bat`**
- **Mở Hermes Master Copilot (CLI):** Click đúp **`copilot.bat`**

### 2. Sử Dụng Dev Superpowers & Harness Engineering
- **Windows:** Click đúp **`dev-superpowers.bat`** hoặc:
  ```cmd
  python engines\harness\dev_harness.py --action all --task "Tên tính năng cần code"
  ```
- Quy trình chuẩn 5 pha: `/spec` ➔ `/plan` ➔ `/build` (TDD) ➔ `/review` ➔ `/ship` ➔ `/eval`

### 3. Khởi Động Vận Hành 24/7
- **Chạy trực tiếp:** Click đúp **`start.bat`** (hoặc `./start.sh`)
- **Chạy nền 24/7 bằng PM2:**
  ```bash
  npm run pm2:start
  ```
  Xem log: `npm run pm2:logs` | Dừng lại: `npm run pm2:stop`

### 4. Nhân Bản Công Ty Mới (Cloning)
```bash
python clone_company.py --name "an-binh-travel" --domain "Du lịch & Đón tiễn Sân bay VIP"
```

---

## 🛡️ TÍNH NĂNG BẢO MẬT & VÒNG LẶP RESILIENT LOOP

1. **JEV Sentinel Zero-Damage Defense:** Tự động chặn các mẫu lệnh nguy hiểm (`rm -rf`, `drop table`, `format`, `git push -f`) và che giấu toàn bộ API tokens trong log.
2. **Thread-Safe Obsidian Sync:** Sử dụng cơ chế khóa phân tán và Atomic File Replace để đảm bảo nhiều agent cùng ghi log không bị corrupt file.
3. **Resilient LLM Loop:** Cơ chế Exponential Backoff với Jitter tự động vượt qua tình trạng Rate Limit (429/503) và nhảy tầng trong 5 lớp failover:
   `openrouter/free` ➔ `nous-hermes-70b` ➔ `deepseek-chat` ➔ `omniroute` ➔ `gemini-2.5-flash`
4. **JEV Closed-Loop Delivery Gate:** Đóng gói sản phẩm với 100% assertions được kiểm chứng, loại bỏ hoàn toàn hiện tượng báo cáo ảo.
