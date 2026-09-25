# TTS Video Pipeline — Session-Specific Detail

> Absorbed from `tts-video-pipeline` (Jul 2026)

## Unique Technical Detail Not Covered in Umbrella Summary

### Unicode Dash Filtering (Critical for Vietnamese)
Vietnamese scripts often use em dashes (—) and en dashes (–) which cause TTS to pause or garble. Always filter:
```python
text = text.replace('\u2014', '-').replace('\u2013', '-')  # em dash → hyphen, en dash → hyphen
```
This prevents Resona/Edge from inserting unnatural pauses mid-sentence.

### Resona v2 Submit + v1 Poll Workaround
Resona v2 submission (`POST /api/v2/text-to-speech`) returns a request ID in format `v2_req_<hex>`, but v2 polling may consistently return 404 if the backend hasn't fully migrated. **Workaround:** after v2 submit (which generates the audio), poll using v1 endpoint (`GET /api/v1/tts/status/<request_id>`). The v1 poll path works even for v2-submitted jobs.
- **ID expiration:** request IDs expire ~60s after completion. If you don't poll fast enough, the ID returns 404 and you must re-submit.
- **Retry strategy:** poll every 2s up to 30 attempts, sleep 2s between failures, give up at 60s.

### Emotion Mapping Table
Different script sections need different TTS parameters:
```python
EMOTIONS = {
    "hook":       {"speed": 0.85, "pitch": 0.9},   # Slow, deep — grab attention
    "climax":     {"speed": 1.0,  "pitch": 1.15},  # Faster, higher pitch — intensity
    "ending":     {"speed": 0.8,  "pitch": 0.85},  # Slow, low — reflective close
    "default":    {"speed": 0.95, "pitch": 1.0},   # Normal narration
}
```

### Ken Burns Zoompan on FFmpeg 8.1.1 Windows
The `zoompan` filter's variable expressions (like `n` for frame count) often fail on Windows FFmpeg 8.1.1 with `Parse error` or silently produce only the first frame and a black screen thereafter.
- **Workaround:** Use simpler scale + crop animation instead of zoompan:
  ```python
  # Instead of: "zoompan=z='zoom+0.001':d=125"
  -vf "scale=1920:1080:force_original_aspect_ratio=1,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#0d0d0d"
  ```
- **If zoompan is essential:** use `st` (time in seconds) not `n` (frame count) in expressions, and test with short clips first.

### Content Expansion for Target Duration
Target format is ~200 words/min at speed 0.9 TTS. If the source script is too short:
```python
target_chars = dur_minutes * 200  # approximate
if len(script_chars) < target_chars * 0.7:
    # Expand: add illustrative stories, examples, or deeper analysis
    # Pattern: introduce a concrete example → analyze → connect back to main point
```
- Keep natural pacing — don't pad with filler words. Add genuine content (case studies, historical context, audience questions).
- Each expansion should add 30-60s of natural spoken content.

### Segment Retry on Failures
When a long script fails to generate audio (or generates garbled audio):
1. Split script into smaller segments (200-400 chars each instead of 500-800)
2. Submit each segment independently
3. Concatenate audio files with FFmpeg concat demuxer
```python
# Build concat list
with open('concat.txt', 'w') as f:
    for seg_file in sorted(os.listdir('segments')):
        f.write(f"file '{seg_file}'\n")
# Concat
os.system(f'ffmpeg -f concat -safe 0 -i concat.txt -c copy combined.mp3 -y')
```

### Edge TTS Fallback Details
- Edge TTS voices: `vi-VN-NamMinhNeural` (male), `vi-VN-HoaiMyNeural` (female)
- Rate adjustment: `rate=-20%` to `rate=+0%` depending on desired speed
- Edge has no emotion/param controls — switch to Resona when emotional variation matters
