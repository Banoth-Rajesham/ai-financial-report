# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: agent_3_aggregator.py
# This version features a cleaner, more robust, and more efficient logic.
# ==============================================================================
import pandas as pd

def hierarchical_aggregator_agent(source_df, notes_structure):
    """
    AGENT 3: Aggregates financial data based on the mapping structure and intelligently
    propagates summary-level data down to the most logical sub-item.
    """
    print("\n--- Agent 3 (Hierarchical Aggregator): Processing data... ---")
    
    # Prepare the source dataframe for efficient matching
    source_df['Particulars_clean'] = source_df['Particulars'].str.lower().str.strip()
    source_df['Amount_CY'] = pd.to_numeric(source_df['Amount_CY'], errors='coerce').fillna(0)
    source_df['Amount_PY'] = pd.to_numeric(source_df['Amount_PY'], errors='coerce').fillna(0)

    # Helper to flatten the nested keyword structure for easier lookup
    def flatten_keywords(structure):
        keyword_map = {}
        def recurse(node, path):
            for key, value in node.items():
                new_path = path + (key,)
                if isinstance(value, list):
                    for keyword in value:
                        keyword_map[keyword.lower().strip()] = new_path
                elif isinstance(value, dict):
                    recurse(value, new_path)
        for note_num, note_data in structure.items():
            if 'sub_items' in note_data:
                recurse(note_data['sub_items'], (note_num,))
        return keyword_map
    
    keyword_to_path = flatten_keywords(notes_structure)

    # Initialize the final data structure
    aggregated_data = {note: {'total': {'CY': 0, 'PY': 0}, 'sub_items': {}, 'title': data.get('title', '')} for note, data in notes_structure.items()}

    # --- Main Aggregation Loop ---
    for _, row in source_df.iterrows():
        term = row['Particulars_clean']
        if term in keyword_to_path:
            path = keyword_to_path[term]
            note_num = path[0]
            
            # Navigate and update the nested sub_items structure
            current_level = aggregated_data[note_num]['sub_items']
            for part in path[1:-1]:
                current_level = current_level.setdefault(part, {})
            
            final_key = path[-1]
            item = current_level.setdefault(final_key, {'CY': 0, 'PY': 0})
            item['CY'] += row['Amount_CY']
            item['PY'] += row['Amount_PY']

    # --- Summation and Data Propagation Loop ---
    for note_num, note_data in aggregated_data.items():
        # Recursively sum up totals from sub_items
        def sum_totals(sub_item_dict):
            cy_total, py_total = 0, 0
            for key, value in sub_item_dict.items():
                if isinstance(value, dict) and 'CY' in value: # It's a line item
                    cy_total += value['CY']
                    py_total += value['PY']
                elif isinstance(value, dict): # It's a sub-header
                    sub_cy, sub_py = sum_totals(value)
                    value['total'] = {'CY': sub_cy, 'PY': sub_py} # Store total for the sub-header
                    cy_total += sub_cy
                    py_total += sub_py
            return cy_total, py_total

        note_total_cy, note_total_py = sum_totals(note_data['sub_items'])
        aggregated_data[note_num]['total'] = {'CY': note_total_cy, 'PY': note_total_py}

        # ** CORRECTED Data Propagation Logic **
        # Use the note's title as the main alias to search for a summary value
        note_title = note_data['title'].lower()
        if note_total_cy == 0:
            # Check if the note's title exists as a direct line item in the source data.
            # This is a common pattern for summary values without detailed breakdowns.
            matched_row = source_df[source_df['Particulars_clean'] == note_title]
            if not matched_row.empty:
                propagated_cy = matched_row['Amount_CY'].sum()
                propagated_py = matched_row['Amount_PY'].sum()

                # Assign the propagated value to the first line item found in the note's structure
                def assign_propagated(sub_items):
                    for key, value in sub_items.items():
                        if isinstance(value, dict) and 'CY' in value: # Found a line item
                            value['CY'] = propagated_cy; value['PY'] = propagated_py
                            return True
                        if isinstance(value, dict) and assign_propagated(value): # Recurse
                            return True
                    return False

                if assign_propagated(note_data['sub_items']):
                    print(f"  -> Propagated summary value for Note {note_num}.")
                    # Recalculate totals after propagation
                    note_total_cy, note_total_py = sum_totals(note_data['sub_items'])
                    aggregated_data[note_num]['total'] = {'CY': note_total_cy, 'PY': note_total_py}

    print("✅ Aggregation & Propagation SUCCESS: Data processed into hierarchical structure.")
    return aggregated_data
