# Podcast/Narrated Video Pattern — Waveform + 4-Corner Layout

A reusable pattern for HyperFrames compositions that drive a narrated podcast-style video with a single background, animated waveform bars, persistent corner chrome, and timed text overlays.

## When to use

- Narrated explainer / podcast / faceless video (~1–12 min)
- Single background image throughout (like The Hidden Self style)
- Camera: slow Ken Burns zoom on static background
- Waveform at bottom as audio visualisation
- 4-corner persistent chrome (scene tag, logo, brand, subscribe CTA)
- Text quotes fade in/out following voiceover

## Template structure

```
hyperframes/
├── index.html              # Composition (4-corner base + scene tags + intro/end card)
├── assets/
│   ├── bg_studio_v2.png    # Background image (1920×1080)
│   ├── logo_v2.jpeg        # Channel logo/avatar (circular crop)
│   └── ...                 # Other assets
├── ep01_text.ass           # ASS subtitle file for text overlays
└── bgm_loop.mp3            # Looped background music (optional)
```

## Waveform Bars (GSAP + Seeded PRNG)

The waveform is 120 bars generated in JS with a mulberry32 seeded PRNG for deterministic output. Each bar has a random base height, variance, animation cycle, and delay — they animate with `sine.inOut` ease, yoyo, finite repeat.

```js
const barCount = 120;
const container = document.getElementById('waveform-container');
const totalDuration = 625; // match composition duration
let seed = 42;
function rand() {
  seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}

for (let i = 0; i < barCount; i++) {
  const bar = document.createElement('div');
  bar.className = 'wave-bar';
  bar.style.height = '8px';
  container.appendChild(bar);
  const baseH = 15 + rand() * 80;
  const variance = 30 + rand() * 100;
  const cycle = 0.6 + rand() * 1.8;
  const delay = rand() * totalDuration;
  const repeats = Math.max(1, Math.floor(totalDuration / cycle) - 1);
  tl.to(bar, { height: baseH + variance, duration: cycle,
    ease: 'sine.inOut', repeat: repeats, yoyo: true }, delay);
}
```

CSS for the bars:
```css
.wave-bar {
  width: 4px; border-radius: 2px;
  background: linear-gradient(to top, rgba(255,215,0,0.2), rgba(255,215,0,0.7));
  transform-origin: bottom center;
}
```

## 4-Corner Layout

Each corner element gets its own `data-track-index` to avoid `overlapping_clips_same_track` errors:

| Position | Element | Track | Style |
|----------|---------|-------|-------|
| Top-left | Scene tag | 8 | Inter, 20px, gold, uppercase, letter-spaced |
| Top-right | Logo (avatar) | 4 | 100px circle, 2.5px gold border, glow |
| Bottom-left | Brand text | 6 | Inter, 19px, gold, uppercase |
| Bottom-right | Subscribe CTA | 5 | Inter, 14px, gold, line+text |

Full-width persistent elements:

| Element | Track | Details |
|---------|-------|---------|
| Background image | 0 | `full-bg`, loop=1, 625s |
| Gradient overlay | 1 | `linear-gradient(180deg, ...)` from transparent → dark at bottom |
| Bottom bar | 2 | 240px, `linear-gradient(180deg, transparent → 0.95 black)` |
| Waveform container | 3 | 160px, centered, gap=3px, padding 0 60px |

**Golden circle avatar logo:**
```css
.logo-container {
  position: absolute; top: 25px; right: 35px;
  width: 100px; height: 100px; border-radius: 50%;
  overflow: hidden; background: #0D0D12;
  border: 2.5px solid rgba(255,215,0,0.55);
  box-shadow: 0 0 25px rgba(255,215,0,0.18);
}
```

## Intro Card (0–5s)

Animated card at video start:
- Logo/title: Playfair Display 72pt gold, fade in
- Divider line: scaleX from 0
- Tagline: Inter 22pt white, fade in
- Entire card fades out at 4.5s

## End Card (last 10–15s)

Full-screen dark overlay with:
- Title: "CẢM ƠN BẠN ĐÃ XEM" (Playfair, gold)
- Subtitle: channel name
- CTA: "ĐĂNG KÝ · CHIA SẺ · BÌNH LUẬN" (bordered button style)

## Scene Tags (section labels)

The video is divided into narrated sections. Scene tags change at section boundaries on the same track (track 8):

