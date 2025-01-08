import os
import json_utils
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx


os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

# Change default theme or settings dynamically
st.set_page_config(
    page_title="TOPIN TAGS | PST-Tech",
    page_icon="icon.png",
    layout="centered",
)

data = None

if not data:
    data = json_utils.get_json_data()

st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
    }
    
    .dropdown-group {
        border: 1px solid #4CAF50;  /* Green border */
        padding: 2px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    </style>
    <div class="center-text">
        <h1>Find Topin Tags</h1>
    </div>
    """,
    unsafe_allow_html=True
)


with st.container():
    st.markdown('<div class="dropdown-group">', unsafe_allow_html=True)
    section = st.selectbox('Choose Section', json_utils.get_sections(data))
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="dropdown-group">', unsafe_allow_html=True)
    topic = st.selectbox('Choose Topic', json_utils.get_topics(data, section))
    st.caption('label')
    st.code(json_utils.get_topic_value(section, topic))
    st.caption('value')
    st.code(topic)
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="dropdown-group">', unsafe_allow_html=True)
    sub_topic = st.selectbox('Choose Sub-Topic', json_utils.get_sub_topics(data, section, topic))
    st.caption('label')
    st.code(json_utils.get_sub_topic_value(section, topic, sub_topic))
    st.caption('value')
    st.code(sub_topic)
    st.markdown("</div>", unsafe_allow_html=True)
