# Brand Audit (2026-07-15)

Initial brand audit findings for GMSP channel identity.

## What was found

| Item | Status | Notes |
|------|--------|-------|
| Logo `.svg` | ✅ Complete | Thái Cực + Bát Quái + text, gold/amber on black |
| Logo `.png` | ✅ Exists | Rendered from SVG |
| 5 logo concepts | ✅ Saved | concept-1 (con dấu đỏ) → concept-5 (phượng hoàng) |
| BRAND_DESIGN.md | ✅ Complete | 6 sections: core → color → font → texture → voice → layout |
| Character source (character-source.jpeg) | ✅ Locked | Silhouette nón lá + áo the — DO NOT change |
| Avatar 1080x1080 | ✅ Exists | GMSP/assets/branding/avatar.png |
| YouTube banner | ✅ Exists | assets/branding/youtube-banner.png (old project) |
| Thumbnail sample | ✅ Exists | GMSP/config/thumbnail-sample.png |
| Intro video | ✅ Exists | GMSP/assets/branding/Intro new.mp4 (3.5s) |
| TikTok cover | ✅ Exists | assets/branding/tiktok-cover.png (old project) |
| Title + quote cards | ✅ Exists | GMSP/assets/branding/ |
| Background textures | ✅ Copied to GMSP | GMSP/assets/backgrounds/ (30+ files) |
| Fonts | ✅ Copied to GMSP | GMSP/assets/fonts/ |
| Watermark | ✅ Exists | GMSP/assets/branding/logo_giai_ma_so_phan_wm.png |
| brand.json (GMSP unified) | ✅ Created | GMSP/config/brand.json |
| brand-tu-vi.json | ✅ Created | GMSP/config/brand-tu-vi.json (gold accent) |
| brand-co-kim.json | ✅ Created | GMSP/config/brand-co-kim.json (brown accent) |
| brand.yaml (design system) | ✅ Created | GMSP/config/brand.yaml |
| brand.json (PTBT) | ✅ Exists | Old: brand/phat-trien-ban-than/brand.json (green + gold) |
| brand.json (Remotion) | ✅ Exists | brand/ptbt-remotion/src/brand.ts (TypeScript) |
| BGM library | ✅ 3 tracks | GMSP/assets/bgm/ — bgm_dark_cinematic.mp3 (3:06), bgm_intro.mp3 (0:48), bgm_mysterious.mp3 (4:23). All Pixabay free, no copyright |
| Outro video | ❌ Not rendered | Spec exists in brand.json but no actual file. Fallback: use bgm_intro.mp3 as placeholder. |
| Remotion intro | 🟡 Partial | ptbt-remotion/ exists but node_modules heavy |

## Brand architecture decision

**Final:** Use 1 brand (Giải Mã Số Phận) for all 3 domains, with per-domain accent colors:
- Tử Vi: black + gold (#FFD700) + red (#8B0000)
- Phát Triển Bản Thân: black + green (#1a6b3c) + gold (#d4a843)
- Bí Kíp Cổ Kim: black + brown (#8B6914) + gold (#BF953F)

**Brand files now at:** `GMSP/config/brand*.json` (unified + domain overrides)

## Color tokens (from BRAND_DESIGN.md)

| Token | Hex | Usage |
|-------|-----|-------|

## Color tokens (from BRAND_DESIGN.md)

| Token | Hex | Usage |
|-------|-----|-------|
| bg-primary | `#0D0D12` | Main background |
| bg-night | `#0A0E1A` | Secondary background |
| accent-gold | `#FFD700` | CTA, highlight, icons |
| accent-gold-deep | `#BF953F` | Borders, gradients, watermark |
| accent-red | `#8B0000` | Sparingly — seal, warnings, shocking stats |
| text-primary | `#F2EFE6` | Main text (off-white) |
| text-muted | `#9A9488` | Captions, metadata |

Gradient: `linear-gradient(135deg, #BF953F 0%, #FFD700 50%, #BF953F 100%)` — for headings.

## Font tokens

- `font-heading`: Playfair Display Black (700/900) — titles, channel name, hooks
- `font-body`: Montserrat Bold (600/700) — subtitles, captions
- `font-accent`: Playfair Display Italic — quotes, emotional closing
- Rule: NO thin fonts (300/400). Everything bold (600+) — fits "gai góc, dứt khoát" persona.

## Character lock

- Silhouette, completely faceless
- Nón lá + áo the cổ cao + khuy đỏ #8B0000
- Gold rim lighting (#FFD700 → #BF953F)
- Thin smoke/mist in background
- DO NOT use: tarot, crystal ball, fedora, cape, Western fantasy elements
- Source file: assets/branding/character-source.jpeg — crop everything from this
- Prompt for new poses: see BRAND_DESIGN.md section 4
