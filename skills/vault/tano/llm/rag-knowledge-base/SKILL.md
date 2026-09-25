---
name: rag-knowledge-base
title: RAG Knowledge Base
description: Build and integrate a Retrieval-Augmented Generation pipeline with ChromaDB, local embeddings, and LLM gateway integration
domain: llm
---

# RAG Knowledge Base

Build a vector-search knowledge base for LLM chatbots. Covers ChromaDB setup, embedding, seeding, querying, and integration into existing chat pipelines.

## When to Use

- User asks to add "kiến thức" / "tra cứu" / "knowledge base" to a chatbot
- LLM needs to answer policy, FAQ, or domain-specific questions accurately
- System prompt is getting too large and you need dynamic context injection
- Existing static data (e.g. aviation_db.py) could be vector-indexed instead of injected raw

## Architecture

```
User query → LLM Gateway → RAG Service → ChromaDB (vector index)
                              ↓
                     Relevant docs injected into system prompt
                              ↓
                    LLM (DeepSeek/Gemini) generates response
```

## Components

### 1. Vector Store (ChromaDB)
- Persistent client (files-based, no server needed)
- In-process, pure Python, works cross-platform (Windows OK)
- Default embedding: ONNX all-MiniLM-L6-v2 (~79MB download on first use)

### 2. Embedding
- Chroma ships ONNX-based embedding, no GPU required
- `chromadb.utils.embedding_functions.ONNXMiniLM_L6_V2`
- Download cached at `~/.cache/chroma/onnx_models/` (one-time)

### 3. Service Layer
- Singleton `RagService` class with initialize/query/close lifecycle
- Collection per domain (`aviation_kb`, `visa_guide`, etc.)
- `format_context()` returns ready-to-inject markdown string

### 4. LLM Integration
- Auto-query RAG before every LLM `chat()` call
- Concatenate base system prompt + RAG context as `system_override`
- RAG failure is non-fatal — logs debug warning, continues without context

## Implementation Steps

```python
# 1. Initialize RagService
from chromadb import PersistentClient, Settings
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from app.services.rag_service import RagService, RAG_DOCS_DIR, init_rag, close_rag

# RagService is a singleton, init_rag/close_rag handle lifecycle in lifespan

# 2. Add admin router to main.py
# from app.api.admin import router as admin_router
# app.include_router(admin_router)

# 3. Create rag_documents directory: backend/rag_documents/
# This is automatically created by RagService.__init__

# 4. Upload documents via Admin Panel or place files directly in backend/rag_documents/
# Supported formats: .pdf, .md, .txt

# 5. Trigger RAG re-indexing (via Admin Panel or direct call)
# await rag_service._index_all_data(clear_existing=True)

# 6. Query
# results = rag_service.query("hành lý VietJet", n_results=3)

# 7. Format context
# context_lines = rag_service.format_context("hành lý VietJet", top_k=3)

# 8. Inject into LLM (pseudo)
# system_override = base_system_prompt + "\n---\n" + context
# llm.chat(message, system_override=system_override)
```

## Seed Data Strategy

`_index_all_data(clear_existing: bool = False)` (renamed from `_seed()`) is now responsible for indexing both initial aviation data and user-uploaded documents.

### Aviation DB Data

| Data type | Document format | Metadata fields |
|-----------|----------------|-----------------|
| Airport | `Sân bay {name} (IATA: {code}). Thành phố: {city}...` | type, code, city, vietnam, **source="aviation_db"** |
| Airline | `Hãng bay {name} (mã IATA: {code}). Chính sách: {policy}...` | type, code, name, **source="aviation_db"** |
| Policy (high-level) | `Hãng {name} ({code}): hành lý: {value}` | type, airline_code, category, subcategory, **source="aviation_db"** |
| Policy (detail) | `Hãng {name} ({code}): Hành lý - Ký gửi: 20kg` | type, airline_code, category, subcategory, **source="aviation_db"** |

### User-Uploaded Documents

-   Files placed in `backend/rag_documents/` (can be `.pdf`, `.md`, `.txt`).
-   Processed by `_process_document_file()` which chunks the content using `textwrap`.
-   Metadata includes: `type="user_doc"`, `source="<filename>"`, `chunk_id`, `file_type`.
-   Each chunk is assigned a unique `uuid` as its ID in ChromaDB.

## Pitfalls

### `system_override` bypasses auto-RAG enrichment

If your `chat()` method auto-queries RAG only when `system_override is None` (the canonical pattern to avoid redundant work), **any endpoint that passes `system_override` will silently skip RAG**. This produces empty or generic LLM responses despite RAG being fully initialized.

**Fix**: Remove `system_override` from endpoint calls and let the LLM gateway handle RAG enrichment itself:

```python
# BAD -- bypasses auto-RAG
llm_response = await llm.chat(message, history=history, system_override=custom_prompt)

# GOOD -- lets gateway auto-enrich with RAG
llm_response = await llm.chat(message, history=history)
```

If you must pass a custom system prompt, merge the RAG context into it manually on the endpoint side rather than passing `system_override` blindly.

### Empty LLM response = RAG enrichment not firing

When LLM tests pass directly but the endpoint returns `content=""`, the #1 suspect is `system_override` being passed by the endpoint. Symptom: direct `llm.chat()` returns 200+ chars, same call through the endpoint returns `""`.

