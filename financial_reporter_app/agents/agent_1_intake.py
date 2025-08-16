# ==============================================================================
# FILE: agents/agent_1_intake.py (CORRECTED)
# ==============================================================================
import pandas as pd

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, finds financial data, and extracts the raw
    particulars and amounts without creating contextual keys.
    """
    print("\n--- Agent 1 (Data Intake): Reading and parsing Excel file... ---")
    try:
        xls = pd.ExcelFile(file_object)
        all_data = []

        # Iterate through all sheets to find relevant data
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            # Search for the pattern [Text, Number, Number] or [Text, Number]
            for i in range(df.shape[1] - 1):
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
                        source_df['Amount_PY'] = 0 # Add a PY column with zeros

                    source_df.dropna(subset=['Particulars'], inplace=True)
                    all_data.append(source_df)
                    break # Move to the next sheet after finding a match

        if not all_data:
            print("❌ Intake FAILED: Could not find any valid [Text, Number] columns in any sheet.")
            return None

        # Combine all found dataframes and clean up
        final_df = pd.concat(all_data, ignore_index=True)
        final_df['Amount_CY'] = pd.to_numeric(final_df['Amount_CY'], errors='coerce').fillna(0)
        final_df['Amount_PY'] = pd.to_numeric(final_df['Amount_PY'], errors='coerce').fillna(0)

        # Remove total rows to avoid double counting
        final_df = final_df[~final_df['Particulars'].str.strip().str.lower().str.contains('total', na=False)]

        print(f"✅ Intake SUCCESS: Extracted {len(final_df)} data rows from the document.")
        return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e}")
        return None
