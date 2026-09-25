# Airport aliases in smart_agent.py

Located in: `app/services/smart_agent.py` — `_AIRPORT_ALIAS` dict.

## When adding new aliases

- Add all common Vietnamese variations for a city
- Merge with existing SGN entry rather than creating duplicate
- Test with `_extract_flight_params(["bay từ <alias> đi ..."])`

## Current SGN aliases (as of 24 Jul 2026)

```python
"sg": "SGN", "sgn": "SGN", "sài gòn": "SGN", "saigon": "SGN",
"hcm": "SGN", "tp hcm": "SGN", "tphcm": "SGN",
"hồ chí minh": "SGN", "thành phố hồ chí minh": "SGN",
```

## Make sure to cover

- Abbreviated forms (sg, hcm, tp hcm)
- Full name with and without diacritics
- Common misspellings
- "thành phố" prefix variations

## Test that aliases work

```python
# In Docker:
MSYS_NO_PATHCONV=1 docker exec abtrip-abtrip-backend-1 python -c "
from app.services.smart_agent import _extract_flight_params
print(_extract_flight_params(['bay từ tp hcm ra hà nội ngày 30/9/2026']))
"
# Should show: {'from': 'SGN', 'to': 'HAN', 'date': '30092026', 'adt': 1}
```
