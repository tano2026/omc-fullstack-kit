#!/usr/bin/env python3
"""
abtrip.vn flight search — API B2B trực tiếp, không cần Playwright
===================================================================
Gọi API production `api-abtrip.timtrungtam.com/v1/Flight/SearchFlight`
với PrivateKey thật, parse response real-time. Không cần Playwright,
không timeout Ant Design, không phụ thuộc browser.

Chuyển đổi từ Playwright scraping → API B2B direct ngày 2026-06-11.
Lý do: API nhanh hơn (2-3s vs 30-60s), ổn định hơn, không bị Ant Design
virtualization bug, dùng chung được cho cả 3 agent Hermes/OpenClaw/Goose.

Usage:
  python scripts/abtrip_search.py --start=HAN --end=DAD --date=30/06/2026 --table
  python scripts/abtrip_search.py --start=VII --end=SGN --date=29/06/2026 --simple
  python scripts/abtrip_search.py --start=CXR --end=HAN --date=12/07/2026 --compact
  python scripts/abtrip_search.py --start=HAN --end=SGN --date=01/07/2026 --json

Output formats:
  --json     (default) Full JSON with all fields
  --table    Pretty ASCII table — good for terminal/web
  --compact  Telegram-optimized (bullet groups by airline)
  --markdown Markdown table in code block — easy to copy
  --simple   Minimal: Số hiệu + Ngày + Nơi đi-đến + Giờ
"""

import sys, json, re, urllib.request, argparse
from datetime import datetime

# ── API credentials ──────────────────────────────────────────────
PRIVATE_KEY = "a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32"
API_ACCOUNT = "ABTRIP"
API_PASSWORD = "CtTXgjVX8AQ1"
API_URL = "https://api-abtrip.timtrungtam.com/v1/Flight/SearchFlight"

# ── Airport data ─────────────────────────────────────────────────
CLOSED_AIRPORTS = {
    "DLI": {
        "msg": "⚠️  Sân bay Liên Khương (Đà Lạt) tạm đóng cửa từ 4/3/2026 → 1/9/2026 để nâng cấp đường băng (nguồn: Báo Chính phủ, VTV)",
        "alt": "bay từ sân bay gần nhất (SGN, DAD) hoặc đi xe/limousine.",
    },
}

AIRLINE_COLORS = {
    "VN": "🔵", "VJ": "🟡", "QH": "🟢",
    "BL": "🟠", "VU": "🔴", "ZV": "🔴",
}
AIRLINE_SHORT = {
    "Vietnam Airlines": "VN", "Vietjet Air": "VJ",
    "Pacific Airlines": "BL", "Bamboo Airways": "QH",
    "Vietravel Airlines": "VU", "VASCO": "ZV",
}
AIRLINE_FULL = {
    "VN": "Vietnam Airlines",
    "VJ": "Vietjet Air",
    "QH": "Bamboo Airways",
    "BL": "Pacific Airlines",
    "VU": "Vietravel Airlines",
    "ZV": "VASCO",
}

# ── API call ─────────────────────────────────────────────────────
def search_flight(start="HAN", end="SGN", date_str="30062026"):
    """Gọi API B2B, trả về list flight dicts hoặc raise Exception."""
    payload = {
        "RequestInfo": {
            "PrivateKey": PRIVATE_KEY,
            "ApiAccount": API_ACCOUNT,
            "ApiPassword": API_PASSWORD,
        },
        "System": "VN",
        "Adt": 1, "Chd": 0, "Inf": 0,
        "ListRoute": [{
            "Leg": 0,
            "StartPoint": start.upper(),
            "EndPoint": end.upper(),
            "DepartDate": date_str,
        }],
    }

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")

    result = json.loads(raw)
    if result.get("Success") is False:
        err = result.get("Message", result.get("Msg", "Unknown error"))
        raise Exception(f"API error: {err}")

    flights = parse_api_response(result, start, end, date_str)
    return flights


