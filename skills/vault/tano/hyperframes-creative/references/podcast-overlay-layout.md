# Podcast / Narrated Video Overlay Layout

Use for narrated YouTube videos, podcast-style visuals, talking-head voiceovers, and one-background-xuyên-suốt productions. This pattern uses a **single persistent background** image (studio, dark academia, etc.) with layered overlays that stay visible for the full duration, plus text quotes that come and go per scene.

## The 4-Corner Branding Layout

```
┌────────────────────────────────┐
│ 🔤 Scene Tag     🅻 Logo       │ ← top: scene info (L) + brand logo (R)
│                                │
│         TEXT QUOTE             │ ← center: main content
│         (fade in/out)         │
│                                │
│ 📝 Channel Name   🔔 Subscribe │ ← bottom: brand (L) + CTA (R)
│       🎵 Waveform Bars        │
└────────────────────────────────┘
```

### Track Allocation (flat composition)

Each persistent overlay needs its **own track** — never share `data-track-index` for elements whose time ranges overlap:

| Track | Element | Duration | Notes |
|-------|---------|----------|-------|
| 0 | Background image | full | `loop 1` img, `object-fit: cover` |
| 1 | Gradient overlay | full | Covers entire frame, 20-25% opacity |
| 2 | Bottom bar | full | ~200-240px, gradient black from transparent→85% |
| 3 | Waveform container | full | 120 bars, GSAP animated, seeded PRNG |
| 4 | Logo (top-right) | full | 90px circle with golden border |
| 5 | Subscribe CTA (bottom-right) | full | "Đăng ký" or "Subscribe" text + line |
| 6 | Brand text (bottom-left) | full | Channel name, small caps |
| 7+ | Quote clips | per-scene | Each quote on its own track to avoid overlap |

### Track Violation Gotcha

Persistent elements (logo, brand text, subscribe, bottom bar, gradient) all run `data-start="0" data-duration="<full>"`. They **cannot share a track** — HyperFrames checks for overlapping clips on the same track and errors. Give each its own `data-track-index`.

## Element Recipes

### Background Image (Track 0)

```html
<img id="bg" class="clip" data-track-index="0" data-start="0" data-duration="30"
  src="assets/studio-bg.png" alt="background"
  style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;" />
```

### Gradient Overlay (Track 1)

Darkens the background so text is readable. Two-stops gradient from transparent to black at bottom.

```html
<div id="overlay" class="clip" data-track-index="1" data-start="0" data-duration="30"
  style="position:absolute;inset:0;background:linear-gradient(180deg,
    rgba(10,14,26,0.0) 0%, rgba(10,14,26,0.15) 40%,
    rgba(10,14,26,0.15) 60%, rgba(10,14,26,0.5) 100%);">
</div>
```

For heavy text, add +10% opacity to the top stop.

### Bottom Bar (Track 2)

A gradient from transparent to dark, anchoring the waveform and preventing the background image from showing through.

```html
<div id="bottom-bar" class="clip" data-track-index="2" data-start="0" data-duration="30"
  style="position:absolute;bottom:0;left:0;width:100%;height:240px;
    background:linear-gradient(180deg,transparent 0%,rgba(0,0,0,0.85) 30%,rgba(0,0,0,0.95) 100%);">
</div>
```

### Waveform Bars (Track 3)

GSAP-animated bars using a seeded PRNG (mulberry32) for deterministic renders. 120 bars, each with random height, variance, cycle time, and delay. No `repeat:-1` — use a finite `repeat` count.

```html
<div id="waveform-container" class="clip" data-track-index="3" data-start="0" data-duration="30"
  style="position:absolute;bottom:30px;left:0;width:100%;height:160px;
    display:flex;align-items:center;justify-content:center;gap:3px;padding:0 60px;pointer-events:none;">
</div>
```

```css
.wave-bar {
  width: 4px; border-radius: 2px;
  background: linear-gradient(to top, rgba(255,215,0,0.2), rgba(255,215,0,0.7));
  transform-origin: bottom center;
}
```

```js
const barCount = 120;
const container = document.getElementById('waveform-container');
const totalDuration = 30;
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

### Logo (Track 4, Top-Right)

Circular crop with golden border, works best with character/profile images on dark backgrounds.

```html
<div id="logo-wrapper" class="clip" data-track-index="4" data-start="0" data-duration="30"
  style="position:absolute;top:25px;right:35px;width:90px;height:90px;
    border-radius:50%;overflow:hidden;border:2px solid rgba(255,215,0,0.5);
    box-shadow:0 0 20px rgba(255,215,0,0.15);background:#0D0D12;">
  <img src="assets/avatar.jpeg" alt="GMSP"
    style="width:100%;height:100%;object-fit:cover;opacity:0.9;" />
</div>
```

For a watermark logo (transparent PNG), skip the circle border:

```html
<img id="logo-wm" class="clip" data-track-index="4" data-start="0" data-duration="0"
  src="assets/logo.png" alt="GMSP"
  style="position:absolute;top:30px;right:40px;width:100px;opacity:0.8;" />
