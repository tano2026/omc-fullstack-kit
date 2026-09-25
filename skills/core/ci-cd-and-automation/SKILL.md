---
name: ci-cd-and-automation
description: Thiết lập Quality Gates và tự động hóa kiểm tra build/test trong pipeline CI/CD.
---

# CI/CD and Automation

Thiết lập Quality Gates và tự động hóa kiểm tra build/test trong pipeline CI/CD.

## Khi sử dụng
- Khi cần thiết lập CI/CD pipeline cho dự án
- Khi cần thêm/chỉnh sửa automated checks
- Khi cần thiết lập deployment pipeline

## Tác động
- Tăng chất lượng code trước merge
- Giảm lỗi production
- Tự động hóa các tác vụ lặp lại

## Trình tự điển hình
1. Thiết lập CI pipeline (lint, type check, test, build)
2. Thiết lập CD pipeline (deploy staging/production)
3. Thiết lập Quality Gates (branch protection, required checks)
4. Thiết lập rollback mechanism

## Quy trình hoạt động
- Khi bắt đầu dự án mới hoặc thêm CI/CD cho dự án hiện có
- Khi cần thêm automated checks
- Khi cần thiết lập deployment pipeline

## Công cụ
- GitHub Actions / GitLab CI / Jenkins
- Quality Gates (branch protection, required checks)
- Deployment tools (Vercel, Docker, Kubernetes)

## Ví dụ (lưu ý ngắn gọn)
"Setup GitHub Actions CI: lint → typecheck → test → build → deploy staging → deploy production."

## Số đo thành công
- Pipeline chạy thành công (%)
- Thời gian pipeline
- Số lần rollback cần thiết
