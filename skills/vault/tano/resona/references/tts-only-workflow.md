# TTS-Only Workflow — Generate Full Voiceover Without Rendering

When the user wants **clean voiceover audio only** (no video), use this workflow.

## When To Use
- Need a fresh TTS pass with corrected text (no metadata pollution)
- Resona credit is available and segments need emotion (speed/pitch) mapping
- User wants to drop the audio into CapCut/DAW manually

## The TTS-Only Script

A standalone Python script lives at the GMSP project root:
```
D:/MMO Du an/Giai ma so phan/tts_generate.py
```

Usage:
```bash
python tts_generate.py                    # Uniform speed 0.9
python tts_generate.py --emotion          # Per-segment speed/pitch
python tts_generate.py --emotion --speed 0.85  # Emotion + baseline speed
```

## What It Does

1. **Parse script** into 12+ segments (strips ALL metadata lines starting with `[`)
2. **Submit** each segment to Resona v2 sequentially (one at a time)
3. **Poll** using v1 endpoint, extracting URL from `audio_urls[0]` (not `audio_url`)
4. **Download** to `audio_segments_tts/seg-XXX.mp3`
5. **Concat** into `voiceover_tts.mp3` via FFmpeg

## Emotion Map (Built-In)

| Segment | Label       | Speed | Pitch |
|---------|-------------|-------|-------|
| 1       | Hook        | 0.85  | 0.9   |
| 2       | Setting     | 0.9   | 1.0   |
| 3       | Intro       | 0.95  | 1.05  |
| 4-5     | Traps 1-2   | 0.9   | 1.0   |
| 6       | Trap 3      | 0.85  | 0.9   |
| 7       | Solution 1  | 1.0   | 1.1   |
| 8       | Solution 2  | 0.95  | 1.05  |
| 9       | Solution 3  | 0.9   | 1.0   |
| 10      | Story       | 0.85  | 0.95  |
| 11      | Climax      | 1.0   | 1.15  |
| 12      | End         | 0.8   | 0.85  |

## Key API Fixes Embedded in the Script

- **Poll URL**: v1 returns `audio_urls[]` (array), NOT `audio_url` (string). Script extracts `urls[0]`.
- **Metadata filter**: Uses `s.startswith("[")` — catches ALL Unicode dashes (em `—`, en `–`, hyphen `-`)
- **Text limit**: Max 5000 chars/request (Resona v2 limit); min ~50 chars (50 credit min)
- **Sequential submission**: One segment at time, submit → poll → download → next. Avoids batch timeout issues.
- **Speed override**: `--speed` flag overrides ALL segments to a uniform speed (for quick neutral voiceover)

## Output

```
audio_segments_tts/
  seg-001.mp3 … seg-012.mp3
  concat.txt
voiceover_tts.mp3              ← final concat (16-17 min)
```

No video, no subtitles, no images — just clean audio.
