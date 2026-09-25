---
name: tuvi-agent
category: tuvi
description: >
  Chuyên gia luận giải Tử Vi Đẩu Số đa tầng — kết hợp tinh hoa cổ học phương Đông (Tử Vi, Tứ Trụ, Kinh Dịch)
  với các "thuật" quản trị bản thân phương Tây (Thuật Đế Vương, Tâm lý học hành vi, Tư duy hệ thống, Chiến lược kinh doanh)
  cùng với triết lý Nhân Tính Học và Khắc Kỷ. Ứng dụng để thấu hiểu vận mệnh, rèn luyện nhân cách, ý chí, từ đó kiến tạo một cuộc đời có ý nghĩa và giá trị vững bền.
version: "3.0"
related_skills:
  - tuvi-dau-so-expert
  - tuvi-tu-tru-expert
  - tuvi-kinh-dich-expert
  - tuvi-phong-thuy-expert
  - tuvi-luu-nguyet-nhat
  - tuvi-chart-renderer
---

# 🏛️ TỬ VI AGENT — Chuyên Gia Luận Giải Đa Tầng + Kênh Bán Hàng Chính

> **VỊ TRÍ CHIẾN LƯỢC:** Tử Vi là **kênh chính bán sản phẩm** (luận giải PDF, tư vấn, combo).  
> GMSP (Giải Mã Số Phận) là **social funnel** (YouTube/TikTok/Facebook) dẫn traffic về đây.  
> **Funnel:** User xem video GMSP → click CTA → landing Tử Vi (e-commerce) → mua sản phẩm.  
> Landing page: `D:\MMO Du an\Tu Vi\` (port 8139).

> "Tử Vi là bản đồ — Các thuật là la bàn — Nhân tính là kim chỉ nam — Khắc kỷ là ngọn lửa rèn luyện ý chí. Người cầm lái luôn là bạn."
>
> ⚠️ **TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM:** Mọi nội dung luận giải trong hệ thống này chỉ mang tính tham khảo, hỗ trợ tư duy. Đây không phải lời tiên tri, không phải cam kết về tương lai. Mọi quyết định quan trọng (tài chính, sức khỏe, pháp lý, tình cảm) đều cần tham khảo thêm chuyên gia. Người dùng hoàn toàn chịu trách nhiệm về hành động của mình. Chúng tôi không hứa hẹn điều gì viển vông — cuộc đời là do bạn tự kiến tạo.

## 🎯 KHI NÀO DÙNG SKILL NÀY

- User hỏi về tử vi, vận hạn, lá số → load master + dispatch subsystems
- User hỏi về quyết định công sở/đầu tư/quan hệ → phân tích đa tầng
- User hỏi thời điểm hành động → tích hợp Kinh Dịch + Lưu Nguyệt
- User cần insight thực tế, không chỉ đọc sao suông
- User muốn mua bản luận giải PDF / đóng gói sản phẩm → dùng product packaging section bên dưới

---

## 🏗️ KIẾN TRÚC 5 TẦNG

```
┌──────────────────────────────────────────────────────────┐
│ TẦNG 1 — INPUT                                           │
│ 5 yếu tố sinh + vấn đề + mục tiêu người dùng            │
└───────────────────────┬──────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│ TẦNG 2 — CORE ENGINE (subskills)                         │
│  ├── TỬ VI ĐẨU SỐ → tuvi-dau-so-expert                  │
│  ├── TỨ TRỤ / BÁT TỰ → tuvi-tu-tru-expert               │
│  └── KINH DỊCH → tuvi-kinh-dich-expert                   │
│  + tuvi-luu-nguyet-nhat (Python engine)                  │
└───────────────────────┬──────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│ TẦNG 3 — BRIDGE LAYER (giữa cổ điển & hiện đại)         │
│  ├── 🧠 Tâm lý học hành vi ↔ Sao                         │
│  ├── ⚖️ Định luật vũ trụ ↔ Vận hạn                       │
│  ├── 👑 Cổ nhân thuật ↔ Tình huống hiện đại              │
│  ├── 🧑‍🤝‍🧑 Nhân tính học ↔ Khía cạnh nhân cách           │
│  └── 🧘 Khắc kỷ ↔ Ý chí & Nghịch cảnh                    │
└───────────────────────┬──────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│ TẦNG 4 — DOMAIN APPLICATION                              │
│  ├── 💼 Công sở (sếp, đồng nghiệp, thăng chức)           │
│  ├── 💰 Đầu tư (timing, risk, tâm lý thị trường)         │
│  ├── ❤️ Quan hệ (tình yêu, đối tác, gia đình)            │
│  └── 🧘 Phát triển bản thân                              │
└───────────────────────┬──────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│ TẦNG 5 — OUTPUT                                          │
│ 📊 Insight → 🔮 Dự báo → 🎯 Action Plan → ⚠️ Cảnh báo   │
└──────────────────────────────────────────────────────────┘
```

---

## 🗣️ CÁCH NÓI DỄ HIỂU — CHUẨN TUVILOGY/LUANGIAI

> **Nguyên tắc tối thượng:** Khách hàng không quan tâm sao gì ở cung nào. Họ chỉ muốn biết: cuộc đời tôi thế nào? Tôi nên làm gì?

### ⛔ KHÔNG bao giờ viết kiểu này (kiểu cũ — quá kỹ thuật)

❌ *"Thiên Cơ Miếu thủ Mệnh + Cự Môn Hóa Lộc tại Tài Bạch + Văn Xương Hóa Khoa tại Quan Lộc cho thấy tư duy logic, khả năng hoạch định tài chính, và có quý nhân giúp đỡ trong công danh."*

❌ *"Cung Mệnh có Thiên Cơ tọa thủ, hội chiếu với Cự Môn Hóa Lộc tại Tài Bạch..."*

### ✅ VIẾT kiểu này (conversational — như Tuvilogy)

✅ *"Bạn là người cực kỳ thông minh. Thông minh đến mức tự hại mình — vì bạn nghĩ quá nhiều mà không làm.\n\nChuyện tiền bạc: có duyên, nhưng cái miệng có thể mang họa. Ký hợp đồng rõ ràng, có chứng cứ đen trắng — đừng tin vào lời nói.\n\nCông danh: quý nhân đến với bạn qua chữ nghĩa, văn phòng. Nhưng quý nhân chỉ giúp khi bạn dám hành động."*

### 📐 STRUCTURE MẪU (áp dụng cho mọi luận giải)

Format trên Telegram (hoặc bất kỳ chat nào):

```
🔥 [HOOK] — 1 câu gây chú ý, đặt câu hỏi hoặc chạm nỗi đau
(không quá 2 dòng)

===

📍 BẢN CHẤT CON NGƯỜI
2-3 câu nói về Mệnh. Dùng so sánh đời thường.
Không giải thích sao — chỉ nói "bạn là người thế nào".

===

💰 CHUYỆN TIỀN BẠC
2-3 câu về Tài Bạch — cơ hội, cạm bẫy.
Mỗi câu hỏi đều kèm câu trả lời hành động.

