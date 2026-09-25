# Resona TTS — API Dead (Jul 2026)

## Status
`api.resona.live` — DNS **fails to resolve** (getaddrinfo error). Web at `resona.dev` has pivoted to real-time speech-to-speech API, no longer offers text-to-speech endpoint.

## History
- API was active 2025 → mid-2026
- Old endpoint: `POST /api/v2/text-to-speech` → `{request_id}`, poll `GET /api/v1/generate-speech/{id}/status`
- Old voice IDs: Trung Thành = `6SLyzXlPxiBrgjKOuELG`
- Old key kept at `config/settings.json` under `resona_api_key` — **unusable now**
- User previously pasted sections manually via Resona web dashboard for quality

## Alternative
- **Edge TTS** (free, auto): `edge-tts --voice vi-VN-NamMinhNeural --rate=+16%`
  - Pitch variation via `--rate`: `+8%` trầm, `+16%` normal, `+25%` cao trào
  - NamMinhNeural = closest Vietnamese male voice to Trung Thành
  - Quality: 7.5/10 vs Resona's 8.5/10 — acceptable for GMSP content
