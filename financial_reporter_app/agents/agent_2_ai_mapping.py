# agents/agent_2_ai_mapping.py

import streamlit as st
import copy
import requests
import json

def ai_mapping_agent(source_particulars, mapping_structure):
    """
    AGENT 2: Uses an external API to map unrecognized financial terms.
    """
    print("\n--- Agent 2 (AI Mapping): Searching for unrecognized terms... ---")

    updated_mapping = copy.deepcopy(mapping_structure)

    # First, find all keywords that are already known in the mapping structure
    all_known_keywords = set()
    def get_all_keywords(node):
        for key, value in node.items():
            if isinstance(value, list):
                for kw in value:
                    all_known_keywords.add(kw.lower())
            if isinstance(value, dict):
                get_all_keywords(value)
    get_all_keywords(updated_mapping)

    # Identify terms from the source data that are not in our known keywords
    unmapped_terms = {p.lower() for p in source_particulars if p.lower() not in all_known_keywords}

    if not unmapped_terms:
        print("✅ All terms are already recognized.")
        return updated_mapping

    print(f"  -> Found {len(unmapped_terms)} unrecognized terms. Calling mapping API...")

    ai_responses = {}
    try:
        # --- SECURELY GET API DETAILS FROM STREAMLIT SECRETS ---
        # These names MUST match the keys in your Streamlit Cloud secrets settings.
        YOUR_API_URL = st.secrets["MAPPING_API_URL"]
        YOUR_API_KEY = st.secrets["MAPPING_API_KEY"]
        # ---------------------------------------------------------

        # Get a list of all possible categories to help the AI
        known_categories = []
        for note in mapping_structure.values():
            for category in note.get('sub_items', {}).keys():
                known_categories.append(category)

        payload = {
            "terms_to_map": list(unmapped_terms),
            "available_categories": known_categories
        }
        headers = {
            "Authorization": f"Bearer {YOUR_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(YOUR_API_URL, headers=headers, data=json.dumps(payload), timeout=45)
        response.raise_for_status() # Raise an error for bad responses (4xx or 5xx)
        ai_responses = response.json()
        print("  -> API response received.")

    except (FileNotFoundError, KeyError) as e:
        print(f"⚠️  API is not configured. Missing secret: {e}. Proceeding without AI enhancements.")
        ai_responses = {}
    except requests.exceptions.RequestException as e:
        print(f"❌ Custom API Mapping FAILED: {e}. Proceeding without AI enhancements.")
        ai_responses = {}

    # This helper function finds where to add the new keyword in the mapping structure
    def find_and_update(node, target_key, new_keyword):
        for key, value in node.items():
            if key == target_key and isinstance(value, list):
                if new_keyword not in value:
                    value.append(new_keyword)
                return True
            if isinstance(value, dict):
                if find_and_update(value, target_key, new_keyword):
                    return True
        return False

    # Update the mapping structure with the responses from the AI
    for term, category in ai_responses.items():
        find_and_update(updated_mapping, category, term)

    print("✅ AI mapping complete.")
    return updated_mapping
