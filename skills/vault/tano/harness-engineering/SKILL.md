---
name: harness-engineering
description: "Harness Engineering — Framework & production patterns. 3 pillars: context engineering, architectural constraints, entropy management."
---

# Harness Engineering — Skill / Framework

## TL;DR
Xu hướng AI 2026: sau Prompt Engineering (2022-24) và Context Engineering (2025), Harness Engineering là kỷ nguyên thứ 3 — xây cái "khung" xung quanh AI agent để nó chạy ổn định production, không phải chỉnh prompt mãi.

## Khi nào dùng
Khi mày đang: build AI agent mà demo thì được nhưng chạy thật thì gãy, deploy agent lên production mà unreliable, bị hỏi tại sao agent làm đúng 1 bước rồi sai lung tung từ bước 2 trở đi. Cũng áp dụng khi muốn thiết kế hệ thống Hermes + OpenClaw chạy 24/7 không cần canh.

## Khung tư duy Harness Engineering

### Roadmap tiến hóa AI Engineering
```
Prompt Engineering (2022-2024)
→ Tập trung: viết câu lệnh đẹp, magic words, few-shot
→ Vấn đề: đổi model version là gãy hết

Context Engineering (2025)
→ Tập trung: nhồi đúng thông tin vào context window
→ Vấn đề: task dài → context window đầy → agent "quên"

Harness Engineering (2026)
→ Tập trung: xây toàn bộ hệ thống XUNG QUANH model
→ Công thức: Agent = Model + Harness
→ Tức là: Harness = Agent - Model (mọi thứ ngoài model)
```

### Định nghĩa nhanh
**Analogy:** Model = CPU, Context = RAM, Harness = Hệ điều hành, Agent = Ứng dụng.
Không ai chạy phần mềm trực tiếp trên CPU không có OS. Tương tự, không deploy agent mà không có harness.

Nguyên tắc cốt lõi (Mitchell Hashimoto định nghĩa, Feb 2026):
> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

### 3 trụ cột của Harness Engineering

**Trụ 1 — Context Engineering (quản lý thông tin)**
- Context compression: tóm gọn thông tin cũ mà giữ đủ ý
- Dynamic context injection: load đúng thứ cần, đúng lúc cần — không nhồi hết từ đầu
- Knowledge persistence: lưu tiến độ ra file ngoài (progress.txt, db) để agent đọc lại khi restart
- Priority scoring: thứ gì quan trọng nhất thì sống sót khi context bị cắt

**Trụ 2 — Architectural Constraints (giới hạn phạm vi)**
- Tool access controls: agent được phép dùng tool nào, chỉnh file nào, gọi API nào
- Structural enforcement: linter/CI tự check output agent trước khi commit — không để agent gãy cả codebase
- Scope boundaries: 1 task chỉ được đụng 1 phần nhỏ, không để agent cascade khắp nơi
- Safety guardrails: filter output trước khi ra production

**Trụ 3 — Entropy Management (chống "rỉ sét" dần dần)**
- Agent code càng nhiều thì inconsistency tích lũy càng nhanh (naming drift, dead code, doc lỗi thời)
- Dùng agent chuyên biệt để định kỳ audit, refactor, dọn test, cập nhật docs
- Monitor model drift: phát hiện khi chất lượng output giảm do model bị update phía provider

## Setup / Áp dụng từng bước

### Bước 1 — Xây progress persistence
```
# Tạo file progress.txt để agent tự ghi tiến độ
echo "TASK: [tên task] | STATUS: in_progress | STEP: 1/5 | LAST_ACTION: ..." > progress.txt
# Agent đọc file này mỗi khi start, không phải nhớ từ đầu
```

### Bước 2 — Đặt tool access controls
Trong system prompt của agent, ghi rõ:
```
ALLOWED TOOLS: web_search, bash_tool, create_file (trong /home/claude/ only)
FORBIDDEN: delete files, push to main branch without review, external API calls to payment systems
REQUIRE HUMAN APPROVAL: push production, modify database schema
```

### Bước 3 — Xây verification loop
```
Sau mỗi bước agent làm xong:
→ Chạy linter/test tự động
→ Nếu pass → tiếp tục
→ Nếu fail → agent đọc error, tự fix, retry (max 3 lần)
→ Nếu vẫn fail → escalate human
```

### Bước 4 — Entropy audit định kỳ
Đặt 1 cron job hoặc Hermes task chạy hàng tuần:
```
"Review toàn bộ /repos/ và /mcps/ trong AI Vibe Toolkit,
tìm entry nào đã outdated (repo bị archive, star thay đổi nhiều),
báo cáo list cần update"
```

## Ví dụ thực tế
**Vấn đề:** Hermes agent đang viết file .md cho kho, nhưng mỗi lần restart lại làm lại từ đầu (quên đã viết cái gì rồi).
**Harness fix:** Tạo file TRACKER.md — agent ghi vào đó sau mỗi task xong. Lần sau start lại, agent đọc file này trước, biết bắt đầu từ đâu.

