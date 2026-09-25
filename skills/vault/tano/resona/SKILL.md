---
name: resona
description: "Resona TTS — giọng tiếng Việt chất lượng cao. V1 (deprecated) và V2 API endpoints."
---

# Resona — TTS & Lồng Tiếng Video AI Tiếng Việt

## TL;DR
Resona (resona.live) là startup VN làm TTS tiếng Việt chất lượng cao + lồng tiếng video.

### 🗣️ Giọng nói ưu tiên (GMSP — updated Jul 2026)

GMSP dùng 4 giọng, mỗi bài chọn 1 giọng phù hợp:

| Giọng | ID | Giới | Vùng | Style | Dùng cho |
|-------|-----|:----:|:----:|-------|----------|
| **Trung Thành** ⭐ | `6SLyzXlPxiBrgjKOuELG` | Nam | Bắc | Tin tức | **Phát triển bản thân** — chính, triết lý, trầm sâu |
| **Vân Anh** | `ODDT6PXH9Eb43SpMXZda` | Nữ | Bắc | Chia sẻ | **PTBT tâm sự** — nhẹ nhàng, kể chuyện |
| **Minh Đức** | `tak3IN3asjyDvk2dC3iR` | Nam | Bắc | Chia sẻ | **Bí kíp cổ kim** — ấm áp, gần gũi |
| **Tuấn Tú** | `C3tEh3RaFrM9GXzy3lGJ` | Nam | Bắc | Sách nói | **Tử vi, tâm linh** — huyền bí, chậm rãi |

Speed mặc định: **0.9** (cân bằng giữa trầm và tốc độ). Dùng pitch 0.85-1.15 cho emotion.

Top voices khác nếu cần: Minh Tuấn (miền nam, tin tức), Thanh Tùng (miền nam, chia sẻ), Huy Thông (miền bắc, tin tức), Mai Thương (nữ, tin tức).

**API Key**: Cần lưu `RESONA_API_KEY=rsk_...` trong `~/.hermes/.env` (Hệ thống sẽ tự redact key trong output).
- **Giá**: Starter 17K/tháng, Creator 23K/tháng (có API)
- **API Base**: `https://resona.live`
- **Cơ chế**: **Async job** — submit → nhận request_id → poll status → download
- **⚠️ Text format (v1)**: *Chỉ v1 mới cần* — mỗi dòng phải bắt đầu bằng "Speaker N:". **V2 dùng text thuần**, không cần prefix.
- **Voice ID**: UUID (vd: `dwK3JbXXe2LLisf6Tfx6` = Minh Tuấn miền Nam)
- **Auth**: Bearer token `rsk_...` (Firebase Custom Token, không có scope)

## API Endpoints (v1 — deprecated July 2026)

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/api/v1/voices` | GET | Liệt kê giọng nói (lọc gender, sort, page) |
| `/api/v1/generate-speech` | POST | **TTS async** — nhận `text` (Speaker N: prefix), trả về `request_id` → poll status |
| `/api/v1/generate-speech/{request_id}/status` | GET | Poll job status → `"completed"` + `audio_url` |
| `/api/v1/generate-text` | POST | Tạo hội thoại multi-speaker |

**Base URL**: `https://resona.live`
**Auth**: `Authorization: Bearer rsk_...` (Bearer trực tiếp, Firebase Custom Token)
**⚠️ Token**: Khi tạo từ Cài đặt chỉ có 2 trường (Tên + Hết hạn) — **không có scope/permission**

## API Endpoints (v2 — current as of July 2026)

