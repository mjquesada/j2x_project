import streamlit as st

def roster_tab():
    # Row 1: Dropdowns
    st.subheader("Filters")

    # Sub-Row 1 (Top Sub-Row)
    col1_top, col2_top, col3_top, col4_top, col5_top, col6_top = st.columns(6)

    with col1_top:
        org_filter = st.selectbox("Org", ["SOCCOM", "SOUTHCOM"])

    with col2_top:
        aor_filter = st.selectbox("AOR", ["CENTCOM", "EUCOM"])

    with col3_top:
        duty_station_filter = st.selectbox("Duty Station", ["Al-Udeid", "Bagram"])

    with col4_top:
        deploy_filter = st.selectbox("Deploy", ["Yes", "No"])

    with col5_top:
        branch_filter = st.selectbox("Branch", ["Army", "Navy"])

    with col6_top:
        service_filter = st.selectbox("Service", ["Active", "National Guard"])

    # Sub-Row 2 (Bottom Sub-Row)
    col1_bottom, col2_bottom, col3_bottom, col4_bottom, col5_bottom, col6_bottom = st.columns(6)

    with col1_bottom:
        group_filter = st.selectbox("Group", ["1", "2"])

    with col2_bottom:
        country_filter = st.selectbox("Country", ["Iraq", "Syria"])

    with col3_bottom:
        type_filter = st.selectbox("Type", ["Not sure", "What is this"])

    with col4_bottom:
        waiver_filter = st.selectbox("Waiver", ["Yes", "No"])

    with col5_bottom:
        sof_filter = st.selectbox("SOF", ["Ranger", "SEAL"])

    with col6_bottom:
        ftn_filter = st.selectbox("FTN", ["12345", "67890"])

    # Add space between rows
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)

    # Row 2: Two Columns
    col1, col2 = st.columns([1, 4])  # 20% width for col1, 80% width for col2

    # Column 1: Personnel Counter
    with col1:
        st.subheader("Personnel")
        personnel_count_value = 1500  # Placeholder value (update dynamically)
        st.metric("Personnel Count", personnel_count_value)

    # Column 2: Table (Placeholder)
    with col2:
        st.subheader("Personnel Table")
        # Placeholder for table (customize based on your data)
        table_data = {
            'Name': ['John', 'Jane', 'Bob'],
            'Rank': ['Captain', 'Sergeant', 'Major'],
            'Role': ['Operator', 'Medic', 'Engineer'],
            'Location': ['AOR1', 'AOR2', 'AOR3']
        }
        st.table(table_data)

# This allows your roster.py to be run as a standalone app
if __name__ == "__main__":
    main()