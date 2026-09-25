#!/usr/bin/env python3
"""
JEV Sentinel - Zero-Damage Advanced Safety Guard & Secret Sanitizer
Kiểm duyệt toàn bộ lệnh nhạy cảm, ngăn chặn phá hoại dữ liệu (Zero-Damage), 
chống rò rỉ API credentials và bảo vệ hệ điều hành Windows/Linux.
"""

import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BLOCKED_PATTERNS = [
    # Linux destructive
    r"rm\s+-rf\s+[/~]",
    r"mkfs",
    r":\(\)\{ :\|:& \};:", # fork bomb
    r"dd\s+if=/dev/zero",
    r">\s*/etc/passwd",
    r">\s*/etc/shadow",
    r"chmod\s+-R\s+777\s+/",
    
    # Windows destructive
    r"rmdir\s+/[sS]\s+/[qQ]\s+[c-zC-Z]:\\",
    r"del\s+/[fF]\s+/[sS]\s+/[qQ]\s+[c-zC-Z]:\\",
    r"format\s+[c-zC-Z]:",
    r"diskpart",
    r"reg\s+delete\s+HK",
    r"Set-ExecutionPolicy\s+(Bypass|Unrestricted)",
    r"Disable-NetFirewallRule",
    
    # Database destructive
    r"drop\s+database",
    r"drop\s+table",
    r"truncate\s+table",
    
    # Git catastrophic
    r"git\s+push\s+.*--force\s+.*(main|master)",
    r"git\s+push\s+-f\s+.*(main|master)",
    r"git\s+reset\s+--hard\s+HEAD~"
]

SENSITIVE_KEY_PATTERNS = [
    (r"(sk-[a-zA-Z0-9]{20,})", "sk-***REDACTED***"),
    (r"(AIzaSy[a-zA-Z0-9_-]{33})", "AIzaSy***REDACTED***"),
    (r"(\d{8,11}:[a-zA-Z0-9_-]{35})", "***TELEGRAM_BOT_TOKEN_REDACTED***"),
    (r"(ghp_[a-zA-Z0-9]{36})", "ghp_***REDACTED***"),
    (r"(github_pat_[a-zA-Z0-9_]{60,})", "github_pat_***REDACTED***"),
    (r"(openrouter-[a-zA-Z0-9_-]{30,})", "openrouter-***REDACTED***")
]

class SafetyGuard:
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Tự động che giấu (mask) API token, password và credentials nhạy cảm khỏi log"""
        if not text:
            return ""
        sanitized = text
        for pattern, replacement in SENSITIVE_KEY_PATTERNS:
            sanitized = re.sub(pattern, replacement, sanitized)
        return sanitized

    @staticmethod
    def audit_command(command: str) -> dict:
        """Kiểm duyệt lệnh trước khi cho phép OpenClaw hoặc Agent thực thi"""
        cmd_lower = command.lower()
        
        # 1. Kiểm tra mẫu lệnh cấm tuyệt đối (CRITICAL)
        for pattern in BLOCKED_PATTERNS:
            if re.search(pattern, cmd_lower):
                return {
                    "allowed": False,
                    "reason": f"LỆNH BỊ CHẶN: Phát hiện mẫu phá hoại dữ liệu nguy hiểm ({pattern})",
                    "risk_level": "CRITICAL"
                }
                
        # 2. Kiểm tra rủi ro cao (HIGH)
        high_risk_keywords = [
            "drop table", "truncate", "del /f", "rm -rf", "reset --hard", 
            "npm publish", "pip install -e", "docker system prune -a"
        ]
        if any(w in cmd_lower for w in high_risk_keywords):
            return {
                "allowed": True,
                "reason": "CẢNH BÁO: Lệnh có rủi ro cao, yêu cầu xác nhận thêm hoặc tạo bản sao lưu.",
                "risk_level": "HIGH"
            }
            
        # 3. Lệnh an toàn
        return {
            "allowed": True,
            "reason": "Lệnh an toàn, đáp ứng quy chuẩn Zero-Damage.",
            "risk_level": "LOW"
        }

    @staticmethod
    def check_env_security(env_path: Path) -> dict:
        """Kiểm tra độ an toàn của file biến môi trường .env"""
        if not env_path.exists():
            return {"status": "ok", "message": "Không tìm thấy file .env (sử dụng biến hệ thống)"}
            
        with open(env_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            
        issues = []
        if "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" in content:
            issues.append("Telegram Bot Token chưa được cấu hình (vẫn là placeholder).")
        if "OPENROUTER_API_KEY=your_openrouter_api_key_here" in content:
            issues.append("OpenRouter API Key chưa được cấu hình.")
            
        if issues:
            return {"status": "warning", "issues": issues}
        return {"status": "ok", "message": "Cấu hình .env hợp lệ và an toàn."}

if __name__ == "__main__":
    test_cmd = sys.argv[1] if len(sys.argv) > 1 else "git status"
    res = SafetyGuard.audit_command(test_cmd)
    print(f"Lệnh: {test_cmd}")
    print(f"Allowed: {res['allowed']} | Risk: {res['risk_level']} | Lý do: {res['reason']}")
    
    # Test sanitization
    secret_str = "Test key sk-1234567890abcdef1234567890 and bot token 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ_1234567"
    print("\nSanitize Test:")
    print(SafetyGuard.sanitize_text(secret_str))