```

### Subscribe CTA (Track 5, Bottom-Right)

Subtle call-to-action. Line + text + optional icon. Use muted gold colors that don't fight with the main content.

```html
<div id="subscribe-box" class="clip" data-track-index="5" data-start="0" data-duration="30"
  style="position:absolute;bottom:58px;right:40px;display:flex;align-items:center;gap:12px;">
  <div style="width:24px;height:1px;background:rgba(255,215,0,0.4);"></div>
  <span style="font-family:'Inter',sans-serif;font-size:12px;color:rgba(255,215,0,0.6);
    letter-spacing:3px;text-transform:uppercase;font-weight:500;">Đăng ký</span>
</div>
```

### Brand Text (Track 6, Bottom-Left)

Channel name in small uppercase. 14-16px, muted gold.

```html
<div id="brand-text" class="clip" data-track-index="6" data-start="0" data-duration="30"
  style="position:absolute;bottom:65px;left:40px;font-family:'Inter',sans-serif;
    font-size:15px;color:rgba(255,215,0,0.55);letter-spacing:4px;text-transform:uppercase;
    font-weight:600;">
  GIẢI MÃ SỐ PHẬN · GMSP
</div>
```

## Vietnamese Font Recommendations

For Vietnamese-language narrated videos (which use đ, ă, â, ê, ô, ơ, ư, and their tone marks):

| Role | Recommended Font | Why |
|------|-----------------|-----|
| **Title / Headline** | **Playfair Display** | Serif handles Vietnamese diacritics well; Dark Academia aesthetic; available bundled in HyperFrames |
| **Body / Subtitles** | **Inter** | Clean sans, good readability at small sizes, excellent Vietnamese support, bundled |
| **Scene tags / Meta** | **Inter** | Same as body, maintains consistency |
| **Subscribe / CTA** | **Inter** | Caps text looks clean |

**Avoid** for Vietnamese: condensed fonts (diacritics clip), fonts with very tight ascenders/descenders (tone marks collide).

## Scene Tags (Top-Left)

Text label indicating episode number and current section. Changes per scene section — use the same track with different time ranges.

```html
<div id="tag-episode" class="clip" data-track-index="8" data-start="0" data-duration="12"
  style="position:absolute;top:32px;left:40px;font-family:'Inter',sans-serif;
    font-size:15px;color:rgba(255,215,0,0.65);letter-spacing:4px;text-transform:uppercase;
    font-weight:500;">
  TẬP 1 · ĐỊNH LUẬT PARKINSON
</div>
<div id="tag-story" class="clip" data-track-index="8" data-start="12" data-duration="16"
  style="position:absolute;top:32px;left:40px;font-family:'Inter',sans-serif;
    font-size:15px;color:rgba(255,215,0,0.65);letter-spacing:4px;text-transform:uppercase;
    font-weight:500;">
  CÂU CHUYỆN
</div>
```

## Text Quotes (Per-Scene Tracks)

Each quote is a centered text block that fades in, holds, then fades out. Give each a **separate track** to prevent overlap.

```html
<div id="quote-1" class="clip" data-track-index="9" data-start="0" data-duration="10"
  style="position:absolute;top:32%;width:100%;text-align:center;
    font-family:'Playfair Display',serif;font-size:60px;font-weight:800;color:#FFD700;
    text-shadow:2px 2px 0 rgba(0,0,0,0.8), 0 2px 12px rgba(0,0,0,0.6);">
  8:00 SÁNG
</div>
```

```js
tl.from('#quote-1', { opacity: 0, y: 20, duration: 0.8, ease: 'power2.out' }, 0.5);
tl.to('#quote-1', { opacity: 0, duration: 0.5, ease: 'power2.in' }, 9.5);
```

## Intro / Outro Cards

### Intro Card (brief, 3-4s)

Full-screen overlay with channel logo, title, and tagline. Fades out before the first text quote.

```html
<div id="intro-card" class="clip" data-track-index="7" data-start="0" data-duration="4"
  style="position:absolute;inset:0;
    background:radial-gradient(ellipse at center,rgba(10,14,26,0.6) 0%,rgba(0,0,0,0.9) 100%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;">
  <div style="font-family:'Playfair Display',serif;font-size:72px;font-weight:800;
    color:#FFD700;">GIẢI MÃ SỐ PHẬN</div>
  <div style="width:80px;height:2px;background:#FFD700;margin:24px 0;opacity:0.4;"></div>
  <div style="font-family:'Inter',sans-serif;font-size:22px;color:rgba(255,255,255,0.65);
    letter-spacing:5px;text-transform:uppercase;font-weight:300;">Mỗi tuần một sự thật</div>
</div>
```

## HyperFrames Checklist

Before rendering:

- [ ] `npx hyperframes check` passes (0 errors)
- [ ] No two overlapping clips on the same track
- [ ] All font families are bundled (Inter, Playfair Display) or properly imported via `@import`/`@font-face`
- [ ] GSAP `repeat:` is a finite integer, never `-1`
- [ ] No `Math.random()` — use a seeded PRNG for waveform bar heights
- [ ] Root div has `data-composition-id`, `data-width`, `data-height`, `data-start`
- [ ] All asset paths are under `assets/` (no `../` paths)
- [ ] Background images are in `assets/` directory, not referenced from outside the project
