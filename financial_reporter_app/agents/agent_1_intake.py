# ==============================================================================
# FILE: agents/agent_1_intake.py (DEFINITIVE, WITH PY DATA DETECTION)
# ==============================================================================
import pandas as pd

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, creates contextual keys, AND detects if Previous Year
    data is missing to ensure full Schedule III compliance.
    """
    print("\n--- Agent 1 (Data Intake): Reading, parsing, and adding context... ---")
    try:
        xls = pd.ExcelFile(file_object)
        all_contextual_rows = []
        py_column_found = False # Flag to track if we find a PY column

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            for i in range(df.shape[1] - 1):
                col1, col2 = df.iloc[:, i], df.iloc[:, i + 1]
                is_text_col = col1.apply(lambda x: isinstance(x, str)).sum() > 5
                is_num_col = pd.to_numeric(col2, errors='coerce').notna().sum() > 3

                if is_text_col and is_num_col:
                    temp_df = None
                    if df.shape[1] > i + 2 and pd.to_numeric(df.iloc[:, i + 2], errors='coerce').notna().sum() > 3:
                        temp_df = df.iloc[:, [i, i + 1, i + 2]].copy()
                        temp_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                        py_column_found = True # We found a PY column!
                    else:
                        temp_df = df.iloc[:, [i, i + 1]].copy()
                        temp_df.columns = ['Particulars', 'Amount_CY']
                        temp_df['Amount_PY'] = 0
                    
                    temp_df.dropna(subset=['Particulars'], inplace=True)
                    temp_df['Amount_CY'] = pd.to_numeric(temp_df['Amount_CY'], errors='coerce')
                    temp_df['Amount_PY'] = pd.to_numeric(temp_df['Amount_PY'], errors='coerce')

                    current_header = ""
                    for _, row in temp_df.iterrows():
                        particular = str(row['Particulars']).strip()
                        is_header = pd.isna(row['Amount_CY']) and pd.isna(row['Amount_PY'])
                        if is_header and 'total' not in particular.lower():
                            current_header = particular
                            continue
                        if not particular or 'total' in particular.lower():
                            continue
                        contextual_key = f"{current_header}|{particular}" if current_header else particular
                        all_contextual_rows.append({
                            'Particulars': contextual_key,
                            'Amount_CY': row['Amount_CY'] if pd.notna(row['Amount_CY']) else 0,
                            'Amount_PY': row['Amount_PY'] if pd.notna(row['Amount_PY']) else 0
                        })
        
        if not all_contextual_rows:
            print("❌ Intake FAILED: Could not extract any valid contextual data.")
            return None, None

        final_df = pd.DataFrame(all_contextual_rows).drop_duplicates()
        
        # --- NEW: Generate the warning if no PY column was ever found ---
        intake_warning = None
        if not py_column_found:
            intake_warning = "⚠️ **Previous Year's data not found.** For full Schedule III compliance and accurate comparisons, please upload an Excel file that includes columns for both the current and previous year."
            print(intake_warning)

        print(f"✅ Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows.")
        return final_df, intake_warning

    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e}")
        return None, None
