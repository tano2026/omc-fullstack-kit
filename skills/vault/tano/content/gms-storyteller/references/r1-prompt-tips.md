# DeepSeek R1 Prompt Tips — Lessons from EP01 → EP02

## Vấn đề: EP01 script quá ngắn (9,292 chars = 8.4 min)
User: "hơi ngắn và hơi sơ sài" → Mục tiêu 12-15 phút

## Fix: Explicit char target mỗi section + strict constraint
Prompt EP02 v2 đã thêm:
- Mỗi section có char target cụ thể: "HOOK (60-90s) ~1000-1400 ký tự"
- Tổng: "TỔNG 13000-16000 ký tự = 12-15 phút"
- Constraint mạnh: "YÊU CẦU ĐỘ DÀI: Tối thiểu 13,000 ký tự = 12-15 phút"

Kết quả: 13,313 chars (dùng file lớn hơn) → đạt.

## Critical: Prompt length matters
- **EP01 v1** (prompt ngắn ~2K chars) → R1 output 9,292 chars
- **EP02 v2** (prompt dài ~3.5K chars + char targets) → R1 output 13,313 chars
- R1 responds to prompt COMPLEXITY, not just constraints. Prompt càng chi tiết, output càng dài.

## Rules for R1 prompts
1. **Put char targets IN the system prompt** not in the user message — R1 treats system as fixed rules
2. **Tổng target at top** — "TỔNG 13000-16000 ký tự = 12-15 phút" right after structure
3. **Individual section targets** — mỗi section ghi rõ ~1000-1400 ký tự
4. **Explicit instruction**: "YÊU CẦU ĐỘ DÀI: Tối thiểu 13,000 ký tự" ở cuối user message
5. **Temperature 0.65** — sufficient creativity without going off-track
6. **max_tokens 32768** — R1 needs 8K+ for reasoning, 24K+ for output
7. **stream: false** — OmniRoute stream mặc định, nhưng non-stream dễ xử lý

## Edge TTS timing recalibration
- Công thức cũ: 1100 chars/phút → sai (chỉ đúng cho Resona/giọng nhanh)
- Thực tế Edge TTS rate +16%: 800 chars/phút
  - 14,131 chars → 17.5 phút (130% dự kiến)
- Công thức đúng: `duration_min = chars / 800`
- Nếu muốn 12-15 phút → script 9,600-12,000 chars

## Segment size effect on Edge TTS reliability
| Segment size | Success rate | Note |
|-------------|-------------|------|
| 700-800 chars | ~95% | Most reliable |
| 1500 chars | ~60-70% | Timeout often |
| >2000 chars | ~30% | Almost always timeout |

Strategy: gen segments 700-800 chars, rate +14% (not +16%), timeout 45s.
