# ==============================================================================
# FILE: agents/agent_1_intake.py (FINAL, ROBUST VERSION)
# ==============================================================================
import pandas as pd
import re

def clean_numeric(series):
    """A more robust function to clean and convert a column to numbers."""
    if series is None:
        return pd.Series(dtype='float64')
    # Convert to string, remove currency symbols, commas, and handle parentheses for negatives
    series_str = series.astype(str)
    series_str = series_str.str.replace(r'[₹,]', '', regex=True)
    series_str = series_str.str.strip()
    # Handle accounting format for negatives, e.g., (500.00) -> -500.00
    series_str = series_str.str.replace(r'^\((.*)\)$', r'-\1', regex=True)
    # Convert to numeric, coercing errors to NaN, then fill NaN with 0
    return pd.to_numeric(series_str, errors='coerce').fillna(0)

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, robustly detects T-account or vertical format,
    transforms T-accounts, and creates unique, contextual keys for each data row.
    This version includes enhanced debugging and more flexible data detection.
    """
    print("\n--- Agent 1 (Data Intake - Final Version): Reading and processing Excel file... ---")
    try:
        xls = pd.ExcelFile(file_object)
        all_data_rows = []

        for sheet_name in xls.sheet_names:
            print(f"\n--- Processing sheet: '{sheet_name}' ---")
            raw_df = pd.read_excel(xls, sheet_name=sheet_name, header=None).fillna('')
            if raw_df.empty:
                print(f"Sheet '{sheet_name}' is empty. Skipping.")
                continue

            # --- Find Header Row and Detect Format ---
            header_row_index = -1
            is_t_format = False
            for i, row in raw_df.head(15).iterrows():
                row_str = ' '.join(str(c).lower() for c in row if c).strip()
                if ('liabilities' in row_str and 'assets' in row_str) or \
                   ('debit' in row_str and 'credit' in row_str) or \
                   (re.search(r'\bdr\.?\b', row_str) and re.search(r'\bcr\.?\b', row_str)):
                    is_t_format = True
                    header_row_index = i
                    print(f"Detected T-format in '{sheet_name}' at row {header_row_index}.")
                    break
            
            if header_row_index == -1:
                 for i, row in raw_df.head(15).iterrows():
                    row_str = ' '.join(str(c).lower() for c in row if c).strip()
                    if 'particular' in row_str and ('amount' in row_str or 'cy' in row_str or 'current' in row_str):
                        header_row_index = i
                        print(f"Detected Vertical format in '{sheet_name}' at row {header_row_index}.")
                        break
            
            if header_row_index == -1:
                print(f"Could not detect a valid header in '{sheet_name}'. Skipping sheet.")
                continue

            df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_index).dropna(how='all').reset_index(drop=True)
            df.columns = [str(c).strip() for c in df.columns]

            # --- Process Data Based on Detected Format ---
            if is_t_format:
                # Find the split point for the T-account
                asset_col_index = -1
                for i, col in enumerate(df.columns):
                    if 'asset' in str(col).lower():
                        asset_col_index = i
                        break
                
                if asset_col_index == -1 or asset_col_index == 0:
                    print(f"Could not determine T-account split for sheet '{sheet_name}'. Skipping.")
                    continue

                # Extract left side (Liabilities/Debits)
                left_df = df.iloc[:, :asset_col_index].copy()
                left_particulars = left_df.iloc[:, 0]
                left_amounts_cy = clean_numeric(left_df.iloc[:, 1])
                left_header = str(df.columns[0])

                # Extract right side (Assets/Credits)
                right_df = df.iloc[:, asset_col_index:].copy()
                right_particulars = right_df.iloc[:, 0]
                right_amounts_cy = clean_numeric(right_df.iloc[:, 1])
                right_header = str(df.columns[asset_col_index])

                # Combine into a single vertical list
                for i, particular in enumerate(left_particulars):
                    if pd.notna(particular) and str(particular).strip():
                        all_data_rows.append({'Particulars': f"{left_header}|{str(particular).strip()}", 'Amount_CY': left_amounts_cy[i], 'Amount_PY': 0})
                for i, particular in enumerate(right_particulars):
                     if pd.notna(particular) and str(particular).strip():
                        all_data_rows.append({'Particulars': f"{right_header}|{str(particular).strip()}", 'Amount_CY': right_amounts_cy[i], 'Amount_PY': 0})
            
            else: # Process Vertical Format
                particulars_col = next((col for col in df.columns if 'particular' in str(col).lower()), None)
                cy_col = next((col for col in df.columns if 'cy' in str(col).lower() or 'current' in str(col).lower()), None)
                py_col = next((col for col in df.columns if 'py' in str(col).lower() or 'previous' in str(col).lower()), None)

                if not particulars_col or not cy_col:
                    print(f"Could not identify Particulars/CY columns in sheet '{sheet_name}'. Skipping.")
                    continue
                
                df[cy_col] = clean_numeric(df[cy_col])
                if py_col: df[py_col] = clean_numeric(df[py_col])

                current_header = ""
                for _, row in df.iterrows():
                    particular = str(row[particulars_col]).strip()
                    # A row is a header if its amount is 0 and it's not a total row
                    is_header = row[cy_col] == 0 and 'total' not in particular.lower()

                    if is_header:
                        current_header = particular
                        continue
                    
                    if not particular or 'total' in particular.lower():
                        continue

                    contextual_key = f"{current_header}|{particular}" if current_header else particular
                    all_data_rows.append({
                        'Particulars': contextual_key,
                        'Amount_CY': row[cy_col],
                        'Amount_PY': row.get(py_col, 0)
                    })

        if not all_data_rows:
            print("❌ Intake FAILED: No valid data rows could be extracted from the Excel file.")
            st.error("Data Intake Failed: The agent could not find any recognizable financial data in the uploaded Excel file. Please check the file format.")
            return None

        final_df = pd.DataFrame(all_data_rows).fillna(0)
        print(f"✅ Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows.")
        # For debugging, you can uncomment the next line to see the extracted data in the logs
        # print(final_df.to_string())
        return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with a critical exception: {e}")
        st.error(f"A critical error occurred during file intake: {e}")
        return None
