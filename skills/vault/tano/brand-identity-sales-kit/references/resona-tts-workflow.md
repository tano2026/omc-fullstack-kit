# Resona TTS Workflow — GMSP Video Production

## API Endpoints
- **Submit (v2):** `POST https://resona.live/api/v2/text-to-speech`
- **Poll (v1):** `GET https://resona.live/api/v1/generate-speech/{request_id}/status`

## Parameters (tested)

| Param | Value | Notes |
|-------|-------|-------|
| voice_id | `6SLyzXlPxiBrgjKOuELG` (Trung Thành) | Male, tin-tuc style |
| | `ODDT6PXH9Eb43SpMXZda` (Vân Anh) | Female, chia-se style |
| | `tak3IN3asjyDvk2dC3iR` (Minh Đức) | Male, chia-se style |
| | `C3tEh3RaFrM9GXzy3lGJ` (Tuấn Tú) | Male, sach-noi style |
| speed | 0.82 | Default for 10-12 min episodes |
| pitch | 1.0 | Neutral. Use 0.85-1.15 for emotional emphasis |

## Speed vs Duration Mapping

| Chars | Speed | Duration | Notes |
|-------|-------|----------|-------|
| ~7200 | 0.9 | 8:33 | Too short, sections feel rushed |
| ~8800 | 0.9 | ~10:00 | Better, but still no pauses |
| ~8800 | 0.82 | 10:25 | ✓ Right length with section gaps |

Formula: `duration_seconds ≈ chars / 14.2 * (0.9 / speed)`

## Text Cleaning Rules

Characters that cause silent TTS failures:
- `"..."` (double quotes) → replace with single quotes `'...'`
- `—` (em dash) → replace with `, `
- `–` (en dash) → replace with `, `
- `[CÂU CHUYỆN N]` markers → strip before submitting
- Metadata lines starting with `[` → strip
- `===` lines → strip

## Segment Splitting

Rule: max 350-400 chars per segment, split at sentence boundaries.

```python
MAX_CHARS = 350
# Split by paragraphs first, then sentence-split any >400c segments
# Use regex: re.split(r'(?<=[.!?])\s+', text)
```

Typical split: ~30-35 segments for 10 min episode.

## Batch Processing

- Submit max 8-10 segments per batch
- 1.5s delay between submissions
- 15-25s wait before polling
- Poll timeout: ~60-120s total per batch
- Cooldown 3s between batches

## Credit Limits

~10-12 sequential jobs before `section_credit_limit_exceeded`. Recovery: wait ~1-2 hours or use backup TTS (Edge TTS).

## Concat with Silence Gaps

```bash
# Create 3s silence
ffmpeg -f lavfi -i anullsrc=cl=mono:r=24000 -t 3 silence_3s.mp3 -y

# Concat segments + silence between sections
# Build filter: segs 1-3, silence, segs 4-8, silence, segs 9-14, silence, ...
# via filter_complex concat
ffmpeg -i seg-001.mp3 ... -i silence_3s.mp3 ... -filter_complex "[0:a][1:a]...concat=n=N:v=0:a=1[out]" -map "[out]" output.mp3
```

## API Key Safety

**NEVER** hardcode `rsk_*` key in:
- `write_file()` — the system redaction replaces it with `***` inline, corrupting the code
- `execute_code()` — same issue

**Always** read from config:
```python
with open("path/to/settings.json") as f:
    cfg = json.load(f)
API_KEY = cfg["resona_api_key"]  # Safe — reads at runtime
```

Then create batch scripts via `sed` from a proven template:
```bash
sed 's/if 1 <= s\["id"\] <= 8:/if 9 <= s["id"] <= 16:/' template.py > new_batch.py
python new_batch.py
```

## Polling Response Format

```json
{
  "status": "completed",
  "audio_urls": ["https://storage.googleapis.com/..."],  // ARRAY, not string!
  "progress": 100
}
```

Key: `audio_urls` is an **array**. Never check `audio_url` (string) — it doesn't exist in the response.
