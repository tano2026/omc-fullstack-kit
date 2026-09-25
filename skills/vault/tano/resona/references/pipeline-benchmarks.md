# Resona TTS Benchmarks & Pipeline Notes

## Gen time benchmarks (July 2026, speed=1.0)

| Text length | Chars | Gen time | Polls (2s) | Status |
|------------|-------|----------|-----------|--------|
| Short phrase | 149 | ~24s | ~12 | ✅ |
| Single frame narration | 191 | ~30s | ~15 | ✅ |
| Half episode (12 frames) | 1,808 | ~64s | ~32 | ✅ |
| Half episode (12 frames) | 1,557 | ~46s | ~23 | ✅ |

**Rule of thumb**: ~30s / 1000 chars at speed 1.0.

## Job TTL
- Job expires ~60-90s after last poll
- Must poll continuously (every 2s) until "completed"
- 404 "Request not found" = job expired, must re-submit
- No pause-and-resume: once you stop polling, the job is gone

## Common errors & resolutions

| Error | Cause | Fix |
|-------|-------|-----|
| `400 Section text is below the 50-credit minimum` | Text < ~50 chars | Add more text or concatenate frames |
| `400 Section text exceeds the 2000-credit limit` | Text > ~2000 chars | Chunk at ~1800 chars |
| `401 Invalid token` | Rate limit / expired key / wrong key | Regenerate from Resona dashboard |
| `404 Request not found` | Job expired | Re-submit, poll at 2s intervals |
| `403 cloudflare` | urllib blocked | Use `requests` with `User-Agent: Mozilla/5.0` |

## Chunk & merge pipeline

```python
# Submit chunks in sequence (NOT parallel — API rate limits)
chunks = chunk_text(full_narration, max_chars=1800)
audio_files = []

for c in chunks:
    url = resona_generate(api_key, f"Speaker 1: {c}")
    if url:
        resp = requests.get(url)
        path = f"chunk_{len(audio_files)}.mp3"
        with open(path, "wb") as f:
            f.write(resp.content)
        audio_files.append(path)

# Merge with FFmpeg
n = len(audio_files)
inputs = "".join([f"[{i}:a]" for i in range(n)])
cmd = ["ffmpeg", "-y"]
for f in audio_files:
    cmd += ["-i", f]
cmd += [
    "-filter_complex", f"{inputs}concat=n={n}:v=0:a=1[out]",
    "-map", "[out]", "merged.mp3", "-loglevel", "error"
]
subprocess.run(cmd, check=True)
```

## Full video pipeline (Ep3 use case)
1. Generate script (29 frames, 20 min)
2. Generate 5 Dark Academia images via Imagen 4
3. Split narration into 2 chunks (~1800 chars each)
4. Submit each chunk to Resona, poll at 2s
5. Download both MP3s
6. Merge with FFmpeg concat filter
7. Render video: render image segments → extract raw H.264 → binary concat → mux with audio
8. Burn subtitles in second pass (re-encode from muxed copy)
9. Send via Telegram Bot API
