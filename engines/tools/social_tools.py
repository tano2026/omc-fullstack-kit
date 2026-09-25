"""
Social & Video Content Production Tools for OMC Agents.
Used by: social-creator, media-producer, dev-automation.
"""

import os
import sys
from typing import Dict, Any, List, Optional
from .registry import register_tool

# Ensure media engine is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from engines.media.video_script_generator import generate_short_form_video_script


@register_tool(
    name="generate_video_script",
    description="Tạo kịch bản video ngắn (30-60s) chuẩn tỉ lệ giữ chân (retention) cho TikTok, Reels, YouTube Shorts. Bao gồm 3 biến thể Hook (0-3s), phân cảnh Storyboard, prompt AI sinh hình ảnh, lời thoại voiceover và lưu ý dựng CapCut.",
    agent_ids=["social-creator", "media-producer", "openclaw-executor"],
    category="social",
    parameters={
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Chủ đề video (ví dụ: 'Cách chọn kem chống nắng cho da dầu mụn')"},
            "duration_sec": {"type": "integer", "description": "Thời lượng video bằng giây (30, 45, hoặc 60)", "default": 45},
            "tone": {"type": "string", "description": "Giọng điệu (ví dụ: 'chuyên gia hóm hỉnh', 'cảnh báo dứt khoát', 'tâm sự gần gũi')", "default": "chuyên gia gần gũi"},
            "target_audience": {"type": "string", "description": "Đối tượng mục tiêu (ví dụ: 'chị em văn phòng 25-35t', 'gen Z')", "default": "khách hàng mục tiêu"}
        },
        "required": ["topic"]
    }
)
def generate_video_script(
    topic: str,
    duration_sec: int = 45,
    tone: str = "chuyên gia gần gũi",
    target_audience: str = "khách hàng mục tiêu"
) -> Dict[str, Any]:
    """Generates a complete short-form video script with hooks and storyboard."""
    script = generate_short_form_video_script(
        topic=topic,
        duration_sec=duration_sec,
        tone=tone,
        target_audience=target_audience
    )
    return script


@register_tool(
    name="generate_viral_hooks",
    description="Tạo 5 biến thể câu Hook mở đầu (0-3 giây đầu tiên) giật ngón tay cái người xem dừng lướt. Áp dụng 5 đòn bẩy tâm lý: Phủ định (Loss Aversion), Bí mật ngành, Con số thực tế, Nghịch lý phản trực giác, và Câu hỏi đồng cảm nỗi đau.",
    agent_ids=["social-creator", "media-producer", "market-spy"],
    category="social",
    parameters={
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Chủ đề cần tạo câu mở đầu cuốn hút"},
            "audience": {"type": "string", "description": "Đối tượng người xem", "default": "đại chúng"},
            "industry": {"type": "string", "description": "Ngành hàng (làm đẹp, dịch vụ, tài chính, khóa học, bán lẻ...)", "default": "chung"}
        },
        "required": ["topic"]
    }
)
def generate_viral_hooks(
    topic: str,
    audience: str = "đại chúng",
    industry: str = "chung"
) -> Dict[str, Any]:
    """Generates 5 distinct psychological hooks for short-form video & social posts."""
    hooks = [
        {
            "type": "Phủ Định (Loss Aversion - Sợ Mất Mát)",
            "hook_text": f"Dừng ngay việc {topic} lại nếu không muốn lãng phí cả đống tiền mà không được gì!",
            "visual_direction": "Nhân vật giơ tay xua trước ống kính, mắt mở to, nền sau rung nhẹ, nhạc kịch tính đột ngột ngắt.",
            "best_for": "TikTok & Reels (tỷ lệ giữ chân 3s đầu cao nhất)"
        },
        {
            "type": "Bí Mật Trong Ngành (Curated Insider Truth)",
            "hook_text": f"Đây là bí mật về {topic} mà 90% người trong ngành không bao giờ muốn bạn biết...",
            "visual_direction": "Nói thầm sát micro, góc máy cận mặt (macro close-up), động tác tay che nửa miệng đầy vẻ bí ẩn.",
            "best_for": "Tạo uy tín chuyên gia, kích thích comment tranh luận"
        },
        {
            "type": "Con Số Đột Phá & Công Thức Cụ Thể (Specific Framework)",
            "hook_text": f"Đúng 3 bước cực dễ để giải quyết triệt để {topic} — chỉ mất 3 phút mỗi ngày!",
            "visual_direction": "Giơ 3 ngón tay dứt khoát, trên màn hình hiện text số '1-2-3' to bản neon, nhạc upbeat nhịp nhàng.",
            "best_for": "YouTube Shorts & TikTok hướng dẫn (Save & Share cao)"
        },
        {
            "type": "Nghịch Lý Phản Trực Giác (Contrarian Shock)",
            "hook_text": f"Ai cũng nghĩ {topic} cần phải làm thế này, nhưng sự thật hoàn toàn ngược lại!",
            "visual_direction": "Đưa ra 1 hình ảnh sai lầm phổ biến và gạch chéo đỏ lớn, biểu cảm bất ngờ lắc đầu.",
            "best_for": "Kích hoạt tranh luận trong phần bình luận, tăng thuật toán phân phối"
        },
        {
            "type": "Câu Hỏi Đồng Cảm Nỗi Đau (Pain-Point Empathy)",
            "hook_text": f"Bạn có đang cảm thấy quá mệt mỏi và bế tắc mỗi khi phải xử lý {topic} không?",
            "visual_direction": "Mặt trầm ngâm, thở dài đồng cảm, zoom chậm vào ánh mắt chân thành.",
            "best_for": "Video tâm sự, bán sản phẩm giá trị cao (High-Ticket), xây dựng thương hiệu cá nhân bền vững"
        }
    ]

    return {
        "topic": topic,
        "audience": audience,
        "industry": industry,
        "total_hooks": len(hooks),
        "hooks": hooks,
        "golden_rule": "Luôn kết hợp: 0-3s câu Hook giật gân + ngay sau 3s phải có câu giải thích (Payoff) để giữ người xem không thoát!"
    }


