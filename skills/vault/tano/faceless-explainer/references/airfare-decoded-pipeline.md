# Airfare Decoded — Non-HeyGen English Explainers

## Khi nào dùng pipeline này
- Kênh YouTube **tiếng Anh** (faceless explainer)
- Không có HeyGen / ElevenLabs / Kokoro (hoặc free tiers bị hạn chế)
- Muốn **$0** hoàn toàn — Edge TTS + Pollinations + HyperFrames CLI

## ⚠️ BẮT BUỘC: Quyết định format TRƯỚC khi làm bất cứ gì

Form factor quyết định script length, figure count, scene timing. **Không gen gì cho tới khi chốt format.**

| Format | Target Duration | Script Length | Scene Count | Use Case |
|--------|----------------|---------------|-------------|----------|
| **Shorts / TikTok** | 15-60s | ~100-200 từ | 4-5 scenes | Daily content, build subs |
| **YouTube video** | 5-8 phút | ~800-1500 từ | 8-12 scenes | Weekly deep dives, affiliate |

⚠️ **135s (2:15) là no man's land** — quá dài cho Shorts, quá ngắn cho YouTube. Không bao giờ làm video 2 phút.

Khi đã chọn format:
- **Shorts** → dùng 6 scene archetypes bên dưới, timing mỗi scene 8-12s
- **YouTube** → viết script dài (800-1500 từ), gen voiceover dài, dùng 8+ scene

## Pipeline

```
CEO nhận lệnh → CHỐT FORMAT (Shorts/YouTube) → plan → hỏi confirm
  ↓
Research: search topic (fare rules, DOT/EU261, stats) → verify accuracy
  ↓
Media:
  1. Viết SCRIPT.md phù hợp format (6 scene archetypes cho Shorts ~54-60s; hoặc 8-12 scene cho YouTube ~5-8min)
  2. Gen ảnh stick-figure qua Pollinations → assets/s{N}-figure.png
  3. Edge TTS voiceover → assets/vo.mp3 (mặc định en-US-AndrewNeural)
  4. Update index.html data-duration khớp voiceover duration
  5. npx hyperframes check (= 0 findings)
  6. npx hyperframes render --quality high → renders/airfare-{N}.mp4
  ↓
Marketing: Description + tags + thumbnail concept (YouTube SEO English)
```

## ⚠️ Khi đổi voice TTS: bắt buộc re-gen voiceover

Đây là pitfall phổ biến: đổi giọng (vd AndrewNeural → GuyNeural) nhưng **quên không gen lại voiceover**. File cũ vẫn tồn tại với giọng cũ → video render dùng giọng cũ.

**Checklist khi đổi voice:**
1. Edge TTS gen lại TOÀN BỘ script với voice mới: `edge-tts --voice en-US-GuyNeural --text "$(cat SCRIPT.md)" --write-media assets/vo-video-01.mp3`
2. Kiểm tra duration mới: `ffprobe -v quiet -show_entries format=duration -of csv=p=0 assets/vo-video-01.mp3`
3. Update index.html data-duration + timing từng scene
4. Xóa file OGG cũ nếu có (là dấu hiệu cho thấy voice cũ)
5. Check bằng cách extract vài giây đầu rồi nghe thử trước khi render

## 6 Scene Archetypes (Airfare Decoded — Shorts format)

| # | Type | Duration | Focus |
|---|------|----------|-------|
| 1 | HOOK | 0-6s | Kinetic title + curiosity gap |
| 2 | CONCEPT | 6-16s | Stick figure + draw-on circle + explanation |
| 3 | COMPARE | 16-26s | Myth vs Reality (2 figures, then resolve) |
| 4 | BIG NUMBER | 26-34s | Count-up stat (max 1-2x/video) |
| 5 | PROCESS | 34-46s | 3-5 steps + connection lines |
| 6 | CTA | 46-54s | Subscribe pulse + brand line |

