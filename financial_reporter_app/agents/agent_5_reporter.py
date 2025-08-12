# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: agent_5_reporter.py
# ==============================================================================
import pandas as pd
import io
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# THIS IS THE PERMANENT FIX: Use a relative import to go up one level to find config.py
from ..config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Constructs a detailed, styled, multi-sheet Excel report that
    exactly matches the user's provided screenshot format.
    """
    print("\n--- Agent 5 (Report Finalizer): Building professionally styled Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            workbook = writer.book

            # --- Define All Cell Formats ---
            title_format = Font(name='Calibri', size=14, bold=True)
            subtitle_format = Font(name='Calibri', size=11, bold=True)
            header_format = Font(name='Calibri', size=11, bold=True)
            section_header_format = Font(name='Calibri', size=11, bold=True)
            total_font = Font(name='Calibri', size=11, bold=True)
            normal_font = Font(name='Calibri', size=11)
            
            center_align = Alignment(horizontal='center', vertical='center')
            left_align = Alignment(horizontal='left', vertical='center')
            right_align = Alignment(horizontal='right', vertical='center')
            
            header_fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid") # Light Grey
            total_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid") # Light Blue
            
            top_border = Border(top=Side(style='thin'))
            
            currency_format = '#,##0;(#,##0);"-"'

            def get_val(note_id, year):
                if note_id == "16_change": return (aggregated_data.get('16', {}).get('total', {}).get('CY', 0) or 0) - (aggregated_data.get('16', {}).get('total', {}).get('PY', 0) or 0) if year == 'CY' else 0
                if note_id == "11_dep": return aggregated_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get(year, 0)
                return aggregated_data.get(str(note_id), {}).get('total', {}).get(year, 0)

            # --- Process Balance Sheet and Profit & Loss ---
            for sheet_name, template in [("Balance Sheet", MASTER_TEMPLATE["Balance Sheet"]), ("Profit and Loss", MASTER_TEMPLATE["Profit and Loss"])]:
                # Create the sheet and set initial widths
                ws = workbook.create_sheet(title=sheet_name)
                ws.column_dimensions['A'].width = 4
                ws.column_dimensions['B'].width = 45
                ws.column_dimensions['C'].width = 8
                ws.column_dimensions['D'].width = 18
                ws.column_dimensions['E'].width = 18

                # Write Titles
                ws.merge_cells('A1:E1'); cell = ws['A1']; cell.value = company_name; cell.font = title_format; cell.alignment = center_align
                ws.merge_cells('A2:E2'); cell = ws['A2']; cell.value = sheet_name; cell.font = subtitle_format; cell.alignment = center_align

                # Write Header Row
                header_row = ws[4]
                header_values = ["", "Particulars", "Note", "As at March 31, 2025", "As at March 31, 2024"]
                for i, val in enumerate(header_values):
                    cell = header_row[i]; cell.value = val; cell.font = header_font; cell.fill = header_fill; cell.alignment = center_align

                # Write Data Rows from Template
                current_row_num = 5
                for r_template in template:
                    row_type = r_template[3]
                    if row_type == "spacer":
                        current_row_num += 1
                        continue

                    # Write the data first
                    ws.cell(row=current_row_num, column=1, value=r_template[0])
                    ws.cell(row=current_row_num, column=2, value=r_template[1])
                    
                    if row_type in ["item", "item_no_alpha", "total"]:
                         note_ref = r_template[2]
                         if isinstance(note_ref, str): ws.cell(row=current_row_num, column=3, value=note_ref)

                         cy_val, py_val = 0, 0
                         if isinstance(note_ref, list):
                             cy_val = sum(get_val(n, 'CY') for n in note_ref)
                             py_val = sum(get_val(n, 'PY') for n in note_ref)
                         else:
                             cy_val, py_val = get_val(note_ref, 'CY'), get_val(note_ref, 'PY')
                         
                         ws.cell(row=current_row_num, column=4, value=cy_val)
                         ws.cell(row=current_row_num, column=5, value=py_val)
                    
                    # Apply Formatting
                    row_to_style = ws[current_row_num]
                    for cell in row_to_style: cell.font = normal_font
                    ws[f'C{current_row_num}'].alignment = center_align
                    ws[f'D{current_row_num}'].number_format = currency_format; ws[f'D{current_row_num}'].alignment = right_align
                    ws[f'E{current_row_num}'].number_format = currency_format; ws[f'E{current_row_num}'].alignment = right_align
                    
                    if row_type in ['header', 'sub_header']:
                        ws[f'B{current_row_num}'].font = section_header_format
                    elif row_type == 'total':
                        for cell in row_to_style:
                            cell.font = total_font
                            cell.fill = total_fill
                            cell.border = top_border
                    
                    current_row_num += 1
                
            # Remove the default sheet created by openpyxl
            if 'Sheet' in workbook.sheetnames:
                workbook.remove(workbook['Sheet'])
            
            # (Note generation logic can be added here if needed, following the same styling principles)

        return output.getvalue()
    except Exception as e:
        print(f"❌ Report Finalizer FAILED: {e}"); import traceback; traceback.print_exc(); return None
