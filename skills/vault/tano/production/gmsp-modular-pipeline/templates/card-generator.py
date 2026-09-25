#!/usr/bin/env python3
"""GMSP — Card Generator: Vertical (TikTok) + Horizontal (YouTube) + Thumbnail + HTML"""
from PIL import Image, ImageDraw, ImageFont
import os, math, argparse, sys

DOMAIN_COLORS = {
    "TỬ VI": "#FFD700",
    "PHÁT TRIỂN BẢN THÂN": "#1a6b3c",
    "BÍ KÍP CỔ KIM": "#8B6914",
    "GIẢI MÃ SỐ PHẬN": "#BF953F",
}

def hexc(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))

def gradient_bg(w, h, cx_ratio=0.5, cy_ratio=0.4):
    img = Image.new('RGB', (w, h))
    pix = img.load()
    stops = [(0, hexc('#0A0E1A')), (0.4, hexc('#0D0D12')), (1, hexc('#060608'))]
    cx, cy = w*cx_ratio, h*cy_ratio
    max_r = max(w, h) * 0.8
    for y in range(h):
        for x in range(w):
            d = math.sqrt((x-cx)**2 + (y-cy)**2) / max_r
            d = min(1, d)
            for i in range(len(stops)-1):
                if stops[i][0] <= d <= stops[i+1][0]:
                    t = (d-stops[i][0])/(stops[i+1][0]-stops[i][0])
                    c = tuple(int(stops[i][1][j]*(1-t)+stops[i+1][1][j]*t) for j in range(3))
                    pix[x,y] = c
                    break
    return img

def vignette(img, strength=0.5):
    w,h = img.size
    cx,cy = w/2,h/2
    overlay = Image.new('RGBA', (w,h), (0,0,0,0))
    pix = overlay.load()
    for y in range(h):
        for x in range(w):
            d = math.sqrt((x-cx)**2 + (y-cy)**2) / (w*0.35)
            if d > 1:
                a = min(200, int((d-1)*strength*200))
                if a > 0: pix[x,y] = (0,0,0,a)
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def load_fonts(sizes):
    """sizes: dict with keys heading, body, mont_b, mont_sb, mont_eb"""
    try:
        return {
            'heading': ImageFont.truetype("C:/Windows/Fonts/PlayfairDisplay-Bold.ttf", sizes['heading']),
            'body': ImageFont.truetype("C:/Windows/Fonts/PlayfairDisplay-Regular.ttf", sizes['body']),
            'mont_b': ImageFont.truetype("C:/Windows/Fonts/Montserrat-Bold.ttf", sizes['mont_b']),
            'mont_sb': ImageFont.truetype("C:/Windows/Fonts/Montserrat-SemiBold.ttf", sizes['mont_sb']),
            'mont_eb': ImageFont.truetype("C:/Windows/Fonts/Montserrat-ExtraBold.ttf", sizes['mont_eb']),
        }
    except:
        f = ImageFont.load_default()
        return {'heading': f, 'body': f, 'mont_b': f, 'mont_sb': f, 'mont_eb': f}

def gold_accent_line(draw, w):
    for x in range(w):
        for y in range(3):
            draw.point((x,y), hexc(['#BF953F','#FFD700','#BF953F'][y]))

def gold_rings(draw, w, h, cx=None, cy=None):
    import math as m
    cx, cy = cx or w/2, cy or h*0.35
    for r in [int(min(w,h)*0.35), int(min(w,h)*0.28)]:
        for a in range(0, 360, 3):
            rad = m.radians(a)
            draw.point((int(cx+r*m.cos(rad)), int(cy+r*m.sin(rad))), (255,215,0,12 if r>200 else 8))

