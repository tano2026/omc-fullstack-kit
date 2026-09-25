# ABTrip RAG Implementation Reference

Concrete example of integrating RAG into a FastAPI + DeepSeek chatbot.

## File Structure

```
backend/
├── app/
│   ├── services/
│   │   ├── rag_service.py      # ChromaDB wrapper + seed + query
│   │   ├── llm_gateway.py      # Modified: auto-RAG in chat()
│   │   └── aviation_db.py      # Source data (airports + airlines + policies)
│   ├── api/
│   │   └── chat.py             # SSE endpoint — unchanged (benefits automatically)
│   └── main.py                 # Lifespan: init_rag/close_rag
└── .chroma/                    # Persistent vector DB (gitignored)
```

## Key Integration Points

### 1. main.py — Lifespan hooks
```python
from app.services.rag_service import init_rag, close_rag

@asynccontextmanager
async def lifespan(app):
    await init_rag()
    yield
    await close_rag()
```

### 2. llm_gateway.py — Auto-RAG in chat()
```python
async def chat(self, message, history=None, system_override=None):
    # RAG enrichment (unless explicit override)
    if system_override is None:
        rag_context = self._query_rag(message)
        if rag_context:
            base_prompt = self._build_system_prompt()
            system_override = f"{base_prompt}\n\n---\n{rag_context}"
    # ... rest of chat logic
```

### 3. rag_service.py — Query facade
```python
def format_context(self, query_text: str, top_k: int = 5) -> str:
    """Query + format as injectable markdown context."""
    docs = self.query(query_text, top_k=top_k)
    if not docs:
        return ""
    lines = ["Dưới đây là thông tin tra cứu được — hãy dùng để trả lời chính xác:\n"]
    for doc in docs:
        meta = doc.get("metadata", {})
        prefix = {"airport": "📍", "airline": "✈️", "policy": "📋"}.get(meta.get("type"), "")
        lines.append(f"- {prefix} {doc['text']}")
    return "\n".join(lines)
```

## Seed Data Design

Aviation data was seeded as 65 documents across 3 types:

| Type | Count | Example query match |
|------|-------|--------------------|
| Airport | ~20 | "sân bay nào ở Đà Lạt?" → Liên Khương (DLI) |
| Airline | ~8 | "VietJet" → airline + full info |
| Policy | ~37 | "hành lý VietJet bao nhiêu kg?" → xách tay 7kg, ký gửi 20-50kg |

Each document is a self-contained Vietnamese sentence so the LLM can consume it directly.

## Query Test Results

```
Query: "hành lý VietJet bao nhiêu kg"
Match 1: [policy] Hãng VietJet Air (VJ): Hành lý - Xách tay: 1 kiện 7kg.
Match 2: [airline] Hãng bay VietJet Air (mã IATA: VJ)... Chính sách hành lý: Ký gửi: Mua thêm...
Match 3: [policy] Hãng VietJet Air (VJ): Phí đổi vé: 150.000-300.000đ + chênh lệch...

→ DeepSeek returned detailed Vietnamese answer with baggage table
```

## Dependencies

- `chromadb >= 1.5.0` (bundles ONNX runtime, no separate ONNX install needed)
- No GPU required — runs on CPU with ONNX

## Debugging Patterns

### Empty LLM response via endpoint (but direct LLM works)

```
Symptom: direct `llm.chat("xin chào")` returns 200+ chars
         endpoint POST /api/chat returns content="" (empty string)

Root cause: endpoint passes `system_override` which bypasses auto-RAG.
            In llm_gateway.chat(), the condition `if system_override is None:`
            skips RAG enrichment when called from the endpoint.

Fix: remove `system_override` from the endpoint's llm.chat() call.
```

### SSE done-event content empty

```
Symptom: SSE endpoint returns {"type":"done","content":"..."} with full text,
         but frontend shows empty message bubble.

Root cause: SSE endpoint emits only `done` event (no intermediate `text` events).
            Frontend's done handler uses `accumulatedContent` which is still ""
            because no `text` events arrived to populate it.

Fix: frontend done handler: const finalContent = accumulatedContent || event.content || '';
```

### curl returns body parsing error on Windows git-bash

```
Symptom: curl -X POST ... -d '{"message":"hi"}' returns
         {"detail":"There was an error parsing the body"}
         Same payload via httpx or FastAPI TestClient works fine.

Root cause: MSYS/git-bash quoting issue -- not a real API bug.

Fix: test with Python httpx instead:
  python -c "import httpx,asyncio; asyncio.run(test())"
  where test() sends the request via httpx.AsyncClient.
```

### Uvicorn starts but responds incorrectly

```
Symptom: health endpoint works (200), chat endpoint fails with parse errors
         which python reveals /d/.../SomeOtherVenv/Scripts/python

Root cause: shell is using a different venv's Python that doesn't
            have chromadb/fastapi installed. Uvicorn starts but app
            modules silently fail to load.

Fix: use explicit Python path:
  /c/Python314/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8767
```

## Known Issues

1. **ONNX model download**: 79MB on first launch. Can take 2+ minutes. Use background process or lazy init.
2. **Windows path space**: `.chroma/` path resolves fine; issue is only with curl/bash tooling.
3. **English-optimized embedding**: all-MiniLM-L6-v2 handles Vietnamese domain terms well enough. For production Vietnamese, consider Cohere multilingual or a Vietnamese embedding model.
4. **Latency**: RAG + DeepSeek takes 4-10s per query. The bottleneck is the DeepSeek free tier via OmniRoute VPS, not the vector search.
