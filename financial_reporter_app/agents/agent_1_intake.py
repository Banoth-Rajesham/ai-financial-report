# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: agents/agent_1_intake.py
# This is the specialized agent for reading T-account style reports.
# ==============================================================================
import pandas as pd
import streamlit as st

def intelligent_data_intake_agent(uploaded_file):
    """
    AGENT 1 (UPGRADED): Ingests complex, two-sided financial statements.
    It reads separate tables for Assets, Liabilities, Debits, and Credits
    and consolidates them into a single, standardized DataFrame.
    """
    print("\n--- Agent 1 (Data Intake): Attempting to ingest T-format report... ---")
    if uploaded_file is None:
        return None

    try:
        # Load the Excel file and try to find the relevant sheets
        xls = pd.ExcelFile(uploaded_file)
        df_bs = None
        df_pl = None

        sheet_names_lower = [name.lower() for name in xls.sheet_names]
        
        if 'balance sheet' in sheet_names_lower:
            bs_sheet_name = xls.sheet_names[sheet_names_lower.index('balance sheet')]
            df_bs = pd.read_excel(xls, sheet_name=bs_sheet_name, header=None)
        
        if 'profit & loss account' in sheet_names_lower:
            pl_sheet_name = xls.sheet_names[sheet_names_lower.index('profit & loss account')]
            df_pl = pd.read_excel(xls, sheet_name=pl_sheet_name, header=None)
        
        if df_bs is None and df_pl is None:
            # Fallback if sheets are not named as expected
            if len(xls.sheet_names) > 0: df_bs = pd.read_excel(xls, sheet_name=0, header=None)
            if len(xls.sheet_names) > 1: df_pl = pd.read_excel(xls, sheet_name=1, header=None)
            if df_bs is None and df_pl is None:
                st.error("Data Intake Error: Could not find any sheets to process in the Excel file.")
                return None

        all_data = []

        # --- Process Balance Sheet ---
        if df_bs is not None:
            # Find header by looking for 'LIABILITIES' and 'ASSETS'
            header_row_index = -1
            asset_col_index = -1
            for i, row in df_bs.iterrows():
                row_str = row.to_string().upper()
                if 'LIABILITIES' in row_str and 'ASSETS' in row_str:
                    header_row_index = i
                    # Find the starting column for ASSETS
                    for j, cell in enumerate(row):
                        if isinstance(cell, str) and 'ASSETS' in cell.upper():
                            asset_col_index = j
                            break
                    break
            
            if header_row_index != -1 and asset_col_index != -1:
                df_liabilities = df_bs.iloc[header_row_index + 1:, :asset_col_index].copy()
                df_assets = df_bs.iloc[header_row_index + 1:, asset_col_index:].copy()
                
                df_liabilities.columns = ['Particulars', 'Amount_CY', 'Amount_PY'][:len(df_liabilities.columns)]
                df_assets.columns = ['Particulars', 'Amount_CY', 'Amount_PY'][:len(df_assets.columns)]
                all_data.extend([df_liabilities, df_assets])

        # --- Process Profit & Loss Account ---
        if df_pl is not None:
            # Find header by looking for 'Dr' and 'Cr'
            header_row_index = -1
            credit_col_index = -1
            for i, row in df_pl.iterrows():
                row_str = row.to_string().upper()
                if 'DR' in row_str and 'CR' in row_str:
                    header_row_index = i
                    for j, cell in enumerate(row):
                        if isinstance(cell, str) and 'CR' in cell.upper():
                            credit_col_index = j
                            break
                    break

            if header_row_index != -1 and credit_col_index != -1:
                # Find the row where the actual data starts (the one after "Particulars")
                data_start_row = -1
                for i in range(header_row_index, len(df_pl)):
                    if 'PARTICULARS' in df_pl.iloc[i].to_string().upper():
                        data_start_row = i + 1
                        break

                if data_start_row != -1:
                    df_debit = df_pl.iloc[data_start_row:, :credit_col_index].copy()
                    df_credit = df_pl.iloc[data_start_row:, credit_col_index:].copy()

                    df_debit.columns = ['Particulars', 'Amount_CY', 'Amount_PY'][:len(df_debit.columns)]
                    df_credit.columns = ['Particulars', 'Amount_CY', 'Amount_PY'][:len(df_credit.columns)]
                    all_data.extend([df_debit, df_credit])

        if not all_data:
            st.error("Data Intake FAILED: Could not parse the T-account structure. Please ensure headers like 'LIABILITIES'/'ASSETS' and 'Dr'/'Cr' are present.")
            return None
            
        # --- Consolidate and Clean the final DataFrame ---
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.dropna(subset=['Particulars'], inplace=True)
        final_df = final_df[~final_df['Particulars'].astype(str).str.contains('Total|TOTAL', case=False, na=False)]
        final_df = final_df[final_df['Particulars'].astype(str).str.strip() != '']
        
        print(f"✅ Data Intake SUCCESS: Consolidated {len(final_df)} line items from the T-format report.")
        return final_df

    except Exception as e:
        st.error(f"Data Intake FAILED: An unexpected error occurred. Please check the Excel file. Error: {e}")
        import traceback
        traceback.print_exc()
        return None
