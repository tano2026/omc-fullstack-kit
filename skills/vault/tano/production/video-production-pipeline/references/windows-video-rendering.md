# Windows Video Rendering with FFmpeg — Session-Specific Detail

> Absorbed from `windows-video-rendering` (Jul 2026)

## Unique Technical Detail Not Covered in Umbrella Summary

### Concat Demuxer Production Pattern

The only reliably working concat method for 13+ clips on Windows FFmpeg 8.1.1:

1. **Render clips with `-an`** (no audio):
```python
cmd = ["ffmpeg", "-loop", "1", "-i", img,
       "-c:v", "libx264", "-t", str(dur),
       "-preset", "fast", "-crf", "23",
       "-pix_fmt", "yuv420p", "-vf", vf,
       "-an",  # ⚡ CRITICAL: no audio in clips
       "-y", clip]
```

2. **Concat with explicit `-map` + `-t DURATION`** (NOT `-shortest`):
```python
cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_txt,
       "-i", VOICE_MP3,
       "-map", "0:v", "-map", "1:a",     # explicit mapping
       "-c:v", "libx264", "-preset", "fast", "-crf", "23",
       "-c:a", "aac", "-b:a", "128k",
       "-pix_fmt", "yuv420p",
       "-t", str(vo_dur),                 # ⚡ use -t not -shortest
       "-y", OUTPUT]
```

**Why this works:** `-an` on clips prevents concat demuxer from getting confused by empty audio tracks. `-map` explicitly selects streams. `-t` prevents `-shortest` from truncating early (concat demuxer reports imprecise video duration from `-loop 1` inputs).

### Raw H.264 Annex B Binary Concat

For very long renders (20+ clips) or when all other methods fail:

1. Render each segment as MP4 with identical encoding params
2. Extract raw H.264 Annex B: `ffmpeg -i seg.mp4 -c:v copy -bsf:v h264_mp4toannexb -f h264 seg.h264`
3. Binary concat: `cat seg1.h264 seg2.h264 > combined.h264` (or Python `shutil.copyfileobj`)
4. Mux with audio using `-t DURATION` (never `-shortest`):
```python
cmd = ['ffmpeg', '-i', combined.h264, '-i', audio.mp3,
       '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
       '-t', str(total_duration), '-pix_fmt', 'yuv420p', output]
```

**CRITICAL:** `-c:v copy` on the mux step — using `-c:v libx264` re-triggers the concat bug. For subtitle burn-in, do a second pass from the muxed output.

### Concat Filter Property Normalization

The `concat` filter silently drops all but the first segment when inputs have **different resolution, framerate, pixel format, or SAR**. No error message — FFmpeg exits with code 0.

**Fix:** Force identical properties on every clip:
- `-r 30` (same framerate on all clips)
- `-pix_fmt yuv420p`
- `scale=1920:1080` or `setsar=1`

**Detection:** Run ffprobe on each clip comparing resolution, r_frame_rate, and pix_fmt before concat.

### ffprobe on Windows MSYS Quirk

`ffprobe -of default=noprint_wrappers=1` on git-bash/MSYS returns prefixed output:
```
duration=1013.357333   # not bare "1013.357333"
```
Always strip the prefix:
```python
raw = r.strip().replace('duration=', '')
dur = float(raw)
```
The `-of csv=p=0` variant works as documented — only `default=noprint_wrappers=1` has this issue on MSYS.

### PNG Size Trick for Subtitle Verification

After burning subtitles, confirm they rendered by comparing PNG file size from the same frame:
```bash
ffmpeg -y -ss 00:02:00 -i subbed.mp4 -vframes 1 sub_test.png
ffmpeg -y -ss 00:02:00 -i no_subs.mp4 -vframes 1 no_sub_test.png
# Difference >200 bytes = text rendered (PNG lossless, text = high-frequency detail)
```

### BorderStyle Critical Distinction
- `BorderStyle=1` = **outline only** (Netflix style — thin stroke, no background) **✓ Use this**
- `BorderStyle=3` = **background box** (solid rectangle behind text — "taking over the screen") **✗ Never use**

### `-t DURATION` on Both Passes
Use `-t DURATION` on BOTH the mux step AND the subtitle burn step. Without it on pass 2, the subtitles filter causes incorrect output duration.

### `fontsdir` Option Breaks Filter Parsing
Do NOT add `fontsdir=C:/Windows/Fonts` to the subtitles filter — the colon in `C:` is interpreted as an option separator, causing `No option name near '/Windows/Fonts'`. Windows auto-detects system fonts; omit `fontsdir` entirely.

### Concat List Newline Pitfall
Write file path per line with actual newlines, not `\n` escape sequences:
```python
# WRONG — writes literal "\n" (one long line)
f.write(f"file '{path}'\\n")
# RIGHT — writes actual newline
f.write(f"file '{path}'\n")
```
Verify with: `cat -A _concat_list.txt` — each line should end with `$` not `\\n$`.

### Windows Path Tab Traps
Directory names containing `\t` (e.g., `tl-01-...`) are interpreted as tab characters. Always normalize paths to forward slashes before writing concat lists.

### ASS → `-c:s mov_text` Does NOT Work
The `mov_text` codec cannot represent ASS formatting. FFmpeg silently drops the subtitle stream. Burn ASS into video via filter or use SRT for soft-subs.

### Common Failure Signal Table

| Signal | Cause | Fix |
|--------|-------|-----|
| `Simple and complex filtering cannot be used together` | Using `-vf` + `-filter_complex` on same stream | Move all into `-filter_complex`, map final label |
| `Error applying option 'original_size'` | Windows drive colon in filter path | Copy file to CWD, use bare filename |
| Output plays but NO audio | `-shortest` with raw H.264 | Use `-t DURATION` instead of `-shortest` |
| Output duration = first segment duration | `-c:v libx264` re-encode on concat | Use `-c:v copy` + separate pass |
| Output duration = first segment, concat filter | Resolution/framerate mismatch | Force `-r 30` + `scale=` + `-pix_fmt` on ALL clips |
| `No option name near` in subtitles filter | `fontsdir=C:/Windows/Fonts` colon in path | Omit fontsdir entirely |
| ffprobe output = `duration=123s` not `123s` | MSYS prefix issue | Strip `duration=` prefix |
