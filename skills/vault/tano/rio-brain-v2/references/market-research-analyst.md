# Market Research Analyst Skill — Applied to RIO Bot

## Source
Tân provided a detailed `market-research-analyst.md` skill defining the methodology for market research agents. Key requirements:

1. **Search query precision** — query must be short, focused on the actual service/product, not generic keywords
2. **Content extraction** — fetch real content from URLs, don't rely on snippets alone
3. **Fact classification** — [FACT]/[ƯỚC TÍNH]/[CẦN XÁC MINH], never fabricate data
4. **Result filtering** — discard off-topic results (Amazon, eBay, generic platforms unless direct competitors)

## Integration into RIO Bot

The `rio-brain-v2` skill was updated to implement these patterns in V4:

### Applied Rules from market-research-analyst.md

| Rule | Implementation |
|------|---------------|
| Search ngắn gọn, trọng tâm | `_optimize_search_query()` — LLM rewrite |
| Fetch nội dung thực tế | `fetch_page_content()` — HTML parser |
| [FACT]/[ƯỚC TÍNH]/[CẦN XÁC MINH] | `_llm_analysis()` prompt instructs LLM to classify |
| Lọc kết quả lạc đề | LLM instructed to discard Amazon/eBay/Shopify etc. |

## LLM Prompt Patterns Used

### Search Query Optimizer Prompt
```
Viết LẠI câu hỏi sau thành 1-2 search query tiếng Việt ngắn gọn (tối đa 5 từ).

QUAN TRỌNG:
- Chỉ giữ từ khóa cốt lõi — bỏ "thị trường", "đối thủ", "giá cả", "ngách"
- Nếu có tên dịch vụ cụ thể, giữ nguyên
- Không thêm từ không có trong câu hỏi gốc
```

### LLM Analysis Prompt
```
Chỉ dùng thông tin CÓ TRONG nội dung nguồn — KHÔNG bịa số liệu.
Nếu nhiều nguồn mâu thuẫn — ghi rõ.
Phân loại: [FACT] có nguồn, [ƯỚC TÍNH] suy luận, [CẦN XÁC MINH] chưa chắc.
LOẠI BỎ kết quả về Amazon, eBay, Etsy, Alibaba, Shopify (trừ khi đối thủ).
Nếu kết quả không liên quan — báo thẳng.
```

## Key Insight

The two-point fix pattern for irrelevant search results:
1. **Fix the query** — make it precise, remove generic keywords that DDG uses to match commercial platforms
2. **Fix the analysis** — add a content-filtering layer that discards off-topic results before synthesis