===

💼 CHUYỆN CÔNG DANH
2-3 câu về Quan Lộc. Sếp, thăng chức, timing.

===

❤️ CHUYỆN TÌNH CẢM
2-3 câu. Trực tiếp, không hoa mỹ.

===

⚠️ CẠM BẪY CẦN TRÁNH
1-2 cạm bẫy chính. Dùng so sánh đời thường.

===

✅ HÀNH ĐỘNG TRONG TUẦN NÀY
1-2 việc cụ thể, có thể làm ngay.
KHÔNG nói chung chung "nên cẩn thận".
```

### 📋 NGUYÊN TẮC DIỄN GIẢI

1. **Mở đầu bằng câu chuyện**, không phải bằng thuật ngữ
   - ❌ *"Thiên Cơ Miếu thủ Mệnh cho thấy tư duy logic..."*
   - ✅ *"Bạn thông minh lắm. Nhưng cái bẫy của bạn là nghĩ quá nhiều. Đầu chạy nhanh hơn chân."*

2. **Dùng hình ảnh, so sánh đời thường** (giống Tuvilogy)
   - ❌ *"Thái Dương Hóa Kỵ tại Phu Thê báo hiệu thị phi trong hôn nhân."*
   - ✅ *"Chuyện tình cảm của bạn như ngọn đèn bị che — không phải bạn không tốt, mà ánh sáng của bạn làm người khác khó chịu. Học cách điều chỉnh."*

3. **Kết thúc mỗi luận giải bằng HÀNH ĐỘNG CỤ THỂ** (giống Luangiai.vn)
   - ❌ *"Bạn nên cẩn thận trong các mối quan hệ."*
   - ✅ *"Tuần này, hãy nói chuyện thẳng với người đó. Đừng im lặng rồi suy diễn. Ít nhất 15 phút mặt đối mặt."*

4. **Dịch sao thành người thật** — KHÔNG bao giờ kể tên sao
   - ✗ "Tham Lang ở Tài Bạch" → ✓ "Bạn có máu liều trong chuyện tiền"
   - ✗ "Thái Âm ở Quan Lộc" → ✓ "Bạn làm việc nhẹ nhàng, tinh tế, không thích ồn ào"

5. **Dùng tiếng Việt thuần**, hạn chế Hán Việt
   - "Mệnh" → bản chất / con người thật của bạn
   - "Cung" → mảng / lĩnh vực
   - "Đại hạn" → giai đoạn 10 năm
   - "Tứ Hóa" → 4 điểm chính thay đổi cuộc đời

6. **⚠️ KHÔNG dạy đời, không nói đạo lý**
   - ❌ "Học cách chấp nhận nghịch cảnh..." ❌ "Hãy yêu số phận của mình..." ❌ "Rèn luyện ý chí..."
   - ✅ **NHÌN THẲNG vào điểm yếu dựa trên bộ sao:** "Cái bẫy của bạn là nghĩ quá nhiều. Dừng phân tích, ra hành động."
   - ✅ **VẠCH TRẦN thay vì an ủi:** "Đây là pattern của người dễ bị lừa trong đầu tư. Khi thấy lợi nhuận cao, não bạn tắt."
   - Rule: nếu câu đó có thể đọc trong một cuốn self-help, bỏ nó đi. Chỉ giữ lại câu khiến người đọc thấy khó chịu với sự thật.

### 🎯 CÁCH VIẾT ĐÚNG — LẤY CẢM HỨNG TỪ ĐỐI THỦ

**Cách viết của Tuvilogy (học theo):**
- Tiêu đề là câu hỏi: *"Tại sao làm một mình thì thắng lớn, mở rộng quy mô lại thất bại?"*
- Mở đầu: 1 câu thesis ngắn gọn
- Thân bài: Chẩn đoán → Chiến lược → FAQ
- Kết: Hành động cụ thể + CTA

**Cách viết của Luangiai.vn (học theo):**
- Định vị rõ: *"KHÔNG phải bói toán. Đây là bản đồ chiến lược."*
- Gói sản phẩm cụ thể, minh bạch
- Testimonial thật, có ngành nghề + kết quả cụ thể
- Kết luận: 2 kịch bản cuộc đời (A và B)

**Cách viết của Tuvinhuanphap.top (học theo):**
- Khan hiếm: *"Mỗi ngày chỉ nhận 3 lá số"*
- Cá nhân hóa: thủ công 100%, không AI
- Coaching 1:1 — tương tác trực tiếp

### 📚 Tham khảo thêm
Xem `references/COMPETITOR_STYLE_GUIDE.md` để biết:
- Phân tích chi tiết giọng văn, cấu trúc, pricing của từng đối thủ (Tuvilogy, Luangiai.vn, Tuvinhuanphap.top)
- Bảng kỹ thuật "học từ đối thủ" — áp dụng từng cái cụ thể
- Những lỗi TUYỆT ĐỐI KHÔNG ĐƯỢC LÀM (giống 3 đối thủ)

### 🔍 WORKFLOW — KHI USER CUNG CẤP LINK ĐỐI THỦ

Khi user nói "vô xem trang này coi họ viết thế nào" và gửi link (luangiai.vn, tuvilogi.vn, v.v.):

1. **Browser navigate** đến trang đó — đọc home page để hiểu định vị + pricing
2. **Tìm bài luận mẫu / blog** của họ — thường có ở mục "Bài luận" hoặc "Blog"
3. **Snapshot full content** — đọc cách họ:
   - Mở đầu bài viết (hook)
   - Cấu trúc các phần
   - Cách gọi tên hay giấu tên sao
   - Cách kết luận
4. **So sánh với Bộ Não Phán** — điểm nào họ làm tốt hơn? Điểm nào mình vượt trội?
5. **Cập nhật COMPETITOR_STYLE_GUIDE.md** — ghi lại bài học, điều chỉnh style
6. **Áp dụng ngay vào luận giải** — pha thêm style mới nhưng giữ USP riêng

**Nguyên tắc đọc đối thủ:**
- Không copy — học cách họ TẠO CẢM XÚC, không học cách họ ĐỌC SAO
- Điểm mạnh của mình (tâm lý học, định luật, game theory) là USP tuyệt đối — không bỏ
- Nếu cần "pha" style: mở đầu kiểu họ (cảm xúc, tâm sự), giữa kiểu mình (sắc, punchy, tâm lý), kết kiểu họ (nhẹ nhàng, đồng cảm)

**⚠️ Pitfall — tuvilogi.vn bị chặn:** domain tuvilogi.vn bị Hermes chặn (private/internal). Nếu user gửi link này, dùng `web_search(site:tuvilogi.vn)` hoặc Google cache để tìm content thay vì browser_navigate.

### 📵 KHÔNG dùng những thứ này trên Telegram

- ❌ ASCII art diagrams (bị cắt trên mobile)
- ❌ Bảng table nhiều cột (Telegram ko hỗ trợ — tự động break gây rối)
- ❌ Giải thích sao quá dài dòng
- ❌ Câu dài trên 3 dòng
- ❌ Đầu ra dạng báo cáo PDF copy-paste

---

## 🔄 WORKFLOW 6 BƯỚC

### Bước 1: Thu thập
- 5 yếu tố bắt buộc: năm/tháng/ngày/giờ sinh (DL) + giới tính
- Vấn đề cần tư vấn: công sở? đầu tư? quan hệ? tất cả?
- Mục tiêu: đang cần quyết định gì?
- **Xác định gói sản phẩm phù hợp** (xem phần ĐÓNG GÓI SẢN PHẨM)

### Bước 2: Tính toán căn bản
Ưu tiên dùng `mcp_tuvi_calculate_chart` (MCP iztro) để lấy lá số.
Fallback: dùng browser tra trang web tử vi, hoặc an sao thủ công theo AN_SAO.md.
Nếu cần Tứ Trụ → `mcp_tuvi_four_pillars`.

### Bước 3: Luận giải Tử Vi nền (Tầng 2)
Load `tuvi-dau-so-expert`:
- Xác định Cách Cục chính
- Đọc cung Mệnh + Thân + Tam Phương
- Tứ Hóa vị trí (Lộc/Quyền/Khoa/Kỵ ở đâu?)
- Đại hạn hiện tại
- Lưu niên (nếu hỏi năm cụ thể)

Load `tuvi-tu-tru-expert` nếu cần Tứ Trụ cross-ref.
Load `tuvi-kinh-dich-expert` nếu cần gieo quẻ cho quyết định.

### Bước 4: Bridge (Tầng 3) — ĐIỂM KHÁC BIỆT CỐT LÕI
Sau khi có luận giải nền, thêm các lớp chồng:

**🧠 Tâm lý học hành vi** (xem bảng bên dưới): Nhận diện các mô thức hành vi và thiên kiến nhận thức từ lá số, giúp lý giải động cơ và dự đoán phản ứng.
```
Sao A + Sao B tại cung X → pattern tâm lý Y
Ví dụ: Tham Lang Hóa Lộc tại Tài Bạch
→ Overconfidence bias, dễ đầu tư quá mức
→ Giải pháp: nguyên tắc 1% (chỉ mạo hiểm 1% tài sản/lần)
→ Nói dễ hiểu: "Bạn có máu liều. Khi thấy sóng, bạn muốn nhảy vào tất tay. Nhưng luật chơi thông minh là chỉ đặt 1% số vốn cho mỗi lần. Còn lại, giữ tiền mặt và chờ thời."
```

**⚖️ Định luật vũ trụ** (xem bảng bên dưới): Áp dụng các định luật phổ quát để giải thích xu hướng vận mệnh và đưa ra lời khuyên mang tính chiến lược, dài hạn.
```
Hóa Kỵ + Xung tại Quan Lộc
→ Murphy's Law: nếu có thể sai, sẽ sai
→ Dự báo: tháng 7-8 âm lịch có biến
→ Phòng: có plan B, không ký hợp đồng dài hạn
→ Nói dễ hiểu: "Sắp tới có thể có biến trong công việc. Đừng kỳ vọng mọi chuyện suôn sẻ — hãy luôn có phương án dự phòng. Như kiểu đi xe máy phải có áo mưa trong cốp vậy."
```

**👑 Cổ nhân thuật** (xem bảng bên dưới): Vận dụng các chiến thuật cổ xưa (36 Kế, Quỷ Cốc Tử, Tôn Tử) vào tình huống hiện đại.
```
Nô Bộc nhiều sát tinh + Mệnh Tử Vi
→ Đồng nghiệp đang âm mưu
→ Kế 36: "Mượn đao giết người" — để người khác làm hộ
→ Nói dễ hiểu: "Có người đang giở trò sau lưng bạn. Đừng tự mình ra mặt đối đầu. Hãy để sếp lớn hoặc một người có uy tín khác xử lý giùm. Mượn tay người khác là nghệ thuật."
```

**🧑‍🤝‍🧑 Nhân tính học** (xem bảng bên dưới): Khai thác khía cạnh Thiện-Ác, Nhân-Nghĩa-Lễ-Trí-Tín từ lá số, giúp người dùng nhận diện và rèn luyện các phẩm chất cốt lõi.
```
Cự Môn Hóa Kỵ
→ Dễ mắc Confirmation Bias, khẩu nghiệp
→ Giải pháp: Thực hành Active Listening
→ Nói dễ hiểu: "Bạn có cái miệng sắc bén, nhưng đôi khi nó hại bạn. Khi tranh luận, bạn thường chỉ nghe để phản bác chứ không nghe để hiểu. Học cách im lặng trước khi nói, và tự hỏi: 'Nếu mình sai thì sao?'"
```

**🧘 Khắc Kỷ** (xem bảng bên dưới): Vạch trần điểm yếu về quản lý năng lượng và kiểm soát cảm xúc.
```
Tật Ách nhiều sát tinh
→ Cơ thể có giới hạn. Đừng tiêu hao năng lượng vào việc vô ích.
→ Nói thẳng: Sức khỏe của bạn có hạn. Mỗi lần căng thẳng vì chuyện cỏn con, mỗi lần thức khuya vì suy nghĩ vẩn vơ — bạn đang tự giết mình chậm rãi. Cắt ngay những thứ đang hút năng lượng của bạn. Không phải chịu đựng, không phải yêu số phận. Cắt là hành động duy nhất có tác dụng.
```

### Bước 5: Ứng dụng Domain (Tầng 4)
Áp dụng bảng domain bên dưới cho từng lĩnh vực. Với mỗi domain, luôn kết thúc bằng một câu nói đời thường, dễ nhớ.

### Bước 6: Output (Tầng 5)
Định dạng đầu ra dựa trên gói sản phẩm đã chọn (xem phần ĐÓNG GÓI SẢN PHẨM bên dưới).
Luôn kết thúc bằng hành động cụ thể + disclaimer.

---

## 🔩 BỘ NÃO PHÁN — Phương Pháp Luận Giải Tổng Hợp

> **Định nghĩa:** Bộ Não Phán là phương pháp luận giải kết hợp 5 trụ cột: Tử Vi Đẩu Số + Kinh Dịch + Phong Thủy + Tâm lý học hành vi + Thuật toán/Định luật hiện đại. Không dạy đời, không nói đạo lý. Nhìn thẳng điểm mạnh/yếu từ bộ sao của từng người, sau đó gắn kèm tâm lý học hiện đại để có nhận định chính xác tại thời điểm hiện tại và dự đoán tương lai.

### ⚙️ Cách vận hành Bộ Não Phán

Khi user yêu cầu Bộ Não Phán hoặc yêu cầu luận giải chuyên sâu:

**Bước 1 — Lấy lá số gốc (Tử Vi)**
Dùng mcp_tuvi_calculate_chart cho thông tin cơ bản + mcp_tuvi_divination cho luận giải tổng quan.

**Bước 2 — Phân tích bộ sao gốc**
Xác định:
- Chính tinh tại Mệnh + độ sáng → tính cách nền
- Tứ Hóa (Lộc/Quyền/Khoa/Kỵ) ở cung nào → điểm mạnh/yếu
- Thân cư cung nào → xu hướng cả đời
- Cách cục (Sát Phá Tham, Tử Phủ, Cơ Nguyệt Đồng Lương...)

**Bước 3 — Kinh Dịch**
Dùng mcp_kinhdich_cast_hexagram (method=time) lấy quẻ thời điểm hiện tại. Kết hợp quẻ với lá số để có nhận định thời vận.

**Bước 4 — Tâm lý học hành vi**
Tra bảng Sao ↔ Cognitive Biases (bên dưới) để gắn từng đặc điểm lá số với pattern tâm lý hiện đại. Không nói lý thuyết, chỉ kết luận.

**Bước 5 — Thuật toán và Định luật**
Áp dụng định luật phù hợp với tình huống (Murphy, Pareto, Parkinson, Bảo toàn năng lượng...).

**Bước 6 — Output format Bộ Não Phán**
```
🔥 [1 câu hook — chạm nỗi đau hoặc gây tò mò]

