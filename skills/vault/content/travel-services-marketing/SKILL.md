---
name: travel-services-marketing
category: content
tags: [marketing, travel, airport, fast-track, esim, landing-page, funnel, content-engine]
description: "Build a marketing system for airport/travel service brands — Fast Track, eSIM, lounge, currency exchange. Covers funnel strategy (TOFU/MOFU/BOFU), content engine setup, landing page architecture, persona crafting, and multi-service cross-sell."
triggers:
  - "xây marketing cho trùm sân bay"
  - "làm phương án marketing tổng thể cho dịch vụ sân bay"
  - "build landing page + content engine cho fast track"
  - "marketing kế hoạch bán esim du lịch"
  - "xây funnel bán dịch vụ sân bay"
  - "trùm sân bay marketing"
  - "phương án bán fast track và sim du lịch"
  - "travel services marketing plan"
---

# Travel Services Marketing — Airport Services Brand

> Dành cho brand bán dịch vụ sân bay: Fast Track, Lounge, eSIM du lịch, đổi tiền.
> Đã áp dụng thành công cho **Trùm Sân Bay** + **An Bình Fast Track**.

## Phương Pháp Tiếp Cận

### 1. Brand Architecture

Xác định cấu trúc brand trước khi làm marketing:

| Mô hình | Khi nào dùng | Ví dụ |
|---------|-------------|-------|
| **Single brand** | 1 chủ thể duy nhất | Trùm Sân Bay (all services) |
| **Master + Sub-brand** | Brand mẹ có sub-service riêng | ABTrip → Fast Track, eSIM |
| **White-label** | Bán qua đối tác/CTV | Fast Track trắng cho hotel/DMC |

### 2. Persona Crafting

Persona content engine cần 3 thành phần:

**Tone:**
- Nhân viên sân bay kỳ cựu (insider, có thẩm quyền, thân thiện)
- Người đã đi nhiều (so sánh thực tế, tips xịn)
- Chuyên gia tư vấn (formal, chuyên nghiệp)

**Voice rules:**
- Không dùng ngôn ngữ bán hàng ép buộc
- Luôn có insider tips miễn phí trước khi promote
- Dùng số liệu thực tế, không bịa
- Giọng "như người anh/chú trong nhà" — casual nhưng có thẩm quyền

**Guardrails:**
- KHÔNG cam kết giá cụ thể (giá thay đổi theo mùa)
- KHÔNG bịa quy định hàng không
- KHÔNG tự động reply comment tiêu cực
- Fact-check bắt buộc với info về an ninh, visa, hành lý

### 3. Content Funnel

Funnel 3 tầng — áp dụng cho mọi travel service brand:

| Tầng | Tỉ lệ | Mục tiêu | Ví dụ hook |
|------|-------|----------|------------|
| **TOFU** | 60% | Awareness — tips miễn phí, không bán | *"3 lỗi khiến bạn mất 2 tiếng ở sân bay"* |
| **MOFU** | 25% | Consideration — so sánh, case study | *"Fast Track 200K có đáng không? Tính thử"* |
| **BOFU** | 15% | Conversion — CTA trực tiếp | *"Đặt Fast Track hôm nay — có người đón tận cửa"* |

**Pillars content:**
1. **Insider tips** — điều nhân viên sân bay biết mà khách không biết
2. **Cảnh báo & bẫy** — lỗi phổ biến khiến khách trễ chuyến / mất tiền
3. **Hướng dẫn từng bước** — quy trình check-in, an ninh, boarding
4. **Giải đáp FAQ** — thắc mắc phổ biến
5. **Promote dịch vụ** — Fast Track, SIM, đổi tiền (tone tư vấn)

### 4. Content Engine Architecture