> Resona đã nâng cấp lên v2. Endpoint base là `https://resona.live` (không có `api.` prefix).
> **⚠️ Quan trọng**: Key v1 (`rsk_...`) KHÔNG hoạt động với v2 endpoint — trả về `401 invalid_token` hoặc `403 insufficient_scope`. Phải tạo **token mới** trên dashboard Resona (trang Khóa API) để dùng v2.

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/api/v2/voices` | GET | Liệt kê/tìm giọng nói (public + đã clone), hỗ trợ filter gender, category, sort, phân trang |
| `/api/v2/generate-text` | POST | Tạo hội thoại nhiều người nói từ prompt (params: `prompt`, `speaker_profiles`, `temperature`, `style`...) |
| `/api/v2/text-to-speech` | POST | **TTS async 1 giọng** — cần `text` và `voice_id`, trả về `request_id` |
| `/api/v2/text-to-speech/:request_id` | GET | ❌ **Broken (returns 404)** — use `/api/v1/generate-speech/{id}/status` instead |
| `/api/v2/text-to-dialogue` | POST | Tạo audio hội thoại nhiều giọng từ mảng `turn` (mỗi turn có `text` + `voice_id` riêng) |
| `/api/v2/text-to-dialogue/:request_id` | GET | Poll trạng thái/lấy kết quả audio dialogue |

**Lưu ý credit**: Mỗi request tốn 50–2000 credit (~1 credit ≈ 1 ký tự).

**Base URL**: `https://resona.live`
**Auth**: `Authorization: Bearer rsk_...` (token v2, created from Khóa API page)

### Curl examples (v1)
```bash
# Liệt kê giọng
curl "https://resona.live/api/v1/voices?gender=male&sort=usage_count&page_size=5" \
  -H "Authorization: Bearer rsk_..."

# TTS — lưu ý "Speaker N:" prefix + voice_ids (plural, array)
# Bước 1: Submit job
curl -X POST "https://resona.live/api/v1/generate-speech" \
  -H "Authorization: Bearer rsk_..." \
  -H "Content-Type: application/json" \
  -d '{"text":"Speaker 1: Nội dung cần đọc. Speaker 1: Tiếp tục nội dung.","voice_ids":["dwK3JbXXe2LLisf6Tfx6"],"language":"vi","speed":1.0}'
# Response: {"request_id":"...","status":"processing","usage":{...}}

# Bước 2: Poll job status
curl "https://resona.live/api/v1/generate-speech/{request_id}/status" \
  -H "Authorization: Bearer rsk_..."
```

### Python client (v1, requests required — urllib bị Cloudflare chặn 403)
```python
import requests, time

def resona_generate_v1(api_key, text, voice_id="dwK3JbXXe2LLisf6Tfx6", lang="vi"):
    """Submit TTS job + poll until done (v1 endpoint)."""
    resp = requests.post(
        "https://resona.live/api/v1/generate-speech",
        headers={"Authorization": f"Bearer {api_key}", "User-Agent": "Mozilla/5.0"},
        json={"text": text, "voice_ids": [voice_id], "language": lang, "speed": 1.0},
    )
    result = resp.json()
    request_id = result["request_id"]
    
    for _ in range(30):
        status_resp = requests.get(
            f"https://resona.live/api/v1/generate-speech/{request_id}/status",
            headers={"Authorization": f"Bearer {api_key}", "User-Agent": "Mozilla/5.0"},
        )
        if status_resp.status_code == 404:
            print(f"⚠️ Job {request_id} expired (not found)")
            break
        status = status_resp.json()
        if status.get("status") == "completed":
            urls = status.get("audio_urls", []) or [status.get("audio_url", "")]
            return urls[0] if urls else None
        time.sleep(2)
    return None

# Usage
key = os.environ.get("RESONA_API_KEY")
text = "Speaker 1: Xin chào các bạn. Speaker 1: Đây là video hôm nay."
audio_url = resona_generate_v1(key, text)
if audio_url:
    aud = requests.get(audio_url, timeout=60)
    with open("voiceover.mp3", "wb") as f:
        f.write(aud.content)
```

## Emotion Mapping — Speed + Pitch Per Segment

Resona v2 supports **per-segment speed AND pitch** for expressive voiceovers. This creates natural lên/xuống/cao trào (rise/fall/climax).

**Confirmed working parameters (tested July 2026):**
- `pitch` values: 0.6 to 1.5 accepted (tested 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15 — all worked)
- `speed` values: 0.8 to 2.0 (tested 0.8, 0.85, 0.9, 0.95, 1.0)
- Invalid params return 422 with error message (not silently dropped)
- Pass both `speed` AND `pitch` in same request to combine effects

**⚠️ Per-segment pitch trumps overall speed:** Pitch and speed are independent parameters. You can have fast + high (speed=1.0, pitch=1.15) or slow + deep (speed=0.8, pitch=0.85). Experiment with combinations.

