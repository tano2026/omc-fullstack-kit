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
     [🌐 Cổng Ingress Đa Kênh (Telegram / Webhook)]
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
| **`gateway/`** | **Cổng Kết Nối Đa Kênh**: Telegram Bot Bridge tự động định tuyến + Webhook REST API Server + Cấu hình OpenRouter Free Tier & Failover 5 tầng. |
| **`ecosystem.config.js`** | **Cấu hình PM2 Supervisor**: Đảm bảo toàn bộ hệ thống tự động khởi động lại khi crash hoặc máy tính reboot 24/7. |
| **`clone_company.py`** | **Tool Nhân Bản 1-Click**: Tạo mới 1 công ty OMC hoàn chỉnh độc lập chỉ trong vài giây. |

---

## 🚀 HƯỚNG DẪN BẮT ĐẦU NHANH

### 0. Cài Đặt Môi Trường (Lần đầu trên máy mới)
- **Windows:** Click đúp **`install.bat`**
- **Linux/Mac:** Chạy `./install.sh`

### 1. Bật Trợ Lý Điều Hành Hermes Master Copilot
- **Windows:** Click đúp **`copilot.bat`**
- **Linux/Mac:** Chạy `./copilot.sh`

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
