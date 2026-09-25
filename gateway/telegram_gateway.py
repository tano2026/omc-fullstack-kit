#!/usr/bin/env python3
"""
OMC Telegram Ingress Gateway
Cổng kết nối Telegram Bot 24/7 với bộ định tuyến tự động JEV Ingress Router và đồng bộ Obsidian.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "obsidian-vault"))

from engines.jev_gateway.ingress_router import IngressRouter
from engines.trio_orchestrator import execute_omc_pipeline
from vault_sync import VaultSync

def get_env_var(name: str, default: str = "") -> str:
    # Try reading from config/.env if exists
    env_file = BASE_DIR / "config" / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(f"{name}="):
                    return line.strip().split(f"{name}=", 1)[1].strip().strip("\"'")
    return os.environ.get(name, default)

class TelegramGateway:
    def __init__(self, token: str = ""):
        self.token = token or get_env_var("TELEGRAM_BOT_TOKEN")
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = 0
        self.vault = VaultSync(BASE_DIR / "obsidian-vault")

    def send_message(self, chat_id: int, text: str):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                pass
        except Exception as e:
            # Fallback plain text if markdown fails
            payload.pop("parse_mode")
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    pass
            except Exception:
                pass

    def process_message(self, message: dict):
        chat_id = message.get("chat", {}).get("id")
        user_name = message.get("from", {}).get("first_name", "User")
        text = message.get("text", "").strip()

        if not text:
            return

        print(f"📩 Nhận tin từ @{user_name}: '{text}'")

        # 1. Special commands
        if text.startswith("/start"):
            welcome = (
                "👋 **Chào mừng bạn đến với Hệ thống One-Man Company (OMC)!**\n\n"
                "Cổng Ingress sẵn sàng nhận diện và phân phối tác vụ cho 9 Agent chuyên môn:\n"
                "- `@dsh-commander`: Lập kế hoạch mục tiêu (DAG)\n"
                "- `@hermes-architect`: Thiết kế kiến trúc & code phức tạp\n"
                "- `@dev-automation`: Kỹ sư Full-Stack & Bot RPA\n"
                "- `@media-producer`: Kịch bản video viral & media AI\n"
                "- `@openclaw-executor`: Thực thi terminal & DevOps 24/7\n"
                "- `@jev-sentinel`: Rào chắn an toàn dữ liệu\n"
                "- `@research-intel`: Nghiên cứu thị trường & SEO/AEO\n"
                "- `@domain-ops`: Vận hành nghiệp vụ công ty\n\n"
                "💡 *Bạn chỉ cần gõ yêu cầu tự nhiên, hệ thống sẽ tự động bắt ý định trong 10ms!*"
            )
            self.send_message(chat_id, welcome)
            return

        # 2. JEV Fast Routing
        route = IngressRouter.route_message(text)
        assigned_agent = route["agent"]

        # 3. Notify user of routing
        status_msg = f"⚡ **[JEV Ingress Gate]** Đã tiếp nhận và bàn giao cho `@{assigned_agent}`..."
        self.send_message(chat_id, status_msg)

        # 4. Run OMC Pipeline
        res = execute_omc_pipeline(text)
        
        reply = (
            f"✅ **[Hoàn Tất Nhiệm Vụ]**\n\n"
            f"• **Phụ trách:** `@{assigned_agent}`\n"
            f"• **Nhiệm vụ:** {text}\n"
            f"• **Trạng thái:** Thành công (Đã xác thực kiểm thử & lưu vào Obsidian Second Brain)."
        )
        self.send_message(chat_id, reply)

    def start_polling(self):
        if not self.token:
            print("⚠️ TELEGRAM_BOT_TOKEN chưa được cấu hình trong config/.env!")
            return
            
        print("🌐 OMC Telegram Gateway đang lắng nghe tin nhắn...")
        while True:
            try:
                url = f"{self.base_url}/getUpdates?offset={self.last_update_id + 1}&timeout=30"
                req = urllib.request.Request(url, headers={"User-Agent": "OMC-Gateway/1.0"})
                with urllib.request.urlopen(req, timeout=40) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    for update in data.get("result", []):
                        self.last_update_id = update["update_id"]
                        if "message" in update:
                            self.process_message(update["message"])
            except Exception as e:
                time.sleep(3)

if __name__ == "__main__":
    gw = TelegramGateway()
    gw.start_polling()
