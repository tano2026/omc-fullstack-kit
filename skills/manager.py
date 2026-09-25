#!/usr/bin/env python3
"""
OMC Central Skills Manager & CLI
Quản lý, tra cứu và trang bị kỹ năng từ Kho 700+ Skills cho các Agent trong hệ thống OMC.
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
CONFIG_FILE = SKILLS_ROOT.parent / "config" / "openclaw.json"

def get_skill_metadata(skill_path: Path) -> dict:
    """Đọc thông tin metadata từ SKILL.md hoặc file .md"""
    target = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
    if not target.exists():
        return {"name": skill_path.stem, "description": "Không có mô tả chi tiết."}
    
    desc = ""
    name = skill_path.stem
    try:
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for line in lines[:30]:
                line_str = line.strip()
                if line_str.startswith("name:"):
                    name = line_str.split("name:", 1)[1].strip()
                elif line_str.startswith("description:"):
                    desc = line_str.split("description:", 1)[1].strip()
                elif not desc and line_str.startswith("#"):
                    desc = line_str.lstrip("#").strip()
    except Exception:
        pass
    
    if not desc:
        desc = "Kỹ năng chuyên ngành tự động hóa OMC."
    return {"name": name, "description": desc, "path": str(target)}

def list_skills(args):
    print("=" * 65)
    print("🎯 DANH SÁCH 20 CORE FOUNDATION SKILLS (BẮT BUỘC)")
    print("=" * 65)
    if CORE_DIR.exists():
        for item in sorted(CORE_DIR.iterdir()):
            meta = get_skill_metadata(item)
            print(f"  ⭐ {item.name:<32} │ {meta['description'][:50]}")
    
    vault_count = len(list(VAULT_DIR.iterdir())) if VAULT_DIR.exists() else 0
    print("\n" + "=" * 65)
    print(f"📚 KHO SKILLS CHUYÊN SÂU (VAULT): {vault_count} SKILLS SẴN DÙNG")
    print("=" * 65)
    print("  Gợi ý: Dùng lệnh 'python manager.py search <từ khóa>' để tra cứu chi tiết.")

def search_skills(args):
    kw = args.keyword.lower()
    print(f"\n🔍 KẾT QUẢ TÌM KIẾM CHO: '{args.keyword}'\n" + "-" * 65)
    matches = []
    
    # Search core
    if CORE_DIR.exists():
        for item in CORE_DIR.iterdir():
            if kw in item.name.lower():
                matches.append(("CORE", item))
    
    # Search vault
    if VAULT_DIR.exists():
        for item in VAULT_DIR.iterdir():
            if kw in item.name.lower():
                matches.append(("VAULT", item))
                
    if not matches:
        print(f"❌ Không tìm thấy skill nào khớp với từ khóa '{args.keyword}'.")
        return
        
    for scope, path in matches:
        meta = get_skill_metadata(path)
        tag = "[CORE]" if scope == "CORE" else "[VAULT]"
        print(f"{tag:<8} 🔹 {path.name:<30} │ {meta['description'][:60]}")
    print(f"\nĐã tìm thấy {len(matches)} kỹ năng phù hợp.")

def assign_skill(args):
    agent_id = args.agent
    skill_name = args.skill
    
    # Check if skill exists
    skill_path = CORE_DIR / skill_name
    if not skill_path.exists():
        skill_path = VAULT_DIR / skill_name
    if not skill_path.exists() and (VAULT_DIR / f"{skill_name}.md").exists():
        skill_path = VAULT_DIR / f"{skill_name}.md"
        
    if not skill_path.exists():
        print(f"❌ Lỗi: Không tìm thấy skill '{skill_name}' trong kho core hoặc vault.")
        return

    # Check agent dir
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
    parser = argparse.ArgumentParser(description="OMC Skills Central Warehouse Manager")
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực thi")
    
    # List
    subparsers.add_parser("list", help="Liệt kê kỹ năng cốt lõi và tổng số trong kho")
    
    # Search
    search_p = subparsers.add_parser("search", help="Tìm kiếm kỹ năng trong kho 700+ skills")
    search_p.add_argument("keyword", type=str, help="Từ khóa tìm kiếm (ví dụ: seo, video, docker, test)")
    
    # Assign
    assign_p = subparsers.add_parser("assign", help="Gán kỹ năng cho một Agent cụ thể")
    assign_p.add_argument("--agent", required=True, type=str, help="ID của Agent (vd: dev-automation, media-producer)")
    assign_p.add_argument("--skill", required=True, type=str, help="Tên Skill cần trang bị")
    
    args = parser.parse_args()
    if args.command == "list":
        list_skills(args)
    elif args.command == "search":
        search_skills(args)
    elif args.command == "assign":
        assign_skill(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
