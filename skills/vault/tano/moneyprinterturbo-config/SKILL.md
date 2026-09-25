---
name: moneyprinterturbo-config
description: Full workflow for MoneyPrinterTurbo — install, configure WebUI, and generate video with pre-written script + local images. Alternative to the custom video-production-pipeline.
---

# MoneyPrinterTurbo — Full Workflow

MoneyPrinterTurbo (MPT) is a turnkey video generator: paste a script → select video source → get a complete video with subtitles. This skill covers the **"already have a script"** workflow (WebUI mode), not the topic-generation mode.

## When to Use

- You have a pre-written script (no need for AI script generation)
- You want a quick render with subtitles and voiceover
- You have local images/storyboard instead of Pexels stock footage
- User says "làm MPT" or "lên MPT"

## Two Modes of Operation

| Mode | MPT tab | Script source | When |
|------|---------|--------------|------|
| **Topic-gen** | "Video Topic" tab | MPT's LLM writes the script | Starting from scratch with a topic |
| **Script-paste** ⭐ | **"Video Subject / Script"** tab | You paste existing script | **When you already have a script** (this skill) |

## ⚠️ Python Version Warning

**MPT requires Python <3.14** — `litellm==1.86.2` (and likely newer pins) requires Python >=3.10,<3.14. If `pip install -r requirements.txt` fails with `Could not find a version that satisfies the requirement litellm`, the system Python is too new.

**ALWAYS use `uv sync` as the primary install method** — uv auto-detects the nearest compatible Python (e.g. 3.11, 3.12) and creates its own `.venv`. `pip install -r requirements.txt` only works when the system Python is <3.14. If pip fails, delete the venv and retry with uv.

## Step 1 — Installation

```bash
cd /d/MMO\\ Du\\ an
git clone --depth 1 https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo

# ✅ REQUIRED (handles Python version compatibility)
uv sync
```

After `uv sync`, binaries go in `.venv/Scripts/` (not `venv/Scripts/`). The project has a `uv.lock` so dependency resolution is instant.

## Step 2 — Configuration

Copy the template and edit `config.toml` (at the repo root, not in a `config/` subdirectory):

```bash
cp config.example.toml config.toml
```

## Step 3 — Start (TWO components)

MPT has a **two-tier architecture**:

| Component | Port | Command | Purpose |
|-----------|------|---------|---------|
| Backend API | **8080** | `python main.py` | FastAPI server — processes tasks, renders videos, serves API at `/docs` |
| WebUI (Streamlit) | **8501** | Streamlit on `webui/Main.py` | Browser UI for pasting scripts, uploading images, triggering renders |

**Both must be running** for the WebUI to work. Start them in order:

### 3a — Backend API (port 8080)
```bash
cd MoneyPrinterTurbo
.venv/Scripts/python.exe main.py
# Opens at http://127.0.0.1:8080 — just a landing page + API docs
```

### 3b — WebUI (port 8501)
Open a **second terminal**:
```bash
cd MoneyPrinterTurbo
.venv/Scripts/python.exe -m streamlit run webui/Main.py --server.address=127.0.0.1 --server.port=8501 --browser.serverAddress=127.0.0.1 --browser.gatherUsageStats=False --client.toolbarMode=minimal --logger.hideWelcomeMessage=True --server.showEmailPrompt=False
```

Alternatively, run `webui.bat` (auto-detects the venv Python):

```bash
cd MoneyPrinterTurbo
.\webui.bat
```

**The actual WebUI is at: http://127.0.0.1:8501**

### 3c — Kill both when done
```bash
# Find by port and kill
taskkill /F /PID $(netstat -ano | grep :8080 | grep LISTENING | awk '{print $5}')
taskkill /F /PID $(netstat -ano | grep :8501 | grep LISTENING | awk '{print $5}')
```

## Config — local images mode

Key settings for local-image workflow:

```toml
# Use "local" when you upload images manually via WebUI
video_source = "local"

# Edge TTS timeout — increase to 60 if you hit timeouts
edge_tts_timeout = 60

# Disable LLM (you paste script manually, no AI generation needed)
llm_provider = "moonshot"
moonshot_api_key = ""

# Edge TTS subtitles (free, fast)
subtitle_provider = "edge"
```

