---
name: dsh-hermes-openclaw-trio
description: >
  Autonomous AI Quad Engine: DeepSeek Harness (DSH) as Chief Orchestrator,
  Hermes as Structured Reasoning Specialist, OpenClaw 2.0 as 24/7 Execution Commander,
  and JEV (TypeSafe AI) as 10ms System One Reflex Decision & Safety Engine.
---

# ⚡ The AI Trio + JEV Reflex Engine (DSH + Hermes + OpenClaw 2.0 + JEV)

> **Kiến trúc liên minh 4 Thành phần:** Tận dụng 100% thế mạnh thực chiến của từng thành phần: DSH (Chiến lược), Hermes (Giải thuật chuyên sâu), OpenClaw 2.0 (Thực thi 24/7), và **JEV (Hệ thần kinh phản xạ nhanh 10ms)** tạo ra cỗ máy phát triển phần mềm an toàn, siêu tốc, khép kín (Zero-Slack, Zero-Damage Closed-Loop Delivery).

---

## 🏛️ 1. Bản chất & Phân chia Trách nhiệm (Core Roles)

```
                            [ USER / TELEGRAM / WEBHOOK ]
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │  ⚡ JEV GATEWAY (Khớp nối 1: Ingress)  │ ◄── [10ms Reflex Router]
                      │  - Lọc tin nhắn rác / chào hỏi        │     (Không tốn token LLM)
                      │  - Phân loại: Task khó hay dễ?        │
                      └───────────────────┬───────────────────┘
                                          │
                     ┌────────────────────┴────────────────────┐
                     ▼ (Task phức tạp)                         ▼ (Việc nhỏ / status)
         ┌───────────────────────┐                  ┌──────────────────────┐
         │ 1. DSH (Master Plan)  │                  │  OpenClaw trả lời    │
         └───────────┬───────────┘                  │  luôn, DSH đi ngủ    │
                     │                              └──────────────────────┘
                     ▼
         ┌───────────────────────┐
         │ 2. HERMES (Code/Spec) │
         └───────────┬───────────┘
                     │
                     ▼
         ┌────────────────────────────────────────────────────────┐
         │       ⚡ JEV SAFETY GATE (Khớp nối 2: Phanh an toàn)    │ ◄── [Zero-Damage Guard]
         │       - Lệnh này có phá hoại (rm -rf, đè file) không?  │     (Chặn đứng sai lầm VPS)
         │       - Rủi ro > 70% ➔ Phanh gấp, hỏi User!           │
         └───────────────────────────┬────────────────────────────┘
                                     │ (Đã duyệt an toàn)
                                     ▼
                        ┌────────────────────────┐
                        │ 3. OPENCLAW (Executes) │ ──► [Server / Git / Terminal]
                        └────────────┬───────────┘
                                     │
                                     ▼
         ┌────────────────────────────────────────────────────────┐
         │       ⚡ JEV EVAL GATE (Khớp nối 3: Đóng Goal)          │ ◄── [Fast Pass/Fail Verifier]
         │       - Đã pass hết test chưa? ➔ Noul: True/False      │
         └───────────────────────────┬────────────────────────────┘
                                     │ (True ➔ Complete)
                                     ▼
                        ┌────────────────────────┐
                        │   DSH SHIP & REPORT    │
                        └────────────────────────┘
```

---

## 🚀 2. 3 Điểm Tích Hợp JEV (TypeSafe AI)

1. **Reflex Gate 1: Ingress Triage (10ms):**
   - Phân loại intent: `choice(['dsh', 'hermes', 'openclaw', 'direct_reply'])`.
   - Tiết kiệm 80% chi phí gọi LLM lớn cho các câu hỏi ngắn hoặc lặp lại.

2. **Reflex Gate 2: Pre-Execution Safety Brake (15ms):**
   - Đánh giá lệnh trước khi OpenClaw gõ vào terminal: `score(risk_level)` và `noul(is_destructive)`.
   - Nếu `risk_score >= 70` ➔ Kích hoạt phanh khẩn cấp, ngăn chặn ghi đè/xóa nhầm server.

3. **Reflex Gate 3: Closed-Loop Delivery Gate (10ms):**
   - Đánh giá kết quả kiểm thử: `noul(did_pass_all_assertions)`.
   - Ngăn chặn ảo giác báo cáo hoàn thành khi test vẫn đỏ.

---

## 🛠️ 3. Cấu hình (`.trio_config.json`)

```json
{
  "trio": {
    "version": "2.1.0",
    "jev": {
      "enabled": true,
      "provider": "typesafe",
      "model": "jev-system-one-v1",
      "safetyThreshold": 70,
      "endpoint": "https://api.typesafe.ai/v1/systemone",
      "mode": "hybrid_reflex"
    },
    "dsh": {
      "mode": "orchestrator",
      "verify_before_completion": true
    },
    "hermes": {
      "provider": "openrouter",
      "model": "nousresearch/hermes-3-llama-3.1-405b",
      "temperature": 0.2,
      "max_tokens": 4096
    },
    "openclaw": {
      "daemon": "local",
      "audit_depth": "deep",
      "git_auto_stage": true
    }
  }
}
```
