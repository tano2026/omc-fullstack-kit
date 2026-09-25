---
name: taste-frontend
description: 'Vibe Toolkit skill: taste-skill - Anti-Slop Frontend (Leonxlnx). Premium UI patterns. Banned: Inter/FontAwesome/shadow-md. 4 variants. Real-world pitfalls from An Binh Aviation build Jul 2026.'
---

# taste-skill - Anti-Slop Frontend

**Nguon:** github.com/Leonxlnx/taste-skill (43.3k⭐)
**Cap nhat:** thang 7/2026 (added practice pitfalls from An Binh Aviation build)

---

## SKILL 1 - TASTE-SKILL V2 (Default, dung cho 80% cases)

**Dung cho:** Landing page, portfolio, redesign
**Install name:** `design-taste-frontend`

Full taste-skill v2 content from Leonxlnx repo. Apply anti-slop rules, design read inference, bento grids, scroll animations. See original repo for raw text.

## Important: When NOT to use this skill's default aesthetic

### Taste skill defaults to: warm monochrome, minimalist, bento-grid, flat, muted pastels

### Flip signals - use dark/dramatic instead of warm/light:
- **Corporate aviation / airport services**: Needs trust, gravitas, professionalism. Use navy/dark blue backgrounds with gold/teal accents. Serif typography for headings. Full-screen hero. B2B trust signals (advisory board, years in business, regulatory credentials).
- **luxury / premium consumer**: Dark backgrounds, gold/champagne accents, editorial photography feel, less white space, larger typography.
- **Agency / creative studio**: Abandon bento-grid; use asymmetric layouts, experimental typography, vertical rhythm breaks.
- **Government / public sector**: Maximum accessibility, trust-first, conservative. No heavy motion.

### CORRECTION from practice (Jul 2026) — Light theme override
Some corporate/B2B clients, especially Vietnamese SMEs, prefer LIGHT themes despite seeming like "corporate" work.
- **Signal:** User says "sáng lên", "đổi màu khác đi", "cứ để tối thui", "sao cứ để tối thui" → flip to light immediately
- **Light theme for corporate:** White #FFFFFF hero/header, Navy #1B3A6B text, Teal #006885 accents, Gold #DBA011 for CTAs/money figures
- **Do NOT default to dark just because it's "corporate aviation".** Always ask or propose a light option first.
- **Corporate landing pages for Vietnamese B2B clients:** prefer white/clean no matter how "premium" dark sounds
- **Dark hero/menu is almost always wrong for Vietnamese SME landing pages.** Users interpret dark as "khó đọc", "tối thui", "lộn xộn". Default to light and let them ask for dark — not the reverse.

### Design Read Mandate
Always output a one-line Design Read before generating code:
```
Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <design system or aesthetic family>.
```

---

## PITFALLS FROM PRACTICE (An Binh Aviation - Jul 2026)

These are real corrections from a Vietnamese corporate aviation website build.
Embed them in every taste-skill-powered build, not just aviation:

### 1. Hero Background Must Be Legible First
- Geometric lines / abstract shapes at >10% opacity over dark backgrounds obscure text.
- Fix: Use dots pattern (radial-gradient rgba(255,255,255,0.03) 1px, transparent 1px at 40px grid) - creates texture without visual noise.
- Colored overlays stay at <5% opacity. Gradient accent on one side only (35% width) to keep reading area clean.
- Rule of thumb: if the hero text could be a background image alt tag, the background is too loud.

### 2. Logo Scaling - Always Bigger Than You Think
- Default AI logos at 28-36px in headers are too small for real brands.
- Minimum: 48px in header, 42px in footer.
- Add filter: drop-shadow(0 0 12px rgba(accent, 0.15)) to make it pop against dark backgrounds.
- For brand logos with gold/teal (airport, aviation, luxury): gold glow works.

### 3. Multilingual Content - Start With 3, Not 2
- Vietnamese clients in tourism/aviation often need VI + EN + CN (Chinese).
- Don't wait to be asked. Add EN + CN inline as secondary lines from the start:
  - Hero subtitle: second line EN, third line CN (smaller, muted, 50% opacity).
  - Section headers: EN below title, CN below that.
- CN font: use same sans-serif (Plus Jakarta Sans works for CJK).
- For hospitality/aviation/travel landing pages, default to VI + EN + CN.
- Users will tell you if they don't need CN; they will NOT tell you to add it.

### 3b. Language Switcher Implementation Pattern
When adding a VI/EN/CN language switcher (not just inline text but actual toggles):
- **DO use JS innerHTML swap** — store content in `data-vi`, `data-en`, `data-cn` attributes, swap on click
- **DO NOT use CSS `display: none` to hide languages** — the CSS selector approach (`.lang-vi [data-en] { display: none !important }`) will hide elements from layout and break the page. Use JS to overwrite `.innerHTML` from the data attribute instead.
- **Pattern:**
  ```html
  <h1 data-vi="Giải Pháp Hàng Không Toàn Diện" 
      data-en="Comprehensive Aviation Solutions" 
      data-cn="全面航空解决方案">Giải Pháp Hàng Không Toàn Diện</h1>
  ```
