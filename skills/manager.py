#!/usr/bin/env python3
"""
OMC Central Skills Manager & Taxonomy CLI
Quản lý, phân loại theo 10 nhóm chức năng và tư vấn gói kỹ năng (Industry Bundles) cho các công ty OMC.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILLS_ROOT = Path(__file__).resolve().parent
CORE_DIR = SKILLS_ROOT / "core"
VAULT_DIR = SKILLS_ROOT / "vault"
AGENTS_DIR = SKILLS_ROOT.parent / "agents"
TAXONOMY_FILE = SKILLS_ROOT / "SKILL_TAXONOMY.json"

def load_taxonomy() -> dict:
    if TAXONOMY_FILE.exists():
        with open(TAXONOMY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def list_skills(args):
    print("=" * 70)
    print("🎯 DANH SÁCH CORE FOUNDATION SKILLS (BẮT BUỘC TRONG MỌI CÔNG TY)")
    print("=" * 70)
    if CORE_DIR.exists():
        for item in sorted(CORE_DIR.iterdir()):
            if item.is_dir() and not item.name.startswith("."):
                print(f"  ⭐ {item.name:<32}")
    
    vault_count = len(list(VAULT_DIR.iterdir())) if VAULT_DIR.exists() else 0
    print("\n" + "=" * 70)
    print(f"📚 KHO SKILLS CHUYÊN SÂU (VAULT): {vault_count} SKILLS SẴN DÙNG")
    print("=" * 70)
    print("  Gợi ý:")
    print("    • Xem 10 nhóm chức năng  : python skills/manager.py categories")
    print("    • Xem các gói ngành nghề: python skills/manager.py bundles")
    print("    • Tư vấn kỹ năng mở cty : python skills/manager.py recommend --industry 'Du lịch'")

def list_categories(args):
    tax = load_taxonomy()
    if not tax:
        print("❌ Chưa tìm thấy SKILL_TAXONOMY.json. Vui lòng chạy: python skills/categorize_skills.py")
        return
        
    print("\n" + "=" * 70)
    print("🗂️ 10 NHÓM CHỨC NĂNG TRONG KHO SKILL OMC (TAXONOMY)")
    print("=" * 70)
    for cat_id, cat in tax["categories"].items():
        skills_len = len(cat["skills"])
        print(f"\n📁 [{cat_id}] {cat['title']} ({skills_len} skills)")
        print(f"   ℹ️ {cat['description']}")
        print(f"   👉 Xem chi tiết: python skills/manager.py group {cat_id}")
    print("\n" + "-" * 70)

def list_group_skills(args):
    cat_id = args.group_id
    tax = load_taxonomy()
    categories = tax.get("categories", {})
    if cat_id not in categories:
        print(f"❌ Không tìm thấy nhóm '{cat_id}'. Chạy 'python skills/manager.py categories' để xem danh sách.")
        return
        
    cat = categories[cat_id]
    print("\n" + "=" * 70)
    print(f"{cat['title']} — {len(cat['skills'])} Skills")
    print("=" * 70)
    for s in cat["skills"]:
        tag = "[⭐ Core]" if s.get("is_core") else "[Vault] "
        print(f"  {tag} {s['id']:<32} │ {s['description'][:50]}...")

def list_bundles(args):
    tax = load_taxonomy()
    bundles = tax.get("industry_bundles", {})
    print("\n" + "=" * 70)
    print("🏢 CÁC GÓI KỸ NĂNG THEO MÔ HÌNH DOANH NGHIỆP (INDUSTRY BUNDLES)")
    print("=" * 70)
    for b_id, b in bundles.items():
        print(f"\n🎯 Gói: {b['industry_name']} (`{b_id}`)")
        print(f"   • Nhóm chức năng : {', '.join(b['recommended_groups'])}")
        print(f"   • Kỹ năng mũi nhọn: {', '.join(b['highlight_skills'])}")
        print(f"   • Lệnh kích hoạt  : python skills/manager.py bundle {b_id}")

def recommend_skills(args):
    query = args.industry.lower()
    tax = load_taxonomy()
    print("\n" + "=" * 70)
    print(f"🤖 HERMES AI SKILL RECOMMENDER CHO LĨNH VỰC: '{args.industry}'")
    print("=" * 70)
    
    # 1. Match Industry Bundles
    matched_bundle = None
    bundles = tax.get("industry_bundles", {})
    for b_id, b in bundles.items():
        if any(w in query for w in b["industry_name"].lower().split()) or b_id in query:
            matched_bundle = (b_id, b)
            break
            
    if matched_bundle:
        b_id, b = matched_bundle
        print(f"\n🎉 TÌM THẤY GÓI NGÀNH PHÙ HỢP NHẤT: {b['industry_name']} ({b_id})")
        print("\n📋 CÁC NHÓM KỸ NĂNG KHUYÊN NẠP CHO BỘ MÁY CÔNG TY:")
        for g in b["recommended_groups"]:
            cat_info = tax["categories"].get(g, {})
            print(f"   • {cat_info.get('title', g)}: {len(cat_info.get('skills', []))} skills sẵn dùng")
            
        print("\n⭐ KỸ NĂNG MŨI NHỌN CẦN TRANG BỊ NGAY CHO CÁC AGENT:")
        for s in b["highlight_skills"]:
            print(f"   🔹 `{s}`")
            
        print(f"\n👉 Lệnh nhân bản công ty kèm gói này:")
        print(f"   python clone_company.py --name \"my-{b_id}\" --domain \"{b['industry_name']}\"")
        return

    # 2. Keyword score matching across all categories
    scored_cats = []
    for cat_id, cat in tax.get("categories", {}).items():
        score = 0
        for kw in cat["keywords"]:
            if kw in query:
                score += 1
        if score > 0:
            scored_cats.append((score, cat_id, cat))
            
    scored_cats.sort(key=lambda x: x[0], reverse=True)
    
    if scored_cats:
        print(f"\n💡 ĐÃ TÌM THẤY {len(scored_cats)} NHÓM KỸ NĂNG LIÊN QUAN TRỰC TIẾP:")
        for score, cat_id, cat in scored_cats:
            print(f"\n📁 {cat['title']} ({cat_id}) — {len(cat['skills'])} skills")
            sample_skills = [s['id'] for s in cat['skills'][:5]]
            print(f"   • Gợi ý: {', '.join(sample_skills)}")
    else:
        print("\nℹ️ Lĩnh vực tùy biến mới. Khuyến nghị nạp gói tiêu chuẩn:")
        print("   • `software-saas` (cho công ty phần mềm/tech)")
        print("   • `media-agency` (cho công ty truyền thông/marketing)")
        print("   • `ecommerce-brand` (cho bán lẻ/thương mại điện tử)")

def assign_skill(args):
    agent_id = args.agent
    skill_name = args.skill
    agent_dir = AGENTS_DIR / agent_id
    if not agent_dir.exists():
        print(f"❌ Lỗi: Agent '{agent_id}' không tồn tại trong thư mục agents/.")
        return
        
    config_json = agent_dir / "config.json"
    if config_json.exists():
        with open(config_json, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        skills = cfg.get("skills", [])
        if skill_name not in skills:
            skills.append(skill_name)
            cfg["skills"] = skills
            with open(config_json, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2, ensure_ascii=False)
            print(f"✅ Đã trang bị thành công skill '{skill_name}' cho agent '{agent_id}'!")
        else:
            print(f"ℹ️ Agent '{agent_id}' đã sở hữu skill '{skill_name}' từ trước.")

def main():
    parser = argparse.ArgumentParser(description="OMC Skills Central Warehouse & Taxonomy Manager")
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực thi")
    
    subparsers.add_parser("list", help="Liệt kê kỹ năng cốt lõi và số lượng kho")
    subparsers.add_parser("categories", help="Liệt kê 10 nhóm chức năng chuyên sâu")
    
    group_p = subparsers.add_parser("group", help="Xem danh sách kỹ năng của 1 nhóm")
    group_p.add_argument("group_id", type=str, help="ID của nhóm (vd: marketing-growth-seo, travel-hospitality-logistics)")
    
    subparsers.add_parser("bundles", help="Xem danh sách các gói kỹ năng theo ngành nghề")
    
    rec_p = subparsers.add_parser("recommend", help="Hermes AI gợi ý gói kỹ năng theo lĩnh vực công ty")
    rec_p.add_argument("--industry", required=True, type=str, help="Tên hoặc mô tả lĩnh vực công ty cần mở")
    
    assign_p = subparsers.add_parser("assign", help="Gán kỹ năng cho một Agent cụ thể")
    assign_p.add_argument("--agent", required=True, type=str, help="ID của Agent")
    assign_p.add_argument("--skill", required=True, type=str, help="Tên Skill")
    
    args = parser.parse_args()
    if args.command == "list":
        list_skills(args)
    elif args.command == "categories":
        list_categories(args)
    elif args.command == "group":
        list_group_skills(args)
    elif args.command == "bundles":
        list_bundles(args)
    elif args.command == "recommend":
        recommend_skills(args)
    elif args.command == "assign":
        assign_skill(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
