"""Generate chapter transition images for GMSP video production.
Creates 1920x1080 RGBA PNG overlays with dark background + gold text.
Each chapter = 6s gap: fade in 0.5s, hold 5s, fade out 0.5s.

Usage: python gen_chapters.py
Output: chapter_1.png through chapter_N.png in the current dir.

Modify the `chapters` array for each episode's section titles."""

from PIL import Image, ImageDraw, ImageFont
import os

chapters = [
    ("I", "Nỗi Sợ Thầm Kín", '"Không ai chuẩn bị cho bạn"'),
    ("II", "Bối Cảnh", '"Tuấn, Hà và chiếc lồng vàng"'),
    ("III", "Tử Vi Giải Mã", '"Mệnh Vô Chính Diệu"'),
    ("IV", "Ba Cái Bẫy", '"Social Clock, Sunk Cost, Parkinson"'),
    ("V", "Giải Pháp 1", '"Giết cái đồng hồ xã hội"'),
    ("VI", "Giải Pháp 2", '"Định nghĩa lại An Toàn"'),
    ("VII", "Giải Pháp 3", '"Chấp nhận mất mát"'),
]

FONT_LARGE = None
FONT_MED = None
FONT_SMALL = None

for fp in [
    "C:/Windows/Fonts/playfairdisplay.ttf",
    "C:/Windows/Fonts/georgia.ttf",
    "C:/Windows/Fonts/tahoma.ttf",
]:
    if os.path.exists(fp):
        FONT_LARGE = ImageFont.truetype(fp, 52)
        FONT_MED = ImageFont.truetype(fp, 24)
        FONT_SMALL = ImageFont.truetype(fp, 22)
        break

if not FONT_LARGE:
    FONT_LARGE = ImageFont.load_default()
    FONT_MED = FONT_LARGE
    FONT_SMALL = FONT_LARGE


def draw_centered_text(draw, text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((1920 - tw) // 2, y), text, fill=color, font=font)


for idx, (num, title, sub) in enumerate(chapters):
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 200))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # PHẦN I (muted gold)
    draw_centered_text(draw, f"PHẦN {num}", 340, FONT_SMALL, (255, 215, 0, 120))

    # Gold line
    draw.rectangle((860, 390, 1060, 393), fill=(255, 215, 0, 180))

    # Title (bold gold)
    draw_centered_text(draw, title, 420, FONT_LARGE, (255, 215, 0, 230))

    # Subtitle quote
    draw_centered_text(draw, sub, 500, FONT_MED, (200, 200, 200, 160))

    img.save(f"chapter_{idx + 1}.png")
    print(f"  chapter_{idx + 1}.png: saved")

print("Done")
