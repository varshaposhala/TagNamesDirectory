from streamlit import columns

import json_utils

import streamlit as st

data = None

if not data:
    data = json_utils.get_json_data()

st.markdown('# Find Topin Tags')

col1, col2, col3 = st.columns([1,1,1])

section = col1.selectbox('Choose Section', json_utils.get_sections(data))

topic = col2.selectbox('Choose Topic', json_utils.get_topics(data, section))

sub_topic = col3.selectbox('Choose Sub-Topic', json_utils.get_sub_topics(data, section, topic))