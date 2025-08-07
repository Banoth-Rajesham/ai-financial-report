# PASTE THIS ENTIRE, COMPLETE CODE BLOCK INTO: agent_5_reporter.py

import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# (I have added back the MASTER_TEMPLATE import)
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def set_styles(ws):
    """Applies professional styling to a worksheet."""
    # Headers and Totals
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    total_font = Font(bold=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # Column widths
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 60
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20

    for row in ws.iter_rows():
        for cell in row:
            cell.border = thin_border
            if cell.row == 1 or cell.row == 2: # Company Name and Sheet Title
                cell.font = Font(bold=True, size=14)
                cell.alignment = Alignment(horizontal='center')
    
    # Style main data headers
    for cell in ws[4]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: This agent uses the MASTER_TEMPLATE to construct a detailed,
    multi-sheet Schedule III compliant Excel report WITH STYLING.
    """
    print("\n--- Agent 5 (Report Finalizer): Building styled report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            
            # --- 1. PROCESS BALANCE SHEET AND PROFIT & LOSS ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), 
                                         ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                
                sheet_data = []
                pbt_cy, pbt_py = 0, 0
                total_revenue_cy, total_revenue_py = 0, 0
                total_expenses_cy, total_expenses_py = 0, 0
                total_tax_cy, total_tax_py = 0, 0

                for row_template in template:
                    _, particulars, note, row_type = row_template
                    
                    row = {
                        'Particulars': particulars,
                        'Note': "" if not isinstance(note, str) or note in ["PBT", "PAT"] else note,
                        'CY': None, # Use None for placeholders
                        'PY': None
                    }

                    if row_type in ["item", "item_no_alpha"]:
                        note_str = str(note)
                        row['CY'] = aggregated_data.get(note_str, {}).get('total', {}).get('CY', 0)
                        row['PY'] = aggregated_data.get(note_str, {}).get('total', {}).get('PY', 0)
                    
                    elif row_type == "total" and isinstance(note, list):
                        row['CY'], row['PY'] = 0, 0
                        for note_to_sum in note:
                            row['CY'] += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('CY', 0)
                            row['PY'] += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('PY', 0)
                        
                        if particulars.startswith("Total Revenue"):
                            total_revenue_cy, total_revenue_py = row['CY'], row['PY']
                        if particulars == "Total Expenses":
                            total_expenses_cy, total_expenses_py = row['CY'], row['PY']
                        if particulars.startswith("Total Tax Expense"):
                            total_tax_cy, total_tax_py = row['CY'], row['PY']

                    elif note == "PBT":
                        pbt_cy = total_revenue_cy - total_expenses_cy
                        pbt_py = total_revenue_py - total_expenses_py
                        row['CY'], row['PY'] = pbt_cy, pbt_py

                    elif note == "PAT":
                        row['CY'] = pbt_cy - total_tax_cy
                        row['PY'] = pbt_py - total_tax_py

                    sheet_data.append(row)

                df = pd.DataFrame(sheet_data).rename(columns={'CY': 'As at March 31, 2025', 'PY': 'As at March 31, 2024'})
                df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=3)
                
                ws = writer.sheets[sheet_name]
                ws.merge_cells('A1:E1')
                ws['A1'] = company_name
                ws.merge_cells('A2:E2')
                ws['A2'] = sheet_name
                set_styles(ws)

            # --- 2. PROCESS ALL NOTES ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info = NOTES_STRUCTURE_AND_MAPPING[note_num_str]
                note_data = aggregated_data.get(note_num_str)
                if note_data and note_data.get('sub_items'):
                    sheet_name = f'Note {note_num_str}'
                    note_title = note_info['title']

                    note_df_data = []
                    
                    def process_sub_items(items, level=0):
                        for key, value in items.items():
                            indent = ' ' * (level * 4)
                            if isinstance(value, dict) and 'CY' in value and 'PY' in value:
                                note_df_data.append({
                                    'Particulars': indent + key,
                                    'As at March 31, 2025': value.get('CY', 0),
                                    'As at March 31, 2024': value.get('PY', 0)
                                })
                            elif isinstance(value, dict):
                                note_df_data.append({'Particulars': indent + key, 'As at March 31, 2025': None, 'As at March 31, 2024': None})
                                process_sub_items(value, level + 1)

                    process_sub_items(note_data['sub_items'])
                    
                    note_df = pd.DataFrame(note_df_data)
                    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY', 0), 'As at March 31, 2024': note_data['total'].get('PY', 0)}])
                    note_df = pd.concat([note_df, total_row], ignore_index=True)
                    
                    note_df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=1)
                    ws_note = writer.sheets[sheet_name]
                    ws_note.merge_cells('A1:C1')
                    ws_note['A1'] = f'Note {note_num_str}: {note_title}'
                    # Basic styling for notes
                    ws_note.column_dimensions['A'].width = 60
                    ws_note.column_dimensions['B'].width = 20
                    ws_note.column_dimensions['C'].width = 20
                    ws_note['A1'].font = Font(bold=True, size=12)


        print("✅ Report Finalizer SUCCESS: Report generated with styling.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None
