# ==============================================================================
# FILE: agents/agent_1_intake.py (DEFINITIVE, MODIFIED FOR PY-AWARENESS)
# This version is required to work with the master config.py file.
# ==============================================================================
import pandas as pd
import io # Imported for type hinting if needed, good practice

def intelligent_data_intake_agent(file_object):
    """
    AGENT 1: Reads Excel, intelligently finds financial data sections, creates
    contextual keys, AND NOW ALSO RETURNS A FLAG INDICATING IF PREVIOUS YEAR
    DATA WAS FOUND.
    """
    print("\n--- Agent 1 (Data Intake): Reading, parsing, and adding context... ---")
    try:
        xls = pd.ExcelFile(file_object)
        all_contextual_rows = []
        
        # ================== CHANGE 1: ADD A FLAG ==================
        # This new variable will track if we find a valid PY column anywhere in the file.
        # It starts as False.
        found_py_column = False
        # ==========================================================

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            for i in range(df.shape[1] - 1):
                col1, col2 = df.iloc[:, i], df.iloc[:, i + 1]
                is_text_col = col1.apply(lambda x: isinstance(x, str)).sum() > 5
                is_num_col = pd.to_numeric(col2, errors='coerce').notna().sum() > 3

                if is_text_col and is_num_col:
                    temp_df = None
                    
                    if df.shape[1] > i + 2 and pd.to_numeric(df.iloc[:, i + 2], errors='coerce').notna().sum() > 3:
                        # ================== CHANGE 2: UPDATE THE FLAG ==================
                        # If we find a valid third numeric column, we set our flag to True.
                        found_py_column = True
                        # ===============================================================
                        temp_df = df.iloc[:, [i, i + 1, i + 2]].copy()
                        temp_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                    else:
                        temp_df = df.iloc[:, [i, i + 1]].copy()
                        temp_df.columns = ['Particulars', 'Amount_CY']
                        temp_df['Amount_PY'] = 0
                    
                    temp_df.dropna(subset=['Particulars'], inplace=True)
                    temp_df['Amount_CY'] = pd.to_numeric(temp_df['Amount_CY'], errors='coerce')
                    temp_df['Amount_PY'] = pd.to_numeric(temp_df['Amount_PY'], errors='coerce')

                    current_header = ""
                    for _, row in temp_df.iterrows():
                        particular = str(row['Particulars']).strip()
                        
                        # A row is a header if it has text but NO numbers. This is the key logic.
                        is_header = pd.isna(row['Amount_CY']) and (pd.isna(row['Amount_PY']) if found_py_column else True)

                        if is_header and 'total' not in particular.lower():
                            current_header = particular
                            continue
                        
                        if not particular or 'total' in particular.lower():
                            continue

                        contextual_key = f"{current_header}|{particular}" if current_header else particular
                        all_contextual_rows.append({
                            'Particulars': contextual_key,
                            'Amount_CY': row['Amount_CY'] if pd.notna(row['Amount_CY']) else 0,
                            'Amount_PY': row['Amount_PY'] if found_py_column and pd.notna(row['Amount_PY']) else 0
                        })
        
        if not all_contextual_rows:
            print("❌ Intake FAILED: Could not extract any valid contextual data.")
            # ================== CHANGE 3: UPDATE RETURN VALUE ON FAILURE ==================
            return None, False
            # ==============================================================================

        final_df = pd.DataFrame(all_contextual_rows).drop_duplicates()
        print(f"✅ Intake SUCCESS: Extracted {len(final_df)} rows. PY Data Found: {found_py_column}")
        
        # ================== CHANGE 4: UPDATE RETURN VALUE ON SUCCESS ==================
        # The function now returns TWO values: the dataframe and the boolean flag.
        return final_df, found_py_column
        # ============================================================================

    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e}")
        # ================== CHANGE 5: UPDATE RETURN VALUE ON EXCEPTION ==================
        return None, False
        # ==============================================================================
