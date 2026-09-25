#!/usr/bin/env python3
"""
JEV Sentinel - Zero-Damage Safety Guard
Kiểm duyệt toàn bộ lệnh nhạy cảm, ngăn chặn các hành động phá hoại dữ liệu (Zero-Damage).
"""

import re
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+[/~]",
    r"rmdir\s+/s\s+/q\s+[c-zC-Z]:\\",
    r"del\s+/[fF]\s+/[sS]\s+/[qQ]\s+[c-zC-Z]:\\",
    r"drop\s+database",
    r"drop\s+table",
    r"truncate\s+table",
    r"mkfs",
    r":\(\)\{ :\|:& \};:", # fork bomb
    r"dd\s+if=/dev/zero",
    r">\s*/etc/passwd",
    r">\s*/etc/shadow"
]

SENSITIVE_KEY_PATTERNS = [
    r"(sk-[a-zA-Z0-9]{20,})",
    r"(AIzaSy[a-zA-Z0-9_-]{33})",
    r"(\d{8,11}:[a-zA-Z0-9_-]{35})",
    r"(ghp_[a-zA-Z0-9]{36})"
]

class SafetyGuard:
    @staticmethod
    def audit_command(command: str) -> dict:
        """Kiểm duyệt lệnh trước khi cho phép OpenClaw hoặc Agent thực thi"""
        cmd_lower = command.lower()
        
        for pattern in BLOCKED_PATTERNS:
            if re.search(pattern, cmd_lower):
                return {
                    "allowed": False,
                    "reason": f"LỆNH BỊ CHẶN: Phát hiện mẫu phá hoại dữ liệu nguy hiểm ({pattern})",
                    "risk_level": "CRITICAL"
                }
                
        # Check high risk warning
        if any(w in cmd_lower for w in ["drop", "truncate", "del /f", "rm -rf", "reset --hard"]):
            return {
                "allowed": True,
                "reason": "CẢNH BÁO: Lệnh có rủi ro cao, yêu cầu xác nhận thêm hoặc tạo bản sao lưu.",
                "risk_level": "HIGH"
            }
            
        return {
            "allowed": True,
            "reason": "Lệnh an toàn, đáp ứng quy chuẩn Zero-Damage.",
            "risk_level": "LOW"
        }

    @staticmethod
    def redact_secrets(text: str) -> str:
        """Che giấu secret keys trước khi log hoặc xuất ra chat"""
        sanitized = text
        for p in SENSITIVE_KEY_PATTERNS:
            sanitized = re.sub(p, r"***REDACTED_SECRET***", sanitized)
        return sanitized

if __name__ == "__main__":
    test_cmd = "rm -rf /"
    res = SafetyGuard.audit_command(test_cmd)
    print("Test command 'rm -rf /':", res)
