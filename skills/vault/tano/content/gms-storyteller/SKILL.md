---
name: gms-storyteller
description: GMSP Script Writer Agent — dùng DeepSeek R1 (reasoning model) viết script cinematic 6 section, đúng gmsp-writing-formula
---

# GMSP Storyteller Agent — Script Writer cho Giải Mã Số Phận

## Khi nào dùng
Viết script tập mới cho kênh **Giải Mã Số Phận** (YouTube 10-15 phút) — dùng reasoning model (DeepSeek R1 hoặc auto/best-reasoning) để tạo nội dung cinematic chất lượng cao.

## Model config
- **Chính**: DeepSeek R1 qua OmniRoute (`auto/best-reasoning`) — rẻ hơn Claude ~7500x ($0.14/M input vs $15/M)
  - Model thực tế trên OmniRoute: `big-pickle`
- **Fallback**: `deepseek-chat` → `gemini-2.5-flash`

## API Quirks (OmniRoute)
- **Streaming mặc định ON** — thêm `"stream": false` nếu muốn non-streaming
- **max_tokens tối thiểu**: 32768 (dưới 8192 → R1 reasoning hết token, ko output → "quality validation" error)
- **Timeout**: script 12-15 phút cần 180-600s
- **Cost**: reasoning tokens ~2-4x completion, vẫn rất rẻ (~$0.01/tập)
- **VQD token error [503]**: transient — retry 30s hoặc chuyển deepseek-chat tạm thời

## Edge TTS timing calibration

### Timing formula (đã hiệu chỉnh Jul 2026)
- **Công thức cũ**: 1100 chars/phút → **sai cho Edge TTS**
- **Thực tế (rate +16%)**: ~800 chars/phút
  - 14,131 chars → thực tế 17.5 phút (thay vì 12.9)
- **Công thức đúng**: `duration_min = chars / 800`
- **Rate map**: +8% trầm, +14% normal, +25% cao trào

### Segment generation rules
- **Segment an toàn**: 700-800 chars (~90% success)
- **Segment tối đa**: 1500 chars (~60-70%)
- **Retry**: timeout +16% → thử +12% với segment nhỏ hơn ½
- **Concat**: `ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp3` — concat demuxer

## Background + Thumbnail per episode (BẮT BUỘC)

User phản ứng nếu tập sau dùng background tập trước.
- Mỗi tập PHẢI có background riêng: run `python pipeline/gen_episode_assets.py` trước render
- Output: `assets/backgrounds/epXX_bg.png`, `assets/thumbnails/epXX_thumb.png`
- Scene tag overlay: `drawtext=text='TẬP XX · TITLE':fontcolor=#FFD700:fontsize=28:x=16:y=16:fontfile='C:/Users/Nguyen Ngoc Tan/playfair-display.ttf'`
- Thumbnail: FAL image gen → Pillow text overlay (Playfair Display, gold, dark gradient)
- Font download: https://fonts.google.com/specimen/Playfair+Display → save as `playfair-display.ttf`

### Filter graph — lưu ý CUỐI CÙNG
Khi chain nhiều overlay, output cuối PHẢI có tên `[out]`:
```ffmpeg
[v4][5:v]overlay=x=0:y=0:enable='between(t,673.6,679.6)'[out]" \
-map '[out]' -map 0:a \
```
Nếu đặt tên khác (vd `[v5]`) → FFmpeg báo lỗi output unconnected.

## Base video generation

### Khi HyperFrames timeout
1. **Gen background** = Pillow (pipeline/gen_episode_assets.py)
2. **Option A — HyperFrames** (có waveform+ branding): Copy HTML, sửa bg + data-duration
3. **Option B — Static** (khi HF fail):
   ```
   ffmpeg -loop 1 -i assets/backgrounds/epXX_bg.png -i tts/voiceover.mp3 \
     -c:v libx264 -preset ultrafast -crf 25 -shortest -pix_fmt yuv420p epXX_base.mp4
   ```

