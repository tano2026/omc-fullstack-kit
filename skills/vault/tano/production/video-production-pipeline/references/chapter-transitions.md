# Chapter Transitions via FFmpeg Image Overlay

When building long-form video (7-12 min) with section breaks, use chapter transition overlays during the gap silences between sections.

## Concept

Each gap (6s between sections) shows a dark overlay + gold text chapter title + subtitle quote. The image fades in, holds, then fades out — creating a Netflix-style "Part I" chapter marker without re-rendering the entire composition.

## Step 1 — Generate chapter images (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Dark overlay (85% opaque)
overlay = Image.new('RGBA', (1920, 1080), (0, 0, 0, 200))
img = Image.alpha_composite(img, overlay)

# Fonts — use Windows fonts or bundled
font_large = ImageFont.truetype("C:/Windows/Fonts/playfairdisplay.ttf", 52)
font_small = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 24)

# "PHẦN I" (muted gold, top)
draw.text((x, 340), "PHẦN I", fill=(255, 215, 0, 120), font=font_small)

# Gold line
draw.rectangle((860, 390, 1060, 393), fill=(255, 215, 0, 180))

# Title (bold gold, center)
draw.text((x, 420), "Nỗi Sợ Thầm Kín", fill=(255, 215, 0, 230), font=font_large)

# Subtitle quote
draw.text((x, 500), '"Không ai chuẩn bị cho bạn"', fill=(200, 200, 200, 160), font=font_med)

img.save("chapter_1.png")
```

## Step 2 — Get gap timings (compute from actual files, don't estimate)

Voiceover concat with 6s gaps between 8 segments (7 gaps total):

```python
# Get each segment's actual duration
import subprocess
durations = {}
for sid in range(1, 9):
    path = f"resona_final/0{sid}_*.mp3"
    cmd = f'ffprobe -v error -show_entries format=duration -of csv=p=0 {path}'
    r = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    dur = float(r.stdout.strip())
    durations[sid] = dur

# Compute gap starts
current = 0
chapters = []
for i in range(8):
    chapters.append({'start': current, 'end': current + durations[i+1]})
    current += durations[i+1]
    if i < 7:  # gap after each section (except last)
        current += 6
    # Gap i+1 starts at chapters[i]['end']
```

Gap start times (example from EP01):
| Chapter | Gap after section | Gap starts at | Duration |
|---------|------------------|---------------|----------|
| 1 | Hook | 41.1s | 6s |
| 2 | Bối Cảnh | 122.5s | 6s |
| 3 | Tử Vi | 200.1s | 6s |
| 4 | Tâm Lý | 286.4s | 6s |
| 5 | Giải Pháp 1 | 339.7s | 6s |
| 6 | Giải Pháp 2 | 382.7s | 6s |
| 7 | Giải Pháp 3 | 427.3s | 6s |

⚠️ **CRITICAL: Gap start = `end_previous_segment`, NOT `end_previous_segment + 6`.** The 6s silence is appended AFTER the segment. Use ffprobe on each actual file — do not trust the script's estimated duration.

## Step 3 — Single FFmpeg command

```bash
ffmpeg -y \
  -i "base.mp4" \
  -i "voiceover.mp3" \
  -i "chapter_1.png" -i "chapter_2.png" ... -i "chapter_7.png" \
  -filter_complex "[0:v]trim=0:487[base]; \
    [2:v]format=rgba,fade=t=in:st=0:d=0.5:alpha=1,fade=t=out:st=5:d=1:alpha=1,setpts=PTS-STARTPTS+41.1/TB[ch1]; \
    [base][ch1]overlay=0:0[t1]; \
    [t1][ch2]overlay=0:0[t2]; \
    ... \
    [t6][ch7]overlay=0:0[vout]" \
  -map "[vout]" -map "1:a" \
  -c:v libx264 -preset ultrafast -crf 28 \
  -c:a aac -b:a 128k \
  -shortest -movflags +faststart \
  "final.mp4"
```

Key parameters:
- `fade=t=in:st=0:d=0.5:alpha=1` — fade from transparent to opaque over 0.5s
- `fade=t=out:st=5:d=1:alpha=1` — fade out over 1s starting at 5s (6s total gap)
- `setpts=PTS-STARTPTS+GAP_START/TB` — delay the overlay until the correct gap time
- All overlay images use `format=rgba` to preserve transparency

## Pitfalls

- **Font path on Windows:** Use `C:/Windows/Fonts/georgia.ttf` etc. with forward slashes. Pillow does NOT auto-discover system fonts like FFmpeg does.
- **Pillow vs HyperFrames:** This approach is a FFmpeg-only fallback when HyperFrames render times out. The ideal approach is to render chapter scenes natively in HyperFrames HTML (using `data-start` attributes on chapter-scene clip divs), but this requires a successful HyperFrames render which is unreliable on Windows for 465s+ compositions.
- **Timing drift:** If gap starts in the concat file don't exactly match, get actual durations from ffprobe on each segment file and recompute gap starts.
- **Trim duration:** `trim=0:487` needs to match total voiceover+gaps duration rounded up. If shorter, the last few seconds may be black; if much longer, the base background ends early.
