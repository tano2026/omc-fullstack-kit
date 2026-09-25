#!/usr/bin/env python3
"""
OMC 1-Click Company Cloner
Nhân bản một công ty One-Man Company (OMC) hoàn chỉnh chỉ trong 30 giây!
Bao gồm: Quad-Engine Trio + JEV, 9 Agents, Kho 700+ Skills, Obsidian Second Brain và Telegram Gateway.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KIT_ROOT = Path(__file__).resolve().parent

def clone_company(name: str, domain: str, dest_dir: Path, bot_token: str = ""):
    print("\n" + "=" * 70)
    print(f"🏭 TIẾN HÀNH NHÂN BẢN CÔNG TY OMC: '{name}'")
    print(f"📌 Lĩnh vực: {domain}")
    print(f"📂 Thư mục đích: {dest_dir}")
    print("=" * 70)

    if dest_dir.exists():
        print(f"⚠️ Thư mục '{dest_dir}' đã tồn tại! Vui lòng chọn tên hoặc đường dẫn khác.")
        return False

    dest_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy Engines
    print("📦 1/6. Sao chép bộ lõi Quad-Engine Trio + JEV...")
    shutil.copytree(KIT_ROOT / "engines", dest_dir / "engines")

    # 2. Copy Agents
    print("👥 2/6. Khởi tạo 9 Phòng Ban Chuyên Môn...")
    shutil.copytree(KIT_ROOT / "agents", dest_dir / "agents")

    # 3. Copy Obsidian Vault
    print("📓 3/6. Thiết lập Obsidian Second Brain...")
    shutil.copytree(KIT_ROOT / "obsidian-vault", dest_dir / "obsidian-vault")

    # 4. Copy Skills
    print("🧰 4/6. Nạp Kho 700+ Skills & Central Manager...")
    shutil.copytree(KIT_ROOT / "skills", dest_dir / "skills")

    # 5. Copy Gateway
    print("🌐 5/6. Thiết lập Cổng Ingress & Webhook...")
    shutil.copytree(KIT_ROOT / "gateway", dest_dir / "gateway")

    # Copy installer files, launchers & configs
    launcher_files = [
        "requirements.txt", "package.json", "install.bat", "install.sh", 
        "INSTALL_GUIDE.md", "README.md", "AGENTS.md", "ecosystem.config.js",
        "copilot.bat", "copilot.sh", "start.bat", "start.sh",
        "chat.bat", "chat.sh", "dev-superpowers.bat", "dev-superpowers.sh",
        "hermes-chat.bat", "hermes-chat.sh", "hermes-dashboard.bat", "hermes-dashboard.sh",
        "openclaw-dashboard.bat", "openclaw-dashboard.sh", "openclaw-chat.bat", "openclaw-chat.sh"
    ]
    for f in launcher_files:
        src_f = KIT_ROOT / f
        if src_f.exists():
            shutil.copy2(src_f, dest_dir / f)

    # 6. Customize Company Profile & Second Brain
    print("✍️ 6/6. Tùy biến thông số doanh nghiệp...")
    profile_path = dest_dir / "obsidian-vault" / "01 - Org" / "Company-Profile.md"
    if profile_path.exists():
        with open(profile_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("{{COMPANY_NAME}}", name).replace("{{COMPANY_DOMAIN}}", domain)
        with open(profile_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Customize domain-ops agent
    domain_identity = dest_dir / "agents" / "domain-ops" / "IDENTITY.md"
    if domain_identity.exists():
        with open(domain_identity, "r", encoding="utf-8") as f:
            c = f.read()
        c = c.replace("Business & Industry Operations Specialist", f"{domain} Operations Specialist")
        with open(domain_identity, "w", encoding="utf-8") as f:
            f.write(c)

    # Create config/.env
    config_dir = dest_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    env_content = f"""# OMC Company Configuration
COMPANY_NAME={name}
COMPANY_DOMAIN={domain}
TELEGRAM_BOT_TOKEN={bot_token}
OPENROUTER_API_KEY=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
DEFAULT_MODEL=openrouter/free
"""
    with open(config_dir / ".env", "w", encoding="utf-8") as f:
        f.write(env_content)

    # Create Start scripts
    start_bat_content = f"""@echo off