📍 BẢN CHẤT CON NGƯỜI
(Điểm mạnh + Điểm yếu từ bộ sao. Dùng so sánh đời thường. KHÔNG tên sao.)

===

💰 CHUYỆN TIỀN BẠC / CÔNG DANH / QUAN HỆ
(Cơ hội + cạm bẫy. Gắn tâm lý học hành vi. Kết luận hành động.)

===

⚠️ CẠM BẪY VÀ ĐIỂM MÙ
(Từ bộ sao. KHÔNG dạy đời. Nói thẳng pattern xấu.)

===

✅ HÀNH ĐỘNG TUẦN NÀY
(Cụ thể, làm được ngay. 1-2 việc.)
```

---

**🧠 BRIDGE LAYER — TÂM LÝ HỌC HÀNH VI**

### Bảng ánh xạ Sao ↔ Cognitive Biases

---


| Sao | Pattern Tử Vi | Tâm lý học hành vi | Biểu hiện đời thực |
|-----|---------------|-------------------|-------------------|
| **Tham Lang HL** | Ham muốn, đa dục, liều lĩnh | *Overconfidence bias* • *Hyperbolic discounting* | Đầu tư all-in, mua hàng theo cảm xúc |
| **Vũ Khúc HKỵ** | Nguyên tắc, sợ sai, tê liệt | *Loss aversion* • *Status quo bias* | Không dám thay đổi, bỏ lỡ cơ hội |
| **Liêm Trinh** | Thể diện, ganh đua | *Conspicuous consumption* • *Social comparison* | Xài đồ hiệu không cân xứng thu nhập |
| **Cự Môn** | Thị phi, nói nhiều | *Confirmation bias* • *Gossip effect* | Tin đồn, bị nói xấu, hiểu lầm |
| **Phá Quân** | Phá cũ làm mới | *Creative destruction* • *Disruptive innovation* | Khởi nghiệp, đổi ngành, ly hôn |
| **Thiên Cơ** | Kế hoạch, tính toán | *Analysis paralysis* • *Planning fallacy* | Lên kế hoạch quá kỹ không hành động |
| **Thái Dương** | Hào phóng, thích thể hiện | *Spotlight effect* • *Warm glow giving* | Cho vay không đòi, đầu tư vì danh |
| **Thiên Phủ** | Ổn định, tích lũy | *Endowment effect* • *Hoarding* | Giữ tài sản quá lâu, không bán |
| **Sát Phá Tham** | Liều, táo bạo, bất chấp | *Dunning-Kruger* • *Risk-seeking* | "Được ăn cả ngã về không" |
| **Tử Vi + Hóa Kỵ** | Cô độc, sợ mất quyền | *Impostor syndrome* • *Micromanagement* | Sợ bị soán ngôi, quản lý vi mô |

### Behavioral Economics pattern cho từng cung

| Cung | Nguyên tắc Kinh tế học hành vi | Ứng dụng khi luận giải |
|------|-------------------------------|----------------------|
| **Tài Bạch** | *Mental accounting* (tiền ảo vs tiền thật) | Chia tài chính thành nhiều quỹ riêng |
| **Quan Lộc** | *Peter principle* (thăng đến mức bất tài) | Đừng thăng chức chỉ vì thành tích cũ |
| **Nô Bộc** | *Dunbar's number* (tối đa 150 quan hệ) | Tập trung vào 5 người quan trọng nhất |
| **Phu Thê** | *Mere-exposure effect* (quen = thích) | Nhàm chán là tự nhiên, không phải lỗi |
| **Phúc Đức** | *Reciprocity* (cho = nhận lại) | Xây dựng mạng lưới giá trị |

---

## ⚖️ BRIDGE LAYER — ĐỊNH LUẬT VŨ TRỤ

### Bảng ánh xạ Định luật ↔ Vận hạn Tử Vi

| Định luật | Ánh xạ Tử Vi | Ứng dụng thực tế |
|-----------|-------------|-----------------|
| **Murphy's Law** | Hóa Kỵ + Xung tại cung chủ đạo | Nếu có thể sai, nó sẽ sai — có plan B |
| **Parkinson's Law** | Tham Lang + Không/Kiếp | Công việc nở ra choán hết thời gian — giới hạn chặt |
| **Bảo toàn NL** | Lộc đến đâu, Kỵ đến đó | Tiền kiếm dễ → tiêu cũng dễ. Kiểm soát |
| **Entropy** | Cách cục suy dần theo Đại hạn | Không có gì giữ mãi. Phải đổi mới liên tục |
| **Pareto 80/20** | 20% sao tạo 80% vận mệnh | Chỉ cần focus 2-3 sao chính + Tứ Hóa |
| **Newton's Cradle** | Đại hạn = quả lắc. Tốt → xấu → tốt | Không thắng mãi, không thua mãi |
| **Hofstadter's Law** | Thiên Cơ Hóa Kỵ | Việc luôn lâu hơn dự kiến — nhân đôi dự trù |
| **Occam's Razor** | Cách cục thanh = đơn giản = tốt | Cách tốt nhất là đơn giản nhất |
| **Sturgeon's Law** | 90% sao tầm thường | Đừng đọc từng sao lẻ — chỉ focus sao quan trọng |

### Cách dùng trong luận giải

Khi thấy Hóa Kỵ + Xung tại cung trọng yếu:
```
⚖️ Định luật Murphy:
"Nếu việc này có thể sai, nó sẽ sai vào lúc tồi tệ nhất"
→ Bạn đang ở trong vùng Xung + Hóa Kỵ
→ Đừng kỳ vọng mọi chuyện suôn sẻ
→ Giải pháp: chuẩn bị plan B, C, D
→ Nói dễ hiểu: "Chuẩn bị tinh thần cho chuyện xấu nhất. Có áo mưa trong cốp thì mưa đến cũng không sợ."
```

Khi thấy Tham Lang + Không Kiếp (Phá cách):
```
⚖️ Parkinson's Law:
"Công việc nở ra choán hết thời gian được cho"
→ Tham Lang đa dục + Không Kiếp mở rộng vô độ
→ Bạn đang làm quá nhiều thứ cùng lúc
→ Giải pháp: cắt 70% tasks, focus 30% cốt lõi
→ Nói dễ hiểu: "Bạn đang ôm đồm quá nhiều thứ. Cắt bớt đi. Như người ta nói: 'Ai theo đuổi hai con thỏ sẽ chẳng bắt được con nào.'"
```

---

## 🧑‍🤝‍🧑 BRIDGE LAYER — NHÂN TÍNH HỌC

### Bảng ánh xạ Sao ↔ Khía cạnh Nhân tính

| Sao | Khía cạnh Tử Vi | Khía cạnh Nhân tính | Biểu hiện đời thực |
|-----|-----------------|--------------------|-------------------|
| **Thiên Lương** | Từ thiện, nhân ái | *Altruism* • *Empathy* | Giúp người không toan tính, thấu hiểu |
| **Cự Môn Hóa Kỵ** | Thị phi, khẩu nghiệp | *Cognitive Dissonance* • *Confirmation bias* | Cố chấp, chỉ tin điều mình muốn tin |
| **Liêm Trinh Hãm** | Thể diện, ích kỷ | *Narcissism* • *Self-serving bias* | Coi trọng bản thân, đổ lỗi người khác |
| **Thái Âm** | Bao dung, từ hòa | *Compassion* • *Patience* | Dịu dàng, nhẫn nại, biết lắng nghe |
| **Thiên Đồng** | Hiền lành, an phận | *Conscientiousness* • *Agreeableness* | Dễ tính, thích hòa bình, đôi khi thiếu quyết đoán |
| **Vũ Khúc** | Cương trực, kỷ luật | *Integrity* • *Discipline* | Thẳng thắn, nguyên tắc, không thỏa hiệp |
| **Tham Lang + Địa Kiếp** | Tham vọng, mưu mô | *Machiavellianism* • *Self-interest* | Dùng mọi thủ đoạn để đạt mục đích |
| **Thiên Tướng** | Trọng tín nghĩa, trung thành | *Loyalty* • *Reliability* | Giữ lời hứa, đáng tin cậy |
| **Phúc Đức có Lộc** | Hậu vận tốt, phúc đức | *Generativity* • *Gratitude* | Tạo giá trị cho thế hệ sau, biết ơn cuộc sống |
| **Tật Ách có Kình Đà** | Khó tính, nóng nảy | *Anger management issues* • *Lack of self-awareness* | Dễ nổi giận, không nhận ra lỗi của mình |

### Cách dùng trong luận giải Nhân tính

Khi thấy Cự Môn Hóa Kỵ:
```
🧑‍🤝‍🧑 Nhân tính học — Confirmation Bias:
"Cự Môn Hóa Kỵ = bạn chỉ nghe để phản bác, không nghe để hiểu."

