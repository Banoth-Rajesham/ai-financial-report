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
                'total_bg': '#F8CBAD',
                'border': '#000000'
            }

            # --- DEFINE CELL FORMATS ---
            num_format_rupee = r'_("₹"* #,##0.00_);_("₹"* (#,##0.00);_("0.00"??_);_(@_)'
            num_format_pct = '0.00"%"'
            
            fmt_title = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'bg_color': colors['title_bg'], 'font_color': colors['title_font']})
            fmt_header = workbook.add_format({'bold': True, 'bg_color': colors['header_bg'], 'border': 1, 'border_color': colors['border'], 'align': 'center', 'valign': 'vcenter'})
            
            fmt_sec_header_lia_eq = workbook.add_format({'bold': True, 'bg_color': colors['lia_eq_header_bg'], 'border': 1, 'border_color': colors['border']})
            fmt_sec_header_asset = workbook.add_format({'bold': True, 'bg_color': colors['asset_header_bg'], 'border': 1, 'border_color': colors['border']})
            fmt_subheader = workbook.add_format({'bg_color': colors['subheader_bg'], 'border': 1, 'border_color': colors['border']})

            fmt_item_text = workbook.add_format({'border': 1, 'border_color': colors['border']})
            fmt_item_num = workbook.add_format({'border': 1, 'border_color': colors['border'], 'num_format': num_format_rupee})
            fmt_item_pct = workbook.add_format({
                'border': 1, 'border_color': colors['border'], 'num_format': num_format_pct
            })
            
            fmt_total_text = workbook.add_format({'bold': True, 'bg_color': colors['total_bg'], 'border': 1, 'border_color': colors['border']})
            fmt_total_num = workbook.add_format({'bold': True, 'bg_color': colors['total_bg'], 'border': 1, 'border_color': colors['border'], 'num_format': num_format_rupee})
            fmt_total_pct = workbook.add_format({
                'bold': True, 'bg_color': colors['total_bg'], 'border': 1,
                'border_color': colors['border'], 'num_format': num_format_pct
            })
            
            # --- 1. RENDER THE MAIN SHEETS (BALANCE SHEET & P&L) ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 5); worksheet.set_column('B:B', 65); worksheet.set_column('C:C', 8); worksheet.set_column('D:E', 20)

                worksheet.merge_range('A1:E1', f"{company_name} - {sheet_name}", fmt_title)
                row_num = 3 # Start table on row 4, leaving row 2 blank for spacing

                get_total = lambda note_list, year: sum(aggregated_data.get(str(n), {}).get('total', {}).get(year, 0) for n in note_list) if isinstance(note_list, list) else 0

                for row_data in template:
                    col_a, particulars, note, row_type = row_data
                    if row_type == "header_col":
                        worksheet.write('B3', particulars, fmt_header); worksheet.write('C3', note, fmt_header)
                        worksheet.write('D3', "As at March 31, 2025", fmt_header); worksheet.write('E3', "As at March 31, 2024", fmt_header)
                        continue

                    cy_val, py_val = 0, 0
                    if row_type in ["item", "item_sub", "item_no_alpha"]:
                        note_total = aggregated_data.get(str(note), {}).get('total', {}); cy_val, py_val = note_total.get('CY', 0), note_total.get('PY', 0)
                    elif row_type == "total":
                        if note == 'PBT': cy_val, py_val = get_total(['21','22'],'CY') - get_total(['23','24','25','11','26'],'CY'), get_total(['21','22'],'PY') - get_total(['23','24','25','11','26'],'PY')
                        elif note == 'PAT': cy_val, py_val = (get_total(['21','22'],'CY') - get_total(['23','24','25','11','26'],'CY')) - get_total(['4'],'CY'), (get_total(['21','22'],'PY') - get_total(['23','24','25','11','26'],'PY')) - get_total(['4'],'PY')
                        else: cy_val, py_val = get_total(note, 'CY'), get_total(note, 'PY')
                    
                    is_asset = any(s in particulars for s in ['ASSETS', 'Fixed assets', 'Current assets', 'Revenue'])
                    is_lia_eq = any(s in particulars for s in ['EQUITY', 'LIABILITIES', 'Shareholder'])
                    
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
            
            # Moved `write_note_level` to a higher scope
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

            # Custom renderer for Note 1 to match the specific layout
            def _render_note1(n1):
                nonlocal row_num
                
                # Main headers for Note 1
                worksheet.write('A3', 'Particulars', fmt_header)
                worksheet.write('B3', 'As at March 31, 2025', fmt_header)
                worksheet.write('C3', 'As at March 31, 2024', fmt_header)
                row_num = 4
                
                # Block 1: Share Capital
                worksheet.write(row_num, 0, '1. Share Capital', fmt_subheader)
                row_num += 1
                
                worksheet.write(row_num, 0, 'Authorised share capital', fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1
                
                worksheet.write(row_num, 0, 'No of shares 10000, Equity shares of Rs.10 each.', fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1

                worksheet.write(row_num, 0, 'Issued, subscribed and fully paid up capital', fmt_item_text)
                worksheet.write_number(row_num, 1, 500000.00, fmt_item_num)
                worksheet.write_number(row_num, 2, 500000.00, fmt_item_num)
                row_num += 1

                worksheet.write(row_num, 0, 'No of shares 10000 Equity shares of Rs.10 each.', fmt_item_text)
                worksheet.write_number(row_num, 1, 500000.00, fmt_item_num)
                worksheet.write_number(row_num, 2, 500000.00, fmt_item_num)
                row_num += 1

                worksheet.write(row_num, 0, 'Issued, subscribed and Partly up capital', fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1
                
                worksheet.write(row_num, 0, 'No of shares 10000 equity shares of Rs.10 each fully paid up.', fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1

                worksheet.write(row_num, 0, "Total", fmt_total_text)
                worksheet.write_number(row_num, 1, 500000.00, fmt_total_num)
                worksheet.write_number(row_num, 2, 500000.00, fmt_total_num)
                row_num += 1
                row_num += 1 # Spacer row
                
                # Block 1.1: Reconciliation
                worksheet.write(row_num, 0, "1.1 Reconciliation of number of shares", fmt_subheader)
                row_num += 1

                worksheet.write(row_num, 0, "Equity shares", fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1
                
                worksheet.write(row_num, 0, "No of shares 10000 Equity shares of Rs. 10 each.", fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1
                
                worksheet.write(row_num, 0, "Add: Additions to share capital on account of fresh issue or bonus issue etc.", fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1

                worksheet.write(row_num, 0, "Ded: Deductions from share capital on account of shares bought back, redemption etc.", fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1
                
                worksheet.write(row_num, 0, "Balance at the end of the year", fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1
                
                worksheet.write(row_num, 0, "No. of shares 10,000 shares of 10 each", fmt_item_text)
                worksheet.write_number(row_num, 1, 0, fmt_item_num)
                worksheet.write_number(row_num, 2, 0, fmt_item_num)
                row_num += 1

                worksheet.write(row_num, 0, "", fmt_total_text)
                worksheet.write_number(row_num, 1, 0, fmt_total_num)
                worksheet.write_number(row_num, 2, 0, fmt_total_num)
                row_num += 1
                row_num += 1 # Spacer row

                # Block 1.2: Shareholders >5%
                worksheet.merge_range(row_num, 0, row_num, 2, "1.2 Details of shares held by shareholders holding more than 5% of the aggregate shares in the company", fmt_subheader)
                row_num += 1
                
                # Multi-level headers for 5% table
                worksheet.merge_range(row_num, 0, row_num + 1, 0, "Name of the shareholders", fmt_header)
                worksheet.merge_range(row_num, 1, row_num, 2, "As at March 31, 2025", fmt_header)
                worksheet.merge_range(row_num, 3, row_num, 4, "As at March 31, 2024", fmt_header)
                row_num += 1
                
                worksheet.write(row_num, 1, "Number of shares", fmt_header)
                worksheet.write(row_num, 2, "Percentage of share holding", fmt_header)
                worksheet.write(row_num, 3, "Number of shares", fmt_header)
                worksheet.write(row_num, 4, "Percentage of share holding", fmt_header)
                row_num += 1

                shareholders = ["M A Waheed Khan", "M A Qhuddus Khan", "M A Khadir Khan Asif", "M A Rauf Khan"]
                for name in shareholders:
                    worksheet.write(row_num, 0, name, fmt_item_text)
                    worksheet.write_number(row_num, 1, 0, fmt_item_num)
                    worksheet.write_number(row_num, 2, 0, fmt_item_pct)
                    worksheet.write_number(row_num, 3, 0, fmt_item_num)
                    worksheet.write_number(row_num, 4, 0, fmt_item_pct)
                    row_num += 1
                
                # Bottom summary row for 5% table
                worksheet.write(row_num, 0, "Total", fmt_total_text)
                worksheet.write_number(row_num, 1, 0, fmt_total_num)
                worksheet.write_number(row_num, 2, 0, fmt_total_pct)
                worksheet.write_number(row_num, 3, 0, fmt_total_num)
                worksheet.write_number(row_num, 4, 0, fmt_total_pct)
                row_num += 1

            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=lambda x: int(x.split('.')[0])):
                note_data = aggregated_data.get(note_num_str)
                if not note_data or 'sub_items' not in note_data: continue

                sheet_name = f"Note {note_num_str}"; worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 65); worksheet.set_column('B:C', 20)
                worksheet.merge_range('A1:C1', f"Note {note_num_str}: {note_data.get('title', '')}", fmt_title)
                
                row_num = 3
                
                # Choose renderer
                if note_num_str.strip() == '1':
                    _render_note1(note_data)
                else:
                    worksheet.write('A3', 'Particulars', fmt_header)
                    worksheet.write('B3', 'As at March 31, 2025', fmt_header)
                    worksheet.write('C3', 'As at March 31, 2024', fmt_header)
                    row_num = 4
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
