# ChatBrain v2.0 — Source Code Reference

**Context:** Full source của `modules/chat_brain.py` từ RIO bot, phiên bản v2.0 (Jul 2026).
**Used when:** Cần implement hoặc debug natural language intent detection layer trên research pipeline.

## Key Design Decisions (V2 vs V1)

| Decision | V1 | V2 |
|----------|----|-----|
| **Stop words** | Không có — search query giữ nguyên conversation filler | 60+ VI stop words + prefix/suffix regex cleanup |
| **Intent model** | 7 research types (market/competitor/trend/sentiment/forecast/swot/deep) | 4 core intent types (comparison/data/trend/advice) + factual/general |
| **Routing** | Luôn gọi brain pipeline với rtype detect → pipeline trả form 6 câu | Chỉ brain cho data/comparison/general; factual/advice → direct search ngắn |
| **Output format** | Template-based với rating badges + source count | Natural language — topic header → snippet bullets → kết luận ngắn |
| **Brain output** | Nguyên xi — brain output dài 3K+ ký tự | Summarization: chỉ lấy exec summary + conclusion sections |
| **User feedback** | Không có typing indicator | `send_action(chat_id, "typing")` trước mỗi request |

## Core Concepts

### 1. VI_STOP_WORDS (60+ entries)

Stop words are MANDATORY for Vietnamese queries. Without them, queries like:
- "mày thấy giờ làm youtbe kiếm tiền thì làm thế nào" → searches for "youtbe kiếm tiền" (correct!)
- Instead of: "mày thấy giờ làm youtbe kiếm tiền thì làm thế nào" → searches garbage

The filter chain:
1. PREFIX_FILTERS — first-position patterns (9 regexes for "cho tao hỏi", "mày thấy", "phân tích"...)
2. SUFFIX_FILTERS — trailing question words ("thế nào", "ra sao", "ko", "nhỉ"...)
3. VI_STOP_WORDS — token-level filter (60+ words)

### 2. _clean_query()

```python
def _clean_query(query: str) -> str:
    """3-layer cleanup: prefix → suffix → stop word token filter"""
    q = query.strip()
    # Layer 1: Remove prefix patterns
    for p in PREFIX_FILTERS:  # "cho tao hỏi", "mày thấy", "làm thế nào"...
        q = re.sub(p, "", q, flags=re.IGNORECASE).strip()
    # Layer 2: Remove suffix question words
    for s in SUFFIX_FILTERS:  # "thế nào", "ko", "nhỉ", "hả"...
        q = re.sub(s, "", q, flags=re.IGNORECASE).strip()
    # Layer 3: Token filter (remove stop words + single chars)
    words = [w for w in q.split() if w.lower() not in VI_STOP_WORDS and len(w) > 1]
    return " ".join(words) if words else query.strip()
```

### 3. Intent Detection (4 types + fallback)

```python
INTENT_CLASSIFIERS = {
    "comparison": {keywords, weight: 1.0},  # "so sánh A vs B", "nên chọn"
    "data":       {keywords, weight: 0.9},  # "giá", "bao nhiêu", "market size"
    "trend":      {keywords, weight: 0.8},  # "xu hướng", "mới", "tương lai"
    "advice":     {keywords, weight: 0.9},  # "nên", "cách", "chiến lược"
}
```

Fallback chain when no keyword matches:
- FACTUAL_PATTERNS → "factual" (confidence 0.7)
- OPINION_PATTERNS → "advice" (confidence 0.5)
- Default → "general" (confidence 0.4)

### 4. Natural Language Response (_build_vi / _build_en)

No template placeholders. Structure:

```python
# MB
lines.append(f"**{topic}:**")  # or "**Số liệu về {topic}:**"

# Nội dung (numbered bullets)
lines.append(f"{i}. {snippet}")   # từng source
lines.append(f"   🔗 {url}")       # link dưới

# Kết (per rtype)
if rtype == "advice":     → "Tùy hoàn cảnh, nhưng hướng này đang được đánh giá cao."
if rtype == "comparison": → "Mỗi bên có thế mạnh riêng."
if rtype == "data":       → "Kiểm tra nguồn gốc trước khi dùng."
else:                     → "{N} nguồn tham khảo — hỏi tiếp nếu cần chi tiết."
```

