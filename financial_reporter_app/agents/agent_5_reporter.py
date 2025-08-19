# ==============================================================================
# FILE: agents/agent_5_reporter.py (DEFINITIVE, FINAL VERSION WITH "My Company Inc." STYLING)
# ==============================================================================
import pandas as pd
import io
import traceback
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Takes final data and writes a complete, multi-sheet Excel report
    with the professional styling from the "My Company Inc." example.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book

            # --- DEFINE "My Company Inc." COLOR PALETTE ---
            colors = {
                'title_bg': '#2F5496', 'title_font': '#FFFFFF',
                'header_bg': '#DDEBF7',
                'lia_eq_header_bg': '#FFF2CC',
                'asset_header_bg': '#E2EFDA',
                'subheader_bg': '#F8D7DA',
                'total_bg': '#F8CBAD'
            }

            # --- DEFINE CELL FORMATS ---
            num_format_rupee = '_("₹"* #,##0.00_);_("₹"* (#,##0.00);_("-"??_);_(@_)'
            fmt_title = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'bg_color': colors['title_bg'], 'font_color': colors['title_font']})
            fmt_header = workbook.add_format({'bold': True, 'bg_color': colors['header_bg'], 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            
            fmt_sec_header_lia_eq = workbook.add_format({'bold': True, 'bg_color': colors['lia_eq_header_bg'], 'border': 1})
            fmt_sec_header_asset = workbook.add_format({'bold': True, 'bg_color': colors['asset_header_bg'], 'border': 1})
            fmt_subheader = workbook.add_format({'bg_color': colors['subheader_bg'], 'border': 1})

            fmt_item_text = workbook.add_format({'border': 1})
            fmt_item_num = workbook.add_format({'border': 1, 'num_format': num_format_rupee})
            
            fmt_total_text = workbook.add_format({'bold': True, 'bg_color': colors['total_bg'], 'border': 1})
            fmt_total_num = workbook.add_format({'bold': True, 'bg_color': colors['total_bg'], 'border': 1, 'num_format': num_format_rupee})
            
            # --- 1. RENDER THE MAIN SHEETS (BALANCE SHEET & P&L) ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 5); worksheet.set_column('B:B', 65); worksheet.set_column('C:C', 8); worksheet.set_column('D:E', 20)

                # Write Titles with a blank row for spacing
                worksheet.merge_range('A1:E1', f"{company_name} - {sheet_name}", fmt_title)
                row_num = 3 # Start writing table from row 4

                get_total = lambda note_list, year: sum(aggregated_data.get(str(n), {}).get('total', {}).get(year, 0) for n in note_list) if isinstance(note_list, list) else 0

                for row_data in template:
                    col_a, particulars, note, row_type = row_data
                    if row_type == "header_col":
                        worksheet.write('B3', particulars, fmt_header); worksheet.write('C3', note, fmt_header)
                        worksheet.write('D3', "As at March 31, 2025", fmt_header); worksheet.write('E3', "As at March 31, 2024", fmt_header)
                        continue

                    cy_val, py_val = 0, 0
                    if row_type in ["item", "item_sub", "item_no_alpha"]:
                        note_total = aggregated_data.get(str(note), {}).get('total', {})
                        cy_val, py_val = note_total.get('CY', 0), note_total.get('PY', 0)
                    elif row_type == "total":
                        cy_val, py_val = get_total(note, 'CY'), get_total(note, 'PY')
                    
                    # Determine styling
                    is_asset = any(s in particulars for s in ['ASSETS', 'Fixed assets', 'Current assets', 'Revenue'])
                    is_lia_eq = any(s in particulars for s in ['EQUITY', 'LIABILITIES', 'Shareholder', 'Profit'])
                    
                    # Write row data with correct formats
                    if row_type in ["header", "sub_header"]:
                        fmt = fmt_sec_header_asset if is_asset else (fmt_sec_header_lia_eq if is_lia_eq else fmt_subheader)
                        worksheet.write(row_num, 0, col_a, fmt); worksheet.write(row_num, 1, particulars, fmt)
                    elif row_type == "total":
                        worksheet.write(row_num, 1, particulars, fmt_total_text)
                        worksheet.write_number(row_num, 3, cy_val, fmt_total_num); worksheet.write_number(row_num, 4, py_val, fmt_total_num)
                    elif row_type not in ["spacer", "item_no_note", "item_no_note_sub"]:
                        worksheet.write(row_num, 0, col_a, fmt_item_text)
                        worksheet.write(row_num, 1, particulars, fmt_item_text)
                        worksheet.write_string(row_num, 2, str(note) if note else '', fmt_item_text)
                        worksheet.write_number(row_num, 3, cy_val, fmt_item_num); worksheet.write_number(row_num, 4, py_val, fmt_item_num)
                    row_num += 1

            # --- 2. RENDER THE NOTE SHEETS ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=lambda x: int(x.split('.')[0])):
                note_data = aggregated_data.get(note_num_str)
                if not note_data or 'sub_items' not in note_data: continue

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
                            worksheet.write(row_num, 0, f"{prefix}{key}", fmt_item_text)
                            worksheet.write_number(row_num, 1, value.get('CY', 0), fmt_item_num)
                            worksheet.write_number(row_num, 2, value.get('PY', 0), fmt_item_num)
                            row_num += 1
                        elif isinstance(value, dict):
                            worksheet.write(row_num, 0, f"{prefix}{key}", fmt_subheader)
                            row_num += 1
                            write_note_level(value, indent_level + 1)
                
                write_note_level(note_data['sub_items'])
                worksheet.write(row_num, 0, "Total", fmt_total_text)
                worksheet.write_number(row_num, 1, note_data.get('total', {}).get('CY', 0), fmt_total_num)
                worksheet.write_number(row_num, 2, note_data.get('total', {}).get('PY', 0), fmt_total_num)

        print("✅ Report Finalizer SUCCESS: Styled Excel file created in memory.")
        return output.getvalue()

    except Exception as e:
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        traceback.print_exc()
        return None
