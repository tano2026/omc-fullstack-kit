# .hermes-knowledge.md — Tri thức hàng không cho AI Agent

## Cơ chế hoạt động

File `.hermes-knowledge.md` tự động được `ai_agent.py` load vào system prompt mỗi khi có chat request.

**Path resolution (ưu tiên từ trên xuống, dùng cái đầu tiên tìm thấy):**
1. `/opt/hermes/` (root project directory)
2. `/opt/hermes/ticketing-agent/` (ticketing-agent repo root)
3. `/opt/hermes/ticketing-agent/backend/` (backend directory)

```python
paths_to_try = [
    os.path.join(os.path.dirname(__file__), "..", "..", ".hermes-knowledge.md"),  # Root project
    os.path.join(os.path.dirname(__file__), "..", ".hermes-knowledge.md"),        # ticketing-agent root
    os.path.join(os.path.dirname(__file__), ".hermes-knowledge.md")               # backend dir
]
```

## Cấu trúc nên có

Maintain entries cho:
- **Hãng hàng không nội địa** — VN, VJ, QH, VU, **9G (Sun PhuQuoc Airways)** (điều kiện vé, hành lý, check-in, đường bay)
- **Thời gian bay tham khảo** — route → duration mapping
- **Quy định đổi/hủy** — theo từng hạng vé
- **Thuật ngữ hàng không** — PNR, ETKT, ADTK, ADM, codeshare...
- **Verified booking history** — PNR đã test OK (tránh lặp test)
- **Nguồn tra cứu** — Timatic, FlightRadar24, Google Flights, GDS, Aerolopa

## Cập nhật

Để update, SSH vào VPS và ghi đè file:
```bash
ssh -i ~/.ssh/hermes_key_vps.pem ubuntu@43.156.72.127
nano /opt/hermes/ticketing-agent/.hermes-knowledge.md
# Restart server:
sudo systemctl restart ticketing-agent  # hoặc process tương ứng
```

## Lưu ý

- File được load vào system prompt MỖI lần chat (có cache giảm tải)
- Dung lượng khuyến nghị: 5-15KB (không nên quá lớn vì tốn context)
- Không chứa thông tin nhạy cảm (credentials)
- Cập nhật khi có chính sách hãng thay đổi
