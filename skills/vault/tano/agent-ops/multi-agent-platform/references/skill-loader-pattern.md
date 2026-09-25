# Skill Loader Pattern — Dynamic .md → Agent Tool

> Tạo 1 module Python đọc skill `.md` từ Hermes Skill Library hoặc AI-Vibe-Toolkit kho, parse thành callable adapter cho agent-core. Option C: dynamic loading thay vì code từng adapter thủ công (Option B).

## Khi nào dùng

- Mày có kho skill .md phong phú (400+ skills) muốn dùng ngay
- Mày muốn agent tự load tool khi cần, thay vì code 1 function/adapter
- Skills thay đổi thường xuyên (add/sửa skill .md → agent tự cập nhật)
- Muốn tối thiểu code adapter, tối đa tái sử dụng skill có sẵn

## Pattern

```
skill_loader.py
├── _fetch_file(path)       # Đọc từ local repo (AI-Vibe-Toolkit) hoặc GitHub API
├── parse_skill(content)    # Parse YAML frontmatter + TL;DR + sections
├── skill_as_tool(path)     # .md → {name, description, instructions, sections}
├── build_skill_registry()  # Map: agent_name → {tools dict, prompt_context}
├── make_skill_adapter()    # Tạo callable ({title, url, snippet}) từ skill
└── build_skill_registry_for_adapter()  # Tạo registry cho build_real_registry()
```

## Directory

File chính: `agent-core/skill_loader.py` (đồng cấp với `real_adapters.py`)

## AGENT_SKILL_MAP

```python
AGENT_SKILL_MAP = {
    "sales": [
        "skills/affiliate-check.md",
        "skills/brand-identity-sales-kit.md",
        "skills/ecc-lead-intelligence.md",
    ],
    "dev": [
        "skills/ecc-github-ops.md",
        "skills/ecc-docker-patterns.md",
    ],
    # ... 8 agents + "_research" (common research skills)
}
```

Mỗi agent tự động kế thừa research skills từ `"_research"`.

## Cách tích hợp vào real_adapters.py

```python
from skill_loader import build_skill_registry_for_adapter

def build_real_registry(agent_name: str) -> dict:
    adapters = {"search": _web_search, ...}
    
    # Merge skill tools vào — biến skill thành callable adapter
    skill_tools = build_skill_registry_for_adapter(agent_name)
    for k, v in skill_tools.items():
        if k not in adapters:
            adapters[k] = v
    adapters["_skill_context"] = skill_tools["_skill_context"]
    
    return adapters
```

## Ưu điểm

- **Code ít hơn**: 1 module ~150 dòng Python thay vì 20+ adapter functions riêng lẻ
- **Zero maintenance khi skill đổi**: update skill .md là đủ
- **Tái sử dụng**: cùng skill dùng được cho nhiều agent
- **Context injection**: skill loader trả về prompt_context có thể nhúng vào system prompt

## Hạn chế

- **Skill .md không phải code**: chỉ hướng dẫn text, không thực thi logic thật
- **LLM-dependent**: agent cần LLM để interpret skill instructions
- **Chi phí token**: load skill → context window tăng
- **Skill format không đồng nhất**: mỗi skill viết khác nhau, parse accuracy tùy file

## Pitfalls

### 1. Path skills ECC — `ecc/` subdirectory
ECC skills nằm ở `skills/ecc/` (vd `skills/ecc/github-ops.md`), KHÔNG ở `skills/`.
Cần sửa AGENT_SKILL_MAP paths:
```python
# SAI
"skills/ecc-github-ops.md"
# ĐÚNG
"skills/ecc/ecc-github-ops.md"
# HOẶC (skill đã có healthcheck)
"skills/ecc-docker-patterns.md"  # file ở skills/ root
```

### 2. .md không có Agent Integration block
Một số skill không có `## 🤖 Agent Integration` section — parse instructions từ "Prompt Template", "Dùng Ngay", "Cách dùng" thay thế.

### 3. Local repo ưu tiên
`_fetch_file` ưu tiên đọc local `KHO_LOCAL` trước, GitHub API làm fallback (cần `GITHUB_TOKEN`).

### 4. Overhead adapter call
Mỗi lần agent gọi skill → parse lại .md. Nếu performance quan trọng, cache registry bằng `_registry_cache` dict (đã có trong skill_loader.py).

### 5. GITHUB_TOKEN trong env
Để fetch từ GitHub API khi local không có skill. Nếu thiếu, chỉ dùng local được.
