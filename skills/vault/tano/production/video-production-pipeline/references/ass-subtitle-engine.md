# ASS Subtitle Engine — Brand-Styled Subtitles in FFmpeg

## Why ASS instead of SRT + force_style

FFmpeg's `subtitles` filter supports `force_style` with SRT files, but colons (`:`) inside the style string **conflict with FFmpeg filter option syntax**. Even properly escaped `force_style` parameters fail unpredictably with complex styles (multiple font/color/border settings).

Solution: **Convert SRT → ASS format** with the style baked into the header. ASS natively supports:

- Font name, size, color
- Outline/border (stroke) width and color
- Shadow
- Bold/italic
- Alignment (bottom-center, top-left, etc.)
- Per-line style overrides

## ASS File Structure

```
[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,54,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,10,10,45,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.000,0:00:05.000,Default,,0,0,0,,Hello world
```

## Brand JSON → ASS Style

The primary color in brand.json is stored as hex `#RRGGBB` (e.g. `#1a6b3c`). ASS uses `&HBBGGRR` (Blue-Green-Red reversed). Convert when building the style string:

```python
def make_ass_style(brand: dict) -> str:
    """Build ASS Style string from brand.json fields."""
    c = brand.get('colors', {})
    primary = c.get('primary', '#000000').lstrip('#')
    r, g, b = primary[0:2], primary[2:4], primary[4:6]
    primary_col = f"&H00{b}{g}{r}&"  # ASS format: BBGGRR

    fontsize = brand.get('subtitle', {}).get('fontSize', 54)
    font = brand.get('subtitle', {}).get('font', 'Arial')
    bold = '-1' if brand.get('subtitle', {}).get('bold', True) else '0'
    outline = str(brand.get('subtitle', {}).get('outline', 1.5))
    shadow = str(brand.get('subtitle', {}).get('shadow', 0.5))
    alignment = str(brand.get('subtitle', {}).get('alignment', 2))

    return (
        f"Default,{font},{fontsize},{primary_col},&H00FFFFFF,"
        f"&H00000000,&H00000000,{bold},0,0,0,100,100,0,0,1,"
        f"{outline},{shadow},{alignment},10,10,10,0"
    )
```

The full ASS style string field order: `Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding`

| brand.json field | ASS field | Notes |
|---|---|---|
| `colors.primary` | PrimaryColour | Hex `#RRGGBB` → ASS `&H00BBGGRR&` |
| `subtitle.font` | Fontname | |
| `subtitle.fontSize` | Fontsize | |
| `subtitle.bold` | Bold | `-1` = bold, `0` = normal |
| `subtitle.outline` | Outline | BorderStyle=1 always, Outline = stroke width |
| `subtitle.shadow` | Shadow | |
| `subtitle.alignment` | Alignment | 2=bottom-center |

## Color Format

