# Dual-Model LLM Routing Implementation Guide

## Hướng dẫn triển khai hệ thống LLM hai mô hình với định tuyến thông minh

### Tổng quan

Hệ thống hai mô hình cho phép tối ưu hóa chi phí và hiệu suất bằng cách:
- Sử dụng mô hình nhanh, rẻ tiền (Sonnet) cho các câu trả lời bình thường
- Sử dụng mô hình mạnh mẽ, chất lượng cao (Opus) cho tác vụ phức tạp như viết mã, phân tích, viết văn
- Tự động định tuyến dựa trên phân tích nội dung tin nhắn
- Cơ chế dự phòng bậc thẳng để đảm bảo độ tin cốt cấu trúc

```
+─────┐       +-------------------+     +------------------+    +------------------+
│ Ứng dụng │─────▶│ Định tuyến mô hình  │────▶│ HETech API Tier 1│────▶│   Thành công      |
└────+─────┘       +-------------------+     +------------------+    +------------------+
        │              │                        │                     ▲
        │              │                        ▼                     │
        │              │               +------------------+            │
        │              │               │ HETech API Tier 2│            │
        │              │               +------------------+            │
        │              │                        │                     │
        │              │                        ▼                     │
        │              │               +------------------+            │
        │              │               │ HETech API Tier 3│            │
        │              │               +------------------+            │
        │              │                        │                     │
        │              │                        ▼                     │
        │              │               +------------------+            │
        │              │               │  OmniRoute API   │            │
        │              │               │               +------------------+            │        │              │               │                         ▼                     │
        │              │               +------------------+            │        │              │               │            Gemini API   │            │        │              │               +------------------+            │        │              │               │   Smart Mock     │◄─────────┘        │              │               +------------------+            │        └─────────────────┘                     +------------------+
```

### Logic định tuyến mô hình

#### Nguyên tắc 결정 định tuyến

Hệ thống sử dụng hàm `_should_use_opus(message: str) -> bool` để quyết định khi nào nên sử dụng mô hình Opus thay vì Sonnet.

**Tiêu chí sử dụng mô hình Opus (chất lượng cao):**

1. **Mẫu mã nguồn lập trình**
   - Khối mã: ```...```
   - Định nghĩa hàm/class: `def `, `function `, `class `
   - Nhập khẩu: `import `, `from `
   - Khai báo biến: `const `, `let `, `var `, `=>`
   - Cú pháp: `{}`, `[]`, `;`
   - Luồng điều khiển: `if `, `else `, `for `, `while `, `try `, `except `
   - Từ khóa đặc biệt: `return `, `yield `, `async `, `await `
   - Bình luận: `# `, `// `, `/*`, `*/`

2. **Các chỉ số về viết kỹ thuật**
   - API, endpoint, database, SQL, query, algorithm
   - Framework, library, package, module, dependency
   - Debug, test, unit test, integration, deploy
   - Version, release, patch, bug, fix, issue
   - Các từ tiếng Việt: `viết`, `viết bài`

3. **Phân tích phức tạp**
   - Phân tích, tối ưu, so sánh, đánh giá, kết luận
   - Giải thích chi tiết, hướng dẫn chi tiết, bài viết
   - Nghiên cứu, tổng hợp, tóm tắt, biểu đồ, bảng

4. **Các thuật ngữ kỹ thuật tiếng Việt**
   - Mã nguồn, lập trình, phát triển, kiểm tra lỗi
   - Cải thiện, nâng cấp, phiên bản, tài liệu kỹ thuật

5. **Heuristic dựa trên độ dài**
   - Tin nhắn dài (> 300 ký tự) thường cần xử lý phức tạp
   - Các mẫu câu hỏi thường xuyên (làm sao, như thế nào, tại sao, vì sao) có ngưỡng độ dài thấp hơn (> 20 ký tự)

**Mặc định sử dụng mô hình Sonnet (nhanh, rẻ tiền):**
- Chào hỏi, giao tiếp thường văn ngắn
- Câu hỏi thực tế đơn giản
- Phản hồi cảm xúc ngắn gọn
- Tin nhắn không chứa bất kỳ chỉ báo nào ở trên

