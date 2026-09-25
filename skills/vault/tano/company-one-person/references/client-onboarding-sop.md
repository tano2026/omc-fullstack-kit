# Client Onboarding SOP — Tano Agency

Áp dụng khi Chủ tịch kickstart dự án mới vào hệ thống.

## Steps

### 1. Tạo CLIENTS/<PROJECT>/SKILL.md
```
CLIENTS/<PROJECT>/
├── SKILL.md       ← Pipeline + brand + key files + skill references + hard rules
└── ...            ← Supporting docs
```

Template:
```markdown
---
name: <project-key>
domain: <domain>
version: 1.0
---

# <Project Name> — Description

## Pipeline
6 bước: ...

## Brand & Design
[Tokens, voice, visuals]

## Key Files

## Agent Skills (load from AI-Vibe-Toolkit)
1. skill-name — description

## Hard Rules
- ...

## Variation Guard (cho video channel)
- Mỗi video phải khác ≥3/5 trục

## Render Config
- Engine: HyperFrames / FFmpeg
```

### 2. Media adapter — `agents/media/adapters.py`

- **Tools mới cần thiết?** `_tool_hyperframes()`, `_tool_pollinations()`, `_tool_tts()` upgrade
- **Auto-detect** — update `_real_image_gen()` để detect project qua topic keywords
- **Pipeline prompt** — update `video_pipeline` analyzer prompt
- **Workdir constant** — thêm `_AIRFARE_ROOT` kiểu constant + register `hyperframes` adapter trong `build_registry()` với workdir mặc định
- **Verify:** `python -c "import ast; ast.parse(open('agents/media/adapters.py').read()); print('✅')"`

### 3. Dev adapter — `agents/dev/adapters.py`

- Thêm keyword→folder path vào `project_map` dict
- VD: `"airfare": ["airfare-decoded-video01"]`
- **Verify:** syntax check

### 4. CEO adapter — `agents/ceo/adapters.py`

- Thêm vào `COMPANY_PROJECTS` dict (status, desc, depts)
- Thêm vào list dự án trong `intake` system prompt
- **Verify:** syntax check

### 5. Final check
- CEO chat hỏi "dự án mới" → CEO phải list được
- Dispatch thử 1 task đến agent đúng phòng ban

## Pitfalls

| Issue | Fix |
|-------|-----|
| Agent không nhận ra project mới | Quên update CEO `COMPANY_PROJECTS` + intake prompt. Cả 2 chỗ. |
| Media dùng sai image gen | Quên update `_real_image_gen()` auto-detect. Topic keyword check phải include cả tên project + từ khóa liên quan. |
| HyperFrames chạy sai folder | `_tool_hyperframes()` cần workdir — set default constant trong `build_registry()`. |
| ElevenLabs key hết hạn/restricted | Luôn có fallback: Edge TTS AndrewNeural cho English, NamMinhNeural cho Việt. |
| Edge TTS không cài | `pip install edge-tts` — free, 0 key. |
