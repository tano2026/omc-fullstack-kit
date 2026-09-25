# AGT API Spec — Key Excerpts

Source: `D:\Downloads\Bo_Tai_Lieu_Dac_Ta_API_ABTRIP_v1.1\abtrip_api_spec.md`
Developed by Viettel Group for ABTrip, version 1.1, dated 28/05/2026.

## Sandbox Environment

```
Base URL: https://api-abtrip.timtrungtam.com/v1
ApiAccount: ABTRIP
ApiPassword: CtTXgjVX8AQ1
PrivateKey: a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32
```

## Authentication

All requests via HTTPS POST. Every body must include `RequestInfo` at top level:
```json
{
    "RequestInfo": {
        "PrivateKey": "...",
        "ApiAccount": "...",
        "ApiPassword": "..."
    }
}
```

## Booking Workflow
1. SearchFlight → get flights + Session token
2. GetAncillary (optional) → baggage options
3. GetSeatMap (optional) → seat availability
4. BookFlight → uses Session + AirlineOptionId + FareOptionId → BookingCode
5. RetrieveBooking → verify booking
6. IssueTicket → after payment confirmed

## GetAncillary — Request Format

```json
{
    "RequestInfo": { ... },
    "System": "VN",
    "SessionInfo": {
        "Session": "{{ABTSession}}",
        "AirlineOptionId": 0,
        "FareOptionId": 0,
        "FlightOptionId": 0
    }
}
```

Response includes `ListBaggage` (e.g., 432,000₫ prepaid bag) and `ListService` (e.g., lounge 344,000₫).

## BookFlight — Request Format (simplified)

```json
{
    "RequestInfo": { ... },
    "Forced": false,
    "System": "VN",
    "GuestContact": { "Name": "...", "Phone": "...", "Email": "..." },
    "AgentContact": { "Name": "...", "Phone": "...", "Email": "..." },
    "ListPassenger": [{ "FirstName": "...", "LastName": "...", "Type": "ADT", "Gender": true }],
    "ListAirOption": [{
        "AirOptionId": 0,
        "System": "VN",
        "FlightOptionId": 0,
        "FareOptionId": 0,
        "Session": "{{ABTSession}}"
    }],
    "Option": "",
    "Payment": { "PaymentType": "CASH", "Amount": 1843181 }
}
```

Response includes `BookingCode` on success.

## SearchFlight — Response Structure

```json
{
    "Success": true,
    "Message": "Thành công",
    "ListGroup": [{
        "GroupId": null,
        "System": "VN",
        "ListAirOption": [{
            "OptionId": 0,
            "Airline": "VN",
            "ListFareOption": [{
                "OptionId": 0,
                "PriceAdt": 1843181,
                "PriceChd": 0,
                "PriceInf": 0,
                "FareClass": "ECONOMY",
                "Seats": 9
            }],
            "ListFlightOption": [{
                "OptionId": 0,
                "ListFlight": [{
                    "FlightId": "1",
                    "Airline": "VN",
                    "Operator": "BL",
                    "StartPoint": "SGN",
                    "EndPoint": "HAN",
                    "StartDate": "29072026 0455",
                    "EndDate": "29072026 0705",
                    "DepartDate": "29072026 0455",
                    "ArriveDate": "29072026 0705",
                    "FlightNumber": "6002",
                    "StopNum": 0,
                    "Duration": 130
                }]
            }]
        }]
    }]
}
```

### Key field mappings (real API vs client assumptions)

| Client expected | Real API field | Level |
|----------------|---------------|-------|
| `AirOptionId` | `OptionId` | `ListAirOption[i]` |
| `AirOptionId` (for ancillary) | `OptionId` from AirOption | `SessionInfo.AirlineOptionId` |
| Price at AirOption level | Price in `ListFareOption[i].PriceAdt` | Nested 1 level deeper |
| `ListSession` param | `SessionInfo` object | GetAncillary/GetSeatMap body |
| `GroupId` (for session) | `null` in sandbox | Unused — session token elsewhere |
