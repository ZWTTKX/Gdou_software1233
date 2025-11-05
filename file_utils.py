from openpyxl import Workbook
import io

def export_to_excel(filename: str, data: list):
    wb = Workbook()
    ws = wb.active
    for row in data:
        ws.append(row)
    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)
    return file_stream
