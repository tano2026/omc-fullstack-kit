# Resona TTS — Parallel Batch Generation

## API Flow (Hybrid v2 Submit + v1 Poll)

Resona v2 API was updated in 2026. v1 is deprecated for submission but its **status endpoint still works** and is the only reliable way to poll job completion.

```
# Submit via v2
POST /api/v2/text-to-speech    → 200 { request_id, status: "processing", usage: { required_credits: N } }

# Poll via v1 (v2 status endpoint returns 404!)
GET  /api/v1/generate-speech/{id}/status → 200 { status: "completed", audio_url: "...", audio_urls: [...] }
# Fallback: v2 GET also works for status (no /status suffix)
GET  /api/v2/text-to-speech/{id}         → 200 { status: "completed", audio_url: "..." }

GET  <audio_url>                → binary .mp3
```

## Important v2→v1 Differences

| Parameter | v1 (old) | v2 (current — use for submit) |
|-----------|----------|-------------------------------|
| Submit endpoint | `/api/v1/generate-speech` | `/api/v2/text-to-speech` |
| Voice ID field | `voice_ids` (array) | `voice_id` (singular string) |
| Text prefix | Must start with `"Speaker 1:"` | No prefix needed (plain text) |
| Status endpoint | `/api/v1/generate-speech/{id}/status` (WORKS) | `/api/v2/text-to-speech/{id}/status` (404!) |
| Get job | N/A | `/api/v2/text-to-speech/{id}` (works, no `/status`) |

## Key Parameters (v2 submit)

- **Base URL:** `https://resona.live`
- **Auth:** `Authorization: Bearer rsk_...` (Firebase Custom Token)
- **Text:** Plain Vietnamese text with full diacritics. No `Speaker N:` prefix needed.
- **Language:** `"vi"` for Vietnamese
- **Voice ID:** Singular string `"6SLyzXlPxiBrgjKOuELG"`, NOT array
- **Speed:** 0.8–2.0 range (0.85 recommended for philosophical/deep narration)
- **Poll interval:** 2 seconds
- **User-Agent:** Must use `"Mozilla/5.0"` — urllib gets blocked by Cloudflare (403 code 1010)

## Text Constraints (v2)

⚠️ **Resona v2 can FAIL on certain text patterns.** Symptoms: job status returns `"failed"` after 20-30 seconds. Known problematic patterns:

| Pattern | Example | Fix |
|---------|---------|-----|
| Quoted text | `"Chờ đủ tiền rồi tính"` | Remove quotes: `Chờ đủ tiền rồi tính` |
| Parentheses | `(đã kiểm chứng)` | Remove parentheses: `đã kiểm chứng` |
| `%` character | `100%`, `60-70%` | Spell out: `100 phần trăm`, `sáu bảy chục phần trăm` |
| Long dash `—` | `không đau — nên bạn` | Replace with `. ` or `, ` |

**Text cleanup before submission:**

```python
def clean_resona_text(text: str) -> str:
    text = text.replace('"', '').replace('"', '').replace('"', '')
    text = text.replace('(', '').replace(')', '')
    text = text.replace('—', ', ')
    text = text.replace('%', ' phần trăm')
    text = text.replace('“', '').replace('”', '')
    return text.strip()
```

## Batch Pattern (v2 submit → v1 poll)

