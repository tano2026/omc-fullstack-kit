import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_flight_itinerary_excel(file_path="Phuong_An_Bay_Chuyen_Nghiep.xlsx", outbound_data=None, middle_data=None, inbound_data=None, note_text=""):
    """
    Creates a highly styled, professional flight itinerary proposal in Excel.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Phương Án Bay"
    ws.views.sheetView[0].showGridLines = True

    # Palette & Styles
    HEADER_FILL = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid") # Navy Blue
    SUB_HEADER_FILL = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid")
    OPTION_FILL_1 = PatternFill(start_color="E6F0FA", end_color="E6F0FA", fill_type="solid") # Soft Blue
    RECOMMEND_FILL = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # Soft Green

    FONT_TITLE = Font(name="Calibri", size=15, bold=True, color="1B365D")
    FONT_SUBTITLE = Font(name="Calibri", size=10, italic=True, color="555555")
    FONT_SECTION = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    FONT_TABLE_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_DATA_BOLD = Font(name="Calibri", size=10, bold=True, color="000000")
    FONT_DATA_REG = Font(name="Calibri", size=10, color="000000")
    FONT_NOTE_TEXT = Font(name="Calibri", size=10, color="385723")

    ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

    BORDER_THIN = Side(border_style="thin", color="D3D3D3")
    BORDER_CELL = Border(left=BORDER_THIN, right=BORDER_THIN, top=BORDER_THIN, bottom=BORDER_THIN)

    # Title Blocks
    ws.merge_cells("A2:I2")
    ws["A2"] = "BẢNG TỔNG HỢP PHƯƠNG ÁN HÀNH TRÌNH BAY CHO KHÁCH HÀNG"
    ws["A2"].font = FONT_TITLE
    ws["A2"].alignment = ALIGN_CENTER

    ws.merge_cells("A3:I3")
    ws["A3"] = "Căn chỉnh chi tiết và phân chia các lựa chọn hành trình tối ưu nhất"
    ws["A3"].font = FONT_SUBTITLE
    ws["A3"].alignment = ALIGN_CENTER

    def write_section_header(row, text):
        ws.merge_cells(f"A{row}:I{row}")
        cell = ws[f"A{row}"]
        cell.value = text
        cell.font = FONT_SECTION
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[row].height = 26

    def write_table_headers(row):
        headers = ["STT", "Phương án", "Chặng bay", "Hãng bay", "Số hiệu", "Hành trình", "Giờ bay (Local)", "Ngày bay", "Transit / Ghi chú"]
        for col_idx, text in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col_idx)
            cell.value = text
            cell.font = FONT_TABLE_HEADER
            cell.fill = HEADER_FILL
            cell.alignment = ALIGN_CENTER
            cell.border = BORDER_CELL
        ws.row_dimensions[row].height = 22

    # Draw sections (implement custom data loop here as done in generate_excel.py)
    # ...
    
    wb.save(file_path)
    return file_path