ASS uses `&HBBGGRR` (Blue-Green-Red hex in reverse order):
- `&H00FFFFFF` = white
- `&H000000FF` = pure red (B=00, G=00, R=FF)
- `&H0000FF00` = pure green
- `&H00FF0000` = pure blue
- `&H003c6b1a&` = green brand (#1a6b3c → B=3c, G=6b, R=1a)

The alpha byte (first two hex digits after &H):
- `00` = fully opaque
- `FF` = fully transparent
- `80` = 50% transparent (for back/background color)

## Common Style Configurations

**Netflix-style (default):**
```
Default,Arial,54,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,10,10,45,0
```
- Font: Arial 54px
- Color: White
- Outline: Black, 3px
- Shadow: 1px semi-transparent
- Alignment: 2 = bottom-center

**Brand green accent (Phát Triển Bản Thân):**
```
Default,Arial,54,&H003c6b1a&,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1.5,0.5,2,10,10,10,0
```
- Font: Arial 54px Bold
- Color: Green (`#1a6b3c` → `&H003c6b1a&`)
- Outline: 1.5px black
- Shadow: 0.5px
- Alignment: 2 = bottom-center

**Clean white on dark (minimal):**
```
Default,Inter,48,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,40,0
```

## SRT → ASS Conversion (Python)

```python
def srt_to_ass(srt_content: str, ass_style: str, ass_path: str) -> str:
    """Convert SRT content to ASS file with brand styling.
    Returns the path to the .ass file.
    """
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1920\n"
        "PlayResY: 1080\n"
        "ScaledBorderAndShadow: yes\n"
        "\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: {ass_style}\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    events = []
    for block in srt_content.strip().split('\n\n'):
        block = block.strip()
        if not block or '-->' not in block:
            continue
        lines = block.split('\n')
        if len(lines) < 2:
            continue
        times = lines[1]
        text = '\\N'.join(l for l in lines[2:] if l.strip()) if len(lines) > 2 else ''
        if '-->' in times:
            start, end = times.split(' --> ')
            # ASS uses '.' as decimal separator (SRT uses ',')
            start_ass = start.replace(',', '.')
            end_ass = end.replace(',', '.')
            # Escape ASS special chars: { } are formatting markers
            text = text.replace('{', '\\\\{').replace('}', '\\\\}')
            events.append(
                f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{text}"
            )

    if not events:
        return ass_path.replace('.ass', '.srt')

    content = header + '\n'.join(events)
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return ass_path
```

## Time-Shifting for Segment Rendering

When rendering individual video segments, each segment has its own time window. Shift the ASS timestamps:

```python
import re

def shift_ass_timestamps(ass_content: str, shift_seconds: float) -> str:
    """Shift all ASS dialogue timestamps."""
    def shift_match(m):
        start = m.group(1)
        end = m.group(2)
        start_sec = parse_time(start)
        end_sec = parse_time(end)
        return f"Dialogue: 0,{format_time(start_sec + shift_seconds)},{format_time(end_sec + shift_seconds)},"

    return re.sub(
        r'Dialogue: \d+,([0-9:\.]+),([0-9:\.]+),',
        shift_match, ass_content
    )
```

## FFmpeg Filter Usage

```bash
# With ASS file (no force_style needed)
ffmpeg -loop 1 -i image.png \
  -vf "subtitles=subtitles.ass" \
  -t 41 output.mp4
```

The `subtitles` filter auto-detects ASS from the `.ass` extension and applies all styling from the file header. No `force_style`, no `charenc`, no `original_size` needed.

**CRITICAL — `fontsdir` breaks filter parsing:**
Do NOT add `fontsdir=C:/Windows/Fonts` to the filter — the colon in `C:` is interpreted as an option separator by FFmpeg's filter graph parser, causing `No option name near '/Windows/Fonts'` and cascading to `Error opening output file: Invalid argument`.

```python
# WRONG — colon in C: breaks everything
sub_filter = f"subtitles={path}:fontsdir=C:/Windows/Fonts"

# RIGHT — omit fontsdir entirely (Windows auto-detects system fonts)
sub_filter = f"subtitles={path}"
```

## ASS File Path on Windows

FFmpeg's subtitles filter uses `:` as option separator. Drive letters like `D:` in the path can confuse it. **Fix**: Copy the ASS to current working directory (bare filename, no path):

```python
temp_ass = f"_temp_sub_{fid:04d}.ass"
shutil.copy2(ass_path, temp_ass)
sub_filter = f"subtitles={temp_ass}"  # bare filename, no path
```

## Style String Reference

The ASS style line format (field order):

```
Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, 
OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, 
ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, 
Alignment, MarginL, MarginR, MarginV, Encoding
```

**BorderStyle values:**
| Value | Effect | Use Case |
|-------|--------|----------|
| 1 | Outline only (thin stroke) | **Netflix clean look** — never blocks video |
| 3 | Opaque background box | Blocks video behind text — avoid |

Always use `BorderStyle=1` for clean overlay subtitles.

**Alignment values:**
| Value | Position |
|-------|----------|
| 2 | Bottom center (default) |
| 5 | Top center |
| 8 | Middle center |
