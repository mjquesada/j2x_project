import streamlit as st
from config import Input_Data, ALL_FILTERS
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from functions import *

def roster_tab():
    # st.set_page_config(layout="wide")
    st.title("Roster")
    df = Input_Data
    state = st.session_state
    
    if "reset_session_state" not in state:
        state.reset_session_state = True

    def reset_session_state():
        state.org = []
        state.aor = []
        state.duty_station = []
        state.deploy = []
        state.branch = []
        state.service = []
        state.group = []
        state.country = []
        state.type = []
        state.waitver = []
        state.sof = []
        state.ftn = []

    # def get_unique_values(df, column_name):
    #     return df[column_name].unique()

    # def get_total_personnel(df):
    #     return len(df)

    # def get_personnel_count_per_column(df, column_name):
    #     return df[column_name].value_counts().index.tolist(), df[column_name].value_counts().values.tolist()

    # def make_queries(df, query):
    #     # Implement your logic to filter DataFrame based on query
    #     return df

    if state.reset_session_state:
        reset_session_state()
        state.reset_session_state = False

    update_queries = []

    # Row 1: Total Personnel and Personnel Count Per Country
    col1, col2 = st.columns((2, 10))

    with col1:
        total = get_total_personnel(df)
        st.metric("Total Personnel", total)

    with col2:
        st.write("PERSONNEL COUNT PER COUNTRY:")
        counts_index, counts_values = get_personnel_count_per_column(df, "Country")
        for index, value in zip(counts_index, counts_values):
            st.write(f"{index} : {value}")

    # Row 2: Filters
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        with st.container():
            state.org = st.multiselect("Org",
                                        options=get_unique_values(df, ALL_FILTERS["Organization"]),
                                        key="Organization")

        with st.container():
            state.aor = st.multiselect("AOR",
                                        options=get_unique_values(df, ALL_FILTERS["AOR"]),
                                        key="AOR")

    with col2:
        with st.container():
            state.duty_station = st.multiselect("Location",
                                        options=get_unique_values(df, ALL_FILTERS["CurrentLocation"]),
                                        key="CurrentLocation")

        with st.container():
            state.deploy = st.multiselect("Deploy",
                                        options=get_unique_values(df, ALL_FILTERS["Deploy"]),
                                        key="Deploy")

    with col3:
        with st.container():
            state.branch = st.multiselect("Branch",
                                        options=get_unique_values(df, ALL_FILTERS["Branch"]),
                                        key="Branch")

        with st.container():
            state.service = st.multiselect("Service",
                                        options=get_unique_values(df, ALL_FILTERS["ServiceSkill"]),
                                        key="ServiceSkill")

    with col4:
        with st.container():
            state.group = st.multiselect("Group",
                                        options=get_unique_values(df, ALL_FILTERS["Group"]),
                                        key="Group")

        with st.container():
            state.country = st.multiselect("Country",
                                        options=get_unique_values(df, ALL_FILTERS["Country"]),
                                        key="Country")

    with col5:
        with st.container():
            state.type = st.multiselect("Type",
                                        options=get_unique_values(df, ALL_FILTERS["PersonnelType"]),
                                        key="PersonnelType")

        with st.container():
            state.waiver = st.multiselect("Waiver",
                                        options=get_unique_values(df, ALL_FILTERS["Waiver"]),
                                        key="Waiver")

    with col6:
        with st.container():
            state.sof = st.multiselect("SOF",
                                        options=get_unique_values(df, ALL_FILTERS["SOF"]),
                                        key="SOF")

        with st.container():
            state.ftn = st.multiselect("FTN",
                                        options=get_unique_values(df, ALL_FILTERS["FTN"]),
                                        key="FTN")
            
    
    # Row 4: Buttons
    update_btn, reset_btn = st.columns(2)

    with update_btn:
        update_btn = st.button(label="Update Filters", type="primary")

    with reset_btn:
        reset_btn = st.button(label="Clear Filters", type="secondary")
        
    if reset_btn:
        reset_session_state()     

    # Grab the selected filters to filter the displayed dataframe
    if update_btn:
        if state.org:
            update_queries.append({"Organization": [state.org]})
        if state.aor:
            update_queries.append({"AOR": [state.aor]})
        if state.duty_station:
            update_queries.append({"AOR": [state.duty_station]})
        if state.deploy:
            update_queries.append({"Country": [state.deploy]})
        if state.branch:
            update_queries.append({"Agency": [state.branch]})
        if state.service:
            update_queries.append({"Type": [state.service]})
        if state.group:
            update_queries.append({"Location": [state.group]})
        if state.country:
            update_queries.append({"State": [state.country]})
        if state.type:
            update_queries.append({"Branch": [state.type]})
        if state.waiver:
            update_queries.append({"State": [state.waiver]})
        if state.sof:
            update_queries.append({"State": [state.sof]})
        if state.ftn:
            update_queries.append({"FTN": [state.ftn]})

    if update_queries:
        df = filter_df(df, update_queries)

    # Row 3: Roster Table
    st.write("Roster Table:")
    st.dataframe(df)

# This allows your roster.py to be run as a standalone app
if __name__ == "__main__":
    main()