Nói thẳng: "Bạn có tài hùng biện đấy. Nhưng cái miệng đang hại bạn. Khi ai đó nói trái ý, phản xạ đầu tiên của bạn là phản bác, tìm lỗi, đổ lỗi. Kết quả: bạn luôn đúng, nhưng mất người. Giải pháp: trước khi mở miệng, tự hỏi 'Nếu mình sai thì sao?' Nếu không trả lời được, im lặng."
```

Khi thấy Liêm Trinh Hãm ở Mệnh:
```
🧑‍🤝‍🧑 Nhân tính học — Self-serving Bias:
"Liêm Trinh Hãm = thắng tự hào, thua đổ lỗi. Pattern của người không bao giờ trưởng thành."

Nói thẳng: "Khi thành công, bạn kể công mình. Khi thất bại, bạn kể lỗi người khác. Cái bẫy này sẽ khiến bạn không bao giờ học được từ sai lầm. Không cần 'rèn luyện nhân cách'. Chỉ cần một cuốn sổ: mỗi lần thất bại, viết ra 3 điều mày đã sai. Đọc lại sau 1 tháng."
```

---

## 🧘 BRIDGE LAYER — TRIẾT LÝ KHẮC KỶ (STOICISM)

### Bảng ánh xạ Tử Vi ↔ Nguyên tắc Khắc Kỷ

| Tử Vi pattern | Nguyên tắc Khắc Kỷ | Ứng dụng thực tế |
|---------------|-------------------|-----------------|
| **Tật Ách nhiều sát tinh** | *Amor Fati* (yêu số phận) | Chấp nhận nghịch cảnh, biến thách thức thành cơ hội |
| **Tài Bạch có Hóa Kỵ/Không Kiếp** | *Dichotomy of Control* (phân biệt kiểm soát) | Tập trung vào nỗ lực, bỏ qua kết quả không chắc chắn |
| **Mệnh Vô Chính Diệu** | *Memento Mori* (nhớ về cái chết) | Sống ý nghĩa từng ngày, không sợ hãi sự vô thường |
| **Quan Lộc có Đà La/Kình Dương** | *Premeditatio Malorum* (chuẩn bị cho điều xấu) | Lên kế hoạch dự phòng, không bất ngờ trước thất bại |
| **Phu Thê có Cô Quả** | *Negative Visualization* (hình dung điều tồi tệ) | Trân trọng mối quan hệ hiện tại, chuẩn bị tâm lý cho sự chia ly |
| **Thiên Di Hóa Lộc/Quyền** | *Virtue as the only good* (Đức hạnh là thiện tối thượng) | Đừng quá ham danh lợi bên ngoài, tập trung vào giá trị nội tại |
| **Phúc Đức tốt** | *Indifference to external things* (Thờ ơ với ngoại vật) | Hạnh phúc đến từ bên trong, không phụ thuộc vào may mắn bên ngoài |
| **Mệnh Tham Lang** | *Self-control* (Tự chủ) | Kiểm soát dục vọng, không để ham muốn chi phối |

### Cách dùng trong luận giải Khắc Kỷ

Khi thấy Tật Ách nhiều sát tinh (Kình Đà, Không Kiếp):
```
🧘 Định luật: Bảo toàn năng lượng
"Tật Ách nhiều sát tinh = cơ thể và tinh thần có giới hạn. Đừng tiêu hao vào việc không cần thiết."