#### Chi tiết thực hiện

```python
def _should_use_opus(self, message: str) -> bool:
    """
    Xác định xem tin nhắn có cần sử dụng cấp độ Opus (cho các tác vụ code/viết/phân tích phức tạp) không.
    
    Trả về True nếu nên sử dụng Opus, False nếu nên sử dụng Sonnet (trò chuyện thường).
    """
    msg_lower = message.lower().strip()
    
    # Các chỉ số rõ ràng cho cấp độ Opus (code, viết kỹ thuật, phân tích phức tạp)
    opus_indicators = [
        # Mẫu mã nguồn
        "```",  # Khối mã
        "def ", "function ", "class ", "import ", "from ",  # Định nghĩa hàm/class
        "const ", "let ", "var ", "=>",  # Khai báo biến
        "{", "}", "[", "]", ";",  # Cú pháp mã nguồn
        "if ", "else ", "for ", "while ", "try ", "except ",  # Luồng điều khiển
        "return ", "yield ", "async ", "await ",  # Từ khóa đặc biệt
        "# ", "// ", "/*", "*/",  # Bình luận
        
        # Các chỉ số về viết kỹ thuật
        "api", "endpoint", "database", "sql", "query", "algorithm",
        "framework", "library", "package", "module", "dependency",
        "debug", "test", "unit test", "integration", "deploy",
        "version", "release", "patch", "bug", "fix", "issue",
        "viết", "viết bài",  # Các từ liên quan đến viết bằng tiếng Việt
        
        # Phân tích và yêu cầu phức tạp
        "phân tích", "tối ưu", "so sánh", "đánh giá", "kết luận",
        "giải thích", "hướng dẫn", "bài viết",
        "nghiên cứu", "tổng hợp", "tóm tắt", "biểu đồ", "bảng",
        
        # Các thuật ngữ kỹ thuật tiếng Việt
        "mã nguồn", "lập trình", "phát triển", "kiểm tra lỗi",
        "cải thiện", "nâng cấp", "phiên bản", "tài liệu kỹ thuật",
    ]
    
    # Kiểm tra các chỉ số dựa trên chuỗi
    for indicator in opus_indicators:
        if isinstance(indicator, str) and indicator in msg_lower:
            return True
    
    # Kiểm tra các mẫu câu hỏi có thể получить lợi thế từ Opus
    # Cẩn thận để không kích hoạt quá mức với các câu hỏi đơn giản
    question_patterns = ["làm sao", "như thế nào", "tại sao", "vì sao"]
    if any(pattern in msg_lower for pattern in question_patterns):
        # Những câu hỏi này thường cần suy luận sâu hơn
        if len(message) > 20:  # Giảm ngưỡng từ 50 xuống 20 để bắt những câu hỏi ngắn nhưng có ý nghĩa
            return True
    
    # Heuristic dựa trên độ dài (tin nhắn rất dài thường cần xử lý phức tạp)
    if len(message) > 300:
        return True
    
    # Mặc định sử dụng Sonnet cho trò chuyện thường
    return False
```

#### Triển khai hệ thống mô hình phân cấp

```python
async def _call_hhtech_tiered(self, messages: list[dict[str, str]], use_opus: bool) -> dict[str, Any]:
    """
    Gọi API HHTech với lựa chọn mô hình phân cấp và dự phòng.
    
    Args:
        messages: Các tin nhắn chat để gửi
        use_opus: Nếu True, sử dụng cấp độ Opus; nếu không, sử dụng cấp độ Sonnet
        
    Returns:
        Phản hồi JSON đã được phân tích từ API
    """
    if use_opus:
        model_list = self._hhtech_opus_models
        tier_name = "OPUS"
        logger.info("Đang thử cấp độ OPUS của HHTech")
    else:
        model_list = self._hhtech_sonnet_models
        tier_name = "SONNET"
        logger.info("Đang thử cấp độ SONNET của HHTech")
    
    last_exception = None
    
    for i, model in enumerate(model_list):
        try:
            logger.info(f"Đang thử mô hình HHTech {tier_name} {i+1}/{len(model_list)}: {model}")
            
            headers = {"Authorization": f"Bearer {self._hhtech_key}"}
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 1024,
                "stream": False,
            }
            res = await self._hhtech_client.post("/chat/completions", json=payload, headers=headers)
            res.raise_for_status()
            raw_response = res.json()
            content = raw_response["choices"][0]["message"]["content"]
            result = _parse_json(content)
            
            logger.info(f"Thành công HHTech {tier_name} với mô hình {model}: type={result.get('type')}")
            return result
            
        except Exception as e:
            last_exception = e
            logger.warning(f"Mô hình HHTech {tier_name} {model} thất bại: {e}")
            # Tiếp tục thử mô hình tiếp theo trong cấp độ này
            continue
    
    # Nếu tất cả các mô hình trong cấp độ đều thất bại, ném ra ngoại lệ cuối cùng
    logger.error(f"Tất cả các mô hình HHTech {tier_name} đều thất bại. Lỗi cuối cùng: {last_exception}")
    raise last_exception
