import streamlit as st
import streamlit_antd_components as sac
from dotenv import load_dotenv
from pages import home_run, register_run


load_dotenv()


def menu_callback():
    st.session_state.page_index = pages[st.session_state.tab_item][1]


pages = {
    "Home": [home_run, 0, "house"],
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
    .appview-container .main .block-container{{
            padding-top: {padding_top}rem; 
            padding-left: 1rem;
            padding-right: 1rem;}}
    </style>
    """.format(
            padding_top=2.0
        ),
        unsafe_allow_html=True,
    )
    sac.tabs(
        [sac.TabsItem(label=i, icon=pages[i][2]) for i in pages.keys()],
        # variant="outline",
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