## V2 Full Source

```python
"""
chat_brain.py — ChatBrain v2.0
================================
ChatBrain là cái não chatbot cho RIO Bot.
Thay vì form nghiên cứu cứng nhắc, nó xử lý ngôn ngữ tự nhiên.

Cách hoạt động:
1. LỌC STOP WORDS + TRÍCH CHỦ ĐỀ — xóa từ vô nghĩa tiếng Việt
2. PHÂN LOẠI INTENT — đặt câu hỏi gì?
3. RESEARCH THÔNG MINH — tìm kiếm có định hướng theo intent
4. TRẢ LỜI TỰ NHIÊN — như chuyên gia tư vấn, không format bảng biểu

Zero dependency core.
"""

import re
import time
from typing import Optional


# ========== STOP WORDS TIẾNG VIỆT ==========

VI_STOP_WORDS = set("""
mày tao tôi bạn chúng tôi chúng mày chúng tao chúng ta
của và là có không sẽ đã đang được bị những các
này kia ấy đó đấy nào đâu đấy thế sao
với cho về từ tại ở thì mà nếu như vì nên
cũng vẫn cứ đều phải muốn cần nên hay hoặc
à ư hử nhỉ nhé nhá chứ đi nào vậy
lắm quá ghê thật à ơi này ư
cái con thằng cả tấm
hãy xin mời chào
giờ bây giờ lúc nãy hôm nay hôm qua ngày mai
thấy nghĩ rằng biết hiểu đoán chắc
thế nào làm sao ra sao bao nhiêu thế này thế kia
có vẻ hình như dường như chắc là
ko kg kh k 0 hong hok
rất hơi khá
nếu như tuy nhiên mặc dù dù
vậy thì thế thì
còn cũng vẫn cứ
việc chuyện điều vấn đề
""".strip().split())

PREFIX_FILTERS = [
    r"^(?:cho tôi hỏi|cho tao hỏi|cho mình hỏi|mình hỏi|tao hỏi|tôi hỏi)\s+",
    r"^(?:hãy|hãy phân tích|phân tích|cho biết|cho tôi biết|kể cho tôi)\s+",
    r"^(?:mày thấy|mày nghĩ|theo mày|theo tao|theo bạn|bạn nghĩ|ông nghĩ)\s+",
    r"^(?:tại sao|vì sao|lý do gì|nguyên nhân)\s+",
    r"^(?:làm thế nào|làm sao|cách nào)\s+",
    r"^(?:có nên|liệu có nên|nên chăng|tôi có nên|mày có nên)\s+",
    r"^(?:kể|nói|kể về|nói về|giải thích|giải đáp)\s+",
    r"^(?:cho tao|cho mình|cho tôi)\s+",
    r"^(?:what is|what are|what's|tell me about|tell me|explain|give me)\s+",
    r"^(?:how to|how do i|how can i|how does)\s+",
    r"^(?:why is|why does|why do|why are|why should)\s+",
    r"^(?:is it|are there|can you|do you|does it)\s+",
    r"^(?:i want|i need|i would like|i'm looking for)\s+",
]

SUFFIX_FILTERS = [
    r"\s+(?:thế nào|làm sao|là gì|như thế nào|ra sao|ko|không|thế)\s*$",
    r"\s*\?\s*$",
    r"\s*(?:nhỉ|nhé|nhá|đi|thôi|vậy|à|ư|hả|hử|chứ|thế)\s*$",
]


# ========== INTENT DETECTION ==========

INTENT_CLASSIFIERS = {
    "comparison": {
        "keywords": ["so sánh", "vs", "khác nhau", "nên chọn", "tốt hơn", "rẻ hơn", "mạnh hơn",
                      "compare", "difference", "versus", "alternative", "which is better"],
        "weight": 1.0,
    },
    "data": {
        "keywords": ["giá", "bao nhiêu", "số liệu", "thống kê", "data", "số lượng",
                      "price", "cost", "how much", "revenue", "market size"],
        "weight": 0.9,
    },
    "trend": {
        "keywords": ["xu hướng", "trend", "mới", "hot", "thịnh hành", "viral",
                      "tương lai", "sẽ ra sao", "phát triển", "gần đây", "hiện tại",
                      "trending", "latest", "emerging", "future", "next big"],
        "weight": 0.8,
    },
    "advice": {
        "keywords": ["nên", "có nên", "không nên", "lời khuyên", "cách", "chiến lược",
                      "nên làm", "tips", "mẹo", "bí quyết", "kinh nghiệm",
                      "how to", "strategy", "tips", "recommend", "advice", "should i"],
        "weight": 0.9,
    },
}

FACTUAL_PATTERNS = [
    r"(?:là gì|ai là|định nghĩa|definition|meaning|nghĩa là)",
    r"(?:khi nào|ngày|tháng|năm|mấy giờ|mấy tuổi)",
    r"(?:ở đâu|địa chỉ|location|nơi nào)",
    r"(?:ai|người nào|tác giả|founder|ceo)",
    r"(?:có\s+\d+|mấy cái|mấy loại|có mấy)",
    r"(?:ko|không|phải không|có phải|có đúng)",
]

OPINION_PATTERNS = [
    r"thấy\s+(thế nào|sao|ra sao)",
    r"nghĩ\s+(sao|thế nào|gì)",
    r"đánh giá\s+(thế nào|ra sao|sao)",
    r"tương lai|có nên|liệu",
    r"có\s+\S+\s+ko|có\s+\S+\s+không",
    r"dự đoán|predict|forecast|triển vọng|outlook",
]


def _clean_query(query: str) -> str:
    """3-layer cleanup: prefix → suffix → stop word token filter"""
    q = query.strip()
    for p in PREFIX_FILTERS:
        q = re.sub(p, "", q, flags=re.IGNORECASE).strip()
    for s in SUFFIX_FILTERS:
        q = re.sub(s, "", q, flags=re.IGNORECASE).strip()
    words = [w for w in q.split() if w.lower() not in VI_STOP_WORDS and len(w) > 1]
    return " ".join(words) if words else query.strip()


def detect_intent(query: str) -> dict:
    """Parse câu hỏi tự nhiên → intent + topic chính xác."""
    cleaned = _clean_query(query)
    has_vietnamese = bool(re.search(r'[àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]', query.lower()))
    language = "vi" if has_vietnamese else "en"

    q_lower = query.lower()
    scores = {}
    for itype, config in INTENT_CLASSIFIERS.items():
        matched = sum(1 for kw in config["keywords"] if kw in q_lower)
        if matched > 0:
            scores[itype] = matched * config["weight"]

    if scores:
        rtype = max(scores, key=scores.get)
        confidence = min(1.0, scores[rtype] / 2.5)
    else:
        is_factual = any(re.search(p, q_lower) for p in FACTUAL_PATTERNS)
        is_opinion = any(re.search(p, q_lower) for p in OPINION_PATTERNS)
        rtype = "factual" if is_factual else ("advice" if is_opinion else "general")
        confidence = 0.7 if is_factual else (0.5 if is_opinion else 0.4)

    topic = cleaned if cleaned else query
    depth = "deep" if any(kw in q_lower for kw in ["phân tích", "so sánh", "tại sao",
                                                     "chiến lược", "analyze", "compare",
                                                     "comprehensive"]) or len(topic.split()) > 8 else "shallow"

    return {"rtype": rtype, "depth": depth, "confidence": confidence,
            "language": language, "topic": topic, "raw_query": query}


class ChatBrain:
    """Natural language research chatbot."""
    
    def __init__(self, adapters: dict = None):
        self.adapters = adapters or {}
        self._conv = []
    
    def chat(self, query: str) -> str:
        start = time.time()
        intent = detect_intent(query)
        topic = intent["topic"]
        self._conv.append({"query": query, "intent": intent, "topic": topic, "time": time.time()})

        if len(query.strip()) < 4:
            return self._greet(intent["language"])

        brain = self.adapters.get("brain")
        search_fn = self.adapters.get("search")
        if not search_fn and not brain:
            return "⚠️ Chưa kết nối công cụ tìm kiếm."

        try:
            # Try brain pipeline for data/comparison/general
            raw = None
            if brain and hasattr(brain, 'run') and intent["rtype"] in ("data", "comparison", "general"):
                chunks = brain.run(intent["rtype"], topic, language=intent["language"],
                                   max_results=8 if intent["depth"] == "deep" else 4)
                raw = chunks[0] if chunks else None

            if raw and len(raw) > 50:
                response = self._summarize_brain_output(raw, intent)
            else:
                response = self._quick_search(query, topic, intent)

            if len(response) > 4000:
                response = response[:3997] + "..."
            return response
        except Exception as e:
            return f"⚠️ Lỗi xử lý: {str(e)[:200]}"
    
    def _quick_search(self, query, topic, intent) -> str:
        search_fn = self.adapters.get("search")
        if not search_fn:
            return "⚠️ Search chưa được cấu hình."

        search_query = self._build_search_query(query, topic, intent)
        results = search_fn(search_query, max_results=6) if search_fn else []
        if not results:
            return f"🤷‍♂️ Chưa tìm thấy info về 'trtopic[:50]}'."
        return self._natural_response(results, topic, intent)

    def _natural_response(self, sources, topic, intent):
        lang, rtype = intent["language"], intent["rtype"]
        if lang == "vi":
            return self._build_vi(sources[:5], topic, rtype)
        return self._build_en(sources[:5], topic, rtype)

    def _build_vi(self, sources, topic, rtype):
        lines = []
        if rtype == "comparison":   lines.append(f"**{topic}** — mấy nguồn nói thế này:")
        elif rtype == "data":       lines.append(f"**Số liệu về {topic}:**")
        elif rtype == "trend":      lines.append(f"**{topic}** — cập nhật gần đây:")
        elif rtype == "advice":     lines.append(f"**{topic}** — tổng hợp kinh nghiệm:")
        else:                       lines.append(f"**{topic}:**")
        lines.append("")

        for i, s in enumerate(sources, 1):
            title = s.get("title", "") or "Nguồn"
            snippet = re.sub(r'\s+', ' ', (s.get("snippet", "") or s.get("description", "") or "")).strip()[:200]
            url = s.get("url", "")
            if snippet:
                lines.append(f"{i}. {snippet}")
            else:
                lines.append(f"{i}. **{title}**")
            if url:
                lines.append(f"   🔗 {url}")
            lines.append("")

        # Per-rtype conclusion
        conclusion = {
            "advice": "💡 *Tóm lại:* Tùy hoàn cảnh cụ thể, nhưng hướng này đang được đánh giá cao.",
            "comparison": "📊 *Kết luận:* Mỗi bên có thế mạnh riêng — tùy nhu cầu cụ thể.",
            "data": "📈 *Lưu ý:* Số liệu có thể đã thay đổi — kiểm tra nguồn gốc trước khi dùng.",
        }.get(rtype, f"🔍 {len(sources)} nguồn tham khảo — hỏi tiếp nếu cần chi tiết hơn.")
        lines.append(conclusion)
        return "\n".join(lines)

    def _summarize_brain_output(self, raw, intent):
        """Rút gọn brain output dài — chỉ lấy summary + conclusion."""
        if len(raw) < 2000:
            return raw
        lines = raw.split("\n")
        summary_lines = []
        capture = False
        for line in lines:
            lower = line.lower()
            if any(kw in lower for kw in ["tóm tắt", "tổng quan", "executive", "**tóm"]):
                capture = True
            elif any(kw in lower for kw in ["kết luận", "tổng kết", "conclusion", "**kết"]):
                capture = True
            elif "nguồn" in lower and "✅" in line:
                capture = False
            if capture:
                summary_lines.append(line)
            if len(summary_lines) > 25:
                break
        if summary_lines:
            result = "\n".join(summary_lines)
            return result if len(result) < 3500 else result[:3497] + "..."
        # Fallback: đầu + cuối
        return "\n".join(lines[:30]) + "\n...\n" + "\n".join(lines[-10:])

    def follow_up(self, query: str) -> Optional[str]:
        if not self._conv:
            return self.chat(query)
        last_topic = self._conv[-1].get("topic", "")
        if len(query.strip().split()) <= 4 and last_topic:
            query = f"{last_topic} {query}"
        return self.chat(query)
```
