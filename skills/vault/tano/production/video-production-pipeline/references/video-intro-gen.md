# Video Intro Generation — Session-Specific Detail

> Absorbed from `video-intro-gen` (Jul 2026)

## Unique Technical Detail Not Covered in Umbrella Summary

### Concept Refresh Rule
When user says "giống cái cũ, giữ nguyên concept" — **interpret this as: "use the same brand/vibe, but generate 100% new visual concept with different imagery."** Never reuse the same generated images or animation from a previous intro. Each intro should be visually distinct while maintaining brand consistency.

### Gemini/Veo for Intro Generation
- Google Gemini cannot generate video (Veo) via API yet — video generation is only available in the web UI
- Use FFmpeg to build intro from still frames + transitions instead of AI video generation
- Brand intro prompt template (GMSP brand example):
  ```
  Phong cách Dark Academia kết hợp với hình ảnh triết học, sách cổ, đồng hồ cát, bầu trời sao, kiến trúc Gothic.
  Tông màu chủ đạo: xanh lá đậm (#1a6b3c) và đen.
  Ánh sáng ấm, mờ khói, cảm giác huyền bí và trí tuệ uyên thâm.
  ```

### FFmpeg Watermark Workflow
When intro has a branding watermark to crop:
1. Detect watermark position via `ffmpeg -vf "cropdetect"` or manual inspection
2. Crop it out: `-vf "crop=W:H:x:y"` where W/H/x/y are adjusted
3. Re-encode to maintain quality
4. If watermark is in a corner, consider covering with a semi-transparent overlay rect instead (less destructive)

### Intro Format Specifications
- **Duration:** 8-15 seconds (12s is standard)
- **Audio:** Ambient + branding jingle (not speech), fade out at 11s
- **Resolution:** 1920×1080, same as main video
- **Transition:** Crossfade from intro into first content frame
- **Text overlay:** Channel name + episode tagline, 3-5s hold before fade