- **JS:**
  ```javascript
  function switchLang(lang) {
    document.querySelectorAll('[data-vi]').forEach(function(el) {
      var val = el.getAttribute('data-' + lang);
      if (val) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.setAttribute('placeholder', val);
        } else {
          el.innerHTML = val;
        }
      }
    });
    localStorage.setItem('site_lang', lang);
  }
  ```
- **CSS only needs:** `.lang-switcher span { cursor: pointer; }` and active state styling
- **Golden rule:** If the browser DevTools Elements panel shows the content is present but invisible, the problem is CSS display:none on the wrong selector. Fix by removing CSS visibility rules entirely — let JS handle it.
- **Save language to localStorage** so preference persists across page loads
- **Initialize on DOMContentLoaded** — read saved lang or default to 'vi'

### 4. Corporate Content Hierarchy - Service Pillars Over Single Product
- Don't let one service dominate the page just because it was the initial focus.
- Structure: 5-6 equal service pillars. If one is "featured", make it visually distinct (dark card, gold top bar) but not size-dominant in storytelling.
- **Ticketing card is always needed for aviation/travel companies** — airline representation and ticketing are distinct. Split them.
- When the user says "6 trụ cột" or "thiếu 1 trụ cột vé máy bay", the lesson is: aviation companies separate operations (GSA, permits) from commerce (ticketing, GDS). Do not merge them.

### 5. Dark Background Best Practices
- Navy/#0F203D backgrounds: text needs rgba(255,255,255,0.78) minimum for readability.
- Gold accent lines/CTAs need contrast ratio >4.5:1 against dark.
- Pure white #fff on navy is too harsh - use rgba(255,255,255,0.85-0.95).
- Form inputs on dark: bg rgba(255,255,255,0.06), border rgba(255,255,255,0.1), focus border=gold.

### 6. Always Use Real Logo - Never Default/AI-Generated
- Check if the project folder has a Logo/ directory.
- If PNG exists, use that instead of creating SVG placeholders.
- Real logo path pattern: ../../Logo/Horizontal/<filename>.png
- Verify file exists before writing references.

### 7. Advisory Board — Skip on Public Landing Pages
- Do NOT include "Ban Cố Vấn / Advisory Board" sections on public-facing websites.
- Vietnamese SMEs often consider this information internal/private.
- **Exception:** Only add when explicitly asked or for investor-facing sites.
- Replace with "Tại Sao Chọn Chúng Tôi / Why Choose Us" block — 3 concrete reasons (location, languages, certifications).
- Reason cards: keep factual (Nội Bài base, multilingual team, IATA/CAAV registration), no names/titles.

---

## Fonts: DO NOT use
Inter, Roboto, Arial, Open Sans, Helvetica

## Fonts: USE instead
Geist, Outfit, Cabinet Grotesk, Satoshi, Clash Display, PP Editorial New, Plus Jakarta Sans

## Icons: DO NOT use
Lucide thick-stroke, FontAwesome standard, Material Icons generic

## Icons: USE instead
Phosphor Light, Remix Line (ultra-thin precision)

## CSS: DO NOT use
- shadow-md / shadow-lg / shadow-xl defaults
- border: 1px solid gray generic
- rounded-full + blue primary button
- Gradient hero sections
- Heavy glassmorphism

## CSS: USE instead
- Ultra-diffuse shadows (rgba 0.03-0.05 opacity)
- border: 1px solid rgba(color, 0.06-0.1)
- Subtle backdrop-blur only for navbar
- scale(1.02) on hover + shadow transition
- cubic-bezier(0.22, 1, 0.36, 1) for spring motion

## Motion
- IntersectionObserver scroll reveal with fadeUp
- Stagger children (50ms delay increments)
- Counter animation (0 to target on scroll)
- Spring curves, NOT ease-in-out defaults

## Layout
- Asymmetric bento grid over 3-column symmetry
- Macro-whitespace, breathing room
- Column widths: icon/STT=8-10px, name=15%, content=39-46%
- Mobile-first responsive, hamburger nav at 768-900px

## Brand Colors for Aviation/Corporate Navy Theme
- Primary: teal #006885
- Accent: gold #DBA011
- Dark bg: navy #0F203D
- Light bg: parchment #F7F5F0
- Text: charcoal #1C1C1E
- Muted: #6B6B75

## Reference Files

- `references/language-switcher-vi-en-cn.html` — Working VI/EN/CN language switcher implementation (data-attr + JS innerHTML swap + localStorage). Copy-paste-ready. See Pitfall 3b for WHY this pattern over CSS display:none.
