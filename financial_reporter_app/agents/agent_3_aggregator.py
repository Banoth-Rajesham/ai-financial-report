# ==============================================================================
# FILE: agents/agent_3_aggregator.py (DEFINITIVE UPDATE)
# ==============================================================================
def hierarchical_aggregator_agent(source_df, notes_structure):
    """
    AGENT 3: Uses the explicit contextual aliases from the config to perform a
    direct, fast, and accurate lookup against the data from Agent 1.
    """
    print("\n--- Agent 3 (Hierarchical Aggregator): Processing data via direct lookup... ---")
    
    # Create a lookup dictionary for fast O(1) access.
    # The keys are the unique contextual strings created by Agent 1.
    data_lookup = {
        row['Particulars'].lower().strip(): {'CY': row['Amount_CY'], 'PY': row['Amount_PY']}
        for _, row in source_df.iterrows()
    }

    def initialize_structure(template):
        """Pre-builds the nested dictionary structure with zero values."""
        initialized = {}
        for key, value in template.items():
            initialized[key] = initialize_structure(value) if isinstance(value, dict) else {'CY': 0, 'PY': 0}
        return initialized

    def process_level(data_node, template_node):
        """Recursively traverses the template and populates data via direct lookup."""
        level_total_cy, level_total_py = 0, 0
        for key, value in template_node.items():
            if isinstance(value, dict): # It's a header/section, so we recurse deeper.
                sub_total_cy, sub_total_py = process_level(data_node[key], value)
                data_node[key]['total'] = {'CY': sub_total_cy, 'PY': sub_total_py}
                level_total_cy += sub_total_cy
                level_total_py += sub_total_py
            else: # It's a leaf node with a list of aliases.
                item_total_cy, item_total_py = 0, 0
                aliases_to_check = value if isinstance(value, list) else [value]
                
                for alias in aliases_to_check:
                    # Directly look up the alias (which is now the full contextual key)
                    search_key = alias.lower().strip()
                    if search_key in data_lookup:
                        matched_data = data_lookup[search_key]
                        item_total_cy += matched_data['CY']
                        item_total_py += matched_data['PY']

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

    print("✅ Aggregation SUCCESS: Contextual data processed into hierarchical structure.")
    return aggregated_data
