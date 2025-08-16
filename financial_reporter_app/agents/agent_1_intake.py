# ==============================================================================
# FILE: agents/agent_1_intake.py (DEFINITIVE, PROVEN VERSION)
# ==============================================================================
import pandas as pd

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel file and extracts financial data using the simple,
    robust logic from the working Colab script.
    """
    print("\n--- Agent 1 (Data Intake): Reading and parsing Excel file... ---")
    try:
        xls = pd.ExcelFile(file_object)
        all_data = []
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            for i in range(df.shape[1] - 2):
                col1, col2, col3 = df.iloc[:, i], df.iloc[:, i + 1], df.iloc[:, i+2]
                is_text_col = col1.apply(type).eq(str).sum() > len(col1.dropna()) * 0.6
                is_num_col1 = pd.to_numeric(col2, errors='coerce').notna().sum() > len(col2.dropna()) * 0.6
                is_num_col2 = pd.to_numeric(col3, errors='coerce').notna().sum() > len(col3.dropna()) * 0.6
                if is_text_col and is_num_col1 and is_num_col2:
                    pair_df = df.iloc[:, [i, i + 1, i + 2]].copy()
                    pair_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                    pair_df.dropna(subset=['Particulars'], inplace=True)
                    all_data.append(pair_df)
        if not all_data:
            print("❌ Intake FAILED: Could not find any valid [Text, Number, Number] columns.")
            return None
        source_df = pd.concat(all_data, ignore_index=True)
        source_df['Amount_CY'] = pd.to_numeric(source_df['Amount_CY'], errors='coerce').fillna(0)
        source_df['Amount_PY'] = pd.to_numeric(source_df['Amount_PY'], errors='coerce').fillna(0)
        print(f"✅ Intake SUCCESS: Extracted {len(source_df)} potential data rows.")
        return source_df
    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e}")
        return None