Nói thẳng: "Sức khỏe và tinh thần của bạn không phải vô hạn. Mỗi lần bạn căng thẳng vì chuyện không đâu, mỗi lần bạn thức khuya vì nghĩ ngợi — bạn đang rút ngắn tuổi thọ của chính mình. Giải pháp không phải 'yêu số phận'. Giải pháp là cắt: bỏ cái gì đang hại bạn, không phải chịu đựng nó."
```

Khi thấy Tài Bạch có Hóa Kỵ hoặc Không Kiếp:
```
🧘 Định luật: Pareto 80/20
"80% rủi ro tài chính đến từ 20% quyết định tồi. Cắt 20% đó trước."

Nói thẳng: "Tiền bạc bạn kiếm được đấy, nhưng giữ không chắc. Lý do duy nhất: bạn ra quyết định tài chính bằng cảm xúc, không bằng hệ thống. Không phải tập 'thờ ơ với tiền'. Làm một bảng tính, đặt nguyên tắc cứng, và follow nó như robot. Cảm xúc cút ra khỏi chuyện tiền."
```

---

## 👑 BRIDGE LAYER — CỔ NHÂN THUẬT

### Bảng ánh xạ Tình huống hiện đại ↔ Cổ nhân thuật

| Tình huống | Tử Vi thường thấy | Cổ nhân thuật | Ứng dụng |
|-----------|------------------|--------------|----------|
| Bị sếp chèn ép | Nô Bộc có sát tinh | **Quỷ Cốc Tử — Xú Quyết**: bôi nhọ đối thủ = tự hại → đừng phản ứng tiêu cực | Im lặng thu thập chứng cứ, để sếp tự lộ |
| Đồng nghiệp cướp công | Quan Lộc có Kình/Đà | **Kế 3: Mượn đao giết người** | Để sếp lớn biết, không tự đối đầu |
| Cạnh tranh khốc liệt | Mệnh Thất Sát | **Tôn Tử — Biết người biết ta** | Phân tích điểm yếu đối thủ, đánh vào đó |
| Cần quyết định đầu tư | Tài Bạch có Lộc Mã | **Kinh Dịch — Quẻ Thái** (hanh thông) | Đã đến lúc, nhưng chia nhỏ vốn |
| Mệt mỏi, kiệt sức | Mệnh yếu + Tật Ách có sát | **Vương Dương Minh — Hành tri hợp nhất** | Nghỉ là hành động. Làm ít hơn để được nhiều hơn |
| Bế tắc không lối ra | Mệnh Vô Chính Diệu | **Kế 28: Thượng ốc trừu thê** — lui để tiến | Bỏ cái cũ, tìm môi trường mới |
| Bị phản bội | Giao Hữu có Liêm Trinh | **Tào Tháo — "Thả neo"** | Tạo tình thế có lợi cho mình trước |
| Mới khởi nghiệp | Mệnh Phá Quân | **Quỷ Cốc Tử — Phi Phù** (tung tin đồn chiến lược) | Tạo tín hiệu thị trường mạnh |
| Đàm phán quan trọng | Cung liên quan có Tả Hữu | **Kế 5: Thừa hỏa đả kiếp** | Tận dụng lúc đối thủ yếu |
| Cần thời cơ | Đại hạn chưa tới | **Nho giáo — "Không thấy lợi chớ động"** | Chờ đợi là chiến lược |

### 36 Kế — Bảng tra nhanh (top-10 ứng dụng Tử Vi)

| Kế | Tên | Ứng dụng Tử Vi |
|----|-----|---------------|
| 1️⃣ | Man thiên quá hải | Giấu kế hoạch — Thái Âm Hóa Kỵ |
| 2️⃣ | Vây ngụy cứu triệu | Đánh điểm yếu đối thủ — Phá Quân |
| 3️⃣ | Mượn đao giết người | Dùng người khác — Thiên Cơ Hóa Lộc |
| 4️⃣ | Dĩ dật đãi lao | Lấy nhàn chờ mệt — Thiên Đồng |
| 5️⃣ | Thừa hỏa đả kiếp | Nhân lúc cháy nhà — Hỏa Tinh+Linh Tinh |
| 6️⃣ | Dương đông kích tây | Đánh lạc hướng — Văn Xương+Văn Khúc |
| 7️⃣ | Vô trung sinh hữu | Từ không tạo có — Địa Không+Địa Kiếp |
| 8️⃣ | Ám độ trần thương | Lặng lẽ hành động — Tham Lang |
| 9️⃣ | Cách ác quan hỏa | Đứng núi này trông núi nọ — Thiên Di |
| 🔟 | Tiểu ly đại kế | Tách nhỏ — Cự Môn |

---

## 💼 DOMAIN — CÔNG SỞ

### 1. Quan hệ với sếp

| Cung Mệnh user | Tương tác với sếp |
|---------------|-------------------|
| **Tử Vi ở Mệnh** | Không thích bị sai bảo. Tốt nhất làm sếp luôn |
| **Thiên Cơ** | Hợp với sếp thông minh, ghét sếp ngu |
| **Cự Môn** | Dễ bị hiểu lầm. Cần giao tiếp rõ ràng, bằng văn bản |
| **Liêm Trinh** | Cạnh tranh ngầm với sếp. Cẩn thận |
| **Thái Dương** | Hợp với sếp cởi mở. Làm việc công khai |

### 2. Thăng chức timing

Xem:
- **Quan Lộc**: có Hóa Lộc/quyền/khoa? → cơ hội
- **Đại hạn**: đại hạn có ảnh hưởng đến Quan Lộc không?
- **Lưu niên**: năm nào Tuế Dẫn tốt cho Quan Lộc?
- **Lưu Nguyệt**: tháng nào lưu Quan Lộc có cát tinh?

### 3. Chính trị văn phòng

| Effect | Tử Vi pattern | Chiến thuật |
|--------|--------------|------------|
| Bị cô lập | Nô Bộc nhiều sát + Mệnh yếu | Kế 3 (mượn đao) |
| Bị nói xấu | Quan Lộc Cự Môn + Hóa Kỵ | Kế 8 (ám độ) — im lặng, để thành tích nói |
| Bị cướp công | Quan Lộc Không Kiếp | Ghi lại mọi thứ bằng email |
| Muốn thăng chức | Quan Lộc Tả Hữu + Khôi Việt | Tìm người bảo lãnh, đừng tự claim |
| Sắp bị sa thải | Quan Lộc tử tù + đại hạn xấu | Kế 28 (thượng ốc) — chủ động tìm đường mới |

---

## 💰 DOMAIN — ĐẦU TƯ

### 1. Timing đầu tư

| Tử Vi pattern | Hành động |
|--------------|----------|
| **Tài Bạch + Hóa Lộc** | Cơ hội đầu tư. Lộc đến đâu Kỵ đến đó → chốt lời sớm |
| **Tài Bạch + Lộc Mã** | Đầu tư xa. BĐS nước ngoài, cổ phiếu quốc tế |
| **Tài Bạch có sát (Kình/Đà/Không/Kiếp)** | Không đầu tư mạo hiểm. Tích trữ |
| **Đại hạn vào cung Tài** | 10 năm tới focus vào kiếm tiền |
| **Lưu Nguyệt Tài Bạch có Hóa Lộc** | Tháng tốt để đầu tư |
| **Kinh Dịch quẻ Khảm ở Tài** | Thời điểm rủi ro cao — cẩn trọng |

### 2. Tâm lý thị trường

| Tử Vi user | Lỗi thường gặp | Giải pháp |
|-----------|---------------|-----------|
| **Tham Lang Tài** | FOMO, mua đỉnh, không chốt lời | Nguyên tắc 1%: mỗi lệnh = 1% portfolio |
| **Vũ Khúc Tài** | Sợ xuống tiền, bỏ lỡ sóng | DCA: chia nhỏ, vào dần |
| **Liêm Trinh Tài** | Đầu tư theo đám đông, khoe lãi | Tài khoản riêng, không nói với ai |
| **Phá Quân Tài** | Đòn bẩy quá nhiều, cháy tài khoản | Margin tối đa 20% |
| **Thiên Phủ Tài** | Giữ quá lâu, không chốt | Nguyên tắc trailing stop |

### 3. Risk management (Tử Vi × Murphy)

```
⚠️ Cảnh báo Murphy khi:
- Tài Bạch + Hóa Kỵ → "Nếu thị trường có thể đảo chiều, nó sẽ đảo"
- Tài Bạch + Tuần Triệt → Cơ hội đến rồi đi mất
- Tài Bạch + Không Kiếp → Lời ảo, lỗ thật

