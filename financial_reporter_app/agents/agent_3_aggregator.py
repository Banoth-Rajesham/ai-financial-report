# ==============================================================================
# FILE: agents/agent_3_aggregator.py (DEFINITIVE MASTER VERSION)
# ==============================================================================
def hierarchical_aggregator_agent(source_df, notes_structure):
    """
    AGENT 3: Uses the detailed aliases from the config to perform a fast and
    accurate lookup against the contextual data from Agent 1.
    """
    print("\n--- Agent 3 (Hierarchical Aggregator): Processing data via direct lookup... ---")
    
    # Create a lookup dictionary from the context-aware keys for instant access
    data_lookup = {
        row['Particulars'].lower().strip(): {'CY': row['Amount_CY'], 'PY': row['Amount_PY']}
        for _, row in source_df.iterrows()
    }

    def initialize_structure(template):
        initialized = {}
        for key, value in template.items():
            initialized[key] = initialize_structure(value) if isinstance(value, dict) else {'CY': 0, 'PY': 0}
        return initialized

    def process_level(data_node, template_node, header_context=""):
        level_total_cy, level_total_py = 0, 0
        for key, value in template_node.items():
            # The current path in the dictionary acts as our header context
            current_context = f"{header_context}|{key}" if header_context else key
            
            if isinstance(value, dict): # It's a header/section, so we recurse deeper.
                sub_total_cy, sub_total_py = process_level(data_node[key], value, current_context)
                data_node[key]['total'] = {'CY': sub_total_cy, 'PY': sub_total_py}
                level_total_cy += sub_total_cy
                level_total_py += sub_total_py
            else: # It's a leaf node with a list of aliases.
                item_total_cy, item_total_py = 0, 0
                aliases = value if isinstance(value, list) else [value]
                
                for alias in aliases:
                    # Construct the full contextual key to search for, e.g., "header|alias"
                    search_key_contextual = f"{header_context}|{alias}".lower().strip()
                    search_key_simple = alias.lower().strip()

                    # First, try a direct match with the full context
                    if search_key_contextual in data_lookup:
                        item_total_cy += data_lookup[search_key_contextual]['CY']
                        item_total_py += data_lookup[search_key_contextual]['PY']
                    # If that fails, try matching the alias as a simple key (for top-level items)
                    elif search_key_simple in data_lookup:
                         item_total_cy += data_lookup[search_key_simple]['CY']
                         item_total_py += data_lookup[search_key_simple]['PY']

                data_node[key] = {'CY': item_total_cy, 'PY': item_total_py}
                level_total_cy += item_total_cy
                level_total_py += item_total_py
        return level_total_cy, level_total_py

    aggregated_data = {}
    for note_num, note_data in notes_structure.items():
        if 'sub_items' in note_data:
            sub_items_result = initialize_structure(note_data['sub_items'])
            # Pass the note title as the initial header context
            note_title_context = note_data.get('title', '')
            note_total_cy, note_total_py = process_level(sub_items_result, note_data['sub_items'])
            aggregated_data[note_num] = {
                'total': {'CY': note_total_cy, 'PY': note_total_py},
                'sub_items': sub_items_result,
                'title': note_title_context
            }

    print("✅ Aggregation SUCCESS: Contextual data fully processed.")
    return aggregated_data
