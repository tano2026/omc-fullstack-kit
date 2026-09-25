#!/usr/bin/env python3
"""
OMC Viral Short-Form Video Production Engine (TikTok, Reels, Shorts)
Tự động hóa toàn bộ quy trình biên kịch video ngắn 30-60s chuẩn công thức giữ chân người xem (Retention Formula):
1. 3 Biến thể Hook giật ngược tâm lý (0s - 3s)
2. Kịch bản lời thoại (Voiceover Script) tối ưu nhịp điệu
3. B-Roll & Cảnh quay trực quan (Visual Storyboard)
4. AI Prompt tạo hình ảnh/video (Midjourney, Runway, Kling)
5. Chỉ dẫn dựng video CapCut/Premiere (SFX, BGM, Text Overlay, CTA)
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "obsidian-vault"))

from vault_sync import VaultSync

class VideoScriptGenerator:
    def __init__(self):
        self.vault = VaultSync(BASE_DIR / "obsidian-vault")
        self.calendar_dir = BASE_DIR / "obsidian-vault" / "02 - Projects" / "Content-Calendar"
        self.calendar_dir.mkdir(parents=True, exist_ok=True)

    def generate_tiktok_script(self, topic: str, target_audience: str = "Khách hàng đại chúng", duration_sec: int = 45) -> dict:
        """Sinh trọn gói kịch bản video viral cho TikTok/Reels"""
        print("\n" + "=" * 70)
        print(f"🎬 KÍCH HOẠT QUY TRÌNH BIÊN KỊCH VIDEO VIRAL CHO: '{topic}'")
        print(f"⏱️ Thời lượng mục tiêu: {duration_sec}s | Đối tượng: {target_audience}")
        print("=" * 70)

        # 1. Tạo 3 Hooks giật ngược tâm lý
        hooks = [
            f"Đừng dại gì mua {topic} nếu chưa biết 3 sự thật này!",
            f"90% mọi người đang hiểu sai về {topic} — Đây là cách đúng chỉ trong 30 giây.",
            f"Nếu bạn đang gặp rắc rối với {topic}, làm ngay bước này trước khi quá muộn!"
        ]

        # 2. Xây dựng phân cảnh Storyboard
        storyboard = [
            {
                "time": "00:00 - 00:03",
                "phase": "HOOK (Giữ chân 3s đầu)",
                "visual": f"Cận cảnh mặt biểu cảm ngạc nhiên/cảnh báo, cầm điện thoại hoặc hình ảnh đối chiếu về {topic}.",
                "audio": hooks[0],
                "text_overlay": "SỰ THẬT ÍT NGƯỜI BIẾT! ⚠️",
                "sfx": "Âm thanh Whoosh mạnh + Tiếng cảnh báo Beep"
            },
            {
                "time": "00:03 - 00:15",
                "phase": "PROBLEM / DRAMA (Khai thác nỗi đau)",
                "visual": "Chuyển cảnh nhanh (B-Roll): Người dùng loay hoay, mệt mỏi, tốn tiền hoặc mất thời gian khi làm theo cách cũ.",
                "audio": f"Hầu hết mọi người tốn cả đống tiền và thời gian nhưng kết quả nhận lại chỉ là sự thất vọng. Tại sao? Vì bạn đang bỏ qua bước quan trọng nhất.",
                "text_overlay": "CÁCH CŨ = TỐN TIỀN & MỆT MỎI ❌",
                "sfx": "Nhạc nền căng thẳng (Suspense Tension)"
            },
            {
                "time": "00:15 - 00:35",
                "phase": "SOLUTION / SECRET (Bí kíp độc quyền)",
                "visual": "Chuyên gia mỉm cười tự tin, màn hình chia đôi (Before / After) hoặc thao tác trực tiếp giải pháp một cách mượt mà.",
                "audio": f"Bí quyết ở đây là: Thay vì làm thủ công, hãy áp dụng quy trình 3 bước này. Bước 1: Chuẩn hóa dữ liệu. Bước 2: Tự động hóa. Và bước 3: Kiểm soát rủi ro.",
                "text_overlay": "BÍ KÍP 3 BƯỚC ĐỘC QUYỀN 💡",
                "sfx": "Nhạc chuyển nhịp vui tươi, năng lượng cao (Upbeat Energy)"
            },
            {
                "time": "00:35 - 00:45",
                "phase": "CTA (Kêu gọi hành động dứt khoát)",
                "visual": "Chỉ tay xuống góc dưới màn hình / bio, icon hộp thư tin nhắn nhấp nháy.",
                "audio": f"Lưu video này lại để áp dụng ngay. Hoặc nhắn tin trực tiếp cho mình để nhận trọn bộ tài liệu chi tiết miễn phí nhé!",
                "text_overlay": "LƯU LẠI & NHẮN TIN NGAY! 📩",
                "sfx": "Tiếng Ting ding chuông báo kết quả thành công"
            }
        ]

        # 3. AI Visual Prompts cho Midjourney / Runway / Kling
        ai_prompts = [
            f"Hyper-realistic cinematic shot, expressive face explaining {topic}, modern studio background with soft neon lighting, 8k resolution, photorealistic, 9:16 vertical aspect ratio --ar 9:16",
            f"Split screen comparison showing before and after result of {topic}, clean modern minimalist UI aesthetic, high engagement visual, 9:16 --ar 9:16"
        ]

        package = {
            "title": f"Video Viral: {topic}",
            "topic": topic,
            "target_audience": target_audience,
            "duration": f"{duration_sec}s",
            "hooks": hooks,
            "storyboard": storyboard,
            "ai_prompts": ai_prompts,
            "recommended_bgm": "Trending Phonk Beat hoặc Upbeat Tech Minimalist"
        }

        # 4. Ghi nhận vào Obsidian Second Brain
        safe_name = "".join(c for c in topic if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "-")
        md_file = self.calendar_dir / f"TikTok-{safe_name}.md"
        
        md_content = f"""# 🎬 KỊCH BẢN VIDEO VIRAL TIKTOK / REELS: {topic}