### Kiểm tra
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 epXX.mp4
# "Invalid NAL unit" → file corrupt, re-render
```

### Background per episode — BẮT BUỘC
User phản ứng nếu tập sau dùng background tập trước.
- Mỗi tập PHẢI có background riêng
- Gen trước: `python pipeline/gen_episode_assets.py`
- Naming: `assets/backgrounds/epXX_bg.png`, `assets/thumbnails/epXX_thumb.png`

## Resona concat — ghép ALL candidates
Khi user paste Resona web, mỗi phần có N candidate file.
→ GHÉP TẤT CẢ, ko chọn 1.
- Gap giữa các phần = **3s** (user chốt — 6s bị chê dài)
- KO gap giữa segment cùng phần
- Concat: `ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp3`

Chi tiết: xem `references/resona-concat-workflow.md`

## Pipeline lỗi thường gặp & fix

| Vấn đề | Triệu chứng | Fix |
|--------|------------|-----|
| R1 output thiếu CTA | Chỉ 1-2 CTA | Thêm tay: HOOK + mid-roll + end |
| R1 nhắc tên kênh trùng | 2 lần trong 1 đoạn | Chuyển 1 lần ra đoạn riêng |
| Encoding lỗi | "Hóa Kị" thay "Hóa Kỵ" | Check Unicode sau R1 |
| Tiếng Anh lạc | "coffee", "subscribe" | Thay: cà phê, đăng ký, tài sản |
| Voiceover quá dài | 17 phút thay 12-15 | Edit script bớt ~3000 chars HOẶC tăng rate |

## User preferences embedded in this skill

### Lesson 1: phải explicit về độ dài
- ❌ "Viết script 12-15 phút" → R1 ra ~8-9K ký tự
- ✅ Đưa exact char target cho mỗi section + "TỔNG: 13,000-16,500 ký tự"

### Lesson 2: thêm section bị thiếu
Section thường thiếu: BỐI CẢNH và GIẢI PHÁP.
Mở rộng bằng: thêm detail case study, thêm 1 giải pháp.

### Lesson 3: luôn review sau R1
Check: encoding, CTA, từ tiếng Anh, tên kênh trùng.

### Lesson 4: Brand mention density
- KO nhắc tên kênh 2 lần trong cùng 1 đoạn
- Phân bố: HOOK (1) + mid-roll (1) + end (1) = 3 lần

### Lesson 5: Background per episode — REQUIRED
User sẽ phàn nàn nếu ko có background riêng.
Luôn chạy `gen_episode_assets.py` trước khi sản xuất tập mới.

### Lesson 6: Resona concat -> ALL candidates
Ko chỉ chọn file best — ghép tất cả candidate theo thứ tự.
Gap 3s (ko 6s).

### Lesson 7: 3s gaps, not 6s
User chốt: 3s là chuẩn. 6s quá dài.
Gen: `ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 3 gap3s.mp3`

### Lesson 8: Background ep MUST be dark, not gold
❌ Background tự gen bị vàng khè → user phàn nàn "chả thấy gì"
✅ Dùng base_v3 từ EP01 (nền đen, waveform vàng, 4-corner branding) thay vì background tự vẽ
- Nếu cần background riêng: ảnh chụp studio tối (ko vẽ gradient vàng)
- Scene tag overlay: tạo ảnh PNG nền đen (#0D0D12) bán trong suốt, text vàng, overlay lên góc trái base_v3
  ```python
  # Gen scene tag
  img = Image.new('RGBA', (400, 100), (0, 0, 0, 0))
  draw.rectangle([(0, 0), (W, H)], fill=(13, 13, 18, 200))
  draw.text((10, 28), text, font=font, fill=(255, 215, 0, 230))
  ```
  FFmpeg overlay:
  ```
  ffmpeg -i base.mp4 -i epXX_tag.png -filter_complex "[0:v][1:v]overlay=x=30:y=30:enable='between(t,0,775)'[out]" -map '[out]' ...
  ```

### Lesson 9: Gen background — DARK, not gold gradient
Script `gen_episode_assets.py` tạo nền gradient vàng → sai. Fix:
- Nền: đen #0D0D12 solid (ko gradient vàng)
- Chỉ text vàng, accent vàng nhẹ ở bottom bar
- Gradient overlay: dùng filter overlay trên base_v3 chứ ko vẽ vô background

### Lesson 10: Viết section cụ thể cho R1
R1 hay viết section BỐI CẢNH & GIẢI PHÁP thiếu so với mục tiêu.
Fix: Trong prompt, đưa char target CỤ THỂ từng section + cấm section dưới target

## Cách dùng

### Step 1: Load input
```python
skill_view('gmsp-writing-formula')
# Read topic + references
```

### Step 2: Viết script (reasoning model)
Gửi prompt template tới `auto/best-reasoning`.

### Step 3: Kiểm tra độ dài
- Đếm ký tự mỗi section
- Nếu < 12,000 → expand

### Step 4: Review (model rẻ)
Dùng deepseek-chat hoặc gemini-2.5-flash.

### Step 5: Fix lỗi
1. Check encoding
2. Thêm CTA lần 1 vào HOOK
3. Kiểm tra tên kênh trùng
4. Sửa từ tiếng Anh
5. Thêm "Đăng ký kênh. Bật chuông." ở end

### Step 6: Lưu → episodes/epXX-<tên>/script.md

---

## Prompt Template — Reasoning Pass

### R1 Prompt Tips (xem references/r1-prompt-tips.md)
- ✅ Đưa char target CHÍNH XÁC mỗi section: "HOOK ~1000-1400 ký tự" 
- ✅ Tổng target ở đầu: "TỔNG 13000-16000 ký tự"
- ✅ max_tokens 32768 (ko dưới)
- ❌ Prompt ngắn <2K chars → R1 output ngắn 8K chars

```json
{
  "model": "auto/best-reasoning",
  "messages": [
    {
      "role": "system",
      "content": "Bạn là GMSP Storyteller — viết script YouTube cho kênh \"Giải Mã Số Phận\".\n\nPHONG CÁCH: Một người đàn ông từng trải, đang kể cho đàn em. Giọng trực diện, dồn dập, cuốn hút. KHÔNG giảng bài. Xưng hô: tôi - bạn.\n\nCẤU TRÚC 6 SECTION — TỔNG 13000-16000 ký tự = 12-15 phút:\n1. HOOK (60-90s) ~1000-1400 ký tự\n2. BỐI CẢNH (3-4 phút) ~3300-4400 ký tự — 2 case study\n3. TỬ VI GIẢI MÃ (2.5-3.5 phút) ~2800-3800 ký tự\n4. TÂM LÝ & ĐỊNH LUẬT (2.5-3.5 phút) ~2800-3800 ký tự\n5. GIẢI PHÁP (2.5-3.5 phút) ~2800-3800 ký tự\n6. CLIFFHANGER + END (45-60s) ~800-1000 ký tự\n\nQUY TẮC:\n- CÓ tên nhân vật — không generic\n- KHÔNG số liệu ảo\n- Tử Vi dịch ra đời thường\n- Case study xuyên suốt: \"Nhớ [tên] không?\"\n- Nhịp luân phiên dài/ngắn/hỏi/beat/điệp\n- 3 CTA + 3 lần \"Giải Mã Số Phận\"\n- Kết section = câu kéo",
      "role": "user",
      "content": "VIẾT SCRIPT EPXX - [TITLE]\n\n[CHI TIẾT CHỦ ĐỀ + CASE STUDY + KHUNG SECTION]\n\nOutput: script thuần, --- giữa các section, ko ghi chú.\nYÊU CẦU ĐỘ DÀI: Tối thiểu 13,000 ký tự = 12-15 phút."
    }
  ],
  "max_tokens": 32768,
  "temperature": 0.65,
  "stream": false
}
```

## Review Prompt (deepseek-chat)

```
Checklist:
1. Case study có tên + cảnh + thoại?
2. Case study xuyên suốt TỬ VI, TÂM LÝ, GIẢI PHÁP?
3. Có số liệu ảo?
4. Đủ 3 CTA + 3 lần tên kênh? KO trùng 1 đoạn.
5. Nhịp: có 2 câu liên tiếp cùng pattern?
6. Mỗi section kết = câu kéo?
7. Tử Vi dịch ra đời thường?
8. Script đủ 13,000+ ký tự?
9. Encoding lỗi? (Hóa Kỵ, Lộc Tồn...)
10. Từ tiếng Anh ko cần thiết?
```

## TTS status
⚠️ Resona API chết (api.resona.live NXDOMAIN).
Edge TTS `vi-VN-NamMinhNeural` — free, fails >5K chars.
Gen per segment (~700-800 chars), concat sau.

## Cost per tập
| Bước | Tokens | Cost |
|------|--------|------|
| Reasoning pass (R1) | ~5K in / ~8K out + reasoning | ~$0.002-0.01 |
| Review pass (deepseek-chat) | ~5K in / ~2K out | ~$0.0001 |
| Total | | ~$0.002-0.01 |
