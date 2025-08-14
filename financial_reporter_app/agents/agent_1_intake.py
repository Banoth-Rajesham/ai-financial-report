# ==============================================================================
# FILE: agents/agent_1_intake.py (FINAL, ROBUST VERSION)
# ==============================================================================
import pandas as pd
import re

def clean_numeric(series):
    """
    A more robust function to clean and convert a column to numbers.
    This handles currency symbols, commas, and accounting-style negatives.
    """
    if series is None:
        return pd.Series(dtype='float64')
    
    # Convert to string, which is necessary for the replace operations
    series_str = series.astype(str)
    
    # 1. Remove currency symbols (₹, $, etc.) and commas
    series_str = series_str.str.replace(r'[₹,]', '', regex=True)
    
    # 2. Handle accounting format for negatives, e.g., (500.00) -> -500.00
    series_str = series_str.str.replace(r'^\s*\((.*)\)\s*$', r'-\1', regex=True)
    
    # 3. Convert to numeric, coercing any errors (like text) to NaN, then fill NaN with 0
    return pd.to_numeric(series_str, errors='coerce').fillna(0)

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, robustly detects T-account or vertical format,
    transforms T-accounts, and creates unique, contextual keys for each data row.
    This version includes enhanced debugging and flexible data detection.
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
                   (re.search(r'\bdr\.?\b', row_str) and re.search(r'\bcr\.?\b', row_str)):
                    is_t_format = True
                    header_row_index = i
                    print(f"Detected T-format in '{sheet_name}' at row {header_row_index}.")
                    break
            
            if header_row_index == -1: # Fallback to check for vertical format
                 for i, row in raw_df.head(15).iterrows():
                    row_str = ' '.join(str(c).lower() for c in row if c).strip()
                    if 'particular' in row_str and ('amount' in row_str or 'cy' in row_str):
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
                # Find the split point by looking for the "Assets" or "Credit" column
                split_col_index = -1
                for i, col in enumerate(df.columns):
                    if any(keyword in str(col).lower() for keyword in ['asset', 'credit', 'cr.']):
                        split_col_index = i
                        break
                
                if split_col_index <= 0:
                    print(f"Could not determine T-account split for sheet '{sheet_name}'. Skipping.")
                    continue

                # Process Left Side (Liabilities/Debits)
                left_df = df.iloc[:, :split_col_index]
                left_header = str(left_df.columns[0])
                if len(left_df.columns) > 1:
                    left_particulars = left_df.iloc[:, 0]
                    left_amounts_cy = clean_numeric(left_df.iloc[:, 1])
                    for i, particular in enumerate(left_particulars):
                        if pd.notna(particular) and str(particular).strip():
                            all_data_rows.append({'Particulars': f"{left_header}|{str(particular).strip()}", 'Amount_CY': left_amounts_cy[i], 'Amount_PY': 0})
                
                # Process Right Side (Assets/Credits)
                right_df = df.iloc[:, split_col_index:]
                right_header = str(right_df.columns[0])
                if len(right_df.columns) > 1:
                    right_particulars = right_df.iloc[:, 0]
                    right_amounts_cy = clean_numeric(right_df.iloc[:, 1])
                    for i, particular in enumerate(right_particulars):
                         if pd.notna(particular) and str(particular).strip():
                            all_data_rows.append({'Particulars': f"{right_header}|{str(particular).strip()}", 'Amount_CY': right_amounts_cy[i], 'Amount_PY': 0})
            
            else: # Process Vertical Format
                # Find columns more robustly
                particulars_col = next((col for col in df.columns if 'particular' in str(col).lower()), None)
                cy_col = next((col for col in df.columns if 'cy' in str(col).lower() or 'current' in str(col).lower()), df.columns[1])
                py_col = next((col for col in df.columns if 'py' in str(col).lower() or 'previous' in str(col).lower()), None)

                if not particulars_col:
                    print(f"Could not identify Particulars column in sheet '{sheet_name}'. Skipping.")
                    continue
                
                # Apply robust cleaning to amount columns
                df[cy_col] = clean_numeric(df[cy_col])
                if py_col: df[py_col] = clean_numeric(df[py_col])

                current_header = ""
                for _, row in df.iterrows():
                    particular = str(row[particulars_col]).strip()
                    is_header = row[cy_col] == 0 and 'total' not in particular.lower()

                    if is_header:
                        current_header = particular
                        continue
                    
                    if not particular or 'total' in particular.lower():
                        continue

                    contextual_key = f"{current_header}|{particular}" if current_header else particular
                    all_data_rows.append({'Particulars': contextual_key, 'Amount_CY': row[cy_col], 'Amount_PY': row.get(py_col, 0)})

        if not all_data_rows:
            st.error("Data Intake Failed: The agent could not find any recognizable financial data. Please check the file format and ensure it contains standard financial terms.")
            return None

        final_df = pd.DataFrame(all_data_rows).fillna(0)
        print(f"✅ Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows.")
        return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with a critical exception: {e}")
        st.error(f"A critical error occurred during file intake: {e}")
        return None
