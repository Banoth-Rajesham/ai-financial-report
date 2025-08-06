# agents/agent_5_reporter.py

import io
import traceback
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from config import MASTER_TEMPLATE # This import is correct for the new structure

def report_finalizer_agent(aggregated_data, company_name="ABC Private Limited"):
    """
    AGENT 5: Builds the final Excel report with high-fidelity styling.
    Returns the file as in-memory bytes on success, or None on failure.
    """
    print("\n--- Agent 5 (Report Finalizer): Building styled report... ---")
    try:
        wb = Workbook()
        wb.remove(wb.active)
        
        # Define styles for the report
        company_title_font = Font(name='Calibri', size=16, bold=True, color="0070C0")
        sheet_title_font = Font(name='Calibri', size=14, bold=True)
        header_font = Font(name='Calibri', size=11, bold=True)
        subheader_font = Font(name='Calibri', size=11, bold=True)
        total_font = Font(name='Calibri', size=11, bold=True)
        item_font = Font(name='Calibri', size=11)
        header_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
        thin_side = Side(style='thin', color="000000")
        top_border = Border(top=thin_side)
        bottom_border = Border(bottom=thin_side)
        number_format = '#,##0.00;(#,##0.00);"-"'

        def build_styled_vertical_sheet(ws, sheet_name, template_data):
            ws.title = sheet_name
            ws.column_dimensions['A'].width = 3
            ws.column_dimensions['B'].width = 5
            ws.column_dimensions['C'].width = 45
            ws.column_dimensions['D'].width = 8
            ws.column_dimensions['E'].width = 20
            ws.column_dimensions['F'].width = 20
            
            ws.merge_cells('B1:F1')
            cell = ws['B1']
            cell.value = company_name
            cell.font = company_title_font
            cell.alignment = Alignment(horizontal='center')
            
            ws.merge_cells('B2:F2')
            cell = ws['B2']
            cell.value = sheet_name
            cell.font = sheet_title_font
            cell.alignment = Alignment(horizontal='center')
            
            row = 4
            headers = ["", "Particulars", "Note", "As at March 31, 2025", "As at March 31, 2024"]
            for col, text in enumerate(headers, 2):
                cell = ws.cell(row, col, text)
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center')
                cell.border = bottom_border
            row += 1
            
            for idx, desc, note_key, line_type in template_data:
                cells = [ws.cell(row, c) for c in range(2, 7)]
                
                if line_type == 'header':
                    ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=6)
                    cells[0].value = desc
                    cells[0].font = header_font
                    cells[0].fill = header_fill
                elif line_type == 'sub_header':
                    ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=6)
                    cells[1].value = desc
                    cells[1].font = subheader_font
                elif line_type in ['item', 'item_no_alpha']:
                    cells[0].value = idx if line_type == 'item' else ""
                    cells[1].value = desc
                    cells[2].value = note_key
                    cells[2].alignment = Alignment(horizontal='center')
                    
                    amount_cy = aggregated_data.get(note_key, {}).get('total', {}).get('CY', 0)
                    amount_py = aggregated_data.get(note_key, {}).get('total', {}).get('PY', 0)
                    
                    cells[3].value = amount_cy
                    cells[3].number_format = number_format
                    cells[4].value = amount_py
                    cells[4].number_format = number_format
                elif line_type == 'total':
                    ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=4)
                    cells[0].value = desc
                    cells[0].font = total_font
                    
                    total_cy = sum(aggregated_data.get(n, {}).get('total', {}).get('CY', 0) for n in note_key)
                    total_py = sum(aggregated_data.get(n, {}).get('total', {}).get('PY', 0) for n in note_key)
                    
                    cells[3].value = total_cy
                    cells[3].font = total_font
                    cells[3].number_format = number_format
                    cells[4].value = total_py
                    cells[4].font = total_font
                    cells[4].number_format = number_format
                    
                    for c in range(2, 7):
                        ws.cell(row, c).border = top_border
                
                row += 1
                if line_type == 'spacer':
                    row += 1

        # Build the main sheets
        build_styled_vertical_sheet(wb.create_sheet("Balance Sheet", 0), "Balance Sheet", MASTER_TEMPLATE["Balance Sheet"])
        build_styled_vertical_sheet(wb.create_sheet("Profit and Loss", 1), "Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])
        
        # (Note sheets are omitted for simplicity in this version, but can be added back)

        wb.active = 0
        output_buffer = io.BytesIO()
        wb.save(output_buffer)
        print("✅ Report Finalizer SUCCESS: Report generated.")
        return output_buffer.getvalue()

    except Exception as e:
        traceback.print_exc()
        print(f"❌ Report Finalizer FAILED: {e}")
        return None