- **Chủ đề:** {topic}
- **Thời lượng:** {duration_sec} giây (Chuẩn giữ chân Retention)
- **Đối tượng:** {target_audience}
- **Nhạc nền đề xuất:** Trending Upbeat / Phonk năng lượng cao

---

## 🎣 3 BIẾN THỂ HOOK GIẬT TÍT (0s - 3s)
1. ⚡ **Hook 1 (Tò mò/Cảnh báo):** *"{hooks[0]}"*
2. ⚡ **Hook 2 (Phản trực giác):** *"{hooks[1]}"*
3. ⚡ **Hook 3 (Giải quyết nỗi đau):** *"{hooks[2]}"*

---

## 📋 PHÂN CẢNH CHI TIẾT (STORYBOARD)

| Thời gian | Giai đoạn | Hình ảnh & Diễn xuất (Visual) | Lời thoại (Voiceover) | Chữ trên màn hình | Âm thanh SFX |
| :---: | :--- | :--- | :--- | :--- | :--- |
"""
        for s in storyboard:
            md_content += f"| `{s['time']}` | **{s['phase']}** | {s['visual']} | *\"{s['audio']}\"* | `{s['text_overlay']}` | {s['sfx']} |\n"

        md_content += f"""
---

## 🎨 PROMPTS TẠO HÌNH ẢNH / VIDEO AI (MIDJOURNEY / RUNWAY / KLING)
```text
{ai_prompts[0]}
```
```text
{ai_prompts[1]}
```

---

## ✂️ HƯỚNG DẪN DỰNG CAPCUT / PREMIERE:
1. Cắt bỏ 100% khoảng lặng (Zero silence gap). Tốc độ nói nhanh 1.15x.
2. Thêm phụ đề tự động (Auto-Captions) chữ to màu vàng viền đen ở giữa ngực.
3. Cứ 2–3 giây đổi góc quay hoặc chèn hình ảnh B-roll 1 lần để chống nhàm chán mắt.
"""
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"✅ Đã tạo kịch bản video và lưu vào: {md_file.relative_to(BASE_DIR)}")
        print("\n🎣 3 BIẾN THỂ HOOK HÚT VIEW:")
        for idx, h in enumerate(hooks, 1):
            print(f"   {idx}. {h}")
            
        return package


def generate_short_form_video_script(topic: str, target_audience: str = "Khách hàng mục tiêu", duration_sec: int = 45, tone: str = "chuyên gia gần gũi") -> dict:
    """Wrapper function to generate viral short-form script."""
    gen = VideoScriptGenerator()
    return gen.generate_tiktok_script(topic=topic, target_audience=target_audience, duration_sec=duration_sec)

def main():
    parser = argparse.ArgumentParser(description="OMC Viral Video Script Generator")
    parser.add_argument("--topic", required=True, type=str, help="Chủ đề video (vd: 'Fast Track Sân Bay', 'Trị Mụn Laser')")
    parser.add_argument("--duration", type=int, default=45, help="Thời lượng giây (30, 45, 60)")
    args = parser.parse_args()

    gen = VideoScriptGenerator()
    gen.generate_tiktok_script(args.topic, duration_sec=args.duration)

if __name__ == "__main__":
    main()

