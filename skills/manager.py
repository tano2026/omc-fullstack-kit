#!/usr/bin/env python3
"""
OMC Central Skills Manager & Taxonomy CLI
Quản lý, phân loại 10 nhóm chức năng, tư vấn kỹ năng theo nhiệm vụ cụ thể (Task Recommender),
và đồng bộ/cập nhật kỹ năng mới từ kho tổng Master (300+ skills) & Global Hub (1,500+ skills).
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILLS_ROOT = Path(__file__).resolve().parent
CORE_DIR = SKILLS_ROOT / "core"
VAULT_DIR = SKILLS_ROOT / "vault"
AGENTS_DIR = SKILLS_ROOT.parent / "agents"
TAXONOMY_FILE = SKILLS_ROOT / "SKILL_TAXONOMY.json"

# External Local Repositories on user machine
EXTERNAL_VAULTS = [
    Path(r"D:\AI Store\AgentConfigs\hermes-local-appdata\skills"),
    Path(r"C:\Users\Nguyen Ngoc Tan\.agents\skills"),
    Path(r"D:\AI Store\OpenClaw\skills")
]

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
    print("    • Gợi ý skill cho task  : python skills/manager.py suggest --task 'Cào giá vé máy bay'")
    print("    • Đồng bộ kho skill mới : python skills/manager.py sync")

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

    matched_cats = []
    for cat_id, cat in tax.get("categories", {}).items():
        score = sum(1 for kw in cat["keywords"] if kw in query)
        if score > 0:
            matched_cats.append((score, cat_id, cat))
            
    matched_cats.sort(key=lambda x: x[0], reverse=True)
    if matched_cats:
        print(f"\n💡 ĐÃ TÌM THẤY {len(matched_cats)} NHÓM KỸ NĂNG LIÊN QUAN TRỰC TIẾP:")
        for score, cat_id, cat in matched_cats:
            print(f"\n📁 {cat['title']} ({cat_id}) — {len(cat['skills'])} skills")
            sample_skills = [s['id'] for s in cat['skills'][:5]]
            print(f"   • Gợi ý: {', '.join(sample_skills)}")

def suggest_task_skills(task_query: str) -> list:
    """Gợi ý top 3-5 skills phù hợp nhất cho một nhiệm vụ cụ thể dựa trên chấm điểm ngữ nghĩa"""
    tax = load_taxonomy()
    q_words = [w for w in task_query.lower().replace(",", " ").replace(".", " ").split() if len(w) > 2]
    
    scored_skills = []
    
    # Duyệt qua toàn bộ skills trong taxonomy
    for cat_id, cat in tax.get("categories", {}).items():
        for s in cat.get("skills", []):
            score = 0
            text = (s["id"] + " " + s["description"]).lower()
            
            for w in q_words:
                if w in s["id"].lower():
                    score += 5 # Tên skill trùng khớp từ khóa có trọng số rất cao
                elif w in text:
                    score += 2
                    
            # Thưởng điểm nếu task khớp nhóm chuyên biệt
            for kw in cat.get("keywords", []):
                if kw in task_query.lower() and kw in text:
                    score += 1
                    
            if score > 0:
                scored_skills.append((score, cat_id, s))
                
    scored_skills.sort(key=lambda x: x[0], reverse=True)
    
    # Map agent gợi ý theo category
    agent_map = {
        "marketing-growth-seo": "research-intel",
        "media-content-creation": "media-producer",
        "travel-hospitality-logistics": "domain-ops",
        "ecommerce-retail-sales": "domain-ops",
        "finance-fintech-crypto": "dsh-commander",
        "saas-frontend-uiux": "dev-automation",
        "saas-backend-data": "dev-automation",
        "automation-rpa-crawlers": "dev-automation",
        "security-devops-cloud": "openclaw-executor",
        "ai-agents-orchestration": "hermes-architect"
    }
    
    print("\n" + "=" * 70)
    print(f"🎯 [HERMES TASK RECOMMENDER] GỢI Ý SKILL CHO NHIỆM VỤ:")
    print(f"   \"{task_query}\"")
    print("=" * 70)
    
    if not scored_skills:
        print("\nℹ️ Không tìm thấy kỹ năng khớp trực tiếp từ khóa.")
        print("Gợi ý các kỹ năng nền tảng luôn sẵn sàng:")
        print("  • `expert-coding-dev` ➔ Giao cho @dev-automation")
        print("  • `superpowers`       ➔ Giao cho @hermes-architect")
        print("  • `planning-and-task-breakdown` ➔ Giao cho @dsh-commander")
        return []
        
    top_matches = scored_skills[:5]
    for idx, (score, cat_id, s) in enumerate(top_matches, 1):
        rec_agent = agent_map.get(cat_id, "main")
        scope = "⭐ Core" if s.get("is_core") else "Vault"
        print(f"\n{idx}. 🔹 Skill: `{s['id']}` ({scope}) [Độ khớp: {score}đ]")
        print(f"   📁 Nhóm   : {cat_id}")
        print(f"   👤 Giao việc: Giao cho [@{rec_agent}] phụ trách")
        print(f"   📝 Mô tả  : {s['description'][:80]}...")
        
    return top_matches

def sync_external_vault():
    """Đồng bộ và cập nhật các kỹ năng mới từ các kho Master trên máy tính"""
    print("\n" + "=" * 70)
    print("🔄 TIẾN HÀNH ĐỒNG BỘ & CẬP NHẬT KHO SKILLS (VAULT SYNC)")
    print("=" * 70)
    
    existing_skills = set(d.name for d in VAULT_DIR.iterdir() if d.is_dir())
    newly_added = 0
    
    for ext_path in EXTERNAL_VAULTS:
        if not ext_path.exists():
            continue
            
        print(f"\n📂 Quét nguồn kỹ năng: {ext_path}")
        count_found = 0
        for item in ext_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                count_found += 1
                if item.name not in existing_skills:
                    target_dest = VAULT_DIR / item.name
                    try:
                        shutil.copytree(item, target_dest)
                        existing_skills.add(item.name)
                        newly_added += 1
                        print(f"   ➕ Đã nạp skill mới: {item.name}")
                    except Exception as e:
                        pass
        print(f"   ✔ Đã quét {count_found} skills tại nguồn này.")
        
    print("\n" + "-" * 70)
    if newly_added > 0:
        print(f"🎉 ĐÃ NẠP THÀNH CÔNG {newly_added} KỸ NĂNG MỚI VÀO KHO PROJECT!")
    else:
        print("✅ Toàn bộ kỹ năng đã đồng bộ mới nhất, không có skill nào bị thiếu.")
        
    # Tự động chạy lại bộ phân loại Taxonomy
    print("\n🔄 Đang lập lại chỉ mục Taxonomy (SKILL_TAXONOMY.json & CATEGORIES.md)...")
    categorize_script = SKILLS_ROOT / "categorize_skills.py"
    if categorize_script.exists():
        subprocess.run([sys.executable, str(categorize_script)], check=False)
    print("=" * 70)

def search_global_skills(keyword: str):
    """Tìm kiếm kỹ năng mở rộng trên TOÀN BỘ các kho nội bộ trên máy (1,800+ skills)"""
    kw = keyword.lower()
    print("\n" + "=" * 70)
    print(f"🌐 TÌM KIẾM TOÀN CỤC TRÊN MỌI KHO SKILL TRÊN MÁY TÍNH CHO: '{keyword}'")
    print("=" * 70)
    
    results = []
    
    # 1. Project skills
    for p in [CORE_DIR, VAULT_DIR]:
        if p.exists():
            for d in p.iterdir():
                if d.is_dir() and kw in d.name.lower():
                    results.append(("Project (" + p.name + ")", d.name, d))
                    
    # 2. External vaults
    for ext in EXTERNAL_VAULTS:
        if ext.exists():
            for d in ext.iterdir():
                if d.is_dir() and kw in d.name.lower():
                    # check if already in results
                    if not any(r[1] == d.name for r in results):
                        results.append(("External: " + ext.name, d.name, d))
                        
    if not results:
        print(f"❌ Không tìm thấy kỹ năng nào chứa từ khóa '{keyword}'.")
        return
        
    print(f"Đã tìm thấy {len(results)} kỹ năng phù hợp:\n")
    for source, name, path in results[:15]:
        print(f"  • [{source:<20}] 🔹 `{name}`")
        
    if len(results) > 15:
        print(f"\n  ... và {len(results) - 15} kỹ năng khác.")

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
    parser = argparse.ArgumentParser(description="OMC Central Skills Manager & Taxonomy CLI")
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực thi")
    
    subparsers.add_parser("list", help="Liệt kê kỹ năng cốt lõi và số lượng kho")
    subparsers.add_parser("categories", help="Liệt kê 10 nhóm chức năng chuyên sâu")
    
    group_p = subparsers.add_parser("group", help="Xem danh sách kỹ năng của 1 nhóm")
    group_p.add_argument("group_id", type=str, help="ID của nhóm")
    
    subparsers.add_parser("bundles", help="Xem danh sách các gói kỹ năng theo ngành nghề")
    
    rec_p = subparsers.add_parser("recommend", help="Hermes AI gợi ý gói kỹ năng theo lĩnh vực công ty")
    rec_p.add_argument("--industry", required=True, type=str, help="Tên hoặc mô tả lĩnh vực công ty cần mở")
    
    sug_p = subparsers.add_parser("suggest", help="Hermes gợi ý kỹ năng tối ưu cho một nhiệm vụ cụ thể")
    sug_p.add_argument("--task", required=True, type=str, help="Mô tả nhiệm vụ cụ thể cần làm")
    
    subparsers.add_parser("sync", help="Đồng bộ nạp các kỹ năng mới từ kho tổng trên máy vào dự án")
    
    glob_p = subparsers.add_parser("search-global", help="Tìm kiếm trên tất cả các kho 1,800+ skills")
    glob_p.add_argument("keyword", type=str, help="Từ khóa tìm kiếm")
    
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
    elif args.command == "suggest":
        suggest_task_skills(args.task)
    elif args.command == "sync":
        sync_external_vault()
    elif args.command == "search-global":
        search_global_skills(args.keyword)
    elif args.command == "assign":
        assign_skill(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
