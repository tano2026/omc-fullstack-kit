# Resona API v2 — Discovery Notes (July 2026)

## Timeline
- User provided key `rsk_0218f70207175288dfce5da1de9f4988`
- Tried `https://api.resona.live` → `Could not resolve host`
- User confirmed base URL is `https://resona.live` (no `api.` prefix)
- User provided full v2 API reference from `/en/docs/api-reference`

## Key Discovery: v1 Keys Don't Work with v2

Key created for v1 returns `401 invalid_token` when calling `/api/v2/voices`:
```json
{"detail":{"status":"invalid_token","message":"The provided token is invalid or has expired."}}
```

This means:
1. Resona has two API versions running simultaneously
2. v1 keys (`rsk_...`) are scoped to v1 only
3. To use v2, user must create a **new token** from the dashboard (Khóa API page)
4. The key prefix doesn't change — still `rsk_...` — but it's scoped differently

## Configuration in settings.json
```json
"resona_api_key": "rsk_0218f70207175288dfce5da1de9f4988",
"resona_api_url": "https://resona.live/api/v2/text-to-speech"
```

Note: `resona_api_url` points to the **submit** endpoint, not the base URL. The pipeline client appends path components for polling (e.g., `/{request_id}`).

## Available Endpoints (v2)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v2/voices` | GET | List/filter voices |
| `/api/v2/generate-text` | POST | Multi-speaker from prompt |
| `/api/v2/text-to-speech` | POST | Single voice TTS (async) |
| `/api/v2/text-to-speech/:request_id` | GET | Poll TTS status/result |
| `/api/v2/text-to-dialogue` | POST | Multi-speaker dialogue TTS (async) |
| `/api/v2/text-to-dialogue/:request_id` | GET | Poll dialogue status/result |

## Key Differences from v1
- v2 uses `voice_id` (singular) vs v1's `voice_ids` (plural array)
- v2 has dedicated `/text-to-speech` endpoint vs v1's `/generate-speech`
- v2 has `/text-to-dialogue` for multi-speaker (v1 required manual speaker prefixes)
- Credit cost: 50–2000 credits per request (~1 char ≈ 1 credit)
