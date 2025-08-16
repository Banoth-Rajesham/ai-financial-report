# ==============================================================================
# FILE: agents/agent_3_aggregator.py (DEFINITIVE CORRECTION)
# ==============================================================================
import pandas as pd

def hierarchical_aggregator_agent(source_df, notes_structure):
    """
    AGENT 3: Uses the explicit contextual aliases from the config to perform a
    flexible search against the contextual data from Agent 1, ensuring accurate
    and detailed data aggregation.
    """
    print("\n--- Agent 3 (Hierarchical Aggregator): Processing data via contextual search... ---")
    
    # Create a lookup dictionary from the source dataframe for fast access.
    # The keys are the unique contextual strings created by Agent 1 (e.g., "Header|Particular").
    # We clean them for reliable matching.
    data_lookup = {
        row['Particulars'].lower().strip(): {'CY': row['Amount_CY'], 'PY': row['Amount_PY']}
        for _, row in source_df.iterrows()
    }
    
    # Get a list of all available contextual keys from the source data
    available_data_keys = list(data_lookup.keys())

    def initialize_structure(template):
        """Pre-builds the nested dictionary structure with zero values."""
        initialized = {}
        for key, value in template.items():
            initialized[key] = initialize_structure(value) if isinstance(value, dict) else {'CY': 0, 'PY': 0}
        return initialized

    def process_level(data_node, template_node):
        """
        Recursively traverses the template, searches for aliases within the
        contextual keys, and aggregates the data.
        """
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
                
                # This is the crucial logic: Search for aliases within the available data keys
                for alias in aliases_to_check:
                    search_term = alias.lower().strip()
                    for data_key in available_data_keys:
                        # If the alias is found within the contextual key, it's a match
                        if search_term in data_key:
                            matched_data = data_lookup[data_key]
                            item_total_cy += matched_data.get('CY', 0)
                            item_total_py += matched_data.get('PY', 0)

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

    print("✅ Aggregation SUCCESS: Contextual data processed into detailed hierarchical structure.")
    return aggregated_data
