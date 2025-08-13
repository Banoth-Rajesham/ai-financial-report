# ==============================================================================
# FILE: agents/agent_5_reporter.py (FINAL, WITH CORRECTED STYLING)
# ==============================================================================
import pandas as pd
import io
import traceback
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def apply_main_sheet_styling(ws, template, company_name):
    """Applies the beautiful, professional styling with orange headers and corrected number format."""

    # --- STYLE DEFINITIONS ---
    header_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
    # New color for headings as requested
    heading_orange_fill = PatternFill(start_color="FDE9D9", end_color="FDE9D9", fill_type="solid")
    total_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    
    title_font = Font(bold=True, size=16)
    subtitle_font = Font(bold=True, size=12)
    header_font = Font(bold=True)
    bold_font = Font(bold=True)
    
    # Corrected currency format to remove unwanted symbols
    currency_format = '#,##0.00'

    # --- APPLY STYLES ---
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 65
    ws.column_dimensions['C'].width = 8
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20

    ws.insert_rows(1, 3)
    ws.merge_cells('A1:E1')
    ws['A1'] = company_name
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')

    ws.merge_cells('A2:E2')
    ws['A2'] = ws.title
    ws['A2'].font = subtitle_font
    ws['A2'].alignment = Alignment(horizontal='center')

    for cell in ws[4]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    for i, row_template in enumerate(template, start=1):
        row_num = i + 4
        row_type = row_template[3]

        # Apply orange background to headers and sub-headers
        if row_type in ['header', 'sub_header']:
            ws[f'B{row_num}'].font = bold_font
            for col in ['A', 'B', 'C', 'D', 'E']:
                ws[f'{col}{row_num}'].fill = heading_orange_fill

        elif row_type == 'total':
            for cell in ws[row_num]:
                cell.font = bold_font
                cell.fill = total_fill

        for col_letter in ['D', 'E']:
            cell = ws[f'{col_letter}{row_num}']
            if cell.value is not None and isinstance(cell.value, (int, float)):
                cell.number_format = currency_format


def apply_note_sheet_styling(ws, note_title):
    """Applies professional styling to a Note sheet."""
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    title_font = Font(bold=True, size=14)
    total_font = Font(bold=True)
    # Corrected currency format to remove unwanted symbols
    currency_format = '#,##0.00'

    ws.column_dimensions['A'].width = 65
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20

    ws.merge_cells('A1:C1')
    ws['A1'] = note_title
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')

    for cell in ws[2]:
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


def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Constructs a detailed, multi-sheet Schedule III compliant Excel report
    with the corrected professional styling.
    """
    print("\n--- Agent 5 (Report Finalizer): Building styled report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:

            # --- 1. Process Main Sheets (Balance Sheet & P&L) ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]),
                                         ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:

                sheet_data = []
                # P&L calculation variables
                pbt_cy, pbt_py = 0, 0
                total_revenue_cy, total_revenue_py = 0, 0
                total_expenses_cy, total_expenses_py = 0, 0
                total_tax_cy, total_tax_py = 0, 0

                for row_template in template:
                    col_a, particulars, note, row_type = row_template
                    row = { ' ': col_a, 'Particulars': particulars, 'Note': "" if not isinstance(note, str) else note,
                            'As at March 31, 2025': None, 'As at March 31, 2024': None }

                    if row_type in ["item", "item_no_alpha"]:
                        note_str = str(note)
                        row['As at March 31, 2025'] = aggregated_data.get(note_str, {}).get('total', {}).get('CY', 0)
                        row['As at March 31, 2024'] = aggregated_data.get(note_str, {}).get('total', {}).get('PY', 0)
                    elif row_type == "total" and isinstance(note, list):
                        cy_val, py_val = 0, 0
                        for note_to_sum in note:
                            cy_val += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('CY', 0)
                            py_val += aggregated_data.get(str(note_to_sum), {}).get('total', {}).get('PY', 0)
                        row['As at March 31, 2025'], row['As at March 31, 2024'] = cy_val, py_val

                        # Store totals for P&L calculations
                        if particulars.startswith("Total Revenue"): total_revenue_cy, total_revenue_py = cy_val, py_val
                        if particulars == "Total Expenses": total_expenses_cy, total_expenses_py = cy_val, py_val
                        if particulars.startswith("Total Tax Expense"): total_tax_cy, total_tax_py = cy_val, py_val
                    elif note == "PBT":
                        pbt_cy = total_revenue_cy - total_expenses_cy
                        pbt_py = total_revenue_py - total_expenses_py
                        row['As at March 31, 2025'], row['As at March 31, 2024'] = pbt_cy, pbt_py
                    elif note == "PAT":
                        row['As at March 31, 2025'] = pbt_cy - total_tax_cy
                        row['As at March 31, 2024'] = pbt_py - total_tax_py

                    sheet_data.append(row)

                df = pd.DataFrame(sheet_data)
                df.to_excel(writer, sheet_name=sheet_name, index=False, header=True, startrow=3)
                ws = writer.sheets[sheet_name]
                apply_main_sheet_styling(ws, template, company_name)

            # --- 2. Process Note Sheets ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info = NOTES_STRUCTURE_AND_MAPPING[note_num_str]
                note_data = aggregated_data.get(note_num_str)
                if note_data and note_data.get('sub_items'):
                    sheet_name = f'Note {note_num_str}'
                    note_title = f'Note {note_num_str}: {note_info["title"]}'
                    note_df_data = []

                    def process_sub_items(items, level=0):
                        for key, value in items.items():
                            indent = '  ' * level
                            if isinstance(value, dict) and 'CY' in value:
                                note_df_data.append({'Particulars': indent + key, 'As at March 31, 2025': value.get('CY', 0), 'As at March 31, 2024': value.get('PY', 0)})
                            elif isinstance(value, dict):
                                note_df_data.append({'Particulars': indent + key, 'As at March 31, 2025': None, 'As at March 31, 2024': None})
                                process_sub_items(value, level + 1)

                    process_sub_items(note_data['sub_items'])

                    note_df = pd.DataFrame(note_df_data)
                    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY', 0), 'As at March 31, 2024': note_data['total'].get('PY', 0)}])
                    note_df = pd.concat([note_df, total_row], ignore_index=True)

                    note_df.to_excel(writer, sheet_name=sheet_name, index=False, header=True, startrow=1)
                    ws_note = writer.sheets[sheet_name]
                    apply_note_sheet_styling(ws_note, note_title)

        print("✅ Report Finalizer SUCCESS: Report generated with styling.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}")
        traceback.print_exc()
        return None
