# Video Content Pipeline — Session-Specific Detail

> Absorbed from `video-content-pipeline` (Jul 2026)

## Unique Technical Detail Not Covered in Umbrella Summary

### Quality Loop Architecture
The content pipeline uses 6 checkpoints with a `ProgressTracker` class:

```python
class ProgressTracker:
    def __init__(self, total: int = 6):
        self.checkpoints = [False] * total

    def mark_done(self, idx: int):
        self.checkpoints[idx] = True

    def resume_from(self) -> int:
        for i, done in enumerate(self.checkpoints):
            if not done:
                return i
        return len(self.checkpoints)
```

**Checkpoints:**
1. Topic validated
2. Research complete
3. Script written
4. Script expanded for target duration
5. Image prompts generated
6. All images generated

### Retry with Context Pattern
When a checkpoint fails (e.g., image generation produces bad output):
```python
if failed:
    # Don't reset — give the agent the current state
    context = f"Checkpoint {idx} failed. Current state: {state}. Error: {error}"
    # Delegate retry with full context for informed recovery
```

### Delegate-to-Subagent for Complex Failures
For quality failures that need manual-style intervention (wrong audio length, bad image style), delegate to a focused subagent with the full project context rather than retrying in the same agent loop. This isolates the complex logic and avoids context pollution.

### Script Expansion Pattern
Expanding a 7-minute source script to 15-min target:
```python
expansion_factor = target_dur / source_dur  # ~2.14x
```
Techniques used:
- Add audience reflection pauses: "Hãy dừng lại một chút và nghĩ về điều này..."
- Insert illustrative analogies that connect the concept to daily life
- Add "Có một câu chuyện..." narrative interludes
- Deepen analysis of each numbered point

### Competitor Research and Content Adaptation
- Research competitor videos on similar topics
- Extract hook patterns, structure templates, and audience engagement techniques
- Adapt successful frameworks (Brutal Truth + Empowerment) without copying content
- Store research in `references/content-adaptation-research.md`

### Domain Pack Structure
```
episodes/<pack>/
├── tl-01-<topic>/
│   ├── track.json       # Frame tracking (29 frames = ~20 min)
│   ├── script.json      # Narration + visual prompts per frame
│   ├── subs.srt         # Generated subtitles
│   ├── voiceover.mp3    # TTS audio
│   ├── images/          # Frame images
│   └── final.mp4        # Rendered video
├── tl-02-<topic>/
└── ...
```

### Image Strategy for Limited Images
When using fewer images than frames (e.g., 5 images for 29 frames across ~20 min):
- Front-load images: first images get more frames (hook needs visual variety)
- Detect scene transitions from narration content — switch image at natural breaks
- For "talking-head" segments, use a static image with subtle subtitle motion
- Ensure image-to-narration alignment at the section level, not per-frame
