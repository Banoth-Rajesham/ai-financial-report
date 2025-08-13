# ==============================================================================
# FILE: agents/agent_1_intake.py (UPDATED)
# ==============================================================================
import pandas as pd
import numpy as np

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, finds financial data, and enriches it with hierarchical context.
    This updated version creates unique particulars based on section headers.
    """
    print("\n--- Agent 1 (Data Intake): Reading, parsing, and adding context... ---")
    try:
        # --- Step 1: Find the most likely sheet and data columns ---
        xls = pd.ExcelFile(file_object)
        source_df = None
        for sheet_name in xls.sheet_names:
            # Heuristic: Financial notes are often in sheets named 'Note' or 'Schedule'
            if "note" in sheet_name.lower() or "schedule" in sheet_name.lower():
                df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                for i in range(df.shape[1] - 2):
                    col1, col2, col3 = df.iloc[:, i], df.iloc[:, i + 1], df.iloc[:, i+2]
                    # Check if we found a valid [Text, Number, Number] triplet
                    is_text_col = col1.apply(lambda x: isinstance(x, str)).sum() > 5
                    is_num_col1 = pd.to_numeric(col2, errors='coerce').notna().sum() > 3
                    if is_text_col and is_num_col1:
                        source_df = df.iloc[:, [i, i + 1, i + 2]].copy()
                        source_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                        source_df.dropna(subset=['Particulars'], inplace=True)
                        break
            if source_df is not None:
                break

        if source_df is None:
            print("❌ Intake FAILED: Could not find any valid data columns in the Excel file.")
            return None

        # --- Step 2: Process the data to add context ---
        contextual_rows = []
        current_header = ""
        source_df['Amount_CY'] = pd.to_numeric(source_df['Amount_CY'], errors='coerce')
        source_df['Amount_PY'] = pd.to_numeric(source_df['Amount_PY'], errors='coerce')

        for index, row in source_df.iterrows():
            particular = str(row['Particulars']).strip()
            # A row is considered a header if it has text but no numeric data.
            is_header = pd.isna(row['Amount_CY']) and pd.isna(row['Amount_PY'])

            if is_header and 'total' not in particular.lower():
                current_header = particular
                continue  # Move to the next row after identifying a header

            # For data rows, create a contextual key if a header is active
            if current_header:
                # This creates keys like: "Authorised share capital|Number of shares"
                contextual_particular = f"{current_header}|{particular}"
            else:
                contextual_particular = particular # Use the original if no header context

            contextual_rows.append({
                # We replace 'Particulars' with our new unique key
                'Particulars': contextual_particular,
                'Amount_CY': row['Amount_CY'] if not pd.isna(row['Amount_CY']) else 0,
                'Amount_PY': row['Amount_PY'] if not pd.isna(row['Amount_PY']) else 0
            })
            
        final_df = pd.DataFrame(contextual_rows)
        print(f"✅ Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows.")
        return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e}")
        return None
