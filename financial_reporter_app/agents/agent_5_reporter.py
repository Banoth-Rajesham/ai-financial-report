# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: agent_5_reporter.py
# ==============================================================================
import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# THIS IS THE PERMANENT FIX: Use the full, absolute path now that app.py sets the root path
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def apply_main_sheet_styling(ws, template, company_name):
    """Applies beautiful, professional styling to the Balance Sheet and P&L."""
    title_font = Font(bold=True, size=16); subtitle_font = Font(bold=True, size=12)
    header_font = Font(bold=True); bold_font = Font(bold=True)
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    ws.column_dimensions['A'].width = 5; ws.column_dimensions['B'].width = 65; ws.column_dimensions['C'].width = 8
    ws.column_dimensions['D'].width = 20; ws.column_dimensions['E'].width = 20
    ws.merge_cells('A1:E1'); ws['A1'] = company_name; ws['A1'].font = title_font; ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A2:E2'); ws['A2'] = ws.title; ws['A2'].font = subtitle_font; ws['A2'].alignment = Alignment(horizontal='center')
    for cell in ws[4]: cell.font = header_font; cell.alignment = Alignment(horizontal='center')
    for i, row_template in enumerate(template):
        row_num = i + 5
        if row_template[3] in ['header', 'sub_header']: ws[f'B{row_num}'].font = bold_font
        elif row_template[3] == 'total':
            for cell in ws[row_num]: cell.font = bold_font
        for col_letter in ['D', 'E']:
            if ws[f'{col_letter}{row_num}'].value is not None: ws[f'{col_letter}{row_num}'].number_format = currency_format

def apply_note_sheet_styling(ws):
    """Applies professional styling to a Note sheet."""
    header_font = Font(bold=True, color="FFFFFF"); title_font = Font(bold=True, size=14); total_font = Font(bold=True)
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    ws.column_dimensions['A'].width = 65; ws.column_dimensions['B'].width = 20; ws.column_dimensions['C'].width = 20
    ws.merge_cells('A1:C1'); ws['A1'].font = title_font
    for cell in ws[2]: cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid"); cell.font = header_font
    for row_idx, row in enumerate(ws.iter_rows(min_row=3, max_col=3), start=3):
        is_total = (str(ws[f'A{row_idx}'].value).strip().lower() == 'total')
        for cell in row:
            if cell.column > 1: cell.number_format = currency_format
            if is_total: cell.font = total_font; cell.border = Border(top=Side(style='thin'))

def report_finalizer_agent(aggregated_data, company_name):
    """AGENT 5: Constructs a detailed, styled, multi-sheet Excel report."""
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            def get_val(note_id, year):
                if note_id == "16_change": return (aggregated_data.get('16', {}).get('total', {}).get('CY', 0) or 0) - (aggregated_data.get('16', {}).get('total', {}).get('PY', 0) or 0) if year == 'CY' else 0
                if note_id == "11_dep": return aggregated_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get(year, 0)
                return aggregated_data.get(str(note_id), {}).get('total', {}).get(year, 0)
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                rows = []
                for r_template in template:
                    row = {' ': r_template[0], 'Particulars': r_template[1], 'Note': r_template[2] if isinstance(r_template[2], str) else "", 'CY': None, 'PY': None}
                    if r_template[3] in ["item", "item_no_alpha"]: row['CY'], row['PY'] = get_val(r_template[2], 'CY'), get_val(r_template[2], 'PY')
                    rows.append(row)
                df = pd.DataFrame(rows).rename(columns={'CY': 'As at March 31, 2025', 'PY': 'As at March 31, 2024'})
                for i, r_template in enumerate(template):
                    if r_template[3] == 'total':
                        notes_to_sum = r_template[2]
                        if isinstance(notes_to_sum, list):
                            cy_sum = df[df['Note'].isin(notes_to_sum)]['As at March 31, 2025'].sum()
                            py_sum = df[df['Note'].isin(notes_to_sum)]['As at March 31, 2024'].sum()
                            df.iloc[i, 3], df.iloc[i, 4] = cy_sum, py_sum
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=3); apply_main_sheet_styling(writer.sheets[sheet_name], template, company_name)
            for note_num in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info, note_data = NOTES_STRUCTURE_AND_MAPPING[note_num], aggregated_data.get(note_num)
                if note_data and note_data.get('sub_items'):
                    df_data, title = [], note_info['title']
                    def process(items, level=0):
                        for key, val in items.items():
                            if isinstance(val, dict) and 'CY' in val: df_data.append({'Particulars': '  '*level+key, 'CY': val.get('CY'), 'PY': val.get('PY')})
                            elif isinstance(val, dict): df_data.append({'Particulars': '  '*level+key, 'CY': None, 'PY': None}); process(val, level+1)
                    process(note_data['sub_items'])
                    df = pd.DataFrame(df_data).rename(columns={'CY': 'As at March 31, 2025', 'PY': 'As at March 31, 2024'})
                    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY'), 'As at March 31, 2024': note_data['total'].get('PY')}])
                    df = pd.concat([df, total_row], ignore_index=True)
                    sheet_name=f'Note {note_num}'; df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1); ws=writer.sheets[sheet_name]; ws['A1'].value=f'Note {note_num}: {title}'; apply_note_sheet_styling(ws)
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}"); import traceback; traceback.print_exc(); return None
