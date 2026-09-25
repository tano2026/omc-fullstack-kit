## TTS Decision Log (Jul 2026)

| Provider | Kết quả | Lý do |
|----------|---------|-------|
| ElevenLabs | ❌ Bỏ | Key restricted (sk_5ecd... thiếu text_to_speech permission), yêu cầu paid plan |
| Kokoro | ❌ Bỏ | pip install fail trên Windows (spacy dependency build lỗi) |
| Resona | ❌ Bỏ | api.resona.live DNS NXDOMAIN — công ty pivoted sang real-time speech agents |
| **Edge TTS** | **✅ Dùng** | Free, $0, không cần API key, giọng AndrewNeural (male, warm, confident), chạy local an toàn |

**Edge TTS command:**
```bash
edge-tts --voice en-US-AndrewNeural --text "script here" --write-media assets/vo.mp3
```
Auto-detect trong Media adapter: nếu text có ký tự VN (unicode > 0x1FFF) → dùng vi-VN-NamMinhNeural. English → AndrewNeural.
