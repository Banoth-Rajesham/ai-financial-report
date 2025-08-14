# ==============================================================================
# FILE: agents/agent_1_intake.py (DEFINITIVE UPDATE WITH T-FORMAT SUPPORT)
# ==============================================================================
import pandas as pd

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, intelligently detects if the format is T-account or
    vertical, transforms T-accounts if necessary, and creates unique, contextual
    keys for each data row (e.g., "Header|Particular").
    """
    print("\n--- Agent 1 (Data Intake): Reading, parsing, and adding context... ---")
    try:
        xls = pd.ExcelFile(file_object)
        all_data_rows = []

        # Process every sheet to find financial data
        for sheet_name in xls.sheet_names:
            print(f"--- Processing sheet: {sheet_name} ---")
            raw_df = pd.read_excel(xls, sheet_name=sheet_name, header=None).fillna('')
            if raw_df.empty:
                continue

            # --- Detect Format (T-Account vs. Vertical) ---
            is_t_format = False
            header_row_index = 0
            # Heuristic: A T-account has distinct left/right headers in the same row
            for i, row in raw_df.head(15).iterrows():
                row_str = ' '.join(str(c).lower() for c in row).strip()
                t_format_keywords = (('liabilities' in row_str and 'assets' in row_str) or
                                     ('debit' in row_str and 'credit' in row_str) or
                                     ('dr.' in row_str and 'cr.' in row_str))
                if t_format_keywords:
                    is_t_format = True
                    header_row_index = i
                    print(f"Detected T-format in sheet '{sheet_name}' at row {i}.")
                    break
            
            # Re-read the sheet with the correct header row
            df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_index).dropna(how='all', axis=1)
            df.columns = [str(c) for c in df.columns] # Ensure column names are strings

            # --- Transform Data if T-Format ---
            if is_t_format:
                # Find the middle of the dataframe to split it
                midpoint = len(df.columns) // 2
                
                # Left side of the T-account (e.g., Liabilities or Debits)
                left_df = df.iloc[:, :midpoint].copy()
                left_header = str(left_df.columns[0]).strip()
                left_df.columns = ['Particulars', 'Amount_CY'] + ['Amount_PY'] * (len(left_df.columns) - 2)
                for _, row in left_df.iterrows():
                    particular = str(row['Particulars']).strip()
                    if particular:
                         all_data_rows.append({
                            'Particulars': f"{left_header}|{particular}",
                            'Amount_CY': row.get('Amount_CY', 0),
                            'Amount_PY': row.get('Amount_PY', 0)
                        })

                # Right side of the T-account (e.g., Assets or Credits)
                right_df = df.iloc[:, midpoint:].copy()
                right_header = str(right_df.columns[0]).strip()
                right_df.columns = ['Particulars', 'Amount_CY'] + ['Amount_PY'] * (len(right_df.columns) - 2)
                for _, row in right_df.iterrows():
                    particular = str(row['Particulars']).strip()
                    if particular:
                        all_data_rows.append({
                            'Particulars': f"{right_header}|{particular}",
                            'Amount_CY': row.get('Amount_CY', 0),
                            'Amount_PY': row.get('Amount_PY', 0)
                        })
            else: # --- Process Vertical Format ---
                print(f"Detected Vertical format in sheet '{sheet_name}'.")
                # Find the 'Particulars' and amount columns
                particulars_col = None
                cy_col, py_col = None, None
                for col in df.columns:
                    col_str = str(col).lower()
                    if 'particular' in col_str and particulars_col is None: particulars_col = col
                    if ('cy' in col_str or 'current' in col_str) and cy_col is None: cy_col = col
                    if ('py' in col_str or 'previous' in col_str) and py_col is None: py_col = col

                if not particulars_col or not cy_col:
                    print(f"Skipping sheet '{sheet_name}': Could not identify required columns.")
                    continue

                current_header = ""
                for _, row in df.iterrows():
                    particular = str(row[particulars_col]).strip()
                    is_header = pd.isna(row[cy_col]) or row[cy_col] == ''
                    
                    if is_header and 'total' not in particular.lower():
                        current_header = particular
                        continue
                    
                    if 'total' in particular.lower() or not particular:
                        continue
                        
                    contextual_key = f"{current_header}|{particular}" if current_header else particular
                    all_data_rows.append({
                        'Particulars': contextual_key,
                        'Amount_CY': row.get(cy_col, 0),
                        'Amount_PY': row.get(py_col, 0) if py_col else 0
                    })

        if not all_data_rows:
            print("❌ Intake FAILED: Could not extract any valid data rows from the Excel file.")
            return None

        # --- Final Cleanup and Return ---
        final_df = pd.DataFrame(all_data_rows)
        final_df['Amount_CY'] = pd.to_numeric(final_df['Amount_CY'], errors='coerce').fillna(0)
        final_df['Amount_PY'] = pd.to_numeric(final_df['Amount_PY'], errors='coerce').fillna(0)
        
        print(f"✅ Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows from all sheets.")
        return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e}")
        return None
