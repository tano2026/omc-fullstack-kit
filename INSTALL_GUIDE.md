# 🛠️ CẨM NANG CÀI ĐẶT & THIẾT LẬP OMC FULLSTACK KIT

> Hướng dẫn triển khai toàn diện bộ khung **One-Man Company (OMC)** trên bất kỳ máy tính mới nào (Windows, macOS, Linux, VPS Ubuntu) tích hợp sẵn **Dev Superpowers & Harness Engineering**.

---

## ⚡ 1. CÀI ĐẶT 1-CLICK (QUICK INSTALL)

### A. Trên Windows:
1. Mở thư mục dự án và click đúp vào file **`install.bat`** (hoặc chạy trong CMD / PowerShell):
   ```cmd
   install.bat
   ```
2. Bộ cài tự động:
   - Kiểm tra Python (>= 3.10) và Node.js (>= 20).
   - Tự động cài đặt toàn bộ thư viện Python trong `requirements.txt` (bao gồm `filelock`, `fastapi`, `pydantic`).
   - Cài đặt **OpenClaw 2.0 Engine** và **PM2 Supervisor** toàn cục.
   - Khởi tạo file cấu hình mẫu `config/.env`.
   - Kiểm tra độ an toàn của JEV Sentinel & kích hoạt bộ Developer Superpowers.

### B. Trên Linux / VPS (Ubuntu / Debian):
Chạy đúng 2 dòng lệnh:
```bash
chmod +x install.sh
./install.sh
```

---

## 🚀 2. BỘ CÔNG CỤ DEVELOPER SUPERPOWERS & HARNESS (TÍCH HỢP SẴN)

Bộ kit đi kèm công cụ phát triển phần mềm chuẩn mực theo triết lý **Jesse Vincent (Superpowers)** và **Mitchell Hashimoto / Anthropic (Harness Engineering)**:

| Lệnh / Flag | Quy trình thực hiện | Ý nghĩa |
| :--- | :--- | :--- |
| **`/spec`** | Lập đặc tả yêu cầu & Acceptance Criteria (AC) | Làm rõ tiêu chí nghiệm thu trước khi gõ 1 dòng code |
| **`/plan`** | Phân rã mục tiêu thành DAG tasks | Bẻ nhỏ việc thành các phần việc độc lập |
| **`/build`** | Test-Driven Development (TDD) | Vòng lặp Red-Green-Refactor: viết test trước |
| **`/review`** | 5-Axis Quality Code Review | Đánh giá Correctness, Security, Simplicity, Performance, ADR |
| **`/ship`** | JEV Sentinel Safety Gate & Commit | Kiểm duyệt Zero-Damage và tạo git commit nguyên tử |
| **`/eval`** | Closed-Loop Evaluation Gate | Kiểm chứng 100% assertions, chống ảo giác (hallucination) |

### Cách chạy:
- **Windows:** Click đúp `dev-superpowers.bat` hoặc:
  ```cmd
  python engines\harness\dev_harness.py --action all --task "Tên tính năng cần làm"
  ```
- **Linux/Mac:** `./dev-superpowers.sh --action all --task "Tên tính năng cần làm"`
- **Qua npm:** `npm run superpowers` hoặc `npm run harness`

---

## 🛡️ 3. TÍNH NĂNG BẢO MẬT & VÒNG LẶP TỰ PHỤC HỒI (SECURITY & RESILIENT LOOP)

1. **JEV Sentinel Zero-Damage Guard & Secret Sanitizer (`engines/jev_gateway/safety_guard.py`):**
   - Chặn đứng 100% các lệnh phá hoại: `rm -rf`, `drop table`, `format`, `dd`, `git push -f origin main`.
   - Tự động che giấu (mask) API Key, Telegram Bot Token khỏi toàn bộ terminal log.
2. **Obsidian Thread-Safe & Atomic Lock (`obsidian-vault/vault_sync.py`):**
   - Chống xung đột ghi đè Markdown khi nhiều agent chạy song song.
   - Cơ chế ghi đè nguyên tử (Atomic replace qua `.tmp`).
3. **Resilient LLM Loop với Exponential Backoff & 5-Layer Failover (`engines/llm_client.py`):**
   - Tự động bắt lỗi HTTP 429 (Rate Limit), 503 để chờ thử lại theo hàm mũ (`2^attempt + jitter`).
   - Tự động nhảy sang model kế tiếp trong chuỗi failover: `openrouter/free` ➔ `nous-hermes-70b` ➔ `deepseek-chat` ➔ `omniroute` ➔ `gemini-2.5-flash`.
4. **Vận hành 24/7 với PM2 Supervisor:**
   - Khởi động giám sát nền: `npm run pm2:start`
   - Xem log real-time: `npm run pm2:logs`
   - Dừng hệ thống: `npm run pm2:stop`

---

## 🔑 4. CẤU HÌNH API KEYS (CONFIG/.ENV)

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

## 📓 5. KẾT NỐI VỚI OBSIDIAN (SECOND BRAIN)

1. Tải ứng dụng **Obsidian** (miễn phí) tại: [https://obsidian.md](https://obsidian.md).
2. Chọn **"Open folder as vault"** ➔ Trỏ tới thư mục:
   `omc-fullstack-kit/obsidian-vault`
3. Mở file `02 - Projects/TASKBOARD.md` để xem toàn cảnh tiến độ các dự án và luồng quyết định ADR.