**In WebUI, set:**
- Video Source: **"Pexels"** (even if using local — the local/upload option appears)
- Enable: **Upload Local Videos** → upload your PNG/JPG images
- LLM Provider: **disable** script generation (since you paste your own)
- Subtitle Provider: **"edge"** (free, fast)
- Video Subject / Script: paste your full script

### Key advanced config options:
```toml
# Subtitle style
[ui]
subtitle_position = "bottom"
# Or "custom" with custom_position = 70.0

# Proxy if needed for stock video downloads
[proxy]
# http = "http://proxy:3128"
# https = "http://proxy:1080"
```
## Step 4 — WebUI Workflow (Script-Paste)

1. Tab: **"Video Subject / Script"** (NOT "Video Topic")
2. **Subject:** Enter a short title (e.g., "30-40 Tuổi — Thức Tỉnh Trước Khi Quá Muộn")
3. **Video Script:** Paste your full script text
4. **Video Source / Background:** Choose "Upload/Local" → upload your images
5. **Voice:** Select desired Edge TTS voice (vi-VN-NamMinhNeural for Vietnamese)
6. **Subtitle:** Enable "Generate Subtitles" (edge provider)
7. Click **Generate** → wait for render → download MP4

### Script formatting tips:
- MPT expects **plain text only** — NO markdown (`#`, `**`, `##`), NO timestamps (`[00-60]`, `[120-200]`), NO metadata lines
- Line breaks in script = natural subtitle breaks (MPT auto-splits into segments)
- The script duration is estimated based on TTS speed; MPT auto-adjusts
- **Clean a script for MPT**: strip all `[00-60]` timestamps, `###` headers, `---` separators, and markdown formatting. Keep only the spoken paragraphs.
- MPT handles long scripts (5000+ words) fine via the WebUI; no need to chunk

## Step 5 — If Video Has No Audio

After render, verify streams:

```bash
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 /path/to/output.mp4
```

Should contain both `video` and `audio`. If missing audio:
- The issue is usually: MPT's FFmpeg step lost the audio stream
- Try reducing video_source to a single image or regenerate

## Edge TTS Timeout Troubleshooting

If MPT logs show `edge_tts stream timed out after 30s`, the Edge TTS API is unreachable (common in certain regions):

**Fix A — Proxy:**
```toml
[proxy]
http = "http://your-proxy:port"
https = "http://your-proxy:port"
```
Then restart WebUI.

**Fix B — OpenAI TTS (if you have an OpenAI key):**
1. Set `llm_provider = "openai"` with a working `openai_api_key` in `config.toml`
2. In WebUI, select OpenAI voice instead of Edge TTS
3. Note: OpenAI TTS costs money per character

**Fix C — Custom audio (pre-generated externally):**
1. Generate audio separately (e.g. Resona TTS, Edge TTS via a proxy machine)
2. MPT's "Upload Video" mode can accept video with pre-embedded audio
3. Or generate video with MPT (muted) and replace audio with FFmpeg post-render:
   ```bash
   ffmpeg -i mpt_video.mp4 -i custom_audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
   ```

**Fix D — Increase timeout** (if Edge TTS just needs more time):
```toml
edge_tts_timeout = 60  # default is 30
```

## Handoff from Custom Pipeline

When the main pipeline (Resona TTS + make.py/FFmpeg) fails, you can fall back to MPT:

1. Extract the script text from your markdown file: strip timestamps `[00-60]`, metadata headers, and markdown formatting — keep only spoken paragraphs
2. Export as a `.txt` file (not markdown)
3. Open MPT WebUI → "Video Subject / Script" tab
4. Paste the clean text into the "Video Script" field
5. Upload your storyboard images as local video background
6. Generate — MPT handles the rest (TTS + subtitles + video)

This is useful when:
- Custom pipeline's TTS (Resona) hits credit limits
- FFmpeg concat has issues
- You need a quick render to verify timing/flow

## Pitfalls

