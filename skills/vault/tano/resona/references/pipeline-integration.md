# Resona — Pipeline Integration: gen_audio.py

## TTS backend switch pattern

`gen_audio.py` supports two backends via `--tts {edge|resona}`:

```python
# In argument parser
parser.add_argument('--tts', choices=['edge', 'resona'], default='edge')
```

The CLI entry point selects the backend:

```python
if args.tts == 'resona':
    # Parallel batch: submit all → poll batch → download → concat
    api_key = os.environ.get('RESONA_API_KEY')
    if not api_key:
        # Fallback: parse ~/.hermes/.env
        ...
    seg_results = resona_batch_generate(api_key, valid_narations, seg_dir)
    # Map results back to frames (with silence fallback for failed ones)
    ...
else:
    # Sequential Edge TTS: 1 frame at a time
    ...
```

## The `resona_batch_generate` function

Located inside `gen_audio.py`. Three steps:

### Step 1: Parallel submit (threading)

```python
results = [None] * total
lock = threading.Lock()

def _submit(idx, text):
    prefixed = f"Speaker 1: {text}"
    try:
        resp = requests.post(
            f"{RESONA_API_BASE}/api/v1/generate-speech",
            headers={"Authorization": f"Bearer {api_key}", "User-Agent": "Mozilla/5.0",
                     "Content-Type": "application/json"},
            json={"text": prefixed, "voice_ids": [RESONA_VOICE_ID],
                  "language": "vi", "speed": RESONA_SPEED},
            timeout=30)
        if resp.status_code == 200:
            with lock:
                results[idx] = {"idx": idx, "request_id": resp.json()["request_id"], "ok": True}
        else:
            with lock:
                results[idx] = {"idx": idx, "ok": False, "error": resp.text[:200]}
    except Exception as e:
        with lock:
            results[idx] = {"idx": idx, "ok": False, "error": str(e)}

threads = [threading.Thread(target=_submit, args=(i, texts[i])) for i in range(total)]
for t in threads: t.start()
for t in threads: t.join()
```

Uses `threading.Thread` (not asyncio) because Resona API calls are blocking HTTP POST. Submitting 29 jobs takes ~1-3s total.

### Step 2: Parallel poll batch (threading)

```python
poll_results = [None] * total

def _poll(idx, request_id):
    headers = {"Authorization": f"Bearer {api_key}", "User-Agent": "Mozilla/5.0"}
    url = f"{RESONA_API_BASE}/api/v1/generate-speech/{request_id}/status"
    deadline = time.time() + 120  # 2 min timeout
    while time.time() < deadline:
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 404:
                break  # job expired
            if resp.json().get("status") == "completed":
                urls = resp.json().get("audio_urls", []) or [resp.json().get("audio_url", "")]
                with lock:
                    poll_results[idx] = urls[0] if urls else None
                return
            time.sleep(2)  # CRITICAL: 2s, not 5s
        except Exception:
            time.sleep(2)

threads = [threading.Thread(target=_poll, args=(r["idx"], r["request_id"]))
           for r in submitted]
for t in threads: t.start()
for t in threads: t.join()
```

### Step 3: Download sequentially (safer)

```python
for idx, url in enumerate(poll_results):
    if not url:
        continue  # will get silence fallback
    resp = requests.get(url, timeout=60)
    seg_path = os.path.join(seg_dir, f"frame_{idx+1:04d}.mp3")
    with open(seg_path, "wb") as f:
        f.write(resp.content)
```

## Key config constants

```python
RESONA_API_BASE = "https://resona.live"
RESONA_VOICE_ID = "dwK3JbXXe2LLisf6Tfx6"  # Minh Tuấn miền nam
RESONA_SPEED = 1.0
```

## Error handling strategy

- **Submit failures** → track as `failed_s`, continue with remaining jobs
- **Poll failures/expiry** → skip, frame gets silence AudioSegment fallback
- **Download failures** → skip, frame gets silence fallback
- **All submissions fail** → generate ALL silence segments at target_duration
- Never crash the pipeline — even if Resona is completely down, produce voiceover.mp3 with silence

## track.json metadata

When using Resona, the output `track.json` includes:
```json
{
  "tts": "resona",
  "voice": "dwK3JbXXe2LLisf6Tfx6",
  "rate": 1.0,
  ...
}
```

This lets downstream scripts (gen_video, publish) know the source.
