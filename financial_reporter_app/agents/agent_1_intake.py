# ==============================================================================
# FILE: agents/agent_1_intake.py (DEFINITIVE UPDATE)
# ==============================================================================
import pandas as pd

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, finds financial data, and creates unique, contextual
    keys for each data row (e.g., "Header|Particular").
    """
    print("\n--- Agent 1 (Data Intake): Reading, parsing, and adding context... ---")
    try:
        xls = pd.ExcelFile(file_object)
        source_df = None
        # Find the first sheet that looks like it contains financial notes
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            for i in range(df.shape[1] - 1): # Check for at least 2 columns
                col1, col2 = df.iloc[:, i], df.iloc[:, i + 1]
                # Heuristics to find the right columns
                is_text_col = col1.apply(lambda x: isinstance(x, str)).sum() > 5
                is_num_col = pd.to_numeric(col2, errors='coerce').notna().sum() > 3
                if is_text_col and is_num_col:
                    # Check if a third column exists for PY data
                    if df.shape[1] > i + 2 and pd.to_numeric(df.iloc[:, i + 2], errors='coerce').notna().sum() > 3:
                        source_df = df.iloc[:, [i, i + 1, i + 2]].copy()
                        source_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                    else: # Handle cases with only one amount column
                        source_df = df.iloc[:, [i, i + 1]].copy()
                        source_df.columns = ['Particulars', 'Amount_CY']
                        source_df['Amount_PY'] = 0
                    source_df.dropna(subset=['Particulars'], inplace=True)
                    break
            if source_df is not None:
                break

        if source_df is None:
            print("❌ Intake FAILED: Could not find valid [Text, Number] columns.")
            return None

        # Convert amount columns to numeric, filling errors with NaN
        source_df['Amount_CY'] = pd.to_numeric(source_df['Amount_CY'], errors='coerce')
        source_df['Amount_PY'] = pd.to_numeric(source_df['Amount_PY'], errors='coerce')

        contextual_rows = []
        current_header = ""
        for _, row in source_df.iterrows():
            particular = str(row['Particulars']).strip()
            # A row is a header if it has text but NO numbers for CY or PY.
            is_header = pd.isna(row['Amount_CY']) and pd.isna(row['Amount_PY'])

            if is_header and 'total' not in particular.lower():
                current_header = particular
                continue # Skip to next row after identifying a header

            # Skip blank rows or rows that are just totals
            if 'total' in particular.lower() or not particular:
                continue

            # Create a unique key using the last known header.
            # This is the key that will be looked up by Agent 3.
            contextual_key = f"{current_header}|{particular}" if current_header else particular

            contextual_rows.append({
                'Particulars': contextual_key,
                'Amount_CY': row['Amount_CY'] if pd.notna(row['Amount_CY']) else 0,
                'Amount_PY': row['Amount_PY'] if pd.notna(row['Amount_PY']) else 0
            })

        final_df = pd.DataFrame(contextual_rows)
        print(f"✅ Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows.")
        return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e}")
        return None
