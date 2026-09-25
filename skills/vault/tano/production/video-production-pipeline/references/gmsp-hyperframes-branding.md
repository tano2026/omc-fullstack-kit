# GMSP HyperFrames Base — 4-Corner Branding & Iterative Delivery

## 4-Corner Branding Layout (đã chốt — lớn)

Layout cho podcast-style base video (HyperFrames index.html, 1920x1080):

| Vị trí | Kích thước | Nội dung | Font | Màu |
|--------|-----------|----------|------|-----|
| **Top-right** | 170x170px | Logo avatar tròn + border 3px vàng | — | gold 0.5 opacity + glow 35px |
| **Top-left** | 28px | Scene tag (ex: "TẬP 1 · 30-40 TUỔI") | Inter bold, letter-spacing 6px | gold 0.75 |
| **Bottom-left** | 24px | "GIẢI MÃ SỐ PHẬN · GMSP" | Inter bold 700, letter-spacing 5px | gold 0.6 |
| **Bottom-right** | 18px | "Đăng ký" + line separator | Inter 600, letter-spacing 4px | gold 0.65 |

## Intro Card (5s đầu)

Radial gradient overlay + animation sequence:
1. **Logo circle** (140px) scale-in from 0.5 → 1.0 (back.out easing, 0.2s → 0.5s)
2. **Title** "GIẢI MÃ SỐ PHẬN" slide-up + fade (Playfair Display 82px, gold, 0.6s)
3. **Gold line** scaleX 0→1 (0.4s)
4. **Subtitle** "Mỗi tuần một sự thật" fade up (Inter 24px, white 0.6, 0.5s)
5. Fade out at 4.5s, hidden at 5.0s

## Waveform Bars (seeded PRNG)

- 120 bars, 5px width, 4px gap
- Bar heights animated with GSAP sine.inOut
- gold gradient bottom→top (rgba(255,215,0,0.15) → rgba(255,215,0,0.65))
- Bottom-bar gradient: transparent→black 0.8 at 30%→black 0.95
- Duration: 800s (exceeds max voiceover for CapCut trimming)

## HyperFrames Composition

```html
<div id="root" data-composition-id="gmsp-podcast"
     data-start="0" data-duration="800"
     data-width="1920" data-height="1080">
```

Tracks: bg → overlay → bottom-bar → waveform → logo → subscribe → brand-text → scene-tags → intro-card → end-card

Each persistent element gets its own track (`data-track-index` separate). Intro/end cards are special effects tracks with own timing.

## Iterative Delivery to Telegram

When user wants to "xem thử" a video:

### Strategy: fail fast, compress harder

1. **First try:** CRF 28 → ~50-80MB → send via Tele. If timeout:
2. **Second try:** CRF 30 + aac 64k → ~23MB → send via Tele. If timeout:
3. **Third try:** 1280x720 scale + CRF 38 + maxrate 300k → ~9MB → send. This ALWAYS works.
4. **Path quirk fix:** If Tele says "media not found" with spaces in path, copy to `/tmp/` or `D:/` (no spaces).

### Key: deliver FAST, get feedback FAST
- Don't explain why first try failed — just tell "nén xuống còn X MB" and send
- User cares about seeing the video, not about compression ratios
- If upload works but user criticizes content (TTS mixed, BGM wrong, subtitle timing off) → fix + re-render + re-send. Accept that each iteration is 3-5 min.

## ASS vs SRT Subtitle Choice

- **ASS complex** — easy to break (truncated text, overlapping, special chars)
- **SRT simple** — reliable, timing calculated from actual voiceover segment durations + 3s gaps between section groups
- **On Windows FFmpeg** — DON'T use `fontsdir=` parameter (colon in `C:\Windows` breaks filter parsing). FFmpeg auto-discovers system fonts.
- **Timing source of truth:** ffprobe each voiceover segment file, sum durations with 3s section gaps, NOT script word-count estimates.

## Final Render — Clean Output (User-Approved)

After multiple iterations, the user CONFIRMED they want:

```bash
ffmpeg -y \
  -i "base_trimmed.mp4" \
  -i "voiceover.mp3" \
  -map "0:v" -map "1:a" \
  -c:v libx264 -preset ultrafast -crf 28 \
  -c:a aac -b:a 128k \
  -shortest -movflags +faststart \
  "ep01_final_clean.mp4"
```

**Explicitly excluded:**
- ❌ NO `-vf subtitles=` filter (user rejected subtitles entirely — "bỏ phụ đề đi")
- ❌ NO BGM (user rejected — "bỏ hết BGM đi", "sao có đoạn nhạc giữa bài")
- ❌ NO ASS/SRT overlay
- ✅ Only base background video + voiceover audio

## HyperFrames Render Timeout Fallback

HyperFrames render via Electron/Chrome can timeout at 600s terminal limit for long compositions.
**Do NOT wait for a fresh render — reuse existing base + trim:**

```bash
# Keep a previous long base render (>800s)
# Trim to match voiceover duration:
ffprobe -v error -show_entries format=duration -of csv=p=0 voiceover.mp3
ffmpeg -y -ss 0 -i "ep01_base_v3.mp4" -t 465 "ep01_base_final.mp4"
```

The waveform animation is seeded PRNG (seed=42) so it looks unique enough across crops.
