# Asset Generation Flow for HyperFrames Explainers

This reference documents a proven end-to-end asset generation pipeline for HyperFrames stick-figure explainer videos, combining Pollinations (figures) + Edge TTS (voiceover) + HyperFrames (composition + render).

## Pipeline summary

1. Script → determine per-scene visuals from DESIGN.md archetypes
2. **Voice selection**: sample 4 candidate voices (~15s each), send to user, let them pick
3. Pollinations → generate figure images per scene
4. Edge TTS → generate full voiceover with chosen voice
5. Convert .ogg → .mp3 (if using Hermes `text_to_speech` tool)
6. Get actual audio duration → rescale all scene timings
7. `hyperframes check` → `hyperframes render` → ffprobe verify

**⚠️ Voice-switch duration pitfall:** Different TTS voices read the same script at wildly different speeds. AndrewNeural → GuyNeural can change duration by 2.3x (59s → 135s). Always select the voice BEFORE generating figures and assembling scenes, so you know the real timing.

## Pollinations figures

Fixed style prefix per video (from DESIGN.md). Prefix must NOT change between videos in same series:

```
minimalist stick figure illustration, hand-drawn black ink line art style, clean white background, single red accent color for key element, simple airport and airplane doodle elements, editorial cartoon style, no text, no words, 16:9
```

URL pattern (appended after prefix with scene-specific description):

```
https://image.pollinations.ai/prompt/{URL_ENCODED_PROMPT}?width=1024&height=1024&nologo=true
```

Verification: file must be >30KB (Pollinations returns JPEG regardless of .png extension or 1024x1024 request — actual size is 768×768).

Curl (bash):
```bash
PROMPT="prefix description scene-specific"
curl -o assets/s1-figure.png "https://image.pollinations.ai/prompt/$(python3 -c "import urllib.parse,os;print(urllib.parse.quote(os.environ['PROMPT']))")?width=1024&height=1024&nologo=true"
```

## Edge TTS voiceover via Hermes tool

- Use `text_to_speech` tool (no API key needed)
- **Voice tryout** (see `hyperframes-media` for full workflow): sample 4 voices with same ~15s excerpt, send to user, let them pick
- Recommended voices for English explainers:
  - `en-US-GuyNeural` — **best all-rounder** (warm, professional explainer — podcast style)
  - `en-US-AndrewNeural` — warm/authoritative (main narrator)
  - `en-US-ChristopherNeural` — authoritative/documentary
  - `en-US-EricNeural` — young/casual
  - `en-US-DavisNeural` — trustworthy/finance
- Tool returns `.ogg` — convert to `.mp3`:
  ```bash
  ffmpeg -y -i vo.ogg -c:a libmp3lame -b:a 128k vo.mp3
  ```
- Get actual duration:
  ```bash
  ffprobe -i vo.mp3 -show_entries format=duration -v quiet -of csv="p=0"
  ```
- Actual duration will differ from script estimate (e.g., 59s actual vs 54s estimate) — rescale ALL scene data-start/data-duration values proportionally

## Timing rescale example

Given audio duration `D_actual` and script estimate `D_script`:
- Scale factor = D_actual / D_script
- Each scene's data-duration ≈ original × scale_factor
- data-start values: first scene starts at 0, each subsequent scene starts at previous scene's start + duration
- Root data-duration = D_actual rounded up to nearest whole second
- Audio data-duration = root data-duration (slightly longer than actual audio is fine — framework clips at media end)

## Render verification (always do this)

After `hyperframes render`:
```bash
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 renders/*.mp4
# MUST show: video + audio (2 lines)

ffprobe -v error -show_entries format=duration -of csv=p=0 renders/*.mp4
# MUST be within 0.5s of audio duration
```

Missing audio is the most common silent failure.
