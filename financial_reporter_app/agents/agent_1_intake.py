# ==============================================================================
# PASTE THIS ENTIRE BLOCK INTO: agents/agent_1_intake.py
# ==============================================================================
import pandas as pd
import streamlit as st

def intelligent_data_intake_agent(uploaded_file):
    """
    AGENT 1 (UPGRADED): Intelligently ingests financial statements,
    handling both single-column (Schedule III) and two-sided (T-Account) formats.
    """
    print("\n--- Agent 1 (Data Intake): Ingesting file... ---")
    if uploaded_file is None:
        return None

    try:
        xls = pd.ExcelFile(uploaded_file)
        
        # --- Attempt to read as a T-Account format first ---
        df_bs = df_pl = None
        sheet_names_lower = [name.lower() for name in xls.sheet_names]
        if 'balance sheet' in sheet_names_lower:
            df_bs = pd.read_excel(xls, sheet_name=xls.sheet_names[sheet_names_lower.index('balance sheet')], header=None)
        if 'profit & loss account' in sheet_names_lower:
            df_pl = pd.read_excel(xls, sheet_name=xls.sheet_names[sheet_names_lower.index('profit & loss account')], header=None)
        
        # Consolidate T-account data if found
        all_data = []
        if df_bs is not None:
            # ... (logic to parse T-account Balance Sheet) ...
            header_row_index = -1; asset_col_index = -1
            for i, row in df_bs.iterrows():
                row_str = row.to_string().upper()
                if 'LIABILITIES' in row_str and 'ASSETS' in row_str:
                    header_row_index = i
                    for j, cell in enumerate(row):
                        if isinstance(cell, str) and 'ASSETS' in cell.upper(): asset_col_index = j; break
                    break
            if header_row_index != -1 and asset_col_index != -1:
                df_liab = df_bs.iloc[header_row_index + 1:, :asset_col_index]; df_assets = df_bs.iloc[header_row_index + 1:, asset_col_index:]
                df_liab.columns = ['Particulars', 'Amount_CY', 'Amount_PY'][:len(df_liab.columns)]; df_assets.columns = ['Particulars', 'Amount_CY', 'Amount_PY'][:len(df_assets.columns)]
                all_data.extend([df_liab, df_assets])
        
        if df_pl is not None:
            # ... (logic to parse T-account Profit & Loss) ...
            header_row_index = -1; credit_col_index = -1
            for i, row in df_pl.iterrows():
                row_str = row.to_string().upper()
                if 'DR' in row_str and 'CR' in row_str:
                    header_row_index = i
                    for j, cell in enumerate(row):
                        if isinstance(cell, str) and 'CR' in cell.upper(): credit_col_index = j; break
                    break
            if header_row_index != -1 and credit_col_index != -1:
                data_start_row = next((i + 1 for i in range(header_row_index, len(df_pl)) if 'PARTICULARS' in df_pl.iloc[i].to_string().upper()), -1)
                if data_start_row != -1:
                    df_debit = df_pl.iloc[data_start_row:, :credit_col_index]; df_credit = df_pl.iloc[data_start_row:, credit_col_index:]
                    df_debit.columns = ['Particulars', 'Amount_CY', 'Amount_PY'][:len(df_debit.columns)]; df_credit.columns = ['Particulars', 'Amount_CY', 'Amount_PY'][:len(df_credit.columns)]
                    all_data.extend([df_debit, df_credit])

        if all_data:
            print("  -> Detected T-Account format. Consolidating data.")
            final_df = pd.concat(all_data, ignore_index=True)
        else:
            # --- Fallback to reading as a single-column Schedule III format ---
            print("  -> T-Account format not detected. Attempting to read as Schedule III format.")
            df = pd.read_excel(xls, sheet_name=0) # Read the first sheet
            # Basic cleaning for Schedule III format
            if 'Particulars' not in df.columns:
                st.error("Data Intake FAILED: The file is not a recognized T-Account format and is missing a 'Particulars' column for Schedule III format.")
                return None
            df.rename(columns={df.columns[2]: 'Amount_CY', df.columns[3]: 'Amount_PY'}, inplace=True)
            final_df = df

        # --- Final Cleaning for all formats ---
        final_df.dropna(subset=['Particulars'], inplace=True)
        final_df = final_df[~final_df['Particulars'].astype(str).str.contains('Total|TOTAL', case=False, na=False)]
        final_df = final_df[final_df['Particulars'].astype(str).str.strip() != '']
        
        print(f"✅ Data Intake SUCCESS: Consolidated {len(final_df)} line items.")
        return final_df

    except Exception as e:
        st.error(f"Data Intake FAILED: An unexpected error occurred. Please check the Excel file. Error: {e}")
        return None
