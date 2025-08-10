# ==============================================================================
# PASTE THIS ENTIRE BLOCK INTO: financial_reporter_app/agents/agent_3_aggregator.py
# This version includes the definitive Data Propagation logic.
# ==============================================================================

import pandas as pd

def hierarchical_aggregator_agent(source_df, notes_structure):
    """
    AGENT 3: Uses the mapping rules and propagates summary data down
    into the detailed structure to ensure cells are filled.
    """
    print("\n--- Agent 3 (Hierarchical Aggregator): Processing data... ---")
    source_df['Particulars_clean'] = source_df['Particulars'].str.lower().str.strip()

    def initialize_structure(sub_items_template):
        initialized = {}
        for key, value in sub_items_template.items():
            initialized[key] = initialize_structure(value) if isinstance(value, dict) else {'CY': 0, 'PY': 0}
        return initialized

    def match_and_aggregate(current_data, current_template, full_df):
        total_cy, total_py = 0, 0
        for key, template_value in current_template.items():
            if isinstance(template_value, dict):
                sub_total_cy, sub_total_py = match_and_aggregate(current_data[key], template_value, full_df)
                current_data[key]['total'] = {'CY': sub_total_cy, 'PY': sub_total_py}
                total_cy += sub_total_cy
                total_py += sub_total_py
            else:
                item_total_cy, item_total_py = 0, 0
                keywords = [kw.lower().strip() for kw in (template_value if isinstance(template_value, list) else [template_value])]
                pattern = '|'.join([r'\b' + kw.replace(r'(', r'\(').replace(r')', r'\)').replace('.', r'\.') + r'\b' for kw in keywords])
                matched_rows = full_df[full_df['Particulars_clean'].str.contains(pattern, na=False, regex=True)]
                
                if not matched_rows.empty:
                    item_total_cy += matched_rows['Amount_CY'].sum()
                    item_total_py += matched_rows['Amount_PY'].sum()

                current_data[key] = {'CY': item_total_cy, 'PY': item_total_py}
                total_cy += item_total_cy
                total_py += item_total_py
        return total_cy, total_py

    aggregated_data = {}
    for note_num, note_data in notes_structure.items():
        if 'sub_items' in note_data:
            sub_items_result = initialize_structure(note_data['sub_items'])
            note_total_cy, note_total_py = match_and_aggregate(sub_items_result, note_data['sub_items'], source_df)
            
            # --- DEFINITIVE DATA PROPAGATION LOGIC ---
            if note_num == '1' and sub_items_result['Issued, subscribed and fully paid up capital']['Equity shares of Rs. 10 each ']['CY'] == 0:
                sub_items_result['Issued, subscribed and fully paid up capital']['Equity shares of Rs. 10 each ']['CY'] = note_total_cy
                sub_items_result['Issued, subscribed and fully paid up capital']['Equity shares of Rs. 10 each ']['PY'] = note_total_py
            
            if note_num == '2' and sub_items_result['2.6 Surplus / (Deficit) in Statement of Profit and Loss']['Balance at the end of the year     ']['CY'] == 0:
                other_reserves_cy = sub_items_result['2.1 Capital reserve']['total']['CY'] + sub_items_result['2.2 Securities premium account']['total']['CY'] + sub_items_result['2.4 General reserve']['total']['CY']
                other_reserves_py = sub_items_result['2.1 Capital reserve']['total']['PY'] + sub_items_result['2.2 Securities premium account']['total']['PY'] + sub_items_result['2.4 General reserve']['total']['PY']
                surplus_cy = note_total_cy - other_reserves_cy
                surplus_py = note_total_py - other_reserves_py
                sub_items_result['2.6 Surplus / (Deficit) in Statement of Profit and Loss']['Balance at the end of the year     ']['CY'] = surplus_cy
                sub_items_result['2.6 Surplus / (Deficit) in Statement of Profit and Loss']['Balance at the end of the year     ']['PY'] = surplus_py

            if note_num == '26':
                # Check if the detailed lines were found. If not, propagate the total.
                sum_of_details_cy = sum(v['CY'] for k, v in sub_items_result.items() if k != 'Other expenses')
                if sum_of_details_cy == 0 and note_total_cy != 0:
                    sub_items_result['Other expenses']['CY'] = note_total_cy
                    sub_items_result['Other expenses']['PY'] = note_total_py
            
            # General propagation for any simple, single-item note that was missed
            if len(note_data['sub_items']) == 1:
                first_key = next(iter(sub_items_result))
                if isinstance(sub_items_result[first_key], dict) and len(sub_items_result[first_key]) == 1:
                     second_key = next(iter(sub_items_result[first_key]))
                     if sub_items_result[first_key][second_key]['CY'] == 0 and note_total_cy != 0:
                        sub_items_result[first_key][second_key]['CY'] = note_total_cy
                        sub_items_result[first_key][second_key]['PY'] = note_total_py
            # --- END OF PROPAGATION LOGIC ---

            aggregated_data[note_num] = {
                'total': {'CY': note_total_cy, 'PY': note_total_py},
                'sub_items': sub_items_result,
                'title': note_data['title']
            }
    print("✅ Aggregation & Propagation SUCCESS: Data processed into hierarchical structure.")
    return aggregated_data
