# Brand JSON Format — Multi-Domain YouTube Channel

## File Structure

```
config/
├── brand.json              ← Brand chính (umbrella)
├── brand-{domain}.json     ← Mỗi domain có file accent riêng
```

## brand.json (Umbrella)

```json
{
  "vertical": "Tên Kênh",
  "slug": "ten-kenh",
  "description": "Mô tả ngắn",
  "tagline": "Tagline ngắn",

  "channel": {
    "youtube": "@handle",
    "tiktok": "@handle"
  },

  "colors": {
    "primary": "#0D0D12",
    "bg_night": "#0A0E1A",
    "accent_gold": "#FFD700",
    "accent_gold_deep": "#BF953F",
    "accent_red": "#8B0000",
    "text_primary": "#F2EFE6",
    "text_muted": "#9A9488"
  },

  "logo": {
    "primary": "logo.svg",
    "watermark": "watermarks/logo_wm.png",
    "avatar": "branding/avatar.png",
    "width": 400,
    "height": 400
  },

  "intro": {
    "duration_seconds": 3.5,
    "file": "branding/Intro.mp4",
    "fps": 30,
    "width": 1920,
    "height": 1080
  },

  "outro": {
    "duration_seconds": 5,
    "fps": 30,
    "width": 1920,
    "height": 1080,
    "cta_text": "Đăng ký để [tagline]",
    "social": "@handle"
  },

  "thumbnail": {
    "width": 1280,
    "height": 720,
    "layout": "character-right + text-left",
    "character": {
      "side": "right",
      "width_percent": 35
    },
    "overlay": {
      "color": "#0D0D12",
      "opacity": 0.75,
      "height_percent": 40
    },
    "title_style": {
      "font": "Playfair Display",
      "font_size": 72,
      "font_weight": 900,
      "color": "#FFFFFF",
      "highlight_color": "#FFD700"
    },
    "eyebrow": {
      "color": "#8B0000",
      "font_size": 20
    },
    "badge": {
      "position": "top-right",
      "text": "Kênh Tên",
      "bg_color": "#0A0E1A"
    }
  },

  "subtitle_style": {
    "font": "Arial",
    "font_size": 54,
    "font_weight": 700,
    "color": "#FFFFFF",
    "stroke_color": "#000000",
    "stroke_width": 3,
    "position": "bottom-center",
    "border_style": 1
  },

  "character": {
    "source": "branding/character-source.jpeg",
    "lock": true,
    "description": "Mô tả visual để dùng cho AI image gen khi cần",
    "style": "Mô tả phong cách"
  },

  "font": {
    "heading": "Playfair Display",
    "body": "Montserrat",
    "subtitle": "Arial"
  }
}
```

## brand-{domain}.json (Domain Accent Override)

```json
{
  "vertical": "Tên Domain",
  "slug": "domain-slug",
  "tagline": "Tagline domain",
  "parent_brand": "umbrella-slug",
  "colors": {
    "accent": "#FFD700",
    "accent_deep": "#BF953F",
    "badge_bg": "#BF953F"
  },
  "thumbnail": {
    "badge_text": "TAG DOMAIN",
    "accent_color": "#FFD700"
  }
}
```

## ASS Subtitle Style Mapping

| Brand JSON field | ASS field | Notes |
|-----------------|-----------|-------|
| `subtitle_style.font` | Fontname | Arial recommended |
| `subtitle_style.font_size` | Fontsize | 54 for 1920x1080 |
| `subtitle_style.font_weight` | Bold | `-1` when 700+ |
| `subtitle_style.color` | PrimaryColour | `#RRGGBB` → `&H00BBGGRR&` |
| `subtitle_style.stroke_color` | OutlineColour | |
| `subtitle_style.stroke_width` | Outline | BorderStyle=1 |
| `subtitle_style.position` | Alignment | 2=bottom-center |

Color conversion: `#1a6b3c` → hex `1a6b3c` → reverse to `3c6b1a` → ASS `&H003c6b1a&`
