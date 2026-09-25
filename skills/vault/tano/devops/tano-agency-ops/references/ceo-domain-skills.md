# CEO Domain Skills — GMSP & Tử Vi

CEO agent có ~300 skills từ auto-discovery. Ngoài skill chiến lược/quản lý thông thường, CEO được gán thêm keyword GMSP + Tử Vi domain:

## Keyword được thêm vào AGENT_KEYWORDS["ceo"] (skill_loader.py)

```
gmsp, giải mã số phận, tử vi, tuvi, đẩu số,
tứ trụ, bát tự, tử bình, phong thủy, kinh dịch,
content strategy, video production, brand strategy,
nội dung, content pipeline
```

## Skill Tử Vi trong kho (skills/tuvi/)

| Skill | Tác dụng |
|-------|---------|
| tuvi-agent | Luận giải Tử Vi Đẩu Số đa tầng — kết hợp cổ học + tâm lý phương Tây |
| tuvi-dau-so-expert | Chuyên sâu Tử Vi Đẩu Số — an sao, Tứ Hóa, 12 cung, đại hạn |
| tuvi-tu-tru-expert | Tử Bình Lạc Việt — Tứ Trụ, Dụng Thần, Cách Cục |
| tuvi-phong-thuy-expert | Phong Thủy — nhà ở, hướng, bố trí |
| tuvi-kinh-dich-expert | Kinh Dịch — gieo quẻ, luận giải 64 quẻ |
| tuvi-chart-renderer | Render lá số Tử Vi ra HTML layout 12 cung |
| tuvi-luu-nguyet-nhat | Tử Vi Lưu Nguyệt/Lưu Nhật |
| bazi-ziwei | Prompt template Tử Vi + Bát Tự |
| tuvi-mcp-server | MCP server Tử Vi — tính lá số, phân tích, so sánh |

## Skill GMSP trong kho (skills/content/)

| Skill | Tác dụng |
|-------|---------|
| gmsp-writing-formula | GMSP Writing Formula v2 — Dark Truth + Cinematic storytelling |
| gms-storyteller | GMSP Script Writer Agent — dùng reasoning model viết script 6 section |
| gmsp-modular-pipeline | 7-stage modular video production pipeline |
| gmsp-video-production | GMSP video production — HyperFrames + FFmpeg render |
| content-creator | Từ 1 ý tưởng ra 10 loại content |
| video-production-pipeline | Multi-step video production pipeline |

## Cách CEO dùng

Khi user hỏi về:
- **"Xem giúp tao lá số..."** → CEO load tuvi-agent + tuvi-dau-so-expert, gọi MCP Tử Vi
- **"Viết script tập mới..."** → CEO load gmsp-writing-formula + gms-storyteller
- **"Phân tích chiến lược nội dung..."** → CEO load GMSP skills + content-creator
