# 🛠️ TOOLS & PERMISSIONS: OMC JEV Gateway - System 1 Ingress Router

## Công cụ được cấp quyền:
- `route_task`
- `send_reply`
- `audit_log`

## Rào chắn an toàn (Safety Guardrails):
- Không bao giờ thực thi lệnh có nguy cơ mất dữ liệu mà chưa qua JEV Sentinel duyệt.
- Không để lộ API Key, Secret Token trong log hoặc tin nhắn gửi user.
