# ==============================================================================
# FILE: agents/agent_5_reporter.py (DEFINITIVE, FINAL VERSION WITH STYLING)
# ==============================================================================
import pandas as pd
import io
import traceback
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Takes the final data and writes a complete, multi-sheet Excel report
    that is a perfect, styled replica of the master config blueprint, using the
    Rainbow Pastels color scheme.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book

            # --- DEFINE RAINBOW PASTEL COLOR PALETTE ---
            colors = {
                'pink': '#FF9AA2', 'light_pink': '#FFB7B2', 'peach': '#FFDAC1',
                'green': '#E2F0CB', 'teal': '#B5EAD7', 'lavender': '#C7CEEA',
                'white': '#FFFFFF', 'dark_grey': '#595959'
            }

            # --- DEFINE CELL FORMATS ---
            fmt_title = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter', 'font_color': colors['dark_grey']})
            fmt_header = workbook.add_format({'bold': True, 'font_size': 11, 'bg_color': colors['pink'], 'font_color': colors['white'], 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            fmt_subheader = workbook.add_format({'bold': True, 'font_size': 11, 'bg_color': colors['light_pink'], 'font_color': colors['dark_grey']})
            
            # Create formats for each color category
            fmt_data_eq = workbook.add_format({'bg_color': colors['lavender'], 'num_format': '#,##0.00'})
            fmt_data_lia = workbook.add_format({'bg_color': colors['peach'], 'num_format': '#,##0.00'})
            fmt_data_asset = workbook.add_format({'bg_color': colors['green'], 'num_format': '#,##0.00'})
            
            fmt_total = workbook.add_format({'bold': True, 'top': 1, 'num_format': '#,##0.00'})
            fmt_grand_total = workbook.add_format({'bold': True, 'bg_color': colors['teal'], 'font_color': colors['dark_grey'], 'top': 1, 'bottom': 2, 'num_format': '#,##0.00'})

            # --- 1. RENDER THE MAIN SHEETS (BALANCE SHEET & P&L) ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 5); worksheet.set_column('B:B', 65); worksheet.set_column('C:C', 8); worksheet.set_column('D:E', 20)
                worksheet.merge_range('A1:E1', f"{company_name} - {sheet_name}", fmt_title)

                row_num = 3
                current_format = fmt_data_eq # Default format

                # Helper to calculate totals based on note numbers
                def get_total_for_notes(note_list, year):
                    if not isinstance(note_list, list): return 0
                    return sum(aggregated_data.get(str(n), {}).get('total', {}).get(year, 0) for n in note_list)

                for row_data in template:
                    col_a, particulars, note, row_type = row_data
                    
                    if row_type == "header_col":
                        worksheet.write('B2', particulars, fmt_header); worksheet.write('C2', note, fmt_header)
                        worksheet.write('D2', "As at March 31, 2025", fmt_header); worksheet.write('E2', "As at March 31, 2024", fmt_header)
                        continue

                    # This logic determines which color to use based on the section
                    if row_type == 'header':
                        if "EQUITY" in particulars: current_format = fmt_data_eq
                        if "ASSETS" in particulars: current_format = fmt_data_asset
                        if "Expenses" in particulars: current_format = fmt_data_lia
                    if row_type == 'sub_header':
                        if "liabilities" in particulars.lower(): current_format = fmt_data_lia

                    cy_val, py_val = None, None
                    if row_type in ["item", "item_sub", "item_no_alpha"]:
                        note_total = aggregated_data.get(str(note), {}).get('total', {})
                        cy_val, py_val = note_total.get('CY', 0), note_total.get('PY', 0)
                    elif row_type == "total":
                        if note == 'PBT':
                            rev_cy = get_total_for_notes(['21', '22'], 'CY'); rev_py = get_total_for_notes(['21', '22'], 'PY')
                            exp_cy = get_total_for_notes(['23', '24', '25', '11', '26'], 'CY'); exp_py = get_total_for_notes(['23', '24', '25', '11', '26'], 'PY')
                            cy_val = rev_cy - exp_cy; py_val = rev_py - exp_py
                        elif note == 'PAT':
                            rev_cy = get_total_for_notes(['21', '22'], 'CY'); rev_py = get_total_for_notes(['21', '22'], 'PY')
                            exp_cy = get_total_for_notes(['23', '24', '25', '11', '26'], 'CY'); exp_py = get_total_for_notes(['23', '24', '25', '11', '26'], 'PY')
                            pbt_cy, pbt_py = rev_cy - exp_cy, rev_py - exp_py
                            tax_cy, tax_py = get_total_for_notes(['4'], 'CY'), get_total_for_notes(['4'], 'PY')
                            cy_val = pbt_cy - tax_cy; py_val = pbt_py - tax_py
                        else:
                            cy_val, py_val = get_total_for_notes(note, 'CY'), get_total_for_notes(note, 'PY')
                    
                    if row_type in ["header", "sub_header"]:
                        worksheet.write(row_num, 0, col_a, fmt_subheader); worksheet.write(row_num, 1, particulars, fmt_subheader)
                    elif row_type == "total":
                        worksheet.write(row_num, 1, particulars, fmt_grand_total)
                        worksheet.write_number(row_num, 3, cy_val, fmt_grand_total); worksheet.write_number(row_num, 4, py_val, fmt_grand_total)
                    elif cy_val is not None:
                        worksheet.write(row_num, 0, col_a, current_format); worksheet.write(row_num, 1, particulars, current_format)
                        worksheet.write_string(row_num, 2, str(note) if note else '', current_format)
                        worksheet.write_number(row_num, 3, cy_val, current_format); worksheet.write_number(row_num, 4, py_val, current_format)
                    row_num += 1

            # --- 2. RENDER THE NOTE SHEETS ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=lambda x: int(x.split('.')[0])):
                note_data = aggregated_data.get(note_num_str)
                if not note_data or 'sub_items' not in note_data: continue

                # Determine the color for the note based on its type
                note_num_int = int(note_num_str)
                if 1 <= note_num_int <= 10: note_format = fmt_data_lia # Liabilities/Equity
                elif 11 <= note_num_int <= 20: note_format = fmt_data_asset # Assets
                else: note_format = fmt_data_eq # P&L

                sheet_name = f"Note {note_num_str}"; worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 65); worksheet.set_column('B:C', 20)
                worksheet.merge_range('A1:C1', f"Note {note_num_str}: {note_data.get('title', '')}", fmt_title)
                worksheet.write('A3', 'Particulars', fmt_header); worksheet.write('B3', 'As at March 31, 2025', fmt_header); worksheet.write('C3', 'As at March 31, 2024', fmt_header)
                row_num = 3
                
                def write_note_level(items, indent_level=0):
                    nonlocal row_num
                    for key, value in items.items():
                        prefix = "    " * indent_level
                        if isinstance(value, dict) and 'CY' in value:
                            worksheet.write(row_num, 0, f"{prefix}{key}", note_format)
                            worksheet.write_number(row_num, 1, value.get('CY', 0), note_format)
                            worksheet.write_number(row_num, 2, value.get('PY', 0), note_format)
                            row_num += 1
                        elif isinstance(value, dict):
                            worksheet.write(row_num, 0, f"{prefix}{key}", fmt_subheader)
                            row_num += 1
                            write_note_level(value, indent_level + 1)
                
                write_note_level(note_data['sub_items'])
                worksheet.write(row_num, 0, "Total", fmt_total)
                worksheet.write_number(row_num, 1, note_data.get('total', {}).get('CY', 0), fmt_total)
                worksheet.write_number(row_num, 2, note_data.get('total', {}).get('PY', 0), fmt_total)

        print("✅ Report Finalizer SUCCESS: Styled Excel file created in memory.")
        return output.getvalue()

    except Exception as e:
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        traceback.print_exc()
        return None
