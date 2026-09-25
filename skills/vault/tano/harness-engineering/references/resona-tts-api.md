# Resona TTS API Reference

Base URL: `https://resona.live`
Auth: `Authorization: Bearer <rsk_...>` (tạo từ Settings → Access Token)
Python: cần `User-Agent` header để tránh Cloudflare 403

## Endpoints

### GET /api/v1/voices
List available voices. Query params: gender, category, sort, page_size, voice_ids.
Returns `{voices: [{voice_id, name, accent, usage_count, ...}], has_more, total_count}`

### POST /api/v1/generate-speech (async)
Submit TTS job. Body:
```json
{
  "text": "Speaker 1: Xinchao...",
  "voice_ids": ["dwK3JbXXe2LLisf6Tfx6"],
  "language": "vi",
  "speed": 1.0
}
```
Response: `{request_id, status: "processing", usage: {requiredCredits, charCount}}`

### GET /api/v1/generate-speech/{request_id}/status
Poll job status. Returns `{status: "completed"|"processing"|"failed", audio_url, ...}`

## Format rules
- Mỗi dòng text **phải bắt đầu bằng "Speaker N:"** (vd: "Speaker 1: Nội dung...")
- Cho single-speaker narration: prefix mỗi dòng với "Speaker 1:"
- Text tối thiểu 50 credits (~50 ký tự)
- Credit = charCount của text

## Giọng có sẵn (top usage)
| Tên | Accent | Voice ID |
|-----|--------|----------|
| Huy Thông | miền bắc | VHISRfUSyorItepwgtVI |
| Minh Tuấn | miền nam | dwK3JbXXe2LLisf6Tfx6 |
| Trung Thành | miền bắc | 6SLyzXlPxiBrgjKOuELG |
| Gia Huy | miền bắc | USYTYBI33ONlIoLQwm6d |

## Implementation pattern (Python)
```python
import requests

class ResonaTTS:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ResonaTTS/1.0",  # Required to avoid Cloudflare 403
        })

    def submit_job(self, text, voice_ids, language="vi", speed=1.0):
        formatted = "\n".join(
            f"Speaker 1: {l}" for l in text.split("\n") if l.strip()
            if not l.startswith("Speaker ")
        )
        resp = self.session.post(
            "https://resona.live/api/v1/generate-speech",
            json={"text": formatted, "voice_ids": voice_ids, "language": language, "speed": speed},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()  # {request_id, status, usage}

    def poll_job(self, request_id, max_retries=30, interval=2):
        for _ in range(max_retries):
            resp = self.session.get(
                f"https://resona.live/api/v1/generate-speech/{request_id}/status",
                timeout=15,
            )
            data = resp.json()
            if data.get("status") == "completed":
                return data
            time.sleep(interval)
        raise TimeoutError(f"Job {request_id} not completed")
```

## Pricing
- Starter 2x: 17K/tháng ~ 5h40p audio
- Creator 3x: 23K/tháng ~ 8h30p audio
- Free tier: ❌ không có API
