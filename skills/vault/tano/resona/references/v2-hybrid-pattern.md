# Resona v2 Hybrid Pattern — Batch Submit + Poll

## Discovery (July 2026)

Resona v2 API (`/api/v2/text-to-speech`) has an unusual architecture:

- **Submit endpoint**: `/api/v2/text-to-speech` — POST, returns `{"request_id": "...", "status": "processing"}`
- **Status endpoints**: 
  - `/api/v2/text-to-speech/{id}/status` → **404** (broken in v2!)
  - `/api/v1/generate-speech/{id}/status` → **200** (works! returns `completed` + `audio_url`)
  - `/api/v2/text-to-speech/{id}` → **200** (returns job metadata but NO `audio_url` in any state)
- **Conclusion**: Submit via v2, poll via v1. This is the "hybrid" pattern.

## Batch Workflow

Instead of serial submit→poll→next→submit→poll (slow, can timeout 300s for 10+ segments), use:

### Phase 1: Submit ALL segments
```python
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})

jobs = []
for i, text in enumerate(segments):
    r = session.post("https://resona.live/api/v2/text-to-speech", json={
        "voice_id": VOICE_ID, "text": text, "speed": SPEED, "language": "vi"
    }, timeout=30)
    data = r.json()
    rid = data.get("request_id", "")
    if rid:
        jobs.append({"index": i, "request_id": rid})
```

### Phase 2: Poll ALL jobs sequentially
```python
for job in jobs:
    rid = job["request_id"]
    for attempt in range(60):
        r = session.get(f"https://resona.live/api/v1/generate-speech/{rid}/status", timeout=15)
        d = r.json()
        if d.get("status") == "completed":
            url = d.get("audio_url", "") or (d.get("audio_urls", [""])[0] if d.get("audio_urls") else "")
            if url:
                dl = requests.get(url, timeout=60)
                with open(f"seg-{job['index']+1:03d}.mp3", "wb") as f:
                    f.write(dl.content)
            break
        if d.get("status") == "failed":
            break
        time.sleep(2)
```

### Phase 3: Concat
```python
with open("concat.txt", "w") as f:
    for p in sorted_segment_paths:
        f.write(f"file '{p}'\n")
os.system(f'ffmpeg -f concat -safe 0 -i concat.txt -c copy "voiceover_full.mp3" -y 2>/dev/null')
```

## Text Cleaning Rules

Resona v2 fails silently on certain Vietnamese text patterns:

1. **`phần trăm`** — causes `status: "failed"`. Replace with `%` or `phan tram` (no diacritic).
2. **Double quotes `"..."`** — can cause job failure. Remove or use single quotes.
3. **Em dashes `—`** — replace with regular dash `-` or space.
4. **Missing diacritics** — text like `tuoi` instead of `tuổi` can trigger CER threshold errors at slow speeds.
5. **Minimum 50 credits** (~50-60 chars). Shorter returns 400 error.
6. **Maximum 2000 credits** (~1800 chars). Longer causes 400 error — chunk before submitting.

## Segment-Level Retry Strategy

When a Resona segment repeatedly fails (status: "failed"):

1. **First attempt**: Clean text of all quotes, dashes, special chars. Resubmit.
2. **If still fails**: Split the segment text into 2-6 smaller parts (~150-300 chars each). Submit each part separately.
3. **Poll and download** all parts as individual MP3s.
4. **Merge with FFmpeg concat** into the final segment file.
5. **If short text also fails**: The key has likely hit its credit limit (`section_credit_limit_exceeded`) — fall back to Edge TTS for remaining segments.

```python
# Example: splitting a failed 947-char segment into 5 parts
parts = [
    "Toi khong noi ai trong so cac ban cung phai khoi nghiep...",
    "10 nam nay, neu ban dung no de hoc, de thu, de xay dung...",
    "Du chi la mot kenh YouTube 50K subs...",
    "Con neu ban dung 10 nam nay de cho doi, de so hai...",
    "Su khac biet giua nguoi thanh cong va nguoi that bai..."
]
rids = [submit_part(p) for p in parts]
poll_all(rids)  # download each as seg-011_part1.mp3 ... seg-011_part5.mp3
# Concat parts into seg-011.mp3
os.system('ffmpeg -f concat -safe 0 -i concat_011.txt -c copy seg-011.mp3 -y')
```

## Credit Limits

- After ~10-12 successful jobs (~4000-5000 credits), Resona starts rejecting with `section_credit_limit_exceeded`.
- **Priority strategy**: Submit hook and key segments first so they complete before the limit hits.
- **Wait-out strategy**: Wait ~30-60 minutes for credit bucket to refill, then submit remaining segments.
- **Fallback**: Edge TTS for low-priority segments when limit is exhausted.

## Keys

- API_KEY: from settings.json `resona_api_key`
- BASE_URL: `https://resona.live`
- Success rate: ~90% (1 in 10 jobs may fail — retry with cleaned text)
- Speed 0.9 is optimal for Trung Thanh — deep tone without being too slow