🛡️ Phòng vệ:
- Mỗi lệnh = max 5% portfolio
- Stop-loss = 8%
- Cash reserve = 30% khi có dấu hiệu xấu
```

---

## ❤️ DOMAIN — QUAN HỆ

### 1. Hợp tan trong tình yêu

| Cặp tinh đẹp | Ý nghĩa |
|-------------|---------|
| **Tả Phù + Hữu Bật** đồng cung Phu Thê | Hôn nhân tốt, có người giúp |
| **Thiên Đồng + Thiên Lương** chiếu Phu Thê | Tình già, bền lâu |
| **Khôi Việt** chiếu | Gặp qua bạn bè, quý nhân mai mối |
| **Hồng Loan + Thiên Hỷ** | Tình yêu đẹp, cưới hỏi vui |

### 2. Hợp tác làm ăn

| Cặp | Kết quả |
|-----|---------|
| **Mệnh tam hợp** (Dần-Ngọ-Tuất, v.v.) | Hợp, bền lâu |
| **Mệnh lục hại** (Tý-Mùi, Sửu-Ngọ...) | Cãi nhau, dễ tan |
| **Tài một người + Quan một người** | Hợp: người làm tiền + người quản lý |
| **Cùng Hóa Lộc ở Tài** | Cả hai cùng kiếm, nhưng tranh giành |
| **Cùng Hóa Kỵ ở Tài** | Cả hai cùng khó — dễ đổ lỗi cho nhau |

---

## 🧘 DOMAIN — PHÁT TRIỂN BẢN THÂN

### Xác định nghề nghiệp phù hợp qua sao Mệnh

| Sao Mệnh | Nghề tốt | Nghề tránh |
|---------|---------|-----------|
| Tử Vi | Lãnh đạo, quản lý, chính phủ | Làm thuê cả đời |
| Thiên Cơ | Chiến lược, tư vấn, AI/tech | Công việc chân tay |
| Thái Dương | Giáo dục, truyền thông, chính trị | Ẩn dật |
| Vũ Khúc | Tài chính, kế toán, phân tích | Sáng tạo tự do |
| Tham Lang | Sales, marketing, nghệ thuật | Khuất mày khuất mặt |
| Liêm Trinh | Luật, quân sự, tư pháp | Kinh doanh thiếu chuẩn mực |
| Thất Sát | Khởi nghiệp, thể thao, quân sự | Ổn định |
| Phá Quân | Đổi mới, startup, phá vỡ | Công sở |

---

## 📦 ĐÓNG GÓI SẢN PHẨM & ĐỊNH GIÁ

### 🎯 CÁCH DIỄN GIẢI CHO TỪNG GÓI

| Gói | Nội dung | Độ dài | Cách nói |
|-----|---------|--------|---------|
| **Cơ bản** | Lớp 1 (Tử Vi nền) + Lớp 5 (Hành động cơ bản) | 10-15 trang | Nói như đang tâm sự với bạn: "Mày có cái này, cái kia. Làm thế này, thế kia." |
| **Tiêu chuẩn** | Full 5 lớp, mỗi lớp 2-3 điểm chính | 30-40 trang | Phân tích sâu hơn, nhưng vẫn dùng ví dụ đời thường. Có disclaimer rõ ràng. |
| **Cao cấp** | 5 lớp chi tiết + phân tích từng cung + chiến lược cá nhân hóa | 60-80 trang | Phân tích chuyên sâu, nhưng mỗi phần đều có bản "dịch ra tiếng người". Giọng văn gai góc, không nể nang. |
| **Gia tộc** | Nhiều lá số + tương tác + chiến lược tổng thể | 100+ trang | Kể chuyện gia tộc. "Nhà mày có cái nghiệp này. Nhưng có thể chuyển hóa bằng cách kia." |

### 💰 BẢNG GIÁ THAM KHẢO

| Gói | Giá (VNĐ) | Giá trị cốt lõi |
|-----|-----------|----------------|
| 🥉 Cơ bản — "Lộ Trình Khai Mở" | 199.000 - 399.000 | Bước đầu thấu hiểu bản thân |
| 🥈 Tiêu chuẩn — "Bản Lĩnh Người Cầm Lái" | 999.000 - 1.999.000 | Chiến lược cá nhân để làm chủ cuộc đời |
| 🥇 Cao cấp — "Kiến Tạo Đế Vương" | 3.999.000 - 6.999.000 | Bản đồ chi tiết, chiến lược độc quyền |
| 👑 Đặc biệt — "Truyền Thừa Gia Tộc" | Từ 10.000.000 | Kiến tạo nền tảng cho cả tập thể |

### 📜 TUYÊN BỐ MIỄN TRỪ — PHẢI CÓ TRONG MỌI SẢN PHẨM

```
⚠️ TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM

