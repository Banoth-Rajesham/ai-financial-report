# ==============================================================================
# FILE: agents/agent_5_reporter.py
# ==============================================================================
import pandas as pd
import io
import traceback
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """Constructs the final, styled Excel report."""
    print("\n--- Agent 5 (Report Finalizer): Building styled report... ---")
    try:
        output_buffer = io.BytesIO()
        with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
            # Main Sheets
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                df = create_main_sheet_df(aggregated_data, template, particulars_header=sheet_name)
                df.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
            # Notes Sheets
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_data = aggregated_data.get(note_num_str)
                if not (note_data and note_data.get('sub_items')): continue
                df = create_note_sheet_df(note_data)
                df.to_excel(writer, sheet_name=f'Note {note_num_str}', index=False, header=True)
        
        output_buffer.seek(0)
        wb = load_workbook(output_buffer)

        # Apply Styling
        apply_main_sheet_styling(wb["Balance Sheet"], MASTER_TEMPLATE["Balance Sheet"], company_name)
        apply_main_sheet_styling(wb["Profit and Loss"], MASTER_TEMPLATE["Profit and Loss"], company_name)
        for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
            if f'Note {note_num_str}' in wb.sheetnames:
                note_info = NOTES_STRUCTURE_AND_MAPPING[note_num_str]
                note_title = f'Note {note_num_str}: {note_info["title"]}'
                apply_note_sheet_styling(wb[f'Note {note_num_str}'], note_title)

        final_buffer = io.BytesIO()
        wb.save(final_buffer)
        print("✅ Report Finalizer SUCCESS: Report generated.")
        return final_buffer.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}")
        traceback.print_exc()
        return None

def create_main_sheet_df(aggregated_data, template, particulars_header=""):
    """Helper to create the DataFrame for main sheets before styling."""
    sheet_data = []
    calc_totals = {}
    for row_template in template:
        col_a, particulars, note, row_type = row_template
        if row_type == "header_col": continue
        row_data = {" ": col_a, "Particulars": particulars, "Note": "" if not isinstance(note, str) else note, "As at March 31, 2025": None, "As at March 31, 2024": None}
        
        def get_val(key, year):
            key = str(key)
            # Special handling for "Changes in Inventory" in P&L expenses
            if key == '16' and "Expenses" in particulars_header: 
                opening_stock = aggregated_data.get('16', {}).get('total', {}).get('PY', 0)
                closing_stock = aggregated_data.get('16', {}).get('total', {}).get('CY', 0)
                return closing_stock - opening_stock
            return aggregated_data.get(key, {}).get('total', {}).get(year, 0)

        if row_type in ["item", "item_no_alpha"]:
            row_data['As at March 31, 2025'] = get_val(note, 'CY')
            row_data['As at March 31, 2024'] = get_val(note, 'PY')
        elif row_type == "total" and isinstance(note, list):
            cy_val = sum(get_val(n, 'CY') for n in note)
            py_val = sum(get_val(n, 'PY') for n in note)
            row_data['As at March 31, 2025'], row_data['As at March 31, 2024'] = cy_val, py_val
            if "Total Revenue" in particulars: calc_totals['rev_cy'], calc_totals['rev_py'] = cy_val, py_val
            if "Total Expenses" in particulars: calc_totals['exp_cy'], calc_totals['exp_py'] = cy_val, py_val
            if "Total Tax Expense" in particulars: calc_totals['tax_cy'], calc_totals['tax_py'] = cy_val, py_val
        elif note == "PBT":
            pbt_cy = calc_totals.get('rev_cy', 0) - calc_totals.get('exp_cy', 0)
            pbt_py = calc_totals.get('rev_py', 0) - calc_totals.get('exp_py', 0)
            row_data['As at March 31, 2025'], row_data['As at March 31, 2024'] = pbt_cy, pbt_py
            calc_totals['pbt_cy'], calc_totals['pbt_py'] = pbt_cy, pbt_py
        elif note == "PAT":
            pat_cy = calc_totals.get('pbt_cy', 0) - calc_totals.get('tax_cy', 0)
            pat_py = calc_totals.get('pbt_py', 0) - calc_totals.get('tax_py', 0)
            row_data['As at March 31, 2025'], row_data['As at March 31, 2024'] = pat_cy, pat_py
        sheet_data.append(row_data)
    return pd.DataFrame(sheet_data)

