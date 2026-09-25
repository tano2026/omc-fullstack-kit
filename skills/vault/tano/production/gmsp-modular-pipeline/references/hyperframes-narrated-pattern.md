# HyperFrames Narrated Video Pattern — GMSP

Pattern cho video podcast-style dài 10-15 phút, dùng HyperFrames thay vì FFmpeg showwaves.

## Khi nào dùng HyperFrames (thay vì FFmpeg)

| Tiêu chí | FFmpeg showwaves | HyperFrames GSAP |
|----------|-----------------|------------------|
| Waveform | Vạch raw, chìm nền | Bar animation mượt, custom |
| Text | drawtext cứng | CSS + GSAP timing animation |
| Font | Arial Windows | Google Fonts (Montserrat/Inter) |
| Kiểm soát | Khó chỉnh | Studio timeline |
| Render speed | ~5s/30s | ~1p/30s (4 workers GPU) |
| Check/Validate | Ko có | Lint + Runtime + Layout + Contrast |
| **Khi nào dùng** | Draft nhanh, iteration | Final quality, polish |

## Layout 4 góc (đã chốt 7/2026)

```
┌─────────────────────────────────────────────┐
│ 🔤 Scene Tag      🅻 Logo                   │  ← Top-left + Top-right
│  (18px, vàng)      (100px, GMSP)             │
│                                              │
│         ░░ TEXT QUOTE CHÍNH GIỮA ░░         │
│         Montserrat 900, #FFD700              │
│         + subtitle 36px, white               │
│                                              │
│                                              │
│ 📝 Brand text       🔔 Đăng ký +           │  ← Bottom-left + Bottom-right
│  (16px, vàng)        (subtle gold)            │
│ 🎵 WAVEFORM BARS (120 bar, GSAP)             │
└─────────────────────────────────────────────┘
```

### Chi tiết 4 góc

| Góc | Element | CSS | Content |
|-----|---------|-----|---------|
| **Top-left** | `.scene-tag` | `top:32px; left:40px; font-size:20px; color:rgba(255,215,0,0.7); letter-spacing:5px; font-weight:600; text-transform:uppercase` | `TẬP 1 · ĐỊNH LUẬT PARKINSON` |
| **Top-right** | `.logo-container` | `top:25px; right:35px; width:100px; height:100px; border-radius:50%; border:2.5px solid rgba(255,215,0,0.55); box-shadow:0 0 25px rgba(255,215,0,0.18); background:#0D0D12; overflow:hidden` | Avatar tròn (nón lá) trong khung vàng |
| **Bottom-left** | `.brand-text` | `bottom:65px; left:40px; font-size:19px; color:rgba(255,215,0,0.6); letter-spacing:4px; font-weight:700` | `GIẢI MÃ SỐ PHẬN · GMSP` |
| **Bottom-right** | `.subscribe-box` | `bottom:58px; right:40px; display:flex; gap:12px; align-items:center` | Line (24px) + "Đăng ký" 14px, font-weight:600 |

### Font cập nhật (7/2026 — chuẩn tiếng Việt)

| Vai trò | Font | Weight | Lý do |
|---------|------|--------|-------|
| **Titles / Quotes** | Playfair Display | 800 (Bold/Black) | Serif Dark Academia, xử lý dấu thanh Việt tốt |
| **Body / Scene tags / Brand** | Inter | 300-700 | Readable, hỗ trợ tiếng Việt ổn |
| **Subscribe / Small text** | Inter | 500-600 | Giữ consistency |

**Không dùng Montserrat cho title nữa** — Playfair Display đẹp hơn cho Dark Academia + dấu tiếng Việt.

## Track Layout

11 tracks cho full composition (30s demo):

| Track | Content | data-start | data-duration |
|-------|---------|-----------|---------------|
| 0 | Background image | 0 | total |
| 1 | Gradient overlay | 0 | total |
| 2 | Bottom bar (đen) | 0 | total |
| 3 | Waveform container | 0 | total |
| 4 | Logo (top-right) | 0 | total |
| 5 | Subscribe (bottom-right) | 0 | total |
| 6 | Brand text (bottom-left) | 0 | total |
| 7 | Intro card | 0 | 4 |
| 8 | Scene tags | staggered | non-overlapping |
| 9+ | Text quotes | staggered | non-overlapping |

**Rule:** clips trên cùng track KHÔNG được overlap. `data-track-index` TĂNG DẦN (0,1,2,...). Intro card + brand text phải khác track.

## HTML Template mới nhất

### Root + CSS

```html
<div id="root" data-composition-id="gmsp-podcast" data-start="0" data-duration="30" data-width="1920" data-height="1080">
```

CSS classes (viết trong `<head><style>`):