```python
import requests, time

API_KEY = "rsk_..."
BASE_URL = "https://resona.live"
VOICE_ID = "6SLyzXlPxiBrgjKOuELG"  # Trung Thành (miền bắc, trầm)
SPEED = 0.9  # 0.85 for short segments, 0.9 for long-form (recommended)

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
})

# Phase 1: Submit ALL jobs (faster than sequential)
jobs = []
for i, text in enumerate(texts):
    r = session.post(
        f"{BASE_URL}/api/v2/text-to-speech",
        json={"voice_id": VOICE_ID, "text": clean_resona_text(text),
              "speed": SPEED, "language": "vi"},
        timeout=30,
    )
    d = r.json()
    rid = d.get("request_id", "")
    if rid:
        jobs.append({"idx": i, "request_id": rid})

# Phase 2: Poll each job via v1 status endpoint
for job in jobs:
    rid = job["request_id"]
    for _ in range(30):
        r = session.get(f"{BASE_URL}/api/v1/generate-speech/{rid}/status", timeout=15)
        d = r.json()
        if d.get("status") == "completed":
            url = d.get("audio_url", "") or (d.get("audio_urls", [""])[0] if d.get("audio_urls") else "")
            if url:
                dl = requests.get(url, timeout=60)
                with open(f"seg-{job['idx']+1:03d}.mp3", "wb") as f:
                    f.write(dl.content)
            break
        elif d.get("status") == "failed":
            break
        time.sleep(2)
```

## Voice Catalog (GMSP-verified)

| Name | ID | Accent | Style |
|------|----|--------|-------|
| Trung Thành | `6SLyzXlPxiBrgjKOuELG` | miền bắc | Trầm, sâu, phù hợp triết lý — ⭐ MẶC ĐỊNH |
| Minh Tuấn | `dwK3JbXXe2LLisf6Tfx6` | miền nam | Ấm áp, gần gũi (cũ mặc định) |
| Huy Thông | `VHISRfUSyorItepwgtVI` | miền bắc | Sáng, rõ ràng |
| Gia Huy | `USYTYBI33ONlIoLQwm6d` | miền bắc | Trung tính |

**Default voice:** Trung Thành @ speed 0.85 for philosophical/self-development content. Switch to Minh Tuấn @ 1.0 for lighter topics.

## Updated Speed Recommendations (2026-07-10)

After testing with ~5,000-char scripts:
- **Trung Thành @ 0.85:** Too slow for long scripts. Good for short (< 1,000 char) segments.
- **Trung Thành @ 0.9:** Sweet spot for philosophical/deep narration. ~90s per 1K chars. 5K chars ≈ 15 min total.
- **Trung Thành @ 1.0:** Good for lighter self-development topics. ~75s per 1K chars.

Use 0.9 as the default for Trung Thành on long-form (10+ min) content.

## Pitfalls (updated)

1. **Key expiry:** Token can be invalidated mid-session. Symptom: GET /voices returns 200, POST returns `invalid_token`. Fix: regenerate key from Resona dashboard.
2. **Job expiry:** Jobs have a short TTL (~30-60s without polling). Must poll every 2s with proper interval.
3. **Cloudflare:** Python's urllib gets HTTP 403 (code 1010). Use `requests` with `User-Agent: Mozilla/5.0`.
4. **Minimum chars:** ~50 credits minimum. Shorter text → `credit_limit_exceeded` error.
5. **Text constraint — CRITICAL:** Remove quotes (including smart quotes `"` `"`), parentheses, `%`, and long dashes before submitting — these cause silent job failure (`status: "failed"` after 20-30s with no useful error message). The user's scripts frequently contain quoted dialogue (`"Chờ đủ tiền rồi tính"`) — this is a common failure source. Always run `clean_resona_text()` before submission.
6. **Response field:** `audio_urls` is an array, not a string. Access via `d.get('audio_urls', [])[0]`.
7. **Voice ID field name (v2):** `"voice_id"` (singular string), NOT `"voice_ids"` (array).
8. **No Speaker prefix:** v2 does NOT require `Speaker 1:` prefix.
9. **Status endpoint:** Use v1 for polling (`/api/v1/generate-speech/{id}/status`). v2 status endpoint returns 404.
10. **Key storage:** Store in `~/.hermes/.env` as `RESONA_API_KEY=rsk_...`. Script should check env var first, then .env file, then `config/settings.json`.
11. **Generation time:** ~20-30s for 300 chars, ~55-65s for 1800 chars. Scales roughly linearly.
