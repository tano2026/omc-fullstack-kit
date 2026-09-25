# Edge TTS for GMSP — Segment Generation & Timing

## Timing calibration (Jul 2026)
Edge TTS `vi-VN-NamMinhNeural` rate +16%:

| Metric | Old estimate | Actual (EP02) |
|--------|-------------|---------------|
| Chars/min | 1,100 | ~800 |
| 14,000 chars | ~12.7 min | ~17.5 min |
| 13,000 chars | ~11.8 min | ~16.3 min |

**Công thức mới**: thời gian = ký tự / 800 (phút)

## Segment generation rules
- Segment size: 700-800 chars (safe), 1500 chars (risky — ~60-70% success)
- Rate: +16% normal, +8% trầm (slow/deep), +25% cao trào (fast/climax)
- Retry: nếu +16% fail → thử +12%
- Timeout: 45s per segment (subprocess timeout, not network)

## Section boundary timing
Khi tính timing cho chapter overlays, dùng cumulative segment durations + gap lengths.
