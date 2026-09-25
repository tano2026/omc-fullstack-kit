---
name: youtube-research-agent
category: content
description: Research agent tự động chui vào YouTube channel, phân tích nội dung, style, topic pattern và map sang GMSP content strategy. Dùng browser + phân tích pattern.
version: "1.0"
related_skills:
  - kho-thuat-dinhluat-tamly
  - tuvi-agent
  - gmsp-modular-pipeline
---

# 🕵️ YOUTUBE RESEARCH AGENT

## KHI NÀO DÙNG

Khi user muốn:
- "Tìm chủ đề mới từ kênh YouTube ABC"
- "Nghiên cứu style của kênh XYZ để học hỏi"
- "Phân tích content pattern của đối thủ"
- "Lấy ý tưởng video từ kênh ABC"

## THIẾT KẾ

Research agent hoạt động theo 4 bước:

```
B1: THU THẬP      → browser_navigate(channel URL) → snapshot
B2: PHÂN TÍCH     → titles, views, description pattern
B3: MAP GMSP      → đối chiếu với kho thuật/định luật/tử vi
B4: OUTPUT TOPIC  → đề xuất chủ đề cho tập GMSP
```

## QUY TRÌNH CHI TIẾT

### B1 — THU THẬP

Dùng browser để lấy thông tin channel:

```python
from hermes_tools import terminal, web_search, write_file

# Cách 1: web_search để tìm video topics (nhanh hơn browser)
web_search(f"site:youtube.com @{channel_name} popular videos")

# Cách 2: browser trực tiếp
browser_navigate(f"https://www.youtube.com/@{channel_name}/videos")
```

Cần thu thập:
- **Tiêu đề video** (từ snapshot / console)
- **Lượt xem** (đánh giá độ hot)
- **Tags / hashtags** (pattern SEO)
- **Mô tả video** (click ...more để xem full)
- **Độ dài video** (phút)

### B2 — PHÂN TÍCH PATTERN

Phân tích từng video theo các chiều:

| Chiều | Câu hỏi | Ví dụ The Hidden Self |
|-------|---------|----------------------|
| Hook | Bắt đầu bằng gì? | Câu hỏi tu từ / sự thật sốc / "điều mày không biết" |
| Chủ đề | Nói về cái gì? | Tài chính, tâm lý, xã hội, bản chất con người |
| Cấu trúc | Mấy phần, mấy màn? | Phơi bày vấn đề → Giải thích hệ thống → Giải pháp |
| Kết thúc | Kêu gọi hành động gì? | Hành động nhỏ cụ thể, cliffhanger cho tập sau |
| Tone | Giọng điệu? | Trần trụi, đối thoại trực tiếp "mày/bạn", không dạy đời |

### B3 — MAP SANG GMSP

Đối chiếu topic với GMSP framework:

```
Xác định:
1. Chủ đề này phù hợp domain nào? (Tử Vi / PTBT / Cổ Kim)
2. Có thể ghép với thuật/định luật/tâm lý nào?
3. Lens Tử Vi nào có thể overlay?
4. Góc "sự thật ẩn giấu" là gì?

Framework ghép nối:
  [Chủ đề YouTube] 
    → [Tử Vi concept] 
    → [Thuật / Định luật / Tâm lý]
    = [GMSP episode concept]
```

**Ví dụ mapping:**

```
The Hidden Self: "Capital Accumulation - Secret Elite không muốn bạn biết"
  ↓
GMSP version:    "Tại sao mày càng chăm càng nghèo? — Định luật Parkinson + Tài Bạch"
```

### B4 — OUTPUT TOPIC

Đề xuất dạng:

```
📌 TOPIC: [tên chủ đề GMSP]
├─ Nguồn cảm hứng: [tên video + channel gốc]
├─ Domain: [Tử Vi / PTBT / Cổ Kim]  
├─ Lens Tử Vi: [sao / cung / cách cục liên quan]
├─ Thuật / Định luật: [công cụ chính]
├─ Hook: [câu hook đề xuất]
├─ Cấu trúc: [3 màn cụ thể]
└─ Giải pháp: [3 actions]
```

## LƯU Ý KHI DÙNG BROWSER

1. YouTube dùng Shadow DOM → standard CSS selectors KHÔNG hoạt động
2. Cách đọc tiêu đề từ snapshot: nhìn `heading` elements trong `generic[ref=eN] clickable`
3. Để xem description: click `...more` button, sau đó snapshot lại
4. KHÔNG dùng `browser_console` querySelector trên YouTube - ko ra kết quả
5. Cách hiệu quả: snapshot → đọc heading text từ accessibility tree
6. Tab "Popular" cho thấy video top view → ưu tiên click @e41 trước

## CHIẾN THUẬT PHÂN TÍCH CHANNEL THỰC TẾ (tested Jul 2026)

Thay vì chỉ dùng browser (YouTube Shadow DOM khó parse), dùng **web_search** với query pattern:

### Pattern tìm video topics

```python
# Pattern 1: Tìm video nổi bật
web_search(f'"@channel_handle" youtube video "keyword" OR "keyword2" tiêu đề')

# Pattern 2: Tìm cấu trúc mô tả
web_search(f'"@channel_handle" youtube giới thiệu')

# Pattern 3: Tìm description keywords
web_search(f'"channel name" youtube nội dung OR chủ đề OR series')
```

### Phát hiện các kênh tương tự

Trong quá trình research, luôn để ý **Related channels** xuất hiện trong sidebar:
- YouTube đề xuất các kênh cùng niche ở sidebar khi xem 1 video
- Ghi lại tất cả competitors tìm thấy

### Ví dụ kết quả thực tế

