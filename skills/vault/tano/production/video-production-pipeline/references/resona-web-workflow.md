# Resona Web Workflow — Manual TTS with Pitch Variation

When automated Resona API fails (DNS resolution errors, credit exhausted, network issues), fall back to:

## Workflow

1. **Prepare cleaned text** — strip `**`, `"`, `—`, metadata, section headers
2. **Split into 8 sections** matching script structure: Hook, Context, Tử Vi, Psychology, CTA, Solution 1/2/3, Cliffhanger+End
3. **Write to .txt file** with section-commented instructions (speed + pitch recommendations per section)
4. **User pastes** each section into Resona web (resona.live), voice=Trung Thành, adjusts speed/pitch
5. **User sends** the 8 MP3 files back via Telegram/Downloads
6. **Copy** to working dir:
   ```bash
   cp "/c/Users/*/Downloads/Khúc*.mp3" tts/resona_final/{01_hook,02_boicanh,...}.mp3
   ```
7. **Generate 3s silence**: `ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 3 tts/resona_final/silence.mp3`
8. **Build concat list** with silence between sections (7 gaps, NOT 8):
   ```
   file '01_hook.mp3'
   file 'silence.mp3'
   file '02_boicanh.mp3'
   ...
   ```
9. **Concat**: `ffmpeg -f concat -safe 0 -i concat.txt -c copy voiceover.mp3`

## Pitch Variation Table (GMSP Tested)

| Section | Speed | Pitch | Effect |
|---------|-------|-------|--------|
| HOOK | 0.90 | 1.0 | Normal, authoritative |
| Câu chuyện Tuấn | 0.86 | 0.90 | Low, serious |
| Câu chuyện Hà | 0.86 | 0.85 | Lower, regretful |
| Tử Vi mở | 0.88 | 0.95 | Mysterious |
| Tử Vi cao trào | 0.90 | 1.05 | Revelation |
| Tâm lý Social Clock | 0.88 | 1.0 | Normal |
| Sunk Cost + Parkinson | 0.90 | 1.05 | Urgent |
| 3 cái bẫy (climax) | 0.92 | 1.10 | Highest energy |
| CTA | 0.90 | 1.05 | Energized |
| Giải pháp 1+3 | 0.90 | 1.05 | Motivational |
| Giải pháp 2 | 0.88 | 1.0 | Normal |
| Cliffhanger | 0.86 | 0.90 | Low, ominous |
| End | 0.90 | 1.0 | Normal |

Note: Speed 0.9 on Resona compresses ~8800 chars into ~7:45 min. For 10-11 min, use 0.82.

## Text Cleaning Rules

Remove before pasting into Resona:
- `**bold**` → plain text
- `"quotes"` → `'quotes'` (straight single quotes)
- `—` em dash → ` - ` space dash space
- `–` en dash → `-`
- `\n` inside paragraphs → single space
- `[SECTION HEADERS]` → remove entirely
- `###` markdown headers → remove
- `---` separators → remove
- Metadata lines (`Series:`, `Thời lượng:`, etc.) → remove

## Pitfalls

- **Speed 0.9 gives ~7:45 for 8800 chars** — shorter than script estimate. User may need to know this and decide if they want slower speed (0.82) for 10-11 min target
- **Resona web per-section limit is ~5000 chars** — 8 sections each under that is safe
- **Files from Downloads may need rename** — Vietnamese filenames with spaces cause shell issues
- **Always produce a clean text file** with the content separated by section headers for easy copy-paste
