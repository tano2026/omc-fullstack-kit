# SRT Timing từ Voiceover Segments — Workflow

Khi cần burn subtitle cố định (hardcode) vào video, dùng SRT thay ASS:

## 1. Lấy duration thật từ từng segment

Dùng ffprobe trên từng file MP3 segment (không ước lượng từ text length):

```bash
for f in dist_v2/seg-*.mp3; do
  name=$(basename "$f" .mp3)
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "$name: $dur"
done
```

## 2. Tính cumulative timing

Groups với gap 3s giữa các section (HOOK, BỐI CẢNH, TỬ VI, TÂM LÝ, GIẢI PHÁP, CLIFFHANGER):

```python
groups = [('HOOK', [2,3]), ('BOI_CANH', [4,5,6]), ...]
current = 0.0
for gname, seg_ids in groups:
    for sid in seg_ids:
        start, end = current, current + durations[sid]
        timestamps[sid] = (start, end)
        current = end
    current += 3.0  # gap
```

## 3. Làm sạch text

```python
text = text.replace("**", "").replace("—", " - ")
text = text.replace('\\"', "'").replace("\\n", " ")
text = re.sub(r'\s+', ' ', text).strip()
```

## 4. Format SRT

```python
def fmt_srt(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# Output:
# 1
# 00:00:00,000 --> 00:00:49,733
# Text content...
```

## 5. Render với FFmpeg

```bash
ffmpeg -i base.mp4 -i voiceover.mp3 \
  -map 0:v -map 1:a \
  -vf "subtitles=subtitles.srt" \
  -c:v libx264 -preset ultrafast -crf 28 \
  -c:a aac -b:a 128k -shortest output.mp4
```

Không thêm BGM trừ khi user yêu cầu.
