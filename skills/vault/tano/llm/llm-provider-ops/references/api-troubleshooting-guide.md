# API Connection Troubleshooting Guide (Vietnamese)

## Hướng dẫn gỡ rối kết nối API cho LLM Providers

### Các bước kiểm tra cơ bản

1. **Kiểm tra cấu hình Hermes**
   ```bash
   hermes config show | grep -i -E 'provider|key|model'
   ```

2. **Kiểm tra biến môi trường**
   ```bash
   echo $OPENROUTER_API_KEY
   echo $HHTECH_API_KEY
   echo $GEMINI_API_KEY
   ```

3. **Kiểm tra file .env**
   ```bash
   # Kiểm tra file .env chính
   cat ~/.hermes/.env | grep -E 'API_KEY|SECRET'
   
   # Kiểm tra file .env cụ thể cho dự án
   cat /path/to/project/.env | grep -E 'API_KEY|SECRET'
   ```

4. **Test trực tiếp bằng curl**
   ```bash
   # Test OpenRouter
   curl -v "https://openrouter.ai/api/v1/chat/completions" \
     -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "anthropic/claude-3.5-sonnet",
       "messages": [{"role": "user", "content": "Xin chào"}],
       "max_tokens": 10
     }'
   
   # Test HHTech API (OpenRouter-compatible)
   curl -v "https://hhtechapi.com/v1/chat/completions" \
     -H "Authorization: Bearer $HHTECH_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "claude-opus-4-8",
       "messages": [{"role": "user", "content": "Xin chào"}],
       "max_tokens": 10
     }'
   ```

5. **Kiểm tra trạng thái dịch vụ**
   - OpenRouter: https://status.openrouter.ai
   - HHTech: Kiểm tra trang status của họ
   - Google Gemini: https://status.cloud.google.com
   - Anthropic: https://status.anthropic.com

### Các lỗi thường gặp và cách giải决

#### Lỗi 401 Unauthorized
- **Nguyên nhân**: API key sai, hết hạn, hoặc chưa được kích hoạt
- **Giải pháp**:
  1. Kiểm tra lại API key trong dashboard của provider
  2. Tạo API key mới nếu cần
  3. Đảm bảo key được copy đúng (không có khoảng trắng thừa)
  4. Kiểm tra xem key có bị giới hạn bởi IP hay không

#### Lỗi 400 Bad Request
- **Nguyên nhân**: Sai model name, sai định dạng request, hoặc thiếu tham số bắt buộc
- **Giải pháp**:
  1. Kiểm tra lại tên model (ví dụ: `claude-3-5-sonnet-20241022` thay vì `claude-sonnet-4-5`)
  2. Đảm bảo request body theo đúng format JSON
  3. Kiểm tra các trường bắt buộc như `model`, `messages`
  4. Xác định xem có tham số không được hỗ trợ không

#### Lỗi 429 Too Many Requests
- **Nguyên nhân**: Vượt quá giới hạn tốc độ (rate limit) hoặc quota hàng tháng
- **Giải pháp**:
  1. Kiểm tra mức sử dụng hiện tại trong dashboard provider
  2. Thực hiện chiến lược backoff và retry
  3. Cân nhắc nâng cấp gói dịch vụ
  4. Thêm logique giới hạn tốc độ côté client
  5. Sử dụng model khác có hạn mức cao hơn

#### Lỗi Connection Timeout
- **Nguyên nhân**: Mạng bị chặn, firewall, hoặc provider đang gặp sự cố
- **Giải pháp**:
  1. Kiểm tra kết nối internet
  2. Thử truy cập trang web của provider từ trình duyệt
  3. Kiểm tra firewall và proxy cài đặt
  4. Thử từ mạng khác (ví dụ: dùng điện thoại làm hotspot)
  5. Liên hệ bộ phận IT nếu đang trong môi trường công ty

#### Lỗi 403 Forbidden
- **Nguyên nhân**: Key không có quyền truy cập tới model cụ thể, hoặc bị giới hạn vùng địa lý
- **Giải pháp**:
  1. Kiểm tra xem tài khoản có được phép truy cập model này không
  2. Xác minh địa chỉ IP của bạn có nằm trong vùng cho phép không
  3. Liên hệ bộ phận hỗ trợ của provider để xin quyền truy cập

### Quy trình debug cụ thể cho HHTech API

1. **Xác minh endpoint chính xác**
   - URL chuẩn: `https://hhtechapi.com/v1/chat/completions`
   - Đảm bảo không có dấu "/" thừa ở cuối

2. **Kiểm tra headers bắt buộc**
   ```
   Authorization: Bearer <your_api_key>
   Content-Type: application/json
   ```

3. **Validate request body**
   ```json
   {
     "model": "claude-opus-4-8",  // hoặc model khác bạn muốn dùng
     "messages": [
       {
         "role": "user",
         "content": "Câu hỏi của bạn ở đây"
       }
     ],
     "max_tokens": 1000,
     "temperature": 0.7
   }
   ```

4. **Xử lý response**
   - Thành công: HTTP 200 với JSON chứa `choices[0].message.content`
   - Lỗi: HTTP 4xx/5xx với JSON chứa thông tin lỗi chi tiết

### Mẹo và thủ thuật

1. **Luôn test với request đơn giản trước**
   - Bắt đầu với `max_tokens: 10` và tin nhắn ngắn
   - Tăng độ phức tạp dần sau khi kết nối ổn định

2. **Sử dụng công cụ debug**
   - Postman hoặc Insomnia để tạo và test requests
   - curl với tùy chọn `-v` để xem chi tiết request/response

3. **Lưu trữ log chi tiết**
   - Bật verbose logging trong Hermes nếu có thể
   - Lưu lại request và response đầy đủ để phân tích sau

4. **Tạo môi trường test riêng**
   - Sử dụng API key khác cho môi trường development
   - Giữ riêng quota và giới hạn cho production

5. **Kiểm tra thời gian phản hồi**
   - Nếu chậm hơn 10 giây, có thể là vấn đề mạng
   - Nếu nhanh nhưng lỗi, có thể là vấn đề xác thực

### Tài nguyên tham khảo

- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [Anthropic Claude API Reference](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [HHTech API Documentation](https://docs.hhtechapi.com) (nếu có)