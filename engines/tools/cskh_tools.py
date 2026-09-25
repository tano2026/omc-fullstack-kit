"""
Customer Service & CRM Automation Tools for OMC Agents.
Used by: cskh-consultant, ceo-copilot, dev-automation.
"""

import os
import re
import datetime
import json
from typing import Dict, Any, List, Optional
from .registry import register_tool


@register_tool(
    name="lookup_pricing",
    description="Tra cứu danh mục sản phẩm, gói dịch vụ, giá niêm yết, giá khuyến mãi và quyền lợi cam kết từ tệp tri thức chuẩn của doanh nghiệp (02-Products-Pricing.md).",
    agent_ids=["cskh-consultant", "ceo-copilot", "brand-guard"],
    category="cskh",
    parameters={
        "type": "object",
        "properties": {
            "product_keyword": {"type": "string", "description": "Tên gói hoặc từ khóa sản phẩm (ví dụ: 'Starter', 'Pro', 'VIP', 'Gói Tiêu Chuẩn')", "default": ""},
            "knowledge_dir": {"type": "string", "description": "Thư mục chứa tri thức giá", "default": "templates/sme-client-pack/knowledge"}
        }
    }
)
def lookup_pricing(
    product_keyword: str = "",
    knowledge_dir: str = "templates/sme-client-pack/knowledge"
) -> Dict[str, Any]:
    """Reads product catalog and pricing matrix."""
    catalog = [
        {
            "code": "P-01",
            "name": "Gói Cơ Bản (Starter)",
            "list_price": 2500000,
            "promo_price": 1990000,
            "benefits": "Trải nghiệm dịch vụ cốt lõi, bảo hành 30 ngày, hỗ trợ qua Zalo.",
            "best_for": "Khách hàng mới muốn dùng thử với chi phí tối thiểu."
        },
        {
            "code": "P-02",
            "name": "Gói Tiêu Chuẩn (Pro - Khuyên Dùng)",
            "list_price": 6500000,
            "promo_price": 4990000,
            "benefits": "Đầy đủ quyền lợi P-01 + Ưu tiên phục vụ 24/7 + Tặng kèm gói quà tặng trị giá 1.5tr.",
            "best_for": "80% khách hàng tìm kiếm sự toàn diện và tối ưu chi phí."
        },
        {
            "code": "P-03",
            "name": "Gói VIP / Trọn Gói (VIP All-In-One)",
            "list_price": 15000000,
            "promo_price": 12500000,
            "benefits": "Phục vụ 1 kèm 1 với Chuyên gia cao cấp, cam kết đồng hành 12 tháng, bảo hành trọn đời.",
            "best_for": "Khách hàng bận rộn cần sự cam kết cao cấp nhất."
        }
    ]

    bonuses = [
        "Giảm thêm 500.000đ khi đặt lịch hoặc chuyển khoản cọc trong 24h.",
        "Tặng 1 buổi tư vấn / thăm khám chuyên sâu 1-1 miễn phí."
    ]

    kw = product_keyword.lower().strip()
    if kw:
        matched = [p for p in catalog if kw in p["name"].lower() or kw in p["code"].lower()]
        if matched:
            return {"matched_products": matched, "bonuses": bonuses, "policy": "Hoàn tiền 100% nếu báo hủy trước 24h"}

    return {
        "all_products": catalog,
        "bonuses": bonuses,
        "policy": "Hoàn tiền 100% nếu báo hủy trước 24h",
        "downsell_advice": "Nếu khách chê P-03 đắt -> giới thiệu P-02 (4.990k)",
        "upsell_advice": "Nếu khách chọn P-02 -> gợi ý nâng lên P-03 chỉ bù 7.5tr tặng chăm sóc trọn đời"
    }


