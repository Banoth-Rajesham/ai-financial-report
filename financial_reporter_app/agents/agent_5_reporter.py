# ==============================================================================
# FILE: agents/agent_5_reporter.py (DEFINITIVE, FINAL, ERROR-FREE VERSION)
# ==============================================================================
import pandas as pd
import io
import traceback
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Takes final data and writes a complete, multi-sheet Excel report
    with professional styling inspired by the Abrikam Group income statement.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book

            # --- DEFINE ABRIKAM COLOR PALETTE ---
            colors = {
                'green_bg': '#E2EFDA', 'green_total': '#C6E0B4', 'green_line': '#70AD47',
                'red_bg': '#FDE9D9', 'red_total': '#F8CBAD', 'red_line': '#FF0000',
                'blue_bg': '#DDEBF7', 'blue_total': '#B4C6E7', 'blue_line': '#4472C4',
                'header_bg': '#F2F2F2', 'dark_grey': '#595959', 'light_grey_line': '#D0D0D0'
            }
            
            # --- DEFINE PROFESSIONAL CELL FORMATS ---
            num_format_rupee = '_("₹"* #,##0_);_("₹"* (#,##0);_("-"??_);_(@_)'
            fmt_title = workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center', 'bottom': 6, 'bottom_color': colors['dark_grey']})
            fmt_subtitle = workbook.add_format({'italic': True, 'font_size': 12, 'align': 'center', 'bottom': 1, 'bottom_color': colors['dark_grey']})
            fmt_header = workbook.add_format({'bold': True, 'bg_color': colors['header_bg'], 'align': 'center', 'bottom': 2, 'bottom_color': colors['dark_grey']})
            bold_format = workbook.add_format({'bold': True})

            # Section headers with colored text and lines
            fmt_sec_asset = workbook.add_format({'bold': True, 'font_color': colors['green_line'], 'bottom': 1, 'bottom_color': colors['green_line']})
            fmt_sec_lia_eq = workbook.add_format({'bold': True, 'font_color': colors['blue_line'], 'bottom': 1, 'bottom_color': colors['blue_line']})
            fmt_sec_exp = workbook.add_format({'bold': True, 'font_color': colors['red_line'], 'top': 1, 'top_color': colors['red_line']})
            
            # Data formats with thin grey bottom border
            fmt_data_green = workbook.add_format({'num_format': num_format_rupee, 'bottom': 1, 'bottom_color': colors['light_grey_line']})
            fmt_data_red = workbook.add_format({'num_format': num_format_rupee, 'bottom': 1, 'bottom_color': colors['light_grey_line']})
            fmt_data_blue = workbook.add_format({'num_format': num_format_rupee, 'bottom': 1, 'bottom_color': colors['light_grey_line']})
            
            # Total formats with colored backgrounds and borders
            fmt_total_asset = workbook.add_format({'bold': True, 'bg_color': colors['green_total'], 'font_color': colors['green_line'], 'top': 1, 'bottom': 1, 'num_format': num_format_rupee})
            fmt_total_lia_eq = workbook.add_format({'bold': True, 'bg_color': colors['blue_total'], 'font_color': colors['blue_line'], 'top': 1, 'bottom': 1, 'num_format': num_format_rupee})
            fmt_total_exp = workbook.add_format({'bold': True, 'bg_color': colors['red_total'], 'font_color': colors['red_line'], 'top': 1, 'bottom': 1, 'num_format': num_format_rupee})
            fmt_net_income = workbook.add_format({'bold': True, 'bg_color': colors['blue_total'], 'font_color': colors['blue_line'], 'top': 1, 'bottom': 6, 'bottom_color': colors['blue_line'], 'num_format': num_format_rupee})

            # --- 1. RENDER P&L and Balance Sheet ---
            for sheet_name in ["Profit and Loss", "Balance Sheet"]:
                template = MASTER_TEMPLATE[sheet_name]
                worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 5); worksheet.set_column('B:B', 65); worksheet.set_column('C:C', 8); worksheet.set_column('D:E', 20)
                worksheet.hide_gridlines(2)

                worksheet.merge_range('A1:E1', company_name, fmt_title)
                worksheet.merge_range('A2:E2', f"Consolidated {sheet_name}", fmt_subtitle)
                
                row_num = 3
                for col_a, particulars, note, row_type in template:
                    if row_type == "header_col":
                        worksheet.write('B3', particulars, fmt_header); worksheet.write('C3', note, fmt_header)
                        worksheet.write('D3', "Amount (CY)", fmt_header); worksheet.write('E3', "Amount (PY)", fmt_header)
                        continue

                    is_asset = any(s in particulars for s in ['ASSETS', 'Fixed assets', 'Current assets', 'Revenue'])
                    is_lia_eq = any(s in particulars for s in ['EQUITY', 'LIABILITIES', 'Shareholder', 'Profit', 'Net Income'])
                    is_exp = any(s in particulars for s in ['Expenses'])
                    
                    cy_val, py_val = 0, 0
                    if row_type in ["item", "item_sub", "item_no_alpha"]:
                        note_total = aggregated_data.get(str(note), {}).get('total', {})
                        cy_val, py_val = note_total.get('CY', 0), note_total.get('PY', 0)
                    elif row_type == "total" and isinstance(note, list):
                        cy_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('CY', 0) for n in note)
                        py_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('PY', 0) for n in note)
                    
                    if row_type in ["header", "sub_header"]:
                        fmt_to_use = fmt_sec_asset if is_asset else (fmt_sec_exp if is_exp else fmt_sec_lia_eq)
                        worksheet.write(row_num, 0, col_a); worksheet.write(row_num, 1, particulars, fmt_to_use)
                    elif row_type == "total":
                        fmt_to_use = fmt_total_asset if is_asset else (fmt_total_exp if is_exp else (fmt_net_income if is_lia_eq else workbook.add_format()))
                        worksheet.write(row_num, 1, particulars, fmt_to_use)
                        worksheet.write_number(row_num, 3, cy_val, fmt_to_use); worksheet.write_number(row_num, 4, py_val, fmt_to_use)
                    elif row_type not in ["spacer", "item_no_note_sub", "item_no_note"]:
                        fmt_data = fmt_data_green if is_asset else (fmt_data_red if is_exp else fmt_data_blue)
                        worksheet.write(row_num, 0, col_a, fmt_data); worksheet.write(row_num, 1, particulars, fmt_data)
                        worksheet.write_string(row_num, 2, str(note) if note else '', fmt_data)
                        worksheet.write_number(row_num, 3, cy_val, fmt_data); worksheet.write_number(row_num, 4, py_val, fmt_data)
                    row_num += 1

            # --- 2. RENDER THE NOTE SHEETS (WITH STYLING) ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=lambda x: int(x.split('.')[0])):
                note_data = aggregated_data.get(note_num_str)
                if not note_data or 'sub_items' not in note_data: continue

                note_num_int = int(note_num_str)
                if 1 <= note_num_int <= 10: fmt_note, fmt_note_total = fmt_data_blue, fmt_total_lia_eq
                elif 11 <= note_num_int <= 20: fmt_note, fmt_note_total = fmt_data_green, fmt_total_asset
                else: fmt_note, fmt_note_total = fmt_data_red, fmt_total_exp

                sheet_name = f"Note {note_num_str}"; worksheet = workbook.add_worksheet(sheet_name)
                worksheet.merge_range('A1:C1', f"Note {note_num_str}: {note_data.get('title', '')}", fmt_title)
                worksheet.write_row('A3', ['Particulars', 'Amount (CY)', 'Amount (PY)'], fmt_header)
                worksheet.set_column('A:A', 65); worksheet.set_column('B:C', 20)
                worksheet.hide_gridlines(2)
                
                row_num = 3
                def write_note_level(items, indent_level=0):
                    nonlocal row_num
                    for key, value in items.items():
                        if isinstance(value, dict) and 'CY' in value:
                            worksheet.write(row_num, 0, "    " * indent_level + key, fmt_note)
                            worksheet.write_number(row_num, 1, value.get('CY', 0), fmt_note)
                            worksheet.write_number(row_num, 2, value.get('PY', 0), fmt_note)
                            row_num += 1
                        elif isinstance(value, dict):
                            worksheet.write(row_num, 0, "    " * indent_level + key, bold_format)
                            row_num += 1; write_note_level(value, indent_level + 1)
                
                write_note_level(note_data['sub_items'])
                worksheet.write(row_num, 0, "Total", fmt_note_total)
                worksheet.write_number(row_num, 1, note_data.get('total', {}).get('CY', 0), fmt_note_total)
                worksheet.write_number(row_num, 2, note_data.get('total', {}).get('PY', 0), fmt_note_total)

        print("✅ Report Finalizer SUCCESS: Styled Excel file created in memory.")
        return output.getvalue()

    except Exception as e:
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        traceback.print_exc()
        return None
