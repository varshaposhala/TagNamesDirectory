import streamlit as st
import json_utils  # Your utility file
import os  # For deployment scenarios (e.g., Streamlit sharing servers)

# Optional: Set environment variable for headless mode
# os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

# Streamlit page configuration
st.set_page_config(
    page_title="TOPIN TAGS | PST-Tech",
    page_icon="✨",
    layout="centered",
)

# --- Data Loading and Caching ---
@st.cache_data
def load_and_prepare_data():
    print("Attempting to fetch and process data from URL...")
    raw_json = json_utils.fetch_and_parse_json_from_url()
    if raw_json:
        processed_dropdown_data = json_utils.get_processed_data(raw_json)
        if not processed_dropdown_data:
            print("Warning: Processed data is empty. Check JSON structure or 'question_tags' key.")
        return raw_json, processed_dropdown_data
    return None, None

# Load data
raw_data_global, processed_data_for_dropdowns_global = load_and_prepare_data()

# Error handling
if not raw_data_global or not processed_data_for_dropdowns_global:
    st.error(
        "🚨 Failed to load or process data. Please check the data source URL, your internet connection, "
        "or the JSON structure (ensure 'question_tags' exists and is structured as expected)."
    )
    st.stop()

# --- Custom CSS Styling ---
st.markdown("""
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #333;
}
.center-text {
    text-align: center;
    margin-bottom: 40px;
}
.center-text h1 {
    color: #007bff;
    font-weight: 700;
    letter-spacing: -0.5px;
}
.dropdown-container {
    border: 1px solid #e0e0e0;
    padding: 25px;
    border-radius: 12px;
    background-color: #fcfdff;
    margin-bottom: 30px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.07);
}
.dropdown-container .stSelectbox > label {
    font-weight: 600;
    font-size: 1.1em;
    color: #2c3e50;
    margin-bottom: 10px;
}
.stSelectbox > label::before {
    content: none !important;
    display: none !important;
}
.output-display {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px dashed #ccc;
}
.output-display .output-pair {
    margin-bottom: 12px;
}
.output-display .output-label {
    font-weight: 500;
    color: #5a6773;
    font-size: 0.9em;
    margin-bottom: 4px;
    display: block;
}
.output-display .stCodeBlock {
    background-color: #e9ecef !important;
    border: 1px solid #ced4da !important;
    border-radius: 6px;
    padding: 8px 12px !important;
    font-size: 0.95em;
    color: #343a40;
    box-shadow: none;
}
.stAlert {
    border-radius: 8px;
    padding: 12px 15px;
    font-size: 1em;
    margin-bottom: 30px;
}
.stAlert p {
    line-height: 1.5;
    margin-bottom: 0;
}
div[data-testid="stVerticalBlock"] > .stAlert {
    margin-bottom: 30px;
}
</style>
<div class="center-text">
    <h1>🏷️ Topin Tags Explorer</h1>
</div>
""", unsafe_allow_html=True)

# --- Section Dropdown ---
# st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
sections_list = json_utils.get_sections(processed_data_for_dropdowns_global)
selected_section = None

if not sections_list:
    st.warning("🤔 No sections available. The data might be empty or not processed correctly.")
else:
    selected_section = st.selectbox(
    label="**Choose Section**",  # Markdown bold
    options=sections_list,
    key="section_selectbox",
    index=0
)

# st.markdown('</div>', unsafe_allow_html=True)

# --- Topic Dropdown ---
selected_topic = None
if selected_section:
    # st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
    topics_list = json_utils.get_topics(processed_data_for_dropdowns_global, selected_section)

    if not topics_list:
        st.info(f"🤷 No topics found for section: '{selected_section}'.")
    else:
        selected_topic = st.selectbox(
            label='**Choose Topic**', 
            options=topics_list,
            key="topic_selectbox",
            index=0 if topics_list else None
        )

        if selected_topic:
            st.markdown('<div class="output-display">', unsafe_allow_html=True)

            st.markdown('<div class="output-pair">', unsafe_allow_html=True)
            st.markdown('<span class="output-label"><b>Topic Label:</b></span>', unsafe_allow_html=True)
            st.code(json_utils.get_topic_label(raw_data_global, selected_section, selected_topic) or "N/A", language=None)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="output-pair">', unsafe_allow_html=True)
            st.markdown('<span class="output-label"><b>Topic Value:</b></span>', unsafe_allow_html=True)
            st.code(selected_topic, language=None)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
    # st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👈 Select a section above to explore topics.")

# --- Sub-Topic Dropdown ---
selected_sub_topic = None
if selected_section and selected_topic:
    # st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
    sub_topics_list = json_utils.get_sub_topics(processed_data_for_dropdowns_global, selected_section, selected_topic)

    if not sub_topics_list:
        st.info(f"📪 No sub-topics found for topic: '{selected_topic}'.")
    else:
        selected_sub_topic = st.selectbox(
            label='**Choose Sub-Topic**', options=sub_topics_list,
            key="subtopic_selectbox",
            index=0 if sub_topics_list else None
        )

        if selected_sub_topic:
            st.markdown('<div class="output-display">', unsafe_allow_html=True)

            st.markdown('<div class="output-pair">', unsafe_allow_html=True)
            st.markdown('<span class="output-label"><b>Sub-Topic Label:</b></span>', unsafe_allow_html=True)
            st.code(json_utils.get_sub_topic_label(raw_data_global, selected_section, selected_topic, selected_sub_topic) or "N/A", language=None)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="output-pair">', unsafe_allow_html=True)
            st.markdown('<span class="output-label"><b>Sub-Topic Value:</b></span>', unsafe_allow_html=True)
            st.code(selected_sub_topic, language=None)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
    # st.markdown('</div>', unsafe_allow_html=True)
elif selected_section:
    st.info("👆 Select a topic above to explore sub-topics.")

else:
    # Placeholder message if no section selected yet (for the sub-topic area)
    # This message might be redundant if the topic placeholder is already shown,
    # but kept for clarity in logic. We can refine if needed.
    if not selected_section : # Only show this if the section placeholder is also active
        pass # The message "Select a section above..." is already handling this
    # else: # This case means section is selected, but topic is not (already handled by topic's elif)
    #    st.info("👈 Start by selecting a section and topic to explore sub-topics.")