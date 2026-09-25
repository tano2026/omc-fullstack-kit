# RAG Knowledge Base — ChromaDB + ONNX

Built 22 Jul 2026. Replaces the old deprecated ChromaDB attempt with a working integrated pipeline.

## Architecture

```
user message
  → chat.py → _build_context(session, message)
      → rag_knowledge.format_context(message, n_results=2)
          → ChromaDB (ONNXMiniLM_L6_V2) → semantic search
      + session last_search context
  → llm_gateway._build_messages()
      → system: [THÔNG TIN PHIÊN LÀM VIỆC HIỆN TẠI] + RAG context
      → system: system prompt (instructed to use [THÔNG TIN TRA CỨU])
      → user: current message
```

## Files

| File | Purpose |
|------|---------|
| `backend/app/services/rag_knowledge.py` | RAG service — init, query, format_context |
| `backend/data/chroma/` | ChromaDB persistence dir (gitignored, ~2MB) |

## How it works

1. `RAGKnowledge` class wraps a ChromaDB collection with ONNXMiniLM_L6_V2 embedding
2. `seed_knowledge()` populates from aviation_db.py POLICIES dict + hardcoded FAQ documents
3. `format_context(query)` returns a `[THÔNG TIN TRA CỨU]` block with top-N matches
4. `chat.py` calls `format_context()` in `_build_context()` before each LLM call
5. System prompt tells LLM to prefer [THÔNG TIN TRA CỨU] for policy questions

## Key API

```python
from app.services.rag_knowledge import get_rag

rag = get_rag()
rag.count  # total documents indexed

# Get context for LLM injection
ctx = rag.format_context("hành lý Vietjet bao nhiêu kg", n_results=2)
# Returns:
# [THÔNG TIN TRA CỨU]:
# [1] 🧳 Hành lý
# CHÍNH SÁCH HÀNH LÝ:
# - VJ: Hành lý xách tay 1 kiện 7kg...
# ---
# [2] 🎒 Mẹo hành lý
# ...

# Raw query (returns list of (text, score, metadata))
results = rag.query("hủy vé VNA có mất phí không", n_results=3)
```

## Seed documents (11 documents)

| ID | Title | Source |
|----|-------|--------|
| policy_baggage | 🧳 Hành lý | aviation_db POLICIES |
| policy_change | 🔄 Đổi vé | aviation_db POLICIES |
| policy_cancel | ❌ Hủy vé | aviation_db POLICIES |
| policy_documents | 📋 Giấy tờ | aviation_db POLICIES |
| tip_luggage | 🎒 Mẹo hành lý | Hardcoded FAQ |
| tip_checkin | ⏰ Check-in | Hardcoded FAQ |
| tip_booking | 💡 Mẹo đặt vé | Hardcoded FAQ |
| tip_airport | 🛫 Sân bay | Hardcoded FAQ |
| service_fasttrack | ⭐ Fast Track | Smart service FAQ |
| service_esim | 📱 eSIM | Smart service FAQ |
| service_visa | 🛂 Visa | Smart service FAQ |

## Pitfalls

1. **No sentence-transformers needed** — ChromaDB's built-in ONNXMiniLM_L6_V2 embedding function works standalone. Installing the full `sentence-transformers` package takes 2-3 minutes and requires PyTorch (500MB+). Use the ONNX variant instead.
2. **Collection init** — `get_collection()` raises `chromadb.errors.NotFoundError` if collection doesn't exist. Always use `try/except` to fallback to `create_collection()`.
3. **Small KB is fine** — The aviation domain has ~11 core documents. RAG still adds value over keyword matching for natural language queries ("bao nhiêu kg" → hành lý).
4. **Embedding format** — ChromaDB returns distance scores. Lower = more similar. Documents are stored with `metadatas={"source": "policies"}`, unused currently but available for filtering.
5. **`format_context()` returns empty string** when no results found (not `None`). Caller checks `if rag_ctx:` before appending.
6. **ChromaDB persistence** — `chromadb.PersistentClient` writes to `data/chroma/`. This dir grows slowly with collection size. No cleanup needed for current 11 docs (~2MB).
