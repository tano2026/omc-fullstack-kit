# Airfare Decoded — FFmpeg Scene-Card Production Pipeline (2026)

## Khi nào dùng pipeline này

- Kênh YouTube tiếng Anh **faceless explainer** 
- Muốn **$0** — không HyperFrames, không Playwright, không HeyGen
- Voice qua Edge TTS, render qua FFmpeg + Pillow scene cards
- Full-length video (8-15 phút) với scene cards tĩnh (text cards)

## Pipeline

```
Research → Script (~2,500 từ) → Voiceover (Edge TTS segment) → Scene Cards (Pillow) → FFmpeg concat → Verify
```

## Step-by-Step

### 1. Script
- ~2,500 từ → 10-13 phút
- 11-13 scene, mỗi scene có: timing, type, title, body
- Saved at `scripts/script-seriesA-video1.md`

### 2. Voiceover — Edge TTS

**Preferred US English male:**
- **SteffanNeural** (`en-US-SteffanNeural`): mid-aged, warm authority → **primary**
- GuyNeural: podcast casual → alternative
- ChristopherNeural: deep authoritative → dramatic

**Edge TTS 5000-char limit:** split script into ~300-char segments, gen each, concat:

```bash
edge-tts --voice en-US-SteffanNeural --text "segment text" --write-media voiceover/segment_XX.mp3
```

Create `concat_list.txt`:
```
file 'segment_01.mp3'
file 'segment_02.mp3'
...
```

Concat: `ffmpeg -f concat -safe 0 -i concat_list.txt -c copy voiceover/steffan_voiceover.mp3`

**Duration:** ~2,500 words → ~768s (12:48)

### 3. FFmpeg Portable Install (Windows, no admin)

```bash
curl -L -o ffmpeg.zip "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
unzip -q ffmpeg.zip -d ~/ffmpeg/
export PATH="$HOME/ffmpeg:$PATH"
```

From Python/execute_code: use `os.path.expanduser("~/ffmpeg/ffmpeg.exe")`

### 4. Scene Cards — Pillow

**1920×1080, dark theme:** `#0A0F1E` bg, `#00BCD4` teal accent, `#FFD700` gold, `#FF5722` accent, `#FF3232` red

**Scene types with colors:**
| Type | Color | Tag |
|------|-------|-----|
| hook | #FF5722 | Hook — The Setup |
| myth | #FF3232 | Myth Debunked |
| myth_bust | #00BCD4 | How It Actually Works |
| reveal | #FFD700 | The Hidden System |
| visual | #00BCD4 | Visual Breakdown |
| scenario | #FFD700 | Real-Time Scenario |
| gds | #00BCD4 | The Middleman |
| atpco | #FFD700 | Industry Secret |
| math | #00BCD4 | The Math |
| timing | #00C853 | Insider Strategy |
| hotel | #00BCD4 | Analogy |
| summary | #FFD700 | Key Takeaways |
| cta | #FF5722 | What's Next |

**Card layout:** 6px accent top line → type tag (top-left) → scene# (top-right) → separator → title (68pt) → body (38pt) with keyword highlighting → bottom bar (progress + timing + brand)

**Keyword highlighting:**
- Fare buckets (`Q =`, `V =`, `M =`) → gold
- "BUCKETED OUT", "SOLD OUT", "ZERO" → red
- Key insights → gold

### 5. FFmpeg Concat

Each scene image is `-loop 1 -i scene_N.png` with `trim=duration=N,setpts=PTS-STARTPTS` in filter_complex. Voiceover mapped as audio.

```bash
ffmpeg -y -loop 1 -i scene_00.png ... -loop 1 -i scene_12.png -i voiceover.mp3 \
  -filter_complex "[0:v]trim=duration=22,setpts=PTS-STARTPTS[v0];...concat=n=13:v=1:a=0[vid];[13:a]adelay=0|0[aud]" \
  -map "[vid]" -map "[aud]" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 192k renders/video_full.mp4
```

### 6. Verify (MANDATORY)

```bash
ffprobe -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 renders/video_full.mp4
# MUST show video AND audio streams

ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1:nokey=1 renders/video_full.mp4
# Verify duration ≈ voiceover duration
```

## Typical Production Stats
- Script: 2,500 words → 12:48 voiceover
- 13 scene cards: 30-60s Pillow gen
- FFmpeg concat: 1-3 min
- Final: ~9-10 MB (1920×1080, CRF 23, AAC 192k)
