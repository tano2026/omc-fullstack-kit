# LLM Bot Architecture — ABTrip Agent

Kiến trúc LLM chatbot cho ABTrip, hoàn thiện 07/2026. Gồm 3 lớp: backend API → SSE streaming → frontend React.

## Kiến trúc tổng thể

```
User UI → ChatInterface (Next.js)
              ↓ SSE (fetch ReadableStream)
         api/chat.py (FastAPI)
              ↓
         llm_gateway.py (OpenAI-compatible → DeepSeek via OmniRoute VPS)
              ↓ fallback
         Google Gemini 2.5 Flash
```

## Backend: SSE Endpoint

### File: `backend/app/api/chat.py`

**SSE endpoint** (`POST /api/chat/stream`):

```python
@router.post("/chat/stream")
async def chat_stream(request: StreamRequest):
    async def event_generator():
        try:
            # ... process ...
            if llm_response.type == "tool_call":
                yield f"data: {json.dumps({'type': 'tool_call', 'tool_name': name})}\n\n"
                # Execute tool, then:
                yield f"data: {json.dumps({'type': 'done', 'content': ..., 'data': flight_data, 'step': 'search_results'})}\n\n"
            elif llm_response.type == "text":
                yield f"data: {json.dumps({'type': 'done', 'content': content, 'step': 'idle'})}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

### SSE Event Types

| Type | Khi nào | Fields |
|------|---------|--------|
| `text` | LLM gửi từng token (chunk) | `type`, `content` |
| `tool_call` | LLM muốn gọi tool | `type`, `tool_name`, `tool_args` |
| `done` | Hoàn thành xử lý | `type`, `content`, `data`, `session_id`, `step`, `suggestions` |
| `error` | Lỗi | `type`, `content` |

### Steps (State Machine)

| Step | Ý nghĩa | Frontend render |
|------|---------|----------------|
| `idle` | Chờ user nhập | Text chat |
| `search_results` | Có kết quả tìm vé | `FlightCardChat` cards |
| `collecting_passengers` | Cần nhập thông tin khách | `PassengerForm` |
| `awaiting_confirmation` | Chờ xác nhận đặt vé | Xác nhận/Hủy buttons |
| `booking_result` | Đã đặt vé xong | Text + booking code |

### Structured Data trong SSE

Search results event cần gửi `data` field chứa parsed flights:
```python
flights_data = _parse_flights(routes[0].get("ListFlight", [])) if routes else []
yield json.dumps({
    'type': 'done', 'content': formatted, 'data': flights_data,
    'session_id': session_id, 'step': 'search_results'
})
```

Collecting passengers event cần `passenger_count`:
```python
passenger_count = tool_args.get("adt", 1) + tool_args.get("chd", 0)
yield json.dumps({
    'type': 'done', 'content': msg, 'data': {'passenger_count': passenger_count},
    'session_id': session_id, 'step': 'collecting_passengers'
})
```

### Parsing flights (backend)

Dùng `_parse_flights()` để extract structured data từ AGT API response sang frontend-compatible array:
```python
def _parse_flights(flights) -> list[dict]:
    # Returns: {airline, flight, depart, arrive, duration, price, currency, session,
    #           AirlineCode, FlightNumber, DepartTime, ArrivalTime, AdultFare, AvailableSeats}
```

## Frontend: SSE Streaming

### File: `frontend/lib/api.ts`

```typescript
export async function streamChat(
  agent: string, message: string, sessionId?: string,
  onEvent: (event: StreamEvent) => void
): Promise<void> {
  const res = await fetch(`${BACKEND_URL}/api/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ agent, message, session_id: sessionId ?? null }),
  });

  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    // Parse SSE events from buffer
    // yield each parsed event to onEvent callback
  }
}
```

### File: `frontend/components/chat/ChatInterface.tsx`

Xử lý các event types từ SSE:

1. **Event `text`**: Append chunk vào `accumulatedContent`, update message in real-time
2. **Event `tool_call`**: Show "⏳ Đang xử lý..." 
3. **Event `done`**: Set `step` + `data` cho message, render structured UI
4. **Event `error`**: Show error message

Rendering theo step:
```tsx
// step === 'search_results' → FlightCardChat cards
{msg.step === 'search_results' && getFlightsArray(msg.data).map((flight, i) => (
  <FlightCardChat key={i} flight={flight} onSelect={handleFlightSelect} />
))}

// step === 'collecting_passengers' → PassengerForm
{msg.step === 'collecting_passengers' && (
  <PassengerForm count={...} onSubmit={handlePassengerSubmit} onCancel={...} />
)}

// step === 'awaiting_confirmation' → Xác nhận / Hủy buttons
{msg.step === 'awaiting_confirmation' && (
  <button onClick={handleConfirmBooking}>✅ Xác nhận</button>
  <button onClick={handleCancelBooking}>✖ Hủy</button>
)}
```

## Các Components

### FlightCardChat (`components/FlightCardChat.tsx`)
- Props: `flight` (object), `onSelect` (callback)
- Hiển thị: airline icon, route, time, price, tags (rẻ nhất/nhanh nhất/bay đêm)
- Click → gọi `onSelect(flight)` → gửi message "chọn chuyến VN230"

### PassengerForm (`components/PassengerForm.tsx`)
- Props: `count` (số hành khách), `onSubmit`, `onCancel`
- Fields: Họ tên, Giới tính, Ngày sinh, Số hộ chiếu
- Validate: fullName + birthDate required
- Submit → `handleSend(JSON.stringify({ action: 'passenger_info', passengers }))`

## Windows-specific Pitfalls

### Port management
- Zombie uvicorn processes stuck on port: use `netstat -ano | findstr :PORT` + `taskkill //f //pid PID`
- PowerShell `Where-Object` breaks with spaces in username path → use `findstr` + `awk` instead
- Always check `netstat -ano | findstr :PORT | grep LISTENING` before starting new process

### Frontend startup
- `npx next dev` fails with space in Windows username → use `npx --no-install` or local `node_modules/.bin/next.cmd`
- Backend URL default mismatch: update `.env.local` **and** `lib/api.ts` fallback constant

### DeepSeek / OmniRoute config
- `"stream": False` is mandatory in payload — OmniRoute proxy defaults to SSE mode
- `oc/deepseek-v4-flash-free` model requires exact prefix `oc/`
- Backend `.env` OPENAI_* vars conflict with Pydantic Settings `model_config` → keep config in `config.py` defaults, avoid `.env` pollution
