# ==============================================================================
# FILE: agents/agent_5_reporter.py (DEFINITIVE, FINAL VERSION WITH HORIZONTAL BS STYLING)
# ==============================================================================
import pandas as pd
import io
import traceback
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Takes the final data and writes a complete, multi-sheet Excel report
    that is a perfect, styled replica of the master config blueprint, using the
    new "Horizontal Balance Sheet" color scheme.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book

            # --- DEFINE NEW "HORIZONTAL BALANCE SHEET" COLOR PALETTE ---
            colors = {
                'blue_header': '#CDE5F5', 'blue_total': '#BDD7EE',
                'green_header': '#D7EACF', 'green_total': '#C5E0B4',
                'pink_header': '#F8D7DA', 'pink_total': '#F4B183',
                'yellow_header': '#FFF2CC', 'yellow_total': '#FFD966',
                'grey_header': '#F2F2F2', 'dark_grey_text': '#404040',
                'border_color': '#BFBFBF'
            }

            # --- DEFINE NEW CELL FORMATS ---
            num_format = '_("$"* #,##0.00_);_("$"* (#,##0.00);_("-"??_);_(@_)'
            fmt_title = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'font_color': colors['dark_grey_text'], 'bg_color': '#DDEBF7', 'border': 1})
            fmt_header = workbook.add_format({'bold': True, 'bg_color': colors['grey_header'], 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            
            fmt_subheader_asset = workbook.add_format({'bold': True, 'bg_color': colors['green_header'], 'border': 1})
            fmt_subheader_lia = workbook.add_format({'bold': True, 'bg_color': colors['yellow_header'], 'border': 1})
            fmt_subheader_eq = workbook.add_format({'bold': True, 'bg_color': colors['blue_header'], 'border': 1})
            fmt_subheader_exp = workbook.add_format({'bold': True, 'bg_color': colors['pink_header'], 'border': 1})

            fmt_data_border = workbook.add_format({'border': 1, 'num_format': num_format})
            
            fmt_total_asset = workbook.add_format({'bold': True, 'bg_color': colors['green_total'], 'border': 1, 'num_format': num_format})
            fmt_total_lia = workbook.add_format({'bold': True, 'bg_color': colors['yellow_total'], 'border': 1, 'num_format': num_format})
            fmt_total_eq = workbook.add_format({'bold': True, 'bg_color': colors['blue_total'], 'border': 1, 'num_format': num_format})
            fmt_total_exp = workbook.add_format({'bold': True, 'bg_color': colors['pink_total'], 'border': 1, 'num_format': num_format})
            
            # --- 1. RENDER THE MAIN SHEETS (BALANCE SHEET & P&L) ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 5); worksheet.set_column('B:B', 65); worksheet.set_column('C:C', 8); worksheet.set_column('D:E', 20)
                worksheet.merge_range('A1:E1', f"{company_name} - {sheet_name}", fmt_title)

                row_num = 3
                get_total = lambda note_list, year: sum(aggregated_data.get(str(n), {}).get('total', {}).get(year, 0) for n in note_list) if isinstance(note_list, list) else 0

                for row_data in template:
                    col_a, particulars, note, row_type = row_data
                    if row_type == "header_col":
                        worksheet.write('B2', particulars, fmt_header); worksheet.write('C2', note, fmt_header)
                        worksheet.write('D2', "As at March 31, 2025", fmt_header); worksheet.write('E2', "As at March 31, 2024", fmt_header)
                        continue

                    # Determine format based on row
                    is_asset = any(s in particulars for s in ['ASSETS', 'Fixed assets', 'Current assets', 'Revenue'])
                    is_lia = any(s in particulars for s in ['LIABILITIES', 'borrowings', 'payables'])
                    is_eq = any(s in particulars for s in ['EQUITY', 'Shareholder', 'Profit', 'Net Income'])
                    is_exp = any(s in particulars for s in ['Expenses'])

                    cy_val, py_val = None, None
                    if row_type in ["item", "item_sub", "item_no_alpha"]:
                        note_total = aggregated_data.get(str(note), {}).get('total', {}); cy_val, py_val = note_total.get('CY', 0), note_total.get('PY', 0)
                    elif row_type == "total":
                        cy_val, py_val = get_total(note, 'CY'), get_total(note, 'PY')
                    
                    if row_type in ["header", "sub_header"]:
                        fmt = fmt_subheader_asset if is_asset else (fmt_subheader_lia if is_lia else (fmt_subheader_eq if is_eq else fmt_subheader_exp))
                        worksheet.write(row_num, 0, col_a, fmt); worksheet.write(row_num, 1, particulars, fmt)
                    elif row_type == "total":
                        fmt = fmt_total_asset if is_asset else (fmt_total_lia if is_lia else (fmt_total_eq if is_eq else fmt_total_exp))
                        worksheet.write(row_num, 1, particulars, fmt)
                        worksheet.write_number(row_num, 3, cy_val, fmt); worksheet.write_number(row_num, 4, py_val, fmt)
                    elif cy_val is not None:
                        worksheet.write(row_num, 0, col_a, fmt_data_border); worksheet.write(row_num, 1, particulars, fmt_data_border)
                        worksheet.write_string(row_num, 2, str(note) if note else '', fmt_data_border)
                        worksheet.write_number(row_num, 3, cy_val, fmt_data_border); worksheet.write_number(row_num, 4, py_val, fmt_data_border)
                    row_num += 1

            # --- 2. RENDER THE NOTE SHEETS ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=lambda x: int(x.split('.')[0])):
                note_data = aggregated_data.get(note_num_str)
                if not note_data or 'sub_items' not in note_data: continue

                # Determine note color
                note_num_int = int(note_num_str)
                if 1 <= note_num_int <= 10: fmt_note, fmt_total_note = fmt_total_lia, fmt_total_eq
                elif 11 <= note_num_int <= 20: fmt_note, fmt_total_note = fmt_total_asset, fmt_total_asset
                else: fmt_note, fmt_total_note = fmt_total_exp, fmt_total_exp

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
                            worksheet.write(row_num, 0, f"{prefix}{key}", fmt_data_border)
                            worksheet.write_number(row_num, 1, value.get('CY', 0), fmt_data_border)
                            worksheet.write_number(row_num, 2, value.get('PY', 0), fmt_data_border)
                            row_num += 1
                        elif isinstance(value, dict):
                            worksheet.write(row_num, 0, f"{prefix}{key}", fmt_subheader_lia)
                            row_num += 1; write_note_level(value, indent_level + 1)
                
                write_note_level(note_data['sub_items'])
                worksheet.write(row_num, 0, "Total", fmt_total_note)
                worksheet.write_number(row_num, 1, note_data.get('total', {}).get('CY', 0), fmt_total_note)
                worksheet.write_number(row_num, 2, note_data.get('total', {}).get('PY', 0), fmt_total_note)

        print("✅ Report Finalizer SUCCESS: Styled Excel file created in memory.")
        return output.getvalue()

    except Exception as e:
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        traceback.print_exc()
        return None
