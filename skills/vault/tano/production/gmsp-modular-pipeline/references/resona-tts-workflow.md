# Resona TTS Workflow — GMSP Edition
> Batch generation with Resona API v2/v1 hybrid

## Overview

Resona TTS is the primary voice for GMSP episodes. The API is split across two endpoints:
- **Submit (v2):** `POST /api/v2/text-to-speech` — returns `request_id`
- **Poll (v1):** `GET /api/v1/generate-speech/{id}/status` — returns `audio_urls[]`

## API Details

### Submit (POST /api/v2/text-to-speech)

```json
POST https://resona.live/api/v2/text-to-speech
Authorization: Bearer {api_key}
Content-Type: application/json
{
  "text": "Text to convert...",
  "voice_id": "6SLyzXlPxiBrgjKOuELG",  // Trung Thành
  "speed": 0.9,    // Range 0.8-1.0
  "pitch": 1.0     // Range 0.85-1.15 for emotion
}
```

Response: `{"request_id": "uuid-string"}`

### Poll (GET /api/v1/generate-speech/{id}/status)

```http
GET https://resona.live/api/v1/generate-speech/{request_id}/status
Authorization: Bearer {api_key}
```

**CRITICAL FIELD:** Response has `audio_urls` as an **ARRAY** — NOT `audio_url` string!
```json
{
  "status": "completed",
  "audio_urls": ["https://storage.googleapis.com/..."],  // ⬅ THIS FIELD
  "progress": 100
}
```

If you poll for `audio_url` (singular) you'll never find it.

## Voice IDs (GMSP Cast)

| Voice | ID | Speed | Pitch | Best for |
|-------|-----|-------|-------|----------|
| Trung Thành | `6SLyzXlPxiBrgjKOuELG` | 0.82 | 1.0 | Self-dev, philosophy |
| Vân Anh | `ODDT6PXH9Eb43SpMXZda` | 0.9 | 1.0 | Storytelling |
| Minh Đức | `tak3IN3asjyDvk2dC3iR` | 0.85 | 1.0 | Ancient wisdom |
| Tuấn Tú | `C3tEh3RaFrM9GXzy3lGJ` | 0.8 | 1.0 | Tử vi, mystical |

## Batch Processing Pipeline

### Why batching is needed

Resona has a soft credit limit (~10-12 jobs before `section_credit_limit_exceeded`). Processing 29+ segments sequentially would hit this limit and waste time.

### Recommended approach: 8-segment batches

```
BATCH 1: segments 2-9    (8 files, ~2 min total)
BATCH 2: segments 10-17   (8 files, ~2 min)
BATCH 3: segments 18-25   (8 files, ~2 min)
BATCH 4: segments 26-29   (4 files, ~1 min)
```
Plus 1 test segment first to verify API is responsive.

### Script template

Write a standalone `.py` file in the episode's `tts/` directory, NOT inline in execute_code (API key gets redacted by the system in execute_code sandbox, corrupting the Python). Use `write_file` to create the script, then `terminal` to run it.

**Key: load API key from config at runtime, never hardcode:**

```python
with open("D:/MMO Du an/GMSP/config/settings.json") as f:
    cfg = json.load(f)
API_KEY = cfg["resona_api_key"]   # OK — loaded at runtime
```

**DON'T write:** `API_KEY = "rsk_..."` — the system's credential redactor will replace the string value with `***` even in file contents, breaking the Python syntax.

### Batch script template (batch_9_16.py pattern)

```python
#!/usr/bin/env python3
import json, time, requests

with open("D:/MMO Du an/GMSP/config/settings.json") as f:
    cfg = json.load(f)
API_KEY = cfg["resona_api_key"]
VOICE_ID = "6SLyzXlPxiBrgjKOuELG"
API_V2 = "https://resona.live/api/v2/text-to-speech"
API_V1 = "https://resona.live/api/v1/generate-speech/{id}/status"
OUT = "D:/MMO Du an/GMSP/episodes/ep01-30-40-tuoi/tts"
H = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

with open(f"{OUT}/segments.json") as f:
    segs = json.load(f)

# Submit batch
reqs = {}
for s in segs:
    if 9 <= s["id"] <= 16:   # ← change range per batch
        r = requests.post(API_V2, json={"text": s["text"], "voice_id": VOICE_ID, "speed": 0.82, "pitch": 1.0}, headers=H, timeout=30)
        if r.status_code == 200:
            reqs[s["id"]] = r.json().get("request_id")
            print(f"ok seg-{s['id']:03d}")
        else:
            print(f"fail seg-{s['id']:03d} HTTP {r.status_code}")
        time.sleep(1.5)  # rate limit spacing

print(f"Submitted {len(reqs)}. Waiting 25s...")
time.sleep(25)

# Poll & download
for sid, rid in sorted(reqs.items()):
    url = API_V1.format(id=rid)
    for _ in range(20):
        r = requests.get(url, headers=H, timeout=10)
        if r.status_code == 200:
            d = r.json()
            urls = d.get("audio_urls")  # ARRAY, not string!
            if urls and isinstance(urls, list) and len(urls) > 0:
                ar = requests.get(urls[0], timeout=60)
                if ar.status_code == 200:
                    p = f"{OUT}/seg-{sid:03d}.mp3"
                    with open(p, "wb") as f: f.write(ar.content)
                    print(f"ok seg-{sid:03d} ({len(ar.content)/1024:.1f} KB)")
                break
            elif d.get("status") in ("failed", "error"):
                print(f"fail seg-{sid:03d}")
                break
        time.sleep(3)
```