## Variation Guard
Mỗi video PHẢI khác video trước ≥3/5 trục (chống flag inauthentic):
1. Thứ tự scene archetypes
2. Layout (figure trái↔phải, compare dọc↔ngang)
3. Hình Pollinations mới 100%
4. Nhịp timeline (offset/duration/stagger)
5. Micro-motion (draw-on circle ↔ underline ↔ arrow ↔ zigzag)

## Quy tắc cứng
- **Cấm số liệu bịa** — verify mọi luật/quy định bằng web_search
- **Case study có tên + cảnh** — không generic "một người đàn ông"
- **≥2 insider detail mỗi video** — knowledge chỉ dân trong nghề biết
- **Không legal advice** — luôn kèm disclaimer
- **Edge TTS toàn bộ script 1 lần** — không gen từng đoạn
- **No BGM, no SFX** — chỉ voiceover + stick figure animation

## Pitfall history — học từ lỗi đã mắc

| Pitfall | Triệu chứng | Root cause | Fix |
|---------|------------|------------|-----|
| **135s no man's land** | Video 2:15 — quá dài cho Shorts, quá ngắn cho YouTube | Mở rộng script từ 54s lên 135s mà không đổi format | **Chốt format trước khi viết script** — Shorts ≤60s, YouTube ≥5min. Không tồn tại "medium format" |
| **Voice swap không re-gen** | Video dùng AndrewNeural dù đã quyết định GuyNeural | Gen voiceover AndrewNeural, sau đó đổi quyết định sang Guy nhưng không gen lại file | Luôn kiểm tra file voiceover mới sau khi đổi voice. Dùng `ffprobe` check duration khớp script |
| **Stretch script vào format cũ** | Giữ 6 scene archetypes cho 135s → nội dung loãng | Chỉ tăng duration mỗi scene thay vì thêm scene | Script dài cần thêm scene (8-12 cho YouTube), không kéo dài scene cũ |

## Edge TTS Voices

| Voice | Tone | Use | Notes |
|-------|------|-----|-------|
| `en-US-AndrewNeural` | Warm, Confident | Default explainer | Giọng "textbook", tin cậy, 24kHz mono |
| `en-US-BrianNeural` | Casual, Sincere | Softer topics | Gần gũi, casual |
| `en-US-ChristopherNeural` | Authoritative | Insider knowledge | Giọng "docusaurus", trầm |
| `en-US-JennyNeural` | Friendly, Clear | Female alternative | Nữ |
| **`en-US-GuyNeural`** | **Podcast, warm** | **For longer YouTube videos** | **Giọng Mỹ thật nhất, tự nhiên, phù hợp podcast/vlog style. 24kHz mono** |

**Khi nào chọn GuyNeural:** khi muốn giọng podcast tự nhiên, không "textbook". Guy nghe như người thật nói chuyện, phù hợp video dài 5-8 phút. AndrewNeural vẫn ổn cho Shorts 15-60s.

Auto-detect: `edge-tts --voice en-US-AndrewNeural --text "$script" --write-media assets/vo.mp3`

## Pollinations Tips
- Style: `black ink simple stick figure, white background, minimalist, line art, educational, single character`
- Format: `1024x1024`, `nologo=true`
- Tool: `_tool_pollinations()` trong Media adapter gọi `https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true`

## Insider Detail Ideas (Airfare)
- GDS segments ≠ fare components (Amadeus TST/TSM)
- BSP settlement cycle (IATA, cash vs credit)
- Timatic visa matrix vs airline check-in system
- Minimum connecting time (MCT) manipulation
- Fare basis codes (WALKUP, NEGO, PUB)
- Hidden city / throwaway ticketing (Rule 240, DOT enforcement)
- Taxes: YQ/YR carrier surcharges (not government tax)
- ET (Electronic Ticket) vs paper — ET DB history
- PNR fields: OSI vs SSR vs SSR DOCS
