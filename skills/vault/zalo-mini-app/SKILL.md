# Zalo Mini App – Skill Overview

## 🎯 Skill Purpose

Tạo kế hoạch chi tiết và khung code cho **Zalo Mini App** — một ứng dụng mini trong Zalo (ZMS) phục vụ **đặt vé máy bay / tour du lịch** cho ABTrip.

Sản phẩm đầu ra là:
1. **Kế hoạch dự án** (kế hoạch, tasks, milestones)
2. **Code skeleton** (mã source, cấu trúc thư mục)
3. **Tích hợp với Zalo API** (lấy số điện thoại, định danh, chat OA, thanh toán)
4. **Hướng dẫn triển khai** (zmp-cli, ZaUI, build, compile)

## 🔧 Khả năng cốt lõi

### 1. Lập kế hoạch dự án
- Phân tích requirements của Zalo Mini App (đặt vé, lịch bay, vé tour)
- Xác định use cases, user flows, tasks
- Tạo kế hoạch dự án chi tiết (phác thảo, user story, acceptance criteria)
- Đề xuất workflow phát triển (design → code → test → deploy)
- Tích hợp với các skill khác của DSH (Hermes + OpenClaw 2.0)

### 2. Tạo khung code
- Cấu trúc thư mục
- Template skeleton ứng dụng cho các tính năng chính:
  - Trang chủ (chọn từ vé máy bay / tour du lịch)
  - Trang chi tiết (giá, lịch trình, hình ảnh)
  - Trang đặt vé / tour
  - Trang thanh toán (cài đặt ví điện tử)
  - Trang lịch sử đặt vé / tour
  - Tin nhắn chatbot (để xác nhận, nhắc nhở)
- Tích hợp với Zalo OpenAPI (getContact, getProfile, zaloOA, thanh toán)
- Cung cấp ví dụ code và hướng dẫn chạy cục bộ

### 3. Tích hợp Stack kỹ thuật
- **Zalo Mini App (ZMS)** – SDK cho ứng dụng mini
- **Mô hình coding loại agent** – DSH + Hermes + OpenClaw 2.0
- **Custom business layer** – xác thực, quản lý dữ liệu, tích hợp với backend ABTrip
- **Orchestration workflow** – để mở rộng các tasks (viết content, đăng bài)

## 📋 Kế hoạch dự án

### Phase 1: Requirements & Planning (3-4 ngày)
- Phỏng vấn người dùng (product owner) – thu thập yêu cầu, ngân sách, timeline
- Tạo user story (hành động khách hàng, điểm chấp nhận)
- Thiết kế wireframes cho UI/ZaUI của Mini App
- Lập kế hoạch kỹ thuật và lựa chọn công nghệ

### Phase 2: Design & Architecture (2-3 ngày)
- Hướng dẫn sử dụng Zalo OpenAPI (lấy số điện thoại, định danh)
- Thiết kế cơ sở dữ liệu cho người dùng, vé máy bay, lịch sử đặt vé, session chat
- Tích hợp DSH + Hermes + OpenClaw 2.0: AI reasoning, content generation, QA
- Thiết kế workflow backend (dùng Node.js/Express)

### Phase 3: Prototype (4-5 ngày)
- App skeleton
- Tích hợp Zalo ID: getContact, getProfile
- Quy trình đặt vé / tour (thêm vào giỏ hàng, checkout)
- Integration với ZaloOA chatbot (nhắn tin xác nhận, nhắc nhở)
- Hiển thị contact list, chọn from list

### Phase 4: Phát triển đầy đủ (10-12 ngày)
- Bảo trì, sửa lỗi
- Tích hợp ứng dụng web hiện tại của ABTrip (DSH, Hermes, OpenClaw)
- Thiết lập CI/CD (GitHub Actions, test suite)
- Triển khai lên Zalo App Store

### Phase 5: Triển khai & Theo dõi (3-5 ngày)
- Tải lên Zalo App Store
- Tạo mã QR cho Zalo Mini App
- Thiết lập monitoring (APM, Crashlytics)
- Hỗ trợ người dùng ban đầu

## 📁 Cấu trúc thư mục (Code skeleton)

```
zalo-mini-app/
├── src/
│   ├── components/          # Thư viện reusable UI (ZaUI)
│   ├── pages/               # Các trang: Home, Flights, Tours, Booking, Payment, History
│   ├── services/            # API client đến DSH Backend, Zalo OpenAPI
│   ├── stores/              # Zustand/React-Context cho auth, cart, booking
│   ├── hooks/               # custom hooks (useContact, useBooking)
│   ├── utils/               # helper functions (validation, date formatting)
│   ├── styles/              # style định nghĩa (ZaUI)
│   └── .DSHIntegration/      # tích hợp với Hermes + OpenClaw 2.0
├── src/app.json              # thông tin app cho Zalo Mini App
├── src/manifest.json         # manifest cho Zalo App Store
├── package.json             # dependencies
├── README.md                 # hướng dẫn sử dụng
└── CHANGELOG.md

---
backend/
├── api/                     # DSH API layer
│   ├── flight-booking.js    # API cho vé máy bay
│   ├── tour-booking.js      # API cho tour du lịch
│   ├── auth.js              # JWT + SSO
│   └── webhook.js           # webhook cho Zalo OA chatbot
├── jobs/                    # OpenClaw jobs cho content, reminders
├── workers/                 # Hermes reasoning workers
└── database/                # SQLite schema
```