```yaml
# The Hidden Self analysis (87.9K subs)
topics_found:
  - "Capital Accumulation — Secret Elite" (346K views)
  - "Jekyll Island — Financial Elite Secret" 
  - "Why Kindness Creates Monsters"
  - "Attention Economy — Tech Corporations"
  - "Short-term Dopamine Addiction"
  - "Redefining Destiny"

topic_clusters:
  - Tài chính ẩn + Phơi bày hệ thống (40% videos)
  - Tâm lý đen + Bản chất con người (30%)
  - Định mệnh + Số phận (15%)
  - Kỹ năng xã hội (15%)

hook_patterns:
  - "Bí mật [điều gì đó]" — khơi gợi tò mò
  - "Tại sao [nghịch lý]?" — câu hỏi tu từ
  - "[Câu khẳng định sốc] — [giải thích]"
  
competitors_found:   # từ sidebar YouTube
  - Clarity & Zen (~55K/video)
  - Buddhism Flow (~69K/video)  
  - The Inner Way (~47K/video)
```

### Tested: From research to GMSP topic

```
Raw video: "Capital Accumulation — Secret That Elite Doesn't Want You To Know"
  → Hidden finance exposé, 346K views
  → Map to: Tử Vi lens (Tài Bạch + Lộc Tồn) 
  → Add: Định luật Parkinson (càng cố càng nát)
  → Add: Cầm thú giao (thời thế tạo anh hùng)
  = GMSP topic: "Bí Mật Giới Tinh Hoa — Sao Chăm Mà Nghèo?"
```

### GMSP Topic Pipeline

```
YouTube research
  → 3-5 topics extracted per channel
  → Filter: phù hợp với GMSP framework? (Tử Vi overlay được ko?)
  → Map: Tử Vi lens + Định luật + Thuật + Tâm lý
  → Rank: views tiềm năng (dựa vào views video gốc)
  → Ghi vào GMSP/research/topics/topics.md với priority
```

## MẪU PROMPT PHÂN TÍCH CHANNEL

Khi cần phân tích 1 channel, dùng prompt structure này:

```
Tôi cần phân tích kênh YouTube @{channel_name}:
1. Mở trang channel → lấy tiêu đề + mô tả + subs count
2. Click tab "Popular" → lấy top 10 video titles + views
3. Mở 2-3 video top view → đọc description + tags
4. Phân tích: hook pattern? topic cluster? tone?
5. Map sang GMSP: nếu Tử Vi overlay thì thế nào?
6. Đề xuất 3 GMSP topics từ phân tích
```

## FILE OUTPUT

Lưu kết quả vào `GMSP/research/channels/{channel_name}.md`:
- Thông tin channel
- Top 10 videos (title + views + length)
- Pattern analysis
- 3 GMSP topic recommendations
- Ghi chú đặc biệt về style/giọng điệu

Mỗi channel research mới → copy vào skill ref để tái sử dụng:
- Nguồn: `D:/MMO Du an/GMSP/research/channels/{channel_name}.md`
- Đích: `{{SKILL_DIR}}/../gmsp-modular-pipeline/references/channel-{channel_name}.md`

### Tone & Giọng điệu

**BẮT BUỘC: Luôn dùng "bạn" — KHÔNG dùng "mày/tao" trong script nội dung.**

Based on user feedback (Jul 2026) — Episode 01 được test thực tế:

- **Default tone: "bạn"** — thay vì "mày". Mở rộng đối tượng, ai cũng nghe được.
- **Narrator:** xưng "tôi" — thân thiện, không dạy đời.
- **Style:** trần trụi sự thật nhưng tôn trọng người nghe.
- **Tránh:** "mày/tao" (giới hạn đối tượng, mất nữ giới + người lớn tuổi).

Khi viết script mới, luôn: "bạn" thay "mày", "tôi" thay "tao".

### Cấu trúc Script 6 phần

Đã test thành công với Episode 01 (10:25):

1. 🔥 **HOOK** (0:00-0:50) — Sự thật trần trụi, câu hỏi tu từ
2. 📖 **BỐI CẢNH + Câu chuyện** (0:50-3:30) — 1-2 câu chuyện người thật
3. 🏛️ **TỬ VI giải mã** (3:30-6:00) — Khái niệm Tử Vi nôm na
4. 🧠 **TÂM LÝ + ĐỊNH LUẬT** (6:00-8:30) — 2-3 định luật/tâm lý
5. ✅ **GIẢI PHÁP** (8:30-11:00) — 3 việc làm ngay
6. 🔮 **CLIFFHANGER** (11:00-11:30) — Set up tập sau

Khoảng cách thời gian tham khảo cho 8800 từ, speed 0.82.

Đã research (2026-07-15):
- **Subs:** 87.9K
- **Channel:** "Nơi sẽ có những sự thật mà xã hội không muốn cho bạn biết"
- **Top video:** "Capital Accumulation - The Secret That The Capitalist Elite Doesn't Want You To Know" (346K views, 18 min)
- **Style:** Exposé hệ thống, brutal truth hook, direct "mày"
- **Topics:** Tài chính cá nhân, bất động sản, tiền ảo, tâm lý đám đông, bẫy xã hội
- **GMSP fit:** Cao nhất cho domain PTBT + Cổ Kim

## VÍ DỤ: The Hidden Path

Đã research (2026-07-15):
- **Subs:** 133
- **Topics:** Lão Tử, Đạo giáo, Khắc Kỷ, Thiền
- **Style:** Question hook → Ancient wisdom → Modern application
- **Sample:** "Transformation Begins With Letting Go | Lao Tzu Wisdom" (196 views, 12:52)
- **GMSP fit:** Domain Cổ Kim (kết hợp với tử vi Tử Phủ)
- **Liên quan:** Clarity & Zen (55K/video), Buddhism Flow (69K), The Inner Way (47K)
