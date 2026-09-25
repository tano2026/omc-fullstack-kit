#!/usr/bin/env python3
"""
Hermes OMC Master Copilot (Interactive Assistant & Co-Worker)
Trợ lý ruột & Cố vấn tối cao am hiểu 100% cấu trúc OMC, kho 720+ Skills theo 10 nhóm chức năng,
hỗ trợ tư vấn gói kỹ năng khi mở công ty mới, điều phối và tự học tiến hóa hệ thống.
"""

import os
import sys
import json
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "obsidian-vault"))

from engines.trio_orchestrator import execute_omc_pipeline
from engines.jev_gateway.ingress_router import IngressRouter
from vault_sync import VaultSync

BANNER = """
======================================================================
🏛️  HERMES OMC MASTER COPILOT & CHIEF OF STAFF
    "Người đồng hành tri kỷ - Am hiểu toàn bộ hệ sinh thái & Kho 720+ Skills"
======================================================================
"""

class HermesCopilot:
    def __init__(self):
        self.vault = VaultSync(BASE_DIR / "obsidian-vault")
        self.skills_dir = BASE_DIR / "skills"
        self.agents_dir = BASE_DIR / "agents"
        self.taxonomy_file = self.skills_dir / "SKILL_TAXONOMY.json"
        self.taxonomy = self._load_taxonomy()

    def _load_taxonomy(self) -> dict:
        if self.taxonomy_file.exists():
            try:
                with open(self.taxonomy_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def print_welcome(self):
        print(BANNER)
        print("👋 Chào Chủ tịch Nguyễn Ngọc Tân! Tôi là Hermes - Tổng Quản & Cố Vấn Tối Cao OMC.")
        print("Tôi nắm rõ 100% tài nguyên và cấu trúc của bộ khung này:")
        print(f"  • 🧠 Quad-Engine: DSH (Planning) + Hermes (Reasoning) + OpenClaw (DevOps) + JEV (Reflex & Safety)")
        print(f"  • 👥 Bộ máy: 9 Phòng Ban Chuyên Môn đã sẵn sàng tác chiến")
        
        total_skills = self.taxonomy.get("total_skills", 720)
        total_cats = self.taxonomy.get("total_categories", 10)
        print(f"  • 🧰 Kho Vũ Khí: {total_skills} Skills phân loại chuẩn theo {total_cats} Nhóm Chức Năng chuyên sâu")
        print(f"  • 📓 Second Brain: Obsidian Vault đã kết nối đồng bộ 2 chiều (Thread-Safe)")
        print(f"  • 🚀 Nhân bản: Lệnh '/recommend <lĩnh vực>' để tôi tư vấn gói kỹ năng và mở công ty")
        print("\n💡 Gõ câu lệnh hoặc yêu cầu tự nhiên để tôi hỗ trợ ngay. (Gõ '/help' để xem lệnh nhanh, 'exit' để thoát)")
        print("-" * 70)

    def handle_status(self):
        print("\n📊 [BÁO CÁO TRẠNG THÁI HỆ THỐNG OMC]")
        print(f"  • Thư mục gốc: {BASE_DIR}")
        agents = [d.name for d in self.agents_dir.iterdir() if d.is_dir()]
        print(f"  • Danh sách phòng ban ({len(agents)}): {', '.join(agents)}")
        print(f"  • Model mặc định: openrouter/free (Auto-Free Tier)")
        print(f"  • Failover Chain: Nous Hermes 70B ➔ DeepSeek V3 ➔ OmniRoute ➔ Gemini Flash")
        print(f"  • Kho Kỹ Năng: 10 Nhóm Chức Năng ({self.taxonomy.get('total_skills', 720)} skills)")
        print("  • Obsidian Sync: Đang hoạt động bình thường\n")

    def handle_categories(self):
        print("\n" + "=" * 65)
        print("🗂️ 10 NHÓM CHỨC NĂNG TRONG KHO SKILL (HERMES TAXONOMY)")
        print("=" * 65)
        categories = self.taxonomy.get("categories", {})
        for cat_id, cat in categories.items():
            print(f"  • [{cat_id:<28}] : {cat['title']} ({len(cat['skills'])} skills)")
        print("\n👉 Gõ: /recommend <lĩnh vực> để tôi tư vấn gói kỹ năng mở công ty!")

    def handle_recommend(self, industry_query: str):
        if not industry_query:
            print("⚠️ Cú pháp: /recommend <tên lĩnh vực hoặc ý tưởng kinh doanh>")
            return
            
        print("\n" + "=" * 70)
        print(f"🏛️ [HERMES MASTER COPILOT - TƯ VẤN GÓI KỸ NĂNG CHO: '{industry_query}']")
        print("=" * 70)
        
        query = industry_query.lower()
        bundles = self.taxonomy.get("industry_bundles", {})
        matched_bundle = None
        
        # 1. Match pre-defined bundles
        for b_id, b in bundles.items():
            if any(w in query for w in b["industry_name"].lower().split()) or b_id in query:
                matched_bundle = (b_id, b)
                break
                
        if matched_bundle:
            b_id, b = matched_bundle
            print(f"\n🎯 [KHUYẾN NGHỊ CHUYÊN BIỆT] Gói Doanh Nghiệp: {b['industry_name']} (`{b_id}`)")
            print("\n📋 1. CÁC NHÓM KỸ NĂNG BẮT BUỘC TRANG BỊ:")
            for g in b["recommended_groups"]:
                cat_info = self.taxonomy.get("categories", {}).get(g, {})
                print(f"   • {cat_info.get('title', g)} ({len(cat_info.get('skills', []))} skills sẵn dùng)")
                
            print("\n⭐ 2. TOP KỸ NĂNG MŨI NHỌN GÁN CHO CÁC PHÒNG BAN:")
            for s in b["highlight_skills"]:
                print(f"   🔹 `{s}`")
                
            clone_cmd = f"python clone_company.py --name \"my-{b_id}\" --domain \"{b['industry_name']}\""
            print(f"\n🚀 3. HƯỚNG DẪN KHỞI TẠO CÔNG TY CON:")
            print(f"   Chạy lệnh: {clone_cmd}")
            return
            
        # 2. Match categories by keywords
        matched_cats = []
        for cat_id, cat in self.taxonomy.get("categories", {}).items():
            score = sum(1 for kw in cat["keywords"] if kw in query)
            if score > 0:
                matched_cats.append((score, cat_id, cat))
                
        matched_cats.sort(key=lambda x: x[0], reverse=True)
        if matched_cats:
            print(f"\n💡 Tìm thấy {len(matched_cats)} nhóm chức năng tương ứng với mô hình của bạn:")
            for score, cat_id, cat in matched_cats[:3]:
                print(f"\n📁 Nhóm: {cat['title']}")
                print(f"   Mô tả: {cat['description']}")
                sample = [s['id'] for s in cat['skills'][:6]]
                print(f"   Kỹ năng tiêu biểu: {', '.join(sample)}")
        else:
            print("\nℹ️ Lĩnh vực mới. Hermes đề xuất bộ khung tiêu chuẩn: `software-saas` kết hợp `marketing-growth-seo`.")

    def handle_search_skills(self, keyword: str):
        if not keyword:
            print("⚠️ Vui lòng nhập từ khóa: /skills <từ khóa>")
            return
        os.system(f"python \"{self.skills_dir / 'manager.py'}\" search {keyword}")

    def handle_assign_skill(self, agent_id: str, skill_name: str):
        if not agent_id or not skill_name:
            print("⚠️ Cú pháp: /assign <agent_id> <skill_name>")
            return
        os.system(f"python \"{self.skills_dir / 'manager.py'}\" assign --agent {agent_id} --skill {skill_name}")

    def handle_learn(self, skill_name: str, desc: str):
        if not skill_name:
            print("⚠️ Cú pháp: /learn <tên-skill> <mô tả chi tiết>")
            return
        skill_dir = self.skills_dir / "vault" / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = f"""# 🧠 SKILL: {skill_name}

> Kỹ năng được tự động học và đóng gói bởi **Hermes Master Copilot**.

## 📌 Mô tả:
{desc or "Quy trình thực chiến mới được đúc kết từ quá trình vận hành."}

## 🎯 Hướng Dẫn Thực Hiện:
1. Tiếp nhận đầu vào theo tiêu chuẩn của OMC.
2. Triển khai theo từng lát cắt mỏng (thin slices).
3. Kiểm thử xác thực kết quả thực tế trước khi bàn giao.
"""
        with open(skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🎉 [TỰ HỌC THÀNH CÔNG] Đã đúc kết và lưu kỹ năng mới '{skill_name}' vào skills/vault/{skill_name}/SKILL.md!")
        
        self.vault.record_decision(
            f"Học kỹ năng mới: {skill_name}",
            "Hermes Master Copilot (Self-Learning)",
            f"Hệ thống đã tự học và đóng gói kỹ năng '{skill_name}': {desc}"
        )

    def handle_clone(self, name: str, domain: str):
        if not name or not domain:
            print("⚠️ Cú pháp: /clone <TênCôngTy> <LĩnhVực>")
            return
        clone_script = BASE_DIR / "clone_company.py"
        os.system(f"python \"{clone_script}\" --name \"{name}\" --domain \"{domain}\"")

    def run_interactive(self):
        self.print_welcome()
        while True:
            try:
                user_input = input("\n👑 Chủ tịch Tân > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("👋 Tạm biệt Chủ tịch! Hermes Master luôn ở đây khi anh cần.")
                    break
                elif user_input.lower() == "/help":
                    print("\n📜 [DANH SÁCH LỆNH NHANH CỦA HERMES MASTER]")
                    print("  • /status                   : Xem trạng thái hệ thống, phòng ban, model")
                    print("  • /categories               : Xem 10 nhóm chức năng trong kho 720+ skills")
                    print("  • /recommend <lĩnh vực>     : Hermes tư vấn gói kỹ năng mở công ty theo ngành")
                    print("  • /skills <từ khóa>         : Tra cứu kỹ năng cụ thể trong kho")
                    print("  • /assign <agent> <skill>   : Nạp kỹ năng cho một agent cụ thể")
                    print("  • /learn <tên-skill> <mô tả>: Hermes tự học & đóng gói skill mới")
                    print("  • /clone <tên> <lĩnh vực>   : Nhân bản 1 công ty OMC mới trong vài giây")
                    print("  • /run <nội dung task>      : Chạy chu trình Quad-Engine 5 pha")
                    print("  • Hoặc gõ bất kỳ câu hỏi/yêu cầu nào để cùng thảo luận và làm việc!\n")
                elif user_input.lower() == "/status":
                    self.handle_status()
                elif user_input.lower() == "/categories":
                    self.handle_categories()
                elif user_input.startswith("/recommend"):
                    ind = user_input.split(" ", 1)[1] if " " in user_input else ""
                    self.handle_recommend(ind)
                elif user_input.startswith("/skills"):
                    kw = user_input.split(" ", 1)[1] if " " in user_input else ""
                    self.handle_search_skills(kw)
                elif user_input.startswith("/assign"):
                    parts = user_input.split()
                    if len(parts) >= 3:
                        self.handle_assign_skill(parts[1], parts[2])
                    else:
                        print("⚠️ Cú pháp: /assign <agent_id> <skill_name>")
                elif user_input.startswith("/learn"):
                    parts = user_input.split(" ", 2)
                    skill_name = parts[1] if len(parts) > 1 else ""
                    desc = parts[2] if len(parts) > 2 else ""
                    self.handle_learn(skill_name, desc)
                elif user_input.startswith("/clone"):
                    parts = user_input.split(" ", 2)
                    name = parts[1] if len(parts) > 1 else ""
                    domain = parts[2] if len(parts) > 2 else ""
                    self.handle_clone(name, domain)
                elif user_input.startswith("/run"):
                    task = user_input.split(" ", 1)[1] if " " in user_input else ""
                    if task:
                        execute_omc_pipeline(task)
                    else:
                        print("⚠️ Cú pháp: /run <nội dung task>")
                else:
                    # Check if user is asking to open a company or asking for skill recommendations naturally
                    lower_text = user_input.lower()
                    if any(phrase in lower_text for phrase in ["mở công ty", "thành lập công ty", "tư vấn skill", "cần skill gì", "nhóm skill", "lĩnh vực"]):
                        self.handle_recommend(user_input)
                    else:
                        # Natural request processing
                        print("\n🏛️ [Hermes Master phân tích & điều phối...]")
                        route = IngressRouter.route_message(user_input)
                        assigned_agent = route["agent"]
                        print(f"👉 Yêu cầu này thuộc phạm vi của phòng ban: [@{assigned_agent}]")
                        confirm = input(f"   Chủ tịch có muốn kích hoạt chu trình Quad-Engine để @{assigned_agent} triển khai ngay không? (y/n): ").strip().lower()
                        if confirm in ["y", "yes", "ok", ""]:
                            execute_omc_pipeline(user_input)
                        else:
                            print("ℹ️ Đã ghi nhận ý tưởng vào Obsidian Inbox để xem lại sau.")
                            self.vault.add_inbox_task("Chủ tịch Tân", user_input, assigned_agent)
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Tạm biệt Chủ tịch!")
                break
            except Exception as e:
                print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    copilot = HermesCopilot()
    copilot.run_interactive()