### curl "body parsing error" on Windows git-bash

`curl -X POST -H "Content-Type: application/json" -d '{...}'` sometimes returns `{"detail":"There was an error parsing the body"}` even when the exact same payload succeeds via httpx or TestClient. This is a git-bash/MSYS quoting issue, not an actual API bug.

**Fix**: Test with Python httpx instead of curl on Windows:
```bash
python -c "import httpx, asyncio; print(asyncio.run(httpx.AsyncClient().post('http://...', json={'msg':'hi'}, timeout=30)).json())"
```

### Wrong Python when uvicorn restarts

On Windows with multiple Python environments, the shell's `python` may resolve to a venv that lacks required packages (e.g. MoneyPrinterTurbo venv without chromadb/fastapi). The uvicorn process starts but app modules silently fail, leaving a half-baked server that responds to health checks but fails on real endpoints.

**Fix**: Check and use explicit system Python path:
```bash
which python             # confirm this is the right one
/c/Python314/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8767
```

### First-run slow

ONNX model download (79MB) happens on first `initialize()`. Use background process + notify_on_complete.

### Port conflicts

Kill stale uvicorn processes before restarting after RAG integration. Use `taskkill //F //PID <pid>` with explicit PIDs.

### Space in username paths

MSYS/bash chokes on `C:\Users\Nguyen Ngoc Tan\`. Use `cd "..."` or background processes.

### RAG response in SSE "done" event (no token streaming)

When the LLM gateway doesn't stream tokens (e.g. `stream: False` for OmniRoute compatibility), the SSE endpoint emits a single `{"type": "done", "content": "...", ...}` event with no preceding `{"type": "text", ...}` token events. The frontend accumulates content from `text` events and only sets the message content from `accumulatedContent` in the `done` handler — so if there were no `text` events, the message appears empty.

**Fix**: In the frontend's `done` handler, fall back to `event.content` when `accumulatedContent` is empty:

```typescript
if (event.type === 'done') {
  const finalContent = accumulatedContent || event.content || '';
  // Update message with finalContent instead of accumulatedContent
}
```

**Prevent**: If you want progressive token rendering, use a streaming-compatible provider or add a chunking wrapper in the LLM gateway that yields tokens from the full response.

### RAG startup blocks lifespan

`await init_rag()` in FastAPI lifespan blocks until model download (~79MB first run) + seeding completes — can take 2+ minutes. The app responds to health checks but endpoints 503 during this window.

**Fix**: Use background task for first-load or lazy-init on first query:

```python
@asynccontextmanager
async def lifespan(app):
    asyncio.create_task(init_rag())  # non-blocking
    yield
    await close_rag()
```

### all-MiniLM-L6-v2 is English-optimized

Works decently for Vietnamese domain terms (airline codes, "hnh lý", policy words). For better Vietnamese accuracy, swap to a multilingual model or use dedicated embedding service.

## Admin Panel for RAG Management

To provide a user-friendly interface for managing RAG knowledge, an internal admin panel can be implemented:

### Endpoints (`app/api/admin.py`)

-   `GET /admin`: Serves the `admin.html` frontend.
-   `POST /admin/upload-document`: Accepts file uploads (`.pdf`, `.md`, `.txt`) and saves them to `backend/rag_documents/`.
-   `GET /admin/documents`: Lists all uploaded documents.
-   `POST /admin/reindex-rag`: Triggers a full re-indexing of the RAG database in a background task, clearing existing data and re-processing all documents (aviation_db + user uploads).

### Frontend (`app/templates/admin.html`)

A simple HTML page provides:
-   A file upload form.
-   A dynamic list of currently indexed documents.
-   A button to trigger RAG re-indexing.
-   JavaScript for asynchronous API calls and UI updates.

### RAG Service Integration (`app/services/rag_service.py`)

The `RagService` is extended to support the admin panel:
-   `get_documents_dir()`: Returns the path to the `backend/rag_documents` directory.
-   `_process_document_file(file_path: Path)`: Reads, chunks, and extracts text from `.pdf`, `.md`, `.txt` files. Uses `fitz` for PDF and `textwrap` for chunking.
-   `_index_all_data(clear_existing: bool = False)`: Renamed from `_seed()`. This now first clears the collection (if `clear_existing` is true), then indexes static `aviation_db` data, and finally scans `RAG_DOCS_DIR` to process and index all user-uploaded documents. Each user document chunk gets a `uuid` as its ID.
-   `reindex_rag_in_background(rag_service: RagService)`: An `async` function outside the class that calls `rag_service._index_all_data(clear_existing=True)` as a `BackgroundTasks` in FastAPI.

## Integration Checklist

- [ ] Install `chromadb`
- [ ] Create `services/rag_service.py` with singleton pattern
- [ ] Call `init_rag()` in app lifespan (startup) and `close_rag()` in shutdown
- [ ] Modify LLM gateway `chat()` to auto-query RAG when no `system_override`
- [ ] Verify with a policy query ("hành lý VietJet") — confirm RAG context in response
- [ ] Add `.chroma/` to `.gitignore` (regeneratable)
- [ ] Add to `requirements.txt`
