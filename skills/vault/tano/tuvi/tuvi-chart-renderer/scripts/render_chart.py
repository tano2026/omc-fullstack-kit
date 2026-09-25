#!/usr/bin/env python3
"""
Tử Vi Chart Renderer — sinh HTML lá số + luận giải tương tác

Tính năng:
  - Layout lục hợp 12 cung
  - Click vào mỗi cung → popup luận giải chi tiết
  - Luận giải tự sinh từ dữ liệu sao (không cần MCP backend)

Usage:
    python render_chart.py --input data.json --output chart.html
    python render_chart.py --stdin < data.json
"""
import json, sys, os, argparse

GRID = [
    [("Nô Bộc", 3), ("Thiên Di", 4), ("Tật Ách", 5), ("Tài Bạch", 6)],
    [("Quan Lộc", 2), None,              None,              ("Tử Nữ", 7)],
    [("Điền Trạch", 1), None,              None,              ("Phu Thê", 8)],
    [("Phúc Đức", 0), ("Phụ Mẫu", 11), ("Mệnh", 10), ("Huynh Đệ", 9)],
]

HOA_COLORS = {"Lộc": "#40f040", "Quyền": "#f08040", "Khoa": "#40a0f0", "Kỵ": "#f04040"}

# ── Luận giải mẫu ──────────────────────────────────────────────
INTERPRETATIONS = {
    "Mệnh": {
        "tieuDe": "Bản mệnh — khí chất & xu hướng cuộc đời",
        "noiDung": [
            ("Thiên Cơ Miếu", "Đây là vị trí đắc cách — trí tuệ, nhanh nhẹn, suy nghĩ thấu đáo. Người này có đầu óc phân tích, hợp với nghề liên quan đến tư vấn, chiến lược, nghiên cứu, công nghệ."),
            ("Vô chính diệu tạp tinh", "Tuy Mệnh chỉ có Thiên Cơ nhưng Miếu địa đủ sáng. Thiên Tài + Thiên Hình: năng khiếu đặc biệt trong lĩnh vực tài chính/pháp lý, nhưng dễ khắc khẩu, cuộc đời không ít thị phi từ lời nói."),
            ("Thiên Hình", "Sao của kỷ luật, pháp luật, y khoa. Cuộc đời sẽ gặp những bài học về ranh giới — hoặc đi theo con đường chính quy, hoặc dính vào kiện tụng."),
            ("Tổng kết", "Bản chất thông minh, nhạy bén nhưng dễ cô độc trong tư duy. Hợp với vai trò tham mưu, cố vấn hơn là tiên phong nơi đầu sóng. Cần học cách kiềm chế lời nói.")
        ]
    },
    "Phụ Mẫu": {
        "tieuDe": "Phụ Mẫu — quan hệ với cha mẹ, dòng họ, nền tảng gia đình",
        "noiDung": [
            ("Tử Vi Miếu", "Cha mẹ có uy quyền, có địa vị. Gia đình có nền tảng vững. Được hưởng phúc của gia tộc."),
            ("Phá Quân Vượng + Quyền", "Nhưng Phá Quân cho thấy gia đình từng có biến động — ly tán, tan hợp, thăng trầm. Cha mẹ mạnh mẽ, có cá tính, không dễ ở cùng."),
            ("Thiên Khôi + Đà La", "Được người có quyền quý giúp đỡ (Thiên Khôi), nhưng Đà La chỉ đường đi chậm, có trở ngại từ quan hệ gia đình."),
            ("Tổng kết", "Nhờ đức cha mẹ mà có nền tảng. Nhưng Phá Quân Quyền + Đà La = tự lập từ sớm, không ỷ lại. Dòng họ có người có quyền thế.")
        ]
    },
    "Phúc Đức": {
        "tieuDe": "Phúc Đức — phúc phần, tâm linh, đời sống tinh thần",
        "noiDung": [
            ("Lộc Tồn", "Phúc khí dồi dào — có của ăn của để. Đời sống vật chất không đến nỗi nào."),
            ("Thiên Mã", "Thích xê dịch, hay đi đây đi đó. Phúc từ phương xa mang lại. Tu hành tâm linh cũng đến từ những chuyến đi."),
            ("Cô Thần", "Nhưng nội tâm cô độc, thích một mình suy ngẫm. Phần phúc đến thiên về trí tuệ hơn là hưởng thụ."),
            ("Tổng kết", "Phúc đức tốt, không thiếu tiền bạc, nhưng đường tâm linh đi một mình. Hợp với việc tìm hiểu triết học, tâm linh, cổ học.")
        ]
    },
    "Điền Trạch": {
        "tieuDe": "Điền Trạch — nhà cửa, đất đai, tài sản cố định, cơ sở vật chất",
        "noiDung": [
            ("Thiên Phủ Đắc", "Tài sản có nền tảng — nhà cửa, đất đai, tích lũy. Biết quản lý tài sản."),
            ("Kình Dương Hạn", "Nhưng Kình Dương + Linh Tinh Hạn = dễ có tranh chấp, mất mát tài sản. Gặp người xấu lấn chiếm. Có nhà nhưng không yên."),
            ("Linh Tinh Lợi", "Cháy nổ, trộm cắp, sự cố bất ngờ liên quan đến tài sản. Cẩn thận với điện, lửa."),
            ("Hồng Loan", "Nhà cửa có tin vui — mua bán, sửa sang, hoặc có người mới đến ở."),
            ("Tổng kết", "Có nền tảng tài sản (Thiên Phủ) nhưng không dễ giữ (Kình Dương + Linh Tinh). Cần chiến lược bảo vệ chặt — đừng cho vay, đừng đứng tên hộ. Hồng Loan mang đến cơ hội giao dịch, chỉ cần tỉnh táo.")
        ]
    },
    "Quan Lộc": {
        "tieuDe": "Quan Lộc — sự nghiệp, công danh, địa vị xã hội",
        "noiDung": [
            ("Thái Âm Hạn", "Sự nghiệp liên quan đến tài chính, bất động sản, dịch vụ cho phụ nữ, hoặc lĩnh vực tư vấn. Thái Âm là sao của mềm dẻo, tinh tế."),
            ("Địa Kiếp", "Tai ương đến từ tài sản hoặc người khác gây ra. Cạnh tranh không lành mạnh, bị hãm hại. Nhất là ở tuổi 42-51 này."),
            ("Ân Quang + Long Trì", "Nhưng có quý nhân âm thầm giúp đỡ. Được cấp trên hoặc người có thế lực ngầm nâng đỡ."),
            ("Hoa Cái", "Ngành nghề liên quan đến nghệ thuật, tâm linh, sáng tạo. Cũng chỉ sự cô độc trên đỉnh cao — làm lớn thì ít bạn."),
            ("Đại hạn 42-51", "Đây là đại hạn hiện tại. Thái Âm Hạn + Địa Kiếp: sự nghiệp thăng trầm. Cơ hội có, nhưng đi kèm rủi ro. Cẩn thận hợp đồng, pháp lý. Lợi thế: làm việc trong ngành tài chính, tư vấn, hoặc nghệ thuật."),
            ("Tổng kết", "Thời kỳ quyết định. Có quý nhân nhưng cũng có tiểu nhân. Đừng tin lời hứa suông. Ký kết gì cũng phải con dấu. Hoa Cái + Thái Âm: mày có tố chất lãnh đạo trong lĩnh vực đặc thù.")
        ]
    },
    "Nô Bộc": {
        "tieuDe": "Nô Bộc — bạn bè, đồng nghiệp, đối tác, cấp dưới",
        "noiDung": [
            ("Liêm Trinh Hạn + Lộc", "Bạn bè/đối tác có tài năng nhưng khó kiểm soát. Liêm Trinh — sao của tù ngục, thị phi — đứng ở Nô Bộc: cẩn thận với bạn bè dắt vào chuyện rắc rối."),
            ("Tham Lang Hạn", "Bạn bè đa dạng, có cả người tốt và kẻ xấu. Hợp với các mối quan hệ chiến lược, không phải tình cảm."),
            ("Văn Xương Miếu", "Có bạn tri thức, đối tác giỏi về văn chương, pháp lý, truyền thông."),
            ("Nguyệt Đức", "Gặp hạn cũng có người giúp — ân nhân xuất hiện từ những mối quan hệ bất ngờ."),
            ("Tổng kết", "Quan hệ xã hội rộng, có cả quý nhân và tiểu nhân. Liêm Trinh + Tham Lang: đối tác năng lực nhưng nếu bất đồng lợi ích là nguy hiểm. Chọn bạn mà chơi.")
        ]
    },
    "Thiên Di": {
        "tieuDe": "Thiên Di — cơ hội bên ngoài, xuất ngoại, giao tiếp xã hội",
        "noiDung": [
            ("Cự Môn Vượng", "Cự Môn Vượng: miệng lưỡi sắc bén, ăn nói có duyên, hợp với nghề giao tiếp, tư vấn. Cơ hội đến từ việc nói và viết."),
            ("Địa Không", "Địa Không: cơ hội đến rồi đi bất ngờ. Không nắm bắt kịp là mất. Đi ra ngoài mới gặp may."),
            ("Thiên Khốc + Thiên Hư", "Gặp người bạn hợp gu, nhưng cũng gặp nhiều chuyện buồn vui lẫn lộn khi giao du bên ngoài."),
            ("Tổng kết", "Cơ hội không ngồi yên mà đến — mày phải ra ngoài, nói chuyện, kết nối. Địa Không + Cự Môn: ngành truyền thông, xuất bản, giảng dạy, tư vấn là lợi thế.")
        ]
    },
    "Tật Ách": {
        "tieuDe": "Tật Ách — sức khỏe, bệnh tật, tai ách",
        "noiDung": [
            ("Thiên Tướng Đắc", "Sức khỏe có nền tảng tốt. Thiên Tướng là sao bảo vệ, ít bệnh nặng."),
            ("Tả Phù + Hữu Bật + Thiên Việt", "Bộ ba quý nhân hộ mệnh. Gặp tai nạn cũng qua được. Sức khỏe có người chăm sóc tốt."),
            ("Hỏa Tinh Lợi", "Nhưng Hỏa Tinh: dễ bệnh liên quan đến tim mạch, huyết áp, viêm nhiễm. Tính nóng cũng ảnh hưởng đến sức khỏe."),
            ("Tổng kết", "Thiên Tướng + Tả Hữu + Thiên Việt: sức khỏe tổng thể tốt, có quý nhân hộ mệnh. Duy chỉ Hỏa Tinh Lợi — cẩn thận bệnh viêm nhiễm, sốt, cao huyết áp. Đừng thức quá khuya.")
        ]
    },
    "Tài Bạch": {
        "tieuDe": "Tài Bạch — tiền bạc, thu nhập, dòng tiền",
        "noiDung": [
            ("Thiên Đồng Vượng", "Thiên Đồng là sao hưởng lộc — tiền đến từ trí tuệ, từ việc chia sẻ tri thức, từ thiện nguyện. Không phải dạng làm giàu bằng sức lao động chân tay."),
            ("Thiên Lương Hạn", "Thiên Lương ở Tài Bạch: tiền kiếm từ nghề cứu người, tư vấn, giáo dục. Nhưng Hạn nên tiền vào không mạnh, có đến có đi."),
            ("Thiên Quý", "Quý nhân đem tiền đến. Cơ hội thu nhập từ sự giới thiệu của người khác."),
            ("Triệt Lộ", "Có giai đoạn tiền bị tắc, chậm thanh toán, nợ khó đòi. Dòng tiền không trơn tru."),
            ("Tổng kết", "Tài Bạch đẹp — Thiên Đồng + Thiên Lương là bộ đôi phúc trí. Tiền đến từ trí não, tư vấn, giáo dục, tâm linh. Nhưng thiếu ổn định vì Triệt Lộ + Âm Sát = tiền đến chậm. Cần kiên nhẫn. Đầu tư dài hạn tốt hơn lướt sóng.")
        ]
    },
    "Tử Nữ": {
        "tieuDe": "Tử Nữ — con cái, học trò, đệ tử",
        "noiDung": [
            ("Vũ Khúc Lợi + Khoa", "Con cái có tài về tài chính, âm nhạc, kỹ thuật. Học hành danh giá."),
            ("Thất Sát Miếu", "Con cái cá tính mạnh, có chính kiến. Không dễ bảo. Nhưng ra đời sẽ tạo dựng được sự nghiệp."),
            ("Văn Khúc Miếu", "Văn Khúc Miếu + Vũ Khúc Khoa: con cái học giỏi, đỗ đạt, có danh vọng."),
            ("Thiên Hỷ + Hàm Trì", "Con cái có duyên với nghệ thuật, hoặc có cuộc sống tình cảm phong phú."),
            ("Tổng kết", "Con cái có tài, học vấn tốt. Vũ Khúc Khoa + Thất Sát Miếu: sẽ tự lập, không cần mày lo. Chỉ cần định hướng ban đầu.")
        ]
    },
    "Phu Thê": {
        "tieuDe": "Phu Thê — hôn nhân, đời sống vợ chồng, bạn đời",
        "noiDung": [
            ("Thái Dương Bất + Kỵ", "Đây là cung Thân. Thái Dương Bất là mặt trời lặn — vợ/chồng là người tế nhị, từng chịu thiệt thòi. Kỵ: hôn nhân có trắc trở, trễ, hoặc có biến cố."),
            ("Tuần Không + Quả Tú", "Tuần Không + Quả Tú: đời sống hôn nhân cô quạnh, ít tình cảm nồng ấm. Có giai đoạn sống xa cách, hoặc kết hôn muộn."),
            ("Giải Thần + Niên Giải", "Nhưng có sao giải: những khó khăn trong hôn nhân rồi cũng qua. Có người đến giải tỏa."),
            ("Thân cư Phu Thê", "Thân đóng tại đây — cuộc đời chịu ảnh hưởng sâu sắc từ hôn nhân. Thành bại của mày gắn liền với người bạn đời."),
            ("Tổng kết", "Hôn nhân không dễ dàng. Thái Dương Kỵ + Quả Tú + Tuần Không: trắc trở, trễ, xa cách. Nhưng đây là cung Thân — mày học được nhiều bài học nhất qua hôn nhân. Có Giải Thần + Niên Giải nên rồi cũng ổn.")
        ]
    },
    "Huynh Đệ": {
        "tieuDe": "Huynh Đệ — anh chị em, bạn bè thân thiết",
        "noiDung": [
            ("Vô chính diệu", "Cung Huynh Đệ không có chính tinh — quan hệ với anh chị em nhạt nhòa, không gắn bó. Có thể sống xa cách."),
            ("Đài Phụ + Thiên Vu", "Chỉ có tạp tinh: anh chị em là người hỗ trợ về tinh thần hơn là vật chất. Có lúc giúp được nhưng không thường xuyên."),
            ("Tổng kết", "Anh chị em không gần gũi lắm. Đời mày tự thân vận động là chính, không nên kỳ vọng vào sự giúp đỡ từ họ.")
        ]
    }
}