**Emotion profile for narrated video (tested and confirmed working):**

| Segment | Speed | Pitch | Effect |
|---------|-------|-------|--------|
| Hook (mở bài) | 0.85  | 0.9   | Slow, deep → attention grabbing |
| Setting (dẫn) | 0.9   | 1.0   | Normal flow |
| Transition | 0.95  | 1.05  | Slightly faster → builds momentum |
| Trap (kịch tính) | 0.85  | 0.9   | Slow + deep → creates pressure |
| Solution 1 | 1.0   | 1.1   | Fast + bright → hope |
| Story (kể) | 0.85  | 0.95  | Slow, narrative → familiar tone |
| Climax  | 1.0   | **1.15** | **Fastest + highest → maximum impact** 🔥 |
| Ending | 0.8   | 0.85  | Very slow, deep → lingers in memory |

**⚠️ CRITICAL — Poll immediately after submit:**
Request IDs have a **very short TTL** (under 60s). After all jobs are submitted, poll each ONE AT A TIME immediately. Do NOT batch-submit-all-then-batch-poll — by the time you finish submitting, the first request IDs will already return `404 Request not found`.

**Correct pattern:**
```python
# Submit ALL first (fast, no waiting)
jobs = []
for text in segments:
    r = session.post(API, json={...})
    rid = r.json().get("request_id", "")
    if rid:
        jobs.append((idx, rid))

# Then poll each IMMEDIATELY — one at a time, no delay between
for idx, rid in jobs:
    for _ in range(45):  # 45 * 3s = 135s max per job
        time.sleep(3)
        r = session.get(f"{POLL}/{rid}/status")
        d = r.json()
        # v1 status response uses audio_urls ARRAY, not audio_url string!
        urls = d.get("audio_urls", [])
        url = urls[0] if urls else ""
        if url:
            download(url)
            break
```

**Feedback-driven parameters:**
- Trung Thành Quân Sư style: speed 0.85-0.9, pitch 0.85-1.0
- For dramatic emphasis: `{"speed": 1.0, "pitch": 1.15}` — fastest + highest
- For deep conclusion: `{"speed": 0.8, "pitch": 0.85}` — slowest + deepest

If segment fails with `status: "failed"` at emotion speed/pitch, fall back to default (speed 0.9, pitch 1.0) or split text shorter.

## Batch Workflow (Recommended)

For full episode scripts (10+ segments), use the **submit-all → poll-immediately** pattern above. See `references/v2-hybrid-pattern.md` for full implementation with Python code.

## Dramatic Post-Processing

After generating clean TTS audio, apply **volume automation + reverb** with FFmpeg for dramatic lên/xuống/cao trào. See `references/dramatic-post-processing.md` for exact commands and profiles.

## Batch Production Workflow (Full Episode, Jul 2026)

For a full 10-12 minute episode (~30-34 TTS segments at speed 0.82):

```text
1. Write scipt → extract clean voiceover text (strip [SECTION] markers, metadata)
2. Split into segments of ~200-350 chars each (save to segments.json)
3. Generate TTS at speed 0.82 (validated for ~10min episodes)
4. Add 3s silence gaps between major sections
5. FFmpeg concat everything → final voiceover_full.mp3
```

### Section Gap Concat Workflow

Sections (HOOK → BỐI CẢNH → TỬ VI → TÂM LÝ → GIẢI PHÁP → CLIFFHANGER) need 3s silence between them for natural pacing.

```python
# Generate 3s silence
# ffmpeg -f lavfi -i anullsrc=cl=mono:r=24000 -t 3 -q:a 2 silence_3s.mp3

# Build input list with silence MP3 interleaved between sections
sections = [(1,3), (4,8), (9,14), (15,22), (23,30), (31,34)]
inputs = []
for si, (start, end) in enumerate(sections):
    for i in range(start, end + 1):
        inputs.append(f"-i seg-{i:03d}.mp3")
    if si < len(sections) - 1:
        inputs.append("-i silence_3s.mp3")

# filter_complex concat
filter_str = "".join(f"[{i}:a]" for i in range(n_inputs)) + f"concat=n={n_inputs}:v=0:a=1[out]"
ffmpeg_cmd = f"ffmpeg {' '.join(inputs)} -filter_complex \"{filter_str}\" -map \"[out]\" -c:a libmp3lame -q:a 2 voiceover_full.mp3 -y"
```

