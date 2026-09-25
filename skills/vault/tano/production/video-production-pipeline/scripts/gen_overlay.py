#!/usr/bin/env python3
"""Generate branding overlay + intro card for a GMSP episode.

Usage:
    python scripts/gen_overlay.py --episode 02 --topic "Bí Mật Giới Tinh Hoa" \
        --accent "#1a6b3c" --accent-rgb "26,107,60" --scene-tag "BÍ MẬT GIỚI TINH HOA"

This produces:
    hyperframes/assets/branding_overlay.png  (4-corner + gradient)
    hyperframes/assets/intro_card.png        (5s intro card)
"""

import argparse, os
from PIL import Image, ImageDraw, ImageFont

def gen_overlay_and_intro(episode_dir, episode_num, topic, scene_tag, accent_hex, accent_rgb):
    assets = os.path.join(episode_dir, "hyperframes", "assets")
    logo_path = os.path.join(assets, "logo_v2.jpeg")
    os.makedirs(assets, exist_ok=True)
    
    r, g, b = [int(x) for x in accent_rgb.split(",")]
    
    # === BRANDING OVERLAY ===
    overlay = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Gradient bottom 20%
    for y in range(864, 1080):
        alpha = int(170 * (1 - (y - 864) / 216))
        draw.rectangle([(0, y), (1920, y+1)], fill=(13, 13, 18, alpha))
    
    # Logo top-right circular 170px
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA").resize((170, 170))
        mask = Image.new('L', (170, 170), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 170, 170), fill=255)
        logo.putalpha(mask)
        overlay.paste(logo, (1920-170-30, 30), logo)
    
    # Fonts
    font_tag = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
    font_brand = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    
    # Scene tag top-left
    draw.text((30, 30), scene_tag, fill=(r, g, b, 220), font=font_tag)
    # Brand bottom-left
    draw.text((30, 1080-50), "GIẢI MÃ SỐ PHẬN", fill=(r, g, b, 200), font=font_brand)
    # Subscribe bottom-right
    draw.text((1920-30-130, 1080-50), "ĐĂNG KÝ", fill=(r, g, b, 200), font=font_sub)
    
    overlay_path = os.path.join(assets, "branding_overlay.png")
    overlay.save(overlay_path)
    print(f"  Overlay: {overlay_path}")
    
    # === INTRO CARD ===
    intro = Image.new('RGBA', (1920, 1080), (13, 13, 18, 255))
    intro_draw = ImageDraw.Draw(intro)
    
    if os.path.exists(logo_path):
        logo_big = Image.open(logo_path).convert("RGBA").resize((260, 260))
        mask_big = Image.new('L', (260, 260), 0)
        ImageDraw.Draw(mask_big).ellipse((0, 0, 260, 260), fill=255)
        logo_big.putalpha(mask_big)
        intro.paste(logo_big, (830, 240), logo_big)
    
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/PLAYBILL.TTF", 72)
    except:
        font_title = ImageFont.load_default()
    
    intro_draw.text((960, 540), "GIẢI MÃ SỐ PHẬN", fill=(255, 215, 0, 255), font=font_title, anchor="mm")
    intro_draw.rectangle([(710, 580), (1210, 583)], fill=(255, 215, 0, 220))
    intro_draw.text((960, 620), f"Tập {episode_num}: {topic}", fill=(200, 200, 200, 200), font=font_tag, anchor="mm")
    
    intro_path = os.path.join(assets, "intro_card.png")
    intro.save(intro_path)
    print(f"  Intro:  {intro_path}")
    
    return overlay_path, intro_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode-dir", required=True, help="Episode root dir")
    parser.add_argument("--episode-num", required=True, help="Episode number (02, 03...)")
    parser.add_argument("--topic", required=True, help="Episode topic")
    parser.add_argument("--scene-tag", required=True, help="Scene tag text")
    parser.add_argument("--accent", default="#1a6b3c", help="Accent hex color")
    parser.add_argument("--accent-rgb", default="26,107,60", help="Accent RGB")
    args = parser.parse_args()
    
    gen_overlay_and_intro(
        args.episode_dir, args.episode_num, args.topic,
        args.scene_tag, args.accent, args.accent_rgb
    )
