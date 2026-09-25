# Landing Page Themes — Giải Mã Số Phận & Bộ Não Phán

> Two brand variants, two themes. This reference documents both so future sessions don't waste time re-evaluating.

## Theme Matrix

| Aspect | Bộ Não Phán (Dark) | Giải Mã Số Phận (Light) |
|--------|-------------------|------------------------|
| **Brand color** | Gold #c9a84c | Gold #D4A017 |
| **Background** | #0a0a1a (dark navy) | #FFFFFF → #F8F9FA (white gradient) |
| **Cards** | #12122a / #1a1a3a | #FFFFFF, border #E2E4E8 |
| **Text** | #e0d5c0 (warm light) | #333333 (dark gray) |
| **Subtext** | #908070 | #6B6F78 |
| **Shadow** | 0 8px 32px rgba(0,0,0,0.4) | 0 4px 16px rgba(0,0,0,0.08) |
| **Footer** | Transparent border-top | #1A1B1E dark footer |
| **Header bg** | rgba(10,10,26,0.92) blur | rgba(255,255,255,0.95) blur |
| **Form bg** | Dark gradient #12122a→#1a1a3a | White card with gray border |
| **Product tier badge** | #c9a84c bg / gold text | #F0F1F3 bg / #6B6F78 text |
| **Buttons** | Gold/brown gradient on dark | Gold gradient on white |
| **Font** | System-ui stack | **Be Vietnam Pro** (Google Fonts) |
| **Icons** | Emoji (🔮🧠💰) | **Lucide SVG icons** (CDN) |

## Giải Mã Số Phận — Light Theme (built 20/07/2026)

### File
`D:\MMO Du an\Tu Vi\frontend\index.html` — 810 lines, 44KB

### Sections

| # | Section | Details |
|---|---------|---------|
| 1 | **Hero** | Gradient gold "Khám Phá Vận Mệnh Của Bạn", badge "AI Tử Vi Thế Hệ Mới", 4 stat counters (12 Cung / 7+ Paint Points / 39 Sản Phẩm / 99% Chính Xác), subtext CTA |
| 2 | **Paint Points** | 6 cards: Overthinking, Tiền Bạc, Sự Nghiệp, Gia Đình, Tình Cảm, Danh Tiếng — Lucide icons, scroll-triggered fade-in via IntersectionObserver |
| 3 | **Form + Result** | Validation inline (year 1920-2020, month 1-12, day 1-31), hour dropdown with 12 canh chi labels, loading spinner, 7 animated confidence bars |
| 4 | **Products** | 39 products from GET /api/products, featured items (VIP/COMBO) marked with ⭐ badge, fallback 6 items |
| 5 | **Testimonials** | 3 fictional cards with 5★ stars, avatar initials, italic quotes |
| 6 | **FAQ** | 6-item accordion with chevron rotation animation, single-open behavior |
| 7 | **Footer** | 3-column grid: brand + links + contact, dark gray #1A1B1E bg |

### API Integration
- `const API_BASE = 'http://localhost:8139'` — full URL because static file served outside Flask
- `POST /api/demo` — returns `{paint_points: [{name, confidence, type}], chart_found}`
- `GET /api/products` — returns `[{id, name, price, group, tier, description}]`
- Fallback arrays used when API is unreachable (no crash)

### Scroll Animations
```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, {threshold: 0.1, rootMargin: '0px 0px -40px 0px'});

document.querySelectorAll('.pain-card, .product-card, .testimonial-card, .fade-in').forEach(el => {
  observer.observe(el);
});
```

### CSS Architecture
- Design tokens as CSS custom properties (22 vars)
- Mobile-first: 3 breakpoints (480px / 768px / 1024px)
- Desktop: 3-column for pain/products/testimonials
- Tablet: 2-column
- Mobile: 1-column
- All animations via CSS transitions (no animation library)

### Paint Point Type Colors (Demo Result)
```css
.type-tai-chinh  { background: rgba(0,200,83,0.1); svg color: #00C853; }
.type-gia-dinh   { background: rgba(255,152,0,0.1); svg color: #FF9800; }
.type-suc-khoe   { background: rgba(233,30,99,0.1); svg color: #E91E63; }
.type-tinh-cach  { background: rgba(33,150,243,0.1); svg color: #2196F3; }
.type-su-nghiep  { background: rgba(156,39,176,0.1); svg color: #9C27B0; }
```

### FAQ Accordion Pattern
```html
<div class="faq-item">
  <button class="faq-q">
    <span>Question text</span>
    <i data-lucide="chevron-down"></i>
  </button>
  <div class="faq-a">
    <p>Answer text</p>
  </div>
</div>
```

```js
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});
```

### CSS for FAQ
```css
.faq-a{max-height:0;overflow:hidden;transition:all .3s ease}
.faq-item.open .faq-a{max-height:300px;padding:0 0 18px}
.faq-item.open .faq-q svg{transform:rotate(180deg);color:var(--gold)}
```

### Key Differences from Dark Theme (Bộ Não Phán)

1. **Landing page is now ONE concept with TWO visual themes** — not a replacement
2. Light theme uses Google Fonts (Be Vietnam Pro) + Lucide CDN — adds 2 external requests
3. Light theme adds Testimonials + FAQ sections the dark theme didn't have
4. Dark theme products used inline emoji icons; light uses Lucide SVGs
5. Light theme has full client-side input validation with error messages; dark had none
6. Light theme has IntersectionObserver scroll animations; dark had none
7. Light theme uses `API_BASE` variable; dark used relative path (served via Flask)