### Speed 0.82 vs 0.9 timing reference

| Speed | ~8000 chars | ~8800 chars |
|-------|-------------|-------------|
| 0.9   | ~8:30       | ~9:30       |
| 0.82  | ~9:30       | ~10:30      |
| 0.78  | ~10:00      | ~11:00      |

For a 10-12 minute episode target with ~8800 chars of script, use **speed 0.82** + 3s section gaps.

## Pitfalls
- **⚠️ Write_file corrupts API key in Python scripts**: When writing scripts that use `cfg["resona_api_key"]`, the `write_file` tool redacts the key value inline, corrupting the Python syntax. **Workaround:** write a working template FIRST (via `write_file`), then use `sed` to modify segment ranges:
  ```bash
  # WRONG (corrupts): write_file → batch.py
  # RIGHT (works):
  sed 's/if 1 <= s["id"] <= 8:/if 9 <= s["id"] <= 16:/' template.py > batch_09_16.py
  python batch_09_16.py
  ```
  The key loads from `cfg["resona_api_key"]` at runtime, so the template only needs the config-read pattern, not the actual key value.

- **⚠️ Script parser must handle Unicode dashes**: When parsing script text into segments, metadata lines often start with `[` and contain dashes like `[00] HOOK — CÂU NÓI THẬT`. The em dash `—` (U+2014) and en dash `–` (U+2013) are NOT matched by a plain `-` (hyphen, U+002D) check in Python. Filter properly:
  ```python
  # WRONG: misses em/en dashes
  if s.startswith("[") and ("-" in s or s.endswith("]")):
      continue
  # RIGHT: catches all Unicode dashes
  if s.startswith("[") and any(c in s for c in ["-", "—", "–"]):
      continue
  # BEST: skip all lines starting with [ — simplest, catches everything
  if s.startswith("["):
      continue
  ```
  Uncaught metadata lines cause TTS to read garbage like "mở ngoặc vuông không không hook câu nói thật". This is a common issue with Vietnamese scripts that use `—` in headers.
- **⚠️ Text patterns causing silent failures**: Resona v2 fails silently on these Vietnamese text patterns:
  - Double quotes `"..."` (e.g. `"Chờ đủ tiền rồi tính."`) — remove quotes or use single quotes
  - Em dashes `—` (long dash) — replace with space or regular dash `-`
  - `phần trăm` — causes `status: "failed"`. Replace with `%` or write as `phan tram` (no diacritics)
  - General rule: clean ALL non-standard punctuation before submitting. If a segment fails repeatedly, split into 3-4 shorter parts and generate separately, then merge audio.