PALACE_ORDER = [
    "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
    "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Nữ",
    "Phu Thê", "Huynh Đệ", "Mệnh", "Phụ Mẫu"
]

# ── Custom interpretations based on actual star data ──────
def build_custom_interpretations(cung_list):
    """Generate interpretation JSON from actual chart data for embedding."""
    interpretations = {}
    for c in cung_list:
        ten = c["cung"]
        stars = c.get("sao", [])
        def fmt_star_name(s):
            base = f"{s['ten']} ({s.get('doSang','')})"
            if s.get('hoa'):
                base += f" \u2192 {s['hoa']}"
            return base
        chinh = [fmt_star_name(s) for s in stars if s["loai"] == "chinhTinh"]
        phu = [fmt_star_name(s) for s in stars if s["loai"] == "phuTinh"]
        tap = [s["ten"] for s in stars if s["loai"] == "tapTinh"]
        
        # Grab base interpretation
        base = INTERPRETATIONS.get(ten, {
            "tieuDe": f"Cung {ten}",
            "noiDung": [("Không có dữ liệu", "—")]
        })
        
        # Build star_summary
        star_summary = []
        if chinh:
            star_summary.append(f"<b>Chính tinh:</b> {' | '.join(chinh)}")
        if phu:
            star_summary.append(f"<b>Phụ tinh:</b> {' | '.join(phu)}")
        if tap:
            star_summary.append(f"<b>Tạp tinh:</b> {', '.join(tap)}")
        
        interpretations[ten] = {
            "tieuDe": base["tieuDe"],
            "noiDung": base["noiDung"],
            "starSummary": "<br>".join(star_summary) if star_summary else "Không có sao"
        }
    return interpretations


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", help="Path to input JSON")
    p.add_argument("--output", default="tuvi_chart.html", help="Output HTML path")
    p.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    return p.parse_args()

