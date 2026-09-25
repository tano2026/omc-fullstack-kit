#!/usr/bin/env python3
"""
OMC Skill Classifier & Taxonomy Generator
Quét toàn bộ 720+ skills trong kho (core + vault), phân loại theo 10 nhóm chức năng và ngành nghề thực chiến,
sinh ra SKILL_TAXONOMY.json và cẩm nang tra cứu CATEGORIES.md để Hermes Master có thể tư vấn mở công ty.
"""

import os
import sys
import json
import re
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = BASE_DIR / "skills"
CORE_DIR = SKILLS_DIR / "core"
VAULT_DIR = SKILLS_DIR / "vault"

TAXONOMY_DEF = {
    "marketing-growth-seo": {
        "title": "📈 Marketing, SEO & Tăng Trưởng (Growth)",
        "description": "Nghiên cứu đối thủ, tối ưu SEO/AEO/GEO, viết bài quảng cáo, email marketing, affiliate và phễu chuyển đổi.",
        "keywords": ["seo", "marketing", "growth", "copywriting", "email", "affiliate", "ad", "ads", "social", "competitor", "conversion", "brand", "audience", "traffic", "geo", "aeo"]
    },
    "media-content-creation": {
        "title": "🎬 Sáng Tạo Nội Dung & Video AI (Media Production)",
        "description": "Biên kịch video ngắn TikTok/Reels/Shorts, kịch bản YouTube, tạo ảnh Midjourney, podcast và viral hooks.",
        "keywords": ["video", "media", "youtube", "tiktok", "reels", "audio", "podcast", "hook", "story", "content", "script", "creative", "film", "voice", "thumbnail"]
    },
    "travel-hospitality-logistics": {
        "title": "✈️ Du Lịch, Khách Sạn & Vận Tải (Travel & Logistics)",
        "description": "Nghiệp vụ đón tiễn sân bay (Fast Track, VIP Lounge), đặt vé máy bay, khách sạn, tour du lịch, hải quan và vận tải.",
        "keywords": ["travel", "airport", "flight", "hotel", "tour", "booking", "trip", "hospitality", "carrier", "customs", "ground-handling", "visa", "itinerary", "passenger"]
    },
    "ecommerce-retail-sales": {
        "title": "🛍️ Thương Mại Điện Tử & Bán Lẻ (E-Commerce & Retail)",
        "description": "Vận hành gian hàng Shopee/Shopify/Amazon, quản lý giỏ hàng, cổng thanh toán, dropshipping và tối ưu đơn hàng.",
        "keywords": ["shop", "commerce", "store", "cart", "product", "checkout", "retail", "stripe", "amazon", "shopee", "dropship", "merchant", "inventory", "sales"]
    },
    "finance-fintech-crypto": {
        "title": "💰 Tài Chính, Kế Toán & Web3/Crypto (Finance & Ops)",
        "description": "Phân tích tài chính, quản lý dòng tiền, hóa đơn kế toán, hợp đồng thông minh crypto, DeFi và theo dõi chi phí.",
        "keywords": ["finance", "money", "crypto", "defi", "invest", "stock", "tax", "accounting", "invoice", "cost", "billing", "revenue", "budget", "pricing", "tokenomics"]
    },
    "saas-frontend-uiux": {
        "title": "🎨 Giao Diện Người Dùng & UI/UX (Frontend Engineering)",
        "description": "Thiết kế component web, dashboard, responsive UI, Tailwind, React, Vue, Next.js, Flutter và thẩm mỹ giao diện.",
        "keywords": ["frontend", "ui", "ux", "design", "css", "tailwind", "react", "vue", "nextjs", "component", "dashboard", "layout", "mobile", "flutter", "animation", "motion"]
    },
    "saas-backend-data": {
        "title": "⚙️ Lập Trình Backend, API & Cơ Sở Dữ Liệu (Backend & DB)",
        "description": "Thiết kế API REST/GraphQL, FastAPI, Node.js, Python, kiến trúc microservices, PostgreSQL, MongoDB và xử lý dữ liệu.",
        "keywords": ["backend", "api", "database", "sql", "postgres", "mongo", "redis", "fastapi", "python", "node", "django", "express", "graphql", "crud", "orm", "data-science"]
    },
    "automation-rpa-crawlers": {
        "title": "🤖 Tự Động Hóa, RPA & Cào Dữ Liệu (Automation & Bots)",
        "description": "Bot Telegram/Zalo, RPA tự động hóa quy trình, crawler cào dữ liệu web, browser automation Playwright và tích hợp Webhook.",
        "keywords": ["automation", "bot", "crawl", "scrape", "rpa", "telegram", "zalo", "whatsapp", "webhook", "playwright", "puppeteer", "browser", "selenium", "scraper", "feed"]
    },
    "security-devops-cloud": {
        "title": "🛡️ Bảo Mật, DevOps & Hạ Tầng Điện Toán Đám Mây (Infra & Security)",
        "description": "Kiểm thử bảo mật Zero-Damage, phòng chống lỗ hổng OWASP, Docker, Kubernetes, CI/CD, Linux server và giám sát hệ thống.",
        "keywords": ["security", "docker", "k8s", "kubernetes", "cloud", "linux", "deploy", "ci-cd", "devops", "git", "auth", "audit", "monitor", "hardening", "vulnerability"]
    },
    "ai-agents-orchestration": {
        "title": "🧠 Kỹ Thuật AI Agents, Harness & Điều Phối (AI Engineering)",
        "description": "Xây dựng AI Agent tự hành, bộ khung Harness, vòng lặp đánh giá Eval, Prompt Engineering, RAG và phối hợp Multi-Agent.",
        "keywords": ["agent", "harness", "eval", "prompt", "llm", "rag", "cot", "reasoning", "cognitive", "hermes", "orchestrat", "autonomous", "superpowers", "council", "trio"]
    }
}

