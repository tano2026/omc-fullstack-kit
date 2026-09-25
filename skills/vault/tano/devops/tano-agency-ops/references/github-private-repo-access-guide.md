---
name: github-private-repo-access
description: "Hướng dẫn cấu hình truy cập repo GitHub private bằng GITHUB_TOKEN."
---

# 🔒 Truy cập Repo GitHub Private bằng GITHUB_TOKEN

Khi làm việc với các repo GitHub private, cần cấu hình `GITHUB_TOKEN` để các công cụ và agent có thể truy cập repo.

## 🔑 Tạo GITHUB_TOKEN (Personal Access Token)

1.  **Đăng nhập GitHub:** Đăng nhập vào tài khoản GitHub của bạn.
2.  **Settings:** Truy cập Settings > Developer settings > Personal access tokens.
3.  **Chọn loại Token:**
    *   **Tokens (classic):** Dạng `ghp_***`. Thường dùng cho các quyền rộng hơn (`repo` cho full control) nhưng cũng rủi ro hơn.
    *   **Fine-grained tokens:** Dạng `github_pat_***`. Cho phép cấp quyền chi tiết hơn (chỉ `Contents Read-only` cho một repo cụ thể), an toàn hơn cho các tác vụ chỉ đọc. **Đây là loại token được khuyến nghị cho các tác vụ chỉ đọc repo private.**
4.  **Tạo token mới:**
    *   Nếu chọn **classic**, cấp các quyền (scopes) cần thiết (ví dụ: `repo` cho full control nếu cần).
    *   Nếu chọn **fine-grained**, chọn repo cụ thể và cấp quyền `Contents Read-only` (hoặc các quyền khác tùy nhu cầu).
    *   **Lưu ý:** Chỉ cấp các quyền cần thiết để đảm bảo bảo mật.
5.  **Lưu token:** Lưu giá trị token vào một nơi an toàn. Token này chỉ hiển thị một lần.

## 💻 Cấu hình GITHUB_TOKEN cho Hermes Agent (Local)

Để Hermes Agent có thể truy cập repo private từ máy local:

1.  **Chỉnh sửa `~/.bashrc`:** Thêm dòng sau vào cuối file `~/.bashrc` (hoặc cập nhật nếu đã có):
    ```bash
    export GITHUB_TOKEN="***" # Thay thế bằng token của bạn
    ```
    **Lưu ý quan trọng:** Đảm bảo paste TOÀN BỘ token, không có khoảng trắng thừa hoặc ký tự bị cắt cụt.
2.  **Load lại môi trường:** Chạy `source ~/.bashrc` để biến môi trường có hiệu lực ngay lập tức.

3.  **Kiểm tra:** `echo $GITHUB_TOKEN` để xác nhận biến đã được set.

## 🌐 Cấu hình GITHUB_TOKEN cho OpenClaw/Agent trên VPS

Nếu bạn có các process agent (như OpenClaw, OmniRoute) chạy trên VPS và cần truy cập repo private:

1.  **Đối với PM2 (nếu dùng):**
    *   Cập nhật biến môi trường cho process cụ thể (ví dụ: OpenClaw có ID 40):
        ```bash
        pm2 set <app_id> GITHUB_TOKEN github_pat_...
        pm2 restart <app_id> --update-env
        ```
    *   (Trong trường hợp này: `pm2 set 40 GITHUB_TOKEN github_pat_...`)

2.  **Đối với file `.env` (nếu dùng):**
    *   Chỉnh sửa file `.env` mà process đó đang đọc để thêm/cập nhật dòng `GITHUB_TOKEN=***`
    *   Sử dụng `sed` để thay thế an toàn (cần `sudo`):
        ```bash
        sudo sed -i "s|^GITHUB_TOKEN=.*|GITHUB_TOKEN=github_pat_...|" /path/to/your/app/.env
        ```
    *   Khởi động lại process để thay đổi có hiệu lực.

### ✅ Xác minh truy cập (BẮT BUỘC)

Sử dụng `curl` để kiểm tra khả năng truy cập một file từ repo private. **Thực hiện các bước này trên MỌI môi trường bạn đã cấu hình token:**

1.  **Kiểm tra tính toàn vẹn của token:**
    *   **Độ dài:** Kiểm tra độ dài token. Ví dụ, token fine-grained PAT thường có 93 ký tự. Nếu ra số khác, token bị cắt cụt hoặc dính ký tự thừa:
        ```bash
        echo -n "$GITHUB_TOKEN" | wc -c
        ```
    *   **Ký tự đầu:** Kiểm tra các ký tự đầu token để đảm bảo đúng loại token và không dùng nhầm token cũ (ví dụ: `github_pat_11B3` cho fine-grained PAT):
        ```bash
        echo "$GITHUB_TOKEN" | head -c 15
        ```
    *   **Nếu độ dài hoặc ký tự đầu không khớp:** **Paste lại token từ nguồn gốc một cách cẩn thận, đảm bảo không có khoảng trắng hoặc ký tự thừa.**

2.  **Xác minh quyền truy cập API GitHub (ưu tiên):**
    *   Dùng lệnh `curl` này để kiểm tra HTTP status code khi cố gắng truy cập một file trong repo private (ví dụ: `KHO-INDEX.md`):
        ```bash
        curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/<user>/<repo>/contents/<path/to/file.md>
        ```
    *   **Kết quả mong muốn:** `200` (thành công).
    *   **Nếu ra `401` (Bad credentials):** Token không hợp lệ hoặc không có quyền truy cập repo. Cần kiểm tra lại token trên GitHub dashboard hoặc cấp quyền.
    *   **Nếu ra `404` (Not Found):** Có thể đường dẫn file hoặc tên nhánh sai.

3.  **Xác minh truy cập Raw Content (cách thay thế, ít đáng tin cậy hơn):**
    *   Để fetch nội dung file trực tiếp (chứ không phải API JSON):
        ```bash
        curl -H "Authorization: token $GITHUB_TOKEN" https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path/to/file.md>
        ```
    *   Thay `<user>`, `<repo>`, `<branch>`, `<path/to/file.md>` bằng thông tin chính xác của bạn.
    *   Nếu trả về nội dung file (không phải 404 hoặc 401), thì đã thành công.


-   **Token là READ-ONLY:** Đảm bảo token chỉ có các quyền cần thiết để tránh rủi ro (đặc biệt khi cấp cho các agent).
-   **KHÔNG ghi token vào log/script/file công khai:** Token chỉ nên nằm trong biến môi trường hoặc các file cấu hình được bảo mật.
-   **Xóa token cũ:** Xóa các token cũ hoặc không cần thiết để giảm thiểu rủi ro.
