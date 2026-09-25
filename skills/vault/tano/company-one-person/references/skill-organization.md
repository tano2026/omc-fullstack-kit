# Skill Organization — tano/ vs ecc/ (Jul 2026)

## Cấu trúc

```
C:/Users/Nguyen Ngoc Tan/AppData/Local/hermes/skills/
├── 📁 tano/               ← 140 skills dự án của user
│   ├── company-one-person/  (Công ty 1 người — umbrella skill)
│   ├── tuvi/                (Tử Vi chuyên sâu)
│   ├── hyperframes/         (Content Pipeline core)
│   ├── gmsp-video-production/
│   ├── content/             (GMSP writing)
│   ├── ke-toan-automation/  (Kế toán)
│   ├── ... 140 skills
├── 📁 ecc-*/              ← 270 ECC generic skills
│   ├── ecc-brand-voice/
│   ├── ecc-python-testing/
│   ├── ecc-fal-ai-media/
│   ├── ... 270 skills
├── 📁 research/            (generic)
├── 📁 analytics/           (generic)
├── 📁 agent-skills/        (generic)
└── ...
```

## Nguyên tắc phân loại

| Vào tano/ | Ở lại root (ECC) |
|-----------|------------------|
| Skill do user tạo hoặc Hermes sinh từ dự án | Skill có tiền tố `ecc-` |
| Skill liên quan tới business cụ thể (Tử Vi, GMSP, Kế toán) | Skill generic pattern |
| Skill đã được customize cho workflow của user | Skill chưa dùng tới |
| Skill dùng thường xuyên (company-one-person, hyperframes) | Skill reference (sẽ load khi cần) |

## Cách load

```python
# Skill dự án
skill_view("tano/company-one-person")
skill_view("tano/tuvi")

# Skill ECC
skill_view("ecc-python-testing")
skill_view("ecc-fal-ai-media")
```

## Lưu ý

- Không move ECC skills vào tano/ — giữ nguyên tiền tố `ecc-`
- tano/ đã có `.hermes-link` file để Hermes detect
- Khi skills_list được gọi, tano/ skills xuất hiện như skill bình thường
