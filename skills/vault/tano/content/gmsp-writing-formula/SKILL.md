---
name: gmsp-writing-formula
description: GMSP Writing Formula v2 — Dark Truth + Cinematic storytelling for YouTube long-form (10-15 min)
---

# GMSP Writing Formula — Dark Truth + Cinematic

> **VỊ TRÍ CHIẾN LƯỢC:** GMSP (Giải Mã Số Phận) là **social funnel** — YouTube/TikTok/Facebook — dùng nội dung cinematic để dẫn traffic về **kênh Tử Vi** (bán sản phẩm luận giải, tư vấn).
> **Mục tiêu script:** Hook → Kể chuyện → CTA dẫn về landing Tử Vi (`fasttracknoibai.com/tuvi` hoặc landing page port 8139).
> **KHÔNG** bán trực tiếp trong video — chỉ tạo sự tò mò và CTA đăng ký kênh/kéo về landing.
> Xem `tuvi-agent` skill cho pipeline luận giải & bán hàng.

## Khi nào dùng
Viết script cho kênh **Giải Mã Số Phận** (YouTube 10-15 phút) — hoặc bất kỳ script nào cần giọng kể chuyện cinematic, dồn dập, mạnh mẽ. Công thức này kết hợp Tử Vi + tâm lý học + định luật trong một cấu trúc 6 section, với case study xuyên suốt.

## Nguyên tắc vàng
**"Kể chuyện, không liệt kê kiến thức."** Mỗi khái niệm phải đi qua 1 câu chuyện — có người, có cảnh, có cảm xúc. Voice content chết vì liệt kê, sống nhờ chuyện.

## Công thức 1 đoạn (áp dụng mọi section)
```
1. CẢNH (sensory detail) — "Anh Tuấn đang ăn cơm thì điện thoại reo"
2. CẢM XÚC — "Anh biết ngay chuyện gì sắp xảy ra"
3. SỰ THẬT (luận điểm) — "Suốt 10 năm không xây gì ngoài CV"
4. KẾT NỐI (với audience) — "Bạn có dám chắc mình không như vậy?"
```
Không bao giờ viết sự thật trần trụi mà không có cảnh dẫn vào. Không bao giờ kể cảnh mà không rút ra sự thật.

## Khung sườn tập (6 section)
```
HOOK (60-90s)         — Sự thật trần trụi / câu hỏi vào insecurity, ~1000-1400 ký tự
BỐI CẢNH (3-4 phút)   — 2 case study có tên + cảnh cụ thể + thoại, ~3300-4400 ký tự
TỬ VI GIẢI MÃ (2.5-3.5 phút)  — Lens mệnh lý, mở đầu bằng "Nhớ [tên] không?", ~2800-3800 ký tự
TÂM LÝ & ĐỊNH LUẬT (2.5-3.5 phút) — Lens hành vi, ~2800-3800 ký tự
GIẢI PHÁP (2.5-3.5 phút)  — 3 giải pháp, MỖI CÁI gắn vào 1 case study, ~2800-3800 ký tự
CLIFFHANGER + END (45-60s) — Kéo tập sau + CTA đăng ký + share, ~800-1000 ký tự
TỔNG: 13,000-16,500 ký tự = 12-15 phút
```
**Quan trọng: Mỗi khi chuyển hệ thống, PHẢI quay lại case study cũ.** Không giới thiệu rồi bỏ. "Nhớ anh Tuấn không?" xuyên suốt cả tập.

## Series continuity — gài tập sau
Cliffhanger/end card KHÔNG được nói chung chung ("hẹn bạn tập sau"). PHẢI gài tên + hook của tập tiếp theo.
- ✅ "Tập sau: *Bí Mật Giới Tinh Hoa* — vì sao mày làm 12h/ngày vẫn nghèo, và họ làm 4h/ngày nhưng giàu. Đăng ký để không bỏ lỡ."
- ❌ "Hẹn bạn tập sau." / "Tập sau sẽ còn nặng hơn."