## ⚡ Thiết kế kỹ thuật

### Framework thiết kế cho UI
- **Zalo ZaUI**: Sử dụng JavaScript/TypeScript, tuân theo style sheet Zalo
- **React/18 + ZaUI**: Tạo các component nhanh chóng, tích hợp với Mini App
- **Zustand**: Quản lý state cục bộ (cart, auth)

### Tích hợp backend
- **API layer**: DSH / Hermes / OpenClaw 2.0 (for content, QA, automation)
- **Database**: SQLite trong Mini App (lưu thông tin giỏ hàng, xác thực người dùng)
- **Zalo OpenAPI**:
  - `getContact` – list contacts từ người dùng
  - `getProfile` – thông tin cá nhân
  - `sendMessage` – chat OA cho xác nhận đặt vé
  - `paymentFlow` – thanh toán trong Zalo Mini App

### Orchestration với DSH + Hermes + OpenClaw
- **Hermes**: AI reasoning (nếu chọn flight/tour, giải thích best flight, recommend)
- **OpenClaw 2.0**: Content marketing automation (tự động tạo content cho booking flow)
- **DSH**: QA, verification, orchestration (chạy nền, điều phối tasks)

## 🛠️ CLI + Build

### Khởi động dev (PowerShell)
```powershell
# Từ thư mục src/
# ZiT (Zalo Integrated Tools) – sử dụng Zalo zmp-cli
zmp dev
sudo npm install
npm start
# Mở Zalo Mini App trên điện thoại
# Quét QR code
```

### Build
```bash
zmp build
# Output vào thư mục ./dist/
# Tích hợp với H5 App (có khả năng native)
```

### Kiểm tra
```bash
npm run test
zmp test --coverage
```

## 📊 Ma trận quyết định

| Decision Point | Option 1 | Option 2 | Chọn | Impact |
|----------------|----------|----------|-------|--------|
| Language | TypeScript | JavaScript | TypeScript (Recommended) | Type safety, hiện đại |
| State management | Zustand | Redux | Zustand (Được đề xuất) | Cấu trúc đơn giản, có thể kết hợp với ZaUI |
| Backend API | DSH (OpenAPI) | Rest JSON | DSH (Đã có sẵn) | Giảm repetitive work, AI reasoning |
| Chatbot Zalo | SMS gửi tin nhắn | Zalo OA (Linh hoạt) | Zalo OA (Recommended) | Tích hợp với DSH + Hermes |
| AI content generation | Kết hợp với Hermes + OpenClaw 2.0 | Truyền thống (human) | Herme + OpenClaw 2.0 (Được đề xuất) | Giảm effort viết content, đảm bảo giọng điệu brand |

## 🎯 Kết quả đầu ra (Code implementation)

### 1. Kế hoạch dự án (MS Word / GitHub issue)
- Kế hoạch, timeline, tasks, assignees
- Acceptance criteria chi tiết cho mỗi user story
- Product backlog được định dạng chuẩn

### 2. Code skeleton (GitHub repo)
- `README.md` – hướng dẫn sử dụng và các bước chạy dev
- `package.json` – scripts (dev, test, build)
- `src/app.json` – thông tin app cho Zalo Mini App
- Các file template cho mỗi page (Home.tsx, FlightDetail.tsx...)
- Tích hợp với .env (credentials, API URLs)

### 3. Tích hợp với DSH stack
- Tích hợp với GitHub repo hiện tại (projects/abtrip-marketing/)
- Self-contained workflow: Hermes → generate recommendations → OpenClaw → post promotion cho đặt vé → DSH → QA

### 4. Hướng dẫn triển khai
- `DEPLOYMENT.md` – cách deploy lên Zalo App Store
- `MONITORING.md` – các chỉ số (lượt đặt vé thành công, N/A, CA)
- `UPGRADE.md` – các bước nâng cấp với phiên bản mới

## 🧪 Testing

### Unit testing
```bash
npm run unit:coverage
```

### E2E testing (Zalo Mini App)
```bash
zmp test --e2e
```

### Tích hợp với DSH QA
```bash
# Chạy AI QA trên content (ví dụ: xác nhận tone)
zmp ai-qa --content="content" --brand=ABTrip
```

