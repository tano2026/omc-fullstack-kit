# GMSP Base Video Rendering — Pitfalls & Workarounds

## Problem: FFmpeg drawtext + long loop is extremely slow
Using `drawtext` filters inside a ~1100s loop causes FFmpeg to render each frame individually, hitting ~1x-2x speed. A 1100s video takes 10+ minutes.

**Fix:** Pre-render all branding text as PNG overlays using Pillow (Python), then use simple `overlay` filter. Overlay filter is ~200x faster than drawtext.

## Problem: Concat-loop with -c copy corrupts H.264 NAL units
```bash
# BAD — produces corrupt video with "Invalid NAL unit size" errors
ffmpeg -f concat -safe 0 -i concat_segments.txt -c copy epXX_base.mp4
```

**Fix:** Always re-encode when concatenating repeated segments:
```bash
ffmpeg -f concat -safe 0 -i concat_segments.txt -c:v libx264 -preset ultrafast -crf 25 epXX_base.mp4
```

Or better: use `-stream_loop` with a single input:
```bash
ffmpeg -stream_loop -1 -i segment.mp4 -c copy -t <duration> epXX_base.mp4
```
(Note: `-stream_loop` with `-c copy` also has issues on some FFmpeg versions — test first.)

## Problem: Base video 1100s + overlay filter_timeout
Even simple overlay filters can timeout on long videos with `-preset ultrafast` at 25fps × 1100s = 27,500 frames.

**Fix:** Swap voiceover audio FIRST (fast copy), THEN add chapter overlays in a separate pass. Overlay 5 chapter images over 1056s video is much faster than rendering base from scratch.

## Problem: Edge TTS actual duration >> character-based estimate
Character-based estimate: ~1100 chars/min for Vietnamese
Edge TTS actual at +16% rate: ~800 chars/min (37% slower)

**Always use ffprobe to measure actual segment durations** before calculating chapter overlay timings.

## Reference: Standard overlay gen commands

**Base render** (10s segment):
```bash
ffmpeg -y -loop 1 -r 25 -i assets/bg_XX.png \
  -i assets/branding_overlay.png -i assets/intro_card.png \
  -filter_complex "\
    [0:v]scale=1920:1080:force_original_aspect_ratio=1,crop=1920:1080,format=yuv420p[bg];\
    [bg][1:v]overlay=x=0:y=0:enable='gte(t,5)'[v1];\
    [2:v]scale=1920:1080,format=yuv420p[intro];\
    [intro][v1]overlay=x=0:y=0:enable='lte(t,5)'[v2]" \
  -map "[v2]" -c:v libx264 -preset ultrafast -crf 25 -t 10 epXX_segment.mp4
```

**Loop segment**:
```bash
for i in $(seq 1 N); do echo "file 'epXX_segment.mp4'"; done > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c:v libx264 -preset ultrafast -crf 25 -c:a aac -b:a 64k -t <dur> epXX_base.mp4
```

**Swap audio**:
```bash
ffmpeg -i epXX_base.mp4 -i tts/voiceover_gap6.mp3 -c copy -map 0:v -map 1:a -shortest epXX_raw.mp4
```

**Chapter overlays**:
```bash
ffmpeg -i epXX_raw.mp4 -i ch1.png -i ch2.png \
  -filter_complex "\
    [0:v][1:v]overlay=0:0:enable='between(t,T1,T1+6)'[v1];\
    [v1][2:v]overlay=0:0:enable='between(t,T2,T2+6)'[out]" \
  -map '[out]' -map 0:a -c:v libx264 -preset fast -crf 25 -c:a copy epXX_final.mp4
```
