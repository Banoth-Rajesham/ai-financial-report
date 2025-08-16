# ==============================================================================
# FILE: agents/agent_5_reporter.py (DEFINITIVE CORRECTION)
# ==============================================================================
import pandas as pd
import io
from config import MASTER_TEMPLATE, NOTES_STRUCTURE_AND_MAPPING

def create_main_sheet_df(aggregated_data, template):
    """Helper function to create the dataframe for Balance Sheet and P&L."""
    sheet_data = []
    calc_totals = {}

    for row_template in template:
        col_a, particulars, note, row_type = row_template
        if row_type == "header_col":
            continue
        
        row_data = {" ": col_a, "Particulars": particulars, "Note": "" if not isinstance(note, str) else note, "Amount (CY)": None, "Amount (PY)": None}
        
        if row_type in ["item", "item_no_alpha"]:
            note_str = str(note)
            # Special handling for Depreciation which is part of Note 11
            if particulars == "Depreciation and amortization expenses":
                 row_data['Amount (CY)'] = aggregated_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get('CY', 0)
                 row_data['Amount (PY)'] = aggregated_data.get('11', {}).get('sub_items', {}).get('Depreciation for the year', {}).get('PY', 0)
            else:
                row_data['Amount (CY)'] = aggregated_data.get(note_str, {}).get('total', {}).get('CY', 0)
                row_data['Amount (PY)'] = aggregated_data.get(note_str, {}).get('total', {}).get('PY', 0)

        elif row_type == "total" and isinstance(note, list):
            cy_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('CY', 0) for n in note)
            py_val = sum(aggregated_data.get(str(n), {}).get('total', {}).get('PY', 0) for n in note)
            row_data['Amount (CY)'], row_data['Amount (PY)'] = cy_val, py_val
            if "Total Revenue" in particulars: calc_totals['rev_cy'], calc_totals['rev_py'] = cy_val, py_val
            if "Total Expenses" in particulars: calc_totals['exp_cy'], calc_totals['exp_py'] = cy_val, py_val
            if "Total Tax Expense" in particulars: calc_totals['tax_cy'], calc_totals['tax_py'] = cy_val, py_val

        elif note == "PBT":
            pbt_cy = calc_totals.get('rev_cy', 0) - calc_totals.get('exp_cy', 0)
            pbt_py = calc_totals.get('rev_py', 0) - calc_totals.get('exp_py', 0)
            row_data['Amount (CY)'], row_data['Amount (PY)'] = pbt_cy, pbt_py
            calc_totals['pbt_cy'], calc_totals['pbt_py'] = pbt_cy, pbt_py

        elif note == "PAT":
            pat_cy = calc_totals.get('pbt_cy', 0) - calc_totals.get('tax_cy', 0)
            pat_py = calc_totals.get('pbt_py', 0) - calc_totals.get('tax_py', 0)
            row_data['Amount (CY)'], row_data['Amount (PY)'] = pat_cy, pat_py
        
        sheet_data.append(row_data)

    return pd.DataFrame(sheet_data)

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Takes final data and writes a complete, multi-sheet Excel report
    including Balance Sheet, P&L, and all detailed notes.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final multi-sheet Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            header_format = workbook.add_format({'bold': True, 'font_size': 11, 'bg_color': '#DDEBF7', 'border': 1, 'align': 'center'})
            title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})
            
            # --- 1. Write Main Sheets: Balance Sheet and P&L ---
            bs_df = create_main_sheet_df(aggregated_data, MASTER_TEMPLATE["Balance Sheet"])
            bs_df.to_excel(writer, sheet_name="Balance Sheet", index=False, startrow=2)
            worksheet_bs = writer.sheets['Balance Sheet']
            worksheet_bs.merge_range('A1:E1', company_name, title_format)
            worksheet_bs.merge_range('A2:E2', 'Balance Sheet', workbook.add_format({'bold': True, 'font_size': 12, 'align': 'center'}))
            for col_num, value in enumerate(bs_df.columns.values):
                 worksheet_bs.write(2, col_num, value, header_format)
            worksheet_bs.set_column('B:B', 45) # Widen Particulars

            pl_df = create_main_sheet_df(aggregated_data, MASTER_TEMPLATE["Profit and Loss"])
            pl_df.to_excel(writer, sheet_name="Profit and Loss", index=False, startrow=2)
            worksheet_pl = writer.sheets['Profit and Loss']
            worksheet_pl.merge_range('A1:E1', company_name, title_format)
            worksheet_pl.merge_range('A2:E2', 'Statement of Profit and Loss', workbook.add_format({'bold': True, 'font_size': 12, 'align': 'center'}))
            for col_num, value in enumerate(pl_df.columns.values):
                 worksheet_pl.write(2, col_num, value, header_format)
            worksheet_pl.set_column('B:B', 45)

            # --- 2. Write all Note Sheets ---
            def traverse_and_write(sheet, data_node, indent_level=0):
                nonlocal row_num
                sorted_keys = sorted(data_node.keys(), key=lambda x: (x.lower() == 'total', x))
                for key in sorted_keys:
                    value = data_node[key]
                    prefix = "    " * indent_level
                    if isinstance(value, dict) and 'CY' in value and 'PY' in value:
                        is_total = 'total' in key.lower()
                        cell_format = workbook.add_format({'bold': is_total})
                        sheet.write(row_num, 0, f"{prefix}{key}", cell_format)
                        sheet.write(row_num, 1, value.get('CY', 0))
                        sheet.write(row_num, 2, value.get('PY', 0))
                        row_num += 1
                    elif isinstance(value, dict):
                        sheet.write(row_num, 0, f"{prefix}{key}", workbook.add_format({'bold': True}))
                        row_num += 1
                        traverse_and_write(sheet, value, indent_level + 1)

            for note_num_str in sorted(NOTES_STRUCTURE_AND_MAPPING.keys(), key=lambda x: int(x)):
                note_data = aggregated_data.get(note_num_str)
                if not (note_data and 'sub_items' in note_data): continue

                sheet_name = f"Note {note_num_str}"
                worksheet = workbook.add_worksheet(sheet_name)
                
                worksheet.merge_range('A1:C1', f"Note {note_num_str}: {note_data.get('title', '')}", title_format)
                worksheet.write('A3', 'Particulars', header_format)
                worksheet.write('B3', 'Amount (CY)', header_format)
                worksheet.write('C3', 'Amount (PY)', header_format)
                worksheet.set_column('A:A', 60)
                worksheet.set_column('B:C', 18)

                row_num = 3
                traverse_and_write(worksheet, note_data['sub_items'])
                
                # Add overall total at the bottom
                total_format = workbook.add_format({'bold': True, 'top': 1})
                worksheet.write(row_num, 0, "Total", total_format)
                worksheet.write(row_num, 1, note_data.get('total', {}).get('CY', 0), total_format)
                worksheet.write(row_num, 2, note_data.get('total', {}).get('PY', 0), total_format)

        print("✅ Report Finalizer SUCCESS: Complete Excel file created in memory.")
        return output.getvalue()

    except Exception as e:
        import traceback
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        traceback.print_exc()
        return None