@register_tool(
    name="format_social_post",
    description="Tối ưu định dạng bài viết đa kênh (Facebook, TikTok, Zalo OA, Threads/Instagram). Tự động chèn ngắt dòng chống mỏi mắt, phân cấp icon emoji, và lời kêu gọi hành động (CTA) phù hợp thuật toán từng mạng.",
    agent_ids=["social-creator", "media-producer", "dev-automation"],
    category="social",
    parameters={
        "type": "object",
        "properties": {
            "platform": {"type": "string", "enum": ["facebook", "tiktok", "zalo", "instagram"], "description": "Nền tảng đích"},
            "content": {"type": "string", "description": "Nội dung thô của bài viết"},
            "hashtags": {"type": "array", "items": {"type": "string"}, "description": "Danh sách hashtag gợi ý", "default": []},
            "cta_target": {"type": "string", "description": "Đích đến của lời kêu gọi (inbox, zalo, comment, call)", "default": "zalo"}
        },
        "required": ["platform", "content"]
    }
)
def format_social_post(
    platform: str,
    content: str,
    hashtags: Optional[List[str]] = None,
    cta_target: str = "zalo"
) -> Dict[str, Any]:
    """Formats raw post text for specific social platforms."""
    plat = platform.lower()
    tags = hashtags or ["#trending", "#viral", "#giaiphapkinhdoanh"]
    tag_str = " ".join(tags)

    ctas = {
        "zalo": "👉 Nhắn ngay qua Zalo để nhận tư vấn 1-1 và bảng giá ưu đãi hôm nay!",
        "inbox": "📩 Inbox ngay cho page để được hỗ trợ kiểm tra miễn phí trong 5 phút!",
        "comment": "👇 Để lại bình luận 'QUAN TÂM' bên dưới, mình gửi chi tiết nhé!",
        "call": "📞 Gọi trực tiếp hotline hỗ trợ 24/7 để được giải đáp ngay!"
    }
    cta_text = ctas.get(cta_target, ctas["zalo"])

    if plat == "tiktok":
        formatted = f"{content.strip()[:200]}...\n\n{cta_text}\n\n{tag_str}"
        notes = "TikTok ưu tiên 2 dòng đầu ngắn gọn trước nút 'Xem thêm', độ dài tối ưu 150-300 ký tự."
    elif plat == "facebook":
        formatted = f"{content.strip()}\n\n---\n{cta_text}\n\n{tag_str}"
        notes = "Facebook ưa chuộng ngắt đoạn 1-2 câu, icon điều hướng rõ ràng, CTA ở cuối."
    elif plat == "zalo":
        formatted = f"Kính gửi Quý khách,\n\n{content.strip()}\n\n{cta_text}\nTrân trọng cảm ơn Quý khách!"
        notes = "Zalo cần văn phong lịch thiệp, tôn trọng, thông tin chính xác, không dùng quá nhiều hashtag."
    else:
        formatted = f"{content.strip()}\n\n{cta_text}\n\n{tag_str}"
        notes = "Định dạng tổng quát chuẩn di động."

    return {
        "platform": plat,
        "formatted_post": formatted,
        "guideline": notes,
        "cta_applied": cta_text
    }


@register_tool(
    name="generate_visual_prompt",
    description="Tạo câu lệnh Prompt AI chuyên nghiệp (Midjourney v6 / Flux / Runway Gen-3) cho phân cảnh video hoặc ảnh bìa Thumbnail. Chuẩn ánh sáng Studio, góc máy Cinematic và tỷ lệ khung hình.",
    agent_ids=["social-creator", "media-producer"],
    category="social",
    parameters={
        "type": "object",
        "properties": {
            "scene_description": {"type": "string", "description": "Mô tả nội dung khung cảnh muốn vẽ/sinh video"},
            "style": {"type": "string", "description": "Phong cách hình ảnh (cinematic commercial, anime, hyper-realistic, 3d render)", "default": "cinematic commercial"},
            "aspect_ratio": {"type": "string", "enum": ["9:16", "16:9", "1:1", "4:5"], "description": "Tỉ lệ khung hình (9:16 cho TikTok/Reels, 16:9 cho YouTube)", "default": "9:16"},
            "lighting": {"type": "string", "description": "Ánh sáng (studio softbox, golden hour, neon dramatic)", "default": "studio softbox"}
        },
        "required": ["scene_description"]
    }
)
def generate_visual_prompt(
    scene_description: str,
    style: str = "cinematic commercial",
    aspect_ratio: str = "9:16",
    lighting: str = "studio softbox"
) -> Dict[str, Any]:
    """Generates production-ready AI image and video generation prompts."""
    mj_prompt = (
        f"{scene_description}, {style} style, {lighting}, shot on 35mm lens, photorealistic 8k, "
        f"hyper-detailed textures, cinematic color grading, high aesthetic, editorial shot --ar {aspect_ratio} --v 6.1 --stylize 250"
    )
    runway_prompt = (
        f"Cinematic slow motion camera push-in: {scene_description}. {lighting}, ultra realistic 4k quality, 24fps smooth motion."
    )
    negative_prompt = "low quality, blur, watermark, deformed hands, cartoonish, low resolution, ugly face, text artifacts"

    return {
        "scene": scene_description,
        "midjourney_prompt": mj_prompt,
        "runway_gen3_prompt": runway_prompt,
        "negative_prompt": negative_prompt,
        "aspect_ratio": aspect_ratio
    }
