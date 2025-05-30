import json
import requests

JSON_URL = "https://nxtwave-assessments-backend-nxtwave-media-static.s3.ap-south-1.amazonaws.com/topin_config_prod/static/static_content.json"

def fetch_and_parse_json_from_url():
    """
    Fetches raw JSON from the defined URL.
    Returns the parsed JSON dictionary or None if an error occurs.
    """
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
        return None
    except json.JSONDecodeError as e: # If response is not valid JSON
        print(f"Error decoding JSON: {e}")
        return None

def get_processed_data(raw_data):
    """
    Processes the raw JSON data (specifically the 'question_tags' part)
    into the nested dictionary structure:
    {section_value: {topic_value: [sub_topic_value1, sub_topic_value2, ...]}}
    This data is used to populate the dropdowns with 'value' fields.
    """
    if not raw_data or "question_tags" not in raw_data:
        print("Warning: 'question_tags' not found in raw_data or raw_data is empty.")
        return {}

    question_tags_data = raw_data.get("question_tags", {})
    updated_data = {}
    
    # Iterate over sorted section keys (these are the 'values' for sections)
    for section_key in sorted(list(question_tags_data.keys())):
        updated_data[section_key] = {}
        
        section_items = question_tags_data.get(section_key, [])
        if not isinstance(section_items, list):
            # print(f"Warning: Expected list for section '{section_key}', got {type(section_items)}. Skipping.")
            continue

        for section_data_item in section_items:
            if not isinstance(section_data_item, dict):
                # print(f"Warning: Expected dict for item in section '{section_key}', got {type(section_data_item)}. Skipping.")
                continue

            topic_name_data = section_data_item.get('topic_name', {})
            topic_value = topic_name_data.get('value')

            if not topic_value: # Skip if topic_value is missing or empty
                # print(f"Warning: Missing topic_name value in section '{section_key}'. Item: {section_data_item}")
                continue
            
            subtopics_values = []
            sub_topics_list = section_data_item.get('sub_topics', [])
            if not isinstance(sub_topics_list, list):
                # print(f"Warning: Expected list for sub_topics in topic '{topic_value}', got {type(sub_topics_list)}. Skipping.")
                continue

            for subtopic_data_item in sub_topics_list:
                if not isinstance(subtopic_data_item, dict):
                    # print(f"Warning: Expected dict for subtopic item in topic '{topic_value}', got {type(subtopic_data_item)}. Skipping.")
                    continue
                
                sub_topic_name_data = subtopic_data_item.get('sub_topic_name', {})
                subtopic_value = sub_topic_name_data.get('value')
                if subtopic_value: # Add only if subtopic_value is not empty
                    subtopics_values.append(subtopic_value)
            
            # Store sorted list of subtopic values for the current topic
            # Only add topic if it has subtopics or if you want to show topics without subtopics
            # Ensure topic is added even if subtopics_values is empty, if the topic itself is valid
            updated_data[section_key][topic_value] = sorted(subtopics_values)
            
    return updated_data

# --- Functions operating on PROCESSED data (for dropdown options) ---
def get_sections(processed_data):
    """Returns a sorted list of section values."""
    return sorted(processed_data.keys())

def get_topics(processed_data, section_value):
    """Returns a sorted list of topic values for a given section."""
    if section_value in processed_data:
        return sorted(processed_data[section_value].keys())
    return [] # Return empty list if section_value not found or has no topics

def get_sub_topics(processed_data, section_value, topic_value):
    """Returns a sorted list of sub-topic values for a given section and topic."""
    if section_value in processed_data and \
       topic_value in processed_data[section_value]:
        return sorted(processed_data[section_value][topic_value])
    return [] # Return empty list if not found

# --- Functions operating on RAW data (for retrieving labels) ---
def get_topic_label(raw_data, section_value, topic_value_to_find):
    """Retrieves the 'label' for a given topic value within a section from raw data."""
    if not raw_data or "question_tags" not in raw_data:
        return None
    
    question_tags_data = raw_data.get("question_tags", {})
    if section_value not in question_tags_data:
        return None
    
    section_items = question_tags_data.get(section_value, [])
    if not isinstance(section_items, list):
        return None

    for item in section_items:
        if isinstance(item, dict):
            topic_name_data = item.get('topic_name', {})
            if topic_name_data.get('value') == topic_value_to_find:
                return topic_name_data.get('label')
    return None # Topic value not found

def get_sub_topic_label(raw_data, section_value, topic_value_to_find, sub_topic_value_to_find):
    """Retrieves the 'label' for a given sub-topic value within a topic and section from raw data."""
    if not raw_data or "question_tags" not in raw_data:
        return None

    question_tags_data = raw_data.get("question_tags", {})
    if section_value not in question_tags_data:
        return None

    section_items = question_tags_data.get(section_value, [])
    if not isinstance(section_items, list):
        return None

    for item in section_items:
        if isinstance(item, dict):
            topic_name_data = item.get('topic_name', {})
            if topic_name_data.get('value') == topic_value_to_find:
                sub_topics_list = item.get('sub_topics', [])
                if not isinstance(sub_topics_list, list):
                    continue # Malformed sub_topics, skip this item
                for sub_item in sub_topics_list:
                    if isinstance(sub_item, dict):
                        sub_topic_name_data = sub_item.get('sub_topic_name', {})
                        if sub_topic_name_data.get('value') == sub_topic_value_to_find:
                            return sub_topic_name_data.get('label')
    return None # Sub-topic value not found