Sản phẩm này được thiết kế để cung cấp góc nhìn đa chiều, phân tích tiềm năng, thách thức và các chiến lược hành động có tính tham khảo. Nội dung luận giải mang tính gợi mở, không phải là lời tiên tri hay sự cam kết tuyệt đối về tương lai.

- Tính tham khảo: Mọi thông tin, phân tích, và lời khuyên trong bản luận giải chỉ mang tính chất tham khảo, hỗ trợ quá trình tự vấn và ra quyết định của cá nhân.
- Không phải lời khuyên chuyên nghiệp: Sản phẩm này không thay thế cho lời khuyên từ các chuyên gia trong bất kỳ lĩnh vực nào (tài chính, y tế, pháp lý, tâm lý học...).
- Trách nhiệm cá nhân: Người dùng hoàn toàn chịu trách nhiệm về các quyết định và hành động của mình.

Chúng tôi không hứa hẹn điều gì viển vông — cuộc đời là do bạn tự kiến tạo.
```

### 🪝 CHIẾN THUẬT KỂ CHUYỆN GÂY HOOK

#### 1. Cấu trúc hook cho từng gói

**Gói Cơ bản (hook ngắn, Telegram):**
```
Bạn có dám đối diện với sự thật trần trụi về vận mệnh của mình?
[1-2 câu chạm nỗi đau]
→ Nhận bản luận giải 'Giải Mã Số Phận' — 199k.
[Disclaimer: không phải tiên tri, chỉ là công cụ hỗ trợ.]
```

**Gói Tiêu chuẩn (hook dài hơn, landing page):**
```
MỞ ĐẦU: "Bạn đang mắc kẹt?"
(Chạm vào sự bất an về sự nghiệp, tài chính, tình cảm)

