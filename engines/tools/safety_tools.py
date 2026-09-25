"""
Brand Safety & Compliance Gatekeeper Tools for OMC Agents.
Used by: brand-guard, jev-sentinel, ceo-copilot.
"""

import re
from typing import Dict, Any, List, Optional
from .registry import register_tool


# Banned phrases that create legal liabilities or breach platform advertising policies
BANNED_PATTERNS = [
    (r"cam kết (100%|khỏi hẳn|dứt điểm|tuyệt đối)", "Vi phạm luật quảng cáo: Không được cam kết hiệu quả y tế/kết quả 100% không căn cứ"),
    (r"chữa khỏi|trị dứt điểm|đặc trị ung thư|thần dược", "Từ ngữ nhạy cảm y tế bị Meta/TikTok bóp tương tác hoặc cấm quảng cáo"),
    (r"lãi suất (khủng|siêu cao)|kiếm tiền dễ dàng|đổi đời sau 1 đêm", "Dấu hiệu lừa đảo tài chính (Scam/Ponzi) bị cấm ngặt"),
    (r"hoàn tiền vô điều kiện dù bất cứ lý do gì", "Rủi ro lạm dụng chính sách, chỉ nên dùng: Hoàn tiền theo điều kiện cam kết văn bản"),
    (r"đối thủ lừa đảo|tẩy chay bên|bọn nó làm ăn chộp giật", "Công kích đối thủ trực tiếp vi phạm đạo đức cạnh tranh lành mạnh")
]


@register_tool(
    name="audit_brand_safety",
    description="Kiểm duyệt nội dung bài viết, video script hoặc tin nhắn trả lời khách hàng trước khi xuất bản. Phát hiện các từ khóa vi phạm chính sách Facebook/TikTok, cam kết lố 100%, rủi ro pháp lý hoặc văn phong công kích.",
    agent_ids=["brand-guard", "jev-sentinel", "ceo-copilot"],
    category="safety",
    parameters={
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "Nội dung cần kiểm duyệt (bài post, kịch bản video, hoặc phản hồi CSKH)"},
            "channel": {"type": "string", "description": "Kênh xuất bản (facebook_ads, tiktok_organic, cskh_chat)", "default": "cskh_chat"}
        },
        "required": ["content"]
    }
)
def audit_brand_safety(
    content: str,
    channel: str = "cskh_chat"
) -> Dict[str, Any]:
    """Scans content for policy violations, dangerous claims, or brand risks."""
    violations = []
    content_lower = content.lower()

    for pattern, reason in BANNED_PATTERNS:
        match = re.search(pattern, content_lower)
        if match:
            violations.append({
                "detected_phrase": match.group(0),
                "reason": reason,
                "severity": "HIGH" if "y tế" in reason or "tài chính" in reason else "MEDIUM"
            })

    is_safe = len(violations) == 0

    return {
        "is_safe": is_safe,
        "total_violations": len(violations),
        "violations": violations,
        "channel": channel,
        "recommendation": (
            "✅ Nội dung đạt chuẩn an toàn thương hiệu. Đủ điều kiện xuất bản/phát ngôn."
            if is_safe else
            "⚠️ Phát hiện từ khóa nhạy cảm. Cần chỉnh sửa lại các từ cam kết tuyệt đối trước khi gửi khách hoặc chạy quảng cáo!"
        )
    }


@register_tool(
    name="verify_price_accuracy",
    description="Xác minh mức giá hoặc ưu đãi mà Agent chuẩn bị báo cho khách hàng có trùng khớp với Bảng giá chính thức trong tri thức doanh nghiệp hay không. Ngăn chặn triệt để tình trạng AI 'ảo giác' tự ý giảm giá làm thâm hụt doanh thu.",
    agent_ids=["brand-guard", "jev-sentinel", "cskh-consultant"],
    category="safety",
    parameters={
        "type": "object",
        "properties": {
            "quoted_price": {"type": "integer", "description": "Mức giá bằng VNĐ mà Bot định báo cho khách (ví dụ: 1990000, 4990000)"},
            "product_code_or_name": {"type": "string", "description": "Mã hoặc tên gói dịch vụ (ví dụ: 'P-01', 'P-02', 'Starter', 'Pro')"}
        },
        "required": ["quoted_price", "product_code_or_name"]
    }
)
def verify_price_accuracy(
    quoted_price: int,
    product_code_or_name: str
) -> Dict[str, Any]:
    """Cross-references quoted price against official catalog."""
    official_prices = {
        "p-01": {"name": "Gói Cơ Bản (Starter)", "valid_prices": [2500000, 1990000]},
        "starter": {"name": "Gói Cơ Bản (Starter)", "valid_prices": [2500000, 1990000]},
        "p-02": {"name": "Gói Tiêu Chuẩn (Pro)", "valid_prices": [6500000, 4990000, 4490000]}, # with fast action bonus 500k
        "pro": {"name": "Gói Tiêu Chuẩn (Pro)", "valid_prices": [6500000, 4990000, 4490000]},
        "p-03": {"name": "Gói VIP (VIP All-In-One)", "valid_prices": [15000000, 12500000, 12000000]},
        "vip": {"name": "Gói VIP (VIP All-In-One)", "valid_prices": [15000000, 12500000, 12000000]}
    }

    key = product_code_or_name.lower().strip()
    match = None
    for k, v in official_prices.items():
        if k in key:
            match = v
            break

    if not match:
        return {
            "valid": False,
            "reason": f"Không tìm thấy gói '{product_code_or_name}' trong bảng giá chuẩn. Vui lòng kiểm tra lại 02-Products-Pricing.md."
        }

    try:
        price_num = int(str(quoted_price).replace(".", "").replace(",", "").replace("đ", "").strip())
    except (ValueError, TypeError):
        return {
            "valid": False,
            "reason": f"Mức giá '{quoted_price}' không hợp lệ (cần là số nguyên)."
        }

    is_valid = price_num in match["valid_prices"]

    return {
        "product": match["name"],
        "quoted_price": price_num,
        "is_valid_price": is_valid,
        "allowed_prices": match["valid_prices"],
        "status": "APPROVED" if is_valid else "REJECTED",
        "action": (
            "✅ Giá chuẩn xác theo chính sách công ty."
            if is_valid else
            f"❌ CẢNH BÁO: Mức giá {price_num:,} đ không nằm trong bảng giá được duyệt ({match['valid_prices']}). Không được báo giá này cho khách!"
        )
    }
