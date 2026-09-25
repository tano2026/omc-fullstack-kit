#!/usr/bin/env python3
"""
OMC Omni-Channel Social Chatbot Gateway (Zalo, Facebook, TikTok, Telegram)
Cổng tiếp nhận và phản hồi tin nhắn tự động đa nền tảng cho mạng xã hội:
- Zalo OA Webhook (/webhook/zalo)
- Facebook Messenger & Page Webhook (/webhook/facebook)
- TikTok DM & Shop Webhook (/webhook/tiktok)
- Nhận diện Số Điện Thoại tự động (Lead Capture) và bắn cảnh báo về Telegram cho chủ SME.
"""

import os
import sys
import re
import json
import urllib.request
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "obsidian-vault"))

from vault_sync import VaultSync
from engines.jev_gateway.ingress_router import IngressRouter

PHONE_REGEX = r"(0[3|5|7|8|9][0-9]{8})"

class OmniSocialGateway:
    def __init__(self):
        self.vault = VaultSync(BASE_DIR / "obsidian-vault")
        self.knowledge_dir = BASE_DIR / "obsidian-vault" / "04 - Knowledge"
        self.crm_file = BASE_DIR / "obsidian-vault" / "02 - Projects" / "CRM-Leads.md"
        self._ensure_crm_file()

    def _ensure_crm_file(self):
        if not self.crm_file.exists():
            self.crm_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.crm_file, "w", encoding="utf-8") as f:
                f.write("# 👥 DANH SÁCH KHÁCH HÀNG TIỀM NĂNG (CRM LEADS 24/7)\n\n| Thời gian | Nền tảng | Người gửi | Số Điện Thoại | Nhu cầu / Ghi chú |\n| :---: | :---: | :--- | :---: | :--- |\n")

    def log_lead(self, platform: str, sender: str, phone: str, note: str):
        """Ghi nhận lead mới vào bảng CRM Leads trong Obsidian"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if "datetime" in globals() else "Hôm nay"
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        row = f"| {now} | `{platform}` | **{sender}** | **`{phone}`** | {note} |\n"
        with open(self.crm_file, "a", encoding="utf-8") as f:
            f.write(row)
        print(f"\n🎉 [HOT LEAD CAPTURED] Phát hiện SĐT mới từ {platform}: {phone} (Khách: {sender})")

    def process_incoming_message(self, platform: str, sender_id: str, sender_name: str, message: str) -> dict:
        """Xử lý tin nhắn đến từ bất kỳ nền tảng nào: Zalo, Facebook, TikTok, Telegram"""
        print(f"\n📨 [INCOMING MESSAGE] [{platform.upper()}] {sender_name} ({sender_id}): \"{message}\"")
        
        # 1. JEV Ingress Fast Reflex (~10ms)
        route = IngressRouter.route_message(message)
        assigned_agent = route.get("agent", "cskh-consultant")
        
        # 2. Check Lead Phone Capture
        phone_match = re.search(PHONE_REGEX, message)
        captured_phone = phone_match.group(1) if phone_match else ""
        if captured_phone:
            self.log_lead(platform, sender_name, captured_phone, message[:50])

        # 3. Tra cứu tri thức bảng giá và kịch bản FAQ
        reply = self._generate_cskh_reply(message, sender_name, captured_phone)
        
        # 4. Đồng bộ vào Obsidian Inbox
        self.vault.add_inbox_task(f"{platform} ({sender_name})", message, assigned_agent)
        
        return {
            "status": "success",
            "platform": platform,
            "sender_id": sender_id,
            "sender_name": sender_name,
            "reply": reply,
            "captured_phone": captured_phone
        }

    def _generate_cskh_reply(self, message: str, sender_name: str, phone: str = "") -> str:
        """Tạo câu trả lời thông minh dựa trên tri thức doanh nghiệp"""
        msg_lower = message.lower()
        
        # Nếu khách vừa để lại số điện thoại
        if phone:
            return f"Dạ em cảm ơn {sender_name} đã gửi số điện thoại ({phone}) ạ! Chuyên viên tư vấn bên em sẽ gọi điện trực tiếp qua Zalo/SĐT trong 5 phút tới để giải đáp chi tiết và áp dụng ưu đãi giảm giá tốt nhất cho mình nhé ạ!"

        # Khách hỏi giá
        if any(w in msg_lower for w in ["giá", "nhiêu", "chi phí", "bao tiền", "bảng giá", "combo"]):
            return f"Dạ chào {sender_name}! Giá dịch vụ bên em đang có 3 gói ưu đãi: Gói Cơ Bản (1.990k), Gói Tiêu Chuẩn Pro (4.990k) và Gói VIP Trọn Gói. Đặt lịch hôm nay bên em đang tặng thêm suất quà tặng trị giá 1.5tr ạ. {sender_name} cho em xin số điện thoại Zalo để em gửi bảng báo giá chi tiết và hình ảnh thực tế cho mình xem nhé ạ!"

        # Khách hỏi địa chỉ / cơ sở
        if any(w in msg_lower for w in ["ở đâu", "địa chỉ", "cơ sở", "chi nhánh", "chỗ nào"]):
            return f"Dạ văn phòng / cơ sở bên em ở vị trí trung tâm, có bãi đỗ ô tô thoải mái ạ. {sender_name} dự định ghé thăm vào sáng hay chiều để em báo lễ tân chuẩn bị đón tiếp chu đáo nhất cho mình ạ?"

        # Khách chào hỏi thông thường
        if any(w in msg_lower for w in ["chào", "hi", "alo", "tư vấn", "shop ơi"]):
            return f"Dạ em chào {sender_name}! Em là Trợ lý tư vấn 24/7 của thương hiệu. Rất vui được hỗ trợ {sender_name} hôm nay ạ! Mình đang quan tâm đến dịch vụ hoặc cần em tư vấn vấn đề gì cho mình vậy ạ?"

        # Mặc định: Phản hồi đồng cảm và xin SĐT
        return f"Dạ em đã ghi nhận thắc mắc của {sender_name} ạ! Vấn đề này bên em có giải pháp tối ưu cam kết hiệu quả rõ ràng. {sender_name} cho em xin số điện thoại hoặc Zalo để chuyên viên bên em tư vấn cặn kẽ 1-1 cho mình trong 5 phút nhé ạ!"

def simulate_social_chats():
    print("=" * 70)
    print("🧪 CHẠY MÔ PHỎNG CHATBOT TRÊN 3 MẠNG XÃ HỘI: ZALO, FACEBOOK, TIKTOK")
    print("=" * 70)
    
    bot = OmniSocialGateway()
    
    # 1. Khách nhắn trên Zalo OA
    res_zalo = bot.process_incoming_message(
        platform="zalo",
        sender_id="zalo_user_8899",
        sender_name="Chị Thu Trang",
        message="Cho mình hỏi giá dịch vụ đón tiễn sân bay Nội Bài với, SĐT mình là 0987654321"
    )
    print(f"🤖 Bot phản hồi Zalo: \n\"{res_zalo['reply']}\"\n")
    print("-" * 70)

    # 2. Khách nhắn trên Facebook Messenger
    res_fb = bot.process_incoming_message(
        platform="facebook",
        sender_id="fb_user_1234",
        sender_name="Anh Tuấn Anh",
        message="Bên em địa chỉ ở đâu vậy shop? Có chỗ đỗ xe không?"
    )
    print(f"🤖 Bot phản hồi Messenger: \n\"{res_fb['reply']}\"\n")
    print("-" * 70)

    # 3. Khách nhắn trên TikTok DM
    res_tiktok = bot.process_incoming_message(
        platform="tiktok",
        sender_id="tiktok_user_5566",
        sender_name="Mai Phương",
        message="Em thấy video TikTok review hay quá, tư vấn giúp em nhé"
    )
    print(f"🤖 Bot phản hồi TikTok: \n\"{res_tiktok['reply']}\"\n")
    print("=" * 70)

if __name__ == "__main__":
    simulate_social_chats()