**Vấn đề:** Agent push nhầm file nhạy cảm lên GitHub.
**Harness fix:** Thêm constraint "không push file có keyword: token, api_key, password, secret" — linter chặn trước khi PUT request được gọi.

**Vấn đề (VPS deploy, 23/07/2026):** Deploy ABTrip lên VPS gãy qua 4 lớp lỗi xếp chồng — nginx root path sai, systemd unit trỏ path không tồn tại, thiếu module `chromadb` sau khi sync code mới, `.env` permission chặn user chạy service. Nếu chỉ sửa 1 lỗi rồi báo "xong" ngay, link vẫn chết ở lớp lỗi tiếp theo — mỗi lớp lỗi che khuất lớp sau nó.
**Harness fix áp dụng (verification loop thủ công, không cần code riêng):** Sau MỖI lần sửa 1 thứ (nginx reload, systemd restart, pip install, chown/chmod), chạy `curl -o /dev/null -w '%{http_code}'` xác nhận trước khi coi là xong, rồi mới sang lỗi tiếp theo. Không gộp nhiều fix rồi test 1 lần cuối — nếu gộp sẽ không biết fix nào thật sự giải quyết được gì khi có nhiều lớp lỗi xếp chồng. Đây chính là "Verification Loop" ở trên áp dụng ngoài code — không cần class Python, chỉ cần disciplined "sửa 1 → verify 1 → sang tiếp" thay vì "sửa hết → verify 1 lần".

## Implementation Patterns (Production-Proven)

### Checkpoint-based Progress Persistence

Replace flat `progress.txt` with structured JSON for robust resume across restarts:

```python
import json, os

PHASES = ["research", "script_gen", "frame_plan", "export", "marketing"]

class ProgressTracker:
    def __init__(self, work_dir, pipeline_name):
        self.checkpoint_file = os.path.join(work_dir, "checkpoint.json")
        self.state = self.load_checkpoint() or {
            "pipeline": pipeline_name,
            "completed": [],
            "artifacts": {}
        }

    def save_checkpoint(self, phase, data=None):
        self.state["completed"].append(phase)
        if data:
            self.state["artifacts"][phase] = data
        with open(self.checkpoint_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def load_checkpoint(self):
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file) as f:
                return json.load(f)
        return None

    def is_done(self, phase):
        return phase in self.state.get("completed", [])

    def get_remaining(self):
        return [p for p in PHASES if p not in self.state.get("completed", [])]

    def get_artifact(self, phase, key, default=None):
        artifacts = self.state.get("artifacts", {}).get(phase, {})
        if isinstance(artifacts, dict):
            return artifacts.get(key, default)
        return default

    def reset(self):
        if os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
        self.state = {"pipeline": "", "completed": [], "artifacts": {}}
```

### Verification Loop (Structural Quality Checks)

After each agent output, verify structure before passing to the next stage:

```python
class VerificationLoop:
    def __init__(self):
        self.results = []

    def verify_script(self, script_data, min_frames=6):
        """6 checks: frame count, narration length, duration ratio, hook, cliffhanger."""
        checks = []
        frames = script_data.get("frames", [])
        checks.append({"name": "frame_count >= min", "passed": len(frames) >= min_frames,
                       "detail": f"{len(frames)} >= {min_frames}"})
        all_non_empty = all(f.get("narration", "") for f in frames)
        checks.append({"name": "no empty narrations", "passed": all_non_empty,
                       "detail": f"{sum(1 for f in frames if f.get('narration',''))}/{len(frames)} filled"})
        narration_lengths = [len(f.get("narration", "")) for f in frames]
        checks.append({"name": "narration >= 20 chars", "passed": all(n >= 20 for n in narration_lengths),
                       "detail": f"min: {min(narration_lengths) if narration_lengths else 0}"})
        duration_consistency = _check_duration_ratio(script_data)
        checks.append({"name": "duration consistency", "passed": duration_consistency})
        passed = all(c["passed"] for c in checks)
        self.results.append({"phase": "script", "passed": passed, "checks": checks})
        return passed

    def verify_frames(self, frames_data, total_minutes):
        """5 checks: durations > 0, total +/-10%, visual prompts, transitions, range."""
        checks = []
        durations = [f.get("duration_seconds", 0) for f in frames_data]
        checks.append({"name": "all durations > 0", "passed": all(d > 0 for d in durations)})
        total_s = sum(durations)
        target = total_minutes * 60
        checks.append({"name": f"total within 10% of {target}s",
                       "passed": abs(total_s - target) / max(target, 1) <= 0.10,
                       "detail": f"{total_s}s vs {target}s"})
        has_visual = all(f.get("visual_prompt", "") for f in frames_data)
        checks.append({"name": "all frames have visual prompts", "passed": has_visual})
        has_transition = all(f.get("transition", "") for f in frames_data)
        checks.append({"name": "all frames have transitions", "passed": has_transition})
        in_range = all(15 <= d <= 90 for d in durations)
        checks.append({"name": "durations 15s-90s", "passed": in_range})
        return all(c["passed"] for c in checks)

    def report(self):
        return {"all_passed": all(r["passed"] for r in self.results), "results": self.results}
```

