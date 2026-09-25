#!/usr/bin/env python3
"""
OMC Webhook & Interactive Web Chat Gateway
Cổng máy chủ HTTP tích hợp 2-trong-1:
1. Giao diện Web Chat trực quan (Single-Page App) tại http://localhost:19888
2. Cổng nhận webhook REST API cho Zalo Mini App, CRM, n8n, Stripe.
"""

import os
import sys
import json
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

PORT = 19888

HTML_CHAT_UI = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMC Command Center - Interactive Chat</title>
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
        .sidebar { width: 300px; background: var(--bg-secondary); border-right: 1px solid var(--border); display: flex; flex-direction: column; }
        .sidebar-header { padding: 20px; border-bottom: 1px solid var(--border); }
        .sidebar-header h1 { font-size: 1.1rem; color: #fff; display: flex; align-items: center; gap: 8px; }
        .sidebar-header p { font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }
        .agent-list { flex: 1; overflow-y: auto; padding: 12px; }
        .agent-item { padding: 10px 12px; border-radius: 6px; margin-bottom: 6px; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: background 0.15s; font-size: 0.85rem; }
        .agent-item:hover, .agent-item.active { background: var(--bg-card); color: #fff; }
        .agent-badge { width: 8px; height: 8px; border-radius: 50%; background: var(--accent-green); }
        
        /* Main Chat */
        .chat-container { flex: 1; display: flex; flex-direction: column; background: var(--bg-primary); }
        .chat-header { padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; background: var(--bg-secondary); }
        .chat-header .title { font-weight: 600; font-size: 1rem; color: #fff; }
        .chat-header .status { font-size: 0.8rem; color: var(--accent-green); display: flex; align-items: center; gap: 6px; }
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
            <h1>🏢 OMC Command Center</h1>
            <p>Quad-Engine: DSH + Hermes + OpenClaw + JEV</p>
        </div>
        <div class="agent-list">
            <div class="agent-item active" onclick="selectAgent('main')"><div class="agent-badge"></div> 🌐 Gateway Ingress (Auto)</div>
            <div class="agent-item" onclick="selectAgent('hermes-master')"><div class="agent-badge"></div> 🏛️ Hermes Master (Chief)</div>
            <div class="agent-item" onclick="selectAgent('dsh-commander')"><div class="agent-badge"></div> 🎯 DSH Commander (Planning)</div>
            <div class="agent-item" onclick="selectAgent('hermes-architect')"><div class="agent-badge"></div> 🏛️ Hermes Architect (Systems)</div>
            <div class="agent-item" onclick="selectAgent('dev-automation')"><div class="agent-badge"></div> 💻 Dev Automation (Fullstack)</div>
            <div class="agent-item" onclick="selectAgent('media-producer')"><div class="agent-badge"></div> 🎬 Media Producer (Video AI)</div>
            <div class="agent-item" onclick="selectAgent('openclaw-executor')"><div class="agent-badge"></div> ⚡ OpenClaw Executor (DevOps)</div>
            <div class="agent-item" onclick="selectAgent('jev-sentinel')"><div class="agent-badge"></div> 🛡️ JEV Sentinel (Safety)</div>
            <div class="agent-item" onclick="selectAgent('research-intel')"><div class="agent-badge"></div> 📊 Research Intel (SEO/Market)</div>
            <div class="agent-item" onclick="selectAgent('domain-ops')"><div class="agent-badge"></div> 💼 Domain Ops (Vận Hành)</div>
        </div>
    </div>
    
    <div class="chat-container">
        <div class="chat-header">
            <div class="title" id="chat-title">Phòng điều phối: 🌐 Gateway Ingress (Auto-Route)</div>
            <div class="status"><div class="agent-badge"></div> Online (Model: OpenRouter Auto-Free)</div>
        </div>
        <div class="chat-box" id="chat-box">
            <div class="msg bot">
                <div class="msg-bubble">👋 Xin chào Chủ tịch! Tôi là OMC Command Center. Bạn có thể trò chuyện trực tiếp tại đây, giao việc cho các phòng ban, hoặc chạy chu trình Quad-Engine. Tôi luôn sẵn sàng!</div>
                <div class="msg-meta">Hệ thống • Vừa xong</div>
            </div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="user-input" class="chat-input" placeholder="Gõ tin nhắn hoặc yêu cầu (ví dụ: Viết kịch bản video TikTok hoặc Lập kế hoạch refactor)..." onkeydown="if(event.key==='Enter') sendMessage()">
            <button class="send-btn" id="send-btn" onclick="sendMessage()">Gửi</button>
        </div>
    </div>

    <script>
        let currentAgent = "main";

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
        if self.path in ("/", "/chat", "/index.html"):
            self._send_html(HTML_CHAT_UI)
        elif self.path == "/health":
            self._send_response(200, {"status": "ok", "service": "OMC Webhook & Web Chat Gateway"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(body) if body else {}
        except Exception:
            payload = {}

        if self.path == "/api/chat":
            message = payload.get("message", "")
            agent = payload.get("agent", "main")
            if not message:
                self._send_response(400, {"error": "Thiếu nội dung 'message'"})
                return

            # Đồng bộ Obsidian
            vault = VaultSync(BASE_DIR / "obsidian-vault")
            vault.add_inbox_task(f"WebChat (@{agent})", message, agent)

            # Thực thi qua Quad-Engine
            result = execute_omc_pipeline(message)
            reply = f"✅ Tác vụ '{message[:40]}...' đã được xử lý bởi @{result.get('agent', agent)} qua chu trình Quad-Engine 5 pha."
            self._send_response(200, {"status": "success", "reply": reply, "result": result})

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
    print(f"🌐 OMC WEB CHAT & WEBHOOK GATEWAY ĐANG CHẠY:")
    print(f"👉 Mở trình duyệt Web để Chat: http://localhost:{port}")
    print(f"👉 Cổng nhận Webhook REST API: http://localhost:{port}/webhook/task")
    print("=" * 70)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
