import streamlit as st
from main import main_tab
from map import map_tab
from roster import roster_tab

def run_app():
    st.set_page_config(page_title='J2X', page_icon=':rocket:')
    custom_css = """
    <style>
    h1 {
        margin-top: 0;
    }
    /* Add this block for custom styling of Row 1 components */
    [data-testid="stHorizontalBlock"] > div {
        margin: 0;
        padding: 0;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown('<div style="display: flex; flex-direction: row;">', unsafe_allow_html=True)

    # Sidebar with buttons
    selected_tab = st.sidebar.radio("Navigation", ['Main', 'Map', 'Roster'])

    if selected_tab == 'Main':
        main_tab()
    elif selected_tab == 'Map':
        map_tab()
    elif selected_tab == 'Roster':
        roster_tab()

if __name__ == "__main__":
    run_app()