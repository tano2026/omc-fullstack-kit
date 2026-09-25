# ABTrip API V1.1 — AGT cấp 1 Postman Analysis

> **Source:** `ABTrip_V1.1.postman_collection.json` (11.3MB, 10 endpoints)
> **Base URL:** `{{host}}` = `https://api.abtrip.vn`

## Authentication

Sent in **body of every request** — NOT HTTP headers:

```json
{
  "RequestInfo": {
    "PrivateKey": "{{PrivateKey}}",
    "ApiAccount": "{{ApiAccount}}",
    "ApiPassword": "{{ApiPassword}}"
  }
}
```

All 3 fields are Postman variables (set per-environment).

## Endpoints (10)

### 1. SearchFlight
- **Method:** POST
- **Path:** `/Flight/SearchFlight`

**Request:**
```json
{
  "RequestInfo": {...},
  "System": "",
  "Adt": 1,
  "Chd": 1,
  "Inf": 0,
  "ListRoute": [
    {"Leg": 0, "StartPoint": "HAN", "EndPoint": "SGN", "DepartDate": "28032026"},
    {"Leg": 1, "StartPoint": "SGN", "EndPoint": "HAN", "DepartDate": "30032026"}
  ]
}
```

### 2. BookFlight
- **Method:** POST
- **Path:** `/Flight/BookFlight`

**Request:** GuestContact, AgentContact, ListPassenger[], ListAirOption[], Option, Payment, ServiceFee, Invoice

### 3. IssueTicket
- **Method:** POST
- **Path:** `/Flight/IssueTicket`
- **Request:** RequestInfo + BookingCode

### 4. RetrieveBooking
- **Method:** POST
- **Path:** `/Flight/RetrieveBooking`
- **Request:** RequestInfo + BookingCode

### 5. GetAncillary
- **Method:** POST
- **Path:** `/Flight/GetAncillary`

**Request:** RequestInfo + SessionInfo{Session, AirlineOptionId, FareOptionId, FlightOptionId}

### 6. GetSeatMap
- **Method:** POST
- **Path:** `/Flight/GetSeatMap`
- **Request:** Same SessionInfo-based as GetAncillary

### 7. GetFareRule
- **Method:** POST
- **Path:** `/Flight/GetFareRule`
- **Request:** Same SessionInfo-based

### 8. GetAirports
- **Method:** POST
- **Path:** `/Flight/GetAirports`
- **Request:** RequestInfo only

### 9. GetAirlines
- **Method:** POST
- **Path:** `/Flight/GetAirlines`
- **Request:** RequestInfo only

### 10. GetAircrafts
- **Method:** POST
- **Path:** `/Flight/GetAircrafts`
- **Request:** RequestInfo only

## Booking Flow

```
1. SearchFlight → Select flight → Get SessionInfo
2. GetFareRule (optional) → Check fare conditions
3. GetSeatMap (optional) → Select seats
4. GetAncillary (optional) → Add baggage/meals
5. BookFlight → Create booking → Get BookingCode
6. IssueTicket → Issue ticket
```

## Response Format

```json
{"StatusCode": "000", "Success": true, "Message": "Thành công", ...}
```

| Code | Meaning |
|------|---------|
| 000 | Success |
| Other | Error (check Message) |

## Key Differences from Old API

| Aspect | Old API | New V1.1 |
|--------|---------|----------|
| Auth method | Header-based | Body-based (RequestInfo) |
| Search format | Flat `{StartPoint, EndPoint}` | Array `ListRoute[{Leg, StartPoint, EndPoint, DepartDate}]` |
| Endpoints | Fewer | 10 endpoints |
| Session management | Separate auth call | Session strings in SearchFlight response |
