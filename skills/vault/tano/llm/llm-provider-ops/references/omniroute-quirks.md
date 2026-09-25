# OmniRoute VPS — API Quirks & Workarounds

These quirks were discovered through production use (GMSP EP01-02 generation on `http://100.64.173.75:20128`).

## Streaming is default ON
- If you request without `"stream": false`, you get SSE events, not a JSON response
- Script calls using `curl` will hang / get truncated output
- **Fix**: Always add `"stream": false` to the request body

## `auto/best-reasoning` model quirks
- Routes to DeepSeek R1, aliased as `big-pickle` on this OmniRoute instance
- **max_tokens** must be ≥ 32768 for reasoning output. Setting 50-8192 → "reasoning consumed all tokens — no content output" error
- **temperature**: 0.65-0.7 works best for creative writing. 0.3-0.5 for factual tasks
- **Long outputs timeout**: 9292+ char outputs take 60-180s. Set curl timeout to 300-600s.

## VQD token error
```
ERROR: {'message': '[503]: Failed to acquire VQD token'}
```
- Transient error on OmniRoute's VQD (value-quality-detection) auth layer
- Usually resolves within 30-60s
- **Retry strategy**: wait 30s, retry up to 3 times
- If persistent, switch to `deepseek-chat` or `gemini-2.5-flash` as interim fallback

## Reasoned output + follow-up review pattern
For writing tasks like GMSP scripts:
1. **Reasoning pass** (R1 via `auto/best-reasoning`): Generate raw creative output
2. **Review pass** (cheaper model): Verify length, CTA count, encoding, language consistency
3. **Expand pass** (if output is too short): Use cheap model again, not R1

## Rate & cost observation
- R1 (auto/best-reasoning): ~$0.002-0.01/session for reasoning + completion tokens
- cheap models (deepseek-chat, gemini-2.5-flash): ~$0.0001-0.001/session
- OmniRoute's `auto/best-reasoning` is significantly cheaper than direct DeepSeek/OpenAI R1 access