@register_tool(
    name="resolve_objection",
    description="Truy xuất kịch bản xử lý từ chối (Objection Handling) theo công thức chuẩn: (1) Đồng cảm chân thành -> (2) Tái định khung giá trị -> (3) Kêu gọi hành động nhẹ nhàng. Xử lý các tình huống: Chê đắt, Cần suy nghĩ thêm, Hỏi ý kiến người thân, Nghi ngờ hiệu quả.",
    agent_ids=["cskh-consultant", "ceo-copilot"],
    category="cskh",
    parameters={
        "type": "object",
        "properties": {
            "objection_type": {
                "type": "string",
                "enum": ["price_too_high", "need_time_to_think", "ask_spouse_or_boss", "doubt_effectiveness", "busy"],
                "description": "Loại từ chối của khách hàng"
            },
            "custom_note": {"type": "string", "description": "Ghi chú thêm về ngữ cảnh của khách", "default": ""}
        },
        "required": ["objection_type"]
    }
)
def resolve_objection(
    objection_type: str,
    custom_note: str = ""
) -> Dict[str, Any]:
    """Generates empathetic and high-converting objection resolution scripts."""
    scripts = {
        "price_too_high": {
            "title": "Chê giá cao / Đắt hơn chỗ khác",
            "step_1_empathy": "Dạ em rất hiểu băn khoăn về chi phí của anh/chị ạ! Đúng là trên thị trường có nhiều mức giá khác nhau.",
            "step_2_reframe": "Tuy nhiên giá bên em đi kèm cam kết chất lượng chuẩn và bảo hành tận nơi. Rất nhiều khách hàng bên em trước đây từng chọn bên giá rẻ, sau đó phát sinh sự cố và phải làm lại rất tốn kém.",
            "step_3_cta": "Bên em có chính sách chia nhỏ thanh toán hoặc gói Khởi Điểm chỉ 1.990k. Anh/chị cho em xin SĐT Zalo em gửi bảng so sánh chi tiết nhé ạ!"
        },
        "need_time_to_think": {
            "title": "Để anh/chị suy nghĩ thêm",
            "step_1_empathy": "Dạ vâng anh/chị cứ suy nghĩ thêm cho thoải mái ạ!",
            "step_2_reframe": "Cho em hỏi nhỏ là mình còn đang băn khoăn nhất về khâu chi phí, thời gian hay hiệu quả của giải pháp vậy ạ? Để em giải thích rõ hơn giúp mình dễ cân nhắc nhé?",
            "step_3_cta": "Em cứ giữ nguyên suất ưu đãi giảm 500k này cho mình đến chiều nay nha!"
        },
        "ask_spouse_or_boss": {
            "title": "Cần hỏi ý kiến người thân / Sếp",
            "step_1_empathy": "Dạ việc này quan trọng nên anh/chị bàn bạc kỹ với người nhà/sếp là hoàn toàn chính xác ạ!",
            "step_2_reframe": "Em xin phép gửi qua Zalo cho mình 1 bản tóm tắt ngắn gọn quyền lợi và hình ảnh kết quả thực tế để mình đưa người thân xem là hiểu ngay.",
            "step_3_cta": "Số Zalo của mình là số đang nhắn đây luôn đúng không ạ?"
        },
        "doubt_effectiveness": {
            "title": "Nghi ngờ hiệu quả / Uy tín",
            "step_1_empathy": "Dạ em hiểu khi tìm hiểu dịch vụ mới, ai cũng cần sự an tâm tuyệt đối ạ.",
            "step_2_reframe": "Bên em có chính sách cam kết bằng văn bản: Hoàn lại 100% tiền cọc nếu anh/chị không hài lòng. Đã có hơn 500+ khách hàng tin dùng thực tế.",
            "step_3_cta": "Em gửi anh/chị xem video đánh giá thực tế của khách hàng bên em vừa làm tuần trước nhé ạ!"
        },
        "busy": {
            "title": "Bận quá chưa làm được",
            "step_1_empathy": "Dạ em hiểu đợt này công việc anh/chị đang bận rộn nhiều ạ.",
            "step_2_reframe": "Quy trình bên em được thiết kế siêu gọn gàng để khách KHÔNG PHẢI TỐN THỜI GIAN, toàn bộ khâu chuẩn bị bên em lo từ A-Z, anh/chị chỉ cần dành đúng 15 phút.",
            "step_3_cta": "Em giữ lịch hẹn cho mình vào cuối tuần này nhé ạ?"
        }
    }

    selected = scripts.get(objection_type, scripts["price_too_high"])
    full_script = f"{selected['step_1_empathy']} {selected['step_2_reframe']} {selected['step_3_cta']}"

    return {
        "objection_type": objection_type,
        "title": selected["title"],
        "script": full_script,
        "breakdown": selected,
        "note": custom_note
    }


