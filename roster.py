import streamlit as st
from config import DF, ALL_FILTERS
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from functions import *

def roster_tab():
    # Row 1: Dropdowns
    # st.subheader("Roster Tab")

    # # Sub-Row 1 (Top Sub-Row)
    # col1_top, col2_top, col3_top, col4_top, col5_top, col6_top = st.columns(6)

    # with col1_top:
    #     org_filter = st.selectbox("Org", ["SOCCOM", "SOUTHCOM"])

    # with col2_top:
    #     aor_filter = st.selectbox("AOR", ["CENTCOM", "EUCOM"])

    # with col3_top:
    #     duty_station_filter = st.selectbox("Duty Station", ["Al-Udeid", "Bagram"])

    # with col4_top:
    #     deploy_filter = st.selectbox("Deploy", ["Yes", "No"])

    # with col5_top:
    #     branch_filter = st.selectbox("Branch", ["Army", "Navy"])

    # with col6_top:
    #     service_filter = st.selectbox("Service", ["Active", "National Guard"])

    # # Sub-Row 2 (Bottom Sub-Row)
    # col1_bottom, col2_bottom, col3_bottom, col4_bottom, col5_bottom, col6_bottom = st.columns(6)

    # with col1_bottom:
    #     group_filter = st.selectbox("Group", ["1", "2"])

    # with col2_bottom:
    #     country_filter = st.selectbox("Country", ["Iraq", "Syria"])

    # with col3_bottom:
    #     type_filter = st.selectbox("Type", ["Not sure", "What is this"])

    # with col4_bottom:
    #     waiver_filter = st.selectbox("Waiver", ["Yes", "No"])

    # with col5_bottom:
    #     sof_filter = st.selectbox("SOF", ["Ranger", "SEAL"])

    # with col6_bottom:
    #     ftn_filter = st.selectbox("FTN", ["12345", "67890"])
        
    # # Sub-Row 3
    # col1_bottom, col2_bottom, col3_bottom, col4_bottom, col5_bottom = st.columns(5)

    # # Add space between rows
    # st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)

    # # Row 2: Two Columns
    # col1, col2 = st.columns([1, 4])  # 20% width for col1, 80% width for col2

    # # Column 1: Personnel Counter
    # with col1:
    #     personnel_count_value = 1500  # Placeholder value (update dynamically)
    #     st.metric("Personnel Count", personnel_count_value)
        
    #     country_count = 2500  # Placeholder value (update dynamically)
    #     st.metric("Country Count", country_count)

    # # Column 2: Table (Placeholder)
    # with col2:
    #     st.write("Personnel Table")
    #     # Placeholder for table (customize based on your data)
    #     table_data = {
    #         'Name': ['John', 'Jane', 'Bob'],
    #         'Rank': ['Captain', 'Sergeant', 'Major'],
    #         'Role': ['Operator', 'Medic', 'Engineer'],
    #         'Location': ['AOR1', 'AOR2', 'AOR3']
    #     }
    #     st.table(table_data)
        
## Luis's Code

    # st.set_page_config(layout="wide")
    st.title("Roster")
    df = DF


    state = get_session_state()

    def reset_session_state():
        state.org_group = []
        state.group = []
        state.aor = []
        state.country = []
        state.duty_status = []
        state.type = []
        state.deployability = []
        state.nondeploy = []
        state.branch = []
        state.ftn = ""

    update_queries = []
    col1, col2 = st.columns((1.5,7))

    with col1:
        
        with st.container():
            total = get_total_personnel(df)
            st.write(f"TOTAL PERSONNEL COUNT: {total}")
        
        with st.container():
            st.write("PERSONNEL COUNT PER COUNTRY: ")
            counts_index, counts_values = get_personnel_count_per_column(df, "Country")
            for index, value in zip(counts_index, counts_values):
                st.write(f"{index} : {value} ")

        
    with col2:

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            with st.container():
                state.org_group =  st.multiselect("Org Group", 
                            options=get_unique_values(DF,ALL_FILTERS["Org Group"]),
                            key="OrgGroup")
                
                
            with st.container():
                state.group = st.multiselect("Group", 
                            options=get_unique_values(DF,ALL_FILTERS["Group"]),
                            key="Group")

        with col2:
            with st.container():
                state.aor = st.multiselect("AOR", 
                            options=get_unique_values(DF,ALL_FILTERS["AOR"]),
                            key="AOR")
                
            with st.container():
                state.country = st.multiselect("Country", 
                            options=get_unique_values(DF,ALL_FILTERS["Country"]),
                            key="Country")

        with col3:
            with st.container():
                state.duty_status = st.multiselect("Duty Status", 
                            options=get_unique_values(DF,ALL_FILTERS["Duty Status"]),
                            key="Duty Status")
                
            with st.container():
                state.type = st.multiselect("Type", 
                            options=get_unique_values(DF,ALL_FILTERS["Type"]),
                            key="Type")

        with col4:
            with st.container():
                state.deployability = st.multiselect("Deployability", 
                            options=get_unique_values(DF,ALL_FILTERS["Deployability"]),
                            key="Deployability")
                
            with st.container():
                state.nondeploy = st.multiselect("Nondeploy", 
                            options=get_unique_values(DF,ALL_FILTERS["Nondeploy"]),
                            key="Nondeploy")
        with col5:
            with st.container():
                state.branch = st.multiselect("Branch", 
                            options=get_unique_values(DF,ALL_FILTERS["Branch"]),
                            key="Branch")
                
            with st.container():
                ftn = st.text_input(label="FTN?", key="FTN")
                
        with col6:
            with st.container():
                state.service_skills = st.multiselect("Service Skill", 
                            options=get_unique_values(DF,ALL_FILTERS["Service Skill"]))
                
            with st.container():
                update_btn = st.button(label="Update Filters", type="secondary")
                reset_btn = st.button(label="Clear Filters", type="primary")

    
    if reset_btn:
        reset_session_state()
        df = DF               

    if state.org_group:
        st.write(state.org_group)
    if state.group:
        st.write(state.group)

    # Grab the selected filters to filter the displayed dataframe
    if update_btn:
        if state.org_group:
            update_queries.append({"Organization": [state.org_group]})
        if state.group:
            update_queries.append({"OrgAbbreviation": [state.group]})
        if state.aor:
            update_queries.append({"AOR": [state.aor]})
        if state.country:
            update_queries.append({"Country": [state.country]})
        if state.duty_status:
            update_queries.append({"Agency": [state.duty_status]})
        if state.type:
            update_queries.append({"Type": [state.type]})
        if state.deployability:
            update_queries.append({"Location": [state.deployability]})
        if state.nondeploy:
            update_queries.append({"State": [state.nondeploy]})
        if state.branch:
            update_queries.append({"Branch": [state.branch]})
        if ftn:
            update_queries.append({"FTN": [state.ftn]})


    if update_queries:
        # df = make_queries(DF, update_queries)
        if len(update_queries) == 1:
            df = make_queries(DF, update_queries[0])
        else:
            df1 = pd.DataFrame()
            for query in update_queries:
                if df1.empty:
                    df1 = make_queries(DF, query)
                    df = df1
                else:
                    df1 = make_queries(DF, query)
                    df = pd.concat([df,df1], ignore_index=True)
        
    st.dataframe(df)

# This allows your roster.py to be run as a standalone app
if __name__ == "__main__":
    main()