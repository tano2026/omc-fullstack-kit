#!/usr/bin/env python3
"""
OMC 1-Click Company Cloner & Client Provisioning Engine
Nhân bản một công ty One-Man Company (OMC) hoàn chỉnh chỉ trong 30 giây!
Hỗ trợ 2 chế độ:
1. Standard OMC: Bộ 9 phòng ban nội bộ đầy đủ.
2. SME Client Pack (--template sme-client): Bộ 5 Agent chuyên biệt bàn giao cho khách hàng SME/Cá nhân.
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

def clone_company(name: str, domain: str, dest_dir: Path, bot_token: str = "", template: str = "standard"):
    print("\n" + "=" * 70)
    print(f"🏭 TIẾN HÀNH NHÂN BẢN CÔNG TY OMC: '{name}' (Template: {template})")
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
    print("👥 2/6. Khởi tạo Bộ Máy Phòng Ban Chuyên Môn...")
    shutil.copytree(KIT_ROOT / "agents", dest_dir / "agents")

    # If SME Client template, inject the 5 specialized client agents
    sme_pack_dir = KIT_ROOT / "templates" / "sme-client-pack"
    if template == "sme-client" and sme_pack_dir.exists():
        print("   🌟 Nạp Biệt Đội 5 Agent Chuyên Biệt Cho Khách Hàng SME:")
        sme_agents = sme_pack_dir / "agents"
        if sme_agents.exists():
            for agent_dir in sme_agents.iterdir():
                if agent_dir.is_dir():
                    target_agent = dest_dir / "agents" / agent_dir.name
                    if target_agent.exists():
                        shutil.rmtree(target_agent)
                    shutil.copytree(agent_dir, target_agent)
                    print(f"      • @{agent_dir.name}")

    # 3. Copy Obsidian Vault
    print("📓 3/6. Thiết lập Obsidian Second Brain...")
    shutil.copytree(KIT_ROOT / "obsidian-vault", dest_dir / "obsidian-vault")

    # If SME Client template, inject the 3 core Knowledge files
    if template == "sme-client" and sme_pack_dir.exists():
        print("   📄 Nạp Bộ 3 File Tri Thức Mẫu (Brand Soul, Products, FAQ)...")
        sme_knowledge = sme_pack_dir / "knowledge"
        dest_knowledge = dest_dir / "obsidian-vault" / "04 - Knowledge"
        dest_knowledge.mkdir(parents=True, exist_ok=True)
        if sme_knowledge.exists():
            for kf in sme_knowledge.glob("*.md"):
                with open(kf, "r", encoding="utf-8") as f:
                    k_content = f.read()
                k_content = k_content.replace("{{BRAND_NAME}}", name).replace("{{FOUNDER_NAME}}", "Chủ Doanh Nghiệp").replace("{{INDUSTRY}}", domain)
                with open(dest_knowledge / kf.name, "w", encoding="utf-8") as f:
                    f.write(k_content)

    # 4. Copy Skills
    print("🧰 4/6. Nạp Kho 720+ Skills & Central Taxonomy...")
    shutil.copytree(KIT_ROOT / "skills", dest_dir / "skills")

    # 5. Copy Gateway
    print("🌐 5/6. Thiết lập Cổng Ingress, Web Chat & Webhook...")
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

    if template == "sme-client" and sme_pack_dir.exists():
        for sf in ["start-client.bat", "start-client.sh"]:
            src_sf = sme_pack_dir / sf
            if src_sf.exists():
                shutil.copy2(src_sf, dest_dir / sf)

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

    # Create README in cloned company
    cloned_readme = f"""# 🏢 {name} - One-Man Company (OMC)

> Lĩnh vực: **{domain}**
> Template: **{template}**
> Vận hành bởi: **OMC Quad-Engine (DSH + Hermes + OpenClaw + JEV)** kết hợp **Obsidian Second Brain**.

---

## 🚀 Khởi Chạy
- **Bàn giao cho Khách hàng SME:** Click đúp vào `start-client.bat`
- **Mở giao diện Web Chat:** Click đúp vào `chat.bat` (hoặc truy cập http://localhost:19888)
- **Kích hoạt Telegram Gateway:** Click đúp vào `start.bat`

## 👥 Biệt Đội Nhân Sự AI Chuyên Trách
1. `@cskh-consultant`: Chuyên viên Tư vấn & Chốt Đơn 24/7 (phản xạ 10ms, trích xuất bảng giá chuẩn)
2. `@social-creator`: Đạo diễn Kịch bản Video & Bài viết Social (Hook 3s, giữ Brand Soul)
3. `@market-spy`: Thám tử Đối thủ & Xu hướng 30 ngày (`last30days`)
4. `@ceo-copilot`: Thư ký riêng cho Chủ SME (Báo cáo 8h sáng & 8h tối)
5. `@brand-guard`: Rào chắn an toàn bảo vệ uy tín thương hiệu (Zero-Damage)

## 📓 Tri Thức Doanh Nghiệp (Obsidian Second Brain)
Mở thư mục `obsidian-vault/` bằng ứng dụng **Obsidian**:
- `04 - Knowledge/01-Brand-Soul.md`: Câu chuyện thương hiệu & Tone of Voice
- `04 - Knowledge/02-Products-Pricing.md`: Danh mục sản phẩm & Bảng giá
- `04 - Knowledge/03-FAQ-Objections.md`: 25 kịch bản xử lý từ chối
"""
    with open(dest_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(cloned_readme)

    print("\n" + "=" * 70)
    print(f"🎉 NHÂN BẢN THÀNH CÔNG CÔNG TY '{name}' TẠI:")
    print(f"👉 {dest_dir}")
    print("=" * 70 + "\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="OMC 1-Click Company Cloner & Provisioner")
    parser.add_argument("--name", required=True, type=str, help="Tên công ty mới (VD: SpaThuyTien, AnBinhAir)")
    parser.add_argument("--domain", required=True, type=str, help="Lĩnh vực kinh doanh (VD: Spa & Skincare, Du lịch sân bay)")
    parser.add_argument("--dest", type=str, default="", help="Đường dẫn thư mục lưu trữ")
    parser.add_argument("--bot-token", type=str, default="", help="Token bot Telegram dành riêng cho công ty này (tùy chọn)")
    parser.add_argument("--template", type=str, choices=["standard", "sme-client"], default="standard", help="Template công ty: standard (OMC nội bộ) hoặc sme-client (Bàn giao cho khách hàng)")

    args = parser.parse_args()
    if args.dest:
        dest_dir = Path(args.dest)
    else:
        dest_dir = KIT_ROOT.parent / "companies" / args.name

    clone_company(args.name, args.domain, dest_dir, args.bot_token, args.template)

if __name__ == "__main__":
    main()