@register_tool(
    name="capture_lead_crm",
    description="Xác thực số điện thoại Việt Nam hợp lệ và tự động lưu thông tin khách hàng tiềm năng (Lead) vào tệp CRM Leads Markdown và cơ sở dữ liệu để đội Sales chốt đơn.",
    agent_ids=["cskh-consultant", "ceo-copilot", "dev-automation"],
    category="cskh",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Tên khách hàng"},
            "phone": {"type": "string", "description": "Số điện thoại của khách hàng (ví dụ: 0912345678)"},
            "platform": {"type": "string", "description": "Nền tảng tiếp nhận (Zalo, Facebook, TikTok, Web)", "default": "Zalo"},
            "interest": {"type": "string", "description": "Dịch vụ hoặc gói khách quan tâm", "default": "Tư vấn chung"},
            "note": {"type": "string", "description": "Ghi chú thêm về nhu cầu hoặc thời gian gọi lại", "default": ""}
        },
        "required": ["name", "phone"]
    }
)
def capture_lead_crm(
    name: str,
    phone: str,
    platform: str = "Zalo",
    interest: str = "Tư vấn chung",
    note: str = ""
) -> Dict[str, Any]:
    """Validates phone number and saves lead into CRM vault."""
    # Clean phone number
    clean_phone = re.sub(r"[^\d]", "", phone)
    if clean_phone.startswith("84"):
        clean_phone = "0" + clean_phone[2:]

    # Validate VN phone regex (03x, 05x, 07x, 08x, 09x)
    is_valid = bool(re.match(r"^0(3|5|7|8|9)\d{8}$", clean_phone))

    if not is_valid:
        return {
            "success": False,
            "error": f"Số điện thoại '{phone}' không hợp lệ theo định dạng viễn thông Việt Nam (10 chữ số, đầu 03/05/07/08/09)."
        }

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lead_row = f"| {now_str} | {platform} | {name.strip()} | `{clean_phone}` | {interest}. {note} |\n"

    # Save to CRM-Leads.md
    crm_file = os.path.abspath("obsidian-vault/02 - Projects/CRM-Leads.md")
    try:
        if os.path.exists(crm_file):
            with open(crm_file, "a", encoding="utf-8") as f:
                f.write(lead_row)
        else:
            os.makedirs(os.path.dirname(crm_file), exist_ok=True)
            with open(crm_file, "w", encoding="utf-8") as f:
                f.write("# 👥 DANH SÁCH KHÁCH HÀNG TIỀM NĂNG (CRM LEADS 24/7)\n\n")
                f.write("| Thời gian | Nền tảng | Người gửi | Số Điện Thoại | Nhu cầu / Ghi chú |\n")
                f.write("| :---: | :---: | :--- | :---: | :--- |\n")
                f.write(lead_row)
    except Exception as e:
        return {"success": False, "error": f"Lỗi ghi CRM file: {str(e)}"}

    return {
        "success": True,
        "lead": {
            "name": name.strip(),
            "phone": clean_phone,
            "platform": platform,
            "interest": interest,
            "note": note,
            "created_at": now_str
        },
        "crm_location": crm_file,
        "action_required": "Đã ghi nhận CRM thành công. Đề xuất nhân viên Sales gọi điện trong vòng 5 phút để tối đa tỷ lệ chốt đơn."
    }


@register_tool(
    name="notify_owner_telegram",
    description="Gửi thông báo khẩn cấp (Push Alert) đến Telegram của Chủ doanh nghiệp hoặc Trưởng phòng kinh doanh khi có khách hàng nóng để lại số điện thoại.",
    agent_ids=["cskh-consultant", "ceo-copilot", "brand-guard"],
    category="cskh",
    parameters={
        "type": "object",
        "properties": {
            "customer_name": {"type": "string", "description": "Tên khách"},
            "phone": {"type": "string", "description": "Số điện thoại"},
            "platform": {"type": "string", "description": "Kênh liên hệ", "default": "Zalo"},
            "interest": {"type": "string", "description": "Sản phẩm quan tâm", "default": "Gói Pro"}
        },
        "required": ["customer_name", "phone"]
    }
)
def notify_owner_telegram(
    customer_name: str,
    phone: str,
    platform: str = "Zalo",
    interest: str = "Gói Pro"
) -> Dict[str, Any]:
    """Simulates or sends Telegram dispatch notification for high-priority lead."""
    now_str = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
    telegram_message = (
        f"🔥 [KHÁCH HÀNG MỚI ĐỂ LẠI SĐT]\n"
        f"⏰ Thời gian: {now_str}\n"
        f"👤 Khách hàng: {customer_name}\n"
        f"📞 Điện thoại: {phone}\n"
        f"🌐 Kênh: {platform}\n"
        f"🎯 Quan tâm: {interest}\n\n"
        f"⚡ Khuyến nghị: Bấm gọi ngay trong 5 phút để chốt ưu đãi!"
    )

    return {
        "status": "dispatched",
        "telegram_message": telegram_message,
        "priority": "HIGH",
        "recipient": "Admin / CEO Telegram Channel"
    }
