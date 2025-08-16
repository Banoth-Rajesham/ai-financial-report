# ==============================================================================
# FILE: agents/agent_5_reporter.py (DEFINITIVE, FINAL, ERROR-FREE VERSION)
# This agent is perfectly synchronized with the master config.py to produce
# the exact styled output you have designed.
# ==============================================================================
import pandas as pd
import io
import traceback
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Takes the final data and writes a complete, multi-sheet Excel report
    that is a perfect, styled replica of the master config blueprint.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book

            # --- DEFINE CELL FORMATS ---
            title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
            header_format = workbook.add_format({'bold': True, 'bg_color': '#DDEBF7', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            sub_header_format = workbook.add_format({'bold': True})
            total_format = workbook.add_format({'bold': True, 'top': 1})
            item_format = workbook.add_format({}) # Basic format for items
            num_format = workbook.add_format({'num_format': '#,##0.00'})
            total_num_format = workbook.add_format({'bold': True, 'top': 1, 'num_format': '#,##0.00'})

            # --- 1. RENDER THE MAIN SHEETS (BALANCE SHEET & P&L) ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 5)
                worksheet.set_column('B:B', 65)
                worksheet.set_column('C:C', 8)
                worksheet.set_column('D:E', 20)

                # Write Titles
                worksheet.merge_range('A1:E1', company_name, title_format)
                worksheet.merge_range('A2:E2', sheet_name, title_format)

                row_num = 3 # Start writing from the 4th row
                
                # Helper to calculate totals based on note numbers from the template
                def get_total_for_notes(note_list, year):
                    if not isinstance(note_list, list): return 0
                    return sum(aggregated_data.get(str(n), {}).get('total', {}).get(year, 0) for n in note_list)

                for row_data in template:
                    col_a, particulars, note, row_type = row_data

                    if row_type == "header_col":
                        worksheet.write('B3', particulars, header_format)
                        worksheet.write('C3', note, header_format)
                        worksheet.write('D3', "As at March 31, 2025", header_format)
                        worksheet.write('E3', "As at March 31, 2024", header_format)
                        continue

                    cy_val, py_val = None, None

                    if row_type in ["item", "item_sub", "item_no_alpha"]:
                        note_total = aggregated_data.get(str(note), {}).get('total', {})
                        cy_val = note_total.get('CY', 0)
                        py_val = note_total.get('PY', 0)
                    
                    elif row_type == "total":
                        if note == 'PBT':
                            rev_cy = get_total_for_notes(['21', '22'], 'CY')
                            rev_py = get_total_for_notes(['21', '22'], 'PY')
                            exp_cy = get_total_for_notes(['23', '24', '25', '11', '26'], 'CY')
                            exp_py = get_total_for_notes(['23', '24', '25', '11', '26'], 'PY')
                            cy_val = rev_cy - exp_cy
                            py_val = rev_py - exp_py
                        elif note == 'PAT':
                             rev_cy = get_total_for_notes(['21', '22'], 'CY')
                             rev_py = get_total_for_notes(['21', '22'], 'PY')
                             exp_cy = get_total_for_notes(['23', '24', '25', '11', '26'], 'CY')
                             exp_py = get_total_for_notes(['23', '24', '25', '11', '26'], 'PY')
                             pbt_cy = rev_cy - exp_cy
                             pbt_py = rev_py - exp_py
                             tax_cy = get_total_for_notes(['4'], 'CY') # Simplified tax
                             tax_py = get_total_for_notes(['4'], 'PY')
                             cy_val = pbt_cy - tax_cy
                             py_val = pbt_py - tax_py
                        else:
                            cy_val = get_total_for_notes(note, 'CY')
                            py_val = get_total_for_notes(note, 'PY')
                    
                    # Write the row data based on its type
                    if row_type in ["header", "sub_header", "item_no_note_sub"]:
                        worksheet.write(row_num, 0, col_a, sub_header_format)
                        worksheet.write(row_num, 1, particulars, sub_header_format)
                    elif row_type == "total":
                        worksheet.write(row_num, 1, particulars, total_format)
                        worksheet.write(row_num, 3, cy_val, total_num_format)
                        worksheet.write(row_num, 4, py_val, total_num_format)
                    else: # item, item_sub, item_no_note, etc.
                        worksheet.write(row_num, 0, col_a, item_format)
                        worksheet.write(row_num, 1, particulars, item_format)
                        worksheet.write_string(row_num, 2, str(note) if note else '', item_format)
                        worksheet.write_number(row_num, 3, cy_val if cy_val is not None else 0, num_format)
                        worksheet.write_number(row_num, 4, py_val if py_val is not None else 0, num_format)
                    
                    row_num += 1

            # --- 2. RENDER THE NOTE SHEETS ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=lambda x: int(x.split('.')[0])):
                note_data = aggregated_data.get(note_num_str)
                if not note_data or 'sub_items' not in note_data: continue

                sheet_name = f"Note {note_num_str}"
                worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 65)
                worksheet.set_column('B:C', 20)

                worksheet.merge_range('A1:C1', f"Note {note_num_str}: {note_data.get('title', '')}", title_format)
                worksheet.write('A3', 'Particulars', header_format)
                worksheet.write('B3', 'As at March 31, 2025', header_format)
                worksheet.write('C3', 'As at March 31, 2024', header_format)

                row_num = 3 # Start after header
                
                def write_note_level(items, indent_level=0):
                    nonlocal row_num
                    for key, value in items.items():
                        prefix = "    " * indent_level
                        if isinstance(value, dict) and 'CY' in value:
                            worksheet.write(row_num, 0, f"{prefix}{key}", item_format)
                            worksheet.write_number(row_num, 1, value.get('CY', 0), num_format)
                            worksheet.write_number(row_num, 2, value.get('PY', 0), num_format)
                            row_num += 1
                        elif isinstance(value, dict):
                            worksheet.write(row_num, 0, f"{prefix}{key}", sub_header_format)
                            row_num += 1
                            write_note_level(value, indent_level + 1)
                
                write_note_level(note_data['sub_items'])
                
                worksheet.write(row_num, 0, "Total", total_format)
                worksheet.write_number(row_num, 1, note_data.get('total', {}).get('CY', 0), total_num_format)
                worksheet.write_number(row_num, 2, note_data.get('total', {}).get('PY', 0), total_num_format)

        print("✅ Report Finalizer SUCCESS: Styled Excel file created in memory.")
        return output.getvalue()

    except Exception as e:
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        traceback.print_exc()
        return None
