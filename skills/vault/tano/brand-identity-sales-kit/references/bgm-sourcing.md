# BGM Sourcing Guide — Free, Copyright-Safe Background Music

## Best Source: Pixabay Music

**URL:** https://pixabay.com/music/
**License:** Pixabay License (free, no attribution required, YouTube monetization safe)
**Blocks:** curl/wget (Cloudflare protection) — use `cloudscraper` (Python) or browser tool

## Search Terms by vibe

| Vibe | Search terms | Typical duration |
|------|-------------|-----------------|
| Dark cinematic | `dark cinematic`, `dark ambient`, `dark mystery` | 2-5 min |
| Mysterious | `mysterious cinematic`, `suspense`, `thriller` | 2-4 min |
| Asian/traditional | `asian ambient`, `japanese traditional`, `chinese music` | 1-3 min |
| Epic trailer | `cinematic trailer`, `dark mystery trailer` | 30s-1min |
| Calm/ambient | `ambient`, `atmospheric`, `calm background` | 3-7 min |

## Track Selection Criteria

- Instrumental only (no lyrics/vocals — interferes with voiceover)
- Loopable (gradual fade in/out, no abrupt stops)
- Matches brand tone (dark/cinematic for GMSP, not upbeat/happy)
- Free/Pixabay license (avoid Creative Commons requiring attribution in description)

## BGM Tracks for GMSP

### Background (main video, 10-15 min, loopable)
1. **"Dark Cinematic"** by leberch (3:06) — dark, suspenseful, good loop
2. **"Mysterious Cinematic Music"** by Tunetank (4:23) — mysterious, orchestral
3. **"Dark"** by The_Mountain (2:20) — ambient, minimalist

### Intro (branded, 30-60s)
1. **"Dark Mystery Trailer (Taking Our Time)"** by AlexGrohl (0:48) — epic, trailer-style

### Music loop extension
For videos longer than track duration, use FFmpeg to loop:
```bash
ffmpeg -stream_loop -1 -i bgm_track.mp3 -t 900 -c copy bgm_loop_15min.mp3
```

## File Naming Convention

```
assets/bgm/
├── bgm_dark_cinematic.mp3    # Background track
├── bgm_mysterious.mp3        # Alternative background
├── bgm_intro.mp3             # Intro bumper
└── README.md                 # Track attribution (optional, Pixabay doesn't require)
```

## License Notes

- **Pixabay License**: Free for commercial use, no attribution required. Safe for YouTube monetization.
- **Shield icon** on Pixabay = verified license (prioritize these)
- **AI-generated tags**: Some tracks are AI-generated — still fine, Pixabay license covers them
- **Avoid**: Creative Commons "BY" tracks (require attribution in video description)
- **Avoid**: YouTube Content ID-flagged tracks (test before publishing)