### Entropy Audit Script (Weekly Cron)

```python
# jobs/entropy-audit.py — run as cronjob weekly
import os, json, time

PHASES = ["research", "script_gen", "frame_plan", "export", "marketing"]

def audit_checkpoints(base_dir):
    """Scan for orphaned checkpoint files."""
    orphans = []
    for root, dirs, files in os.walk(base_dir):
        if "checkpoint.json" in files:
            cf = os.path.join(root, "checkpoint.json")
            with open(cf) as f:
                state = json.load(f)
            completed = state.get("completed", [])
            if len(completed) >= len(PHASES):
                age = time.time() - os.path.getmtime(cf)
                if age > 7 * 86400:
                    orphans.append(cf)
    return orphans
```

### Retry Pattern for Transient Failures

```python
import time

def call_with_retry(fn, max_attempts=3, base_delay=2):
    """Exponential backoff retry. Use for API calls with transient failures."""
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_attempts:
                raise
            delay = base_delay ** attempt
            print(f"  Attempt {attempt}/{max_attempts} failed: {e}. Retry in {delay}s...")
            time.sleep(delay)
```

## Python Pitfalls (phát hiện khi build harness thực tế)

### 1. PHASES phải là module-level constant, không phải class attribute

```python
# ✅ ĐÚNG
PHASES = ["research", "script_gen", "frame_plan"]

class ProgressTracker:
    def get_remaining(self):
        return [p for p in PHASES if not self.is_done(p)]

# ❌ SAI — AttributeError tại runtime
class ProgressTracker:
    PHASES = [...]
    def get_remaining(self):
        return [p for p in self.PHASES if ...]
```

### 2. import re trong function body gây UnboundLocalError

```python
# ❌ SAI
def cmd(args):
    safe = re.sub(...)  # UnboundLocalError
    import re  # Python treat re là local variable CHO TOÀN BỘ function

# ✅ ĐÚNG import ở module level
import re
def cmd(args):
    safe = re.sub(...)
```

### 3. write() argument order khi signature là write(system, prompt)

```python
# ❌ SAI — positional arg đầu là system
result = write(prompt_string, system="...")
# → system = prompt_string, sau đó set lại = keyword → multiple values

# ✅ ĐÚNG
result = write(system="...", prompt=prompt_string)
```

### 4. getattr fallback chain cho field name không chắc chắn

```python
# Field có thể là "narration" hoặc "narrator" hoặc "description"
text = getattr(frame, 'narration', '') or getattr(frame, 'description', '') or ''
```

### 5. dotenv auto-load cho key từ ~/.hermes/.env

```python
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/.hermes/.env"))
# Sau đó os.environ.get("RESONA_API_KEY") hoạt động
```

## Lưu ý / Lỗi thường gặp
- "Harness Engineering" đang là buzzword mạnh trong 2026 — nhiều bài viết làm nó nghe phức tạp hơn thực tế. Core idea đơn giản: xây hệ thống xung quanh AI để nó reliable, không phải cứ chỉnh prompt.
- Constraint không làm agent yếu hơn — ngược lại, agent trong môi trường có giới hạn rõ ràng chạy tự tin hơn vì biết "sai là có người catch", không sợ làm gãy gì quan trọng.
- Áp ngay vào AI Vibe Toolkit: TRACKER.md là 1 dạng harness (progress persistence), token placeholder trong file push lên GitHub là 1 dạng constraint, sequential push thay vì parallel là 1 dạng entropy prevention.
- 88% AI agent project không lên được production vì harness quá fragile (số liệu Deloitte 2026) — lý do không phải model tệ, mà là hệ thống xung quanh không ổn.

## Đánh giá cá nhân
- Điểm mạnh: framework thực sự giải quyết đúng vấn đề mà bất kỳ ai build agent đều gặp — agent reliable trong production. Không phải buzzword thuần tuý.
- Điểm yếu: term còn mới, tài liệu đang rải rác nhiều nguồn, chưa có 1 "canonical book" hay course nào thực sự chuẩn hoá hết.
- Có nên dùng: 9/10 — bắt buộc phải hiểu nếu mày muốn Hermes + OpenClaw của AI Vibe Toolkit chạy production 24/7 không người trông.

## Linked Files
- [Resona TTS API](references/resona-tts-api.md) — async TTS integration pattern (submit → poll → download)
- [Multi-Skill Upgrade Pattern](references/multi-skill-upgrade-pattern.md) — phối hợp nhiều class-level skills để nâng cấp 1 production module, 5-bước workflow, nguyên tắc chống ảo giác

## Link
- Bài gốc định nghĩa chính thức (OpenAI, Ryan Lopopolo, Feb 2026): tìm "Harness Engineering: Leveraging Codex in an Agent-First World" trên OpenAI blog
- Bài giải thích dễ hiểu nhất: https://primotech.com/harness-engineering-beyond-prompt-context-engineering/
- Full framework 3 pillars: https://harnessengineering.academy/blog/what-is-harness-engineering-introduction-2026/
- Faros.ai breakdown (5 layers): https://www.faros.ai/blog/harness-engineering
