# ==============================================================================
# PASTE THIS ENTIRE, CORRECTED BLOCK INTO: agent_2_ai_mapping.py
# ==============================================================================
import copy
import requests
import json

def ai_mapping_agent(source_particulars, mapping_structure, api_url=None, api_key=None):
    """
    AGENT 2: Uses an external API to map unrecognized financial terms.
    """
    print("\n--- Agent 2 (AI Mapping): Searching for unrecognized terms... ---")
    updated_mapping = copy.deepcopy(mapping_structure)
    def get_all_keywords(node, keywords_set):
        for key, value in node.items():
            if isinstance(value, list):
                for kw in value: keywords_set.add(kw.lower())
            elif isinstance(value, dict):
                get_all_keywords(value, keywords_set)

    all_known_keywords = set()
    get_all_keywords(updated_mapping, all_known_keywords)
    unmapped_terms = {p.lower() for p in source_particulars if p.lower() not in all_known_keywords}
    if not unmapped_terms:
        print("✅ All terms are already recognized.")
        return updated_mapping

    if not api_url or not api_key:
        print("⚠️  API credentials not provided. Proceeding without AI enhancements.")
        return updated_mapping
    print(f"  -> Found {len(unmapped_terms)} unrecognized terms. Calling mapping API...")

    ai_responses = {}
    try:
        known_categories = [note['title'] for note in mapping_structure.values()]
        payload = {"terms_to_map": list(unmapped_terms), "available_categories": known_categories}
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=45)
        response.raise_for_status()
        ai_responses = response.json()
        print("  -> API response received.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Custom API Mapping FAILED: {e}. Proceeding without AI enhancements.")
        return updated_mapping

    def find_and_update(node, target_title, new_keyword):
        for note_data in node.values():
            if note_data.get('title') == target_title:
                for sub_item in note_data.get('sub_items', {}).values():
                    if isinstance(sub_item, list):
                        if new_keyword not in sub_item: sub_item.append(new_keyword)
                        return True
                return False

    for term, category_title in ai_responses.items():
        if not find_and_update(updated_mapping, category_title, term):
            print(f"  -> Warning: Could not find a place to map '{term}' under category '{category_title}'.")
    print("✅ AI mapping complete.")
    return updated_mapping
