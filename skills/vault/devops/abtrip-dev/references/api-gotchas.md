# AGT API Response Structure Gotchas

## `SearchFlight` response structure (truth from 24 Jul 2026 debug)

```
Response
├── StatusCode, Success, Message
├── Session (string)
├── ListGroup[]
│   └── Group
│       ├── TripType, Journey, StartPoint, EndPoint, DepartDate
│       └── ListAirOption[]
│           └── AirOption
│               ├── Airline            ← NOT AirlineName!
│               ├── OptionId, Leg, Itinerary, FlightType
│               ├── ListFlightOption[]
│               │   └── ListFlight[]
│               │       └── Flight
│               │           ├── FlightNumber, StartDate, EndDate
│               │           ├── StartPoint, EndPoint
│               │           ├── Duration, StopNum
│               │           └── ListSegment[]
│               └── ListFareOption[]    ← nested under AirOption, NOT Group!
│                   └── FareOption
│                       ├── OptionId, FareClass, FareBasis, FareFamily
│                       ├── CabinCode, CabinName, Refundable
│                       ├── Availability, TotalFare, BaseFare, PriceAdt
│                       └── ListFarePax[]
```

## Pitfalls fixed (24 Jul 2026)

### 1. `AirlineName` does not exist
The field is `Airline` on the AirOption object. Old code `air_options[0].get("AirlineName", "?")` always returned `?`.

### 2. `ListFareOption` is nested under `ListAirOption[]`, NOT at Group level
Old code did `grp.get("ListFareOption")` which was always empty. Correct: `ao.get("ListFareOption")` where `ao` is an AirOption.

### 3. Flight details are deeply nested
Path: `AirOption → ListFlightOption[0] → ListFlight[0]` gives `FlightNumber`, `StartDate`, `EndDate`.
- `StartDate` / `EndDate` format: `"23082026 0500"` — last 4 chars are HHMM for display.

### 4. Fare display fields
Use `FareFamily` (Vietnamese: "Phổ thông tiết kiệm"), `CabinName` (Economy/Premium/Business), `Availability` (remaining seats).
`FareType` does not exist — was a guess that never matched the API.

### 5. Route keys are `StartPoint`/`EndPoint`, NOT `Origin`/`Destination`
Client sends: `{"StartPoint": "HAN", "EndPoint": "SGN", "DepartDate": "23082026"}`
Using `Origin`/`Destination` makes the API return empty routes.