def create_note_sheet_df(note_data):
    """Helper to create the DataFrame for note sheets."""
    note_df_data = []
    def process_sub_items(items, level=0):
        for key, value in items.items():
            indent = '    ' * level
            if isinstance(value, dict) and 'CY' in value and 'PY' in value:
                note_df_data.append({'Particulars': indent + key, 'As at March 31, 2025': value.get('CY', 0), 'As at March 31, 2024': value.get('PY', 0)})
            elif isinstance(value, dict):
                note_df_data.append({'Particulars': indent + key, 'As at March 31, 2025': None, 'As at March 31, 2024': None})
                process_sub_items(value, level + 1)
    process_sub_items(note_data['sub_items'])
    note_df = pd.DataFrame(note_df_data)
    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY', 0), 'As at March 31, 2024': note_data['total'].get('PY', 0)}])
    return pd.concat([note_df, total_row], ignore_index=True)

def apply_main_sheet_styling(ws, template, company_name):
    """Applies consistent styling to main report sheets."""
    ws.insert_rows(1, 3)
    ws.column_dimensions['B'].width = 65; ws.column_dimensions['C'].width = 8
    ws.column_dimensions['D'].width = 20; ws.column_dimensions['E'].width = 20
    title_font = Font(name='Calibri', size=16, bold=True, color="0070C0")
    subtitle_font = Font(name='Calibri', size=14, bold=True)
    header_font = Font(name='Calibri', size=11, bold=True)
    bold_font = Font(name='Calibri', size=11, bold=True)
    currency_format = '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)'
    
    ws.merge_cells('B1:E1'); cell=ws['B1']; cell.value=company_name; cell.font=title_font; cell.alignment=Alignment(horizontal='center')
    ws.merge_cells('B2:E2'); cell=ws['B2']; cell.value=ws.title; cell.font=subtitle_font; cell.alignment=Alignment(horizontal='center')
    for cell in ws[4]:
        cell.font = header_font
        cell.border = Border(bottom=Side(style='thin'))
        cell.alignment = Alignment(horizontal='center')
    for i, row_template in enumerate(template):
        row_num = i + 5
        if row_num > ws.max_row: continue
        row_type = row_template[3]
        if row_type in ['header', 'sub_header', 'total']:
            for cell in ws[row_num]: cell.font = bold_font
        if row_type == 'total':
             for cell in ws[row_num]: cell.border = Border(top=Side(style='thin'), bottom=Side(style='double'))
        for col_letter in ['D', 'E']:
            if isinstance(ws[f'{col_letter}{row_num}'].value, (int, float)):
                ws[f'{col_letter}{row_num}'].number_format = currency_format

def apply_note_sheet_styling(ws, note_title):
    """Applies consistent styling to note sheets."""
    ws.insert_rows(1)
    ws.column_dimensions['A'].width = 65
    ws.column_dimensions['B'].width = 20; ws.column_dimensions['C'].width = 20
    title_font = Font(bold=True, size=14); header_font = Font(bold=True)
    total_font = Font(bold=True); sub_header_font = Font(bold=True)
    currency_format = '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)'
    ws.merge_cells('A1:C1'); ws['A1'].value = note_title; ws['A1'].font = title_font
    for cell in ws[2]: cell.font = header_font
    for row in ws.iter_rows(min_row=3, max_col=3):
        particulars_cell = row[0]
        if particulars_cell.value and row[1].value is None: particulars_cell.font = sub_header_font
        if particulars_cell.value == 'Total':
            for cell in row: cell.font = total_font; cell.border = Border(top=Side(style='thin'))
        for cell in row[1:]:
            if isinstance(cell.value, (int, float)): cell.number_format = currency_format
