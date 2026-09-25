# Image-to-Frame Mapping

`gen_video.py` maps script images to frame segments by `frame_id`. Understanding this mapping is critical to getting the right number of rendered frames.

## Indexing Mismatch (1-based vs 0-based)

| System | Indexing | First item |
|--------|----------|------------|
| `images/scene_*.png` files | 0-based | `scene_01.png` → `images[0]` |
| `track.json` `frame_id` | **1-based** | First frame has `frame_id: 1` (NOT 0) |

**Consequence:** `frame_id=1` maps to `images[1]` → `scene_04.png` (the second image), NOT `scene_01.png` (images[0]). `scene_01.png` is NEVER used by any frame.

## Render Threshold

Only frames where `frame_id < len(images)` are rendered:

```python
# In gen_video.py:
[f for f in track if f['frame_id'] < len(img_files)]
```

**Example:** 6 images → max valid `frame_id` = 5. If track has 29 frames with `frame_id` 1–29, only frames 1–5 render (5 out of 29).

## Practical Rule

Generate at least 1 image per ~3-5 frames for full coverage. For a 29-frame episode:
- 6 images → only 5 frames render (~3.5 min video)
- 29 images → full episode renders (~20 min video)

## Debug

If fewer frames render than expected, check:

```python
# Count available vs needed
avail = len(img_files)
needed = max(f['frame_id'] for f in track)
print(f"Images: {avail}, Max frame_id needed: {needed}")
missing = [f['frame_id'] for f in track if f['frame_id'] >= avail]
print(f"Frames skipped due to missing images: {len(missing)}")
```
