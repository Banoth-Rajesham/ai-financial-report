# ==============================================================================
# FILE: agents/agent_5_reporter.py (UPDATED)
# ==============================================================================
import pandas as pd
import io

def report_finalizer_agent(aggregated_data, company_name):
    """
    AGENT 5: Takes the final hierarchical data and writes it to a structured
    Excel report, including all nested notes and sub-items.
    """
    print("\n--- Agent 5 (Report Finalizer): Generating final Excel report... ---")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            header_format = workbook.add_format({'bold': True, 'font_size': 12, 'bg_color': '#DDEBF7', 'border': 1})
            title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})

            # This recursive function is the key to writing the full hierarchy
            def traverse_and_write(sheet, data_node, indent_level=0):
                """Recursively writes data nodes to the sheet with indentation."""
                nonlocal row_num # Allows modification of the row_num from the outer scope
                
                # Sort keys to ensure consistent order, putting 'total' last
                sorted_keys = sorted(data_node.keys(), key=lambda x: (x.lower() == 'total', x))

                for key in sorted_keys:
                    value = data_node[key]
                    
                    # Indentation for visual hierarchy in the Excel sheet
                    prefix = "    " * indent_level
                    
                    # Check if it's a data item (leaf node) with CY/PY values
                    if isinstance(value, dict) and 'CY' in value and 'PY' in value:
                        sheet.write(row_num, 0, f"{prefix}{key}")
                        sheet.write(row_num, 1, value.get('CY', 0))
                        sheet.write(row_num, 2, value.get('PY', 0))
                        row_num += 1
                    
                    # Check if it's a section with sub-items (internal node)
                    elif isinstance(value, dict):
                        # Write the section header
                        sheet.write(row_num, 0, f"{prefix}{key}", workbook.add_format({'bold': True}))
                        row_num += 1
                        # Recurse into the sub-items
                        traverse_and_write(sheet, value, indent_level + 1)

            # --- Write each Note to its own sheet ---
            for note_num, note_data in aggregated_data.items():
                sheet_name = f"Note {note_num}"
                worksheet = workbook.add_worksheet(sheet_name)
                
                # Write Titles and Headers
                worksheet.merge_range('A1:C1', f"Note {note_num}: {note_data.get('title', '')}", title_format)
                worksheet.write('A3', 'Particulars', header_format)
                worksheet.write('B3', 'Amount (CY)', header_format)
                worksheet.write('C3', 'Amount (PY)', header_format)
                worksheet.set_column('A:A', 50) # Widen the particulars column
                worksheet.set_column('B:C', 15)

                row_num = 3 # Start writing data from row 4 (index 3)
                
                # Start the recursive writing process for the note's sub_items
                if 'sub_items' in note_data:
                    traverse_and_write(worksheet, note_data['sub_items'])

        print("✅ Report Finalizer SUCCESS: Excel file created in memory.")
        return output.getvalue()

    except Exception as e:
        print(f"❌ Report Finalizer FAILED with exception: {e}")
        return None
