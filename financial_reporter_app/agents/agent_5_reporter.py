# ==============================================================================
# PASTE THIS ENTIRE, FINAL, AND CORRECTED CODE BLOCK INTO: agent_5_reporter.py
# ==============================================================================
import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from financial_reporter_app.config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def apply_main_sheet_styling(ws, template, company_name):
    """Applies beautiful, professional styling to the Balance Sheet and P&L."""
    header_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
    revenue_fill = PatternFill(start_color="EBF1DE", end_color="EBF1DE", fill_type="solid")
    expenses_fill = PatternFill(start_color="F2DCDB", end_color="F2DCDB", fill_type="solid")
    net_income_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    title_font = Font(bold=True, size=16)
    subtitle_font = Font(bold=True, size=12)
    header_font = Font(bold=True)
    bold_font = Font(bold=True)
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'

    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 65
    ws.column_dimensions['C'].width = 8
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20
    
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

    for i, row_template in enumerate(template):
        row_num = i + 5
        row_type = row_template[3]
        
        if row_type in ['header', 'sub_header']:
            ws[f'B{row_num}'].font = bold_font
        elif row_type == 'total':
            fill_color = None
            particulars = ws[f'B{row_num}'].value
            if particulars and "Revenue" in particulars: fill_color = revenue_fill
            elif particulars and "Expenses" in particulars: fill_color = expenses_fill
            elif particulars and ("Profit" in particulars or "TOTAL" in particulars): fill_color = net_income_fill
            for cell in ws[row_num]:
                cell.font = bold_font
                if fill_color: cell.fill = fill_color

        for col_letter in ['D', 'E']:
            if ws[f'{col_letter}{row_num}'].value is not None:
                ws[f'{col_letter}{row_num}'].number_format = currency_format

def apply_note_sheet_styling(ws):
    """Applies professional styling to a Note sheet."""
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    title_font = Font(bold=True, size=14)
    total_font = Font(bold=True)
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'

    ws.column_dimensions['A'].width = 65; ws.column_dimensions['B'].width = 20; ws.column_dimensions['C'].width = 20
    ws.merge_cells('A1:C1'); ws['A1'].font = title_font
    for cell in ws[2]: cell.fill = header_fill; cell.font = header_font
    
    for row_idx, row in enumerate(ws.iter_rows(min_row=3, max_col=3), start=3):
        is_total_row = (str(ws[f'A{row_idx}'].value).strip().lower() == 'total')
        for cell in row:
            if cell.column > 1: cell.number_format = currency_format
            if is_total_row: cell.font = total_font; cell.border = Border(top=Side(style='thin'))

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Uses MASTER_TEMPLATE to construct a detailed, multi-sheet Schedule III
    compliant Excel report WITH PROFESSIONAL STYLING.
    """
    print("\n--- Agent 5 (Report Finalizer): Building styled report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            
            def get_value(note_id, year):
                """Helper to get values and handle special P&L calculations based on the note_id."""
                if note_id == "16_change": # Special key for P&L inventory change
                    cy = aggregated_data.get('16', {}).get('total', {}).get('CY', 0)
                    py = aggregated_data.get('16', {}).get('total', {}).get('PY', 0)
                    return cy - py if year == 'CY' else 0
                if note_id == "11_dep": # Special key for P&L depreciation
                    return aggregated_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get(year, 0)
                
                # Default behavior: get the total value for the note
                return aggregated_data.get(str(note_id), {}).get('total', {}).get(year, 0)

            # --- Process Balance Sheet and P&L ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                sheet_data, totals = [], {}
                for row_template in template:
                    col_a, particulars, note, row_type = row_template
                    row = {' ': col_a, 'Particulars': particulars, 'Note': "" if not isinstance(note, str) else note, 'As at March 31, 2025': None, 'As at March 31, 2024': None}
                    
                    if row_type in ["item", "item_no_alpha"]:
                        # Use special keys for specific P&L items
                        calc_note = note
                        if sheet_name == "Profit and Loss":
                            if particulars == "Changes in inventories": calc_note = "16_change"
                            if particulars == "Depreciation and amortization expenses": calc_note = "11_dep"
                        
                        row['As at March 31, 2025'] = get_value(calc_note, 'CY')
                        row['As at March 31, 2024'] = get_value(calc_note, 'PY')
                    
                    elif row_type == "total":
                        # This part dynamically calculates totals based on the report values
                        totals[particulars] = {'CY': row.get('As at March 31, 2025', 0), 'PY': row.get('As at March 31, 2024', 0)}

                    sheet_data.append(row)
                
                df = pd.DataFrame(sheet_data)
                # Recalculate totals based on dataframe to ensure accuracy
                for i, row_template in enumerate(template):
                    if row_template[3] == 'total':
                        notes_to_sum = row_template[2]
                        if isinstance(notes_to_sum, list):
                            cy_sum, py_sum = 0, 0
                            for note_id in notes_to_sum:
                                # Find the corresponding row in the DataFrame and sum its value
                                for idx, r in df.iterrows():
                                    if r['Note'] == note_id:
                                        cy_sum += r['As at March 31, 2025'] or 0
                                        py_sum += r['As at March 31, 2024'] or 0
                            df.at[i, 'As at March 31, 2025'] = cy_sum
                            df.at[i, 'As at March 31, 2024'] = py_sum

                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=3)
                apply_main_sheet_styling(writer.sheets[sheet_name], template, company_name)

            # --- Process Notes to Accounts ---
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info = NOTES_STRUCTURE_AND_MAPPING[note_num_str]
                note_data = aggregated_data.get(note_num_str)
                if note_data and note_data.get('sub_items'):
                    df_data, note_title = [], note_info['title']
                    def process_items(items, level=0):
                        for key, value in items.items():
                            if isinstance(value, dict) and 'CY' in value: df_data.append({'Particulars': '  '*level + key, 'As at March 31, 2025': value.get('CY'), 'As at March 31, 2024': value.get('PY')})
                            elif isinstance(value, dict):
                                df_data.append({'Particulars': '  '*level + key, 'As at March 31, 2025': None, 'As at March 31, 2024': None}); process_items(value, level + 1)
                    process_items(note_data['sub_items'])
                    df = pd.DataFrame(df_data)
                    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY'), 'As at March 31, 2024': note_data['total'].get('PY')}])
                    df = pd.concat([df, total_row], ignore_index=True)
                    sheet_name = f'Note {note_num_str}'; df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1); ws = writer.sheets[sheet_name]
                    ws['A1'].value = f'Note {note_num_str}: {note_title}'; apply_note_sheet_styling(ws)

        print("✅ Report Finalizer SUCCESS: Report generated with styling.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}"); import traceback; traceback.print_exc(); return None
