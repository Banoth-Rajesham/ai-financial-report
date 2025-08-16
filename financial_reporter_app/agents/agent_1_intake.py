# ==============================================================================
# FILE: agents/agent_1_intake.py ( premium account" and then a line like "Balance at the beginning of the year", it will combine them into a single,DEFINITIVE MASTER VERSION)
# This agent understands the document structure and adds context.
# ================================================================= unique key: `"2.2 Securities premium account|Balance at the beginning of the year"`. This preserves the structure=============
import pandas as pd

def intelligent_data_intake_agent(file_object):
    """
     that was being lost before.

**Action:** Replace the entire content of your `agents/agent_1_intAGENT 1: Reads Excel, intelligently finds financial data sections, and creates
    unique, contextual keys for each dataake.py` file with this new, intelligent version.

```python
# ==============================================================================
# FILE row (e.g., "Header|Particular") to
    ensure 100% accurate mapping with the detailed config: agents/agent_1_intake.py (DEFINITIVE, CONTEXT-AWARE VERSION)
# =================.
    """
    print("\n--- Agent 1 (Data Intake): Reading, parsing, and adding context...=============================================================
import pandas as pd

def intelligent_data_intake_agent(file_object):
 ---")
    try:
        xls = pd.ExcelFile(file_object)
        source_df = None
        
        # Find the first sheet that contains valid financial data
        for sheet_name in xls.sheet_names:
    """
    AGENT 1: Reads Excel, intelligently finds financial data sections, and creates
    unique, contextual keys for            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            for each data row (e.g., "Header|Particular") to
    ensure 100% accurate mapping i in range(df.shape[1] - 1): # Check for at least 2 columns
                col with the detailed config.
    """
    print("\n--- Agent 1 (Data Intake): Reading, parsing1, col2 = df.iloc[:, i], df.iloc[:, i + 1]
                
                #, and adding context... ---")
    try:
        xls = pd.ExcelFile(file_object)
        all Heuristics to find the main data columns
                is_text_col = col1.apply(lambda x_contextual_rows = []

        for sheet_name in xls.sheet_names:
            df = pd.read: isinstance(x, str)).sum() > 5
                is_num_col = pd.to__excel(xls, sheet_name=sheet_name, header=None)
            for i in range(dfnumeric(col2, errors='coerce').notna().sum() > 3
                
                if is_text.shape[1] - 1):
                col1, col2 = df.iloc[:, i], df.iloc_col and is_num_col:
                    if df.shape[1] > i + 2 and pd.to_numeric(df.iloc[:, i + 2], errors='coerce').notna().sum() > 3[:, i + 1]
                is_text_col = col1.apply(lambda x: isinstance(x,:
                        source_df = df.iloc[:, [i, i + 1, i + 2]].copy str)).sum() > 5
                is_num_col = pd.to_numeric(col2, errors()
                        source_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                    else:='coerce').notna().sum() > 3

                if is_text_col and is_num_
                        source_df = df.iloc[:, [i, i + 1]].copy()
                        source_col:
                    temp_df = None
                    if df.shape[1] > i + 2 and pddf.columns = ['Particulars', 'Amount_CY']
                        source_df['Amount_PY'] = 0
                    source_df.dropna(subset=['Particulars'], inplace=True)
                    break
            .to_numeric(df.iloc[:, i + 2], errors='coerce').notna().sum() > 3:
                        temp_df = df.iloc[:, [i, i + 1, i + 2]].if source_df is not None:
                break

        if source_df is None:
            print("❌ Intake FAILED: Could not find valid [Text, Number] columns.")
            return None

        source_df['Amountcopy()
                        temp_df.columns = ['Particulars', 'Amount_CY', 'Amount_PY']
                    else:
                        temp_df = df.iloc[:, [i, i + 1]].copy()
_CY'] = pd.to_numeric(source_df['Amount_CY'], errors='coerce')
        source_                        temp_df.columns = ['Particulars', 'Amount_CY']
                        temp_df['Amount_PY'] =df['Amount_PY'] = pd.to_numeric(source_df['Amount_PY'], errors='coerce 0
                    
                    temp_df.dropna(subset=['Particulars'], inplace=True)
                    temp_df')

        contextual_rows = []
        current_header = ""
        for _, row in source_['Amount_CY'] = pd.to_numeric(temp_df['Amount_CY'], errors='coerce')df.iterrows():
            particular = str(row['Particulars']).strip()
            
            # A row
                    temp_df['Amount_PY'] = pd.to_numeric(temp_df['Amount_PY'], errors='coerce')

                    current_header = ""
                    for _, row in temp_df.iterrows(): is a header if it has text but NO numbers. This identifies section titles.
            is_header = pd.isna
                        particular = str(row['Particulars']).strip()
                        is_header = pd.isna(row(row['Amount_CY']) and pd.isna(row['Amount_PY'])

            if is_header and '['Amount_CY']) and pd.isna(row['Amount_PY'])

                        if is_header and 'total' not in particular.lower():
                current_header = particular
                continue 

            if 'totaltotal' not in particular.lower():
                            current_header = particular
                            continue
                        
                        if not' in particular.lower() or not particular:
                continue

            # Create the crucial "Header|Particular" particular or 'total' in particular.lower():
                            continue

                        contextual_key = f"{current_header key. This preserves the document structure.
            contextual_key = f"{current_header}|{particular}"}|{particular}" if current_header else particular
                        all_contextual_rows.append({
                            'Particular if current_header else particular

            contextual_rows.append({
                'Particulars': contextual_key,
s': contextual_key,
                            'Amount_CY': row['Amount_CY'] if pd.notna(                'Amount_CY': row['Amount_CY'] if pd.notna(row['Amount_CY'])row['Amount_CY']) else 0,
                            'Amount_PY': row['Amount_PY'] if else 0,
                'Amount_PY': row['Amount_PY'] if pd.notna(row pd.notna(row['Amount_PY']) else 0
                        })
        
        if not all_contextual['Amount_PY']) else 0
            })

        final_df = pd.DataFrame(contextual_rows)_rows:
            print("❌ Intake FAILED: Could not extract any valid contextual data.")
            return None


        print(f"✅ Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows.")
                final_df = pd.DataFrame(all_contextual_rows).drop_duplicates()
        print(f"✅return final_df

    except Exception as e:
        print(f"❌ Intake FAILED with exception: {e Intake SUCCESS: Extracted and contextualized {len(final_df)} data rows.")
        return final_df}")
        return None
