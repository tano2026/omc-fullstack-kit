---
name: gmsp-modular-pipeline
description: "7-stage modular video production pipeline for GMSP — independent stages, no redo from scratch. Dual format: YouTube (10-12min) + TikTok clips from same script."
---

# GMSP Modular Pipeline

Pipeline 7 stage cho sản xuất video GMSP. Mỗi stage là script riêng, input/output qua file. Có thể chạy lại từng stage độc lập.

**Triết lý: "Không sa đà — ship trước, auto sau."** Giai đoạn này tập trung ra video 1 tháng/tập, không over-engineer pipeline. Auto hoá từ từ khi workflow ổn định.

[Content below remains identical to current SKILL.md, just ensuring the format is correct]

## Stages

| # | Stage | Input | Output | Script |
|---|-------|-------|--------|--------|
| 1 | **Nghiên cứu** | Chủ đề | `01-research.md` | `01_research.py` |
| 2 | **Chiến lược nội dung** | Research | `02-strategy.md` | `02_content.py` |
| 3 | **TTS** | Script | `voiceover_*.mp3` + segments | `03_tts.py` |
| 4 | **Media** | Script | `images/frame-*.png` | `04_media.py` |
| 5 | **Render** | TTS + Ảnh | `episode-*.mp4` (YT) + clips (TikTok) | `05_render.py` |
| 6 | **Đăng bài** | Video | YouTube + TikTok post | `06_publish.py` |
| 7 | **Social** | Post | Analytics/tương tác | `07_social.py` |
