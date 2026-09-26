"""
Multi-Brand Manager & Client Onboarding Engine for OMC Fullstack Kit.
Empowers an Agency to manage multiple brand profiles (Knowledge, Pricing, FAQs) seamlessly from one dashboard.
"""

import os
import sys
import re
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


BASE_DIR = Path(__file__).resolve().parent.parent
BRANDS_DIR = BASE_DIR / "brands"
ACTIVE_BRAND_FILE = BRANDS_DIR / ".active_brand"

def init_default_brands():
    """Initializes default brand directories if not present."""
    BRANDS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Tano Agency
    tano_dir = BRANDS_DIR / "tano-agency"
    if not tano_dir.exists():
        tano_dir.mkdir(parents=True, exist_ok=True)
        config = {
            "id": "tano-agency",
            "name": "Tano Agency & AI Automation",
            "industry": "Digital Marketing & AI Automation",
            "hotline": "0988.888.999",
            "color": "#1f6feb",
            "core_offer": "Hệ thống AI Tự Hành & Marketing Automation cho Doanh Nghiệp"
        }
        with open(tano_dir / "config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    # 2. An Binh Airport & Travel
    anbinh_dir = BRANDS_DIR / "an-binh-travel"
    if not anbinh_dir.exists():
        anbinh_dir.mkdir(parents=True, exist_ok=True)
        config = {
            "id": "an-binh-travel",
            "name": "An Bình Air Services & Travel",
            "industry": "Dịch Vụ Đón Tiễn Sân Bay & Fast Track VIP",
            "hotline": "0912.345.678",
            "color": "#2ea043",
            "core_offer": "Fast Track Ga Quốc Tế/Nội Địa, Xe Đưa Đón VIP, Phòng Chờ Thương Gia"
        }
        with open(anbinh_dir / "config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    # 3. Spa Hoa Mai
    spa_dir = BRANDS_DIR / "spa-hoa-mai"
    if not spa_dir.exists():
        spa_dir.mkdir(parents=True, exist_ok=True)
        config = {
            "id": "spa-hoa-mai",
            "name": "Thẩm Mỹ Viện & Spa Hoa Mai",
            "industry": "Chăm Sóc Da Chuyên Sâu & Điều Trị Mụn Laser",
            "hotline": "0977.112.233",
            "color": "#f85149",
            "core_offer": "Phác Đồ Trị Mụn Laser Y Khoa, Trẻ Hóa Da, Phục Hồi Hàng Rào Bảo Vệ Da"
        }
        with open(spa_dir / "config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    if not ACTIVE_BRAND_FILE.exists():
        set_active_brand("tano-agency")

def list_brands() -> List[Dict[str, Any]]:
    """Returns a list of all available brands."""
    init_default_brands()
    active_id = get_active_brand_id()
    brands = []
    for d in BRANDS_DIR.iterdir():
        if d.is_dir() and not d.name.startswith("."):
            cfg_file = d / "config.json"
            if cfg_file.exists():
                try:
                    with open(cfg_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        data["is_active"] = (data.get("id") == active_id)
                        brands.append(data)
                except Exception:
                    pass
    return brands

def get_active_brand_id() -> str:
    """Returns the ID of the currently active brand."""
    if ACTIVE_BRAND_FILE.exists():
        try:
            with open(ACTIVE_BRAND_FILE, "r", encoding="utf-8") as f:
                val = f.read().strip()
                if val:
                    return val
        except Exception:
            pass
    return "tano-agency"

def get_active_brand() -> Dict[str, Any]:
    """Returns the full metadata of the active brand."""
    active_id = get_active_brand_id()
    for b in list_brands():
        if b.get("id") == active_id:
            return b
    return list_brands()[0] if list_brands() else {"id": "default", "name": "Default"}

def set_active_brand(brand_id: str) -> bool:
    """Switches the active brand."""
    b_dir = BRANDS_DIR / brand_id
    if not b_dir.exists():
        return False
    with open(ACTIVE_BRAND_FILE, "w", encoding="utf-8") as f:
        f.write(brand_id)
    return True

def create_brand(
    name: str,
    industry: str,
    hotline: str,
    core_offer: str,
    pricing_starter: str = "1.990.000đ",
    pricing_pro: str = "4.990.000đ",
    pricing_vip: str = "12.500.000đ"
) -> Dict[str, Any]:
    """
    1-Click Brand Creation:
    Generates brand directory, configuration, and tailored knowledge files.
    """
    init_default_brands()
    # Generate clean ID slug
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        slug = f"brand-{len(list_brands()) + 1}"

    brand_dir = BRANDS_DIR / slug
    brand_dir.mkdir(parents=True, exist_ok=True)

    config = {
        "id": slug,
        "name": name.strip(),
        "industry": industry.strip(),
        "hotline": hotline.strip(),
        "color": "#1f6feb",
        "core_offer": core_offer.strip(),
        "pricing": {
            "starter": pricing_starter,
            "pro": pricing_pro,
            "vip": pricing_vip
        }
    }

    with open(brand_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # 1. Brand Soul
    with open(brand_dir / "01-Brand-Soul.md", "w", encoding="utf-8") as f:
        f.write(f"# 🌟 BẢN SẮC THƯƠNG HIỆU: {name.upper()}\n\n")
        f.write(f"- **Lĩnh vực:** {industry}\n")
        f.write(f"- **Hotline/Zalo:** {hotline}\n")
        f.write(f"- **Định vị cốt lõi:** {core_offer}\n")
        f.write(f"- **Tone of Voice:** Lịch thiệp, chuyên nghiệp, tận tâm, cam kết bằng kết quả thực tế.\n")

    # 2. Products Pricing
    with open(brand_dir / "02-Products-Pricing.md", "w", encoding="utf-8") as f:
        f.write(f"# 💰 BẢNG GIÁ DỊCH VỤ CHUẨN: {name.upper()}\n\n")
        f.write(f"| Mã | Tên Gói | Giá Niêm Yết | Giá Ưu Đãi | Quyền Lợi |\n")
        f.write(f"| :---: | :--- | :---: | :---: | :--- |\n")
        f.write(f"| **P-01** | Gói Khởi Điểm (Starter) | -- | {pricing_starter} | Trải nghiệm dịch vụ cơ bản |\n")
        f.write(f"| **P-02** | Gói Tiêu Chuẩn (Pro - Khuyên dùng) | -- | {pricing_pro} | Đầy đủ quyền lợi + Tặng quà 1.5tr |\n")
        f.write(f"| **P-03** | Gói VIP All-In-One | -- | {pricing_vip} | Phục vụ 1-1 Chuyên gia trưởng, bảo hành dài hạn |\n")

    # Set as active
    set_active_brand(slug)

    return {
        "status": "success",
        "brand": config,
        "message": f"Đã khởi tạo thương hiệu '{name}' thành công! Toàn bộ Bot và Studio đã được chuyển sang thương hiệu này."
    }

if __name__ == "__main__":
    init_default_brands()
    print("Available Brands:", [b["name"] for b in list_brands()])
    print("Active Brand:", get_active_brand()["name"])
