# Pipeline Format Mismatch Audit — GMSP Case Study (July 2026)

## Symptom

`make.py status` shows all domains as "⏳ Đang chờ" (pending) even though work has been done — episodes exist in subdirectories with scripts, images, audio, and rendered video.

## Root Cause: Format Mismatch

The pipeline (`make.py`) was designed for **short-form content** (15-45s TikTok/Shorts):

```
Rate: +15% → ~838 words → ~2-3 min
Word/s: 168 → ~5-7 words/sec (fast pace)
```

But scripts like **#15 "30-40 Tuổi"** are **long-form** (~16 min, 5K words).

**Result:** make.py tracks 3 domain-level "episodes" as placeholders but never runs them because:
1. The domain-level entries (bi-kip-co-kim, giai-ma-so-phan, phat-trien-ban-than) are too coarse — they're categories, not individual episodes
2. Individual episode folders (e.g. `episodes/phat-trien-ban-than/tl-15-tuoi-30-40/`) aren't registered in make.py's internal tracking
3. The pipeline wraps per-domain, but actual content is produced per-episode at a deeper level

## Episode Registration Structure

```
make.py status → tracks DOMAIN-level entries (3 items):
  - bi-kip-co-kim
  - giai-ma-so-phan
  - phat-trien-ban-than

Actual content lives at EPISODE level:
  episodes/phat-trien-ban-than/tl-15-tuoi-30-40/
  episodes/phat-trien-ban-than/tl-14-.../
  episodes/bi-kip-co-kim/tl-01-.../
  episodes/giai-ma-so-phan/tv-01-.../
```

The pipeline never "sees" individual episodes. When you work on `tl-15`, the pipeline still shows "pending" because it's tracking the domain, not the episode.

## How to Fix (per domain/pipeline)

### Option A: Register episodes in make.py
If the pipeline supports per-episode registration:
```python
# In make.py's domain config, add episodes array:
DOMAINS = {
    "phat-trien-ban-than": {
        "episodes": ["tl-15-tuoi-30-40", "tl-14-..."],
        ...
    }
}
```
Then `make.py run phat-trien-ban-than tl-15-tuoi-30-40` should work.

### Option B: Bypass make.py for long-form
Since make.py is tuned for shorts, for long-form content use:
- `gen_audio.py` + `gen_video.py` from `scripts/` directly (these support `--pack` + `--ep`)
- Or manual pipeline per the `video-production-pipeline` skill

## Fragmented Rendering History

Work on `tl-15-tuoi-30-40` went through 3 approaches without completing any:

| Approach | Status | Issue |
|----------|--------|-------|
| **FFmpeg direct** (segment render) | ❌ | Audio dropped after concat; no `-map 1:a` |
| **HyperFrames** (tried for intro) | ❌ | Chromium storage limit >30s on Windows |
| **CapCut** (manual) | ❌ | Not automated, stopped halfway |

**Lesson:** When switching rendering approaches mid-episode, data fragmentation makes it worse:
- Multiple audio versions (no "final" tagged)
- Video segments at different stages
- No single command to resume from interruption

## Verification Checklist for Pipeline Recovery

When picking up a stalled episode:

- [ ] `make.py status` shows domains, not episodes — check the actual episode dir
- [ ] Audio: are there multiple `.mp3`/`.wav` files? Which is final?
- [ ] Scenes: track.json exists? How many frames vs how many images?
- [ ] Images: count != frames → gen_video.py silently skips unmapped frames
- [ ] Previous render approach: check for `_concat_list.txt`, `.hyperframes/`, CapCut exports
- [ ] **Pick ONE approach and commit** — don't switch again mid-episode

## Decision Matrix

| Factor | Short-form (<3 min) | Long-form (>5 min) |
|--------|:-------------------:|:------------------:|
| Pipeline to use | `make.py run` | `gen_audio.py` + `gen_video.py` direct |
| Image count | 1 per 5-10s (6-36 images) | 1 per 10-20s (30-100 images) |
| TTS batch | 1-2 segments | 10-30 segments (Resona batch) |
| Render | FFmpeg segment concat | FFmpeg concat demuxer |
| Intro/outro | Optional | Recommended (brand) |
