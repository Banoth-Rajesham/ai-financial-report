# ==============================================================================
# FILE: agents/agent_1_intake.py (CORRECTED TO SUPPORT DETAILED CONFIG)
# ==============================================================================
import pandas as pd

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads all sheets in an Excel file to find and extract all possible
    financial data rows in a [Text, Number, Number] format. It extracts the
    text as-is to allow the detailed mapping config to work correctly.
    """
    print("\n--- Agent 1 (Data Intake): Reading and parsing all sheets for raw data... ---")
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
                    temp_df = None
                    # Check if a third column exists for PY data
                    if df.shape[1] > i + 2 and pd.to_numeric(df.iloc[:, i + 2], errors='coerce').notna().sum() > 3:
                        temp_df = df.iloc[:, [i, i + 1, i + 2]].copy()
                        temp_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                    else: # Handle cases with only one amount column
                        temp_df = df.iloc[:, [i, i + 1]].copy()
                        temp_df.columns = ['Particulars', 'Amount_CY']
                        temp_df['Amount_PY'] = 0 # Add a PY column with zeros

                    temp_df.dropna(subset=['Particulars'], inplace=True)
                    all_data.append(temp_df)
                    # We don't break here, to allow finding data in multiple column sets per sheet

        if not all_data:
            print("❌ Intake FAILED: Could not find any valid [Text, Number] columns in any sheet.")
            return None

        # Combine all found dataframes and clean up
        final_df = pd.concat(all_data, ignore_index=True).drop_duplicates()
        final_df['Amount_CY'] = pd.to_numeric(final_df['Amount_CY'], errors='coerce').fillna(0)
        final_df['Amount_PY'] = pd.to_numeric(final_df['Amount_PY'], errors='coerce').fillna(0)

        print(f"✅ Intake SUCCESS: Extracted {len(final_df)} raw data rows from the document.")
        return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e}")
        return None
