# ==============================================================================
# FILE: agents/agent_3_aggregator.py (CORRECTED TO SUPPORT DETAILED CONFIG)
# ==============================================================================
import pandas as pd

def hierarchical_aggregator_agent(source_df, notes_structure):
    """
    AGENT 3: Uses the detailed aliases from the config to perform a flexible and
    accurate keyword search against the raw data from Agent 1.
    """
    print("\n--- Agent 3 (Hierarchical Aggregator): Processing data via detailed alias search... ---")

    # Prepare the source dataframe by cleaning the 'Particulars' column for searching
    source_df['Particulars_clean'] = source_df['Particulars'].str.lower().str.strip()
    
    # Create a copy to prevent modification issues during iteration
    data_to_search = source_df.copy()

    def initialize_structure(template):
        """Pre-builds the nested dictionary structure with zero values."""
        initialized = {}
        for key, value in template.items():
            initialized[key] = initialize_structure(value) if isinstance(value, dict) else {'CY': 0, 'PY': 0}
        return initialized

    def process_level(data_node, template_node):
        """Recursively traverses the template and populates data via keyword search."""
        level_total_cy, level_total_py = 0, 0
        for key, value in template_node.items():
            if isinstance(value, dict):  # It's a header/section, so we recurse deeper.
                sub_total_cy, sub_total_py = process_level(data_node[key], value)
                data_node[key]['total'] = {'CY': sub_total_cy, 'PY': sub_total_py}
                level_total_cy += sub_total_cy
                level_total_py += sub_total_py
            else:  # It's a leaf node with a list of aliases.
                item_total_cy, item_total_py = 0, 0
                aliases_to_check = value if isinstance(value, list) else [value]
                
                # Build a precise regex pattern from the aliases to search the dataframe
                # Using word boundaries (\b) prevents partial matches (e.g., 'rent' matching 'current')
                pattern = '|'.join([r'\b' + kw.lower().strip().replace(r'(', r'\(').replace(r')', r'\)').replace('.', r'\.') + r'\b' for kw in aliases_to_check])
                
                matched_rows = data_to_search[data_to_search['Particulars_clean'].str.contains(pattern, na=False, regex=True)]

                if not matched_rows.empty:
                    item_total_cy += matched_rows['Amount_CY'].sum()
                    item_total_py += matched_rows['Amount_PY'].sum()

                data_node[key] = {'CY': item_total_cy, 'PY': item_total_py}
                level_total_cy += item_total_cy
                level_total_py += item_total_py
        return level_total_cy, level_total_py

    aggregated_data = {}
    for note_num, note_data in notes_structure.items():
        if 'sub_items' in note_data:
            sub_items_result = initialize_structure(note_data['sub_items'])
            note_total_cy, note_total_py = process_level(sub_items_result, note_data['sub_items'])
            aggregated_data[note_num] = {
                'total': {'CY': note_total_cy, 'PY': note_total_py},
                'sub_items': sub_items_result,
                'title': note_data['title']
            }

    print("✅ Aggregation SUCCESS: Detailed alias search and data processing complete.")
    return aggregated_data
