# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: agent_1_intake.py
# ==============================================================================
import pandas as pd
import streamlit as st
import openpyxl # Use a more powerful library for scanning

def intelligent_data_intake_agent(uploaded_file):
    """
    AGENT 1: Ingests the uploaded Excel file with a highly robust method for
    finding the header row and standardizing columns to prevent KeyErrors.
    This version uses openpyxl to be immune to merged cells and formatting.
    """
    print("\n--- Agent 1 (Data Intake): Ingesting file... ---")
    if uploaded_file is None:
        return None

    try:
        # --- THIS IS THE PERMANENT FIX ---
        # Use openpyxl to scan the raw structure of the sheet cell by cell

        workbook = openpyxl.load_workbook(uploaded_file, read_only=True)
        sheet = workbook.active

        header_row_idx = -1
        particulars_col_idx = -1

        # Scan the first 30 rows to find the exact cell with 'Particulars'
        for r_idx in range(1, 31):
            for c_idx in range(1, 21):
                cell = sheet.cell(row=r_idx, column=c_idx)
                if cell.value and isinstance(cell.value, str) and 'particulars' in cell.value.lower():
                    # openpyxl is 1-indexed, pandas header is 0-indexed
                    header_row_idx = r_idx - 1
                    particulars_col_idx = c_idx - 1
                    break
            if header_row_idx != -1:
                break
        # --- END OF SCANNING LOGIC ---

        if header_row_idx == -1:
            st.error("Data Intake Error: Could not find a cell containing the word 'Particulars' within the first 30 rows of the uploaded file. Please check the file.")
            return None

        # Now that we know the exact header row, read the file with pandas
        # We need to reset the file pointer to read it again
        uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file, header=header_row_idx)

        # Get the actual column name from the found index
        original_cols = df.columns
        particulars_col_name = original_cols[particulars_col_idx]
        
        # The next three columns are assumed to be Note, CY, PY
        if len(original_cols) < particulars_col_idx + 4:
             st.error("Data Intake Error: The file appears to be missing the Note and/or Amount columns after the 'Particulars' column.")
             return None
             
        note_col_name = original_cols[particulars_col_idx + 1]
        cy_col_name = original_cols[particulars_col_idx + 2]
        py_col_name = original_cols[particulars_col_idx + 3]

        # Create a new, clean DataFrame with standard names
        df_clean = df[[particulars_col_name, note_col_name, cy_col_name, py_col_name]].copy()
        df_clean.columns = ['Particulars', 'Note', 'Amount_CY', 'Amount_PY']

        # Drop rows where 'Particulars' is completely empty or is the header again
        df_clean = df_clean.dropna(subset=['Particulars'])
        df_clean = df_clean[df_clean['Particulars'].astype(str).str.lower() != 'particulars']
        
        print("✅ Data Intake SUCCESS: File ingested, header found, and columns standardized.")
        return df_clean

    except Exception as e:
        st.error(f"Data Intake FAILED: An unexpected error occurred. Please ensure the Excel file is not corrupted and is in a standard format. Error: {e}")
        import traceback
        traceback.print_exc()
        return None
