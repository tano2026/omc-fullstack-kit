# Remotion Brand → FFmpeg Pipeline Integration

How Remotion brand assets (intro.mp4, outro.mp4, thumbnail.png) integrate with the FFmpeg-based video production pipeline.

## Architecture

```
brand.json (colors, fonts, durations, subtitle_style)
     |
     +-- Remotion: Intro.tsx, Outro.tsx, Thumbnail.tsx
     |       |-- render -> out/intro.mp4 (3.5s)
     |       |-- render -> out/outro.mp4 (5s)
     |       +-- still -> out/thumbnail.png
     |
     +-- content_gen.py (reads brand.json for visual style + color)
     |
     +-- gen_video.py (reads brand.json for subtitle style + intro/outro paths)
             |-- Step 1: Generate subtitles.srt
             |-- Step 1b: Convert SRT -> ASS with brand styling
             |-- Step 2: Render body segments (ASS subtitles burned in)
             |-- Step 3: Concat intro.mp4 + body segments + outro.mp4 + mux audio
             +-- Output: final.mp4 (intro + body + outro)
```

## ASS Subtitle Styling (Instead of force_style)

**Problem:** FFmpeg `subtitles=file.srt:force_style='FontSize=54,...'` uses `:` as both filter option separator and force_style value separator, causing parsing conflicts with hex colors (`&H00FFFFFF`) and long style strings.

**Solution:** Convert SRT to ASS format with the style baked in, then use `subtitles=file.ass` directly:

```python
# gen_video.py — pattern:
def get_brand_ass_style(brand: dict) -> str:
    """Build ASS [V4+ Styles] from brand.json subtitle_style."""
    ss = brand.get('subtitle_style', {})
    # ... extract font, size, color, stroke from brand.json

    # ASS uses BGR format for colors!
    primary = f"&H00{color[4:6]}{color[2:4]}{color[0:2]}"  # RGB -> BGR
    outline = f"&H00{shadow[4:6]}{shadow[2:4]}{shadow[0:2]}"

    return (
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, ...\n"
        f"Style: Default,{font},{size},{primary},..."
    )

def convert_srt_to_ass(srt_path: str, ass_path: str, ass_style: str) -> bool:
    """Parse SRT entries, shift to ASS format with brand style header."""
    # ... parse SRT regex
    # ... write ASS entries with Dialogue: 0,start,end,Default,,0,0,0,,text
```

## ASS Color Format

ASS uses **BGR** not RGB:
- `&H00BBGGRR` (hex color in BGR order)
- Example: brand color `#1a6b3c` (RGB) → `&H003C6B1A` (ASS BGR)
- Python: `f"&H00{color[4:6]}{color[2:4]}{color[0:2]}"`

## Intro/Outro Concat Pattern

```python
def concat_segments(segments, audio_path, output_path,
                    intro_path="", outro_path=""):
    # Collect: [intro?] + body_segments + [outro?]
    all_pieces = []
    if intro_path and os.path.exists(intro_path):
        all_pieces.append(intro_path)
    all_pieces.extend(segments)
    if outro_path and os.path.exists(outro_path):
        all_pieces.append(outro_path)

    # Concat via demuxer (stream copy = fast)
    with open(concat_list, 'w') as f:
        for seg in all_pieces:
            f.write(f"file '{seg}'\\n")

    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0',
                    '-i', concat_list, '-c', 'copy', '-fflags', '+genpts',
                    temp_video])

    # Mux audio (voiceover) on top
    subprocess.run(['ffmpeg', '-i', temp_video, '-i', audio_path,
                    '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0',
                    '-map', '1:a:0', '-shortest', output_path])
```

Intro/outro have no audio — concat with body (no audio) then mux voiceover on top.

## Finding Remotion Outputs from Python

```python
def resolve_remotion_output(pack_slug: str, asset: str) -> str:
    """Search common remotion project directories for intro/outro/thumbnail."""
    remotion_base = os.path.join(BASE, 'brand')
    for d in os.listdir(remotion_base):
        if '-remotion' in d and pack_slug in d:
            path = os.path.join(remotion_base, d, 'out', asset)
            if os.path.exists(path):
                return path
    return ""
```

## brand.json Structure (minimal)

```json
{
  "vertical": "Phát Triển Bản Thân",
  "slug": "phat-trien-ban-than",
  "colors": {
    "primary": "#1a6b3c",
    "accent": "#d4a843",
    "bg": "#0d1b11",
    "text": "#ffffff"
  },
  "intro": { "duration_seconds": 3.5, "fps": 30, "width": 1920, "height": 1080 },
  "outro": { "duration_seconds": 5, "fps": 30, "cta_text": "...", "social": "@..." },
  "thumbnail": { "width": 1920, "height": 1080, "overlay": {...}, "title_style": {...} },
  "subtitle_style": {
    "font": "Arial", "font_size": 54, "font_weight": 700,
    "color": "#ffffff", "shadow_color": "#000000", "stroke_width": 3
  }
}
```

## Key Rules

1. **brand.json is the single source of truth** for colors/durations — hardcode nothing in components or scripts
2. **ASS over force_style** — avoids FFmpeg colon parsing conflicts
3. **Remotion outputs go to `out/`** dir inside the remotion project
4. **gen_video.py auto-discovers** remotion output dirs by scanning `brand/*-remotion/out/`
5. **content_gen.py reads brand.json** for visual style + color (not hardcoded VERTICALS)
