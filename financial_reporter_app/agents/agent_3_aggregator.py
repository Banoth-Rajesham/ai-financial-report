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
            # This logic checks if the note's sub-items were filled. If not, it propagates the note's total
            # down to the most logical sub-item, ensuring summary data fills the detailed report.

            sum_of_sub_items_cy = sum(v['CY'] for k,v in sub_items_result.items() if isinstance(v, dict) and 'CY' in v) + \
                                  sum(v['total']['CY'] for k,v in sub_items_result.items() if isinstance(v, dict) and 'total' in v)
            
            if note_total_cy != 0 and sum_of_sub_items_cy == 0:
                # Find the first valid line-item (not a sub-header) to place the total
                for key, value in sub_items_result.items():
                    if isinstance(value, dict) and 'CY' in value: # It's a line item
                        sub_items_result[key]['CY'] = note_total_cy
                        sub_items_result[key]['PY'] = note_total_py
                        break 
                    elif isinstance(value, dict): # It's a sub-header, look inside it
                         for sub_key, sub_value in value.items():
                             if isinstance(sub_value, dict) and 'CY' in sub_value:
                                 sub_items_result[key][sub_key]['CY'] = note_total_cy
                                 sub_items_result[key][sub_key]['PY'] = note_total_py
                                 break
                         else: continue
                         break
            # --- END OF PROPAGATION LOGIC ---

            aggregated_data[note_num] = {
                'total': {'CY': note_total_cy, 'PY': note_total_py},
                'sub_items': sub_items_result,
                'title': note_data['title']
            }
    print("✅ Aggregation & Propagation SUCCESS: Data processed into hierarchical structure.")
    return aggregated_data
