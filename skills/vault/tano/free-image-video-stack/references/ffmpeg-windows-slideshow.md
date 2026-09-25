# FFmpeg Windows Slideshow & Concat Guide

## Image Slideshow → Video

### Single image (static)
```bash
ffmpeg -loop 1 -t 30 -i image.png -c:v libx264 -pix_fmt yuv420p -r 24 output.mp4
```

### Ken Burns zoompan effect
```bash
ffmpeg -loop 1 -t 30 -i image.png \
  -vf "zoompan=z=1.05+0.005*n:d=720:fps=24:s=1920x1080" \
  -c:v libx264 -pix_fmt yuv420p output.mp4
```
Note: On some Windows FFmpeg 8.1.1 builds, `n` variable may not work. Use `st` (time in secs): `zoompan=z=1.05+0.1*st:d=720:fps=24:s=1920x1080`

### Resize + pad to 1920x1080 (Dark Academia style)
```bash
-vf "scale=1920:1080:force_original_aspect_ratio=1,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#0d0d0d"
```

## ⚠️ Windows FFmpeg Concat Bug (8.1.1)

**Bug**: Tất cả concat methods fail trên Windows với `-loop 1` inputs. Output chỉ chứa segment đầu tiên.

**Broken** (Windows only):
- `[0:v][1:v]concat=n=2:v=1:a=0[vid]` → chỉ segment 1
- `ffmpeg -f concat -safe 0 -i list.txt` → chỉ segment 1
- `ffmpeg -i concat:seg1.mp4|seg2.mp4` → chỉ segment 1
- MPEG-TS middle format → same failure

## ✅ RAW H.264 BINARY CONCAT (Windows, WORKS) — RECOMMENDED

**Giải pháp**: Binary concat raw H.264 Annex B bitstreams, sau đó mux với audio.

### Full pipeline: 5 images → 20 min video + audio + subtitles

```python
import subprocess, os, tempfile, shutil

images = ['scene_01.png', 'scene_02.png', ...]  # N images
durations = [246, 246, 246, 246, 205]           # seconds per image
audio_path = 'voiceover.mp3'
subs_path = 'subs.srt'   # optional SRT file
output = 'final.mp4'
total_s = sum(durations)

tmp = tempfile.mkdtemp()
raws = []

# Step 1: Render each image segment + extract raw H.264 Annex B
for img, dur in zip(images, durations):
    seg = os.path.join(tmp, 'seg.mp4')
    subprocess.run(['ffmpeg', '-y', '-loop', '1', '-t', str(dur), '-i', img,
        '-vf', 'scale=1920:1080:force_original_aspect_ratio=1,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#0d0d0d',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '22',
        '-pix_fmt', 'yuv420p', '-r', '24', seg, '-loglevel', 'error'], check=True)
    raw = os.path.join(tmp, 'raw.h264')
    subprocess.run(['ffmpeg', '-y', '-i', seg, '-c:v', 'copy',
        '-bsf:v', 'h264_mp4toannexb', '-f', 'h264', raw, '-loglevel', 'error'], check=True)
    raws.append(raw)

# Step 2: Binary concat raw H.264 streams
combined = os.path.join(tmp, 'combined.h264')
with open(combined, 'wb') as out:
    for raw in raws:
        with open(raw, 'rb') as f:
            out.write(f.read())

# Step 3: Mux video + audio
# ⚠️ CRITICAL: Use -t DURATION, NOT -shortest with raw H.264
# -shortest can't detect raw H.264 duration → audio stream dropped silently
no_subs = os.path.join(tmp, 'no_subs.mp4')
subprocess.run(['ffmpeg', '-y', '-i', combined, '-i', audio_path,
    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
    '-t', str(total_s),
    '-pix_fmt', 'yuv420p', no_subs, '-loglevel', 'error'], check=True)

# Step 4 (optional): Embed subtitles as track — NO re-encode!
subprocess.run(['ffmpeg', '-y', '-i', no_subs, '-i', subs_path,
    '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text',
    '-metadata:s:s:0', 'language=vie', output, '-loglevel', 'error'], check=True)

shutil.rmtree(tmp, ignore_errors=True)
```

## Netflix-Style Subtitles (Burned-in)

### ⚠️ Critical: BorderStyle=3 is BOX, not outline
`BorderStyle=3` creates a **background box** behind the text — on long Vietnamese subtitles it appears as "taking up the whole screen" because the box stretches the full text width. This is NOT outline.

```bash
# ✅ NETFLIX STYLE (outline, no box) — BordersStyle=1
# PrimaryColour format: &H+AABBGGRR (Alpha, Blue, Green, Red)
style='FontName=Arial,FontSize=54,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1,Shadow=0,MarginV=60,Alignment=2'

# Apply with subtitles filter + force_style
ffmpeg -i input.mp4 \
  -vf "subtitles='subs.srt':force_style='$style':original_size=1920x1080" \
  -c:v libx264 -preset veryfast -crf 24 \
  -c:a aac -b:a 128k \
  -t DURATION \
  -pix_fmt yuv420p output.mp4
```