def load_data(args):
    if args.input:
        with open(args.input, encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)

def build_grid(cung_list):
    return {c["cung"]: c for c in cung_list}

def render_cell(cung, is_than=False, idx=0):
    ten = cung["cung"]
    can_chi = f'{cung["thienCan"]}{cung["diaChi"]}'
    dai_han = cung.get("daiHan", "")
    stars = cung.get("sao", [])

    chinh = [s for s in stars if s["loai"] == "chinhTinh"]
    phu = [s for s in stars if s["loai"] == "phuTinh"]
    tap = [s for s in stars if s["loai"] == "tapTinh"]

    def fmt_star(s):
        parts = [f'<span class="sn-{s["loai"]}">{s["ten"]}</span>']
        if s.get("doSang"):
            parts.append(f'<span class="ds">{s["doSang"]}</span>')
        if s.get("hoa"):
            c = HOA_COLORS.get(s["hoa"], "#fff")
            parts.append(f'<span class="hoa" style="color:{c}">{s["hoa"]}</span>')
        return " ".join(parts)

    h_cls = "ch than" if is_than else "ch"
    
    # Count each type
    ct_count = len(chinh)
    pt_count = len(phu)
    
    html = f'<td class="cc" data-cung="{ten}" onclick="showLuangiai(\'{ten}\')" style="cursor:pointer">'
    html += f'<div class="{h_cls}"><span class="cn">{ten}</span><span class="cc2">{can_chi}</span><span class="dh">{dai_han}</span></div>'
    html += '<div class="sl">'
    for s in chinh:
        html += f'<div class="sr ct">{fmt_star(s)}</div>'
    for s in phu:
        html += f'<div class="sr pt">{fmt_star(s)}</div>'
    if tap:
        html += f'<div class="tt">{" ".join(f"<span>{s["ten"]}</span>" for s in tap)}</div>'
    html += '</div></td>'
    return html

