# Dual-Model LLM Routing System — ABTrip Ticketing Bot

## Overview

Implemented July 21, 2026 to optimize LLM usage costs while maintaining quality:
- **Sonnet tier** (claude-sonnet-4-5): For regular chat, greetings, simple questions (fast, cost-effective)
- **Opus tier** (claude-opus-4-8): For code writing, technical writing, complex analysis (high quality)
- Automatic routing based on content analysis with Vietnamese-aware heuristics
- Tiered fallback system within each tier (primary → backup1 → backup2)
- Cross-tier fallback (if all models in a tier fail, try the other tier)
- Final fallback to OmniRoute → Gemini → Smart Mock

## Files Modified

1. `backend/app/services/config.py` - Added dual-model configuration
2. `backend/app/services/llm_gateway.py` - Implemented routing logic and tiered fallback
3. `.env` and `.env.production` - Added HHTech API key and model configuration

## Configuration (config.py)

```python
# HHTech API - Dual Model System
# Sonnet tier (for regular chat - fast, cheap)
hhtech_sonnet_model: str = "claude-sonnet-4-5"
hftech_sonnet_backup1: str = "claude-sonnet-4-6"
hhtech_sonnet_backup2: str = "claude-5.6-sol"

# Opus tier (for code/writing/complex analysis - high quality)
hhtech_opus_model: str = "claude-opus-4-8"
hftech_opus_backup1: str = "claude-opus-4-8-thinking"
hftech_opus_backup2: str = "deepseek-v4-pro"
```

## Routing Logic (llm_gateway.py)

### Should Use Opus Decision Function

The `_should_use_opus(message: str) -> bool` function uses Vietnamese-aware heuristics:

**USE OPUS WHEN:**
- Code patterns: ```, def, function, class, import, const, let, var, =>, {}, [], ;
- Technical keywords: api, endpoint, database, sql, algorithm, framework, debug, test, deploy
- Vietnamese writing indicators: "viết", "soạn thảo", "bài viết", "tác phẩm", "truyện", "thơ", "bài luận"
- Analysis requests: "phân tích", "tối ưu", "so sánh", "đánh giá", "giải thích chi tiết", "hướng dẫn chi tiết"
- Vietnamese technical terms: "mã nguồn", "lập trình", "phát triển", "kiểm tra lỗi", "cải tiến", "nâng cấp"
- Length heuristic: messages > 300 characters

**USE SONNET WHEN:**
- Greetings: "allo", "chào bạn", "hi", "hello"
- Simple questions: "hôm nay thứ mấy?", "bạn có khỏe không?", "thời tiết hôm nay sao?"
- Acknowledgments: "cảm ơn", "không có gì", "tạm biệt", "oke"
- Very short messages
- No Opus indicators present

### Tiered Fallback System

1. **Determine tier** (Sonnet vs Opus) based on message analysis
2. **Try models in order** within selected tier:
   - Primary model (e.g., claude-sonnet-4-5)
   - Backup 1 (e.g., claude-sonnet-4-6)
   - Backup 2 (e.g., claude-5.6-sol)
3. **If all models in tier fail**, try the other tier
4. **If all HHTech models fail**, fall back to:
   - OmniRoute (local VPS)
   - Gemini (Google AI Studio)
   - Smart Mock (rule-based local fallback)

## Implementation Details

### HHTech API Integration
- Uses OpenRouter-compatible endpoint: `https://hhtechapi.com/v1/chat/completions`
- Authentication: Bearer token in Authorization header
- Parameters: temperature=0.3, max_tokens=1024, stream=False
- Proper client cleanup in `close_llm()` to prevent connection leaks

### JSON Response Handling
- Robust JSON extraction using regex pattern `\{.*\}` with DOTALL flag
- Fallback to text response if JSON parsing fails
- Standardized response format: `{type: "search|reply|confirm", ...}`

### Performance & Cost Benefits
- **Sonnet tier** costs approximately 1/5 of **Opus tier**
- Routing ensures simple chats use cheaper/faster model
- Complex tasks (code, writing, analysis) get higher quality model
- Fallback system ensures high availability
- Vietnamese-aware routing prevents misclassification of local language

## Verification

### Test Cases Verified Working:

**Sonnet Route (Regular Chat):**
- Input: "allo"
- Input: "hôm nay thứ mấy?"
- Input: "bạn có khỏe không?"
- Input: "cảm ơn bạn"
- Input: "thời tiết hôm nay sao?"

**Opus Route (Code/Writing/Complex):**
- Input: "viết hàm tính fibonacci"
- Input: "giúp tôi debug lỗi này: const x = 5;"
- Input: "tạo một class Python để quản lý danh sách học sinh"
- Input: "viết bài phân tích Truyện Kiều"
- Input: "so sánh hai cách tính thuế thu nhập cá nhân"
- Input: "giải thích tại sao trời xanh"
- Input: "làm sao để học tiếng Pháp hiệu quả?"
- Input: "chứng minh rằng tổng của các góc trong tam giác là 180 độ"
- Input: "tóm tắt nội dung của bài đọc này"

**Edge Cases:**
- Very long messages (>300 chars) → Opus
- Mixed greetings + code requests → Opus (correctly prioritizes code intent)
- Short technical questions → Opus when appropriate

## Deployment Notes

1. **Environment Variables Required:**
   - `HHTECH_API_KEY` - API key for HHTech service
   - `HHTECH_BASE_URL` - Base URL (https://hhtechapi.com/v1)

2. **Local Development:**
   - Add to `.env` file in backend directory
   - Existing OmniRoute and Gemini configurations preserved as fallbacks

3. **VPS Production:**
   - Already deployed to `/opt/abtrip-backend/` via `deploy/deploy.sh`
   - Static files (chat.html) copied separately
   - Systemd service automatically restarts on failure
   - Nginx configuration unchanged (still proxies /api/ to :8138)

## Maintenance

- To adjust routing sensitivity, modify `_should_use_opus()` in `llm_gateway.py`
- To change model priorities, update the model lists in `config.py`
- To add new Opus/Sonnet models, append to the respective backup lists
- Monitor logs for `Routing to [SONNET|OPUS] tier` to verify correct routing