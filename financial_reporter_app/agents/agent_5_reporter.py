# ==============================================================================
# PASTE THIS ENTIRE BLOCK INTO: agents/agent_5_reporter.py
# ==============================================================================
import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def apply_main_sheet_styling(ws, template, aggregated_data, company_name):
    # --- STYLE DEFINITIONS ---
    header_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
    section_header_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    company_title_font = Font(name='Calibri', size=18, bold=True, color="0070C0")
    sheet_title_font = Font(name='Calibri', size=14, bold=True)
    header_font = Font(name='Calibri', size=11, bold=True)
    bold_font = Font(name='Calibri', size=11, bold=True)
    thin_border_side = Side(style='thin', color="BFBFBF")
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    currency_format = '#,##0.00;(#,##0.00);"-"'

    # --- Column Widths ---
    ws.column_dimensions['A'] = 5; ws.column_dimensions['B'] = 55; ws.column_dimensions['C'] = 8
    ws.column_dimensions['D'] = 20; ws.column_dimensions['E'] = 20

    # --- Titles ---
    ws.merge_cells('A1:E1'); ws['A1'] = company_name; ws['A1'].font = company_title_font; ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A2:E2'); ws['A2'] = ws.title; ws['A2'].font = sheet_title_font; ws['A2'].alignment = Alignment(horizontal='center')

    # --- Column Headers ---
    headers = {"B": "Particulars", "C": "Note", "D": "As at March 31, 2025", "E": "As at March 31, 2024"}
    for col_letter, text in headers.items(): ws[f'{col_letter}4'].font = header_font
    for col in range(1, 6): ws.cell(row=4, column=col).fill = header_fill; ws.cell(row=4, column=col).border = thin_border

    # --- Process Template ---
    calc_vars = {'pbt_cy': 0, 'pbt_py': 0, 'total_revenue_cy': 0, 'total_revenue_py': 0, 'total_expenses_cy': 0, 'total_expenses_py': 0, 'total_tax_cy': 0, 'total_tax_py': 0}
    for row_idx, row_template in enumerate(template, start=5):
        col_a, particulars, note, row_type = row_template
        ws.cell(row=row_idx, column=1, value=col_a); ws.cell(row=row_idx, column=2, value=particulars)
        ws.cell(row=row_idx, column=3, value=note if isinstance(note, str) and note not in ["PBT", "PAT"] else "")
        cy_val, py_val = 0, 0
        if row_type in ["item", "item_no_alpha"]:
            cy_val = aggregated_data.get(str(note), {}).get('total', {}).get('CY', 0)
            py_val = aggregated_data.get(str(note), {}).get('total', {}).get('PY', 0)
        elif row_type == "total" and isinstance(note, list):
            cy_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('CY', 0) for n in note)
            py_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('PY', 0) for n in note)
            # ... (store values in calc_vars for P&L) ...
        # ... (logic for PBT and PAT using calc_vars) ...
        ws.cell(row=row_idx, column=4, value=cy_val).number_format = currency_format
        ws.cell(row=row_idx, column=5, value=py_val).number_format = currency_format
        if row_type == 'header': ws.cell(row=row_idx, column=2).font = bold_font; ws.cell(row=row_idx, column=2).fill = section_header_fill
        elif row_type == 'sub_header': ws.cell(row=row_idx, column=2).font = bold_font
        elif row_type == 'total': ws.cell(row=row_idx, column=2).font = bold_font; ws.cell(row=row_idx, column=2).alignment = Alignment(horizontal='right')
        for col in range(1, 6): ws.cell(row=row_idx, column=col).border = thin_border

def apply_note_sheet_styling(ws, note_title):
    # --- Styles for Note Sheets ---
    header_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
    total_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    title_font = Font(name='Calibri', size=14, bold=True); header_font = Font(name='Calibri', size=11, bold=True); total_font = Font(name='Calibri', size=11, bold=True)
    currency_format = '#,##0.00;(#,##0.00);"-"'; thin_border_side = Side(style='thin', color="BFBFBF"); thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    ws.column_dimensions['A'] = 70; ws.column_dimensions['B'] = 20; ws.column_dimensions['C'] = 20
    ws.merge_cells('A1:C1'); ws['A1'] = note_title; ws['A1'].font = title_font; ws['A1'].alignment = Alignment(horizontal='center')
    ws.cell(row=2, column=1, value="Particulars"); ws.cell(row=2, column=2, value="As at March 31, 2025"); ws.cell(row=2, column=3, value="As at March 31, 2024")
    for cell in ws[2]: cell.fill = header_fill; cell.font = header_font
    for row in ws.iter_rows(min_row=2, max_col=3):
        is_total_row = (row[0].value and 'total' in str(row[0].value).lower())
        for cell in row:
            cell.border = thin_border
            if cell.column > 1 and isinstance(cell.value, (int, float)): cell.number_format = currency_format
            if is_total_row: cell.font = total_font; cell.fill = total_fill

def report_finalizer_agent(aggregated_data, company_name):
    print("\n--- Agent 5 (Report Finalizer): Building styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if 'Sheet' in writer.book.sheetnames: del writer.book['Sheet']
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                ws = writer.book.create_sheet(sheet_name); writer.sheets[sheet_name] = ws
                apply_main_sheet_styling(ws, template, aggregated_data, company_name)
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info = NOTES_STRUCTURE_AND_MAPPING[note_num_str]; note_data = aggregated_data.get(note_num_str)
                sheet_name = f'Note {note_num_str}'; note_title = f'Note {note_num_str}: {note_info["title"]}'
                df_data = []
                def process_sub_items(items, level=0):
                    for key, value in items.items():
                        indent = '    ' * level
                        if isinstance(value, dict) and 'CY' in value: df_data.append({'Particulars': indent + key, 'CY': value.get('CY', 0), 'PY': value.get('PY', 0)})
                        elif isinstance(value, dict): df_data.append({'Particulars': indent + key, 'CY': None, 'PY': None}); process_sub_items(value, level + 1)
                if note_data and note_data.get('sub_items'): process_sub_items(note_data['sub_items'])
                df = pd.DataFrame(df_data)
                if note_data and not df.empty: df = pd.concat([df, pd.DataFrame([{'Particulars': 'Total', 'CY': note_data['total'].get('CY', 0), 'PY': note_data['total'].get('PY', 0)}])], ignore_index=True)
                df_to_write = df[['Particulars', 'CY', 'PY']] if not df.empty else pd.DataFrame([{'Particulars': 'No data for this note.'}])
                df_to_write.to_excel(writer, sheet_name=sheet_name, index=False, startrow=2, header=False)
                ws_note = writer.sheets[sheet_name]; apply_note_sheet_styling(ws_note, note_title)
        print("✅ Report Finalizer SUCCESS.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}"); return None