- **⚠️ Credit limit exhaustion**: After ~10-12 successful jobs (or ~4000-5000 credits), Resona may reject subsequent requests with `section_credit_limit_exceeded`. Workaround: prioritize critical segments (hook, key traps) first so they complete before the limit hits, or wait ~1 hour.
- **⚠️ Retry strategy for failed segments**: 1) Clean text of quotes/dashes/special chars. 2) Submit just the first sentence (50-80 chars) to verify connection. 3) If ok, split original text into 2-3 shorter parts and submit each. 4) Concatenate with FFmpeg. 5) If short text also fails → key hitting credit limits → Edge TTS fallback.
- **⚠️ Key v1 không dùng được v2**: Key `rsk_...` tạo trước khi v2 ra mắt chỉ có quyền v1. Gọi `/api/v2/*` với key cũ → `401 invalid_token`. Phải regenerate key từ dashboard Resona (trang Khóa API).
- **⚠️ V2 /status endpoint broken**: `/api/v2/text-to-speech/{id}/status` returns 404. Use `/api/v1/generate-speech/{id}/status` instead — it still works for v2-submitted jobs.
- **⚠️ Text "phần trăm" causes silent failures**: Jobs with this exact Vietnamese phrase can fail with `status: "failed"`. Replace with `%` or `phần tram` or avoid entirely by writing numeric (e.g. `70 phần trăm` -> `70%`).
- **⚠️ Vietnamese diacritics required**: Text lacking diacritics (e.g. `tuoi` vs `tuổi`) can trigger CER threshold errors at slow speeds. Always use proper Vietnamese with full diacritics.
- **⚠️ Text with double quotes or em dashes**: Double quotes `"..."` and long dashes `—` inside the text payload can cause silent failures. Clean these from text before submitting.
- **⚠️ Slow speed increases poll time**: Speed 0.85 takes ~10-12 polls vs 7-9 at speed 1.0. Speed 0.9 is a good middle ground for philosophical narration - still deep but faster generation.
- ⚠️ "Speaker N:" prefix (v1 only): Chỉ endpoint v1 (/api/v1/generate-speech) mới yêu cầu prefix này. V2 (/api/v2/text-to-speech) dùng text thuần — gửi nguyên văn, không cần thêm gì.
- **⚠️ Language field**: Luôn gửi `"language": "vi"` cho tiếng Việt
- **⚠️ Cơ chế async**: Response trả về `request_id` + `"status":"processing"`, **không có audio_url ngay** — cần poll
- **⚠️ Cloudflare chặn Python urllib**: HTTP 403 code 1010. Dùng `requests` với `User-Agent: Mozilla/5.0` hoặc curl
- **⚠️ Minimum text length**: 50 credits (~50-60 ký tự). Text ngắn hơn → 400 error
- **⚠️ 2000-credit limit per job**: Text trên 2000 credits → 400 error `Section text exceeds the 2000-credit limit`. Phải chunk text thành các phần ~1800 chars mỗi chunk, submit riêng, sau merge audio bằng FFmpeg concat filter.
- **⚠️ Generation time**: ~55-65s cho 1800 chars (poll mỗi 2s, cần 25-35 polls). Job có TTL cực ngắn — **phải poll ngay sau khi submit**, ko delay. Submit all → poll từng cái ngay lập tức.
- **⚠️ Poll interval**: Dùng 2-3s intervals. KHÔNG đợi lâu giữa các job — request ID sẽ expire.
- **⚠️ Request ID TTL ~60s**: Submit ALL jobs first (batch submit, ~2s each), THEN poll each one immediately. Do NOT submit-1→poll-1→submit-2→poll-2 — the API's internal queue has very short TTL. Observed behavior: request IDs return `404 Request not found` when polled >60s after submission, even though the job was accepted. If you see this, resubmit with fresh request ID.
- **⚠️ Max 5000 characters per request**: Text exceeding 5000 characters returns `validation_error` with `text exceeds maximum length of 5000 characters`. Split long scripts into segments <5000 chars, submit each separately, then merge audio with FFmpeg concat.
- **⚠️ Response field**: Khi completed, `audio_urls` là **array of strings**, không phải string. Dùng `rj.get('audio_urls', [])[0]` để lấy URL
- **⚠️ Token là Firebase Custom Token**: Token `rsk_...` (prefix rsk_ + 32 hex chars = 36 chars total) không có scope — tất cả endpoint dùng chung.
- **⚠️ Key expiry behavior**: Key có thể bị invalidate giữa chừng. Symptom: `GET /api/v1/voices` vẫn trả về 200 OK, nhưng `POST /api/v1/generate-speech` trả về **401 "Invalid token"**. Giải pháp: regenerate key từ Settings → Tạo mã thông báo mới. Key cũ không revive được.
- **⚠️ Key storage**: Lưu trong `~/.hermes/.env` dưới dạng `RESONA_API_KEY=rsk_...`. Hệ thống auto-redact key trong tool outputs.
- **Price tiers**: Starter 17K/tháng, Creator 23K/tháng. Free tier không có API
- **Speed range**: 0.8-2.0

## Vị trí trong pipeline video
```text
Script → Resona TTS → voiceover.mp3
  ↓
HyperFrames → slides.mp4
  ↓
FFmpeg ghép → final.mp4
  ↓
Upload TikTok/YouTube Shorts
```

## Link
- Web: https://resona.live
- API docs: https://resona.live/vi/docs/api-reference
- Pricing: https://resona.live/vi/pricing
