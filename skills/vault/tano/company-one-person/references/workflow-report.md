# Quy trình làm việc — Công ty 1 người

## 3 cách tương tác

### Cách 1: Web Dashboard (khuyên dùng)
Mở http://localhost:8137 trên phone → chat với CEO.

### Cách 2: Gọi thẳng 1 agent
```bash
cd D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core
python run.py <agent> <task_type> "<nội dung>"
```

Agent list: ceo, dev, sales, marketing, operations, support, analytics, media

### Cách 3: Qua CEO (nhiều phòng ban)
```bash
python run.py ceo intake "mô tả nhiệm vụ"    # CEO phân tích
python run.py ceo delegate "mô tả"            # CEO lập kế hoạch
python run.py ceo track "dự án"               # Xem taskboard
python run.py ceo report "dự án"              # CEO tổng hợp báo cáo
```

## Luồng CEO v2 (khi chat)
1. User gửi mệnh lệnh tiếng Việt bất kỳ
2. CEO intake: LLM phân tích → JSON {mission, type, urgency, goal, depts}
3. CEO delegate: LLM lập kế hoạch → JSON {plan: [{dept, task, priority}]}
4. CEO dispatch: ghi taskboard → auto gọi agents (ThreadPoolExecutor, 90s timeout)
5. CEO track: đọc taskboard → LLM tổng hợp executive brief

## Luồng agent (brain pipeline 7 stage)
INTAKE → PLAN → COLLECT → VALIDATE → ANALYZE → SYNTHESIZE → VERIFY → DELIVER

## Xử lý lỗi thường gặp
- **PowerShell không chạy** → disable execution policy: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- **Jinja2 cache error** → `templates.env.loader = FileSystemLoader(...)`
- **Port 8137 bị chiếm** → `cmd.exe //c "taskkill /F /PID <PID>"`
- **CEO dispatch timeout** → tăng `per_task_timeout` trong `run_assignments()`
- **Web search trống** → DDG rate limit, đợi 30s thử lại
