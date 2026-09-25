# FAL Image/Video Gen on Windows — Integration Notes

## DNS quirk: `queue.fal.ai` vs `fal.run`

On this Win10 host, `queue.fal.ai` fails with `[Errno 11001] getaddrinfo failed`.
Use `fal.run` for sync POST calls instead.

**Sync pattern (no polling needed):**

```python
url = f"https://fal.run/{endpoint}"
req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
resp = urllib.request.urlopen(req, timeout=60)
return json.loads(resp.read())
```

## Common models

| Model ID | Purpose | Cost |
|----------|---------|------|
| `fal-ai/flux/schnell` | Quick image gen, 4 steps | Rẻ |
| `fal-ai/flux-dev` | Higher quality, 25 steps | Medium |
| `fal-ai/flux-realism` | Photorealistic | Cao |
| `fal-ai/ltx-video` | Short video 3s, 25 frames | Video |
| `fal-ai/minimax-video` | 5s 720p video | Video |

## FAL Key Troubleshooting

- FAL keys from dashboard.fal.ai may return "No user found for Key ID and Secret" even when valid
- Hermes' internal `image_gen` tool works via Nous subscription backend regardless
- If your Python script gets 401, but Hermes tool works → use the Hermes tool, don't block on the key

## File: `dashboard/image_gen.py`

Import in both `app.py` and `main.py`:
```python
from dashboard.image_gen import generate_image, generate_video, PHOTO_MODELS, VIDEO_MODELS
```
