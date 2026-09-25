# GMSP Resona Concat Workflow

## Khi nào dùng
User paste Resona web TTS cho EP → có nhiều candidate files mỗi phần.

## Các bước

### 1. Liệt kê file
```bash
ls -la Resona/*.mp3 | sort
```

### 2. Xác định thứ tự
Mỗi phần có N candidate. User yêu cầu: GHÉP TẤT CẢ, ko chọn 1.

### 3. Tạo gap file
```bash
ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t 3 gap3s.mp3
```

### 4. Build concat list
File text với:
```
file 'PHẦN 1 — HOOK - 1.mp3'
file 'PHẦN 1 — HOOK - 2.mp3'
file 'gap3s.mp3'
file 'PHẦN 2 — BỐI CẢNH - 1.mp3'
...
```
- Gap CHỈ giữa các phần (section boundaries), KO giữa segment cùng phần
- Gap = 3s (user chốt — 6s là quá dài)

### 5. Concat
```bash
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy output.mp3
```
Dùng `-c copy` (copy stream, ko re-encode)

### 6. Kiểm tra
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 output.mp3
```

## File naming
Output: epXX_resona_full.mp3 (copy ra D:\epXX_resona_full.mp3)

## Timing recalculation
Sau khi có concat MP3 mới, phải recalculate chapter overlay timings cho video.
Dùng `ffprobe` để lấy duration từng segment, accumulate để tìm chapter positions.
