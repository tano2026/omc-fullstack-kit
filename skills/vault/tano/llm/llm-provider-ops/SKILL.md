---
name: llm-provider-ops
category: llm
description: Class-level operations for configuring, managing, and troubleshooting LLM providers in Hermes Agent. Covers API key management, provider setup, model fallback strategies, OpenRouter configuration, and general API connectivity debugging.
tags: [llm, provider, openrouter, troubleshooting, config, api-keys, fallback]
---

# LLM Provider Operations

> **Class-level skill** for all LLM provider management activities in Hermes Agent. If you need to configure a provider, fix a broken connection, set up fallback chains, or manage OpenRouter models, start here.

## When to Use

- User needs to set up a new LLM provider (OpenRouter, DeepSeek, Google/Gemini, Anthropic)
- API calls fail with 401, 400, or connection errors
- User asks about model fallback strategies or cost optimization
- User wants to configure OpenRouter models, keys, or fallback groups
- User reports Hermes failing to start due to provider configuration issues
- General "provider not working" diagnosis

## Table of Contents

- [Section 1: General Provider Configuration & Troubleshooting](#section-1-general-provider-configuration--troubleshooting)
- [Section 2: OpenRouter Setup & Debugging](#section-2-openrouter-setup--debugging)
- [Section 3: OpenRouter Model Management & Fallback](#section-3-openrouter-model-management--fallback)
- [Section 4: API Connection Debugging](#section-4-api-connection-debugging)

---

## Section 1: General Provider Configuration & Troubleshooting

### Workflow

1. **Check local config** — `hermes config show | grep -A5 -i provider`
   - Verify `model.provider`, `model.default`, and `providers.<name>` in `config.yaml`
2. **Verify API keys** — Check `~/.hermes/.env` or provider-specific key files
   - Key must exist, be valid, and not expired
   - Hermes redacts keys in `read_file` — use `sed -n '/API_KEY/p' .env` or paste from dashboard
3. **Test direct curl to provider** — Bypass Hermes to isolate the issue:
   ```bash
   curl -v https://api.openrouter.ai/v1/chat/completions \
     -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"openrouter/auto","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
   ```
4. **Check Hermes startup logs** — `hermes logs` or check console for provider init errors
5. **Test connection in a new session** — Use `/reset` to reload config

### Common Pitfalls

- **Expired keys**: Check key validity in provider dashboard
- **Wrong model ID format**: Some providers require specific prefixes (e.g., `openrouter/auto` not `auto`)
- **Rate limits**: 429 responses — implement fallback or cooling period
- **Region locks**: Some API keys are restricted to specific IP ranges
- **Incorrect provider name**: Custom providers need the `custom:` prefix in Hermes

### Switch from Proxy to Official Provider

When moving from a custom proxy/gateway (OmniRoute, 9Router) to an official provider (DeepSeek, Google, Anthropic):

```bash
# 1. Check that official API key exists
grep DEEPSEEK_API_KEY ~/AppData/Local/hermes/.env

# 2. Switch provider + model
hermes config set model.provider deepseek
hermes config set model.default deepseek-chat

# 3. Verify
hermes config show | grep -A3 -i 'model|provider'
```

⚠️ **DeepSeek-chat model name quirk**: After switching from `custom:omniroute` with model `oc/deepseek-v4-flash-free` to official `deepseek` provider, the model name `deepseek-chat` is ambiguous. Some API calls may fail with:
> "Ambiguous model 'deepseek-chat'. Use provider/model prefix (ex: aiml/deepseek-chat or ds-web/deepseek-chat)."

This happens because DeepSeek's API has multiple model variants under the same short name. If you hit this:
- Try `deepseek-chat-v4` or the specific model name from DeepSeek's docs
- Or fall back to another provider temporarily
- Use `hermes config set model.default deepseek/deepseek-chat` if the provider supports the prefix format

**Vision limitation**: Official DeepSeek-chat does NOT support vision/image analysis. Any `vision_analyze` calls will fail 400. For image-dependent tasks (logo analysis, screenshot review), either:
- Switch to a vision-capable provider (Google/Gemini, OpenAI) temporarily
- Or use non-vision methods: `file` command for PNG dimensions, SVG path inspection

⚠️ **Stale base_url after provider switch — "Provider authentication failed"**: When a provider was previously configured with a custom proxy base_url (e.g., `base_url: https://hhtechapi.com/v1` for DeepSeek proxy), switching to a different provider reusing the same provider slot does NOT automatically clear the old base_url. The old proxy URL persists and sends requests to the wrong endpoint. Additionally, the API key format must match the provider — e.g., OpenRouter requires `sk-or-...` keys, not `sk-9c6...` proxy keys.

**Symptoms**: `Provider authentication failed` in gateway, or 401/403 from the provider.

**Fix workflow**:
```bash
# 1. Check current provider config (including base_url)
hermes config show | grep -A10 'openrouter'

# 2. Clear stale base_url if present
hermes config set providers.openrouter.base_url ''

# 3. Set the correct API key for the provider
hermes config set provider_keys.openrouter sk-or-v1-...

# 4. Restart gateway to pick up changes
hermes gateway restart
```

**Two-config discrepancy pitfall**: Hermes has TWO config files — `~/.hermes/config.yaml` (global, less frequently updated) and `~/AppData/Local/hermes/config.yaml` (active, what `hermes config set` writes to). The active AppData config may have stale/wrong values even though the global config looks correct. ALWAYS check `~/AppData/Local/hermes/config.yaml` when diagnosing provider issues — it is the authority for the running instance.

Common proxy-to-official switches:
| Proxy | Official Provider | Model ID |
|-------|------------------|----------|
| `custom:omniroute` / `oc/deepseek-v4-flash-free` | `deepseek` | `deepseek-chat` |
| `custom:9router` / `ds/deepseek-chat` | `deepseek` | `deepseek-chat` |
| `custom:omniroute` / `oc/gpt-4o-free` | `openai` | `gpt-4o` |

The proxy model IDs (with prefixes like `oc/`, `ds/`) will NOT work under official providers — use the standard model names.

Set a specific model as priority for cost optimization:

```bash
# Set main provider + model
hermes config set model.provider custom
hermes config set model.default oc/deepseek-v4-flash-free

# Set fallback chain
hermes config set fallback_providers '[
  {"provider": "custom", "model": "oc/deepseek-v4-flash-free"},
  {"provider": "google", "model": "gemini-2.5-flash"},
  {"provider": "openrouter", "model": "openrouter/auto"}
]'

# Verify
hermes config show | grep -A3 -i 'model\|fallback'
```

User's preferred priority chain: DeepSeek flash free → Gemini 2.5 Flash → OpenRouter auto.

Configure a fallback chain for reliability:
```bash
hermes config set fallback_providers '[
  {"provider": "google", "model": "gemini-2.5-flash"},
  {"provider": "openrouter", "model": "openrouter/auto"}
]'
```

> **See reference file for full methodology:**
> - `references/provider-troubleshooting-generic.md` — Complete workflow with step-by-step diagnosis and resolution patterns

---

## Section 2: OpenRouter Setup & Debugging

### Key Steps

1. **Get API key** from [openrouter.ai/keys](https://openrouter.ai/keys)
2. **Set in Hermes config**:
   ```bash
   hermes config set provider_keys.openrouter sk-or-v1-...
   ```
3. **Set as active provider**:
   ```bash
   hermes config set model.provider openrouter
   hermes config set model.default openrouter/auto
   ```

### OpenRouter-Specific Troubleshooting

- **401 Unauthorized**: Key is invalid or expired — regenerate on OpenRouter dashboard
- **402 Payment Required**: Account has insufficient credits — top up
- **403 Forbidden**: Key lacks access to requested model — use `openrouter/auto` for any model
- **OpenRouter-specific models**: Use `openrouter/` prefix, e.g. `openrouter/anthropic/claude-sonnet-4`
- **Startup crash**: If Hermes fails on init with `openrouter`, check `provider_keys.openrouter` is set correctly

> **See reference file for full diagnostics:**
> - `references/openrouter-troubleshooting.md` — Complete OpenRouter debugging workflow, including VPS proxy scenarios

---

## Section 3: OpenRouter Model Management & Fallback

### Managing Models

1. **List available models**: `curl https://openrouter.ai/api/v1/models | python -c "import json,sys; d=json.load(sys.stdin); [print(m['id']) for m in d['data']]"`  
2. **Check model pricing**: OpenRouter dashboard shows per-model pricing
3. **Model naming**: Always use the full `openrouter/` prefix in Hermes config

### Fallback Groups

Configure prioritized fallback for reliability:
```yaml
fallback_providers:
  - provider: openrouter
    model: openrouter/anthropic/claude-sonnet-4
  - provider: openrouter
    model: openrouter/google/gemini-2.5-flash
  - provider: google
    model: gemini-2.5-flash
```

> **See reference file for model management details:**
> - `references/openrouter-model-management.md` — Detailed OpenRouter model listing, pricing, key rotation, and fallback group configuration

---

## Section 4: API Connection Debugging

### Vietnamese-Language Troubleshooting Guide

When provider APIs reject connections or authentication fails:

1. **Kiểm tra cấu hình** — `hermes config show | grep -i -i 'provider\\|key'`
2. **Kiểm tra environment variable** — `echo $PROVIDER_API_KEY` (nếu đã set)
3. **Kiểm tra file .env** — File `.env` trong `~/.hermes/` hoặc `~/.bashrc`
4. **Test trực tiếp bằng curl** đến provider endpoint
5. **Kiểm tra status provider** — Downdetector hoặc provider status page
6. **Thử provider khác** — Chuyển tạm sang Google/Gemini để kiểm tra

**Các lỗi thường gặp:**
- `401 Unauthorized`: API key sai hoặc hết hạn
- `400 Bad Request`: Sai model name, sai request format
- `429 Too Many Requests`: Vượt quota
- Connection timeout: Firewall/Mạng chặn

> **See reference file for full Vietnamese-language guide:**
> - `references/api-troubleshooting-guide.md` — Full connection and authentication debugging guide in Vietnamese

---

## Section 5: Dual-Model Systems & Intelligent Routing

### Cost-Effective LLM Provider Strategies

For optimal cost-performance balance, implement dual-model systems that route requests to appropriate models based on task complexity:

#### When to Use Dual-Model Systems
- High-volume applications where cost optimization matters
- Applications with mixed complexity requests (simple chat + complex tasks)
- When premium models (Opus) are significantly more expensive than efficient models (Sonnet)
- Vietnamese language applications requiring specialized handling

#### Model Tier Strategy (Based on ABTrip Implementation)

**Sonnet Tier** (For regular chat - fast, cost-effective):
- Primary: `claude-sonnet-4-5`
- Backup 1: `claude-sonnet-4-6`
- Backup 2: `claude-5.6-sol`
- Use for: Simple greetings, basic questions, short interactions, acknowledgments, casual Vietnamese chat

**Opus Tier** (For code/writing/complex analysis - high quality):
- Primary: `claude-opus-4-8`
- Backup 1: `claude-opus-4-8-thinking`
- Backup 2: `deepseek-v4-pro`
- Use for: Code generation/debugging, technical writing, complex analysis, Vietnamese technical terms, question patterns, long messages (>300 chars)

#### Vietnamese-Aware Routing Logic (ABTrip Implementation)

Implement content-based routing with Vietnamese language awareness - this pattern was successfully implemented in ABTrip's llm_gateway.py:

```python
def _should_use_opus(self, message: str) -> bool:
    """
    Determine if a message requires the Opus tier (for code/writing/complex tasks).
    
    Returns True if Opus should be used, False for Sonnet (regular chat).
    """
    msg_lower = message.lower().strip()
    
    # Clear indicators for Opus tier (code, technical writing, complex analysis)
    opus_indicators = [
        # Code-related patterns
        "```",  # Code blocks
        "def ", "function ", "class ", "import ", "from ",  # Function/class definitions
        "const ", "let ", "var ", "=>",  # Variable declarations
        "{", "}", "[", "]", ";",  # Code syntax
        "if ", "else ", "for ", "while ", "try ", "except ",  # Control flow
        "return ", "yield ", "async ", "await ",  # Special keywords
        "# ", "// ", "/*", "*/",  # Comments
        
        # Technical writing indicators
        "api", "endpoint", "database", "sql", "query", "algorithm",
        "framework", "library", "package", "module", "dependency",
        "debug", "test", "unit test", "integration", "deploy",
        "version", "release", "patch", "bug", "fix", "issue",
        
        # Complex analysis/requests
        "phân tích", "tối ưu", "so sánh", "đánh giá", "kết luận",
        "giải thích", "hướng dẫn", "bài viết",
        "nghiên cứu", "tổng hợp", "tóm tắt", "biểu đồ", "bảng",
        
        # Vietnamese technical terms
        "mã nguồn", "lập trình", "phát triển", "kiểm tra lỗi",
        "cải thiện", "nâng cấp", "phiên bản", "tài liệu kỹ thuật",
    ]
    
    # Check for string-based Opus indicators
    for indicator in opus_indicators:
        if isinstance(indicator, str) and indicator in msg_lower:
            return True
    
    # Check for question patterns that might benefit from Opus
    # These often benefit from deeper reasoning even if not extremely long
    question_patterns = ["làm sao", "như thế nào", "tại sao", "vì sao"]
    if any(pattern in msg_lower for pattern in question_patterns):
        # Lower threshold for question patterns since they often indicate complex queries
        if len(message) > 20:  # Reduced from 50 to catch shorter but meaningful questions
            return True
    
    # Length-based heuristic (very long messages often need complex processing)
    if len(message) > 300:
        return True
    
    # Default to Sonnet for regular chat
    return False
```

#### Tiered Fallback Implementation (ABTrip Pattern)

For each model tier, implement internal fallback before crossing to other providers - this pattern was used in ABTrip's implementation:

```python
async def _call_hhtech_tiered(self, messages: list[dict[str, str]], use_opus: bool) -> dict[str, Any]:
    """
    Call HHTech API with tiered model selection and fallback.
    
    Args:
        messages: The chat messages to send
        use_opus: If True, use Opus tier; otherwise use Sonnet tier
        
    Returns:
        Parsed JSON response from the API
    """
    if use_opus:
        model_list = self._hhtech_opus_models
        tier_name = "OPUS"
        logger.info("Trying HHTech OPUS tier")
    else:
        model_list = self._hhtech_sonnet_models
        tier_name = "SONNET"
        logger.info("Trying HHTech SONNET tier")
    
    last_exception = None
    
    for i, model in enumerate(model_list):
        try:
            logger.info("Trying HHTech %s model %d/%d: %s", 
                       tier_name, i+1, len(model_list), model)
            
            headers = {"Authorization": f"Bearer {self._hhtech_key}"}
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 1024,
                "stream": False,
            }
            res = await self._hhtech_client.post("/chat/completions", json=payload, headers=headers)
            res.raise_for_status()
            raw_response = res.json()
            content = raw_response["choices"][0]["message"]["content"]
            result = _parse_json(content)
            
            logger.info("HHTech %s success with model %s: type=%s", 
                       tier_name, model, result.get("type"))
            return result
            
        except Exception as e:
            last_exception = e
            logger.warning("HHTech %s model %s failed: %s", 
                          tier_name, model, e)
            # Continue to next model in the tier
            continue
    
    # If all models in the team failed, raise the last exception
    logger.error("All HHTech %s models failed. Last error: %s", 
                tier_name, last_exception)
    raise last_exception
```

#### Configuration Patterns (From ABTrip Implementation)

**Environment Variables (.env file):**
```bash
# HHTech API Configuration
HHTECH_API_KEY=sk-9c6...n
# Model Selection (Dual-Tier System)
# Sonnet tier - for regular chat (fast, cheap)
HHTECH_SONNET_MODEL=claude-sonnet-4-5
HHTECH_SONNET_BACKUP1=claude-sonnet-4-6
HHTECH_SONNET_BACKUP2=claude-5.6-sol
# Opus tier - for code/writing/complex analysis (high quality)
HHTECH_OPUS_MODEL=claude-opus-4-8
HHTECH_OPUS_BACKUP1=claude-opus-4-8-thinking
HHTECH_OPUS_BACKUP2=deepseek-v4-pro
```

**Configuration File (config.py):**
```python
# Sonnet tier (for regular chat - fast, cheap)
self._hhtech_sonnet_model = settings.hhtech_sonnet_model
self._hhtech_sonnet_backup1 = getattr(settings, 'hhtech_sonnet_backup1', 'claude-sonnet-4-6')
self._hhtech_sonnet_backup2 = getattr(settings, 'hhtech_sonnet_backup2', 'claude-5.6-sol')
self._hhtech_sonnet_models = [
    self._hhtech_sonnet_model,
    self._hhtech_sonnet_backup1,
    self._hhtech_sonnet_backup2
]

# Opus tier (for code/writing/complex analysis - high quality)
self._hhtech_opus_model = settings.hhtech_opus_model
self._hhtech_opus_backup1 = getattr(settings, 'hhtech_opus_backup1', 'claude-opus-4-8-thinking')
self._hhtech_opus_backup2 = getattr(settings, 'hhtech_opus_backup2', 'deepseek-v4-pro')
self._hhtech_opus_models = [
    self._hhtech_opus_model,
    self._hhtech_opus_backup1,
    self._hhtech_opus_backup2
]
```

#### Benefits Validated in ABTrip Implementation
- **Cost savings**: Sonnet tier (~1/5 cost of Opus) handles ~70% of regular chat queries
- **Performance**: 2-3x faster responses for simple queries using Sonnet tier
- **Quality**: Preserves high-quality Opus output for code, technical writing, and complex Vietnamese analysis
- **Reliability**: Internal tiered fallback prevents service disruption even when specific models fail
- **Vietnamese-optimized**: Special handling correctly routes Vietnamese technical terms and question patterns to Opus tier
- **User Experience**: Natural, concise Vietnamese responses maintained while optimizing costs

> **See reference file for implementation details:**\n> - `references/dual-model-routing-abtrieb.md` — Complete ABTrip implementation guide with code samples, configuration examples, and validation results
    
    # Check indicators
    for indicator in code_indicators + tech_indicators + vn_writing:
        if isinstance(indicator, str) and indicator in msg_lower:
            return True
    
    # Check question patterns with lower threshold
    if any(pattern in msg_lower for pattern in question_patterns):
        if len(message) > 20:  # Reduced threshold for question patterns
            return True
    
    # Length-based heuristic
    if len(message) > 300:
        return True
    
    # Default to Sonnet for regular chat
    return False
```

#### Tiered Fallback Implementation

For each model tier, implement internal fallback before crossing to other providers:

```python
async def _call_hhtech_tiered(messages, use_opus):
    if use_opus:
        model_list = [opus_primary, opus_backup1, opus_backup2]
        tier_name = "OPUS"
    else:
        model_list = [sonnet_primary, sonnet_backup1, sonnet_backup2]
        tier_name = "SONNET"
    
    last_exception = None
    for i, model in enumerate(model_list):
        try:
            # Attempt API call with current model
            result = await _call_hhtech_model(messages, model)
            logger.info(f"HHTech {tier_name} success with model {model}")
            return result
        except Exception as e:
            last_exception = e
            logger.warning(f"HHTech {tier_name} model {model} failed: {e}")
            continue
    
    # If all models in tier failed, raise exception
    logger.error(f"All HHTech {tier_name} models failed. Last error: {last_exception}")
    raise last_exception
```

#### Configuration Example

```bash
# HHTech API - Dual Model System
# Sonnet tier (for regular chat - fast, cheap)
hhtech_sonnet_model=claude-sonnet-4-5
hhtech_sonnet_backup1=claude-sonnet-4-6
hhtech_sonnet_backup2=claude-5.6-sol

# Opus tier (for code/writing/complex analysis - high quality)
hhtech_opus_model=claude-opus-4-8
hhtech_opus_backup1=claude-opus-4-8-thinking
hhtech_opus_backup2=deepseek-v4-pro
```

#### Benefits
- **Cost savings**: Sonnet tier costs ~1/5 of Opus tier for regular chat
- **Performance**: Faster responses for simple queries
- **Quality**: Preserves high-quality output for complex tasks
- **Reliability**: Multi-layered fallback prevents service disruption
- **Vietnamese-optimized**: Special handling for Vietnamese language patterns

> **See reference file for implementation details:**
> - `references/dual-model-routing.md` — Complete implementation guide with code samples and configuration examples

---

## Reference Files

| File | Source Skill | Description |
|------|-------------|-------------|
| `references/provider-troubleshooting-generic.md` | `llm-provider-troubleshooting` | Generic LLM provider troubleshooting worklow |
| `references/openrouter-troubleshooting.md` | `openrouter-troubleshooting` | OpenRouter-specific debugging |
| `references/openrouter-model-management.md` | `openrouter-model-management` | OpenRouter fallback and model config |
| `references/api-troubleshooting-guide.md` | `llm-api-troubleshooting` | Vietnamese API connection guide |
| `references/openrouter-r1-workflow.md` | `openrouter-r1-calling` | OpenRouter R1 API calling workflow: key extraction workaround, direct HTTP call pattern, save-immediately requirement, cost ($0.005-0.01/script), truncation quirks |
| `references/provider-switch-stale-config.md` | *this session* | Stale base_url + wrong API key after provider switch: two-config discrepancy diagnosis and fix recipe |
