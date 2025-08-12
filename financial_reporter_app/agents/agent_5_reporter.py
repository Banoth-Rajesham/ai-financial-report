# PASTE THIS ENTIRE, COMPLETE, AND FINAL CODE BLOCK INTO: agent_5_reporter.py

import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

# ================================================================================= #
# == POWERFUL STYLING ENGINE: This part makes the report look professional       == #
# ================================================================================= #

def apply_main_sheet_styling(ws, template, company_name):
    """Applies the beautiful, professional styling to the Balance Sheet and P&L."""
    
    # --- Define Styles ---
    header_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid") # Light Grey
    total_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid") # Light Blue
    header_font = Font(bold=True)
    bold_font = Font(bold=True)
    title_font = Font(size=14, bold=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'

    # --- Set Column Widths ---
    ws.column_dimensions['A'].width = 4
    ws.column_dimensions['B'].width = 60
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20
    
    # --- Write and Style Titles ---
    ws.merge_cells('A1:E1')
    ws['A1'] = company_name
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A2:E2')
    ws['A2'] = ws.title
    ws['A2'].font = Font(size=12, bold=True)
    ws['A2'].alignment = Alignment(horizontal='center')

    # --- Apply styles to all cells based on template ---
    for row_idx, row_template in enumerate(template, start=4):
        row_type = row_template[3]
        current_row = ws[row_idx]

        for cell in current_row:
            cell.border = thin_border # Apply border to all cells in the range
        
        if row_type == 'header_col':
            for cell in current_row:
                cell.font = bold_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center')
        elif row_type in ['header', 'sub_header']:
            ws[f'B{row_idx}'].font = bold_font
        elif row_type == 'total':
            for cell in current_row:
                cell.font = bold_font
                cell.fill = total_fill
            ws[f'B{row_idx}'].alignment = Alignment(horizontal='right')
        
        # Apply currency format to number columns
        for col_letter in ['D', 'E']:
            if isinstance(ws[f'{col_letter}{row_idx}'].value, (int, float)):
                ws[f'{col_letter}{row_idx}'].number_format = currency_format

def apply_note_sheet_styling(ws, note_title):
    """Applies professional styling to a Note sheet."""
    header_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    title_font = Font(bold=True, size=14)
    header_font = Font(bold=True)
    total_font = Font(bold=True)
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'

    ws.column_dimensions['A'].width = 65
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20

    ws.merge_cells('A1:C1')
    ws['A1'] = note_title
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')
    
    header_row = ws[2]
    for cell in header_row:
        cell.fill = header_fill
        cell.font = header_font
    
    for row in ws.iter_rows(min_row=3, max_col=3):
        is_total_row = (row[0].value == 'Total')
        for cell in row:
            if cell.column > 1 and isinstance(cell.value, (int, float)):
                cell.number_format = currency_format
            if is_total_row:
                cell.font = total_font
                cell.border = Border(top=Side(style='thin'))

# --- MAIN AGENT FUNCTION ---
def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: This agent uses the MASTER_TEMPLATE to construct a detailed,
    multi-sheet Schedule III compliant Excel report WITH PROFESSIONAL STYLING.
    """
    print("\n--- Agent 5 (Report Finalizer): Building styled report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            
            # --- PROCESS AND STYLE BALANCE SHEET AND PROFIT & LOSS ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), 
                                         ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                
                # Create DataFrame from template
                df_data = []
                for row_template in template:
                    df_data.append({
                        ' ': row_template[0],
                        'Particulars': row_template[1],
                        'Note': row_template[2],
                        '__type__': row_template[3] # Helper column for styling
                    })
                df = pd.DataFrame(df_data)
                df['As at March 31, 2025'] = 0.0
                df['As at March 31, 2024'] = 0.0

                # Calculate values
                pbt_cy, pbt_py = 0, 0
                total_revenue_cy, total_revenue_py = 0, 0
                total_expenses_cy, total_expenses_py = 0, 0
                total_tax_cy, total_tax_py = 0, 0

                for index, row in df.iterrows():
                    note = row['Note']
                    row_type = row['__type__']
                    
                    if row_type in ["item", "item_no_alpha"]:
                        note_str = str(note)
                        df.loc[index, 'As at March 31, 2025'] = aggregated_data.get(note_str, {}).get('total', {}).get('CY', 0)
                        df.loc[index, 'As at March 31, 2024'] = aggregated_data.get(note_str, {}).get('total', {}).get('PY', 0)
                    elif row_type == "total" and isinstance(note, list):
                        cy_val, py_val = 0, 0
                        for note_to_sum in note:
                            cy_val += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('CY', 0)
                            py_val += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('PY', 0)
                        df.loc[index, 'As at March 31, 2025'], df.loc[index, 'As at March 31, 2024'] = cy_val, py_val
                        if row['Particulars'].startswith("Total Revenue"): total_revenue_cy, total_revenue_py = cy_val, py_val
                        if row['Particulars'] == "Total Expenses": total_expenses_cy, total_expenses_py = cy_val, py_val
                        if row['Particulars'].startswith("Total Tax Expense"): total_tax_cy, total_tax_py = cy_val, py_val
                    elif note == "PBT":
                        pbt_cy = total_revenue_cy - total_expenses_cy
                        pbt_py = total_revenue_py - total_expenses_py
                        df.loc[index, 'As at March 31, 2025'], df.loc[index, 'As at March 31, 2024'] = pbt_cy, pbt_py
                    elif note == "PAT":
                        df.loc[index, 'As at March 31, 2025'] = pbt_cy - total_tax_cy
                        df.loc[index, 'As at March 31, 2024'] = pbt_py - total_tax_py

                # Write to Excel and apply styles
                final_df = df[[' ', 'Particulars', 'Note', 'As at March 31, 2025', 'As at March 31, 2024']]
                final_df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=3)
                ws = writer.sheets[sheet_name]
                apply_main_sheet_styling(ws, template, company_name)


            # --- PROCESS AND STYLE ALL NOTES ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info = NOTES_STRUCTURE_AND_MAPPING[note_num_str]
                note_data = aggregated_data.get(note_num_str)
                if note_data and note_data.get('sub_items'):
                    sheet_name = f'Note {note_num_str}'
                    note_title = note_info['title']
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
                    note_df = pd.concat([note_df, total_row], ignore_index=True)
                    
                    note_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                    ws_note = writer.sheets[sheet_name]
                    apply_note_sheet_styling(ws_note, f'Note {note_num_str}: {note_title}')

        print("✅ Report Finalizer SUCCESS: Report generated with styling.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None
