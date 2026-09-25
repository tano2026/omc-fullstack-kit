---
name: auto-research-trending
description: Vibe Toolkit skill - Auto Research Trending. Scan GitHub Trending, Reddit, Product Hunt, Douyin, Weibo, Xiaohongshu, Bilibili for trending topics and tools
---

# Skill: Auto Research Trending — Tự Động Tìm Tools Hay + Trend Mới Mỗi Tuần

> Skill này dùng để tự research trending từ nhiều nền tảng — từ GitHub/Reddit/Product Hunt (tools) đến Douyin/Weibo/Xiaohongshu (trend xã hội Trung Quốc). Output: top trending tools hoặc trend content đáng làm.

---

## 📌 Thông tin cơ bản

| | |
|--|--|
| **Loại** | Research Skill |
| **Tần suất** | Hàng tuần hoặc khi gọi |
| **Output** | Top trending tools + trend Trung Quốc + insights |
| **Trigger** | "tìm trending", "research mới", "xu hướng Trung Quốc" |

---

## 🔍 Nguồn tao check

| Nguồn | Tìm gì |
|-------|--------|
| GitHub Trending (weekly) | Repos nhiều stars nhất tuần |
| Reddit r/ClaudeAI | MCP, skills được cộng đồng khen |
| Reddit r/vibecoding | Tools vibe coders đang dùng |
| Reddit r/cursor | Cursor + AI tools trending |
| Product Hunt | AI tools mới ra |
| TikTok/YouTube trends | Content dạng nào đang viral |
| **Douyin (抖音) hot search** | Trend xã hội Trung Quốc, hot topics, viral content |
| **Weibo (微博) hot search** | Weibo trending list — tin tức, giải trí, sự kiện |
| **Xiaohongshu (小红书) trending** | Lifestyle/beauty/fashion trends Trung Quốc |
| **Bilibili (B站) ranking** | Top video giới trẻ Trung Quốc, gaming/anime |
| **Baidu trending** | Hot search Baidu — tin tức tổng hợp Trung Quốc |
| **Zhihu (知乎) trending** | Q&A hot, tâm lý xã hội Trung Quốc |

---

## 📋 Prompt Research Trending Tools (GitHub/Reddit/PH)

```
Search GitHub Trending tuần này (since=weekly) — 
lọc repos liên quan đến: AI tools, MCP servers, 
Claude skills, coding agents, data visualization, 
automation tools.

Với mỗi repo/tool tìm được, đánh giá theo:
1. Stars và growth rate
2. Phù hợp với vibe coders không chuyên không
3. Có thể setup trong < 30 phút không
4. Wow factor — nhìn vào có muốn xem thêm không
5. Chưa có trong kho AI Vibe Toolkit chưa

Output: Top 5
```

---

## 📋 Prompt Research Trend Trung Quốc

```
Scan trending topics từ các nền tảng Trung Quốc:
- Douyin hot search: dùng Douyin trending API hoặc web_search site:douyin.com
- Weibo hot search: weibo trending (site:weibo.com)
- Xiaohongshu trending notes: site:xiaohongshu.com
- Bilibili hot: site:bilibili.com

Với mỗi nền tảng:
1. Top 5-10 trending topics
2. Chủ đề nào đang hot
3. Trend nào có thể apply cho content Việt Nam (GMSP, TikTok, YouTube)
4. Tìm ra pattern: ngách nào đang lên, format nào viral

Output: Báo cáo theo nền tảng + đề xuất content
```

---

## 📊 Format Output Chuẩn

```
## Top 5 Trending Tuần [XX/XX]

### 1. [Tên repo/tool / Trend topic]
- Nguồn: GitHub / Douyin / Weibo / ...
- Link: ...
- Độ hot: ⭐ / 🔥 / 📈
- Tóm tắt: [1 câu]
- Tại sao hay: [1-2 câu]

### 2. ...
```

---

## ⚡ Cách Kích Hoạt

```
"tìm trending tuần này"
"research mới đi"
"có gì hay không"
"xu hướng Trung Quốc tuần này"
"douyin đang có gì hot"
"trend Trung Quốc mới nhất"
```

---

## 🎯 Tiêu Chí Filter

### AI Tools
✅ Liên quan đến AI tools, MCP, coding agents, automation
✅ Phù hợp với vibe coders — không cần background kỹ thuật sâu
✅ Có thể demo được trong video ngắn
✅ Free hoặc có free tier đáng dùng
✅ Chưa có trong kho

❌ Quá academic, không có ứng dụng thực tế ngay

### Chinese Trends (cho GMSP content)
✅ Trend đang viral trên Douyin/Weibo/Xiaohongshu
✅ Có thể áp dụng cho khán giả Việt Nam
✅ Có góc nhìn mới, bất ngờ
✅ Liên quan đến tâm lý, xã hội, lifestyle, self-dev