title OMC Company - {name}
echo ========================================================
echo   KHOI DONG HE THONG OMC: {name} ({domain})
echo ========================================================
python engines/trio_orchestrator.py "Khoi dong he thong van hanh cho {name}"
echo.
echo Dang khoi chay Telegram Ingress Gateway...
python gateway/telegram_gateway.py
pause
"""
    with open(dest_dir / "start.bat", "w", encoding="utf-8") as f:
        f.write(start_bat_content)

    start_sh_content = f"""#!/bin/bash
echo "========================================================"
echo "  KHOI DONG HE THONG OMC: {name} ({domain})"
echo "========================================================"
python3 engines/trio_orchestrator.py "Khoi dong he thong van hanh cho {name}"
python3 gateway/telegram_gateway.py
"""
    with open(dest_dir / "start.sh", "w", encoding="utf-8") as f:
        f.write(start_sh_content)
    try:
        os.chmod(dest_dir / "start.sh", 0o755)
    except Exception:
        pass

    # Create Copilot scripts
    copilot_bat_content = f"""@echo off
title Hermes OMC Master Copilot - {name}
python "%~dp0engines\\hermes_reasoner\\hermes_copilot.py"
pause
"""
    with open(dest_dir / "copilot.bat", "w", encoding="utf-8") as f:
        f.write(copilot_bat_content)

    copilot_sh_content = f"""#!/bin/bash
DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" >/dev/null 2>&1 && pwd )"
python3 "$DIR/engines/hermes_reasoner/hermes_copilot.py"
"""
    with open(dest_dir / "copilot.sh", "w", encoding="utf-8") as f:
        f.write(copilot_sh_content)
    try:
        os.chmod(dest_dir / "copilot.sh", 0o755)
    except Exception:
        pass

    # Create README in cloned company
    cloned_readme = f"""# 🏢 {name} - One-Man Company (OMC)

> Lĩnh vực: **{domain}**
> Vận hành bởi: **OMC Quad-Engine (DSH + Hermes + OpenClaw + JEV)** kết hợp **Obsidian Second Brain**.

---

## 🚀 Khởi Chạy
- **Trên Windows:** Click đúp vào `start.bat`
- **Trên Linux/VPS:** Chạy lệnh `./start.sh`

## 👥 9 Phòng Ban Chuyên Môn
1. `main`: Cổng định tuyến JEV Ingress Gateway
2. `dsh-commander`: Lập kế hoạch mục tiêu DAG
3. `hermes-architect`: Thiết kế kiến trúc & code phức tạp
4. `dev-automation`: Kỹ sư Full-Stack & Bot Automation
5. `media-producer`: Kịch bản video viral & media AI
6. `openclaw-executor`: Thực thi terminal & DevOps 24/7
7. `jev-sentinel`: Rào chắn phòng thủ an toàn Zero-Damage
8. `research-intel`: Nghiên cứu thị trường & SEO/AEO
9. `domain-ops`: Chuyên gia nghiệp vụ chuyên sâu cho `{domain}`

## 📓 Quản Trị Tri Thức
Mở thư mục `obsidian-vault/` bằng ứng dụng **Obsidian** để xem sơ đồ tổ chức, dự án, nhật ký và sổ cái quyết định ADR.
"""
    with open(dest_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(cloned_readme)

    print("\n" + "=" * 70)
    print(f"🎉 NHÂN BẢN THÀNH CÔNG CÔNG TY '{name}' TẠI:")
    print(f"👉 {dest_dir}")
    print("=" * 70 + "\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="OMC 1-Click Company Cloner")
    parser.add_argument("--name", required=True, type=str, help="Tên công ty mới (VD: AnBinhAir, TanoDigital)")
    parser.add_argument("--domain", required=True, type=str, help="Lĩnh vực kinh doanh (VD: Airport Services, Marketing Agency)")
    parser.add_argument("--dest", type=str, default="", help="Đường dẫn thư mục lưu trữ (mặc định: platform/companies/<name>)")
    parser.add_argument("--bot-token", type=str, default="", help="Token bot Telegram dành riêng cho công ty này (tùy chọn)")

    args = parser.parse_args()
    if args.dest:
        dest_dir = Path(args.dest)
    else:
        dest_dir = KIT_ROOT.parent / "companies" / args.name

    clone_company(args.name, args.domain, dest_dir, args.bot_token)

if __name__ == "__main__":
    main()