def parse_api_response(data, start_airport="", end_airport="", date_str=""):
    """Parse JSON response từ API B2B thành list flight dicts."""
    flights = []
    groups = data.get("ListGroup", data.get("listGroup", []))

    if not groups:
        return flights

    for group in groups:
        for air_opt in group.get("ListAirOption", group.get("listAirOption", [])):
            opt_airline = air_opt.get("Airline", "").strip().upper()
            if not opt_airline:
                continue

            # Fare options — map OptionId -> cheapest TotalFare
            fare_options = air_opt.get("ListFareOption", [])
            fare_map = {}
            for fo in fare_options:
                oid = fo.get("OptionId", 0)
                total = fo.get("TotalFare", 0) or 0
                if oid not in fare_map or total < fare_map[oid]["price"]:
                    fare_map[oid] = {"price": total, "fare_class": fo.get("FareClass", ""),
                                     "cabin": fo.get("CabinName", "")}

            flight_opts = air_opt.get("ListFlightOption", air_opt.get("listFlightOption", []))
            for fo in flight_opts:
                flist = fo.get("ListFlight", fo.get("listFlight", []))
                oid = fo.get("OptionId", 0)
                best_fare = fare_map.get(oid, fare_map.get(0, {"price": 0}))

                for f in flist:
                    fn = f.get("FlightNumber", "").strip() or f.get("FlightNo", "").strip()
                    if not fn:
                        continue

                    # Real airline: check Operator (e.g. VN operated by BL)
                    operator = f.get("Operator", "").strip().upper()
                    real_airline = operator if operator else opt_airline

                    # Times: "29062026 0935" -> "09:35"
                    dep_raw = f.get("DepartDate", f.get("StartDate", ""))
                    arr_raw = f.get("ArriveDate", f.get("EndDate", ""))
                    dep_time = _extract_hhmm(dep_raw)
                    arr_time = _extract_hhmm(arr_raw)

                    # Duration: 115 (minutes)
                    duration_min = f.get("Duration", 0)
                    if isinstance(duration_min, str):
                        duration_min = int(re.sub(r"\D", "", duration_min)) if re.search(r"\d", duration_min) else 0
                    duration = f"{duration_min // 60} giờ {duration_min % 60}p" if duration_min else ""

                    # Next day
                    next_day = ""
                    if dep_time and arr_time:
                        try:
                            dh, dm = map(int, dep_time.split(":"))
                            ah, am = map(int, arr_time.split(":"))
                            if (ah * 60 + am) < (dh * 60 + dm):
                                next_day = "+1"
                        except:
                            pass

                    # Stops
                    stop_num = f.get("StopNum", f.get("Stops", 0))
                    if isinstance(stop_num, str):
                        stop_num = 0
                    stops_str = "Bay thẳng" if stop_num == 0 else f"{stop_num} điểm dừng"

                    # Price from fare options
                    price = best_fare["price"] or 0

                    flights.append({
                        "airline": real_airline,
                        "airline_full": AIRLINE_FULL.get(real_airline, real_airline),
                        "code": fn,
                        "depart": dep_time,
                        "arrive": arr_time,
                        "duration": duration if duration else "N/A",
                        "price": price,
                        "price_raw": f"{price:,} VND" if price else "",
                        "from": start_airport.upper(),
                        "to": end_airport.upper(),
                        "next_day": next_day,
                        "stops": stops_str,
                        "date": date_str,
                    })

    return flights


def _extract_hhmm(datetime_str):
    """Trích xuất HH:MM từ string 'DDMMYYYY HHMM'."""
    if not datetime_str:
        return ""
    parts = datetime_str.strip().split()
    if len(parts) >= 2:
        time_part = parts[-1]  # "0935" or "09:35"
        time_part = time_part.replace(":", "")
        if len(time_part) >= 4 and time_part.isdigit():
            return f"{time_part[:2]}:{time_part[2:4]}"
    m = re.search(r"(\d{1,2}):(\d{2})", datetime_str)
    if m:
        return f"{int(m.group(1)):02d}:{m.group(2)}"
    return datetime_str


# ── Sắp xếp ─────────────────────────────────────────────────────
def sort_flights(flights):
    """Sort by airline code, then by departure time."""
    def sort_key(f):
        t = f.get("depart", "00:00")
        try:
            h, m = map(int, t.split(":"))
        except:
            h, m = 0, 0
        return (f.get("airline", ""), h * 60 + m)
    flights.sort(key=sort_key)
    return flights


# ── Formatters ───────────────────────────────────────────────────
def format_json(flights, start, end, date_str):
    return json.dumps({
        "flights": flights,
        "query": {"from": start, "to": end, "date": date_str},
        "count": len(flights),
        "timestamp": datetime.now().isoformat(),
    }, ensure_ascii=False, indent=2)


def format_table(flights, start, end, date_display):
    if not flights:
        return f"❌ Không tìm thấy chuyến bay {start}→{end} ngày {date_display}"
    out = []
    sep = "─" * 80
    out.append(f"\n{sep}")
    out.append(f"  {start} → {end}  |  {date_display}  |  {len(flights)} chuyến bay")
    out.append(sep)
    out.append(f"  {'Hãng':23s} {'Chuyến':8s} {'Giờ đi':10s} {'Giờ đến':10s} {'TG bay':10s} {'Giá từ':14s}")
    out.append(sep)
    flights = sort_flights(flights)
    for f in flights:
        price = f"{f['price']:,}₫" if f['price'] else ""
        ar = f["arrive"]
        if f["next_day"]:
            ar += "+1"
        nd = ""
        out.append(f"  {f['airline_full']:23s} {f['code']:8s} {f['depart']:>5s}→  {ar:>6s}    {f['duration']:10s} {price:>14s}")
    out.append(sep)
    out.append(f"  ⏱  {datetime.now().strftime('%H:%M %d/%m/%Y')}")
    return "\n".join(out)


