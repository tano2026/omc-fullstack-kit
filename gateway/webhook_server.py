#!/usr/bin/env python3
"""
OMC Webhook Ingress Server
Cổng nhận webhook HTTP REST API cho các hệ thống bên ngoài (Zalo Mini App, CRM, n8n, Stripe).
"""

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

PORT = 19888

class OMCWebhookHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send_response(200, {"status": "ok", "service": "OMC Webhook Gateway"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if self.path == "/webhook/task":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(body)
                task_text = payload.get("task") or payload.get("message") or payload.get("prompt")
                if not task_text:
                    self._send_response(400, {"error": "Missing 'task' parameter"})
                    return
                
                result = execute_omc_pipeline(task_text)
                self._send_response(200, {"status": "success", "result": result})
            except Exception as e:
                self._send_response(500, {"error": str(e)})
        else:
            self._send_response(404, {"error": "Unknown webhook route"})

def run_server(port=PORT):
    server = HTTPServer(("0.0.0.0", port), OMCWebhookHandler)
    print(f"🌐 OMC Webhook Ingress Server đang lắng nghe tại http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