## 🎨 Thiết kế UI (ZaUI Style)

### Các component tiêu chuẩn
- Button – `zmp-btn` (xác nhận, thanh toán)
- Card – `zmp-card` (hiển thị thông tin flight/tour)
- Input – `zmp-input` (form booking)
- Select – `zmp-select` (chọn from contact list)
- List – `zmp-list` (contact list, flight list)

### Color Palette (Kết hợp brand ABTrip)
```css
--primary: #1A3A5C; /* Deep Navy */
--accent: #E8772E;   /* Vibrant Orange */
--background: #F9F9F7; /* Soft Pearl */
--text-primary: #2C2C2C;
```

## 🚀 Lịch trình triển khai (Sprint-based)

|Sprint|Duration|Goal|Deliverables|Acceptance Criteria|
|------|--------|----|-------------|-------------------|
| Sprint 1 | 3 ngày | Core Mini App (Home, Flights, Tours) | Code skeleton, app.json | Các trang cơ bản hiển thị | [ ] Home page hiển thị banner, 2 mục chính (Vé Máy Bay, Tour Du Lịch) |
| Sprint 2 | 4 ngày | Detail pages, Contact list | Chi tiết flight, form booking | [ ] Chọn từ contact thành công, gửi tin nhắn xác nhận |
| Sprint 3 | 3 ngày | Thêm vào giỏ hàng, Thanh toán | Checkout flow, webhoock sang backend | [ ] Quy trình thanh toán hoàn tất, gửi email xác nhận |
| Sprint 4 | 4 ngày | Tích hợp với DSH + Hermes + OpenClaw 2.0 | Post tự động, content bot | [ ] Content theo tone brand được đăng lên các kênh social |
| Sprint 5 | 3 ngày | Kiểm tra, QA, triển khai | CI/CD, test coverage | [ ] Không có lỗi bugs nghiêm trọng, coverage ≥80% |
| Sprint 6 | 3 ngày | Deployment lên Zalo App Store | App live, QR code, user onboarding | [ ] App sẵn sàng trên Zalo App Store, user có thể đăng ký thử |

## ✅ Success Metrics

- **Product-Metric**: 
  - Conversion rate (CR) cho đặt vé: ≥15%
  - Average Revenue Per User (ARPU): ≥$250
- **User-Metric**:
  - Daily Active Users (DAU): ≥3k
  - Session duration: ≥5 phút
- **Technical**: 
  - Thời gian tải trang: <2 giây
  - Khả năng tương thích với Zalo OA: 99%
- **Quality**:
  - Content quality score: ≥4.5/5 (DSH QA)
  - Tỷ lệ lỗi: <0.5%

## 🛡️ Risk & Mitigation

| Risk | Level | Impact | Mitigation |
|------|-------|--------|------------|
| Khả năng tương thích với Zalo API | Cao | Bị từ chối hoặc chậm trễ | Luôn test trên môi trường sandbox | [ ] Có sẵn backlog cho mỗi thay đổi |
| Tích hợp backend chậm trễ | Trung bình | Thành phẩm không đồng bộ | Sử dụng GraphQL, caching (Redis) |
| Tone content không đúng brand | Trung bình | Giảm lòng tin tưởng của khách hàng | DSH QA + Hermes + content generator automation |

## 📚 Tài liệu tham khảo

- **Zalo Mini App Documentation** – https://developers.zalo.me/docs/miniapp
- **ZaUI Component Library** – https://za-ui.zalo.design
- **DSH + Hermes + OpenClaw 2.0 Integration Guide** – (Có sẵn trong repo DSH)
- **DevOps & CI/CD** – GitHub Actions workflow (`.github/workflows/ci.yml`)

## 🎖️ Grant milestone achievements

- [ ] **Phase 1**: Hoàn thành kế hoạch dự án + code skeleton + design app.json
- [ ] **Phase 2**: Hoàn thành tích hợp backend + Zalo OpenAPI
- [ ] **Phase 3**: Hoạt động MVP (Home → Detail → Booking → Payment)
- [ ] **Phase 4**: Hoàn tất tích hợp DSH + Hermes + OpenClaw 2.0
- [ ] **Phase 5**: Triển khai lên Zalo App Store

## 📧 Liên hệ

- **Chủ sở hữu dự án**: ABTrip Product Manager
- **Technical lead**: Backend Engineer (DSH + Hermes)
- **QA**: DSH + OpenClaw 2.0 automation team
- **Hỗ trợ người dùng**: Zalo OA (support@abtrip.vn)

---

*Skill này được duy trì và cập nhật bởi team **Zalo Mini App** thuộc **DSH + Hermes + OpenClaw 2.0 Marketing Automation Team***

**Sẵn sàng để bắt đầu: Input: yêu cầu từ Product Owner hoặc User, Output: kế hoạch + code skeleton cho Zalo Mini App**