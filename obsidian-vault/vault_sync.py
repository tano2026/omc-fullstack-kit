#!/usr/bin/env python3
"""
OMC Obsidian Second Brain Sync Engine
Đồng bộ hai chiều giữa các Agent AI và Obsidian Vault (ghi log, nhận nhiệm vụ, lưu trữ quyết định ADR).
"""

import os
import sys
import datetime
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VAULT_ROOT = Path(__file__).resolve().parent
INBOX_FILE = VAULT_ROOT / "06 - Inbox" / "Telegram-Inbox.md"
PROJECTS_FILE = VAULT_ROOT / "02 - Projects" / "Active-Projects.md"
ADR_DIR = VAULT_ROOT / "07 - Decisions-ADR"

class VaultSync:
    def __init__(self, vault_path: Path = VAULT_ROOT):
        self.vault_path = vault_path

    def add_inbox_task(self, sender: str, text: str, assigned_agent: str = "main") -> bool:
        """Ghi nhận tin nhắn / task mới từ Telegram vào Inbox"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n- [ ] **[{now}]** ({sender} ➔ `{assigned_agent}`): {text}\n"
        
        try:
            if not INBOX_FILE.exists():
                INBOX_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(INBOX_FILE, "w", encoding="utf-8") as f:
                    f.write("# 📥 Hộp Thư Tiếp Nhận (Telegram & Webhook Ingress)\n\n---\n")
                    
            with open(INBOX_FILE, "a", encoding="utf-8") as f:
                f.write(entry)
            print(f"✅ Đã ghi nhận task vào Obsidian Inbox: [{assigned_agent}] {text[:40]}...")
            return True
        except Exception as e:
            print(f"❌ Lỗi ghi Inbox Obsidian: {e}")
            return False

    def record_decision(self, title: str, author: str, decision_text: str, context: str = "") -> str:
        """Tạo một file Architecture Decision Record (ADR) mới trong 07 - Decisions-ADR"""
        now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        existing_adrs = list(ADR_DIR.glob("ADR-*.md"))
        next_num = len(existing_adrs) + 1
        adr_id = f"ADR-{next_num:03d}"
        
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "-")
        filename = f"{adr_id}-{safe_title}.md"
        target_path = ADR_DIR / filename
        
        content = f"""# 🏛️ {adr_id}: {title}

- **Trạng thái:** Đã phê duyệt (Approved)
- **Tác giả:** {author}
- **Ngày:** {now_date}

## 1. Ngữ cảnh
{context or "Quyết định kỹ thuật hoặc vận hành được thông qua bởi CEO và Agent."}

## 2. Quyết định
{decision_text}

## 3. Hệ quả & Cam kết
- Tự động ghi nhận vào sổ cái Obsidian Second Brain.
- Tất cả các Agent đọc và tuân thủ theo quyết định này.
"""
        try:
            ADR_DIR.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Đã lưu quyết định kiến trúc: {filename}")
            return str(target_path)
        except Exception as e:
            print(f"❌ Lỗi ghi ADR Obsidian: {e}")
            return ""

    def update_project_status(self, task_name: str, status: str = "done") -> bool:
        """Cập nhật trạng thái task trong Active-Projects.md"""
        if not PROJECTS_FILE.exists():
            return False
            
        try:
            with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            new_lines = []
            updated = False
            for line in lines:
                if task_name.lower() in line.lower():
                    if status == "done" and "[ ]" in line:
                        line = line.replace("[ ]", "[x]")
                        updated = True
                    elif status == "progress" and "[ ]" in line:
                        line = line.replace("[ ]", "[/]")
                        updated = True
                new_lines.append(line)
                
            if updated:
                with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"✅ Đã cập nhật trạng thái dự án trong Obsidian: '{task_name}' -> {status}")
            return updated
        except Exception as e:
            print(f"❌ Lỗi cập nhật dự án Obsidian: {e}")
            return False

if __name__ == "__main__":
    sync = VaultSync()
    sync.add_inbox_task("User (Test)", "Kiểm thử hệ thống đồng bộ Obsidian Second Brain", "main")
    sync.record_decision("Chuẩn hóa định dạng Markdown cho Vault", "Hermes Architect", "Mọi ghi chú trong Vault phải tuân thủ chuẩn CommonMark và Mermaid diagrams.")
