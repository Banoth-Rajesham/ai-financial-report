# ==============================================================================
# PASTE THIS ENTIRE, COMPLETE, AND FINAL CODE BLOCK INTO: agent_5_reporter.py
# This version produces a beautifully styled, multi-sheet Excel report.
# ==============================================================================
import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
# This assumes your config file is in a folder that Python can see.
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

# ================================================================================= #
# == STYLING ENGINE: This is where you change the look of your Excel report.     == #
# ================================================================================= #

def apply_main_sheet_styling(ws, template, aggregated_data, company_name):
    """
    Builds and styles the main sheets (Balance Sheet, P&L) cell-by-cell
    based on the template, guaranteeing a professional and exact format.
    """
    # --- STYLE DEFINITIONS: Change colors, fonts, and borders here ---
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid") # Dark Blue
    total_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid") # Light Blue
    header_font = Font(bold=True, color="FFFFFF") # White text
    bold_font = Font(bold=True)
    title_font = Font(size=16, bold=True)
    thin_border_side = Side(style='thin', color="BFBFBF") # Grey border
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    # This format shows commas for thousands, parentheses for negatives, and a dash for zero.
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'

    # --- SET COLUMN WIDTHS: Adjust these values to make columns wider or narrower ---
    ws.column_dimensions['A'].width = 4
    ws.column_dimensions['B'].width = 60
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20
    
    # --- WRITE REPORT TITLES ---
    ws.merge_cells('A1:E1')
    ws['A1'] = company_name
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A2:E2')
    ws['A2'] = ws.title
    ws['A2'].font = Font(size=14, bold=True)
    ws['A2'].alignment = Alignment(horizontal='center')

    # --- PROCESS TEMPLATE ROW-BY-ROW ---
    # These variables are needed to calculate PBT and PAT on the P&L sheet
    pbt_cy, pbt_py = 0, 0
    total_revenue_cy, total_revenue_py = 0, 0
    total_expenses_cy, total_expenses_py = 0, 0
    total_tax_cy, total_tax_py = 0, 0
    
    # Write the main data table
    for row_idx, row_template in enumerate(template, start=4):
        # Unpack the template for the current row
        col_a, particulars, note, row_type = row_template
        
        # Write static text from the template
        ws.cell(row=row_idx, column=1, value=col_a)
        ws.cell(row=row_idx, column=2, value=particulars)
        # Only write note number if it's not a calculated field like PBT
        ws.cell(row=row_idx, column=3, value=note if isinstance(note, str) and note not in ["PBT", "PAT"] else "")

        # Calculate and fetch dynamic values
        cy_val, py_val = None, None
        if row_type in ["item", "item_no_alpha"]:
            note_str = str(note)
            cy_val = aggregated_data.get(note_str, {}).get('total', {}).get('CY', 0)
            py_val = aggregated_data.get(note_str, {}).get('total', {}).get('PY', 0)
        
        elif row_type == "total" and isinstance(note, list):
            cy_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('CY', 0) for n in note)
            py_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('PY', 0) for n in note)
            
            # Store totals needed for P&L calculations
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
        
        # Write the calculated Current Year and Previous Year values
        ws.cell(row=row_idx, column=4, value=cy_val).number_format = currency_format
        ws.cell(row=row_idx, column=5, value=py_val).number_format = currency_format

        # Apply styles based on the row type defined in the template
        current_row = ws[row_idx]
        if row_type == 'header_col':
            for cell in current_row: 
                cell.font = header_font
                cell.fill = header_fill
        elif row_type in ['header', 'sub_header']:
            ws[f'B{row_idx}'].font = bold_font
        elif row_type == 'total':
            for cell in ws[row_idx:row_idx]: cell.font = bold_font # Slicing ensures all cells get styled
            ws[f'B{row_idx}'].font = bold_font
            ws[f'B{row_idx}'].alignment = Alignment(horizontal='right')
            ws[f'D{row_idx}'].fill = total_fill
            ws[f'E{row_idx}'].fill = total_fill
        
        # Apply a border to all cells in the row
        for cell_idx in range(1, 6):
            ws.cell(row=row_idx, column=cell_idx).border = thin_border


def apply_note_sheet_styling(ws, note_title):
    """Applies professional styling to an individual Note sheet."""
    # --- STYLE DEFINITIONS for Notes: Change colors and fonts here ---
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid") # Dark Blue
    total_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid") # Light Blue
    title_font = Font(bold=True, size=14)
    header_font = Font(bold=True, color="FFFFFF") # White text
    total_font = Font(bold=True)
    currency_format = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
    thin_border_side = Side(style='thin', color="BFBFBF")
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    # --- SET COLUMN WIDTHS for Notes ---
    ws.column_dimensions['A'].width = 65
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20

    # Style the title
    ws.merge_cells('A1:C1')
    ws['A1'] = note_title
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')
    
    # Style the header row
    for cell in ws[2]:
        cell.fill = header_fill
        cell.font = header_font
    
    # Style all data rows
    for row in ws.iter_rows(min_row=2, max_col=3):
        is_total_row = (row[0].value and 'total' in str(row[0].value).lower())
        for cell in row:
            cell.border = thin_border
            # Apply currency format to number columns
            if cell.column > 1 and isinstance(cell.value, (int, float)):
                cell.number_format = currency_format
            # Apply special formatting for the 'Total' row
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
            
            # 1. CREATE AND STYLE MAIN SHEETS
            # The default 'Sheet' is removed later
            if 'Sheet' in writer.book.sheetnames:
                del writer.book['Sheet']

            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), 
                                         ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                # Create a new sheet and apply the main styling and data writing function
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
                # This recursive function handles nested sub-items with indentation
                def process_sub_items(items, level=0):
                    for key, value in items.items():
                        indent = '    ' * level
                        # If it's a final item with values
                        if isinstance(value, dict) and 'CY' in value and 'PY' in value:
                            df_data.append({'Particulars': indent + key, 'As at March 31, 2025': value.get('CY', 0), 'As at March 31, 2024': value.get('PY', 0)})
                        # If it's a sub-header for more nested items
                        elif isinstance(value, dict):
                            df_data.append({'Particulars': indent + key, 'As at March 31, 2025': None, 'As at March 31, 2024': None})
                            process_sub_items(value, level + 1)
                
                if note_data and note_data.get('sub_items'):
                    process_sub_items(note_data['sub_items'])
                
                # Convert the collected data into a DataFrame
                df = pd.DataFrame(df_data)
                
                # Add the 'Total' row at the end
                if note_data:
                    total_row = pd.DataFrame([{'Particulars': 'Total', 'As at March 31, 2025': note_data['total'].get('CY', 0), 'As at March 31, 2024': note_data['total'].get('PY', 0)}])
                    df = pd.concat([df, total_row], ignore_index=True)
                
                # Write the DataFrame to the note's sheet
                df_to_write = df[['Particulars', 'As at March 31, 2025', 'As at March 31, 2024']] if not df.empty else pd.DataFrame([{}])
                df_to_write.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                
                # Apply the styling to the newly created note sheet
                ws_note = writer.sheets[sheet_name]
                apply_note_sheet_styling(ws_note, note_title)

        print("✅ Report Finalizer SUCCESS: Styled report generated in memory.")
        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: An error occurred while building the report. Error: {e}")
        import traceback
        traceback.print_exc()
        return None