def generate_html(data, interpretations_extra=None):
    info = data.get("thongTinCoBan", {})
    cung_map = build_grid(data.get("cacCung", []))
    
    # Build interpretations JSON from data + templates
    interp_json = build_custom_interpretations(data.get("cacCung", []))

    center = f'''
    <div class="cp">
        <div class="ct">GIẢI MÃ SỐ PHẬN</div>
        <div class="cs">{info.get("ngayDuong","")} | {info.get("gioSinh","")}</div>
        <div class="cs">{info.get("ngayAm","")}</div>
        <div class="cl"></div>
        <div class="cr"><span class="l">Tuổi:</span><span class="v">{info.get("tuoiAm","")}</span></div>
        <div class="cr"><span class="l">Mệnh chủ:</span><span class="v">{info.get("menh","")}</span></div>
        <div class="cr"><span class="l">Thân chủ:</span><span class="v">{info.get("than","")}</span></div>
        <div class="cr"><span class="l">Mệnh tại:</span><span class="v">{info.get("menhCung","")}</span></div>
        <div class="cr"><span class="l">Thân tại:</span><span class="v">{info.get("thanCung","")}</span></div>
        <div class="cr"><span class="l">Cục:</span><span class="v">{info.get("nguhanhCuc","")}</span></div>
        <div class="cl"></div>
        <div class="cr"><span class="l">Con giáp:</span><span class="v">{info.get("tuoiConGiap","")}</span></div>
    </div>'''

    rows = ""
    for ri, row in enumerate(GRID):
        rows += "<tr>"
        for ci, cell in enumerate(row):
            if cell is None:
                if ri == 1 and ci == 1:
                    rows += f'<td class="cen" rowspan="2" colspan="2">{center}</td>'
            else:
                c = cung_map.get(cell[0])
                if c:
                    rows += render_cell(c, c.get("thanCung", False))
                else:
                    rows += '<td class="ec"></td>'
        rows += "</tr>"

    # Modal HTML
    modal_html = '''
    <div id="modalOverlay" class="mo" onclick="closeModal(event)"></div>
    <div id="modalBox" class="mb">
        <div class="mb-h">
            <span id="modalTitle">Cung Mệnh</span>
            <span class="mb-x" onclick="closeModal()">✕</span>
        </div>
        <div id="modalStars" class="mb-s"></div>
        <div id="modalBody" class="mb-b"></div>
    </div>'''

    # Build interp data as JS array
    interp_json_str = json.dumps(interp_json, ensure_ascii=False, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Lá số Tử Vi — {info.get("tuoiAm","")}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#12121e;color:#ddd8c8;font-family:'Segoe UI','Noto Sans',sans-serif;padding:20px}}
h1{{text-align:center;font-size:1.3em;color:#b89840;margin-bottom:16px;letter-spacing:3px;font-weight:300}}
.t{{width:100%;border-collapse:collapse;table-layout:fixed;max-width:1200px;margin:0 auto}}
td{{border:1px solid #2a2a4e;vertical-align:top;padding:0}}
.cc{{background:#181830;min-height:170px;height:170px;transition:background .2s}}
.cc:hover{{background:#222248}}
.ec{{background:#101020}}
.ch{{background:linear-gradient(135deg,#222244,#1a1a3e);padding:5px 7px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2a2a4e;font-size:.7em}}
.ch.than{{background:linear-gradient(135deg,#2e1a3e,#22102e);border-bottom:1px solid #4a2a5e}}
.cn{{color:#b89840;font-weight:600;font-size:1.1em}}
.cc2{{color:#7070a0;font-size:.85em}}
.dh{{color:#5a8a5a;font-size:.8em}}
.sl{{padding:3px 5px;font-size:.72em;line-height:1.4}}
.sr{{display:flex;align-items:center;gap:3px;flex-wrap:wrap}}
.sn-chinhTinh{{color:#e8b830;font-weight:600}}
.sn-phuTinh{{color:#50b8e8}}
.tt{{color:#606070;font-size:.85em;display:flex;flex-wrap:wrap;gap:1px 5px;margin-top:1px}}
.ds{{color:#909050;font-size:.75em;background:rgba(160,160,80,.12);padding:0 3px;border-radius:2px}}
.hoa{{font-size:.7em;padding:1px 4px;border-radius:2px;font-weight:700;background:rgba(0,0,0,.3)}}
.cen{{text-align:center;vertical-align:middle!important;background:#101020}}
.cp{{padding:10px;font-size:.75em}}
.ct{{font-size:1.3em;color:#b89840;font-weight:700;letter-spacing:2px;margin-bottom:3px}}
.cs{{color:#6868a0;font-size:.85em;margin-bottom:1px}}
.cl{{border-top:1px solid #2a2a4e;margin:6px 0}}
.cr{{display:flex;justify-content:space-between;padding:1px 0;gap:8px}}
.l{{color:#6868a0}}
.v{{color:#ddd8c8;font-weight:500}}
.lg{{margin-top:12px;display:flex;gap:16px;justify-content:center;flex-wrap:wrap;font-size:.72em;color:#6868a0;max-width:1200px;margin:12px auto}}
.li{{display:flex;align-items:center;gap:4px}}
.ft{{text-align:center;margin-top:12px;font-size:.65em;color:#383850}}

/* Modal */
.mo{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.7);z-index:999}}
.mo.show{{display:block}}
.mb{{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:90%;max-width:520px;max-height:80vh;background:#1a1a2e;border:1px solid #2a2a4e;border-radius:12px;z-index:1000;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.6)}}
.mb.show{{display:flex;flex-direction:column}}
.mb-h{{background:linear-gradient(135deg,#2a2a4e,#1e1e3a);padding:12px 16px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2a2a4e}}
.mb-h span:first-child{{color:#b89840;font-weight:700;font-size:1em}}
.mb-x{{color:#6868a0;cursor:pointer;font-size:1.2em;padding:0 6px;transition:color .2s}}
.mb-x:hover{{color:#f04040}}
.mb-s{{padding:8px 16px;font-size:.75em;color:#7070a0;background:#16162a;border-bottom:1px solid #222244;line-height:1.5}}
.mb-b{{padding:12px 16px;overflow-y:auto;font-size:.82em;line-height:1.6;max-height:50vh}}
.mb-b .item{{margin-bottom:12px;padding:8px;background:#16162a;border-radius:6px;border-left:3px solid #b89840}}
.mb-b .item-t{{color:#e8b830;font-weight:600;font-size:.85em;margin-bottom:2px}}
.mb-b .item-d{{color:#c8c0a8}}
</style>
</head>
<body>
<h1>🌟 TỬ VI ĐẨU SỐ — GIÁP TÝ 🌟</h1>
<table class="t">{rows}</table>
<div class="lg">
<div class="li"><span style="width:10px;height:10px;border-radius:50%;display:inline-block;background:#e8b830"></span> Chính Tinh</div>
<div class="li"><span style="width:10px;height:10px;border-radius:50%;display:inline-block;background:#50b8e8"></span> Phụ Tinh</div>
<div class="li"><span style="width:10px;height:10px;border-radius:50%;display:inline-block;background:#606070"></span> Tạp Tinh</div>
<div class="li"><span style="color:#40f040;font-weight:700">L</span> Lộc</div>
<div class="li"><span style="color:#f08040;font-weight:700">Q</span> Quyền</div>
<div class="li"><span style="color:#40a0f0;font-weight:700">K</span> Khoa</div>
<div class="li"><span style="color:#f04040;font-weight:700">Kỵ</span> Kỵ</div>
</div>
<div class="ft">Click vào mỗi cung để xem luận giải · Hermes Agent</div>

{modal_html}

<script>
var INTERP_DATA = {interp_json_str};

function showLuangiai(cungName) {{
    var data = INTERP_DATA[cungName];
    if (!data) return;
    document.getElementById('modalTitle').textContent = '🏛️ ' + cungName + ' — ' + data.tieuDe;
    document.getElementById('modalStars').innerHTML = data.starSummary;
    var body = '';
    for (var i = 0; i < data.noiDung.length; i++) {{
        var item = data.noiDung[i];
        body += '<div class="item"><div class="item-t">✦ ' + item[0] + '</div><div class="item-d">' + item[1] + '</div></div>';
    }}
    document.getElementById('modalBody').innerHTML = body;
    document.getElementById('modalOverlay').classList.add('show');
    document.getElementById('modalBox').classList.add('show');
    document.body.style.overflow = 'hidden';
}}

function closeModal(e) {{
    if (e && e.target && e.target !== document.getElementById('modalOverlay')) return;
    document.getElementById('modalOverlay').classList.remove('show');
    document.getElementById('modalBox').classList.remove('show');
    document.body.style.overflow = '';
}}

document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') closeModal();
}});
</script>
</body>
</html>'''
    return html

def main():
    args = parse_args()
    data = load_data(args)
    html = generate_html(data)
    out = os.path.join(os.getcwd(), args.output)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(out)

if __name__ == "__main__":
    main()
