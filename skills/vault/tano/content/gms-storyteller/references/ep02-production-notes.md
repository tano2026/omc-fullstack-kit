# EP02 Production — Key Decisions (2026-07-17)

## Script stats
- Written by: DeepSeek R1 via OmniRoute (`auto/best-reasoning` → `big-pickle`)
- Length: 14,136 chars → Edge TTS: 17.5 min (not 12.9 as estimated)
- Sections: 6 (HOOK, BỐI CẢNH, TỬ VI, TÂM LÝ & ĐỊNH LUẬT, GIẢI PHÁP, CLIFF)
- Brand mentions: 5 (HOOK 1, mid-roll 1, end 2, cliffhanger 1) → user OK'd
- After user correction: mark "Kênh này là..." removed from HOOK → 4 mentions, clean

## Edge TTS production
- 11 segments (later 13 after splitting failed ones)
- Rate: +14% (down from +16% for reliability)
- Max segment: 1500 chars → 700-800 chars for retry
- Timeout: 45s per segment
- Failed segments: seg-004 (1497 chars) + seg-006 (1496 chars) → split into 2 each
- Total voiceover: 1050s (17.5 min) incl 6×6s gaps
- Rate recalibration: 800 chars/min (not 1100)

## Base video
- Copied from EP01 `ep01_base_v3.mp4` (800s)
- Extended to 1100s via `-stream_loop 2` loop (needed 1050s)
- Final: `ep02_base_ext.mp4`

## Chapter transitions (5 chapters)
Timings computed from voiceover concat order:
| Chapter | Time | Title |
|---------|------|-------|
| 1 | 94.9-100.9s | Bẫy Thời Gian |
| 2 | 308.7-314.7s | Bẫy Kỹ Năng |
| 3 | 416.9-422.9s | Bẫy An Toàn |
| 4 | 467.3-473.3s | Pareto 80/20 |
| 5 | 673.6-679.6s | Xoay chuyển thời thế |

## Thumbnail
- Source: FAL image gen (dark academic, bookshelf, businessman)
- Addition: dark gradient overlays (top 300px + bottom 250px)
- Font: Playfair Display (downloaded from Google Fonts)
- Text: TẬP 02 + "Bí Mật Giới Tinh Hoa" + subtitle
- Output: `ep02_thumbnail.png`

## Font lesson
- Windows không có Playfair Display mặc định
- Playbill (PLAYBILL.TTF) xấu — font gothic thô, ko phải serif
- Fix: download từ https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf
- Save: `C:/Users/Nguyen Ngoc Tan/playfair-display.ttf`
- Bold variant: URL 404 → dùng variable font với weight

## Background scene tag fix
User complaint: "Sao vẫn là tập 1"
Fix: drawtext overlay:
```bash
ffmpeg -i base.mp4 -vf "drawtext=text='TẬP 02 · BÍ MẬT GIỚI TINH HOA':\
  fontcolor=#FFD700:fontsize=28:x=16:y=16:\
  fontfile='C:/Users/Nguyen Ngoc Tan/playfair-display.ttf'" output.mp4
```

## Final file
- `D:/ep02_final.mp4` (4.0 MB, 480p, Telegram-ready)
- Steps: script → TTS (Edge, 13 segs) → base extend → chapters overlay → scene tag → compress