def format_markdown(flights, start, end, date_display):
    if not flights:
        return f"❌ Không tìm thấy chuyến bay {start}→{end} ngày {date_display}"
    flights = sort_flights(flights)
    out = []
    out.append(f"📋 **{start} → {end}** | **{date_display}** | {len(flights)} chuyến\n")
    out.append("```")
    out.append("| Hãng | Chuyến | Giờ đi - Giờ đến | TG bay | Giá từ (VNĐ) |")
    out.append("| ---- | ------ | ---------------- | ------ | ------------ |")
    for f in flights:
        code_short = f["airline"]
        nd = f" {f['next_day']}" if f["next_day"] else ""
        time_range = f"{f['depart']} - {f['arrive']}{nd}"
        price = f"{f['price']:,}" if f["price"] else ""
        out.append(f"| {code_short:<4s} | {f['code']:>6s} | {time_range:>14s} | {f['duration']:>7s} | {price:>12s} |")
    out.append("```")
    out.append("")
    out.append("*Giá có thể thay đổi.*")
    out.append(f"*Tra cứu API B2B abtrip vào {datetime.now().strftime('%H:%M %d/%m/%Y')}.*")
    return "\n".join(out)


def format_compact(flights, start, end, date_display):
    if not flights:
        return f"❌ Không tìm thấy chuyến bay {start}→{end} ngày {date_display}"
    flights = sort_flights(flights)

    # Group by airline
    groups = {}
    order = []
    for f in flights:
        a = f["airline"]
        if a not in groups:
            groups[a] = []
            order.append(a)
        groups[a].append(f)

    lines = []
    for a in order:
        g = groups[a]
        full = g[0]["airline_full"]
        dur = g[0]["duration"] if g else ""
        color = AIRLINE_COLORS.get(a, "✈️")
        lines.append(f"{color} {full} ({dur})")
        for f in g:
            nd = f" +1" if f["next_day"] else ""
            price = f"{f['price']:,}₫" if f["price"] else ""
            lines.append(f"  {f['depart']}→{f['arrive']}{nd} · {price}")
        lines.append("")

    # Cheapest
    prices = [f["price"] for f in flights if f["price"]]
    if prices:
        all_min = min(prices)
        lines.append(f"→ Rẻ nhất: {all_min:,}₫")
    else:
        lines.append("→ Không có giá")

    return "\n".join(lines)


def format_simple(flights, start, end, date_display):
    """Minimal: Số hiệu + Ngày + Nơi đi-đến + Giờ (bỏ hãng, TG bay, giá)."""
    if not flights:
        return f"❌ Không tìm thấy chuyến bay {start}→{end} ngày {date_display}"
    flights = sort_flights(flights)
    lines = []
    lines.append(f"📋 **{start} → {end}** | **{date_display}** | {len(flights)} chuyến")
    lines.append("")
    for f in flights:
        nd = f" +1" if f["next_day"] else ""
        lines.append(f"• {f['code']} · {date_display} · {start}→{end} · {f['depart']}→{f['arrive']}{nd}")
    prices = [f["price"] for f in flights if f["price"]]
    if prices:
        lines.append("")
        lines.append(f"📌 {len(flights)} chuyến · {start}→{end} · {date_display}")
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="abtrip.vn flight search — API B2B")
    parser.add_argument("--start", default="HAN")
    parser.add_argument("--end", default="PQC")
    parser.add_argument("--date", default=datetime.now().strftime("%d/%m/%Y"),
                        help="DD/MM/YYYY")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--table", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--simple", action="store_true")
    parser.add_argument("--timeout", type=int, default=0,
                        help="Bỏ qua (API luôn timeout=15s)")
    args = parser.parse_args()

    # Normalize date
    raw_date = args.date.replace("-", "/")
    parts = raw_date.split("/")
    if len(parts) == 3:
        date_api = f"{parts[0].zfill(2)}{parts[1].zfill(2)}{parts[2]}"
    else:
        date_api = datetime.now().strftime("%d%m%Y")
    date_display = raw_date

    start = args.start.upper()
    end = args.end.upper()

    # Check closed airports
    for code, info in CLOSED_AIRPORTS.items():
        if code in (start, end):
            print(f"{info['msg']}")
            print(f"   Route: {start} → {end} không khả dụng.")
            print(f"   Gợi ý: {info['alt']}")
            sys.exit(1)

    try:
        flights = search_flight(start, end, date_api)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    if not flights:
        print(f"❌ Không tìm thấy chuyến bay {start}→{end} ngày {date_display}")
        sys.exit(0)

    if args.markdown:
        print(format_markdown(flights, start, end, date_display))
    elif args.simple:
        print(format_simple(flights, start, end, date_display))
    elif args.table:
        print(format_table(flights, start, end, date_display))
    elif args.compact:
        print(format_compact(flights, start, end, date_display))
    else:
        print(format_json(flights, start, end, date_display))


if __name__ == "__main__":
    main()
