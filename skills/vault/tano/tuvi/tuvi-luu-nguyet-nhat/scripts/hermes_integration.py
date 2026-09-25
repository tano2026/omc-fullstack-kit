"""
Hermes Integration — Tử Vi Lưu Nguyệt & Lưu Nhật
=================================================
Gọi từ execute_code() để xem vận hạn nhanh.

Cách dùng:
    from hermes_tools import execute_code  # không cần, chạy trực tiếp
    
    exec(open(r"<path>/hermes_integration.py").read())
    result = xem_luu_nguyet_hn(1984, 5, 1, 9, "male", 2026, 5)
    print(result)
    
Hoặc chạy nguyên script này với birth info cố định ở cuối.
"""
import sys, os

SKILL_DIR = r"D:\AI Store\AgentConfigs\hermes-local-appdata\skills\tuvi\tuvi-luu-nguyet-nhat"
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from tuvi_luu_engine import xem_luu_nguyet, xem_luu_nhat, xem_tong_hop_thang
from datetime import datetime, timedelta


def xem_luu_nguyet_hn(birth_year, birth_month, birth_day, birth_hour, gender,
                       target_year=None, target_lunar_month=None):
    """Xem Lưu Nguyệt — trả về text format Telegram."""
    return xem_luu_nguyet(birth_year, birth_month, birth_day, birth_hour, gender,
                           target_year, target_lunar_month)


def xem_luu_nhat_hn(birth_year, birth_month, birth_day, birth_hour, gender,
                    target_date=None):
    """Xem Lưu Nhật 1 ngày — trả về text format Telegram."""
    return xem_luu_nhat(birth_year, birth_month, birth_day, birth_hour, gender,
                         target_date)


def xem_lien_tiep_hn(birth_year, birth_month, birth_day, birth_hour, gender,
                      start_date, num_days=7):
    """Xem Lưu Nhật nhiều ngày liên tiếp."""
    lines = []
    for i in range(num_days):
        d = start_date + timedelta(days=i)
        result = xem_luu_nhat(birth_year, birth_month, birth_day, birth_hour, gender, d)
        # Chỉ lấy phần tóm tắt (từ dòng đầu đến hết Tứ Hóa)
        parts = result.split("---")
        if len(parts) >= 2:
            # Lấy header + Tứ Hóa
            header = parts[0].strip()
            lines.append(header)
            lines.append("")
        lines.append("=" * 40)
    return "\n".join(lines)


def xem_tong_hop_hn(birth_year, birth_month, birth_day, birth_hour, gender,
                     target_year=None, target_lunar_month=None):
    """Xem tổng hợp 12 cung cho tháng."""
    return xem_tong_hop_thang(birth_year, birth_month, birth_day, birth_hour, gender,
                               target_year, target_lunar_month)


# ===== TEST VỚI THÔNG TIN CỦA TÂN =====
if __name__ == "__main__":
    BIRTH = {"year": 1984, "month": 5, "day": 1, "hour": 9, "gender": "male"}
    
    print("=== THÁNG 5 ÂM LỊCH 2026 (BÍNH NGỌ) ===")
    print(xem_luu_nguyet_hn(**BIRTH, target_year=2026, target_lunar_month=5)[:2500])
    
    print("\n\n=== NGÀY 30/06/2026 ===")
    print(xem_luu_nhat_hn(**BIRTH, target_date=datetime(2026, 6, 30))[:2500])