| Style parameter | Meaning | Netflix value |
|----------------|---------|---------------|
| `BorderStyle=1` | **Outline** (text + outline, no background) | ✅ Correct |
| `BorderStyle=3` | **Box** (full background rectangle behind text) | ❌ Cover entire screen area |
| `Outline=1` | Outline thickness in pixels | 1px (thin, clean) |
| `Shadow=0` | Shadow depth | None (Netflix doesn't use shadow) |
| `MarginV=60` | Bottom margin from edge | 60px clearance |
| `Alignment=2` | Bottom center | Standard subtitle position |

### Two approaches for subtitles

**Approach A: Embed as track (no re-encode, instant, recommended)**
Use when the target platform (Telegram, YouTube) supports soft subtitles:
```bash
ffmpeg -i video.mp4 -i subs.srt -c:v copy -c:a copy -c:s mov_text output.mp4
```

**Approach B: Burn into video (re-encode, slow)**
Use when you MUST have subtitles in the pixels (TikTok, Instagram, uploaded to sites that strip metadata):
```bash
# Must use -t DURATION (not -shortest) and -c:a aac (not -c:a copy + -map)
# These workarounds fix the FFmpeg Windows audio-tracking bug
ffmpeg -i no_subs.mp4 \
  -vf "subtitles='subs.srt':force_style='FontName=Arial,FontSize=54,...':original_size=1920x1080" \
  -c:v libx264 -preset veryfast -crf 24 \
  -c:a aac -b:a 128k \
  -t DURATION \
  output.mp4
```
⚠️ Burning subtitles is 5-10x slower (0.2x-1x speed) than copying. A 20-minute video takes 15-30 min real time.

### Single-line subtitle generation from script JSON
When generating SRT from a structured script:

```python
# Extract narration, cap at ~75 chars, one line only
import json, re

with open('script.json') as f:
    data = json.load(f)

for i, fr in enumerate(data['frames']):
    raw = fr.get('narration', '')
    m = re.search(r'\*\*narration:\*\*\s*["""](.*?)["""]', raw, re.DOTALL)
    text = m.group(1).strip() if m else ''
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Override headers, empty frames with clean text
    if not text or len(text) < 8:
        text = 'Continue watching...'
    
    # Single line, max 80 chars
    text = text[:77] + '...' if len(text) > 77 else text
    
    start = i * frame_duration  # e.g. 41s per frame
    end = start + frame_duration
    # Format as SRT or VTT entry
```

### Verification checklist (updated)
```bash
# Check audio exists
ffprobe -v quiet -select_streams a -show_entries stream=index output.mp4

# Check duration
ffprobe -v quiet -show_entries format=duration -of csv=p=0 output.mp4

# Check subtitles (track approach)
ffprobe -v quiet -select_streams s -show_entries stream=codec_name output.mp4
# → shows "mov_text" ✓

# Verify Netflix style burned-in (use browser_vision or screenshot)
# White text, thin black outline, bottom center, no box background
```

### Key fixes — why each matters

| Problem | Symptom | Fix |
|---------|---------|-----|
| Concat only 1 segment | 3:27 instead of 20 min | Binary concat raw H.264 Annex B (not FFmpeg concat) |
| No audio in output | Telegram file has no sound | `-t DURATION` not `-shortest` with raw H.264 input |
| Subtitles remove audio | Video plays silent after subtitle burn | Embed as mov_text track (no re-encode) instead of burning in |
| Windows path in subtitles filter | "Unable to open subs.srt" | Copy SRT to CWD, use relative path |
| Frame drop/loss | Video shorter than expected | Use `-c:v copy` for muxing, never re-encode concatenated H.264 |

### Verification checklist
```bash
# Check audio exists
ffprobe -v quiet -select_streams a -show_entries stream=index output.mp4
# Should output "index" → audio present

# Check duration
ffprobe -v quiet -show_entries format=duration -of csv=p=0 output.mp4
# Should be ~1189 for 20-min video

# Check subtitles
ffprobe -v quiet -select_streams s -show_entries stream=codec_name output.mp4
# Should show "mov_text" → subs embedded

# Send via Telegram (if Bot API available)
# Use curl/requests with multipart upload:
curl -F chat_id=762010475 -F video=@output.mp4 \
  -F caption="Video title" \
  https://api.telegram.org/bot${TOKEN}/sendVideo
```

## Concat Audio (works fine on Windows)

```bash
ffmpeg -y -i chunk1.mp3 -i chunk2.mp3 \
  -filter_complex '[0:a][1:a]concat=n=2:v=0:a=1[out]' \
  -map '[out]' -c:a aac -b:a 128k output.mp3
```
