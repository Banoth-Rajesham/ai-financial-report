# ==============================================================================
# FILE: agents/agent_5_reporter.py (FINAL with all corrected notes rendering)
# ==============================================================================

import pandas as pd
import io
import traceback
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Finalizes the Excel report.
    - Balance Sheet & P&L: unchanged
    - Notes: Note 1 gets sectioned layout to match the reference.
    - Other Notes: remain in their generic recursive layout.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book

            # --- Colors and formats (unchanged semantics) ---
            colors = {
                'title_bg': '#2F5496', 'title_font': '#FFFFFF',
                'header_bg': '#DDEBF7',
                'lia_eq_header_bg': '#FFF2CC',
                'asset_header_bg': '#E2EFDA',
                'subheader_bg': '#F8D7DA',
                'total_bg': '#F8CBAD',
                'border': '#000000'
            }

            num_format_rupee = '\_("₹"* #,##0.00_);\_("₹"* (#,##0.00);\_("0.00"??_);\_(@\_)'

            fmt_title = workbook.add_format({
                'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                'bg_color': colors['title_bg'], 'font_color': colors['title_font']
            })
            fmt_header = workbook.add_format({
                'bold': True, 'bg_color': colors['header_bg'], 'border': 1,
                'border_color': colors['border'], 'align': 'center', 'valign': 'vcenter'
            })
            fmt_sec_header_lia_eq = workbook.add_format({
                'bold': True, 'bg_color': colors['lia_eq_header_bg'], 'border': 1,
                'border_color': colors['border']
            })
            fmt_sec_header_asset = workbook.add_format({
                'bold': True, 'bg_color': colors['asset_header_bg'], 'border': 1,
                'border_color': colors['border']
            })
            fmt_subheader = workbook.add_format({
                'bg_color': colors['subheader_bg'], 'border': 1,
                'border_color': colors['border']
            })
            fmt_item_text = workbook.add_format({'border': 1, 'border_color': colors['border']})
            fmt_item_num = workbook.add_format({
                'border': 1, 'border_color': colors['border'], 'num_format': num_format_rupee
            })
            fmt_total_text = workbook.add_format({
                'bold': True, 'bg_color': colors['total_bg'], 'border': 1,
                'border_color': colors['border']
            })
            fmt_total_num = workbook.add_format({
                'bold': True, 'bg_color': colors['total_bg'], 'border': 1,
                'border_color': colors['border'], 'num_format': num_format_rupee
            })

            # --- 1) Balance Sheet & Profit and Loss (unchanged) ---
            for sheet_name, template in [
                ("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]),
                ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])
            ]:
                worksheet = workbook.add_worksheet(sheet_name)
                worksheet.set_column('A:A', 5)
                worksheet.set_column('B:B', 65)
                worksheet.set_column('C:C', 8)
                worksheet.set_column('D:E', 20)

                worksheet.merge_range('A1:E1', f"{company_name} - {sheet_name}", fmt_title)
                row_num = 3  # start at row 4

                get_total = lambda note_list, year: (
                    sum(aggregated_data.get(str(n), {}).get('total', {}).get(year, 0) for n in note_list)
                    if isinstance(note_list, list) else 0
                )

                for col_a, particulars, note, row_type in template:
                    if row_type == "header_col":
                        worksheet.write('B3', particulars, fmt_header)
                        worksheet.write('C3', note, fmt_header)
                        worksheet.write('D3', "As at March 31, 2025", fmt_header)
                        worksheet.write('E3', "As at March 31, 2024", fmt_header)
                        continue

                    cy_val = 0
                    py_val = 0
                    if row_type in ["item", "item_sub", "item_no_alpha"]:
                        note_total = aggregated_data.get(str(note), {}).get('total', {})
                        cy_val, py_val = note_total.get('CY', 0), note_total.get('PY', 0)
                    elif row_type == "total":
                        if note == 'PBT':
                            cy_val = get_total(['21', '22'], 'CY') - get_total(['23', '24', '25', '11', '26'], 'CY')
                            py_val = get_total(['21', '22'], 'PY') - get_total(['23', '24', '25', '11', '26'], 'PY')
                        elif note == 'PAT':
                            cy_val = (get_total(['21', '22'], 'CY') - get_total(['23', '24', '25', '11', '26'], 'CY')) - get_total(['4'], 'CY')
                            py_val = (get_total(['21', '22'], 'PY') - get_total(['23', '24', '25', '11', '26'], 'PY')) - get_total(['4'], 'PY')
                        else:
                            cy_val, py_val = get_total(note, 'CY'), get_total(note, 'PY')

                    is_asset = any(s in particulars for s in ['ASSETS', 'Fixed assets', 'Current assets', 'Revenue'])
                    is_lia_eq = any(s in particulars for s in ['EQUITY', 'LIABILITIES', 'Shareholder'])

                    if row_type in ["header", "sub_header"]:
                        fmt = fmt_sec_header_asset if is_asset else (fmt_sec_header_lia_eq if is_lia_eq else fmt_subheader)
                        worksheet.write(row_num, 0, col_a, fmt)
                        worksheet.write(row_num, 1, particulars, fmt)
                    elif row_type == "total":
                        worksheet.write(row_num, 1, particulars, fmt_total_text)
                        worksheet.write_number(row_num, 3, cy_val, fmt_total_num)
                        worksheet.write_number(row_num, 4, py_val, fmt_total_num)
                    elif row_type not in ["spacer", "item_no_note", "item_no_note_sub"]:
                        worksheet.write(row_num, 0, col_a, fmt_item_text)
                        worksheet.write(row_num, 1, particulars, fmt_item_text)
                        worksheet.write_string(row_num, 2, str(note) if note else '', fmt_item_text)
                        worksheet.write_number(row_num, 3, cy_val, fmt_item_num)
                        worksheet.write_number(row_num, 4, py_val, fmt_item_num)
                    row_num += 1

            # --- 2) Note sheets: Note 1 sectioned, others generic ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=lambda x: int(x.split('.')[0])):
                note_data = aggregated_data.get(note_num_str)
                if not note_data or 'sub_items' not in note_data:
                    continue

                worksheet = workbook.add_worksheet(f"Note {note_num_str}")
                worksheet.set_column('A:A', 65)
                worksheet.set_column('B:C', 20)

                worksheet.merge_range('A1:C1', f"Note {note_num_str}: {note_data.get('title', '')}", fmt_title)
                worksheet.write('A3', 'Particulars', fmt_header)
                worksheet.write('B3', 'As at March 31, 2025', fmt_header)
                worksheet.write('C3', 'As at March 31, 2024', fmt_header)

                row_num = 3

                # helpers for sectioned Note 1
                def _w_kv(label, cy, py):
                    nonlocal row_num
                    worksheet.write(row_num, 0, label, fmt_item_text)
                    worksheet.write_number(row_num, 1, cy or 0, fmt_item_num)
                    worksheet.write_number(row_num, 2, py or 0, fmt_item_num)
                    row_num += 1

                def _sp(rows=1):
                    nonlocal row_num
                    row_num += rows

                def _w_sec(title):
                    nonlocal row_num
                    worksheet.merge_range(row_num, 0, row_num, 2, title, fmt_subheader)
                    row_num += 1

                def _cy_py(d):
                    if isinstance(d, dict) and ('CY' in d or 'PY' in d):
                        return d.get('CY', 0), d.get('PY', 0)
                    return 0, 0
                
                # --- The Corrected _render_note1 function ---
                def _render_note1(n1):
                    nonlocal row_num
                    si = n1.get('sub_items', {})
                    
                    # 1. Authorised Share Capital Section
                    _w_sec("Particulars")
                    
                    # Authorised share capital
                    label_auth = 'Authorised share capital'
                    cy_auth, py_auth = _cy_py(si.get(label_auth, {}))
                    worksheet.write(row_num, 0, f"{label_auth}\n(No. of shares 18000 Equity shares of Rs. 10 each.)", fmt_item_text)
                    worksheet.write_number(row_num, 1, cy_auth, fmt_item_num)
                    worksheet.write_number(row_num, 2, py_auth, fmt_item_num)
                    row_num += 1
                    
                    # Issued, subscribed and fully paid up capital
                    label_issued = 'Issued, subscribed and fully paid up capital'
                    cy_issued, py_issued = _cy_py(si.get(label_issued, {}))
                    worksheet.write(row_num, 0, f"{label_issued}\n(No. of shares 18000 Equity shares of Rs. 10 each.)", fmt_item_text)
                    worksheet.write_number(row_num, 1, cy_issued, fmt_item_num)
                    worksheet.write_number(row_num, 2, py_issued, fmt_item_num)
                    row_num += 1

                    # Issued, subscribed and Partly up capital
                    worksheet.write(row_num, 0, "Issued, subscribed and Partly up capital", fmt_item_text)
                    worksheet.write_number(row_num, 1, 0, fmt_item_num)
                    worksheet.write_number(row_num, 2, 0, fmt_item_num)
                    row_num += 1
                    
                    # Total for this section
                    cy_total_1 = cy_auth + cy_issued
                    py_total_1 = py_auth + py_issued
                    worksheet.write(row_num, 0, "Total", fmt_total_text)
                    worksheet.write_number(row_num, 1, cy_total_1, fmt_total_num)
                    worksheet.write_number(row_num, 2, py_total_1, fmt_total_num)
                    row_num += 1
                    _sp(1)

                    # 2. Reconciliation of number of shares Section
                    _w_sec("1.1 Reconciliation of number of shares")
                    recon = si.get('1.1 Reconciliation of number of shares', {})
                    
                    # Equity shares
                    label_equity = 'Equity shares'
                    cy_equity, py_equity = _cy_py(recon.get(label_equity, {}))
                    _w_kv(f"No. of shares 10000 Equity shares of Rs. 10 each.", cy_equity, py_equity)
                    
                    # Additions
                    label_add = 'Add: Additions to share capital on account of fresh issue or bonus issue etc.,'
                    cy_add, py_add = _cy_py(recon.get(label_add, {}))
                    _w_kv(label_add, cy_add, py_add)
                    
                    # Deductions
                    label_ded = 'Ded: Deductions from share capital on account of shares bought back, redemption etc.,'
                    cy_ded, py_ded = _cy_py(recon.get(label_ded, {}))
                    _w_kv(label_ded, cy_ded, py_ded)
                    
                    # Balance at the end of the year
                    label_balance = 'Balance at the end of the year'
                    cy_balance, py_balance = _cy_py(recon.get(label_balance, {}))
                    _w_kv(f"{label_balance}\nNo. of shares 18,000 shares of 10 each", cy_balance, py_balance)
                    _sp(1)

                    # 3. Shareholders holding >5% Section
                    _w_sec("1.2 Details of shares held by shareholders holding more than 5% of the aggregate shares in the company")
                    worksheet.write(row_num, 0, "Name of the shareholders", fmt_header)
                    worksheet.write(row_num, 1, "Number of shares", fmt_header)
                    worksheet.write(row_num, 2, "Percentage of share holding", fmt_header)
                    row_num += 1

                    sh = si.get('1.2 Details of share held by shareholders holding more than 5% of the aggregate shares in the company', {})
                    for name in ['M A Waheed Khan', 'M A Qhuddus Khan', 'M A Khadir Khan Asif', 'M A Rauf Khan']:
                        row = sh.get(name, {})
                        shares = (row.get('CY', 0) if isinstance(row, dict) and 'CY' in row else 0)
                        pct = (row.get('PY', 0) if isinstance(row, dict) and 'PY' in row else 0)
                        worksheet.write(row_num, 0, name, fmt_item_text)
                        worksheet.write_number(row_num, 1, shares, fmt_item_num)
                        worksheet.write_number(row_num, 2, pct, fmt_item_num)
                        row_num += 1

                # choose renderer robustly
                if note_num_str.strip().split()[-1] == '1':
                    _render_note1(note_data)
                else:
                    _write_note_level(note_data['sub_items'])

                # total row
                worksheet.write(row_num, 0, "Total", fmt_total_text)
                worksheet.write_number(row_num, 1, note_data.get('total', {}).get('CY', 0), fmt_total_num)
                worksheet.write_number(row_num, 2, note_data.get('total', {}).get('PY', 0), fmt_total_num)

        print("✅ Report Finalizer SUCCESS: Styled Excel file created in memory.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        traceback.print_exc()
        return None
