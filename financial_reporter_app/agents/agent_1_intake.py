# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: agent_1_intake.py
# ==============================================================================
import pandas as pd
import streamlit as st

def intelligent_data_intake_agent(uploaded_file):
    """
    AGENT 1: Ingests the uploaded Excel file with robust header detection
    and column renaming to prevent KeyErrors.
    """
    print("\n--- Agent 1 (Data Intake): Ingesting file... ---")
    if uploaded_file is None:
        return None

    try:
        # First, read the file without a header to inspect it
        df_no_header = pd.read_excel(uploaded_file, header=None)

        # Find the row that contains 'Particulars' (case-insensitive)
        header_row_index = -1
        for i, row in df_no_header.iterrows():
            # Check if any cell in the row contains the string 'particulars'
            if any('particulars' in str(cell).lower() for cell in row.values):
                header_row_index = i
                break

        if header_row_index == -1:
            st.error("Data Intake Error: Could not find a header row containing the word 'Particulars' in the uploaded file.")
            return None

        # Now, read the Excel file again, using the correct row as the header
        df = pd.read_excel(uploaded_file, header=header_row_index)

        # --- THIS IS THE PERMANENT FIX FOR THE KEYERROR ---
        # Clean up column names by stripping whitespace and converting to lower case
        df.columns = df.columns.str.strip().str.lower()
        
        # Find the actual column names by looking for keywords
        cols = df.columns
        particulars_col = [c for c in cols if 'particulars' in c][0]
        note_col = [c for c in cols if 'note' in c][0]
        
        # Find amount columns, which might be unnamed or have dates
        amount_cols = [c for c in cols if 'unnamed' in str(c) or 'as at' in str(c) or 'amount' in str(c)]
        
        if len(amount_cols) < 2:
            st.error("Data Intake Error: Could not identify at least two amount columns for Current and Previous Year.")
            return None

        cy_col = amount_cols[0]
        py_col = amount_cols[1]
        
        # Select and rename the columns to a consistent standard
        df_renamed = df[[particulars_col, note_col, cy_col, py_col]].copy()
        df_renamed.columns = ['Particulars', 'Note', 'Amount_CY', 'Amount_PY']
        
        # Drop rows where 'Particulars' is completely empty, which often represent spacer rows
        df_cleaned = df_renamed.dropna(subset=['Particulars'])
        
        print("✅ Data Intake SUCCESS: File ingested, header found, and columns standardized.")
        return df_cleaned

    except Exception as e:
        st.error(f"Data Intake FAILED: An unexpected error occurred. Please ensure the Excel file contains columns for 'Particulars', 'Note', and two amount columns. Error: {e}")
        import traceback
        traceback.print_exc()
        return None
