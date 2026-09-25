#!/usr/bin/env python3
"""Generate 7 chapter transition overlay images for GMSP episodes.
Each image = 1920x1080 RGBA PNG with dark overlay + gold text.

Edit the CHAPTERS list below for each episode's chapter titles/subtitles.
Then run: python gen_chapters.py
Output: hyperframes/chapters/chapter_1.png ... chapter_7.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

CHAPTERS = [
    ("I", "Nỗi Sợ Thầm Kín", '"Không ai chuẩn bị cho bạn"'),
    ("II", "Bối Cảnh", '"Tuấn, Hà và chiếc lồng vàng"'),
    ("III", "Tử Vi Giải Mã", '"Mệnh Vô Chính Diệu"'),
    ("IV", "Ba Cái Bẫy", '"Social Clock, Sunk Cost, Parkinson"'),
    ("V", "Giải Pháp 1", '"Giết cái đồng hồ xã hội"'),
    ("VI", "Giải Pháp 2", '"Định nghĩa lại An Toàn"'),
    ("VII", "Giải Pháp 3", '"Chấp nhận mất mát"'),
]

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "hyperframes", "chapters")
os.makedirs(OUT_DIR, exist_ok=True)

# Font lookup — try GMSP fonts first, fall back to system
FONT_PATHS = [
    "C:/Windows/Fonts/PLAYR.ttf",           # Playfair Display
    "C:/Windows/Fonts/playfairdisplay.ttf",
    "C:/Windows/Fonts/georgia.ttf",
    "C:/Windows/Fonts/tahoma.ttf",
]
FONT = None
for fp in FONT_PATHS:
    if os.path.exists(fp):
        FONT = ImageFont.truetype(fp, 50)
        break
FONT_SM = ImageFont.truetype(FONT.path if FONT else None, 26) if FONT else ImageFont.load_default()

for idx, (num, title, sub) in enumerate(CHAPTERS):
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 200))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Draw centered text
    texts = [
        (f"PHẦN {num}", FONT_SM, (255, 215, 0, 120), 340),
        ("─" * 8, FONT_SM, (255, 215, 0, 180), 390),
        (title, FONT or ImageFont.load_default(), (255, 215, 0, 230), 430),
        (sub, FONT_SM, (200, 200, 200, 160), 520),
    ]
    for text, font, color, y in texts:
        bbox = draw.textbbox((0, 0), str(text), font=font)
        tw = bbox[2] - bbox[0]
        draw.text(
            ((1920 - tw) // 2, y),
            str(text),
            fill=color,
            font=font,
        )

    path = os.path.join(OUT_DIR, f"chapter_{idx + 1}.png")
    img.save(path)
    print(f"  chapter_{idx + 1}.png")
