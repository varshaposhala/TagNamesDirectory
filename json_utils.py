import os
import json


def get_json_data():
    file_path = os.path.join(os.getcwd(), 'jsons', 'tags.json')

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        updated_data = {}
        for section in sorted(list(data.keys())):
            updated_data[section] = {}

            for section_data in data.get(section):
                topic = section_data.get('topic_name').get('value')
                subtopics = []

                for subtopic_data in section_data.get('sub_topics'):
                    subtopics.append(subtopic_data.get('sub_topic_name').get('value'))

                updated_data[section][topic] = sorted(subtopics)


    return updated_data

def get_sections(data):
    return sorted(data.keys())

def get_topics(data, section):
    if section in data.keys():
        return sorted(data[section].keys())

def get_sub_topics(data, section, topic):
    if section in data.keys() and topic in data[section].keys():
        return sorted(data[section][topic])