```

#### Cấu hình

Cập nhật `app/services/config.py` để bao gồm các cài đặt mô hình mới:

```python
# HHTech API - Hệ thống Hai Mô-đun
# Cấp độ Sonnet (dành cho trò chuyện thường - nhanh, tiết kiệm)
hhtech_sonnet_model: str = "claude-sonnet-4-5"
hhtech_sonnet_backup1: str = "claude-sonnet-4-6"
hhtech_sonnet_backup2: str = "claude-5.6-sol"

# Cấp độ Opus (dành cho code/viết/phân tích phức tạp - chất lượng cao)
hhtech_opus_model: str = "claude-opus-4-8"
hhtech_opus_backup1: str = "claude-opus-4-8-thinking"
hhtech_opus_backup2: str = "deepseek-v4-pro"
```

Cập nhật file `.env` để bao gồm các biến mới:

```bash
# Cấu hình API HHTech
HHTECH_API_KEY=sk-9c6...n

# Lựa chọn Mô-đun (Hệ thống Hai Mô-đun)
# Cấp độ Sonnet - dành cho trò chuyện thường (nhanh, tiết kiệm)
HHTECH_SONNET_MODEL=claude-sonnet-4-5
HHTECH_SONNET_BACKUP1=claude-sonnet-4-6
HHTECH_SONNET_BACKUP2=claude-5.6-sol

# Cấp độ Opus - dành cho code, viết, phân tích phức tạp (chất lượng cao)
HHTECH_OPUS_MODEL=claude-opus-4-8
HHTECH_OPUS_BACKUP1=claude-opus-4-8-thinking
HHTECH_OPUS_BACKUP2=deepseek-v4-pro
```

#### Lợi ích

1. **Tiết kiệm chi phí đáng kể**: Sonnet tốn khoảng 1/5 chi phí của Opus cho các truy vấn đơn giản
2. **Phản hồi nhanh hơn** cho trò chuyện thường (không cần chờ mô hình "chậm" xử lý)
3. **Vẫn giữ chất lượng cao** cho các tác vụ cần thiết như viết mã, phân tích logic, viết văn
4. **Hoàn toàn tự động** - người dùng không cần chỉ định mô hình nào
5. **An toàn tuyệt đối** - có hệ thống dự phòng bậc thẳng nếu mô hình nào gặp sự cố

#### Quy trình kiểm tra

1. **Thử Sonnet**: Gửi `"hôm nay thứ mấy?"` → Nên trả về nhanh bằng mô hình Sonnet rẻ tiền
2. **Thử Opus**: Gửi `"viết hàm Python tính số fibonacci với Memoization"` → Nên trả về chi tiết bằng mô hình Opus
3. **Xác định định tuyến**: Xem log để xác nhận việc định tuyến đúng
4. **Kiểm tra dự phòng**: Tạm thời vô hiệu hóa một lớp để xác nhận việc chuyển sang lớp khác hoạt động

### Tài nguyên tham khảo

- [HHTech API Documentation](https://docs.hhtechapi.com)
- [Anthropic Claude Model Comparison](https://www.anthropic.com/news/clause-3-models)
- [DeepSeek Model Documentation](https://docs.deepseek.com)
- [Google Gemini Models](https://ai.google.dev/gemini-api/docs/models)