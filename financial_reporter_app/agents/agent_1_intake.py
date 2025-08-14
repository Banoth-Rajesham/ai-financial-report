# ==============================================================================
# FILE: agents/agent_1_intake.py (FINAL, ROBUST VERSION)
# ==============================================================================
import pandas as pd
import re

def clean_numeric(series):
    """A robust function to clean and convert a column to numbers."""
    if series is None: return pd.Series(dtype='float64')
    series_str = series.astype(str)
    series_str = series_str.str.replace(r'[₹,]', '', regex=True)
    series_str = series_str.str.strip()
    series_str = series_str.str.replace(r'^\s*\((.*)\)\s*$', r'-\1', regex=True)
    return pd.to_numeric(series_str, errors='coerce').fillna(0)

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, robustly detects T-account or vertical format,
    transforms T-accounts, and creates unique, contextual keys for each data row.
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
            
            if header_row_index == -1:
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

            if is_t_format:
                split_col_index = -1
                for i, col in enumerate(df.columns):
                    if any(keyword in str(col).lower() for keyword in ['asset', 'credit', 'cr.']):
                        split_col_index = i
                        break
                
                if split_col_index <= 0:
                    print(f"Could not determine T-account split for sheet '{sheet_name}'. Skipping.")
                    continue

                left_df = df.iloc[:, :split_col_index]
                left_header = str(left_df.columns[0])
                if len(left_df.columns) > 1:
                    left_particulars = left_df.iloc[:, 0]
                    left_amounts = clean_numeric(left_df.iloc[:, 1])
                    for i, p in enumerate(left_particulars):
                        if pd.notna(p) and str(p).strip() and 'total' not in str(p).lower():
                            all_data_rows.append({'Particulars': f"{left_header}|{str(p).strip()}", 'Amount_CY': left_amounts[i], 'Amount_PY': 0})
                
                right_df = df.iloc[:, split_col_index:]
                right_header = str(right_df.columns[0])
                if len(right_df.columns) > 1:
                    right_particulars = right_df.iloc[:, 0]
                    right_amounts = clean_numeric(right_df.iloc[:, 1])
                    for i, p in enumerate(right_particulars):
                         if pd.notna(p) and str(p).strip() and 'total' not in str(p).lower():
                            all_data_rows.append({'Particulars': f"{right_header}|{str(p).strip()}", 'Amount_CY': right_amounts[i], 'Amount_PY': 0})
            
            else: # Process Vertical Format
                p_col = next((c for c in df.columns if 'particular' in str(c).lower()), None)
                cy_col = next((c for c in df.columns if 'cy' in str(c).lower() or 'current' in str(c).lower()), df.columns[1])
                py_col = next((c for c in df.columns if 'py' in str(c).lower() or 'previous' in str(c).lower()), None)

                if not p_col:
                    print(f"Could not identify Particulars column in '{sheet_name}'. Skipping.")
                    continue
                
                df[cy_col] = clean_numeric(df[cy_col])
                if py_col: df[py_col] = clean_numeric(df[py_col])

                current_header = ""
                for _, row in df.iterrows():
                    particular = str(row[p_col]).strip()
                    is_header = row[cy_col] == 0 and 'total' not in particular.lower()

                    if is_header and particular: current_header = particular
                    elif not particular or 'total' in particular.lower(): continue
                    else:
                        key = f"{current_header}|{particular}" if current_header else particular
                        all_data_rows.append({'Particulars': key, 'Amount_CY': row[cy_col], 'Amount_PY': row.get(py_col, 0)})

        if not all_data_rows:
            print("❌ Intake FAILED: No valid data rows could be extracted.")
            # We return None, and app.py will handle showing the error to the user.
            return None

        final_df = pd.DataFrame(all_data_rows).fillna(0)
        print(f"✅ Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows.")
        return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with a critical exception: {e}")
        # We return None, and app.py will handle showing the error to the user.
        return None
