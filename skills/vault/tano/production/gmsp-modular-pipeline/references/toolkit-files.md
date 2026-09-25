# Toolkit References — loaded from AI Vibe Toolkit to GMSP

7 reference files have been loaded from the AI Vibe Toolkit into `GMSP/research/references/`. 
These are here so the agent can read them when writing script, gen media, or publishing.

## Master list

| # | File | Source skill | Purpose |
|---|------|-------------|---------|
| 01 | `01-storytelling-system-prompt.md` | content-agent-pipeline | Core prompt for writing YT scripts with 3-Act + frame structure |
| 02 | `02-frame-scaling.md` | content-agent-pipeline | Frame count by duration, narration word count formulas |
| 03 | `03-gemini-image-gen.md` | video-production-pipeline | Free image gen with Gemini 2.5 Flash ($0, 60 req/min) |
| 04 | `04-windows-render.md` | video-production-pipeline | FFmpeg 8.1.1 concat + raw H.264 on Windows |
| 05 | `05-ass-subtitles.md` | video-production-pipeline | Netflix-style burnt-in subs via ASS |
| 06 | `06-youtube-marketing.md` | youtube-marketings | 21 commands for YouTube SEO, title, tags, desc |
| 07 | `07-competitor-adaptation.md` | content-agent-pipeline | Convert competitor topics → GMSP content |

## When to load each

- **Script writing →** read 01 + 02 first
- **Image gen →** read 03 for Gemini API details
- **Render on Windows →** read 04 + 05 for FFmpeg pitfalls
- **Publishing →** read 06 for YouTube metadata
- **Choosing topics →** read 07 for competitor research patterns
