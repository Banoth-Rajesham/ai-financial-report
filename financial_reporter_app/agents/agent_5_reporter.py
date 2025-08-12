# PASTE THIS ENTIRE, COMPLETE, AND FINAL CODE BLOCK INTO: agent_5_reporter.py

import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

# ================================================================================= #
# == POWERFUL STYLING ENGINE: This part makes the report look professional       == #
# ================================================================================= #

def apply_main_sheet_styling(ws, template, aggregated_data, company_name):
    """
    Builds the sheet cell-by-cell based on the template, applying styles as it goes.
    This guarantees the output matches the desired format exactly.
    """
    # --- Define Styles ---
    header_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid") # Light Grey
    total_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid") # Light Blue from your image
    header_font = Font(bold=True)
    bold_font = Font(bold=True)
    title_font = Font(size=14, bold=True)
    thin_border_side = Side(style='thin')
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    # This format will show commas and a dash for zero
    currency_format = '#,##0;(#,##0);"-"'

    # --- Set Column Widths ---
    ws.column_dimensions['A'].width = 4
    ws.column_dimensions['B'].width = 60
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20
    
    # --- Write Titles ---
    ws.merge_cells('A1:E1')
    ws['A1'] = company_name
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A2:E2')
    ws['A2'] = ws.title
    ws['A2'].font = Font(size=12, bold=True)
    ws['A2'].alignment = Alignment(horizontal='center')

    # --- Process template row-by-row ---
    pbt_cy, pbt_py = 0, 0
    total_revenue_cy, total_revenue_py = 0, 0
    total_expenses_cy, total_expenses_py = 0, 0
    total_tax_cy, total_tax_py = 0, 0

    for row_idx, row_template in enumerate(template, start=4):
        col_a, particulars, note, row_type = row_template
        
        # Write static text from template
        ws.cell(row=row_idx, column=1, value=col_a)
        ws.cell(row=row_idx, column=2, value=particulars)
        ws.cell(row=row_idx, column=3, value=note if isinstance(note, str) and note not in ["PBT", "PAT"] else "")

        # Calculate and write dynamic values
        cy_val, py_val = None, None
        if row_type in ["item", "item_no_alpha"]:
            note_str = str(note)
            cy_val = aggregated_data.get(note_str, {}).get('total', {}).get('CY', 0)
            py_val = aggregated_data.get(note_str, {}).get('total', {}).get('PY', 0)
        elif row_type == "total" and isinstance(note, list):
            cy_val, py_val = 0, 0
            for note_to_sum in note:
                cy_val += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('CY', 0)
                py_val += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('PY', 0)
            
            if particulars.startswith("Total Revenue"): total_revenue_cy, total_revenue_py = cy_val, py_val
            if particulars == "Total Expenses": total_expenses_cy, total_expenses_py = cy_val, py_val
            if particulars.startswith("Total Tax Expense"): total_tax_cy, total_tax_py = cy_val, py_val
        elif note == "PBT":
            pbt_cy = total_revenue_cy - total_expenses_cy
            pbt_py = total_revenue_py - total_expenses_py
            cy_val, py_val = pbt_cy, pbt_py
        elif note == "PAT":
            cy_val = pbt_cy - total_tax_cy
            py_val = pbt_py - total_tax_py
        
        ws.cell(row=row_idx, column=4, value=cy_val).number_format = currency_format
        ws.cell(row=row_idx, column=5, value=py_val).number_format = currency_format

        # Apply styles based on row type
        current_row = ws[row_idx]
        if row_type == 'header_col':
            for cell in current_row: cell.font = bold_font; cell.fill = header_fill
        elif row_type in ['header', 'sub_header']:
            ws[f'B{row_idx}'].font = bold_font
        elif row_type == 'total':
            for cell in current_row: cell.font = bold_font; cell.fill = total_fill
            ws[f'B{row_idx}'].alignment = Alignment(horizontal='right')
        
        for cell in current_row:
             cell.border = thin_border

def apply_note_sheet_styling(ws, note_title):
    """Applies professional styling to a Note sheet."""
    header_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    total_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
    title_font = Font(bold=True, size=14)
    header_font = Font(bold=True)
    total_font = Font(bold=True)
    currency_format = '#,##0;(#,##0);"-"'
    thin_border_side = Side(style='thin')
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    ws.column_dimensions['A'].width = 65
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20

    ws.merge_cells('A1:C1')
    ws['A1'] = note_title
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')
    
    for cell in ws[2]: # Header row
        cell.fill = header_fill
        cell.font = header_font
    
    for row in ws.iter_rows(min_row=2, max_col=3):
        is_total_row = (row[0].value == 'Total')
        for cell in row:
            cell.border = thin_border
            if cell.column > 1 and isinstance(cell.value, (int, float)):
                cell.number_format = currency_format
            if is_total_row:
                cell.font = total_font
                cell.fill = total_fill


# --- MAIN AGENT FUNCTION ---
def report_finalizer_agent(aggregated_data, company_name):
    print("\n--- Agent 5 (Report Finalizer): Building styled report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), 
                                         ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                ws = writer.book.create_sheet(sheet_name)
                writer.sheets[sheet_name] = ws
                apply_styles_and_write_data(ws, template, aggregated_data, company_name)
            
            if 'Sheet' in writer.book.sheetnames:
                del writer.book['Sheet']

            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info = NOTES_STRUCTURE_AND_MAPPING[note_num_str]
                note_data = aggregated_data.get(note_num_str)
                sheet_name = f'Note {note_num_str}'
                note_title = f'Note {note_num_str}: {note_info["title"]}'

                df_data = []
                def process_sub_items(items, level=0):
                    for key, value in items.items():
                        indent = '    ' * level
                        if isinstance(value, dict) and 'CY' in value and 'PY' in value:
                            df_data.append({'Particulars': indent + key, 'As at March 31, 2025': value.get('CY', 0), 'As at March 31, 2024': value.get('PY', 0)})
                        elif isinstance(value, dict):
                            df_data.append({'Particulars': indent + key, 'As at March 31, 2025': None, 'As at March 31, 2024': None})
                            process_sub_items(value, level + 1)
                
                if note_data and note_data.get('sub_items'):
                    process_sub_items(note_data['sub_items'])
                
                df = pd.DataFrame(df_data)
                
                if note_data:
                    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY', 0), 'As at March 31, 2024': note_data['total'].get('PY', 0)}])
                    df = pd.concat([df, total_row], ignore_index=True)
                
                df_to_write = df[['Particulars', 'As at March 31, 2025', 'As at March 31, 2024']] if not df.empty else pd.DataFrame([{}])
                df_to_write.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                ws_note = writer.sheets[sheet_name]
                apply_note_sheet_styling(ws_note, note_title)

        print("✅ Report Finalizer SUCCESS: Report generated with styling.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None