1. **MPT not installed?** Run `git clone --depth 1` + `uv sync` (Step 1). No Docker needed unless specified. Do NOT use `pip install -r requirements.txt` unless you are on Python 3.10-3.13.
2. **WebUI not opening?**  
   - Port 8080 (API) vs 8501 (WebUI). The WebUI is at **8501**, not 8080. Make sure both are running.  
   - Check running: `netstat -ano | grep LISTENING | grep -E '8080|8501'`  
   - Kill port: `taskkill /F /PID $(netstat -ano | grep :PORT | grep LISTENING | awk '{print $5}')`
3. **Local images not appearing?** Use MPT's "Upload Local Videos" button in WebUI — it accepts JPG/PNG. Or set `material_directory` in app.toml to point to your images folder.
4. **Subtitles not generating?** Set `subtitle_provider = "edge"` in config.toml and enable in WebUI.
5. **Short render fails?** MPT defaults to ~60s minimum for some modes. For very short scripts (<30s), extend with repeated content or use FFmpeg directly instead.
6. **Long scripts (>1000 words)?** MPT handles them fine via the WebUI. No need to chunk.
7. **⚠️ Long Vietnamese scripts (>3000 chars) — Edge TTS timeout:** MPT's built-in Edge TTS **frequently times out** on Vietnamese scripts longer than ~3000 characters (about 5-7 min of speech). The backend gets stuck at `state=4 progress=20` indefinitely. Increasing `edge_tts_timeout` to 60+ in config.toml does NOT fix this.
8. **⚠️ Custom audio workaround also fails for long scripts:** Submitting a task with `custom_audio_file` pre-generated (Resona) results in `state=-1` (silent fail) when the script exceeds ~5000 chars with a single static image. The subtitle sync + FFmpeg assembly can't handle long-form single-image content.
9. **⚠️ MPT scope:** Only suitable for **short-form content (<3 min)** where Edge TTS can complete in one pass. For 10+ min Vietnamese videos with single-image background, use HyperFrames + Resona pipeline (`sk:gmsp-modular-pipeline`).
7. **Python 3.14+:** If `pip install -r requirements.txt` fails on `litellm`, the system Python is too new. Delete the venv, use `uv sync` instead — uv auto-detects the nearest compatible Python (e.g. 3.11, 3.12) and creates its own `.venv`. The project has a `uv.lock` so resolution is instant.
10. **Two-port confusion:** Backend API = :8080 (FastAPI), WebUI = :8501 (Streamlit). **ALWAYS open http://127.0.0.1:8501** for the actual WebUI. Opening :8080 in a browser only shows a static landing page with no functionality.
11. **Process management:** After starting `main.py` or the WebUI in the background, kill by PID: `taskkill /F /PID <PID>`. Find PIDs: `netstat -ano | findstr :8080` then `netstat -ano | findstr :8501`.

## ⛔ MPT Không Phù Hợp Cho GMSP

MPT thất bại với pipeline GMSP (video dài, 1 ảnh nền, Resona TTS) vì:

1. **Edge TTS timeout** — Script >6000 từ tiếng Việt → Edge TSS mất kết nối, stuck ở state=4/progress=20
2. **Custom audio không sync** — `custom_audio_file` với Resona pre-gen → MPT không tính được subtitle timing, task failed (state=-1)
3. **1 ảnh nền duy nhất** — MPT sinh ra cho multi-clip stock footage, không waveform/branding overlay

**Dùng MPT cho:** Video ngắn <3 phút, stock footage, Edge TTS ngắn.
**Pipeline GMSP dùng:** HyperFrames + Resona TTS + CapCut (manual) hoặc FFmpeg ghép SRT (auto).

## Config Template

Full TOML config template is below. Only the sections above need active changes — most defaults work for the script-paste workflow.

```toml
[app]
video_source = "pexels"
hide_config = false
edge_tts_timeout = 30
tls_verify = true
pexels_api_keys = []
pixabay_api_keys = []
coverr_api_keys = []
llm_provider = "openai"
openai_api_key = ""
openai_base_url = ""
openai_model_name = "gpt-4o-mini"
subtitle_provider = "edge"
material_directory = ""
max_concurrent_tasks = 5
max_queued_tasks = 100

[ui]
hide_log = false

[proxy]

[azure]
speech_key = ""
speech_region = ""

[siliconflow]
api_key = ""
```
