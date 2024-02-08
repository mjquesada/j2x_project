import streamlit as st
from functions import set_background_color_row1, set_background_color_row2

def main_tab():
    # Your main tab content here
    st.title('Main Tab')

    # Row 1: Personnel Count and AOR Breakdown
    col1, col2 = st.columns([2, 3])

    # Component on the left (col1): Personnel Count
    with col1:
        personnel_count_title = "<h2>Personnel Count</h2>"
        personnel_count_content = "1500"  # You can update the count dynamically
        styled_component = set_background_color_row1('#87CEEB', 15, personnel_count_title, personnel_count_content)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component on the right (col2): AOR Breakdown
    with col2:
        aor_breakdown_title = "<h2>AOR Breakdown</h2>"
        aor_labels = ['AFRICOM', 'CENTCOM', 'EUCOM', 'INDOPACOM']
        aor_values = [700, 800, 600, 1053]

        # Combine AOR breakdown into a single component
        aor_component = ""
        for label, value in zip(aor_labels, aor_values):
            aor_component += f"{label}: {value} people<br>"

        # Apply styling to the entire AOR breakdown
        styled_component = set_background_color_row1('#87CEEB', 15, aor_breakdown_title, aor_component)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Add more space between Row 1 and Row 2 using margin
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)

    # Row 2: Components with logos and words
    col1_row2, col2_row2, col3_row2, col4_row2, col5_row2 = st.columns(5)

    # Component 1 (col1_row2): USASOC
    with col1_row2:
        usasoc_component = {
            'image_path': 'images/USASOC.png',
            'title': 'USASOC',
            'content': 'Some description about USASOC'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=usasoc_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 2 (col2_row2): NSW
    with col2_row2:
        nsw_component = {
            'image_path': 'images/NSW.jpeg',
            'title': 'NSW',
            'content': 'Some description about NSW'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=nsw_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 3 (col3_row2): HEADQUARTERS
    with col3_row2:
        headquarters_component = {
            'image_path': 'images/SOCOM.png',
            'title': 'HEADQUARTERS',
            'content': 'Some description about HEADQUARTERS'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=headquarters_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 4 (col4_row2): MARSOC
    with col4_row2:
        marsoc_component = {
            'image_path': 'images/MARSOC.jpeg',
            'title': 'MARSOC',
            'content': 'Some description about MARSOC'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=marsoc_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 5 (col5_row2): AFSOC
    with col5_row2:
        afsoc_component = {
            'image_path': 'images/AFSOC.png',
            'title': 'AFSOC',
            'content': 'Some description about AFSOC'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=afsoc_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Add more space between Row 1 and Row 2 using margin
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)

    # Row 3: Components with logos and words
    col1_row3, col2_row3, col3_row3, col4_row3, col5_row3, col6_row3, col7_row3 = st.columns(7)

    # Component 1 (col1_row3): SOCCENT
    with col1_row3:
        soccent_component = {
            'image_path': 'images/SOCCENT.png',
            'title': 'SOCCENT',
            'content': 'Some description about SOCCENT'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=soccent_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 2 (col2_row3): SOCSOUTH
    with col2_row3:
        socsouth_component = {
            'image_path': 'images/SOCSOUTH.jpeg',
            'title': 'SOCSOUTH',
            'content': 'Some description about SOCSOUTH'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=socsouth_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 3 (col3_row3): SOCNORTH
    with col3_row3:
        socnorth_component = {
            'image_path': 'images/SOCNORTH.jpeg',
            'title': 'SOCNORTH',
            'content': 'Some description about SOCNORTH'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=socnorth_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 4 (col4_row3): SOCPAC
    with col4_row3:
        socpac_component = {
            'image_path': 'images/SOCPAC.jpeg',
            'title': 'SOCPAC',
            'content': 'Some description about SOCPAC'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=socpac_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 5 (col5_row3): SOCKOR
    with col5_row3:
        sockor_component = {
            'image_path': 'images/SOCKOR.png',
            'title': 'SOCKOR',
            'content': 'Some description about SOCKOR'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=sockor_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 6 (col6_row3): SOCEUR
    with col6_row3:
        soceur_component = {
            'image_path': 'images/SOCEUR.png',
            'title': 'SOCEUR',
            'content': 'Some description about SOCEUR'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=soceur_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)

    # Component 7 (col7_row3): SOCAF
    with col7_row3:
        socaf_component = {
            'image_path': 'images/SOCAF.png',
            'title': 'SOCAF',
            'content': 'Some description about SOCAF'
        }
        styled_component = set_background_color_row2('#cccccc', padding=15, component=socaf_component, fixed_height=True)
        st.markdown(styled_component, unsafe_allow_html=True)