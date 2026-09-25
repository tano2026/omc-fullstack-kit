# Voiceover Duration Expansion — Mid-Production Re-Roll

## When This Happens

You have a HyperFrames video whose scenes, timing, and figures are already set for one voiceover duration. Then:
- The user changes the TTS voice (e.g., AndrewNeural 59s → GuyNeural 135s)
- Or the script is re-written longer
- Or the TTS speed changes

The existing figures, scene layouts, and timings are now wrong for the new duration.

## What Breaks

| Artifact | Problem | Fix |
|----------|---------|-----|
| `index.html` `data-duration` | Still set to old duration | Update root `data-duration` |
| Per-scene `data-start` / `data-duration` | Sum doesn't match new total | Recalculate proportional timing |
| Scene figures (images) | Generated for shorter cuts, may look sparse or stretched | Regenerate for new per-scene duration |
| Composition HTML layouts | Pure-text scenes feel empty at 2x duration | Add visual columns, secondary images, data viz |

## Timing Recalculation Formula

Given old total duration D_old (e.g., 60s) and new D_new (e.g., 135s):

For each scene with old duration t_i, new duration = t_i × (D_new / D_old)

But human voices don't scale linearly — **the best approach is to listen to the new voiceover and divide by content beats**:

1. Play the new voiceover
2. Identify natural section boundaries (topic shifts)
3. Count the number of major beats = number of scenes (usually same as before)
4. Divide D_new by N_scenes for approximate per-scene slot
5. Adjust boundaries so they land on content breaks

Example from this session:
```
Old: 6 scenes, 60s total = ~10s per scene
New: 6 scenes, 135s total = ~22.5s per scene
Final: S1(0-22s) S2(22-44s) S3(44-64s) S4(64-86s) S5(86-110s) S6(110-135s)
```

## When to Re-Generate Figures

Re-generate figures when:
- **Scene duration doubles or more** — the old figure was designed for a ~10s glance, now needs to hold attention for 22s
- **Scene layout changes** — going from text-only to text+images means new art needed
- **Content emphasis shifts** — what the voiceover says in that scene changed

Don't re-generate when:
- Only timing changed but the figure still fills the scene well
- The figure is a general background illustration, not tied to specific content

## Scene Layout Adaptation

When a scene's duration doubles, the layout should add visual depth:

| Duration | Recommended Layout |
|----------|-------------------|
| ≤10s | Single focal point — text or 1 image |
| 10–20s | Text + 1 image side-by-side |
| 20s+ | Multi-column: counter + 2 images, or text + infographic + data viz |

## Pitfalls

- **Don't keep old figures that were timed for shorter cuts** — they'll look awkward held for 2x duration with nothing happening
- **Animation timing inside each scene must still fit** — GSAP timeline in the composition HTML has its own `duration` values; they don't auto-scale with `data-duration`. If S4 had a 2s count-up animation and now S4 is 22s, add secondary animations (images sliding in, text fading) to fill the extra time
- **Regenerate don't reuse** from the old render — the old assets were sized/cropped for a different scene context
- **Verify audio streams after re-render** — voiceover change means new audio encoding; double-check ffprobe shows both video+audio streams