Đã có code mẫu tại `D:\MMO Du an\Trum Du Lich\`:

```
agent.py           ← 710 dòng — pipeline agent
orchestrator.py    ← 651 dòng — brain thật, ghép 9 agent
system-prompt.md   ← Persona prompt
ARCHITECTURE.md    ← Chi tiết sub-agent + platform
HARNESS.md         ← 3 trụ: context, constraints, entropy
```

**Pipeline (từ orchestrator.py):**

```bash
python3 orchestrator.py weekly     # Research → Ideation → Writer → Visual → Brand Check
python3 orchestrator.py comments   # Fetch + classify + draft reply
python3 orchestrator.py token_check  # Health check token
```

**7 sub-agents:**
1. **Research** — crawl RSS, TikTok, FB → giới hạn 5-10 items/nguồn
2. **Ideation** — 7-10 idea/tuần, gắn pillar tag (TOFU/MOFU/BOFU)
3. **Writer** — caption từng platform, fact-check guardrail
4. **Visual** — gen ảnh/video (Gemini free tier / HyperFrames)
5. **Brand Design** — validate màu, font, logo, contrast
6. **Adapter** — adapt format từng platform (FB 1200x630, IG 1080x1080, TikTok 9:16)
7. **Publisher** — đăng qua API, retry + idempotency

**Harness gồm:**
- `progress.json` persistence — crash-safe, biết dừng ở đâu
- Pipeline gate — mỗi bước chỉ chạy nếu status hợp lệ
- Safety filter — chặn "100% đảm bảo", cam kết giá
- Weekly entropy audit — kiểm tra hook trùng, token hết hạn, engagement trend

### 5. Landing Page — Travel Services

Có **2 approaches** — chọn theo đối tượng và mục tiêu:

#### Approach A: Traditional Multi-Section (B2B / CTV Recruitment)

Dùng cho: Bán gói CTV, đại lý, giải thích nhiều tính năng, cần SEO content.

| Page | Mục đích | Nội dung |
|------|---------|----------|
| **Home** | Tổng quan dịch vụ | Hero + 3 service cards + trust signals + CTA |
| **Fast Track** | Chi tiết + đặt | Pricing table, how it works, policies, booking form |
| **eSIM** | Chi tiết + đặt | Data plans, countries, activation guide |
| **Blog** | SEO + organic | Tips, hướng dẫn, so sánh |

**Mobile-first** — khách hàng chủ yếu dùng điện thoại.

**Booking flow:**
```
Landing → Chọn dịch vụ → Điền info → Gửi Telegram CEO bot → Xác nhận
```

#### Approach B: Conversational Single-Screen (Chat-first, B2C + B2B Modern)

<!-- Key insight from Smart Agent project (Jul 2026): user rejected multi-section landing, wanted "1 trang như ChatGPT, đặt dịch vụ = ngôn ngữ tự nhiên, ko chọt chọt" -->

Dùng cho: Người dùng cuối, khách lẻ, đối tượng quen chat AI (Gen Z, digital native). Loại bỏ hoàn toàn navigation multi-page, form fields, và traditional CTA buttons.

**Kiến trúc:**
```
1 màn duy nhất: Header + Chat Messages + Input Box
Không hero section riêng — welcome screen tích hợp trong chat
Không pricing grid riêng — AI báo giá trong luồng hội thoại
Không contact form — khách đặt dịch vụ bằng cách "nói 1 câu"
```

**Components bắt buộc:**
- Welcome screen (khi chưa có message): logo icon + tagline + suggestion pills (5-6 câu mẫu)
- Chat interface: user bubble → assistant bubble → result cards (giá vé, Fast Track, eSIM)
- Quick tools bar: 4-5 nút nhỏ trên input box
- Input box: 1 dòng, Enter gửi, placeholder gợi ý câu nói mẫu
- Result cards: inline trong chat — danh sách chuyến bay + nút "Đặt ngay" (ko form riêng)

**Design rules (taste-frontend applied):**
- Font: Plus Jakarta Sans / Geist / Cabinet Grotesk — KHÔNG Inter, Roboto, Arial
- Màu nền ấm: #FAF8F5 (light) hoặc #1A1206 (dark gold)
- Chat bubble: user = inverted, assistant = white card + border
- KHÔNG shadow-md/shadow-lg mặc định — box-shadow: 0 1px 3px rgba(0,0,0,0.04)
- KHÔNG gradient cards, glossy glassmorphism nặng
- Mobile-first: 1 cột full-width, input box bottom
**Flow booking qua hội thoại:**

```
User: "Vé SG đi Nha Trang thứ 7 2 người"
  → AI search flight → result card: VJ 1.2tr/người
  → User: "Đặt chuyến VJ"
  → AI collect info trong chat → xác nhận → đặt