```css
/* Background - full brightness */
.full-bg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
/* Gradient overlay */
.overlay { position:absolute; inset:0; background:linear-gradient(180deg, rgba(10,14,26,0.2) 0%, rgba(10,14,26,0.15) 40%, rgba(10,14,26,0.15) 60%, rgba(10,14,26,0.5) 100%); }
/* Bottom bar waveform */
.bottom-bar { position:absolute; bottom:0; left:0; width:100%; height:200px; background:linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.85) 30%, rgba(0,0,0,0.9) 100%); }
/* Waveform bars */
.wave-bar { width:4px; border-radius:2px; background:linear-gradient(to top, rgba(255,215,0,0.3), rgba(255,215,0,0.8)); transform-origin:bottom center; }
/* 4 góc */
.scene-tag { position:absolute; top:35px; left:40px; font-family:'Inter',sans-serif; font-size:18px; color:rgba(255,215,0,0.7); letter-spacing:5px; text-transform:uppercase; font-weight:600; }
.logo { position:absolute; top:30px; right:40px; width:100px; opacity:0.8; }
.brand-text { position:absolute; bottom:60px; left:40px; font-family:'Inter',sans-serif; font-size:16px; color:rgba(255,215,0,0.6); letter-spacing:4px; text-transform:uppercase; font-weight:700; }
.subscribe-box { position:absolute; bottom:55px; right:40px; display:flex; align-items:center; gap:10px; }
.subscribe-text { font-family:'Inter',sans-serif; font-size:13px; color:rgba(255,215,0,0.7); letter-spacing:3px; text-transform:uppercase; font-weight:600; }
.subscribe-icon { width:28px; height:28px; border-radius:50%; border:2px solid rgba(255,215,0,0.5); display:flex; align-items:center; justify-content:center; font-size:14px; color:rgba(255,215,0,0.7); }
/* Text quotes */
.quote-main { color:#FFD700; font-size:68px; font-weight:900; letter-spacing:2px; line-height:1.2; }
.quote-sub { color:#ffffff; font-size:36px; font-weight:400; letter-spacing:1px; }
.quote-accent { color:#FFD700; font-size:44px; font-style:italic; }
.quote-number { color:#FFD700; font-size:80px; font-weight:900; }
/* Intro card */
.intro-card { position:absolute; width:100%; height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; background:radial-gradient(ellipse at center, rgba(10,14,26,0.6) 0%, rgba(0,0,0,0.9) 100%); }
.intro-title { font-family:'Montserrat',sans-serif; font-weight:900; font-size:72px; color:#FFD700; letter-spacing:4px; margin-bottom:16px; }
.intro-sub { font-family:'Inter',sans-serif; font-weight:300; font-size:24px; color:rgba(255,255,255,0.7); letter-spacing:6px; text-transform:uppercase; }
```

### Waveform Bars — Full Pattern

```html
<div id="waveform-container" class="clip" data-track-index="3" data-start="0" data-duration="TOTAL" style="position:absolute;bottom:20px;left:0;width:100%;height:160px;display:flex;align-items:center;justify-content:center;gap:3px;padding:0 60px;"></div>
```

```javascript
// Seeded PRNG (mulberry32)
let seed = 42;
function rand() {
  seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}

const barCount = 120;
const totalDuration = TOTAL; // match data-duration
const container = document.getElementById('waveform-container');
const tl = gsap.timeline({ paused: true });

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

  tl.to(bar, {
    height: baseH + variance,
    duration: cycle,
    ease: 'sine.inOut',
    repeat: repeats,
    yoyo: true,
  }, delay);
}
```

**Lưu ý:** Để `Math.floor` cho `repeats` — KHÔNG `Math.ceil` (sẽ vượt duration). `repeat: -1` bị lint lỗi.

## Intro Card Pattern

### HTML
```html
<div id="intro-card" class="clip" data-track-index="7" data-start="0" data-duration="4" style="position:absolute;inset:0;">
  <div class="intro-card">
    <img class="end-logo" src="assets/logo.png" alt="GMSP" />
    <div class="intro-title">GIẢI MÃ SỐ PHẬN</div>
    <div style="width:80px;height:2px;background:#FFD700;margin:20px 0 16px;opacity:0.5;"></div>
    <div class="intro-sub">Mỗi tuần một sự thật</div>
  </div>
</div>
```

### GSAP Animation
```javascript
tl.from('#intro-card .intro-title', { opacity:0, y:-20, duration:0.6, ease:'power2.out' }, 0.3);
tl.from('#intro-card .intro-line', { scaleX:0, duration:0.4, ease:'power2.out' }, 0.8);
tl.from('#intro-card .intro-sub', { opacity:0, y:10, duration:0.5, ease:'power2.out' }, 1.2);
tl.to('#intro-card', { opacity:0, duration:0.5, ease:'power2.in' }, 3.5);
```

## Thêm Audio (voiceover + BGM)

HyperFrames render video KHÔNG audio (chỉ video). Ghép sau:

```bash
# Ghép voiceover
ffmpeg -i episode_raw.mp4 -i voiceover_full.mp3 \
  -c:v copy -c:a aac -map 0:v -map 1:a \
  -shortest episode_with_audio.mp4

# Ghép voiceover + BGM (cần mix trước)
ffmpeg -i voiceover_full.mp3 -i bgm.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=3[audio]" \
  -c:v copy -map 0:v -map "[audio]" episode_final.mp4
```

