---
name: documentation-and-adrs
description: Ghi lại tài liệu quyết định kiến trúc (ADR) và lý do đằng sau các giải pháp kỹ thuật.
---

# Documentation and ADRs

Ghi lại tài liệu quyết định kiến trúc (ADR) và lý do đằng sau các giải pháp kỹ thuật.

## Khi sử dụng
- Khi cần ghi lại quyết định kiến trúc
- Khi cần document design choices
- Khi cần giải thích lý do đằng sau giải pháp kỹ thuật

## Tác động
- Tăng khả năng bảo trì
- Cải thiện onboarding cho team mới
- Giảm thiểu hiểu lầm về design choices

## Trình tự điển hình
1. Xác định quyết định cần document
2. Ghi ADR (Architecture Decision Record)
3. Review và approve
4. Publish cho team

## Quy trình hoạt động
- Khi có quyết định kiến trúc quan trọng
- Khi cần document design choices
- Khi cần giải thích lý do đằng sau giải pháp kỹ thuật

## Công cụ
- ADR template
- Documentation tools (Markdown, wiki, etc.)

## Ví dụ (lưu ý ngắn gọn)
"ADR: Chọn PostgreSQL thay vì MongoDB vì project cần ACID transactions và complex queries."

## Số đo thành công
- Số lượng ADR được tạo
- Thời gian onboarding cho member mới
- Số lần hiểu lầm về design choices
