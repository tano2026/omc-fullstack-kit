#!/usr/bin/env python3
"""
OMC Webhook & Omni-Channel Social Gateway (Web Chat, Zalo, Facebook, TikTok)
Cổng máy chủ HTTP tích hợp 3-trong-1:
1. Giao diện Web Chat trực quan (Single-Page App) tại http://localhost:19888
2. Cổng nhận webhook mạng xã hội: Zalo OA, Facebook Messenger, TikTok
3. Cổng nhận webhook REST API cho các hệ thống CRM, n8n, Stripe.
"""

import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "obsidian-vault"))

from engines.trio_orchestrator import execute_omc_pipeline
from engines.jev_gateway.ingress_router import IngressRouter
from vault_sync import VaultSync
from gateway.social_gateway import OmniSocialGateway

PORT = 19888

HTML_CHAT_UI = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMC Command Center - Omni-Social & Media Studio</title>
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --text-main: #c9d1d9;
            --text-muted: #8b949e;
            --accent: #58a6ff;
            --accent-green: #2ea043;
            --border: #30363d;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background: var(--bg-primary); color: var(--text-main); height: 100vh; display: flex; overflow: hidden; }
        
        /* Sidebar */
        .sidebar { width: 320px; background: var(--bg-secondary); border-right: 1px solid var(--border); display: flex; flex-direction: column; }
        .sidebar-header { padding: 20px; border-bottom: 1px solid var(--border); }
        .sidebar-header h1 { font-size: 1.05rem; color: #fff; display: flex; align-items: center; gap: 8px; }
        .sidebar-header p { font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }
        .section-title { font-size: 0.7rem; text-transform: uppercase; color: var(--text-muted); padding: 12px 16px 4px; font-weight: 600; letter-spacing: 0.5px; }
        .agent-list { flex: 1; overflow-y: auto; padding: 6px 12px; }
        .agent-item { padding: 9px 12px; border-radius: 6px; margin-bottom: 4px; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: background 0.15s; font-size: 0.83rem; }
        .agent-item:hover, .agent-item.active { background: var(--bg-card); color: #fff; }
        .agent-badge { width: 8px; height: 8px; border-radius: 50%; background: var(--accent-green); }
        
        /* Main Chat */
        .chat-container { flex: 1; display: flex; flex-direction: column; background: var(--bg-primary); }
        .chat-header { padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; background: var(--bg-secondary); }
        .chat-header .title { font-weight: 600; font-size: 0.95rem; color: #fff; }
        .chat-header .channels { font-size: 0.75rem; color: var(--text-muted); display: flex; gap: 8px; }
        .channel-pill { background: var(--bg-card); padding: 2px 8px; border-radius: 12px; border: 1px solid var(--border); }
        .chat-box { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
        
        /* Messages */
        .msg { display: flex; flex-direction: column; max-width: 80%; }
        .msg.user { align-self: flex-end; }
        .msg.bot { align-self: flex-start; }
        .msg-bubble { padding: 12px 16px; border-radius: 8px; font-size: 0.9rem; line-height: 1.5; word-wrap: break-word; }
        .msg.user .msg-bubble { background: #1f6feb; color: #fff; border-bottom-right-radius: 2px; }
        .msg.bot .msg-bubble { background: var(--bg-card); border: 1px solid var(--border); border-bottom-left-radius: 2px; white-space: pre-wrap; }
        .msg-meta { font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; }
        .msg.user .msg-meta { text-align: right; }
        
        /* Input Area */
        .chat-input-area { padding: 16px 24px; background: var(--bg-secondary); border-top: 1px solid var(--border); display: flex; gap: 12px; }
        .chat-input { flex: 1; background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 12px 16px; color: #fff; font-size: 0.9rem; outline: none; }
        .chat-input:focus { border-color: var(--accent); }
        .send-btn { background: var(--accent-green); color: #fff; border: none; border-radius: 6px; padding: 0 20px; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
        .send-btn:hover { opacity: 0.9; }
        .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>🏢 OMC Omni-Command Center</h1>
            <p>Research • Video Media • Social Chatbot 24/7</p>
        </div>
        <div class="section-title">Kênh Mạng Xã Hội Đang Kết Nối</div>
        <div class="agent-list" style="flex: 0 0 auto; max-height: 120px;">
            <div class="agent-item"><div class="agent-badge"></div> 💬 Zalo OA (Webhook Active)</div>
            <div class="agent-item"><div class="agent-badge"></div> 📘 Facebook Messenger & Page</div>
            <div class="agent-item"><div class="agent-badge"></div> 🎵 TikTok DM & Comments</div>
        </div>
        <div class="section-title">Biệt Đội Nhân Sự AI Vận Hành</div>
        <div class="agent-list">
            <div class="agent-item active" onclick="selectAgent('cskh-consultant')"><div class="agent-badge"></div> 💬 CSKH & Chốt Đơn 24/7</div>
            <div class="agent-item" onclick="selectAgent('social-creator')"><div class="agent-badge"></div> 🎬 Kịch Bản Video & Social</div>
            <div class="agent-item" onclick="selectAgent('market-spy')"><div class="agent-badge"></div> 🕵️ Soi Trend & Đối Thủ 30 Ngày</div>
            <div class="agent-item" onclick="selectAgent('ceo-copilot')"><div class="agent-item-icon">👑</div> Thư Ký Báo Cáo Cho Sếp</div>
            <div class="agent-item" onclick="selectAgent('brand-guard')"><div class="agent-badge"></div> 🛡️ Rào Chắn Bảo Vệ Thương Hiệu</div>
            <div class="agent-item" onclick="selectAgent('hermes-master')"><div class="agent-badge"></div> 🏛️ Hermes Master (Tổng Quản)</div>
        </div>
    </div>
    
    <div class="chat-container">
        <div class="chat-header">
            <div class="title" id="chat-title">Phòng điều phối: 💬 CSKH & Chốt Đơn 24/7 (Zalo, FB, TikTok)</div>
            <div class="channels">
                <span class="channel-pill">Zalo OA: 🟢</span>
                <span class="channel-pill">Facebook: 🟢</span>
                <span class="channel-pill">TikTok: 🟢</span>
                <span class="channel-pill">CRM Sync: 🟢</span>
            </div>
        </div>
        <div class="chat-box" id="chat-box">
            <div class="msg bot">
                <div class="msg-bubble">👋 Chào bạn! Tôi là Trợ Lý Tư Vấn & Chăm Sóc Khách Hàng 24/7. Tôi túc trực đa kênh trên Zalo, Facebook Messenger và TikTok. Bạn cần tư vấn dịch vụ, kiểm tra bảng giá hay lên kịch bản video TikTok? Hãy nhắn cho tôi nhé!</div>
                <div class="msg-meta">Hệ thống • Vừa xong</div>
            </div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="user-input" class="chat-input" placeholder="Nhập tin nhắn (thử gõ: 'Cho mình hỏi giá gói VIP và SĐT mình là 0912345678' hoặc 'Lên kịch bản video TikTok')..." onkeydown="if(event.key==='Enter') sendMessage()">
            <button class="send-btn" id="send-btn" onclick="sendMessage()">Gửi</button>
        </div>
    </div>

    <script>
        let currentAgent = "cskh-consultant";

        function selectAgent(agent) {
            currentAgent = agent;
            document.querySelectorAll('.agent-item').forEach(el => el.classList.remove('active'));
            event.currentTarget.classList.add('active');
            document.getElementById('chat-title').innerText = "Phòng điều phối: @" + agent;
            appendMessage("bot", "Đã chuyển sang phòng điều phối @" + agent + ". Bạn có thể bắt đầu giao việc!");
        }

        function appendMessage(sender, text) {
            const chatBox = document.getElementById('chat-box');
            const msgDiv = document.createElement('div');
            msgDiv.className = 'msg ' + sender;
            const now = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            msgDiv.innerHTML = `
                <div class="msg-bubble">${escapeHtml(text)}</div>
                <div class="msg-meta">${sender === 'user' ? 'Bạn' : '@' + currentAgent} • ${now}</div>
            `;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }

        async function sendMessage() {
            const input = document.getElementById('user-input');
            const btn = document.getElementById('send-btn');
            const text = input.value.trim();
            if (!text) return;

            appendMessage('user', text);
            input.value = '';
            input.disabled = true;
            btn.disabled = true;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, agent: currentAgent })
                });
                const data = await response.json();
                if (data.reply) {
                    appendMessage('bot', data.reply);
                } else if (data.result) {
                    appendMessage('bot', "🚀 Quad-Engine đã thực thi hoàn tất!\\n" + JSON.stringify(data.result, null, 2));
                } else {
                    appendMessage('bot', "Đã ghi nhận yêu cầu vào hệ thống.");
                }
            } catch (err) {
                appendMessage('bot', "❌ Lỗi kết nối máy chủ: " + err.message);
            } finally {
                input.disabled = false;
                btn.disabled = false;
                input.focus();
            }
        }
    </script>
</body>
</html>
"""

class OMCWebhookHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.social_bot = OmniSocialGateway()
        super().__init__(*args, **kwargs)

    def _send_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _send_html(self, html_content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # 1. Web Chat UI
        if parsed.path in ("/", "/chat", "/index.html"):
            self._send_html(HTML_CHAT_UI)
            
        # 2. Facebook Webhook Verification Handshake
        elif parsed.path == "/webhook/facebook":
            query_params = urllib.parse.parse_qs(parsed.query)
            mode = query_params.get("hub.mode", [""])[0]
            token = query_params.get("hub.verify_token", [""])[0]
            challenge = query_params.get("hub.challenge", [""])[0]
            
            # Default verify token
            if mode == "subscribe":
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(challenge.encode("utf-8"))
                print(f"✅ Facebook Webhook Handshake xác thực thành công!")
            else:
                self._send_response(403, {"error": "Verification failed"})
                
        # 3. Health check
        elif parsed.path == "/health":
            self._send_response(200, {
                "status": "ok",
                "service": "OMC Omni-Social & Webhook Gateway",
                "channels": ["zalo", "facebook", "tiktok", "telegram", "web"]
            })
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(body) if body else {}
        except Exception:
            payload = {}

        # 1. Internal Web Chat API
        if self.path == "/api/chat":
            message = payload.get("message", "")
            agent = payload.get("agent", "cskh-consultant")
            if not message:
                self._send_response(400, {"error": "Thiếu nội dung 'message'"})
                return

            res = self.social_bot.process_incoming_message(
                platform="web",
                sender_id="web_visitor",
                sender_name="Khách Web",
                message=message
            )
            self._send_response(200, {"status": "success", "reply": res["reply"], "lead": res["captured_phone"]})

        # 2. Zalo Official Account (OA) Webhook
        elif self.path == "/webhook/zalo":
            event_name = payload.get("event_name", "user_send_text")
            sender_id = payload.get("sender", {}).get("id", "zalo_anonymous")
            user_msg = payload.get("message", {}).get("text", "")
            
            res = self.social_bot.process_incoming_message(
                platform="zalo",
                sender_id=sender_id,
                sender_name="Khách Zalo",
                message=user_msg
            )
            self._send_response(200, {"error": 0, "message": "Success", "reply": res["reply"]})

        # 3. Facebook Messenger Webhook
        elif self.path == "/webhook/facebook":
            # Extract messaging events
            entries = payload.get("entry", [])
            reply_text = ""
            for entry in entries:
                for messaging_event in entry.get("messaging", []):
                    sender_id = messaging_event.get("sender", {}).get("id", "")
                    message_text = messaging_event.get("message", {}).get("text", "")
                    if message_text:
                        res = self.social_bot.process_incoming_message(
                            platform="facebook",
                            sender_id=sender_id,
                            sender_name="Khách Messenger",
                            message=message_text
                        )
                        reply_text = res["reply"]
            self._send_response(200, {"status": "EVENT_RECEIVED", "reply": reply_text})

        # 4. TikTok DM & Shop Webhook
        elif self.path == "/webhook/tiktok":
            sender_id = payload.get("user_id", "tiktok_user")
            message_text = payload.get("content", "")
            res = self.social_bot.process_incoming_message(
                platform="tiktok",
                sender_id=sender_id,
                sender_name="Khách TikTok",
                message=message_text
            )
            self._send_response(200, {"code": 0, "reply": res["reply"]})

        # 5. Generic Task Webhook (n8n, Zapier, Stripe, CRM)
        elif self.path == "/webhook/task":
            task_text = payload.get("task") or payload.get("message") or payload.get("prompt")
            if not task_text:
                self._send_response(400, {"error": "Missing 'task' parameter"})
                return
            result = execute_omc_pipeline(task_text)
            self._send_response(200, {"status": "success", "result": result})

        else:
            self._send_response(404, {"error": "Unknown webhook route"})

def run_server(port=PORT):
    server = HTTPServer(("0.0.0.0", port), OMCWebhookHandler)
    print("=" * 70)
    print(f"🌐 OMC OMNI-SOCIAL & MEDIA WEBHOOK GATEWAY ĐANG CHẠY:")
    print(f"👉 Mở Web Chat điều hành : http://localhost:{port}")
    print(f"👉 Webhook Zalo OA       : http://localhost:{port}/webhook/zalo")
    print(f"👉 Webhook Facebook Page : http://localhost:{port}/webhook/facebook")
    print(f"👉 Webhook TikTok DM     : http://localhost:{port}/webhook/tiktok")
    print(f"👉 Webhook CRM / n8n     : http://localhost:{port}/webhook/task")
    print("=" * 70)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
