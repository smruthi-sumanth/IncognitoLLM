import os

import streamlit as st
import streamlit_antd_components as sac
from dotenv import load_dotenv
from pages import register_run, dashboard_run
load_dotenv()

def menu_callback():
    st.session_state.page_index = pages[st.session_state.tab_item][1]

pages = {
    "Dashboard": [dashboard_run, 0, "house"],
    "Register": [register_run, 1, "search"],
}

def main():
    st.set_page_config(
        page_title="SecurA",
        page_icon="👮🏻",
        layout="wide",
    )

    if "page_index" not in st.session_state:
        st.session_state.page_index = 0

    st.markdown(
        """
        <style>
   .appview-container.main.block-container{{
            padding-top: {padding_top}rem; 
            padding-left: 1rem;
            padding-right: 1rem;}}
    .block-container.st-emotion-cache-1jicfl2 {{
    padding: 2rem 1rem 10rem;
    }}
    </style>
    """.format(
            padding_top=0.5
        ),
        unsafe_allow_html=True,
    )
    sac.tabs(
        [sac.TabsItem(label=i, icon=pages[i][2]) for i in pages.keys()],
        index=st.session_state.page_index,
        color="teal",
        on_change=menu_callback,
        size="xl",
        key="tab_item",
    )
    try:
        pages[st.session_state.tab_item][0]()
    except Exception as e:
        st.error(f"Page '{st.session_state.tab_item}' not found.")
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