INDUSTRY_BUNDLES = {
    "travel-agency": {
        "industry_name": "Công ty Du Lịch, Đón Tiễn Sân Bay & Vé Máy Bay",
        "recommended_groups": ["travel-hospitality-logistics", "marketing-growth-seo", "automation-rpa-crawlers", "media-content-creation"],
        "highlight_skills": ["airport-ops", "customs-trade-compliance", "competitive-intel-ground-handling", "carrier-relationship-management", "last30days", "viral-hooks", "humanizer"]
    },
    "media-agency": {
        "industry_name": "Agency Truyền Thông, Sáng Tạo Nội Dung & Video AI",
        "recommended_groups": ["media-content-creation", "marketing-growth-seo", "automation-rpa-crawlers"],
        "highlight_skills": ["video-production-pipeline", "viral-hooks", "content-strategy", "copywriting", "deck-generator", "data-storytelling", "last30days"]
    },
    "ecommerce-brand": {
        "industry_name": "Công ty Bán Lẻ, Thương Mại Điện Tử & D2C",
        "recommended_groups": ["ecommerce-retail-sales", "marketing-growth-seo", "media-content-creation", "automation-rpa-crawlers"],
        "highlight_skills": ["customer-billing-ops", "conversion-ops", "brand-voice", "cold-email", "affiliate-skills", "viral-hooks"]
    },
    "software-saas": {
        "industry_name": "Công ty Công Nghệ, SaaS & Giải Pháp Phần Mềm",
        "recommended_groups": ["saas-frontend-uiux", "saas-backend-data", "security-devops-cloud", "ai-agents-orchestration"],
        "highlight_skills": ["superpowers", "harness-engineering", "test-driven-dev", "spec-driven-development", "api-and-interface-design", "frontend-ui-engineering", "security-hardening"]
    },
    "automation-service": {
        "industry_name": "Công ty Cung Cấp Giải Pháp Tự Động Hóa & RPA",
        "recommended_groups": ["automation-rpa-crawlers", "saas-backend-data", "security-devops-cloud"],
        "highlight_skills": ["data-scraper-agent", "browser-qa", "expert-coding-dev", "terminal-ops", "ci-cd-and-automation"]
    },
    "consulting-finance": {
        "industry_name": "Công ty Tư Vấn Chiến Lược, Tài Chính & Đầu Tư",
        "recommended_groups": ["finance-business-ops", "marketing-growth-seo", "ai-agents-orchestration"],
        "highlight_skills": ["ceo-decision-lens", "business-guru", "council", "competitive-intel", "cost-tracking", "deep-research"]
    }
}

def extract_meta(path: Path) -> dict:
    target = path / "SKILL.md" if path.is_dir() else path
    desc = ""
    name = path.stem
    if target.exists():
        try:
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(2000)
                m_name = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
                if m_name:
                    name = m_name.group(1).strip()
                m_desc = re.search(r"^description:\s*(?:>|\|)?\s*\n?\s*([^\n]+)", content, re.MULTILINE)
                if m_desc:
                    desc = m_desc.group(1).strip()
        except Exception:
            pass
    if not desc:
        desc = "Kỹ năng chuyên ngành tự động hóa OMC."
    return {"id": path.stem, "name": name, "description": desc, "relative_path": str(path.relative_to(SKILLS_DIR))}

