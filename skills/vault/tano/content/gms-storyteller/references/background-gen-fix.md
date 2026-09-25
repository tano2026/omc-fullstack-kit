# Background generation fix — don't make it yellow (Jul 2026)

## The bug
`gen_episode_assets.py` created backgrounds with a gold gradient overlay (lines `for i in range(H): draw.line(...)`). Result: full-screen gold haze. User: "video vàng khè, chả thấy gì".

## The fix
Background must be DARK (#0D0D12) with ONLY text in gold (#FFD700). No gold gradient.

Replace gradient loop with:
```python
# NO gold gradient overlay — just solid dark
# Text only in gold, no background color wash
```

## Instead of custom background
Use **ep01_base_v3.mp4** as the base for ALL episodes:
- It has dark bg + waveform bars (gold) + 4-corner branding + gradient overlay + intro card
- Just trim duration + overlay new scene tag + chapter transitions

Scene tag overlay approach:
```python
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 100
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rectangle([(0, 0), (W, H)], fill=(13, 13, 18, 200))  # semi-transparent dark
draw.text((10, 28), "TẬP 2 · BÍ MẬT GIỚI TINH HOA", font=font, fill=(255, 215, 0, 230))
```

FFmpeg:
```bash
ffmpeg -i epXX_base.mp4 -i epXX_tag.png \
  -filter_complex "[0:v][1:v]overlay=x=30:y=30:enable='between(t,0,775)'[out]" \
  -map '[out]' -map 0:a ...
```

## Thumbnails
Thumbnails CAN use gold text on dark bg — just no full-screen gold wash.
