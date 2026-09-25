# ECC FAL AI Media — Nhúng vào Media Agent

Skill gốc: `ecc-fal-ai-media` (270 ECC skills)

## Nhúng vào _real_image_gen() — agents/media/adapters.py

**LLM prompt rules (sinh prompt tiếng Anh từ task.topic):**
```python
prompt_out = llm.chat(
    f"Viết prompt tạo ảnh AI từ: {task.topic}\n"
    f"Trả về JSON: {{\"prompt\": \"...\", \"negative\": \"...\", \"ratio\": \"square|landscape|portrait\"}}",
    system="Mày là media designer. Prompt tiếng Anh, chi tiết, chuyên nghiệp.",
    task_type="format", max_tokens=500
)
```

**Template prompt structure:**
```
[subject], [style], [lighting], [composition], [color palette], professional photography, high detail
```

**Common ratios:**
- `square` (1:1) — Instagram post
- `landscape` (16:9) — YouTube thumbnail, banner
- `portrait` (9:16) — TikTok, Reels, Story

**Pitfalls:**
- LLM hay sinh prompt tiếng Việt → system prompt phải nói rõ "Prompt tiếng Anh"
- image_generate tool chỉ chạy trong Hermes context (subprocess import)
- FAL backend yêu cầu FAL_KEY trong env (Hermes đã config từ user subscription)
