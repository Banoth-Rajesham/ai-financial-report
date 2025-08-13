# ==============================================================================
# FILE: agents/agent_3_aggregator.py (UPDATED)
# ==============================================================================

def hierarchical_aggregator_agent(source_df, notes_structure):
    """
    AGENT 3: Uses the mapping rules and the contextual data from Agent 1
    to process and sum up the data accurately via an exact-match strategy.
    """
    print("\n--- Agent 3 (Hierarchical Aggregator): Processing contextual data... ---")

    # Clean the contextual keys from Agent 1 ONCE for efficient matching.
    source_df['Particulars_clean'] = source_df['Particulars'].str.lower().str.strip()

    # Create a lookup dictionary for fast O(1) access to source data.
    # Key: "header|particular", Value: {'CY': amount, 'PY': amount}
    data_lookup = {
        row['Particulars_clean']: {'CY': row['Amount_CY'], 'PY': row['Amount_PY']}
        for _, row in source_df.iterrows()
    }

    def initialize_structure(template):
        """Recursively initializes the nested dictionary structure with zero values."""
        initialized = {}
        for key, value in template.items():
            if isinstance(value, dict):
                initialized[key] = initialize_structure(value)
            else:
                initialized[key] = {'CY': 0, 'PY': 0}
        return initialized

    def process_level(data_node, template_node, parent_header=""):
        """
        Recursively traverses the template, using the immediate parent key as the
        header context to perform an exact match against the data from Agent 1.
        """
        level_total_cy, level_total_py = 0, 0

        for key, value in template_node.items():
            if isinstance(value, dict):
                # This is a header/section. Recurse deeper, passing the current key as the new context.
                sub_total_cy, sub_total_py = process_level(data_node[key], value, key)
                data_node[key]['total'] = {'CY': sub_total_cy, 'PY': sub_total_py}
                level_total_cy += sub_total_cy
                level_total_py += sub_total_py
            else:
                # This is a leaf node (an actual data item).
                item_total_cy, item_total_py = 0, 0
                aliases_to_check = [key] + value if isinstance(value, list) else [key]

                for alias in aliases_to_check:
                    # Strategy 1: Look for a contextual match (e.g., "header|particular").
                    if parent_header:
                        search_key = f"{parent_header}|{alias}".lower().strip()
                        if search_key in data_lookup:
                            matched_data = data_lookup.get(search_key, {'CY': 0, 'PY': 0})
                            item_total_cy += matched_data['CY']
                            item_total_py += matched_data['PY']

                    # Strategy 2: Look for a standalone match (particular with no header).
                    # This is important for items that are not under a specific header.
                    standalone_key = alias.lower().strip()
                    if standalone_key in data_lookup:
                        matched_data = data_lookup.get(standalone_key, {'CY': 0, 'PY': 0})
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
            # Start the recursion for the note. The initial parent_header is an empty string.
            note_total_cy, note_total_py = process_level(sub_items_result, note_data['sub_items'], "")

            aggregated_data[note_num] = {
                'total': {'CY': note_total_cy, 'PY': note_total_py},
                'sub_items': sub_items_result,
                'title': note_data['title']
            }

    print("✅ Aggregation SUCCESS: Contextual data processed into hierarchical structure.")
    return aggregated_data