## Full Workflow từ đầu → render

```bash
# 1. Init project
npx hyperframes init "./episodes/epXX-yyyy/hyperframes" --example blank

# 2. Copy assets (dùng absolute path, ko ../)
cp /d/GMSP/episodes/ep01/studio-bg.png assets/
cp /d/GMSP/assets/branding/logo.png assets/

# 3. Viết composition
# index.html với 11+ tracks (4 góc + waveform + intro + text)

# 4. Check (bắt buộc trước render)
npx hyperframes check

# 5. Fix lỗi (xem bảng bên dưới)

# 6. Render BASE video (không text quotes)
npx hyperframes render --quality draft --output ../epXX_base.mp4

# 7. Ghép ASS subtitle + audio
ffmpeg -i ../epXX_base.mp4 -i ../voiceover_full.mp3 -i bgm_loop.mp3 \
  -filter_complex "[1:a][2:a]amix=inputs=2:duration=first:weights=1 0.15[aout];[0:v]ass=../epXX_text.ass[vout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -c:a aac -shortest ../epXX_preview.mp4

# 8. Cho user review → nếu ổn → render high quality + publish
```

## ASS Subtitle Workflow

Cho video 10-15p, text quotes dùng ASS overlay (FFmpeg subtitles filter) thay vì HyperFrames text clips.

**Lý do:** HyperFrames render tất cả frames (18,750 frames cho 10:25 @ 30fps). Nếu text quotes nằm trong composition, mỗi text thay đổi = cần render lại toàn bộ. ASS overlay cho phép chỉ cần render lại BASE (hiếm khi thay đổi) + sửa file .ass (text timing).

**ASS style mẫu:** Xem content-strategy.md section 5 hoặc GMSP episodes/*/ep01_text.ass

**FFmpeg lệnh:**
```bash
ffmpeg -i base.mp4 -i audio.mp3 \
  -filter_complex "[0:v]ass=text.ass[vout]" \
  -map "[vout]" -map 1:a -c:v libx264 -c:a aac -shortest final.mp4
```

## Common Errors & Fixes (từ thực tế)

| Error | Cause | Fix |
|-------|-------|-----|
| `overlapping_clips_same_track` | 2 clips cùng track-index, overlap thời gian | Mỗi persistent element 1 track riêng (0-6). Non-overlapping elements (scene tags, quotes) dùng cùng track. |
| `root_missing_composition_id` / `root_missing_dimensions` | data-composition-id, data-width, data-height sai element | Đặt trên `<div id="root">`, ko phải `<html>` |
| `non_deterministic_code` | Math.random() | Seeded PRNG (mulberry32), seed cố định |
| `gsap_infinite_repeat` | repeat: -1 | `Math.floor(duration/cycle) - 1` |
| `missing_local_asset` / `invalid_parent_traversal_in_asset_path` | Dùng ../ trong path | Copy vào assets/, đường dẫn root-relative |
| `font_family_without_font_face` | Font ko có @font-face | Dùng Montserrat hoặc Inter (HyperFrames bundle sẵn) |
| Ảnh quá tối | brightness() + gradient overlay | Chỉ dùng 1 trong 2, ko dùng cả 2 |
| Audio mất sau mux | -shortest + -map sai | Verify với ffprobe: check `codec_type=audio` |

## Checklist trước render

- [ ] `npx hyperframes check` — 0 errors, 0 warnings
- [ ] Asset paths: root-relative (`assets/bg.png`), ko `../`
- [ ] Mỗi clip trên track riêng nếu overlap thời gian
- [ ] Root có `data-composition-id`, `data-start`, `data-duration`, `data-width`, `data-height`
- [ ] Font: Montserrat/Inter (bundled)
- [ ] repeat: finite (`Math.floor(duration/cycle) - 1`)
- [ ] Math.random() → seeded PRNG (mulberry32)
- [ ] Intro card + brand text khác tracks
- [ ] Bottom bar có gradient đen → waveform nổi bật
- [ ] Gradient overlay 25% → text readable, ảnh ko bị tối quá

## So sánh FFmpeg showwaves vs HyperFrames bars

| Khía cạnh | FFmpeg | HyperFrames |
|-----------|--------|-------------|
| Render 30s | ~5s | ~1p (59s với 4 workers) |
| Waveform | showwaves mode=cline, màu đơn | 120 bar, animation mượt, gradient vàng |
| Text overlay | drawtext: timing cứng, font limited | GSAP animation, Google Fonts |
| Check | Ko có auto check | Lint + Runtime + Layout + Contrast + Motion |
| Iteration cycle | Sửa → chạy → xem | Sửa → check → render → xem |
| File size (30s, 1080p) | ~950KB (draft) | ~2.4 MB (draft) |
| **Kết luận** | Nhanh, cho draft | **Đẹp hơn, chuẩn hơn — cho final** |
