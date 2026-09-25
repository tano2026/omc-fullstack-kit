---
name: ke-toan-automation
description: Ke Toan Tu Dong Hoa - Accounting automation skills for Vietnamese businesses
---

# Ke Toan Tu Dong Hoa (Accounting Automation)

**Stack:** Python + Google Workspace MCP + Google Drive/Sheets
**Cap nhat:** thang 7/2026

---

## 3 Workflows Chinh

### Workflow 1: Phan Loai Sao Ke Ngan Hang
```
CSV sao ke tho -> AI phan loai -> Bang chi phi chuan thue + ITC
```

### Workflow 2: Chuoi Tac Vu Hoa Don
```
Xuat PDF hoa don -> Upload Drive -> Sync Google Sheets
```

### Workflow 3: PDF Hoa Don -> Extract -> Excel -> Nhap Misa
```
PDF hoa don ban le -> AI doc + phan loai -> Excel -> Import Misa
```
Giai quyet: ke toan go tay du lieu tu PDF hoa don vao Misa.
Tool: `extract.py` tai `~/pdf-invoice-tool/`
Stack: PyMuPDF + DeepSeek/Gemini API + openpyxl

```bash
python ~/pdf-invoice-tool/extract.py --file "hoa-don.pdf" --output ket_qua.xlsx
python ~/pdf-invoice-tool/extract.py --dir "hoa-don-t5/" --output thang5.xlsx
python ~/pdf-invoice-tool/extract.py --file test.pdf --dry-run
```

**Pitfalls khi goi DeepSeek API qua 9Router:**
- `stream: False` bat buoc voi model `oc/` - tra SSE mac dinh
- DeepSeek reasoning model tra output o `reasoning_content`, ko phai `content` - fallback: dung ca 2
- `max_tokens` phai du lon (4096+) - reasoning ngon token truoc khi tra content
- Nhiet do thap (0.05) cho structured extraction
- Model `oc/deepseek-v4-flash-free` KHONG ho tro vision
- Strip `<think>` tags truoc khi parse JSON

---

## PROMPT 1 - Phan Loai Sao Ke Ngan Hang

Copy paste vao Claude Code khi co file CSV sao ke:

```
Toi co file sao ke ngan hang [ten file]. Hay:
1. Doc file CSV, parse cac cot: Ngay, Noi dung, So tien
2. Phan loai tung giao dich theo danh muc chi phi chuan
3. Xac dinh khau tru thue GTGT
4. Tinh ITC (Input Tax Credit)
5. Output bang ket qua: Ngay | Noi dung | Danh muc | Khau tru | Ty le | ITC
6. Tong hop cuoi: tong chi phi, tong ITC, dieu kien hoan thue
```

---

## PROMPT 2 - Hoa Don -> Drive -> Sheets

```
INPUT: Danh sach hoa don (so HD, khach hang, ngay, tong tien, thue)
BUOC 1 - Xuat PDF: reportlab/weasyprint, template logo + thong tin
BUOC 2 - Upload Google Drive: tao folder theo nam/thang, lay shareable link
BUOC 3 - Update Google Sheets: append row tracking
BUOC 4 - Gui email: PDF dinh kem + link Drive, CC ke-toan
Yeu cau: error handling, --dry-run mode, config.yaml
```

---

## PROMPT 3 - Logic Thue Tu Dong

```
Dua vao thong tin khach hang, loai dich vu, khu vuc -> xac dinh:
1. Thue suat ap dung (GTGT 10%/5%/0%, EU VAT, My Sales Tax)
2. Thong tin hoa don (MST, tien te, phuong thuc TT)
3. Yeu cau phap ly (Nghi dinh 123/2020/ND-CP, VAT ID, Sales Tax Cert)
Output: Thong tin hoa don san sang de tao PDF
```

---

## PROMPT 4 - Bao Cao Tong Hop Thue Thang

```
Tu du lieu sao ke da phan loai -> bao cao:
1. Bang chi phi theo danh muc
2. Tong ket: tong chi phi, ITC, thue dau ra/vào, phai nop/duoc hoan
3. Dieu kien hoan thue
4. Checklist cuoi thang
Luu vao Google Doc + Drive + Sheets Dashboard
```

---

## Python Script Mau

```python
# ke_toan_classifier.py
import pandas as pd, anthropic, sys, argparse

CATEGORIES = {
    "dien nuoc": {"name": "Chi phi dien nuoc", "deductible": True, "rate": 100},
    "dich vu": {"name": "Chi phi dich vu", "deductible": True, "rate": 100},
    "ngan hang": {"name": "Chi phi ngan hang", "deductible": True, "rate": 100},
    "mua hang": {"name": "Mua hang hoa", "deductible": True, "rate": 100},
    "quang cao": {"name": "Chi phi quang cao", "deductible": True, "rate": 80},
    "nhan su": {"name": "Chi phi nhan su", "deductible": False, "rate": 0},
}

def classify_transaction(client, description, amount):
    prompt = f"""Phan loai giao dich ke toan:
Noi dung: {description}
So tien: {amount:,} VND
Tra ve JSON: {{"category":"ten danh muc","deductible":true/false,"rate":0-100,"itc":so_tien,"note":"ghi chu"}}"""
    response = client.messages.create(
        model="claude-haiku-4-5", max_tokens=200,
        messages=[{"role": "user", "content": prompt}])
    import json
    return json.loads(response.content[0].text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    client = anthropic.Anthropic()
    df = pd.read_csv(args.input, encoding='utf-8-sig')
    results = []
    for _, row in df.iterrows():
        result = classify_transaction(client, row['Noi dung'], row['So tien'])
        results.append({
            'Ngay': row['Ngay'], 'Noi dung': row['Noi dung'],
            'So tien': row['So tien'], 'Danh muc': result['category'],
            'Khau tru': 'Duoc khau tru' if result['deductible'] else 'Khong khau tru',
            'Ty le': f"{result['rate']}%", 'ITC (VAT)': result['itc'],
            'Ghi chu': result.get('note', '')})
        print(f"OK {row['Noi dung'][:40]} -> {result['category']}")

    if not args.dry_run:
        pd.DataFrame(results).to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"Saved: {args.output}")

    df_result = pd.DataFrame(results)
    print(f"Tong chi phi: {df_result['So tien'].sum():,.0f} d")
    print(f"Tong ITC: {df_result['ITC (VAT)'].sum():,.0f} d")

if __name__ == "__main__":
    main()
```

---

*AI Vibe Toolkit | cap nhat thang 7/2026*
