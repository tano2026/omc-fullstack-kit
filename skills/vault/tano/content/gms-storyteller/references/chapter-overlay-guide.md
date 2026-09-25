# Chapter Overlay Guide — FFmpeg

## Timing calculation
Chapter positions = cumulative sum of voiceover segment durations + gaps.

```
Section 1 → GAP → Section 2 → GAP → Section 3 ...
         ↑       ↑        ↑
     chapter_1  chapter_2  chapter_3
```

Each chapter starts at the GAP beginning, duration = 6s.

Example (EP02):
- GAP1 at 94.9s → chapter_1: enable='between(t,94.9,100.9)'
- GAP2 at 308.7s → chapter_2: enable='between(t,308.7,314.7)'
- GAP3 at 416.9s → chapter_3: enable='between(t,416.9,422.9)'
- GAP4 at 467.3s → chapter_4: enable='between(t,467.3,473.3)'
- GAP5 at 673.6s → chapter_5: enable='between(t,673.6,679.6)'

## FFmpeg command
```bash
ffmpeg -y -i base.mp4 \
  -i ch1.png -i ch2.png -i ch3.png -i ch4.png -i ch5.png \
  -filter_complex "\
    [0:v][1:v]overlay=x=0:y=0:enable='between(t,94.9,100.9)'[v1];\
    [v1][2:v]overlay=x=0:y=0:enable='between(t,308.7,314.7)'[v2];\
    [v2][3:v]overlay=x=0:y=0:enable='between(t,416.9,422.9)'[v3];\
    [v3][4:v]overlay=x=0:y=0:enable='between(t,467.3,473.3)'[v4];\
    [v4][5:v]overlay=x=0:y=0:enable='between(t,673.6,679.6)'[out]" \
  -map '[out]' -map 0:a \
  -c:v libx264 -preset ultrafast -crf 25 \
  -c:a copy \
  -movflags +faststart \
  output.mp4
```

⚠️ CRITICAL: Last overlay's output MUST be `[out]`, not `[v5]` — otherwise FFmpeg error "Filter overlay has output unconnected".

## Generating chapter images
Use Pillow script `gen_chapters.py`:

```python
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGBA', (1920, 1080), (13, 13, 18, 255))
draw = ImageDraw.Draw(img)
# Playfair Display at 72pt for chapter title
# Subtitle at 36pt Inter
# Gold #FFD700 text, center-aligned
img.save('chapter_N.png')
```

## Chapter content formula
Format: "Phần {N} — {Title}" / "{Subtitle}"

For EP02 (Bí Mật Giới Tinh Hoa — 3 bẫy):
- Phần I — Bẫy Thời Gian / "Công việc nở ra cho đầy thời gian"
- Phần II — Bẫy Kỹ Năng / "Giỏi trong cái lồng"
- Phần III — Bẫy An Toàn / "Cột neo của nỗi sợ"
- Phần IV — Giải Pháp 1 / "Pareto 80/20"
- Phần V — Giải Pháp 2 / "Xoay chuyển thời thế"
