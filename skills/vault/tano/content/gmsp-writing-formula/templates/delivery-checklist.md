# GMSP Delivery Checklist — 1 Episode

## Giai đoạn 1: Script
- [ ] Research topic (Tử Vi lens + tâm lý lens + định luật)
- [ ] Viết script 6 section (HOOK → BỐI CẢNH → TỬ VI → TÂM LÝ → GIẢI PHÁP → CLIFF)
- [ ] Tên kênh 3 lần: Hook + Mid-roll + Cliffhanger
- [ ] 2 case study cụ thể (có tên, cảnh, thoại)
- [ ] Nối case study xuyên suốt
- [ ] Không số liệu bịa
- [ ] User duyệt script

## Giai đoạn 2: TTS
- [ ] Split script → segments (max 800 chars/seg, 3s silence giữa section)
- [ ] Sanitize text (bỏ quote kép, em dash, bold)
- [ ] Resona Trung Thành (speed 0.82-0.9, pitch 1.0)
- [ ] Nếu credit limit → đợi + resubmit (hoặc Edge fallback)
- [ ] Concat → voiceover_full.mp3
- [ ] Verify duration, nghe thử

## Giai đoạn 3: Base Video
- [ ] HyperFrames init (nếu chưa có project)
- [ ] Update duration = voiceover + 150s đệm
- [ ] 4-corner branding: logo + scene tag + brand + subscribe
- [ ] Waveform bars 120 bar seeded PRNG
- [ ] `npx hyperframes check` — 0 errors
- [ ] `npx hyperframes render --quality draft`

## Giai đoạn 4: Delivery
- [ ] Copy voiceover → delivery/voiceover_epXX_trungthanh.mp3
- [ ] Copy base video → delivery/background_epXX_base.mp4
- [ ] Copy script → delivery/script.md
- [ ] Gửi user link file (hoặc Tele)

## Optional: Full render
- [ ] Tạo SRT subtitle (16-20 entries, no ASS)
- [ ] BGM loop (dark cinematic, mix 0.15)
- [ ] FFmpeg ghép: base + voiceover + bgm + srt
