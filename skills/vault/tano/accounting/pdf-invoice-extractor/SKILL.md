---
name: pdf-invoice-extractor
description: Tool đọc PDF hóa đơn bán lẻ, OCR scan, extract dữ liệu, phân loại chi phí, xuất Excel format cho Misa
---

# PDF Invoice Extractor

**Vị trí:** `C:\Users\Nguyen Ngoc Tan\pdf-invoice-tool\extract.py`
**Chi phí:** $0 (Tesseract OCR local + DeepSeek Free qua 9Router)

## Cách dùng

```bash
cd /c/Users/Nguyen Ngoc Tan/pdf-invoice-tool

# 1 file
python extract.py --file "path/to/invoice.pdf"

# Cả thư mục (batch)
python extract.py --dir "path/to/folder" --output ket_qua.xlsx

# Dry run (không gọi API)
python extract.py --file test.pdf --dry-run
```

## Yêu cầu

- Python 3.11+
- PyMuPDF, httpx, openpyxl (đã cài)
- Tesseract OCR (đã cài tại `C:\Program Files\Tesseract-OCR\`)
- Tiếng Việt traineddata (đã cài tại `pdf-invoice-tool/tessdata/vie.traineddata`)
- 9Router đang chạy (localhost:20128)

## Dependencies

```bash
pip install PyMuPDF httpx openpyxl
```

## Output

Excel file với các cột: STT, File gốc, Ngày HĐ, Số HĐ, Nhà cung cấp, MST, Khách hàng, Tổng tiền, Thuế GTGT, Tổng cộng, Phân loại, Ghi chú.

Kèm tổng kết: số hóa đơn, tổng tiền, tổng VAT, phân loại theo category.

## Workflow

1. PDF → PyMuPDF đọc text
2. Nếu text <50 chars → Tesseract OCR (vie+eng)
3. Text → DeepSeek Free (9Router) → JSON có cấu trúc
4. JSON → Excel format

## Cấu hình

Sửa `config.json`:
- `api.model`: đổi model (mặc định `oc/deepseek-v4-flash-free`)
- `categories`: thêm/bớt danh mục phân loại