```

**Tối ưu hóa Luồng Nhập thông tin hành khách (23 Jul 2026):**
Để hạn chế việc khách hàng phải gõ nhiều và chống đứt luồng, luồng thu thập thông tin hành khách đã được tối ưu hóa:
- **Trạng thái chủ động:** Sau khi chọn chuyến bay, bot chuyển sang trạng thái `awaiting_passenger_info` để chuyên biệt hóa việc thu thập dữ liệu hành khách.
- **Gợi ý cú pháp:** Bot chủ động gửi kèm mẫu cú pháp để khách chỉ cần sao chép và sửa (ví dụ: `NGUYEN VAN A / Nam / 15-10-1995 / 0987654321 / a@gmail.com`).
- **Trích xuất thông tin linh hoạt:** Bot cố gắng trích xuất thông tin (tên, ngày sinh, giới tính, SĐT, email) ngay cả khi nhận được dữ liệu dạng một phần từ khách (ví dụ: khách chỉ gõ tên riêng trước).
- **Hỏi cụ thể các trường còn thiếu:** Thay vì trả lời chung chung, bot sẽ lịch sự hỏi tiếp các trường thông tin còn thiếu một cách cụ thể, kèm theo các gợi ý nhanh (quick replies) phù hợp (ví dụ: "Nam", "Nữ" cho giới tính; ngày sinh gợi ý theo độ tuổi người lớn/trẻ em/em bé).
- **Tự động điền thông tin liên hệ:** Thông tin số điện thoại và email của hành khách đầu tiên sẽ được tự động gợi ý hoặc điền cho các hành khách tiếp theo nếu khách không cung cấp lại.
- **Xử lý ảnh (placeholder):** Đã có logic nhận diện URL ảnh Hộ chiếu/CCCD, tuy nhiên, việc trích xuất thông tin tự động từ ảnh bằng `vision_analyze` hiện đang là placeholder và cần tích hợp tool-calling trực tiếp từ Hermes Agent.

**Pitfalls:**
- Cần SSE streaming backend — request-response thường >3s là mất user
- Suggestion pills phải realistic — ko ghi chung chung
- Result cards phải clickable — ko redirect ra trang khác
- Welcome screen ẩn khi có message đầu — ko scroll đi
- Auto-scroll theo mỗi token stream
- Typing indicator 3-dot khi AI đang trả lời

**Khi nào dùng A, khi nào dùng B:**
- **A**: bán cho CTV/đại lý, cần SEO, cần giải thích nhiều
- **B**: bán cho khách lẻ, cần đặt nhanh, Gen Z friendly

### 6. Product-Specific Playbooks

#### Fast Track (An Bình Fast Track)

**USP chính:** Onsite staff 24/7 — đơn vị duy nhất tại HAN có người đón tận nơi.

**Brand constraints:**
- Không dùng tên "Nội Bài"/"Noi Bai" trong brand (quy định sân bay)
- Dùng "Fast Track HAN" hoặc "Fast Track Hà Nội"
- Brand color: Teal #006885 + Gold #DBA011

**Pricing tiers:**
- 3 bảng giá: Retail (1 cột) / Agent (2 cột) / Full (3 cột)
- Phụ thu đêm 23:00-06:00 +200K
- VAT chưa bao gồm

**Cross-sell:**
- Khách đặt vé → offer Fast Track
- Khách đặt Fast Track → offer SIM
- Combo: vé + Fast Track + SIM = du lịch trọn gói

#### eSIM (SIM Du Lịch)

**Need-to-know:**
- Supplier IST1 — source code có sẵn
- Activation: scan QR / nhập code
- Price: theo data plan + quốc gia

**Bán kèm:** gói combo "Du lịch trọn gói" = vé + Fast Track + SIM

### 7. Multi-Platform Publishing

Các platform và format tối thiểu:

| Platform | Format ảnh | Format video | Caption limit | Hashtag |
|----------|-----------|--------------|---------------|---------|
| Facebook | 1200x630 | 16:9, max 20p | 63,206 chars | 3-5 |
| Instagram Feed | 1080x1080 | 1:1, max 60s | 2,200 chars | 5-10 |
| Reels | 1080x1920 | 9:16, max 90s | 2,200 chars | 3-5 |
| TikTok | 1080x1920 | 9:16, 15-60s | 2,200 chars | 3-5 |
| YouTube Shorts | 1080x1920 | 9:16, max 60s | title 100 chars | - |

**Nhịp đăng:** 7 post/tuần, gen hàng loạt → queue chờ review → đăng thủ công (semi-auto)

### 8. Measurement & Optimization

| Metric | Theo dõi | Hành động nếu xấu |
|--------|---------|-------------------|
| Engagement rate | Hàng tuần | Đổi hook style |
| Click-through to booking | Hàng tháng | Tối ưu CTA |
| Conversion rate | Hàng tháng | A/B test pricing display |
| Comment sentiment | Hàng ngày | Xử lý complaint nhanh |
| Token health | Hàng ngày | Refresh trước khi expire |

## Workflow Steps

1. **Data gathering** — audit existing code/pipeline (agent.py, orchestrator, system-prompt)
2. **Brand positioning** — define persona, tone, funnel
3. **Landing page** — build home + service pages
4. **Content engine** — set up orchestrator pipeline, connect social APIs
5. **Harness** — add progress.json, pipeline gates, safety filters
6. **First content batch** — gen 7 post tuần đầu, review, publish
7. **Cross-sell integration** — connect booking flow: landing → CEO bot → AGT/Fast Track

## Pitfalls

- **Không bắt đầu với social trước.** Landing page + SEO là nền tảng, content là chất xúc tác. Làm landing page trước.
- **Đừng chạy full-auto ngay.** Bắt đầu semi-auto: gen → người review → approve → publish. Sau 2-3 tuần mới tính auto.
- **Persona phải nhất quán xuyên suốt.** Cùng 1 giọng trên landing page, Facebook, TikTok. Không để persona content khác persona web.
- **Fast Track brand constraint:** KHÔNG dùng tên sân bay cụ thể (Nội Bài) trong brand name. Dùng "Fast Track HAN".
- **Giá + chính sách thay đổi thường xuyên.** Không hardcode trong code — dùng config file hoặc env.
- **API token hết hạn âm thầm.** Cần proactive check hàng ngày, không đợi fail mới biết.
- **Airtable queue phồng to.** Archive record >90 ngày định kỳ.
- **Không đăng content vào ngày không ai review.** Queue sẽ chết, engagement giảm.

## Related Skills

| Skill | Quan hệ |
|-------|---------|
| `brand-identity-sales-kit` | Brand assets — landing page, pricelist, brochure HTML deliverables |
| `social-media-stack` | Công cụ đa nền tảng — Buffer, Meta, TikTok |
| `content-creator` | Tạo content từ 1 ý tưởng |
| `viral-hooks` | Hook formulas cho TikTok/Reels |
| `harness-engineering` | 3 trụ production agent |
| `abtrip-flight-search` | ABTrip flight services (cross-sell partner) |
| `expert-ticketing-aviation` | Aviation domain expertise |

| `expert-ticketing-aviation` | Aviation domain expertise |

## Reference Files

- `references/trumsanbay-architecture.md` — Full architecture from Trùm Sân Bay standalone repo
- `references/fast-track-brand-guide.md` — An Bình Fast Track brand + pricing
- `references/conversational-landing-smart-agent.md` — Working example of Approach B (chat-first landing, Smart Agent project Jul 2026)
- `references/an-binh-aviation-corporate-landing.md` — An Bình Aviation corporate landing page (6-service pillars, light theme, pricing PDF/Excel workflow, language switcher pattern)
