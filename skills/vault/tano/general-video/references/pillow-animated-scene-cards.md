# Pillow-Animated Scene Cards (Non-HyperFrames Lane)

## When to use this

Use Python Pillow + FFmpeg (instead of HyperFrames HTML) when:

- **Data-driven animations** — fare class ladders, growing spreadsheets, bar charts, count-up stats
- **Staggered reveal** — elements appear one-by-one with timing (scene cards, feature lists)
- **Glow/border effects** — neon borders, shadow layering, glow highlights (easier in Pillow than CSS)
- **Grid backgrounds** — animated scanlines, subtle grid movements
- **Simple geometric motion** — slides, fades, scales — no 3D, no complex path animations
- **No narration sync needed** — visual-only segments that will be later overlaid with audio

Do NOT use for: complex 3D, text-heavy kinetic typography, interactive elements, or anything that needs per-frame asset generation from AI.

## Production Pipeline

```
Python (Pillow) → PNG frames (360-900) → FFmpeg → MP4
```

### Step 1: Frame generation script structure

```
project/
  scenes/
    scene06_fareclass.py     # Frame generator
    frames_scene06/          # Output: frame_00000.png ... frame_00360.png
  output/
    scene06_demo.mp4         # Final video
```

**Key classes and patterns:**

```python
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 30
DURATION = 12  # seconds
TOTAL_FRAMES = FPS * DURATION

# Color constants
BG = (13, 18, 30)       # Dark navy
TEAL = (0, 180, 200)
GOLD = (255, 215, 0)
WHITE = (230, 235, 245)
DIM = (100, 110, 130)
RED = (220, 50, 60)

# Frame loop
for frame in range(TOTAL_FRAMES):
    t = frame / FPS
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # ... render this frame ...
    img.save(f"frames_scene06/frame_{frame:05d}.png", "PNG")
```

### Step 2: Essential rendering patterns

**Background gradient:**
```python
def draw_bg(draw):
    for y in range(H):
        ratio = y / H
        r = int(BG[0] + (NAVY[0] - BG[0]) * ratio)
        g = int(BG[1] + (NAVY[1] - BG[1]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
```

**Animated grid lines (subtle):**
```python
offset = int(t * 20) % 80
for x in range(0, W, 80):
    alpha = max(0, 255 - abs((x + offset) % 160 - 80) * 4)
    draw.line([(x, 0), (x, H)], fill=(255, 255, 255, alpha // 8))
```

**Ease-out timing (staggered reveal):**
```python
stagger = min(1.0, max(0, (t - i * 0.3) * 2))
ease = 1 - (1 - stagger) ** 2  # ease out quad
offset_x = int((1 - ease) * 200)  # slide from left
```

**Glow border card:**
```python
# Shadow layer
for i in range(3):
    draw.rounded_rectangle([sx+4+i, sy+4+i, sx+sw-4+i, sy+sh-4+i], 
                           radius=6, fill=(0, 0, 0, 50))
# Card body
draw.rounded_rectangle([sx, sy, sx+sw, sy+sh], radius=6, fill=BG)
# Border
draw.rounded_rectangle([sx, sy, sx+sw, sy+sh], radius=6, 
                       outline=color, width=2)
```

### Step 3: FFmpeg assembly

```bash
ffmpeg -y -framerate 30 -i frames_scene06/frame_%05d.png \
  -c:v libx264 -pix_fmt yuv420p -preset medium -crf 22 \
  -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" scene06_demo.mp4
```

### Step 4: Post-render verification

```bash
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 output.mp4
# Expect: video
ffprobe -v error -show_entries format=duration -of csv=p=0 output.mp4
# Should match DURATION value ±0.1s
```

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `RGBA` vs `RGB` | Transparent/black background in MP4 | Use `Image.new("RGBA", ...)` and `pix_fmt yuv420p` |
| Font path missing | Script crash | Use `try/except` fallback chain: `arialbd.ttf` → `segoeui.ttf` → `default` |
| Frame count wrong | Video too fast/slow | Verify `TOTAL_FRAMES = FPS * DURATION` |
| FFmpeg invalid arg | Zoompan errors | Use `scale` + `crop` chain instead of `zoompan` on Windows |
| Large file size | >50MB for 12s | Increase `-crf` to 28-32, reduce resolution to 1280x720 |

## Hybrid Video Production Pattern

For explainer videos (like Airfare Decoded), split the production:

| Component | Tool | Duration |
|-----------|------|----------|
| Narrative scene cards | HyperFrames / scene cards | 60-70% of video |
| Animated data segments | Pillow + FFmpeg | 20-30% of video |
| Title/CTA cards | Static image | 10% of video |

Concatenate with FFmpeg `filter_complex concat`:
```bash
ffmpeg -i narrative.mp4 -i animated_scene.mp4 -i cta.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1" \
  output.mp4
```

## Performance Notes

- 1920×1080 at 30fps: ~4MB RAM for 1 frame, ~1.5GB for full frame buffer
- 360 frames @ 1920×1080: ~45 seconds render on modern CPU
- For 60fps or longer durations, use lower CRF and `-preset ultrafast` for preview, then re-render at `-preset slow` for final delivery
- On Windows: use `"$HOME/ffmpeg/ffmpeg.exe"` path, single quotes for filter expressions FAIL — use double quotes or escape