def classify_skill(skill_info: dict) -> str:
    text = (skill_info["id"] + " " + skill_info["name"] + " " + skill_info["description"]).lower()
    
    # Priority check for specific strong categories
    for cat_id, cat_data in TAXONOMY_DEF.items():
        for kw in cat_data["keywords"]:
            # word boundary match or clean substring
            if re.search(r"\b" + re.escape(kw) + r"\b", text) or kw in skill_info["id"]:
                return cat_id
                
    # Fallback default
    return "saas-backend-data"

def build_taxonomy():
    all_skills = []
    
    # Scan core skills
    if CORE_DIR.exists():
        for d in sorted(CORE_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                meta = extract_meta(d)
                meta["is_core"] = True
                all_skills.append(meta)
                
    # Scan vault skills
    if VAULT_DIR.exists():
        for d in sorted(VAULT_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                meta = extract_meta(d)
                meta["is_core"] = False
                all_skills.append(meta)

    # Classify into taxonomy
    categorized = {k: {**v, "skills": []} for k, v in TAXONOMY_DEF.items()}
    
    for s in all_skills:
        cat = classify_skill(s)
        categorized[cat]["skills"].append(s)

    # Output JSON Taxonomy
    output_json = SKILLS_DIR / "SKILL_TAXONOMY.json"
    data_to_save = {
        "version": "2.0.0",
        "total_skills": len(all_skills),
        "total_categories": len(categorized),
        "categories": categorized,
        "industry_bundles": INDUSTRY_BUNDLES
    }
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Đã lập chỉ mục {len(all_skills)} skills vào {len(categorized)} nhóm tại: {output_json}")

    # Generate Markdown Reference Guide
    output_md = SKILLS_DIR / "CATEGORIES.md"
    md_lines = [
        "# 📚 CẨM NANG PHÂN NHÓM KHO SKILLS & GÓI DOANH NGHIỆP OMC",
        "",
        "> Bản phân loại toàn diện hơn **720+ Skills** theo 10 nhóm chức năng và các gói trang bị chuyên biệt cho từng loại hình công ty.",
        "> **Hermes Master Copilot** sử dụng cẩm nang này để tư vấn gói kỹ năng phù hợp nhất mỗi khi bạn thành lập công ty mới.",
        "",
        "---",
        "",
        "## 🏢 1. BỘ GÓI KỸ NĂNG THEO MÔ HÌNH CÔNG TY (INDUSTRY BUNDLES)",
        ""
    ]

    for b_id, b in INDUSTRY_BUNDLES.items():
        md_lines.append(f"### 🎯 Gói: {b['industry_name']} (`{b_id}`)")
        md_lines.append(f"- **Các nhóm kỹ năng phụ trách:** {', '.join([f'`{g}`' for g in b['recommended_groups']])}")
        md_lines.append(f"- **Kỹ năng mũi nhọn khuyên dùng:** {', '.join([f'`{s}`' for s in b['highlight_skills']])}")
        md_lines.append(f"- **Lệnh nạp nhanh:** `python skills/manager.py bundle {b_id}`")
        md_lines.append("")

    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 🗂️ 2. CHI TIẾT 10 NHÓM CHỨC NĂNG (TAXONOMY DIRECTORY)")
    md_lines.append("")

    for cat_id, cat in categorized.items():
        skills_count = len(cat["skills"])
        md_lines.append(f"### {cat['title']} (`{cat_id}`) — [{skills_count} Skills]")
        md_lines.append(f"> *{cat['description']}*")
        md_lines.append("")
        md_lines.append("| Tên Skill | Cốt lõi | Mô tả chức năng |")
        md_lines.append("| :--- | :---: | :--- |")
        
        # Show top 15 skills per category to keep markdown readable
        for s in cat["skills"][:20]:
            core_badge = "⭐ Core" if s.get("is_core") else "Vault"
            clean_desc = s["description"][:70].replace("|", "-")
            md_lines.append(f"| `{s['id']}` | {core_badge} | {clean_desc}... |")
            
        if skills_count > 20:
            md_lines.append(f"| *... và {skills_count - 20} kỹ năng chuyên sâu khác* | Vault | Tra cứu đầy đủ bằng: `python skills/manager.py group {cat_id}` |")
        md_lines.append("")

    with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print(f"✅ Đã tạo cẩm nang tra cứu Markdown tại: {output_md}")

if __name__ == "__main__":
    build_taxonomy()