### To change batch range

```bash
# Template: copy previous batch script
sed 's/if 9 <= s\["id"\] <= 16:/if 17 <= s["id"] <= 24:/' batch_9_16.py > batch_17_24.py
```

## Script Preparation

### Clean voiceover text from script.md

1. Strip metadata lines (Series/Thời lượng/Giọng/Tử Vi lens etc.)
2. Strip section markers `[HOOK — 0:00-0:45]`, `[BỐI CẢNH...]`, `====` lines
3. Replace: em dash `—` → `, `, double quotes `"..."` → `'...'`, ellipsis `...` → `.`
4. Collapse multiple spaces/newlines
5. Split into ~350-400 char segments (Resona max: 5000 chars/job but 350-400 is optimal for natural breaks)

### Segment splitting strategy

Split by **paragraph breaks** first (preserves natural pauses), then by **sentence boundaries** if > 400 chars.

Target: 29-35 segments for a 12-minute script (~7,000 chars).

## Concatenation

Use FFmpeg `filter_complex concat` (NOT concat demuxer — Windows FFmpeg 8.1.1 has issues with the demuxer for MP3):

```bash
ffmpeg -i seg-001.mp3 -i seg-002.mp3 ... -filter_complex "[0:a][1:a]...concat=n=29:v=0:a=1[out]" -map "[out]" -c:a libmp3lame -q:a 2 voiceover_full.mp3
```

On Windows with spaces in path, create a `.bat` file and run with:
```bash
cmd.exe /c concat.bat
```

### Section gaps technique

Thêm 3s silence giữa các section (HOOK, BỐI CẢNH, TỬ VI, TÂM LÝ, GIẢI PHÁP, CLIFFHANGER) để kéo dài total duration ~30-60s và tạo nhịp nghỉ tự nhiên:

```bash
# Tạo silence
ffmpeg -f lavfi -i anullsrc=cl=mono:r=24000 -t 3 -q:a 2 silence_3s.mp3 -y

# Trong concat filter_complex: chèn silence giữa section-boundary segments
# VD: seg-003 (end HOOK) → silence_3s → seg-004 (start BỐI CẢNH)
# Nhóm segment theo section:
#   HOOK: 1-3      → gap → 
#   BỐI CẢNH: 4-8  → gap →
#   TỬ VI: 9-14    → gap →
#   TÂM LÝ: 15-22  → gap →
#   GIẢI PHÁP: 23-30 → gap →
#   CLIFFHANGER: 31-34
#   Tổng: 34 file + 5 silence gaps = 39 inputs
```

### Verification

After concat, always verify with ffprobe:
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 voiceover_full.mp3
```
Expected duration: ~11-12 minutes (~700 seconds) for a 7,000-char script.

## Known Issues

1. **write_file API key redaction:** Writing Python files with `API_KEY = cfg["resona_api_key"]` via `write_file` triggers the system's credential redactor, which corrupts the Python syntax (garbles the next line). 
   - **Workaround:** Create batch scripts via `sed` from a working template: `sed 's/if 9 <= s["id"] <= 16:/if 17 <= s["id"] <= 24:/' batch_9_16.py > batch_17_24.py`
   - Or use `terminal()` with inline python -c instead of write_file
2. **Trigger words for silent failures:** Strip any metadata lines starting with `[` that aren't section markers
2. **Rate limiting:** ~10-12 jobs before `section_credit_limit_exceeded`. Wait 30-60s between batches or switch to Edge TTS fallback
3. **Edge TTS fallback:** `edge-tts --voice vi-VN-NamMinhNeural --rate=+16% --text "..." --write-media output.mp3`
4. **No em dashes:** `—` and `–` cause silent failures — replace with `, ` before submitting
5. **No double quotes:** `"` causes script text truncation — replace with single quotes `'`
