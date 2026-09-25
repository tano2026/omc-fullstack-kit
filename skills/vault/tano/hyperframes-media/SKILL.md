---
name: hyperframes-media
description: Audio and media assets for HyperFrames compositions — multi-provider TTS (HeyGen / ElevenLabs / Edge TTS / Kokoro local), background music + sound effects, Whisper transcription, background removal, and caption authoring.
---

# HyperFrames Media

Create the audio and media assets a composition needs — voiceover (TTS), background music + sound effects, transcription, captions, background removal — then consume and animate that data in HTML.

## Provider chain (updated)

| Order | Provider          | Env trigger                     | Word timestamps              | Cost  |
|-------|-------------------|----------------------------------|------------------------------|-------|
| 1     | HeyGen (Starfish) | `$HEYGEN_API_KEY` / OAuth login  | **Yes** (native)             | Free OAuth tier |
| 2     | ElevenLabs        | `$ELEVENLABS_API_KEY`            | No — chain `transcribe`      | Paid API |
| 3     | **Edge TTS**      | **always (no key)**              | **No** — chain `transcribe`  | **$0** |
| 4     | Kokoro-82M        | always (local fallback)          | No — chain `transcribe`      | $0 |

### Edge TTS (free, no API key)

Best for: English explainers, faceless videos, prototyping. No key, no signup, works offline after first model download.

```bash
pip install edge-tts

# List voices
edge-tts --list-voices | grep "en-US"

# Generate audio
edge-tts \
  --voice en-US-AndrewNeural \
  --text "Your script here." \
  --write-media assets/vo.mp3
```

**Recommended voices (English explainer/educational):**

| Voice | Style | Best for |
|-------|-------|----------|
| `en-US-AndrewNeural` | Warm, Confident | Main narrator |
| `en-US-GuyNeural` | Warm, Professional, Explainer | **Best all-rounder** — podcast, tech explainer, educational |
| `en-US-BrianNeural` | Casual, Sincere | Friendly explainer |
| `en-US-ChristopherNeural` | Authority, Deep | Insider/educational, documentary |
| `en-US-EricNeural` | Young, Conversational | Casual content, beginner audience |
| `en-US-DavisNeural` | Mid-age, Trustworthy | Finance, health, serious topics |
| `en-US-AriaNeural` | Positive, Confident | Female narrator |
| `en-US-JennyNeural` | Friendly, Approachable | Conversational |

**Vietnamese voices (for Edge TTS):**

| Voice | Style |
|-------|-------|
| `vi-VN-NamMinhNeural` | Male, natural |
| `vi-VN-HoaiMyNeural` | Female, natural |

**Limitations:**
- No native word timestamps — chain `npx hyperframes transcribe vo.mp3` for captions
- Voiceover >5K chars per segment may fail — split into ~16 segments with 30s timeout
- Rate variation: +8% speed = deeper, +16% normal, +25% = higher energy
- Use `--rate=-10%` for slower, more authoritative delivery

## The audio engine

For a full audio pass (TTS + BGM + SFX in one shot), use `scripts/audio.mjs`:

```bash
node <SKILL_DIR>/scripts/audio.mjs --request ./audio_request.json --hyperframes . --out ./audio_meta.json
```

## ffmpeg requirement

All cloud TTS (HeyGen, ElevenLabs) return mp3. Edge TTS returns mp3 too. Transcode to wav when downstream tools expect it.

## Transcription

```bash
npx hyperframes transcribe assets/vo.mp3 --model base
```

## Language rules for Edge TTS

- English uses the voice name's locale (e.g. `en-US-AndrewNeural` = US English)
- Edge TTS supports 100+ languages — use the correct voice prefix for non-English
- When script has mixed language, generate separate segments per language

## Voice Tryout Workflow (Multi-Voice Selection)

When the user wants to hear voice options before committing to one:

1. **Select 4 candidate voices** from the recommended table above — pick diverse styles (e.g., authority + conversational + professional + young)
2. **Generate a sample** of the same ~15-20s script excerpt for each voice using `text_to_speech` tool:
   - Use the opening hook paragraph (most distinctive, sets the channel's tone)
   - Label files as `samples/sample_<voicename>.mp3` or equivalent
3. **Send all samples** to the user as audio files (MEDIA: or voice bubbles)
4. **Wait for user to pick one** — provide a recommendation but let them decide
5. **Regenerate the full voiceover** with the chosen voice
6. **Update all timing** in index.html to match the actual audio duration (see `hyperframes-core/references/asset-gen-flow.md`)

**Voice count rule:** Sample exactly 4 voices unless the user specifies otherwise. Fewer than 3 gives too little contrast; more than 5 overwhelms.

**Voice recommendation heuristic:**
- For educational/explainer → prefer `en-US-GuyNeural` (warm, clear, professional)
- For documentary/insight → prefer `en-US-ChristopherNeural` (deep, authoritative)
- For casual/conversational → prefer `en-US-EricNeural` or `en-US-BrianNeural`
- For finance/trust → prefer `en-US-DavisNeural`

**Pitfall: Duration changes on voice switch.** Different voices speak at different speeds even at the same rate percentage. GuyNeural delivered a 2:15 script that AndrewNeural had read in 0:59 (2.3x difference). Always re-measure duration after voice change and rebuild scene timing.

## Duration Mismatch Handling

When TTS voice or script changes mid-production, the old scene timings, figures, and layouts break. See `general-video/references/voiceover-duration-expansion.md` for the full recovery procedure:

When running inside Hermes agent, use the `text_to_speech` tool instead of the `edge-tts` CLI. The tool returns an `.ogg` file (Opus codec in OGG container), NOT mp3. Convert and verify:

```bash
ffmpeg -y -i output.ogg -c:a libmp3lame -b:a 128k assets/vo.mp3
ffprobe -i assets/vo.mp3 -show_entries format=duration -v quiet -of csv="p=0"
```

## Post-TTS timing adjustment

Generated voiceover duration ALWAYS differs from script timing estimate. After TTS generation:

1. Get actual duration: `ffprobe -i assets/vo.mp3 -show_entries format=duration -v quiet -of csv="p=0"`
2. Compare to script estimate (e.g., 59s actual vs 54s estimate)
3. Scale all scene `data-start`/`data-duration` timings proportionally in `index.html`
4. Update root `data-duration` to match actual audio duration (round up)
5. If audio is shorter than total scene durations, add a 0.5-1s tail to root duration

Failing to rescale = scenes out of sync with narration.

```bash
# Edge TTS — one-shot (English)
edge-tts --voice en-US-AndrewNeural --text "..." --write-media assets/vo.mp3

# Edge TTS — from file
edge-tts --voice en-US-AndrewNeural -f script.txt --write-media assets/vo.mp3

# HeyGen TTS (requires key)
node scripts/heygen-tts.mjs "..." -o assets/vo.wav --words assets/words.json

# Transcribe for captions
npx hyperframes transcribe assets/vo.mp3 --model base
```
