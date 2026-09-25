# SIM/eSIM Supplier: IST1 API Reference

**Found at:** `D:\MMO Du an\AI Agent Future\SIM API_IST1_2026.docx`
**Source:** Tài liệu IST1 — Integration Protocol Standards (517 paragraphs, DOCX)

## Overview

eSIM wholesale supplier với RESTful API, auth bằng MD5 signing.
Dùng cho SIM du lịch agent trong ABTrip AI Platform (thay thế Tour agent).

## Authentication

- Method: MD5 signing
- Mỗi request kèm chữ ký MD5 của params + secret key
- Format: JSON request body

## API Endpoints

| Mã | Endpoint | Mô tả |
|----|----------|-------|
| F100 | Get Location | Danh sách quốc gia có eSIM |
| F200 | Obtain Commodities | Danh sách gói eSIM theo quốc gia |
| — | Get commodity price | Giá gói eSIM |
| — | Query Order Information | Tra cứu đơn hàng |
| — | Create ESIM order | Tạo đơn mua eSIM |
| — | Query Validity of Card | Kiểm tra hạn thẻ |
| — | Daily Flow Query | Lưu lượng data hàng ngày |

## Key Parameters

- MD5 sign — chữ ký xác thực
- Commodity ID — mã gói eSIM
- Country code — mã quốc gia
- Order ID — mã đơn hàng
- IC CID — mã thẻ eSIM (ICCID)

## Integration Status

| Khoản | Trạng thái |
|-------|-----------|
| Tài liệu | ✅ Đã tìm thấy tại `D:\MMO Du an\AI Agent Future\SIM API_IST1_2026.docx` |
| Parser | ⏳ Chưa parse ra structured data |
| Backend | ⏳ Chưa tích hợp chat API |
| Frontend | ✅ ChatPanel + Tab đã có placeholder |
| Postman | ✅ `ABTrip V1.1.postman_collection.json` cùng folder |

## File Paths

```
D:\MMO Du an\AI Agent Future\
├── SIM API_IST1_2026.docx         ← 517 paragraphs, 7 endpoints
├── ABTrip V1.1.postman_collection.json
├── ABTrip V1.1.postman_collection.zip
└── agent.tkt/                    ← project code
```

## Next Steps

1. Parse DOCX → structured JSON (packages, countries, pricing)
2. Build `services/sim_client.py` — wrapped HTTP client với MD5 signing
3. Add `api/chat.py` SIM handler → gọi SIM API khi user hỏi
4. Wire into frontend ChatPanel (đã có tab + placeholder)