def make_title_card(ep, title_lines, subtitle, domain, out_dir, size='vertical'):
    VERT = (1080, 1920) if size == 'vertical' else (1920, 1080)
    W, H = VERT
    c_ratio = 0.5 if size == 'vertical' else 0.5
    r_ratio = 0.4 if size == 'vertical' else 0.45
    color = DOMAIN_COLORS.get(domain, '#BF953F')
    img = vignette(gradient_bg(W, H, c_ratio, r_ratio))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    f_size = {'heading': 90, 'body': 50, 'mont_b': 20, 'mont_sb': 16, 'mont_eb': 14}
    if size == 'horizontal':
        f_size = {'heading': 100, 'body': 55, 'mont_b': 22, 'mont_sb': 18, 'mont_eb': 16}
    f = load_fonts(f_size)

    gold_accent_line(draw, W)
    gold_rings(draw, W, H)

    # Episode
    bb = draw.textbbox((0,0), ep, font=f['mont_eb'])
    ey = 350 if size == 'vertical' else 150
    draw.text(((W-(bb[2]-bb[0]))//2, ey), ep, fill='#9A9488', font=f['mont_eb'])

    # Domain badge
    bb = draw.textbbox((0,0), domain, font=f['mont_sb'])
    tw = bb[2]-bb[0]
    by = 410 if size == 'vertical' else 200
    bx = (W-tw-40)//2
    draw.rounded_rectangle((bx-16, by-6, bx+tw+16, by+28), radius=4, outline=color, width=1)
    draw.text((bx, by), domain, fill=color, font=f['mont_sb'])

    # Title
    y = 560 if size == 'vertical' else 320
    step = 110 if size == 'vertical' else 130
    for txt, col in [(title_lines[0] if len(title_lines)>0 else '','#F2EFE6'),
                      (title_lines[1] if len(title_lines)>1 else '','#FFD700'),
                      (title_lines[2] if len(title_lines)>2 else '','#F2EFE6')]:
        if not txt: continue
        bb = draw.textbbox((0,0), txt, font=f['heading'])
        draw.text(((W-(bb[2]-bb[0]))//2, y), txt, fill=col, font=f['heading'])
        y += step

    # Subtitle
    bb = draw.textbbox((0,0), subtitle, font=f['body'])
    draw.text(((W-(bb[2]-bb[0]))//2, y+60), subtitle, fill='#9A9488', font=f['body'])

    # Bottom
    items = ["GIẢI MÃ SỐ PHẬN", "●", "@giaimasophan"]
    tws = [draw.textbbox((0,0),it,font=f['mont_eb'])[2]-draw.textbbox((0,0),it,font=f['mont_eb'])[0] for it in items]
    gap = 40
    x = (W-(sum(tws)+gap*2))//2
    by2 = H-100 if size == 'vertical' else H-60
    for i, item in enumerate(items):
        draw.text((x, by2), item, fill='#2A2A30', font=f['mont_eb'])
        x += tws[i] + gap

    suffix = "_h" if size == 'horizontal' else "_v2"
    path = os.path.join(out_dir, f"title_card{suffix}.png")
    img.save(path)
    return path

def make_quote_card(ep, quote_lines, attribution, out_dir, size='vertical'):
    VERT = (1080, 1920) if size == 'vertical' else (1920, 1080)
    W, H = VERT
    img = vignette(gradient_bg(W, H, 0.5, 0.35 if size == 'vertical' else 0.4))
    draw = ImageDraw.Draw(img, 'RGBA')

    f_size = {'heading': 90, 'body': 50, 'mont_b': 20, 'mont_sb': 16, 'mont_eb': 14}
    if size == 'horizontal':
        f_size = {'heading': 90, 'body': 55, 'mont_b': 22, 'mont_sb': 18, 'mont_eb': 16}
    f = load_fonts(f_size)

    gold_rings(draw, W, H)

    # Badge
    bb = draw.textbbox((0,0), "GIẢI MÃ SỐ PHẬN", font=f['mont_sb'])
    tw = bb[2]-bb[0]
    bx = (W-tw-40)//2
    by = 350 if size == 'vertical' else 180
    draw.rounded_rectangle((bx-16, by-6, bx+tw+16, by+24), radius=3, outline='#BF953F', width=1)
    draw.text((bx, by), "GIẢI MÃ SỐ PHẬN", fill='#BF953F', font=f['mont_sb'])

    # Quote mark
    q = '"'
    bb = draw.textbbox((0,0), q, font=f['heading'])
    qy = 460 if size == 'vertical' else 260
    draw.text(((W-(bb[2]-bb[0]))//2, qy), q, fill='#FFD700', font=f['heading'])

    try:
        f_i = ImageFont.truetype("C:/Windows/Fonts/PlayfairDisplay-Italic.ttf", f_size['body'])
    except:
        f_i = f['body']

    y = 580 if size == 'vertical' else 370
    step = 80 if size == 'vertical' else 90
    for line in quote_lines:
        if not line: continue
        bb = draw.textbbox((0,0), line, font=f_i)
        draw.text(((W-(bb[2]-bb[0]))//2, y), line, fill='#F2EFE6', font=f_i)
        y += step

    bb = draw.textbbox((0,0), attribution, font=f['mont_b'])
    draw.text(((W-(bb[2]-bb[0]))//2, y+70), attribution, fill='#9A9488', font=f['mont_b'])

    suffix = "_h" if size == 'horizontal' else "_v2"
    path = os.path.join(out_dir, f"quote_card{suffix}.png")
    img.save(path)
    return path

def make_thumbnail(ep, domain, hook, subtitle, out_dir):
    W, H = 1280, 720
    color = DOMAIN_COLORS.get(domain, '#BF953F')
    img = vignette(gradient_bg(W, H, 0.7, 0.5))
    draw = ImageDraw.Draw(img, 'RGBA')
    f = load_fonts({'heading': 72, 'body': 36, 'mont_b': 18, 'mont_sb': 14, 'mont_eb': 12})

    # Bottom gold line
    for yy in range(H-6, H-3):
        for x in range(W):
            t = abs(x-W/2)/(W/2)
            draw.point((x,yy), (int(255*(1-t)+191*t), int(215*(1-t)+149*t), int(0*(1-t)+63*t)))

    # Domain badge top-right
    bb = draw.textbbox((0,0), domain, font=f['mont_sb'])
    tw = bb[2]-bb[0]
    px, py = W-tw-30, 20
    draw.rounded_rectangle((px-10, py-4, px+tw+10, py+24), radius=3, fill=color)
    draw.text((px, py), domain, fill='#FFFFFF', font=f['mont_sb'])

    # Hook
    bb = draw.textbbox((0,0), hook, font=f['heading'])
    draw.text((40, 200), hook, fill='#FFD700', font=f['heading'])

    # Subtitle
    bb = draw.textbbox((0,0), subtitle, font=f['body'])
    draw.text((40, 280), subtitle, fill='#FFFFFF', font=f['body'])

    # Episode
    bb = draw.textbbox((0,0), ep, font=f['mont_b'])
    draw.text((40, 380), ep, fill='#9A9488', font=f['mont_b'])

    # Red accent left
    for yy in range(180, 450, 2):
        draw.point((25, yy), hexc('#8B0000'))

    path = os.path.join(out_dir, "thumbnail_sample_v2.png")
    img.save(path)
    return path

def make_html_title(ep, title_lines, subtitle, domain, out_dir, size='vertical'):
    """Generate HTML template for title card"""
    W = "1080" if size == "vertical" else "1920"
    H = "1920" if size == "vertical" else "1080"
    fs_title = "72px" if size == "vertical" else "100px"
    fs_sub = "48px" if size == "vertical" else "55px"
    domain_low = domain.lower().replace(" ", "-")
    
    html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Montserrat:wght@600;700;900&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ width: {W}px; height: {H}px; background: #0D0D12; font-family: 'Playfair Display', serif; position: relative; overflow: hidden; }}
  .bg {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 40%, #0A0E1A 0%, #0D0D12 50%, #060608 100%); }}
  .vignette {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.7) 100%); }}
  .accent {{ position: absolute; left: 20px; top: 80px; bottom: 80px; width: 3px;
    background: linear-gradient(180deg, transparent, #8B0000 30%, #8B0000 70%, transparent); }}
  .ep-label {{ position: absolute; top: {350 if size=="vertical" else 150}px; width: 100%; text-align: center;
    font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 14px; color: rgba(242,239,230,0.4); letter-spacing: 6px; text-transform: uppercase; }}
  .badge {{ position: absolute; top: {410 if size=="vertical" else 200}px; width: 100%; text-align: center; }}
  .badge span {{ display: inline-block; padding: 4px 26px; border: 1px solid {color}; border-radius: 4px;
    font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 16px; color: {color}; letter-spacing: 3px; }}
  .content {{ position: absolute; top: {560 if size=="vertical" else 320}px; width: 100%; text-align: center; z-index: 10; }}
  .title-line {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: {fs_title}; line-height: 1.3; }}
  .gold {{ background: linear-gradient(135deg, #BF953F, #FFD700, #BF953F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
  .subtitle {{ font-family: 'Playfair Display', serif; font-weight: 400; font-size: {fs_sub}; color: rgba(242,239,230,0.6); margin-top: 40px; }}
  .footer {{ position: absolute; bottom: {100 if size=="vertical" else 60}px; width: 100%; text-align: center;
    font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 14px; color: rgba(42,42,48,0.6); letter-spacing: 3px; }}
  .glow {{ position: absolute; top: {30 if size=="vertical" else 18}%; left: 50%; width: 60%; height: 50%; transform: translate(-50%,-50%);
    background: radial-gradient(ellipse, rgba(255,215,0,0.03) 0%, transparent 70%); }}
  .bottom-line {{ position: absolute; bottom: 4px; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent 10%, #BF953F 30%, #FFD700 50%, #BF953F 70%, transparent 90%); }}
</style>
</head>
<body>
  <div class="bg"></div>
  <div class="vignette"></div>
  <div class="bottom-line"></div>
  <div class="glow"></div>
  <div class="accent"></div>
  <div class="ep-label">{ep}</div>
  <div class="badge"><span>{domain}</span></div>
  <div class="content">
    <div class="title-line" style="color:#F2EFE6">{title_lines[0]}</div>
    <div class="title-line gold">{title_lines[1]}</div>
    <div class="title-line" style="color:#F2EFE6">{title_lines[2]}</div>
    <div class="subtitle">{subtitle}</div>
  </div>
  <div class="footer">GIẢI MÃ SỐ PHẬN &nbsp;●&nbsp; @giaimasophan</div>
</body>
</html>'''
    suffix = "_h" if size == 'horizontal' else "_v2"
    path = os.path.join(out_dir, f"title_card{suffix}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path

def make_html_thumbnail(ep, domain, hook, subtitle, out_dir):
    color = DOMAIN_COLORS.get(domain, '#BF953F')
    html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Montserrat:wght@600;700;900&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ width: 1280px; height: 720px; background: #0D0D12; position: relative; overflow: hidden; }}
  .bg {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 60% 50%, #0A0E1A 0%, #0D0D12 50%, #060608 100%); }}
  .vignette {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.7) 100%); }}
  .grid {{ position: absolute; inset: 0; opacity: 0.03; background-image: linear-gradient(rgba(255,215,0,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(255,215,0,0.3) 1px, transparent 1px); background-size: 60px 60px; }}
  .accent-bar {{ position: absolute; left: 20px; top: 80px; bottom: 80px; width: 3px;
    background: linear-gradient(180deg, transparent, #8B0000 30%, #8B0000 70%, transparent); }}
  .badge {{ position: absolute; top: 20px; right: 30px; padding: 8px 20px; background: {color}; color: #fff;
    font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 16px; letter-spacing: 3px; border-radius: 3px; }}
  .content {{ position: relative; z-index: 10; padding-left: 60px; max-width: 800px; top: 160px; }}
  .ep-label {{ font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 14px; color: rgba(242,239,230,0.4); letter-spacing: 6px; text-transform: uppercase; margin-bottom: 15px; }}
  .hook {{ font-family: 'Playfair Display', serif; font-weight: 900; font-size: 72px; color: #FFD700; line-height: 1.2; margin-bottom: 10px; }}
  .subtitle {{ font-family: 'Playfair Display', serif; font-weight: 700; font-size: 48px; color: #F2EFE6; }}
  .subtitle .gold {{ background: linear-gradient(135deg, #BF953F, #FFD700, #BF953F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
  .bottom-line {{ position: absolute; bottom: 4px; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent 10%, #BF953F 30%, #FFD700 50%, #BF953F 70%, transparent 90%); }}
</style>
</head>
<body>
  <div class="bg"></div>
  <div class="grid"></div>
  <div class="vignette"></div>
  <div class="bottom-line"></div>
  <div class="accent-bar"></div>
  <div class="badge">{domain}</div>
  <div class="content">
    <div class="ep-label">{ep}</div>
    <div class="hook">{hook}</div>
    <div class="subtitle">{subtitle}</div>
  </div>
</body>
</html>'''
    path = os.path.join(out_dir, "thumbnail_v2.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GMSP Card Generator — all formats')
    parser.add_argument('--ep', default='TẬP 15')
    parser.add_argument('--title', nargs='+', default=['30-40 Tuổi', 'Giai Đoạn Điên Rồ', 'Của Cuộc Đời'],
                        help='3 title lines (2nd line gets gold gradient)')
    parser.add_argument('--sub', default='Thức tỉnh hay lụi tàn?')
    parser.add_argument('--domain', default='PHÁT TRIỂN BẢN THÂN')
    parser.add_argument('--hook', default='30-40 TUỔI:',
                        help='Thumbnail hook text (large, gold)')
    parser.add_argument('--thumb-sub', default='GIAI ĐOẠN ĐIÊN RỒ',
                        help='Thumbnail subtitle (white)')
    parser.add_argument('--out', default='./cards',
                        help='Output base directory')
    args = parser.parse_args()

    # Create output directories
    dirs = {}
    for sub in ['vertical', 'horizontal', 'thumbnail', 'html']:
        d = os.path.join(args.out, sub)
        os.makedirs(d, exist_ok=True)
        dirs[sub] = d

    # Generate ALL formats
    t_v = make_title_card(args.ep, args.title, args.sub, args.domain, dirs['vertical'], 'vertical')
    t_h = make_title_card(args.ep, args.title, args.sub, args.domain, dirs['horizontal'], 'horizontal')
    thumb = make_thumbnail(args.ep, args.domain, args.hook, args.thumb_sub, dirs['thumbnail'])
    ht_v = make_html_title(args.ep, args.title, args.sub, args.domain, dirs['html'], 'vertical')
    ht_h = make_html_title(args.ep, args.title, args.sub, args.domain, dirs['html'], 'horizontal')
    ht_thumb = make_html_thumbnail(args.ep, args.domain, args.hook, args.thumb_sub, dirs['html'])

    print(f"✅ Generated 6 files:")
    print(f"   {t_v}")
    print(f"   {t_h}")
    print(f"   {thumb}")
    print(f"   {ht_v}")
    print(f"   {ht_h}")
    print(f"   {ht_thumb}")