Lý do: YouTube recommendation hoạt động dựa trên retention. Nếu người xem biết chính xác tập sau nói gì, họ có lý do để đăng ký.
- Nếu tập sau chưa được viết, viết hook mơ hồ nhưng vẫn gọi tên: "Tập sau: một bí mật mà giới tinh hoa không muốn bạn biết."
- Khi viết tập sau, PHẢI mở đầu bằng câu nối: "Như đã hẹn ở tập trước..."

### Production ordering rule
Khi cliffhanger EP[N] gài CỤ THỂ chủ đề EP[M]:
- EP[M] PHẢI được sản xuất NGAY SAU EP[N], không chen tập khác
- Nếu gài chung chung ("Hẹn bạn tập sau") thì thứ tự tự do
- Kiểm tra: trước khi bắt đầu tập mới, đọc cliffhanger của tập trước
- Lý do: YouTube dựa trên watch time liên tục. Xem N → muốn M ngay, nếu gặp X chen giữa, họ mất luồng.

### Background per episode — BẮT BUỘC
Mỗi tập PHẢI có background riêng. Không dùng lại background tập trước.
User sẽ phàn nàn nếu ko có background riêng: "cái ảnh nền mày phải fix theo từng tập chứ"
- Script: `pipeline/gen_episode_assets.py`
- Gen trước khi sản xuất mỗi tập
- Output: `assets/backgrounds/epXX_bg.png`, `assets/thumbnails/epXX_thumb.png`
- Scene tag: drawtext overlay với Playfair Display font
- Thumbnail: image_generate (FAL) + Pillow text overlay (Playfair Display, gold #FFD700, dark gradient)

### Thumbnail pipeline
```python
from PIL import Image, ImageDraw, ImageFont
# 1. Gen ảnh nền với image_generate prompt: dark academic, [chủ đề], 1920x1080
# 2. Dark gradient overlay (top 300px + bottom 250px)
# 3. Text: TẬP N (gold 36pt), Title (gold 64pt), Subtitle (white 32pt)
# 4. Font: Playfair Display (DOWNLOAD từ Google Fonts, ko dùng Playbill)
```

## Cinematic Storytelling Rules
Mỗi tập PHẢI có background riêng. Không dùng lại background tập trước.
- Script: `pipeline/gen_episode_assets.py` — gen 15 backgrounds + thumbnails
- Output: `assets/backgrounds/epXX_bg.png`, `assets/thumbnails/epXX_thumb.png`
- Thumbnail: 1280x720, nền + TẬP N + title + subtitle
- Khi render video → phải đổi bg từ `ep01_bg` sang `epXX_bg`

## Cinematic Storytelling Rules

### 1. Cụ thể hóa nhân vật
- ❌ "Một người đàn ông 34 tuổi, làm quản lý"
- ✅ "Anh Tuấn đang ngồi ăn cơm cùng vợ con thì điện thoại reo. Số lạ. 'Anh xuống phòng họp 5 phút.'"

### 2. Sensory detail — chỉ 1-2 chi tiết
- "Thùng carton đựng cốc cà phê, khung ảnh gia đình" → đủ để thấy cảnh sa thải
- "Chị HR mỉm cười chuyên nghiệp" → 1 câu là đủ lạnh lưng

### 3. Có câu thoại — ngắn, thật
- "Anh xuống gặp sếp 5 phút"
- "Giờ làm gì?"
- "Ổn định trước đã, làm liều sau."

### 4. Không kể lại — cho họ thấy
- Kể: "Anh ta hỏi giờ phải làm sao"
- Cho thấy: "Giờ làm gì?"

## Nhịp điệu Rhythm — CỰC KỲ QUAN TRỌNG
Script mà 1 pattern = nghe như robot. Phải biến thiên liên tục.

### 5 Pattern:
| Pattern | Tác dụng | Ví dụ |
|---------|----------|-------|
| **Dài (flowing)** | Miêu tả, dẫn dắt, không khí | "Cả phòng xì xào suốt tuần về tái cơ cấu — nhưng ai cũng nghĩ không đến lượt mình." |
| **Ngắn (staccato)** | Giật, đánh thức, điểm nhấn | "Anh ta gật đầu. Ký tên. Ra về." |
| **Câu hỏi tu từ** | Lôi kéo audience vào cuộc hội thoại | "Bạn có dám chắc mình không như vậy?" |
| **1-chữ beat** | Khoảng lặng trước thông tin quan trọng | "Mười năm. Trong tích tắc." |
| **Điệp khúc (anaphora)** | Tăng kịch tính, tạo pattern rồi phá vỡ | "Chờ sếp. Chờ chỉ đường. Chờ người khác quyết định thay." |

### Quy tắc phân bổ (1 section 90-120s):
1 câu dài mở đầu → 2-3 câu ngắn giật → 1 câu hỏi tu từ → 1 beat → lặp lại
→ KHÔNG 2 câu liên tiếp cùng độ dài/pattern.

## CTA & Branding — 3 lần xuyên suốt
| Vị trí | Nội dung |
|--------|----------|
| **Hook** (cuối phần mở) | Nhấn đăng ký trước khi tôi kể tiếp. Kênh này là Giải Mã Số Phận. |
| **Mid-roll** (sau phần lý giải, trước giải pháp) | Nếu bạn vẫn đang nghe — đăng ký kênh Giải Mã Số Phận ngay... |
| **Cliffhanger + End** | Tập sau, Giải Mã Số Phận sẽ mổ xẻ... Đăng ký để không bỏ lỡ |
| **End card** | Giải Mã Số Phận — mỗi tuần một sự thật. Đăng ký, bật chuông. |

**KHÔNG nhắc tên kênh 2 lần trong cùng 1 đoạn văn.** Trông như nhồi nhét, gây nhàm.
- Nếu mở đầu đã nói "Trong tập X của Giải Mã Số Phận" → cuối HOOK ko nhắc lại nữa
- Tên kênh total: 3 lần per script (mỗi section khác nhau)

## Cấm
- ❌ **Số liệu không kiểm chứng** — "Harvard 40%", "90% người Việt..." Ko check nguồn trong 2 phút → bỏ. Thay bằng lập luận logic.
- ❌ Giảng bài kiểu "hôm nay chúng ta sẽ học về" — mất attention ngay
- ❌ Nói chung chung kiểu "ai cũng có số phận" — không có gì để bám
- ❌ Thuật ngữ Tử Vi không dịch ra đời thường — mất audience
- ❌ 2 câu liên tiếp cùng độ dài/pattern — gây buồn ngủ
- ❌ Giải pháp generic không gắn case study — advice sáo rỗng
- ❌ **Script dưới 12 phút (~11,000 ký tự)** — EP01 bị chê "hơi ngắn và hơi sơ sài". Mục tiêu 12-15 phút (~13,000-16,500 ký tự).

## Bắt buộc
- ✅ Mở bằng cảnh hoặc sự thật trần trụi — có hình ảnh, không lý thuyết
- ✅ Case study có tên + cảnh + thoại — Tuấn, Hà, Hương... tên người thật
- ✅ Kết nối Tử Vi → đời thường bằng 1 câu dịch
- ✅ Kết mỗi section bằng câu hỏi hoặc câu ngắn giật — kéo sang section sau
- ✅ Case study xuất hiện lại ở mỗi phần — nối các lăng kính
- ✅ Kết bằng giải pháp gắn vào case study — không advice chung chung
- ✅ Xen kẽ nhịp — dài, ngắn, hỏi, beat, lặp lại
- ✅ CTA 3 lần: Hook + Mid-roll + Cliffhanger
- ✅ Tên kênh 3 lần

## Production handoff
After script is finalized → split into **8 sections** → Edge TTS (segments) → concat với gap 6s → gen chapter overlays → FFmpeg render.

Key constants user has approved:
- **3-second gaps** between sections (for chapter transitions) — user chốt 3s, 6s bị chê dài
- **Gap timing**: gen với `ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 3 gap3s.mp3`
- **No BGM, no subtitles**
- **4-corner branding** (logo 170px, scene tag 28px, brand 24px, subscribe 18px)
- **Intro card 5s** (logo + title + line animation)
- **Single voice** throughout
- Final delivery = single `.mp4`
- **Edge TTS** (Resona API dead since Jul 2026) — `vi-VN-NamMinhNeural`, rate variation for pitch

## Related skills
- `gms-storyteller` — Script writer agent dùng reasoning model (DeepSeek R1) để viết script mới