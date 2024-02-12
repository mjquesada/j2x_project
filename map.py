import streamlit as st
import pandas as pd
from functions import load_data, spatial_join, aggregate_data, filter_data, get_filters, create_choropleth_map

def map_tab():
    # Put your map tab content here
    st.subheader("Map Tab")

    # Layout setup
    col1, col2 = st.columns([1, 3])  # 25% width for col1, 75% width for col2

    # Components in Column 1
    with col1:
        # Placeholder values
        personnel_count = 1000
        country_count = 500


        # Per Stat Component
        st.metric("Personnel Count", personnel_count)

        # Count by TSOC Component
        st.metric("Country Count", country_count)

        # Duty Status Breakout Component with Bar Chart
        st.write("AOR Breakdown")
        st.bar_chart({"Placeholder": [50, 30, 20]}, height=220, use_container_width=True)  # Placeholder bar chart

        # Count by Component Component with Bar Chart
        st.write("Breakdown by Branch")
        st.bar_chart({"Placeholder": [30, 40, 10, 20]}, height=220, use_container_width=True)  # Placeholder bar chart

    # Components in Column 2
    with col2:
        # Filter row
        st.subheader("Filters")

        # Create a horizontal layout for the filter row
        filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)

        with filter_col1:
            aor_filter = st.selectbox("AOR", ["Placeholder AOR1", "Placeholder AOR2"])

        with filter_col2:
            country_filter = st.selectbox("Country", ["Placeholder Country1", "Placeholder Country2"])

        with filter_col3:
            branch_filter = st.selectbox("Branch", ["Placeholder Branch1", "Placeholder Branch2"])

        with filter_col4:
            type_filter = st.selectbox("Type", ["Placeholder Type1", "Placeholder Type2"])

        with filter_col5:
            service_skill_filter = st.selectbox("Service Skill", ["Placeholder Skill1", "Placeholder Skill2"])

        # Map Section
        # Load Data
        gdf_countries, df = load_data()

        # Spatial Join
        joined_gdf = spatial_join(df, gdf_countries)

        # Aggregate Data
        gdf_aggregated = aggregate_data(gdf_countries, joined_gdf)

        # Filter Data
        selected_countries, selected_agencies, selected_branches, selected_personnel_types = get_filters(joined_gdf)

        # Filtered Data
        filtered_gdf = filter_data(joined_gdf, selected_countries, selected_agencies, selected_branches, selected_personnel_types)

        # Aggregate Filtered Data
        filtered_aggregated_data = filtered_gdf.groupby('ADMIN').size().reset_index(name='RecordCount')
        filtered_gdf_aggregated = pd.merge(gdf_countries, filtered_aggregated_data, how='left', left_on='ADMIN', right_on='ADMIN')
        filtered_gdf_aggregated['RecordCount'].fillna(0, inplace=True)

        # Create Choropleth Map
        fig_filtered = create_choropleth_map(filtered_gdf_aggregated)

        # Streamlit Title
        #st.title('Force Disposition')

        # Display the Filtered Map using Streamlit's st.plotly_chart function
        st.plotly_chart(fig_filtered)

    # Display Filtered DataFrame
    st.write(f"Filtered Data (Total Records: {len(filtered_gdf)})")
    st.write(filtered_gdf)

    # Display additional information or statistics
    st.sidebar.write(f'Total Records in selection: {len(filtered_gdf)}')

# This allows your map.py to be run as a standalone app
if __name__ == "__main__":
    main()