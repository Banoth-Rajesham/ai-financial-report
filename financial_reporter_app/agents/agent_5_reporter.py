# ==============================================================================
# PASTE THIS ENTIRE, FINALIZED BLOCK INTO: agent_5_reporter.py
# This agent is updated to produce a professionally styled report that
# EXACTLY matches the format and appearance of your target images.
# ==============================================================================
import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

# ================================================================================= #
# == POWERFUL STYLING ENGINE: This is where you change the report's appearance   == #
# ================================================================================= #

def apply_main_sheet_styling(ws, template, aggregated_data, company_name):
    """
    Builds and styles the main sheets (Balance Sheet, P&L) cell-by-cell.
    This guarantees the output matches your desired format exactly.
    """
    # --- STYLE DEFINITIONS: Change colors, fonts, and borders here ---
    header_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid") # Light Blue from your image
    section_header_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid") # Light Grey for EQUITY/ASSETS
    total_fill = PatternFill(start_color="A9D08E", end_color="A9D08E", fill_type="solid") # A sample total color, adjust as needed

    company_title_font = Font(name='Calibri', size=18, bold=True, color="0070C0") # Blue title
    sheet_title_font = Font(name='Calibri', size=14, bold=True)
    header_font = Font(name='Calibri', size=11, bold=True)
    bold_font = Font(name='Calibri', size=11, bold=True)
    
    thin_border_side = Side(style='thin', color="BFBFBF")
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    
    # This format shows commas, 2 decimal places, and a dash for zero.
    currency_format = '#,##0.00;(#,##0.00);"-"'

    # --- SET COLUMN WIDTHS: Adjust these values to make columns wider or narrower ---
    ws.column_dimensions['A'].width = 5   # For the (a), (b), (c)
    ws.column_dimensions['B'].width = 55  # For Particulars
    ws.column_dimensions['C'].width = 8   # For Note No.
    ws.column_dimensions['D'].width = 20  # For Current Year
    ws.column_dimensions['E'].width = 20  # For Previous Year

    # --- WRITE REPORT TITLES ---
    ws.merge_cells('A1:E1')
    ws['A1'] = company_name
    ws['A1'].font = company_title_font
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A2:E2')
    ws['A2'] = ws.title # This gets the sheet name, e.g., "Balance Sheet"
    ws['A2'].font = sheet_title_font
    ws['A2'].alignment = Alignment(horizontal='center')

    # --- WRITE COLUMN HEADERS (Row 4) ---
    ws.cell(row=4, column=2, value="Particulars").font = header_font
    ws.cell(row=4, column=3, value="Note").font = header_font
    ws.cell(row=4, column=4, value="As at March 31, 2025").font = header_font
    ws.cell(row=4, column=5, value="As at March 31, 2024").font = header_font
    for col in range(1, 6): # Apply fill and border to header row
        ws.cell(row=4, column=col).fill = header_fill
        ws.cell(row=4, column=col).border = thin_border

    # --- PROCESS TEMPLATE ROW-BY-ROW (Starting from row 5) ---
    pbt_cy, pbt_py = 0, 0
    total_revenue_cy, total_revenue_py = 0, 0
    total_expenses_cy, total_expenses_py = 0, 0
    total_tax_cy, total_tax_py = 0, 0
    
    for row_idx, row_template in enumerate(template, start=5):
        col_a, particulars, note, row_type = row_template
        
        # Write static text from the template
        ws.cell(row=row_idx, column=1, value=col_a)
        ws.cell(row=row_idx, column=2, value=particulars)
        ws.cell(row=row_idx, column=3, value=note if isinstance(note, str) and note not in ["PBT", "PAT"] else "")

        # Calculate and fetch dynamic values
        cy_val, py_val = None, None
        if row_type in ["item", "item_no_alpha"]:
            cy_val = aggregated_data.get(str(note), {}).get('total', {}).get('CY', 0)
            py_val = aggregated_data.get(str(note), {}).get('total', {}).get('PY', 0)
        elif row_type == "total" and isinstance(note, list):
            cy_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('CY', 0) for n in note)
            py_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('PY', 0) for n in note)
            if particulars.startswith("Total Revenue"): total_revenue_cy, total_revenue_py = cy_val, py_val
            if particulars == "Total Expenses": total_expenses_cy, total_expenses_py = cy_val, py_val
            if particulars.startswith("Total Tax Expense"): total_tax_cy, total_tax_py = cy_val, py_val
        elif note == "PBT":
            pbt_cy = total_revenue_cy - total_expenses_cy
            pbt_py = total_revenue_py - total_expenses_py
            cy_val, py_val = pbt_cy, pbt_py
        elif note == "PAT":
            cy_val = pbt_cy - total_tax_cy
            py_val = pbt_py - total_tax_py
        
        # Write the calculated values
        ws.cell(row=row_idx, column=4, value=cy_val).number_format = currency_format
        ws.cell(row=row_idx, column=5, value=py_val).number_format = currency_format

        # Apply styles based on the row type from the template
        particulars_cell = ws.cell(row=row_idx, column=2)
        if row_type == 'header':
            particulars_cell.font = bold_font
            particulars_cell.fill = section_header_fill
        elif row_type == 'sub_header':
            particulars_cell.font = bold_font
        elif row_type == 'total':
            particulars_cell.font = bold_font
            particulars_cell.alignment = Alignment(horizontal='right')
            # Uncomment the below to add a fill color to total rows
            # for col in range(1, 6): ws.cell(row=row_idx, column=col).fill = total_fill

        # Apply borders to all data cells
        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).border = thin_border


