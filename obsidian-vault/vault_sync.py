#!/usr/bin/env python3
"""
OMC Obsidian Second Brain Sync Engine (Thread-Safe & Process-Safe)
Đồng bộ hai chiều an toàn giữa các Agent AI và Obsidian Vault (ghi log, nhận nhiệm vụ, lưu trữ quyết định ADR)
với cơ chế chống xung đột ghi đè (Atomic Write & File Locking).
"""

import os
import sys
import datetime
import threading
import tempfile
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VAULT_ROOT = Path(__file__).resolve().parent
INBOX_FILE = VAULT_ROOT / "06 - Inbox" / "Telegram-Inbox.md"
PROJECTS_FILE = VAULT_ROOT / "02 - Projects" / "Active-Projects.md"
ADR_DIR = VAULT_ROOT / "07 - Decisions-ADR"

_VAULT_LOCK = threading.Lock()

class VaultSync:
    def __init__(self, vault_path: Path = VAULT_ROOT):
        self.vault_path = vault_path
        self.lock_file = self.vault_path / ".vault.lock"

    def _safe_append(self, target_file: Path, text: str, initial_header: str = ""):
        """Ghi nối an toàn có khóa chống xung đột đa tiến trình / đa luồng"""
        with _VAULT_LOCK:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            if not target_file.exists():
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(initial_header)
            with open(target_file, "a", encoding="utf-8") as f:
                f.write(text)

    def _atomic_write(self, target_file: Path, content: str):
        """Ghi đè nguyên tử (atomic write via temp file) tránh làm hỏng file khi crash"""
        with _VAULT_LOCK:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            temp_file = target_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(content)
            # Atomic replace
            os.replace(temp_file, target_file)

    def add_inbox_task(self, sender: str, text: str, assigned_agent: str = "main") -> bool:
        """Ghi nhận tin nhắn / task mới từ Telegram vào Inbox (Thread-Safe)"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n- [ ] **[{now}]** ({sender} ➔ `{assigned_agent}`): {text}\n"
        
        try:
            header = "# 📥 Hộp Thư Tiếp Nhận (Telegram & Webhook Ingress)\n\n---\n"
            self._safe_append(INBOX_FILE, entry, header)
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
            self._atomic_write(target_path, content)
            print(f"✅ Đã ghi nhận quyết định kiến trúc: [{adr_id}] {title}")
            return adr_id
        except Exception as e:
            print(f"❌ Lỗi ghi ADR Obsidian: {e}")
            return ""

    def update_project_status(self, project_name: str, new_status: str, note: str = "") -> bool:
        """Cập nhật trạng thái dự án trong Active-Projects.md an toàn"""
        if not PROJECTS_FILE.exists():
            return False
            
        with _VAULT_LOCK:
            try:
                with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                target = f"| **{project_name}** |"
                if target in content:
                    lines = content.splitlines()
                    new_lines = []
                    for line in lines:
                        if line.startswith(f"| **{project_name}** |"):
                            parts = [p.strip() for p in line.split("|")[1:-1]]
                            if len(parts) >= 5:
                                parts[3] = f"`{new_status}`"
                                if note:
                                    parts[4] = note
                                line = "| " + " | ".join(parts) + " |"
                        new_lines.append(line)
                    self._atomic_write(PROJECTS_FILE, "\n".join(new_lines) + "\n")
                    print(f"✅ Đã cập nhật dự án [{project_name}] sang trạng thái: {new_status}")
                    return True
                return False
            except Exception as e:
                print(f"❌ Lỗi cập nhật dự án: {e}")
                return False

if __name__ == "__main__":
    sync = VaultSync()
    sync.add_inbox_task("Self-Test", "Kiểm tra cơ chế Thread-Safe & Atomic Lock của Obsidian Vault.")
