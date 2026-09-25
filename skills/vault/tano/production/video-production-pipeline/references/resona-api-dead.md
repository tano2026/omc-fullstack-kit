# Resona TTS API — Dead (July 2026)

## Investigation

1. `api.resona.live` — DNS NXDOMAIN (confirmed via nslookup, ping, curl)
2. `resona.dev` — website is live, but **completely rebranded** to real-time speech-to-speech (voice agents)
3. No mention of text-to-speech REST API anywhere on `resona.dev`
4. No docs page (docs.resona.dev/docs returns 404, /documentation returns 404)
5. The product now has:
   - Real-time voice agents (WebRTC/WebSocket)
   - Voice cloning
   - Telephony (SIP)
   - **No text-to-speech endpoint**

## Timeline

- **July 15, 2026:** First DNS failure observed during EP01 TTS generation
- **July 16, 2026:** Confirmed DNS dead — `getaddrinfo failed` for `api.resona.live`
- The transition appears to have happened ~July 10-14, 2026

## Current Options

| Option | Cost | Quality | Auto? | Notes |
|--------|:----:|:-------:|:-----:|-------|
| Edge TTS (`NamMinhNeural`) | Free | 7/10 | ✅ | Timeout on scripts >5K chars |
| Resona Web (manual) | Paid (user's credit) | 8.5/10 | ❌ | Works if user has session |
| ElevenLabs | ~$5/mo | 9/10 | ✅ | API still active |
| Fish Audio | Free tier | 7/10 | ✅ | Open source option |

## Resona key

User still has a Resona API key (`rsk_10be95...`) which was valid before the transition. The key is now useless for TTS since the endpoint doesn't exist.
