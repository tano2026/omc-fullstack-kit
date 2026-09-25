# 🏛️ ADR-001: Lựa Chọn Kiến Trúc Quad-Engine (Trio + JEV) Cho OMC

- **Trạng thái:** Đã phê duyệt (Approved)
- **Tác giả:** Hermes Architect & DSH Commander
- **Ngày quyết định:** 2026-09-25

## 1. Ngữ cảnh
Một cá nhân vận hành toàn bộ công ty (One-Man Company) không thể tự tay làm hết mọi việc từ lập kế hoạch, code, media, nghiên cứu thị trường đến kiểm thử. Cần một hệ sinh thái AI tự hành nhưng phải đảm bảo:
- Không bị ảo giác (hallucination loop).
- Không phá hủy hệ thống dữ liệu (zero damage).
- Chi phí vận hành thấp nhất có thể.

## 2. Quyết định
Áp dụng mô hình **Quad-Engine kết hợp Obsidian Second Brain**:
- DSH quản lý mục tiêu (Planning).
- Hermes tư duy giải pháp (Reasoning).
- OpenClaw thực thi kỹ thuật 24/7 (Execution).
- JEV rào chắn an toàn 10ms (Safety & Router).
- Obsidian lưu trữ toàn bộ trạng thái và tri thức (Persistent Second Brain).

## 3. Kết quả
Hệ thống có thể nhân bản sang bất kỳ công ty hoặc dự án mới nào trong vòng 30 giây.
