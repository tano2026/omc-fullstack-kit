# Dramatic Audio Post-Processing (FFmpeg)

When TTS alone can't deliver the emotional lên/xuống/cao trào, use FFmpeg post-processing to add drama to an already-generated voiceover.

## Volume Automation

Creates a dynamic volume curve across the voiceover, simulating rising tension and resolution.

```bash
ffmpeg -i voiceover.mp3 \
  -af "volume='if(between(t,0,200),1)+if(between(t,200,500),1.3)+if(between(t,500,700),1.7)+if(between(t,700,850),1.3)+if(gte(t,850),0.7)':eval=frame" \
  -y dramatic.mp3
```

### Typical profile for 16-17 minute video:

| Time Range | Volume | Effect |
|------------|--------|--------|
| 0:00–3:20  | 1.0× (0dB) | Normal intro |
| 3:20–8:20  | 1.3× (+2.3dB) | Build-up |
| 8:20–11:40 | 1.7× (+4.6dB) | **Climax** |
| 11:40–14:10 | 1.3× (+2.3dB) | Resolution |
| 14:10–end | 0.7× (-3dB) + fade | Soft ending |

### Adjusting for shorter/longer videos:
```python
# Proportional mapping based on duration
d = duration  # seconds
filter = (
    f"volume='if(between(t,0,{d*0.2}),1)"
    f"+if(between(t,{d*0.2},{d*0.5}),1.3)"
    f"+if(between(t,{d*0.5},{d*0.7}),1.7)"
    f"+if(between(t,{d*0.7},{d*0.85}),1.3)"
    f"+if(gte(t,{d*0.85}),0.7)':eval=frame"
)
```

## Reverb for Dramatic Depth

Adds space/atmosphere to make the voice feel cinematic. Light reverb at emotional peaks.

```bash
# Light reverb (conversational)
ffmpeg -i voiceover.mp3 \
  -af "aecho=0.8:0.7:100|200:0.3|0.15" \
  -y reverb.mp3

# Heavy reverb (cinematic/cavernous)
ffmpeg -i voiceover.mp3 \
  -af "aecho=0.8:0.5:250|500:0.5|0.25" \
  -y cinematic.mp3
```

Parameters explained:
- `aecho=in_gain:out_gain:delays:decays`
- `delays` (ms): 100|200 = two echo taps at 100ms and 200ms
- `decays`: 0.3|0.15 = first echo at 30% volume, second at 15%
- For dramatic sections, higher delay (250|500ms) + higher decay (0.5|0.25)

## Combined: Volume + Reverb + Compression

Full chain for a 16-min narrated explainer:

```bash
ffmpeg -i voiceover.mp3 \
  -af "volume='if(between(t,0,200),1)+if(between(t,200,500),1.3)+if(between(t,500,700),1.7)+if(between(t,700,850),1.3)+if(gte(t,850),0.7)':eval=frame,\
       aecho=0.8:0.7:100|200:0.3|0.15" \
  -y voiceover_dramatic.mp3
```

## Removing Metadata Noise from Segment Starts

If TTS read metadata like "[00] HOOK — CÂU NÓI THẬT" at the start of a segment, trim 3 seconds from each audio file before concatenating:

```bash
# Trim 3s from front of one segment
ffmpeg -i seg-001.mp3 -ss 3 -c copy -y seg-001-trimmed.mp3

# Then concat all trimmed segments
ffmpeg -f concat -safe 0 -i concat.txt -c copy -y voiceover_clean.mp3
```

For batch trimming:
```python
import subprocess, os
for i in range(1, 13):
    subprocess.run([
        "ffmpeg", "-i", f"seg-{i:03d}.mp3",
        "-ss", "3", "-c", "copy", "-y",
        f"seg-{i:03d}-trimmed.mp3"
    ])
```

## When to Use Post-Processing vs. TTS-Engine Emotion

| Situation | Recommendation |
|-----------|---------------|
| TTS supports speed+pitch per segment | Use engine params (more natural) |
| TTS engine has no emotion control | Use FFmpeg post-processing |
| Want both | Combine: engine for pitch variation + FFmpeg for volume/reverb |
| Segment already rendered (can't redo) | Trim metadata + add volume automation |
| Need maximum dramatic impact | Engine pitch variation + FFmpeg reverb + volume automation |
