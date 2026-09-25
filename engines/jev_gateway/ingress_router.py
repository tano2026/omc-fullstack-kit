#!/usr/bin/env python3
"""
JEV Ingress Router - System 1 Reflex Routing (~10ms)
Nhận diện ý định và tự động định tuyến yêu cầu từ Telegram / Webhook đến đúng Agent chuyên môn.
"""

import re
import sys
from typing import Dict, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROUTING_RULES = [
    # Explicit mentions
    (r"^@(main)\b", "main"),
    (r"^@(dsh-commander|dsh|planner)\b", "dsh-commander"),
    (r"^@(hermes-architect|hermes|architect)\b", "hermes-architect"),
    (r"^@(dev-automation|dev|coder|bot)\b", "dev-automation"),
    (r"^@(media-producer|media|video)\b", "media-producer"),
    (r"^@(openclaw-executor|executor|devops)\b", "openclaw-executor"),
    (r"^@(jev-sentinel|sentinel|security)\b", "jev-sentinel"),
    (r"^@(research-intel|research|seo)\b", "research-intel"),
    (r"^@(domain-ops|ops|airport-ops|travel)\b", "domain-ops"),
    
    # Natural language keywords
    (r"(video|tiktok|reels|shorts|kịch bản|storyboard|midjourney|runway)", "media-producer"),
    (r"(code|script|api|bug|lập trình|zalo|webhook|bot|crawler|cào dữ liệu|frontend|backend)", "dev-automation"),
    (r"(seo|aeo|geo|nghiên cứu đối thủ|từ khóa|thị trường|social listening|market)", "research-intel"),
    (r"(kiến trúc|thiết kế hệ thống|audit|tối ưu thuật toán|adr|refactor)", "hermes-architect"),
    (r"(lập kế hoạch|kế hoạch|phân rã|mục tiêu|dag|tiến độ|roadmap)", "dsh-commander"),
    (r"(deploy|server|pm2|git|terminal|chạy lệnh|restart|service|docker)", "openclaw-executor"),
    (r"(bảo mật|xóa|drop|quyền|an toàn|audit code|quét lỗi)", "jev-sentinel"),
    (r"(sân bay|fast track|lounge|phòng chờ|đón tiễn|vé máy bay|đặt tour)", "domain-ops")
]

class IngressRouter:
    @staticmethod
    def route_message(text: str) -> Dict[str, Any]:
        """Phân tích nội dung và trả về agent được phân công trong 10ms"""
        cleaned_text = text.strip()
        matched_agent = "main" # default fallback
        confidence = "normal"
        
        # 1. Check explicit mention
        for pattern, agent_id in ROUTING_RULES[:9]:
            if re.search(pattern, cleaned_text, re.IGNORECASE):
                # Remove mention from text
                prompt = re.sub(pattern, "", cleaned_text, flags=re.IGNORECASE).strip()
                return {
                    "agent": agent_id,
                    "prompt": prompt or cleaned_text,
                    "confidence": "explicit_mention",
                    "routing_mode": "manual"
                }

        # 2. Check natural language regex
        for pattern, agent_id in ROUTING_RULES[9:]:
            if re.search(pattern, cleaned_text, re.IGNORECASE):
                matched_agent = agent_id
                confidence = "high_intent_match"
                break
                
        return {
            "agent": matched_agent,
            "prompt": cleaned_text,
            "confidence": confidence,
            "routing_mode": "auto_reflex"
        }

if __name__ == "__main__":
    tests = [
        "@dev-automation Viết script cào dữ liệu giá vé máy bay",
        "Lên kịch bản 3 video ngắn TikTok review dịch vụ",
        "Nghiên cứu từ khóa SEO cho tour du lịch mùa đông",
        "Lập kế hoạch triển khai tính năng thanh toán tự động",
        "Khách chuyến VN214 cần 2 Fast Track T2 Nội Bài"
    ]
    for t in tests:
        res = IngressRouter.route_message(t)
        print(f"[{res['agent']:<18}] ➔ '{t}'")
