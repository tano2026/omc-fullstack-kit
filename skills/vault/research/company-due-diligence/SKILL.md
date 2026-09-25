---
name: company-due-diligence
title: Company Due Diligence — Tra Cứu Doanh Nghiệp Việt Nam
description: Systematic multi-source investigation of Vietnamese companies. Cross-reference business registry, website, Facebook, director info, and red-flag detection. For partnership evaluation, competitor analysis, or supplier verification.
triggers:
  - "tra cứu công ty"
  - "tìm hiểu doanh nghiệp"
  - "kiểm tra đối tác"
  - "công ty này thế nào"
  - "verify company"
  - "due diligence"
  - "tìm công ty"
  - "xem công ty X có uy tín không"
---

# Company Due Diligence (Tra Cứu Doanh Nghiệp Việt Nam)

## Trigger
User provides company name, MST (mã số thuế), phone number, business card image, or website of a Vietnamese company they want vetted.

## Methodology (6-Step Cross-Reference)

### Step 1: Business Registry Lookup
- Search by MST (mã số thuế) on **masothue.com** or **thuvienphapluat.vn**
- Extract: tên chính xác, MST, người đại diện PL, ngày thành lập, trạng thái, địa chỉ trụ sở, số lao động, ngành nghề
- **Key check**: tên công ty trên danh thiếp/website có khớp với đăng ký thuế không?
  - "TNHH" vs "CP" (cổ phần) là khác nhau về mặt pháp lý — nếu website tự ghi "CP" mà đăng ký là "TNHH" là bất thường

### Step 2: VPĐD / Chi Nhánh Verification
- Search MST kèm "-001", "-002" etc. để tìm văn phòng đại diện / chi nhánh đã đăng ký
- **Cross-check**: địa chỉ trên danh thiếp có khớp với VPĐD đã đăng ký không?
- Cảnh báo nếu có văn phòng ghi trên danh thiếp mà không có đăng ký pháp nhân tương ứng

### Step 3: Website Analysis
- Tìm website (search tên công ty + MST)
- Check: SSL, WordPress/tech stack, độ chuyên nghiệp, dịch vụ listing
- **Cross-check**: tên công ty trên website footer/about có khớp với ĐKKD không?
- Check: chính sách, điều khoản, thông tin liên hệ

### Step 4: Social Presence (Facebook)
- Search fanpage theo tên công ty: `site:facebook.com "Tên Công Ty"`
- Search personal Facebook của giám đốc: `site:facebook.com "Họ Tên Giám Đốc"`
- Check: nội dung bài viết, hoạt động gần đây, tương tác
- **Cross-check**: địa chỉ trên fanpage có khớp với đăng ký không?

### Step 5: Director / Representative Info
- Từ MST → tên người đại diện pháp luật
- Search personal info: Facebook, bài báo, danh sách doanh nghiệp liên quan
- **If user asks about personal details** (gia đình, hôn nhân, etc.):
  - Search web + Facebook carefully
  - Only report publicly available information
  - Bài đăng công khai (chúc Tết, sinh nhật) có thể tiết lộ tình trạng gia đình

### Step 6: Red Flag Detection Summary
Compile checklist:
- [ ] Tên công ty trên website ≠ ĐKKD? (TNHH vs CP warning)
- [ ] Địa chỉ VP không khớp VPĐD đã đăng ký?
- [ ] MST không tìm thấy / không hoạt động?
- [ ] Website không SSL / sơ sài?
- [ ] Fanpage ít tương tác / nội dung spam?
- [ ] Giám đốc là đại diện nhiều công ty khác ngành?
- [ ] Thành lập gần đây (<6 tháng) mà quảng cáo "uy tín lâu năm"?
- [ ] Số lao động khai báo rất ít (<3) với dịch vụ phức tạp?

## Pitfalls
- **VPĐD mới thành lập**: Nếu VPĐD chỉ mới đăng ký (ví dụ 2 tháng trước), địa chỉ đó có thể là địa chỉ "thuê dịch vụ" chứ không phải trụ sở thật
- **Website tự ý đổi tên**: Một số website tự ý sửa tên công ty trên footer mà không cập nhật ĐKKD — đây là hành vi sai pháp luật (hành chính)
- **Multiple MST search**: Khi search giám đốc, kiểm tra cả masothue.com và các site tổng hợp để xem người đó đại diện bao nhiêu doanh nghiệp
- **Facebook privacy**: Personal profiles may be private — respect privacy, only report what's publicly visible
- **Thông tin đối chiếu**: Luôn ưu tiên dữ liệu từ masothue.com/ĐKKD hơn website hoặc danh thiếp

## Reference Sources
- masothue.com — MST lookup (most reliable)
- thuvienphapluat.vn — legal document lookup
- Facebook graph search — `site:facebook.com "company name"`
- Google search with dork: `"MST" "tên công ty"`

## Memory Saving (after investigation)
Save to memory under relevant project: key findings — verified/not verified, red flags, director name. Do NOT save full investigation logs.