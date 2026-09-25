#!/usr/bin/env python3
"""Generate YouTube thumbnail for a GMSP episode.

Usage:
    python scripts/gen_thumbnail.py --episode-dir ... --episode-num 02 \
        --title "BÍ MẬT GIỚI TINH HOA" --hook "Tại sao làm 12h vẫn nghèo?" \
        --accent-rgb "26,107,60"

Produces thumb_epXX.png in the episode root.
"""

import argparse, os, textwrap
from PIL import Image, ImageDraw, ImageFont

def gen_thumbnail(episode_dir, episode_num, title, hook, subtitle, accent_rgb):
    assets = os.path.join(episode_dir, "hyperframes", "assets")
    logo_path = os.path.join(assets, "logo_v2.jpeg")
    bg_path = os.path.join(assets, "bg_02.png")
    
    r, g, b = [int(x) for x in accent_rgb.split(",")]
    
    img = Image.new('RGB', (1280, 720), (13, 13, 18))
    draw = ImageDraw.Draw(img)
    
    # Background
    if os.path.exists(bg_path):
        try:
            bg = Image.open(bg_path).convert("RGB").resize((1280, 720))
            img.paste(bg, (0, 0))
        except:
            pass
    
    # Dark overlays
    for y in range(400, 720):
        alpha = int(200 * (1 - (y - 400) / 320))
        draw.rectangle([(0, y), (1280, y+1)], fill=(13, 13, 18, alpha))
    for y in range(0, 200):
        alpha = int(100 * (1 - y / 200))
        draw.rectangle([(0, y), (1280, y+1)], fill=(13, 13, 18, alpha))
    
    # Accent bar bottom
    draw.rectangle([(0, 660), (1280, 720)], fill=(r, g, b, 220))
    
    # Fonts
    try:
        font_num = ImageFont.truetype("C:/Windows/Fonts/PLAYBILL.TTF", 32)
        font_title = ImageFont.truetype("C:/Windows/Fonts/PLAYBILL.TTF", 64)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
        font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    except:
        font_num = font_title = font_sub = font_small = ImageFont.load_default()
    
    draw.text((640, 140), f"TẬP {episode_num}", fill=(r, g, b, 220), font=font_num, anchor="mm")
    
    # Title (split by space into 2 lines if needed)
    words = title.split()
    if len(words) > 4:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
    else:
        line1 = words[0] if words else ""
        line2 = " ".join(words[1:]) if len(words) > 1 else ""
    
    y_pos = 250
    if line1:
        draw.text((640, y_pos), line1, fill=(255, 255, 255, 255), font=font_title, anchor="mm")
        y_pos += 80
    if line2:
        draw.text((640, y_pos), line2, fill=(255, 215, 0, 255), font=font_title, anchor="mm")
    
    # Hook subtitle
    if hook:
        draw.text((640, y_pos + 80), hook, fill=(200, 200, 200, 200), font=font_sub, anchor="mm")
    
    # Gold separator
    draw.rectangle([(540, y_pos + 120), (740, y_pos + 123)], fill=(255, 215, 0, 200))
    
    # Tagline
    if subtitle:
        draw.text((640, y_pos + 160), subtitle, fill=(180, 180, 180, 180), font=font_small, anchor="mm")
    
    draw.text((640, 690), "GIẢI MÃ SỐ PHẬN", fill=(255, 215, 0, 220), font=font_sub, anchor="mm")
    
    # Logo corner
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA").resize((80, 80))
        mask = Image.new('L', (80, 80), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 80, 80), fill=255)
        logo.putalpha(mask)
        img.paste(logo, (30, 30), logo)
    
    out = os.path.join(episode_dir, f"thumb_ep{episode_num}.png")
    img.save(out)
    print(f"Thumbnail: {out}")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode-dir", required=True)
    parser.add_argument("--episode-num", required=True)
    parser.add_argument("--title", required=True, help="Main title text")
    parser.add_argument("--hook", default="", help="Hook line below title")
    parser.add_argument("--subtitle", default="", help="Tagline at bottom")
    parser.add_argument("--accent-rgb", default="255,215,0")
    args = parser.parse_args()
    
    gen_thumbnail(args.episode_dir, args.episode_num, args.title,
                  args.hook, args.subtitle, args.accent_rgb)
