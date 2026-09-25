# Team Bot Workflow — Hermes + OpenClaw + Anti_bot

## Phân công vai trò

| Bot | Vai trò | Strengths |
|-----|---------|-----------|
| **Hermes** (@tan_hermes_bot) | Search flight nhanh, tra cứu, test | Gọi `abtrip_browser.py` native Python — nhanh nhất vì không qua MCP/gateway |
| **OpenClaw** (@openclaw_tano_bot) | Booking thật, xuất vé, backend | Có MCP `abtrip-flight` server, xử lý form booking |
| **Anti_bot** (@Tan_ti_bot) | Wake-up call, Antigravity AI phân tích | Cầu nối sang Google DeepMind / Gemini, phân tích số mệnh KH |

## Flow làm việc chuẩn

1. **Search** → **Hermes** (nhanh nhất)
   - `import abtrip_browser; asyncio.run(abtrip_browser.search_flights(origin, dest, date))`
   - Trả về dict: `{success, flights_found, options}` — mỗi option có `airline, flight_number, dep_time, arr_time, duration, total_price`
   - Kết quả format Telegram-style (bullet list theo hãng, ko table)

2. **Chốt vé** → **OpenClaw** (qua MCP)
   - MCP server: `D:\AI Store\Hermes Agent\mcp-abtrip-server.py`
   - Gọi từ OpenClaw dashboard hoặc MCP tool `search_flights` / `book_flight`
   - Chậm hơn Hermes vì qua HTTP + Gateway layers

3. **Phân tích KH** → **Anti_bot** → Antigravity AI
   - /project chọn context
   - Phân tích Tử Vi, tâm lý KH

## Tại sao Hermes search nhanh hơn OpenClaw?

- **Hermes**: gọi `abtrip_browser.py` bằng `python -c "import abtrip_browser..."` — chạy Playwright native (Python process trực tiếp)
- **OpenClaw**: gọi qua MCP stdio transport → gateway → xử lý event → response — 3 layers overhead
- **Benchmark thực tế** (HAN→UIH, June 2026):
  - Hermes: ~3-5 giây (1 Python process)
  - OpenClaw MCP: ~15-30 giây (stdin/stdout + HTTP gateway)

## Cấu trúc response `abtrip_browser.search_flights()`

```python
{
    "success": True,
    "flights_found": 10,
    "options": [
        {
            "airline": "Bamboo Airways",
            "flight_number": "QH1215",
            "dep_time": "16:20",
            "arr_time": "18:00",
            "duration": "1 giờ 40p",
            "total_price": "1,732,000 VND"
        },
        ...
    ]
}
```

Không phải list của flight — mà là dict với `options` là list.

## Telegram format cho kết quả search

Dùng bullet format, chia theo hãng, **KHÔNG dùng table**:

```
| | Hãng | Chuyến | Giờ | Giá |
|:--:|:--|:--:|:--:|:--:|
| 1 | 🟢 Bamboo | QH1215 | 16:20→18:00 | 1.732.000 🏆 |
```

Hàng đầu có `| | Hãng | Chuyến | Giờ | Giá |` như header. Mỗi chuyến một dòng với số thứ tự. Rẻ nhất đánh dấu 🏆.
