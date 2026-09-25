# API B2B Payload Format (bat buoc dung)

## Request payload

```json
{
  "System": "VN",
  "Adt": 1,
  "Chd": 0,
  "Inf": 0,
  "ListRoute": [{
    "Leg": 0,
    "StartPoint": "HAN",
    "EndPoint": "SGN",
    "DepartDate": "30062026"
  }],
  "RequestInfo": {
    "PrivateKey": "a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32",
    "ApiAccount": "ABTRIP",
    "ApiPassword": "CtTXgjVX8AQ1"
  }
}
```

## Headers

```
Content-Type: application/json
```

## Endpoint

```
POST https://api-abtrip.timtrungtam.com/v1/Flight/SearchFlight
```

## Response format

```json
{
  "Success": true,
  "ListGroup": [{
    "ListAirOption": [{
      "Airline": "VJ",
      "ListFareOption": [{
        "OptionId": 0,
        "TotalFare": 990000,
        "Availability": 9,
        "Unavailable": false,
        "Promotion": false,
        "FareFamily": "Eco Saver",
        "Refundable": false,
        "Exchangeable": false
      }],
      "ListFlightOption": [{
        "OptionId": 0,
        "ListFlight": [{
          "FlightNumber": "VJ123",
          "Operator": "VJ",
          "DepartDate": "30062026 0935",
          "ArriveDate": "30062026 1135",
          "Duration": 120,
          "StopNum": 0
        }]
      }]
    }]
  }]
}
```

## Common errors

| HTTP Status | Cause | Fix |
|-------------|-------|-----|
| 400 | Wrong payload format (flat dict instead of ListRoute+RequestInfo) | Dùng format đúng ở trên |
| 400 | Date format sai (e.g. "30/06/2026" instead of "30062026") | DDMMYYYY, không dấu `/` |
| 400 | Thiếu `System` field | Thêm `"System": "VN"` |
| 401/403 | Sai PrivateKey/ApiAccount/ApiPassword | Kiểm tra trong `.env` hoặc `config.py` |
| 200 with empty ListGroup | Route không tồn tại | Kiểm tra cặp sân bay có bay thẳng không |
| 200 with Unavailable=true | Hết chỗ | Cần Availability > 0 mới còn |
| 408/timeout | Server-side timeout 15s | Check lại, API tự timeout |

## Lưu ý

- Date format: **DDMMYYYY** — không slash, không dash, không space
- `DepartDate` là string, không phải number
- `ListRoute` là array, mỗi route 1 item với `Leg` bắt đầu từ 0
- `RequestInfo` credentials — lấy từ `D:\AI Store\Hermes Agent\ticketing-agent\backend\config.py` hoặc `.env`
