# Landing Page Design — "Giải Mã Số Phận" (Tử Vi)

## Theme (confirmed 20/07/2026)
- **Theme:** Light theme (WHITE #FFFFFF, gray #F8F9FA → #333)
- **Brand name:** "Giải Mã Số Phận" — KHÔNG dùng "Bộ Não Phán" nữa
- **Font:** Be Vietnam Pro (Google Fonts) — tiếng Việt đẹp
- **Gold accent:** #B8860B (dark gold) — dùng #D4A017 cho hover
- **Navy:** #1a1a2e (deep navy cho logo + headings)
- **Cream:** #FFF8E7 (nền nhẹ cho section highlight)

## CSS Tokens
```css
:root {
  --gold: #D4A017;
  --gold-dark: #B8860B;
  --gold-light: #E8C350;
  --gold-bg: rgba(212,160,23,0.08);
  --navy: #1a1a2e;
  --cream: #FFF8E7;
  --white: #FFFFFF;
  --gray-50: #F8F9FA;
  --gray-100: #F0F1F3;
  --gray-200: #E2E4E8;
  --gray-300: #C4C7CC;
  --gray-500: #8A8D96;
  --gray-600: #6B6F78;
  --gray-700: #4A4D54;
  --gray-800: #2D2F35;
  --gray-900: #1A1B1E;
  --text: #333333;
  --text-muted: #6B6F78;
}
```

## Media Assets (updated Phase 2)
| Asset | Path | Notes |
|-------|------|-------|
| Logo SVG | `assets/logo.svg` | "GIẢI MÃ" navy + "SỐ PHẬN" gold, Bắc Đẩu 7 sao + mắt thứ 3, viewBox 0 0 400 120 |
| Favicon | `assets/favicon.svg` | Navy nền + gold Bắc Đẩu |
| Icons Sprite | `assets/icons.svg` | 8 SVG symbols: star, money, heart, brain, shield, career, moon, scroll — dùng `<use href="/assets/icons.svg#icon-name">` |
| OG Image | `assets/og-image.svg` | 1200×630 social share image |

## Sections (8 sections)

### 1. Hero
- **Headline**: "Số phận của bạn không phải bí ẩn — nó là bản đồ."
- **Sub**: Kết hợp Tử Vi cổ học với tâm lý học hành vi. Không mê tín. Không phán xét.
- **CTA**: "Khám phá số mệnh của bạn — Miễn phí"
- **Stats**: "Đã có 1,247 người khám phá bản đồ cuộc đời họ"
- **Visual**: CSS particles (12 floating gold/cream dots staggered animation) + gradient glow

### 2. Features (thay vì Paint Points static)
- Feature 1: **"Xem ngay lá số"** — 3 giây, 12 cung tử vi
- Feature 2: **"7 góc nhìn cuộc đời"** — Tiền bạc, sự nghiệp, tình duyên, gia đình, sức khỏe, tinh thần, vận hạn
- Feature 3: **"Tâm lý + Tử Vi"** — Behavioral Psychology + Game Theory
- Feature 4: **"Dự đoán vận hạn"** — Đại hạn, lưu niên, tháng

### 3. Form nhập thông tin
- Năm/Tháng/Ngày/Giờ sinh (canh chi) + Giới tính
- Validation: year 1900-2010
- Loading state khi submit → API call

### 4. Demo Result (từ MCP thật)
- 7 paint points progress bars
- Color gradient theo severity: đỏ (90%+) / vàng (70-89%) / xanh (50-69%)
- Icon auto-detect từ Paint Point name
- Stagger fade-in animation
- `result-content.js` — giải thích bằng văn nói cho từng PP

### 5. Products
- 39 sản phẩm từ API
- Payment modal: Momo + VNPay

### 6. Testimonials (3 case studies realistic)
- Minh (32, Developer) — "Money Anxiety"
- Lan (28, Marketing) — "Overthinking"
- Chú Hùng (45, Kinh doanh) — "Career Plateau"

### 7. FAQ (8 câu hỏi)
- Tử vi là gì?
- Có chính xác không?
- Mất bao lâu?
- Có cần đăng ký?
- Khác gì web tử vi khác?
- Không nhớ giờ sinh?
- Xem cho người khác?
- Gói trả phí có gì?

### 8. Footer
- 3-column grid

## API Integration
- Backend: FastAPI port 8139
- `POST /api/demo` — {year, month, day, hour (0-23), gender ("male"/"female")}
- `GET /api/products` — 39 products
- `POST /api/payment/momo` — tạo order + redirect Momo sandbox
- `POST /api/payment/vnpay` — tạo order + redirect VNPay sandbox
- Fallback data arrays khi API fail (ko crash)

## Result Visualization (MEDIA-06)
```css
/* Severity colors */
--severity-high: #dc3545;    /* ≥90% */
--severity-mid: #e8a317;     /* 70-89% */
--severity-low: #28a745;     /* 50-69% */
/* Gradient progress bars with icon + stagger animation */
```

## Scroll Animations
- `.section-fade-in` — IntersectionObserver, fade + translateY
- `.stagger-fade-in` — children stagger delay (0.1s increments)
- `.result-card` — staggered by index * 0.15s

## Nội dung guidelines
- **Dễ hiểu cho người thường** — ko thuật ngữ Tử Vi khô khan
- **Tiếng Việt thuần** — "bạn" xưng hô, "khám phá vận mệnh", "phân tích lá số"
- **Không "Bộ Não Phán"** — brand xuyên suốt là "Giải Mã Số Phận"
- **CTA tự nhiên** — "Xem Ngay Miễn Phí", "Khám Phá Ngay"
- **Testimonial realistic** — có tên, nghề nghiệp, kết quả cụ thể
- **FAQ thật** — "Tử vi là gì?", "Có chính xác không?", "Bao lâu có kết quả?"

## Brand Voice (from docs/BRAND_VOICE_GUIDE.md)
- Tone: "Người bạn thông thái, từng trải, luôn nói thật"
- Nói thẳng nhưng không phán xét
- Dùng từ đời thường, giải thích Tử Vi bằng ngôn ngữ hiện đại
- Cấm: "tam hợp", "xung chiếu", "tứ hóa", "kiếp", "nghiệp", "quả báo"
- Khuyến khích: "vận mệnh", "bản đồ cuộc đời", "điểm mạnh", "thử thách", "tiềm năng"

## Kỹ thuật
- 1 file duy nhất index.html (inline CSS + JS + HTML) — trừ khi quá lớn
- Mobile-first: breakpoints 480/768/1024
- Micro-animations: IntersectionObserver scroll fade-in, hover effects, loading spinner
- Icons: Lucide CDN + assets/icons.svg sprite
- Font: Google Fonts Be Vietnam Pro
- SEO: title, meta description, OG tags, keywords, robots
- Validation form client-side trước gọi API

## File Structure
```
D:\MMO Du an\Tu Vi\
├── frontend\
│   ├── index.html           # Landing page (651 dòng, Phase 2)
│   ├── app.js               # API calls + form + payment (17KB)
│   ├── style.css            # External CSS (335 dòng — result cards, testimonial, FAQ, animations, particles)
│   └── result-content.js    # 7 paint point explanations (văn nói)
├── assets\
│   ├── logo.svg             # Logo SVG 400×120
│   ├── favicon.svg          # Favicon SVG
│   ├── icons.svg            # SVG sprite 8 icons
│   └── og-image.svg         # OG Image 1200×630
├── backend\
│   ├── main.py              # FastAPI + payment
│   └── models.py            # SQLAlchemy
├── engine\
│   ├── paint_point_engine.py # 21+ rules, 512 lines
│   └── tuvi_mcp_client.py   # MCP wrapper 7 methods
└── docs\
    ├── BRAND_VOICE_GUIDE.md  # Tone + từ cấm + khuyến khích
    └── TEASER_POSTS.md       # FB + TikTok + Zalo teaser
```
