# LLM Function Calling — ABTrip SmartAgent

Added: 22 Jul 2026. Replaces brittle JSON-format prompting with OpenAI-compatible
function calling (tool use). LLM now calls named functions instead of returning
hand-crafted JSON strings.

## Architecture

```
LLM Gateway                           API Response
───────────                           ────────────
_TOOLS (3 tools)                      tool_calls[]
    │                                       │
    ▼                                       ▼
POST /chat/completions              _parse_response_message()
{"tools": _TOOLS,                         │
 "tool_choice": "auto"}          ┌────────┴────────┐
                                │                  │
                          tool_calls path     JSON fallback
                                │                  │
                    search_flight()            _parse_json()
                    answer_question()          (backward compat)
                    ask_clarification()
```

## Tools Defined

```python
_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_flight",
            "description": "Tìm chuyến bay nội địa Việt Nam...",
            "parameters": {
                "properties": {
                    "origin": ..., "destination": ..., "date": ...,
                    "adults": ..., "children": ..., "infants": ...,
                },
                "required": ["origin", "destination", "date"],
            },
        },
    },
    # + answer_question, ask_clarification
]
```

## API Request (example)

```json
POST /chat/completions
{
    "model": "claude-sonnet-4",
    "messages": [...],
    "tools": [...],
    "tool_choice": "auto"
}
```

## API Response — Tool Call (primary path)

```json
{
    "choices": [{
        "message": {
            "tool_calls": [{
                "id": "call_abc123",
                "type": "function",
                "function": {
                    "name": "search_flight",
                    "arguments": "{\"origin\":\"SGN\",\"destination\":\"HAN\",\"date\":\"25072026\",\"adults\":1}"
                }
            }]
        },
        "finish_reason": "tool_calls"
    }]
}
```

Parsed by `_parse_response_message()` into internal format:
```json
{"type": "search", "params": {"origin": "SGN", "destination": "HAN", "date": "25072026", "adults": 1}}
```

## API Response — JSON Fallback (backward compat)

If the provider doesn't support tools (or tool_choice is ignored), the LLM
will return plain content. `_parse_response_message()` falls back to JSON parsing:

```json
{"type": "reply", "reply": "Chào bạn, tôi có thể giúp gì?"}
```

Parsed into:
```json
{"type": "reply", "content": "Chào bạn, tôi có thể giúp gì?"}
```

## Internal Format (consumed by chat.py)

| Tool Call | Internal Format |
|-----------|----------------|
| `search_flight(args)` | `{"type": "search", "params": {...}}` |
| `answer_question(reply)` | `{"type": "reply", "content": "..."}` |
| `ask_clarification(question, missing)` | `{"type": "clarify", "content": "...", "missing": [...]}` |

## System Prompt (new, shorter)

```
Bạn là trợ lý đặt vé máy bay ABTrip. Giúp khách hàng tìm vé và trả lời thông tin.

QUAN TRỌNG: Bạn có 3 CÔNG CỤ để sử dụng:
1. search_flight — khi khách muốn tìm vé máy bay
2. answer_question — khi khách hỏi thông tin chung
3. ask_clarification — khi khách muốn tìm vé nhưng thiếu thông tin.
...
LUÔN DÙNG CÔNG CỤ — không trả lời text thuần nếu có công cụ phù hợp.
```

## Provider Support

Both HHTech and OmniRoute endpoints accept `tools` + `tool_choice: "auto"`.
Providers that don't support function calling will ignore these parameters
and return regular content — the JSON fallback path handles this gracefully.

Gemini fallback does NOT support function calling — it will always use
the JSON fallback path via `_call_gemini()`.

## Pitfalls

1. **Tool arguments must be valid JSON**: If the LLM generates malformed JSON
   in `function.arguments`, the parse will fail and the LLM response is discarded.
   The provider chain continues to the next fallback.
2. **Date format**: The tool expects `DDMMYYYY` format (e.g., `25072026`), not ISO.
   This is documented in the tool parameter description.
3. **Only first tool_call is used**: If the LLM returns multiple tool_calls,
   only the first one is processed. This matches the single-intent-per-turn
   design of the chat flow.