def apply_note_sheet_styling(ws, note_title):
    """Applies professional styling to an individual Note sheet."""
    # --- STYLE DEFINITIONS for Notes ---
    header_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
    total_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    title_font = Font(name='Calibri', size=14, bold=True)
    header_font = Font(name='Calibri', size=11, bold=True)
    total_font = Font(name='Calibri', size=11, bold=True)
    currency_format = '#,##0.00;(#,##0.00);"-"'
    thin_border_side = Side(style='thin', color="BFBFBF")
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    # --- SET COLUMN WIDTHS for Notes ---
    ws.column_dimensions['A'].width = 70
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20

    # Style the title
    ws.merge_cells('A1:C1')
    ws['A1'] = note_title
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')
    
    # Style the header row (which is row 2)
    for cell in ws[2]:
        cell.fill = header_fill
        cell.font = header_font
    
    # Style all data rows
    for row in ws.iter_rows(min_row=2, max_col=3):
        is_total_row = (row[0].value and 'total' in str(row[0].value).lower())
        for cell in row:
            cell.border = thin_border
            if cell.column > 1 and isinstance(cell.value, (int, float)):
                cell.number_format = currency_format
            if is_total_row:
                cell.font = total_font
                cell.fill = total_fill


# --- MAIN AGENT FUNCTION ---
def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Builds the final, professionally styled, multi-sheet Excel report.
    """
    print("\n--- Agent 5 (Report Finalizer): Building styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            
            # Remove the default sheet created by pandas
            if 'Sheet' in writer.book.sheetnames:
                del writer.book['Sheet']

            # 1. CREATE AND STYLE MAIN SHEETS
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), 
                                         ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                ws = writer.book.create_sheet(sheet_name)
                writer.sheets[sheet_name] = ws
                apply_main_sheet_styling(ws, template, aggregated_data, company_name)
            
            # 2. CREATE AND STYLE ALL INDIVIDUAL NOTE SHEETS
            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=int):
                note_info = NOTES_STRUCTURE_AND_MAPPING[note_num_str]
                note_data = aggregated_data.get(note_num_str)
                sheet_name = f'Note {note_num_str}'
                note_title = f'Note {note_num_str}: {note_info["title"]}'

                df_data = []
                # Recursive function to handle nested items with proper indentation
                def process_sub_items(items, level=0):
                    for key, value in items.items():
                        indent = '    ' * level
                        if isinstance(value, dict) and 'CY' in value and 'PY' in value:
                            df_data.append({'Particulars': indent + key, 'As at March 31, 2025': value.get('CY', 0), 'As at March 31, 2024': value.get('PY', 0)})
                        elif isinstance(value, dict):
                            # This is a sub-header, print its name and recurse
                            df_data.append({'Particulars': indent + key, 'As at March 31, 2025': None, 'As at March 31, 2024': None})
                            process_sub_items(value, level + 1)
                
                if note_data and note_data.get('sub_items'):
                    process_sub_items(note_data['sub_items'])
                
                df = pd.DataFrame(df_data)
                
                if note_data and not df.empty:
                    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY', 0), 'As at March 31, 2024': note_data['total'].get('PY', 0)}])
                    df = pd.concat([df, total_row], ignore_index=True)
                
                df_to_write = df[['Particulars', 'As at March 31, 2025', 'As at March 31, 2024']] if not df.empty else pd.DataFrame([{'Particulars': 'No data available for this note.'}])
                df_to_write.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                
                ws_note = writer.sheets[sheet_name]
                apply_note_sheet_styling(ws_note, note_title)

        print("✅ Report Finalizer SUCCESS: Styled report generated in memory.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: An error occurred while building the report. Error: {e}")
        import traceback
        traceback.print_exc()
        return None
