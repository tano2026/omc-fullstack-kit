---
name: research-agent
description: "Vibe Toolkit skill: Research Agent - Biến Claude Thành Máy Research"
---

# Skill: Research Agent — Biến Claude Thành Máy Research

> Copy prompt này vào — Claude tự lên kế hoạch research, tìm kiếm, tổng hợp báo cáo — như có intern làm việc cho mày.

---

## 📌 Thông tin cơ bản

| | |
|--|--|
| **Loại** | System Prompt + Prompt Template |
| **Dùng với** | Claude (có Brave Search + Firecrawl MCP càng tốt) |
| **Level** | Beginner |
| **Tốt nhất khi** | Research thị trường, tìm hiểu chủ đề mới, phân tích đối thủ |

---

## 🎯 Skill này làm được gì

Thay vì mày phải Google, đọc 10 trang, tổng hợp tay — paste prompt này vào, Claude tự làm hết:
- Xác định nguồn cần research
- Thu thập thông tin có cấu trúc
- Tổng hợp báo cáo rõ ràng
- Đưa ra insights và next steps

---

## 📋 Prompt Template

```
Mày là Research Agent chuyên nghiệp. Nhiệm vụ: research toàn diện về [CHỦ ĐỀ].

**Yêu cầu output:**
1. Tổng quan (3-5 câu)
2. Các điểm chính cần biết (bullet points)
3. Số liệu và dữ kiện quan trọng
4. Xu hướng hiện tại
5. Cơ hội và rủi ro
6. Nguồn tham khảo

**Phong cách:** Ngắn gọn, có số liệu cụ thể, tránh nói chung chung.

**Chủ đề cần research:** [PASTE CHỦ ĐỀ VÀO ĐÂY]

Bắt đầu research ngay, không hỏi thêm.
```

## 🧠 Advanced Workflow — Multi-Agent Research (Batch Mode)

Khi cần research nhiều mảng song song (3-6 chủ đề cùng lúc), dùng Hermes `delegate_task`:

- Mỗi subagent search web độc lập, trả về báo cáo riêng
- Main agent tổng hợp thành file markdown duy nhất

**Workflow:**
1. Xác định 3-6 mảng cần research, mỗi mảng = 1 sub-question
2. Dùng `delegate_task` với tasks array (tối đa 3 task/lần)
3. Mỗi task cần: `goal` (câu hỏi cụ thể) + `context` (background) + `toolsets: ["web"]`
4. Sau khi nhận kết quả từ subagents — tổng hợp thành 1 file markdown duy nhất
5. Lưu file + báo cáo tóm tắt cho user

**Kinh nghiệm thực tế:** Pattern này đã dùng cho research thị trường CTV du lịch VN — 6 subagents, 7 mảng, ~45 phút research thực tế qua web search. Output: 17KB file markdown với 8 sections bao gồm thị trường CTV, đối thủ, pháp lý, hotel/DMC, và số liệu kinh tế.

**Tối ưu nghiên cứu:** Dùng deep-researchs skill với các tier L0-L5 cho phù hợp độ sâu.

**Pitfalls:**
- Subagents KHÔNG có session memory — phải pass đủ context trong field `context`
- Nếu user viết tiếng Việt, ghi rõ "Output bằng tiếng Việt" trong context của subagent
- Mỗi subagent dùng mô hình mặc định (deepseek-chat) — không nên override model cho research đơn giản

---

## 💡 Ví dụ thực tế

**Input:**
```
[CHỦ ĐỀ] = "Thị trường AI tools cho content creators Việt Nam 2025"
```

**Output Claude trả về:**
```
## Tổng quan
Thị trường AI content tools VN đang tăng trưởng 40%/năm...

## Điểm chính
- 78% content creators VN đã thử ít nhất 1 AI tool
- Top tools đang dùng: ChatGPT, Canva AI, CapCut AI
...

## Xu hướng
- Short-form video AI đang chiếm 60% demand
...
```

---

## 🔧 Biến thể hay dùng

**Research đối thủ:**
```
Research đối thủ [TÊN CÔNG TY/KÊNH].
Tìm: sản phẩm họ bán, giá, điểm mạnh yếu, 
content strategy họ đang dùng, 
audience họ target.
Output thành bảng so sánh.
```

**Research trước khi làm video:**
```
Tao chuẩn bị làm video về [CHỦ ĐỀ] cho audience là vibe coders VN.
Research xem:
- Họ đang hỏi gì về chủ đề này (pain points)
- Góc độ nào chưa ai làm
- Hook nào có thể viral
Output: 5 góc độ video tiềm năng, sắp xếp theo potential viral.
```

---

## 📊 Đánh giá

| Tiêu chí | Điểm |
|----------|------|
| Tiết kiệm thời gian | ⭐⭐⭐⭐⭐ |
| Dễ dùng | ⭐⭐⭐⭐⭐ |
| Output chất lượng | ⭐⭐⭐⭐☆ |

**Tốt hơn nhiều khi kết hợp với Brave Search + Firecrawl MCP** — Claude sẽ search thật thay vì dùng kiến thức cũ.

---

*Thêm vào kho: 06/2025*

---

## 🤖 Hermes — Cách dùng skill này

**Use case:** research tasks, báo cáo thị trường

```python
import urllib.request, json, base64

def fetch_skill(skill_file, token="[GITHUB_TOKEN]"):
    req = urllib.request.Request(
        f"https://api.github.com/repos/tano2026/AI-Vibe-Toolkit/contents/skills/{skill_file}",
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    )
    data = json.loads(urllib.request.urlopen(req).read())
    return base64.b64decode(data["content"]).decode()

# Bước 1: Fetch skill này về
skill_prompt = fetch_skill("research-agent.md")

# Bước 2: Extract phần "Prompt Template" hoặc "Nội dung skill"
# (tìm block code đầu tiên sau header ## Prompt)
import re
match = re.search(r'```\n([\s\S]+?)\n```', skill_prompt)
prompt = match.group(1) if match else skill_prompt

# Bước 3: Nhúng vào LLM call
def call_with_skill(user_input, system_prompt):
    # Gọi Claude/DeepSeek với skill làm system prompt
    payload = json.dumps({
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 2000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_input}]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=payload,
        headers={"x-api-key": "[ANTHROPIC_KEY]",
                 "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"}
    )
    r = json.loads(urllib.request.urlopen(req).read())
    return r["content"][0]["text"]

# Dùng:
# result = call_with_skill("Phân tích thị trường AI tools VN 2026", prompt)
```

> Skills không cần cài gì — fetch về, nhúng làm system prompt, gọi LLM.
