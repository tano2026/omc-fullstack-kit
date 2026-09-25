# 🛠️ CẨM NANG CÀI ĐẶT & THIẾT LẬP OMC FULLSTACK KIT

> Hướng dẫn triển khai toàn diện bộ khung **One-Man Company (OMC)** trên bất kỳ máy tính mới nào (Windows, macOS, Linux, VPS Ubuntu).

---

## ⚡ 1. CÀI ĐẶT 1-CLICK (QUICK INSTALL)

### A. Trên Windows:
1. Mở thư mục dự án và click đúp vào file **`install.bat`** (hoặc chạy trong CMD / PowerShell):
   ```cmd
   install.bat
   ```
2. Bộ cài tự động:
   - Kiểm tra Python (>= 3.10) và Node.js (>= 20).
   - Tự động cài đặt toàn bộ thư viện Python trong `requirements.txt`.
   - Cài đặt **OpenClaw 2.0 Engine** toàn cục qua `npm install -g openclaw`.
   - Khởi tạo file cấu hình mẫu `config/.env`.

### B. Trên Linux / VPS (Ubuntu / Debian):
Chạy đúng 2 dòng lệnh:
```bash
chmod +x install.sh
./install.sh
```

---

## 🧩 2. CÁC THÀNH PHẦN ĐƯỢC CÀI ĐẶT & KẾT NỐI

| Thành phần | Cơ chế cài đặt & Vai trò | Vị trí trong Kit |
| :--- | :--- | :--- |
| **OpenClaw 2.0** | Engine thực thi terminal, git, devops, tự phục hồi lỗi 24/7. Cài qua `npm install -g openclaw@latest`. | `engines/openclaw_runtime/` |
| **Hermes Reasoner** | Tư duy chiều sâu (Chain-of-Thought), đặc tả kiến trúc và tự học kỹ năng mới. | `engines/hermes_reasoner/` |
| **DSH Planner** | Phân rã mục tiêu lớn thành các task con không phụ thuộc vòng lặp (DAG Task Breakdown). | `engines/dsh_planner/` |
| **JEV Gateway** | Cổng đón tin nhắn phản xạ 10ms và Rào chắn bảo mật phòng thủ Zero-Damage. | `engines/jev_gateway/` |
| **Obsidian Vault** | Bộ não thứ hai (Second Brain) quản lý dự án, OKR và sổ cái quyết định ADR. | `obsidian-vault/` |
| **Kho 722+ Skills** | Tích hợp sẵn 100% trong repo, không cần tải thêm từ bên ngoài. | `skills/` |

---

## 🔑 3. CẤU HÌNH API KEYS (CONFIG/.ENV)

Mở file `config/.env` và cập nhật khóa API:
```env
# Token Telegram Bot nhận việc từ điện thoại/máy tính (Lấy từ @BotFather)
TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"

# Khóa API OpenRouter ($0 Free Tier)
OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Model mặc định
DEFAULT_MODEL="openrouter/free"
```

---

## 📓 4. KẾT NỐI VỚI OBSIDIAN

1. Tải ứng dụng **Obsidian** (miễn phí) tại: [https://obsidian.md](https://obsidian.md).
2. Mở Obsidian ➔ Chọn **Open folder as vault**.
3. Chọn đường dẫn đến thư mục `obsidian-vault/` trong repo.
4. Bạn sẽ thấy toàn bộ cơ cấu công ty, Kanban dự án, sơ đồ tổ chức dạng đồ thị trực quan (Graph View) và các quyết định ADR.

---

## 🎯 5. BẮT ĐẦU VẬN HÀNH

- **Trò chuyện cùng Cố vấn Trưởng Hermes Copilot:**
  - Click đúp `copilot.bat` (Windows) hoặc `./copilot.sh` (Linux).
- **Khởi động Bot Telegram 24/7:**
  - Click đúp `start.bat` (Windows) hoặc `./start.sh` (Linux).
- **Nhân bản một công ty mới trong 8 giây:**
  ```cmd
  python clone_company.py --name "MyAgency" --domain "Digital Marketing & AI"
  ```