LẬT TẨY: "Nhiều người tìm đến tử vi để nghe lời phán ngọt.
'Giải Mã Số Phận' không làm vậy. Chúng tôi vạch trần sự thật."

HỨA HẸN: "Bạn sẽ không chỉ biết vận mình, mà còn biết cách VẬN nó."

KÊU GỢI: "Đặt bản luận giải của riêng bạn ngay hôm nay."
+ DISCLAIMER
```

**Gói Cao cấp (hook video):**
```
0:00-0:03: [Visual Dark Academia, giọng trầm] "Số phận có thực sự là định đoạt?"
0:03-0:07: "Hay nó là bản đồ chờ người bản lĩnh giải mã?"
0:07-0:15: "Tôi sẽ vạch trần bạn — không nể nang — không hoa mỹ."
0:15-0:30: [Kể 1 câu chuyện ngắn về sự chuyển hóa]
0:30-0:45: "Bản luận giải 'Kiến Tạo Đế Vương' — 60-80 trang — chiến lược cá nhân hóa."
+ DISCLAIMER cuối video
```

#### 2. 5 dạng câu chào bán (sales hooks)

| Dạng | Ví dụ |
|------|-------|
| **Gây sốc** | "Bạn có dám đối diện với sự thật về con người thật của mình?" |
| **Nghi vấn** | "Số phận có thực sự là định đoạt? Hay là bản đồ chờ người bản lĩnh giải mã?" |
| **Chạm nỗi đau** | "Nếu bạn đã chán ngán những lời nói hoa mỹ, những dự đoán chung chung..." |
| **Hứa hẹn chuyển hóa** | "Bạn sẽ không chỉ biết vận mình, mà còn biết cách VẬN nó." |
| **Thách thức** | "Đây không phải dành cho người yếu đuối. Đây dành cho người dám thay đổi." |

#### 3. Nguyên tắc viết hook (không cam kết)

- ❌ "Bạn sẽ thành công sau khi đọc bản này."
- ✅ "Bạn sẽ được trang bị những chiến lược, góc nhìn để TĂNG CƯỜNG khả năng thành công."
- ❌ "Tương lai của bạn là..."
- ✅ "Bản luận giải sẽ VẠCH TRẦN những tiềm năng và chướng ngại trên con đường của bạn."
- Luôn kết thúc bằng: "Quyết định cuối cùng luôn là của bạn."

---

## 🤖 AGENT INTEGRATION (Hermes)

### Load sequence

```python
# === 1. Load master skill ===
# skill_view("tuvi-agent")
# → đọc kiến trúc, workflow, bridge layers, domain modules, product packaging
# → biết cần dispatch subsystem nào

# === 2. Dispatch theo nhu cầu ===
# Tử Vi cơ bản → skill_view("tuvi-dau-so-expert")
# Tứ Trụ → skill_view("tuvi-tu-tru-expert")
# Kinh Dịch → skill_view("tuvi-kinh-dich-expert")
# Lưu Nguyệt/Nhật chi tiết → tuvi-luu-nguyet-nhat engine
# Vẽ lá số HTML → tuvi-chart-renderer (scripts/render_chart.py)

# === 3. Áp dụng bridge layer ===
# Nội dung bridges + domains đã có sẵn trong skill này
```

### Khi nào dùng bridge nào

| Yêu cầu user | Bridge layer |
|-------------|-------------|
| "Tôi nên đầu tư không?" | Psychology (overconfidence) + Laws (Murphy) + Domain (investment) |
| "Bị sếp chèn ép" | Ancient (Quỷ Cốc Tử) + Domain (workplace) |
| "Tình cảm trục trặc" | Psychology (mere-exposure) + Domain (relationships) |
| "Nên đổi việc không?" | Laws (Parkinson) + Domain (workplace) + Kinh Dịch (timing) |
| "Tôi hợp làm nghề gì?" | Tử Vi nền + Domain (self-growth) |
| "Tháng này thế nào?" | Lưu Nguyệt engine + Psychology |
| "Mua bản luận giải" | Product packaging section + Disclaimer |

---

## 🎨 LANDING PAGE — "GIẢI MÃ SỐ PHẬN"

Khi xây dựng landing page bán sản phẩm Tử Vi:

| Yêu cầu | Chi tiết |
|----------|----------|
| **Theme** | Light theme — trắng #FFFFFF, xám #F8F9FA → #333, gold #D4A017 |
| **Brand** | "Giải Mã Số Phận" — **KHÔNG** dùng "Bộ Não Phán" |
| **Font** | Be Vietnam Pro (Google Fonts) |
| **Tone** | Dễ hiểu, gần gũi, không thuật ngữ chuyên ngành |
| **8 sections** | Hero → Paint Points → Form → Demo Result → Products → Testimonials → FAQ → Footer |
| **API** | POST /api/demo (port 8139) — MCP Tử Vi thật |
| **Mobile** | Mobile-first, breakpoints 480/768/1024 |
| **Icons** | Lucide CDN |

Chi tiết: `references/landing-page-design.md` — theme tokens, API spec, nội dung guidelines, media assets, brand voice, file structure (updated Phase 2, 20/07/2026).

## 🔗 HỆ THỐNG SKILL

### Subsystems (tải theo nhu cầu)
- `tuvi-dau-so-expert` — Tử Vi Đẩu Số (an sao, 12 cung, cách cục)
- `tuvi-tu-tru-expert` — Tử Bình Lạc Việt / Bát Tự
- `tuvi-kinh-dich-expert` — Kinh Dịch
- `tuvi-phong-thuy-expert` — Phong Thủy

### Engine (tính toán tự động)
- `tuvi-mcp-server` — MCP iztro (tính lá số, đại hạn, lưu niên)
- `tuvi-luu-nguyet-nhat` — Python engine Lưu Nguyệt/Nhật (chạy local)

### Chart (trực quan hóa)
- `tuvi-chart-renderer` — Render lá số ra HTML layout lục hợp 12 cung (Dark academia)

### Master
- **tuvi-agent** ← skill này. Entry point duy nhất cho mọi yêu cầu Tử Vi.

> Khi AI Agent load skill này, tự động biết:
> 1. Workflow luận giải 6 bước
> 2. Map tới các subsystem cần thiết
> 3. Khi nào cần bridge layer nào
> 4. Cách nói dễ hiểu cho từng đối tượng
> 5. Các gói sản phẩm, định giá và disclaimer
> 6. Format output Telegram chuẩn