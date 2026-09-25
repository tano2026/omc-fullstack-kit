# Goose AI Agent — Windows Install & Configure Guide

## Version Installed
- **Binary:** `C:\Users\Nguyen Ngoc Tan\goose\goose.exe`
- **Version:** 1.43.0
- **Date:** 2026-07-19

## Installation

```bash
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash
```

Goose auto-installs to `~/goose/goose.exe` and `~/goose/skills/`.

## Provider Config

Config file: `C:\Users\Nguyen Ngoc Tan\AppData\Roaming\Block\goose\config\config.yaml`

### DeepSeek Configuration

```yaml
providers:
  openai:
    model: deepseek-chat
    api_key_env: DEEPSEEK_API_KEY
    base_url: https://api.deepseek.com/v1
```

### Known Issues

**Issue #9041:** `deepseek-v4-flash` and `deepseek-v4-pro` models have a thinking mode that returns `reasoning_content` in the response. Goose's backend (goosed.exe) does not handle this field, causing a 400 error on follow-up turns:
```
Request failed: Bad request (400): Error from provider (DeepSeek):
The reasoning_content in the thinking mode must be passed back to the API.
```

**Fix:** Use `deepseek-chat` (the standard model) instead of V4 flash/pro models. DeepSeek V4 models are not available under the `deepseek-chat` name if that's all your API key has access to — check with `curl https://api.deepseek.com/v1/models`.

## Interactive Setup

Goose requires an interactive terminal. **It cannot be configured via Hermes terminal tool** (bash non-PTY). Steps:

1. Open Git Bash or Command Prompt
2. Set your API key: `export DEEPSEEK_API_KEY=***` (on Windows: `set DEEPSEEK_API_KEY=***`)
3. Run interactive config: `~/goose/goose.exe configure`
4. Dialog flow:
   - Share usage data? → `n`
   - Select provider → `OpenAI` (DeepSeek is OpenAI-compatible)
   - Model → `deepseek-chat`
   - API Key env var → `DEEPSEEK_API_KEY`
   - Base URL → `https://api.deepseek.com/v1`
   - Save to keyring? → `Yes`
5. The model fetch step will likely fail (401) — this is OK because the API key might only have access to V4 models, not standard `deepseek-chat`. The core config works without a successful model fetch.
6. Test: `DEEPSEEK_API_KEY=*** ~/goose/goose.exe doctor`

### Env var loading pitfall
The `.env` file in the project root has `DEEPSEEK_API_KEY` but it's not loaded automatically in Git Bash. Use:
```bash
cd /d/"MMO Du an"/TANO-AGENCY/PLATFORM/agent-core
source .env
/c/Users/"Nguyen Ngoc Tan"/goose/goose.exe session
```
Or set export inline.

## Usage

```bash
# Interactive session (best for code work)
DEEPSEEK_API_KEY=*** ~/goose/goose.exe session

# Session management
~/goose/goose.exe session list      # List all sessions
~/goose/goose.exe session remove    # Remove sessions interactively
~/goose/goose.exe session export    # Export a session
~/goose/goose.exe session import    # Import from JSON

# Diagnostics
~/goose/goose.exe doctor            # Health check
```

## Architecture

Goose is a standalone AI agent tool (similar to Claude Code) that:
- Writes and edits code
- Runs terminal commands
- Has session-based memory
- Supports MCP extensions
- Works with any OpenAI-compatible provider

It is NOT an orchestrator or multi-agent system — it's a single-agent developer tool. For the TANO-AGENCY company-of-one, use Goose for focused code/development tasks where its superior coding capabilities (function calling, tool use) outperform the CEO bot's generic chat.
