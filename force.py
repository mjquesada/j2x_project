import streamlit as st
import pandas as pd
from functions import load_data, spatial_join, aggregate_data, filter_data, get_filters, create_choropleth_map

def force_tab():
    # Put your map tab content here
    st.subheader("Force Disposition")

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

    # Components in Column 2
    with col2:
        # Use st.columns to create two columns
        col3, col4 = st.columns(2)

        # AOR Breakdown Component with Bar Chart
        with col3:
            st.write("AOR Breakdown")
            st.bar_chart({"Placeholder": [50, 30, 20]}, height=134, use_container_width=True)  # Placeholder bar chart

        # Breakdown by Branch Component with Bar Chart
        with col4:
            st.write("Breakdown by Branch")
            st.bar_chart({"Placeholder": [30, 40, 10, 20]}, height=134, use_container_width=True)
        
        
    # Filter row
    # st.subheader("Filters")

    # Create a horizontal layout for the filter row
    # filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)

    # with filter_col1:
    #     aor_filter = st.selectbox("AOR", ["Placeholder AOR1", "Placeholder AOR2"])

    # with filter_col2:
    #     country_filter = st.selectbox("Country", ["Placeholder Country1", "Placeholder Country2"])

    # with filter_col3:
    #     branch_filter = st.selectbox("Branch", ["Placeholder Branch1", "Placeholder Branch2"])

    # with filter_col4:
    #     type_filter = st.selectbox("Type", ["Placeholder Type1", "Placeholder Type2"])

    # with filter_col5:
    #     service_skill_filter = st.selectbox("Service Skill", ["Placeholder Skill1", "Placeholder Skill2"])

    # Map Section
    # Load Data
    gdf_countries, df = load_data()

    # Spatial Join
    joined_gdf = spatial_join(df, gdf_countries)
    
    # Filter Data
    selected_countries, selected_agencies, selected_branches, selected_personnel_types, selected_service_skill = get_filters(joined_gdf)

    # Filtered Data
    filtered_gdf = filter_data(joined_gdf, selected_countries, selected_agencies, selected_branches, selected_personnel_types)

    # Aggregate Filtered Data
    filtered_aggregated_data = filtered_gdf.groupby('ADMIN').size().reset_index(name='RecordCount')
    filtered_gdf_aggregated = pd.merge(gdf_countries, filtered_aggregated_data, how='left', left_on='ADMIN', right_on='ADMIN')
    filtered_gdf_aggregated['RecordCount'].fillna(0, inplace=True)

    # Create Choropleth Map
    fig_filtered = create_choropleth_map(filtered_gdf_aggregated)

    # Display the Filtered Map using Streamlit's st.plotly_chart function
    st.plotly_chart(fig_filtered, width=1600)

    # Convert the 'geometry' column to string
    filtered_gdf_display = filtered_gdf.copy()
    filtered_gdf_display['geometry'] = filtered_gdf_display['geometry'].astype(str)

    # Display Filtered DataFrame
    st.write(f"Filtered Data (Total Records: {len(filtered_gdf)})")
    st.dataframe(filtered_gdf_display)
    
    # Display additional information or statistics
    st.sidebar.write(f'Total Records in selection: {len(filtered_gdf)}')

# This allows your map.py to be run as a standalone app
if __name__ == "__main__":
    main()