```html
<div data-track-index="8" data-start="5"   data-duration="40">  TẬP 1 · CHỦ ĐỀ</div>
<div data-track-index="8" data-start="45"  data-duration="140"> CÂU CHUYỆN</div>
<div data-track-index="8" data-start="185" data-duration="140"> TỬ VI LÝ GIẢI</div>
<div data-track-index="8" data-start="325" data-duration="120"> THUẬT · ĐỊNH LUẬT</div>
<div data-track-index="8" data-start="445" data-duration="140"> GIẢI PHÁP</div>
<div data-track-index="8" data-start="585" data-duration="30">  CLIFFHANGER</div>
```

## ASS Subtitles for Text Overlays (Post-FFmpeg)

Instead of inlining dozens of text clips into the HyperFrames composition (which makes timeline management unwieldy), render the base video with HyperFrames, then overlay timed text quotes using FFmpeg + ASS subtitles.

**Step 1: Create ASS file** (`ep01_text.ass`)
```
[Script Info]
Title: GMSP Ep01 - Text Overlays
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MainQuote,Playfair Display,60,&H00FFD700,&H00FFD700,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,1,2,100,100,50,1
Style: SubQuote,Inter,32,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,1,2,100,100,50,1
Style: AccentQuote,Playfair Display,44,&H00FFD700,&H00FFD700,&H00000000,&H80000000,0,1,0,0,100,100,0,0,1,4,1,5,100,100,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:05.00,0:00:12.00,MainQuote,,0,0,100,,Key quote here
```

Key ASS style notes:
- Alignment=2 centers text horizontally
- PrimaryColour=`&H00FFD700` for gold, `&H00FFFFFF` for white
- OutlineColour=`&H00000000` black stroke, Outline=3–5 for readability on dark
- `\N` for line breaks in ASS text

**Step 2: FFmpeg final assembly**
```bash
ffmpeg -i ep01_base.mp4 -i voiceover_full.mp3 -i bgm_loop.mp3 \
  -filter_complex "\
    [1:a][2:a]amix=inputs=2:duration=first:weights=1 0.15[aout];\
    [0:v]ass=ep01_text.ass[vout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -c:a aac -shortest ep01_final.mp4
```

Voiceover = 100% volume. BGM = 15% volume.

## Check Errors & Fixes (Common Pitfalls)

| Error | Cause | Fix |
|-------|-------|-----|
| `root_missing_composition_id` | `data-composition-id` on wrong element | Put on the `#root` div, not `<html>` |
| `root_missing_dimensions` | `data-width`/`data-height` on wrong element | Same as above — put on `#root` |
| `overlapping_clips_same_track` | Two clips start at same time on same track | Put each persistent element on its own track index |
| `gsap_infinite_repeat` | GSAP `repeat:-1` | Use finite repeat: `repeat: Math.max(1, Math.floor(totalDuration / cycle) - 1)` |
| `gsap_exit_missing_hard_kill` | GSAP fade ends at clip boundary without set() | Add `tl.set('#element', { opacity: 0 }, clipEndTime);` |
| `invalid_parent_traversal_in_asset_path` | Asset path uses `../` | Copy assets into the project's `assets/` directory, reference with `assets/filename.png` |
| `font_family_without_font_face` | Using a font not loaded via Google Fonts CDN | HyperFrames bundles Montserrat & Inter; Playfair Display must be added |
| `missing_local_asset` | Referenced file doesn't exist | Copy asset file into `assets/` first |
| Contrast fail (WCAG) | Brand text too subtle | Increase opacity: `rgba(255,215,0,0.6)` → `0.7`+, or use white instead |

## Font strategy for Vietnamese

- **Titles/Quotes**: Playfair Display (serif, handles diacritics well, Dark Academia feel)
- **Body/Scene tags/Subscribe**: Inter (clean sans, good Vietnamese support)
- **Do not use**: Montserrat for Vietnamese body text (diacritics can clip)
- Load via CDN: `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>` handles GSAP; fonts are injected by HyperFrames compiler from Google Fonts cache

## BGM Looping (FFmpeg concat approach)

When BGM tracks are shorter than the video:

```bash
# Create file list
for i in 1 2 3 4; do echo "file 'bgm_dark_cinematic.mp3'" >> bgm_list.txt; done
# Concat with trim to exact duration
ffmpeg -f concat -safe 0 -i bgm_list.txt -c copy -t 630 "bgm_loop.mp3"
```

The `aloop` filter on Windows FFmpeg 8.1.1 has inconsistent behaviour with `size=0`. Use concat demuxer instead.

## Render pipeline

1. **Demo**: Render 30s draft (`--quality draft`) for style approval
2. **Base render**: Full 625s draft render (takes ~20–25 min for 18,750 frames at 30fps with 4 GPU workers)
3. **Assembly**: FFmpeg overlays ASS text + voiceover + BGM
4. **Verification**: ffprobe check for both video+audio streams, duration match
