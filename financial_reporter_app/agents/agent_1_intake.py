# ==============================================================================
# agents/agent_1_intake.py
# AGENT 1: Data intake and initial cleaning.
# ==============================================================================
import pandas as pd
from io import BytesIO

def intelligent_data_intake_agent(uploaded_file):
    """
    AGENT 1: Reads and cleans an uploaded financial data Excel file.
    It intelligently detects the correct header row.
    """
    print("\n--- Agent 1 (Data Intake): Starting data ingestion... ---")
    try:
        # Read the file into a BytesIO buffer to handle different file types
        excel_data = BytesIO(uploaded_file.read())
        
        # Read the first 10 rows to find the header
        temp_df = pd.read_excel(excel_data, header=None, nrows=10)
        
        # Find the row containing 'Particulars' (case-insensitive) to use as the header
        header_row_index = temp_df[temp_df.apply(lambda row: row.astype(str).str.contains('Particulars', case=False).any(), axis=1)].index
        
        if not header_row_index.empty:
            header_index_to_use = header_row_index[0]
            # Read the full file again with the correct header
            source_df = pd.read_excel(excel_data, header=header_index_to_use)
            
            # Standardize column names
            source_df.rename(columns={
                'Particulars': 'Particulars',
                'As at March 31, 2025': 'Amount_CY',
                'As at March 31, 2024': 'Amount_PY',
                'Amount': 'Amount_CY' # Handle cases where only a single column is present
            }, inplace=True)
            
            # Drop rows where 'Particulars' is null or a blank space
            source_df = source_df.dropna(subset=['Particulars'])
            
            # Ensure Amount columns are numeric, filling non-numeric values with 0
            for col in ['Amount_CY', 'Amount_PY']:
                if col in source_df.columns:
                    source_df[col] = pd.to_numeric(source_df[col], errors='coerce').fillna(0)
            
            print("✅ Data Intake SUCCESS: File read and cleaned.")
            return source_df
        else:
            print("❌ Data Intake FAILED: Could not find 'Particulars' header.")
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ Data Intake FAILED: An unexpected error occurred: {e}")
        return pd.DataFrame()
