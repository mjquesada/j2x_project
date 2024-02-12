import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

def load_data():
    # Load GeoJSON file with country boundaries
    geojson_path = '../data/countries.geojson'
    gdf_countries = gpd.read_file(geojson_path)

    # Load CSV file with coordinates
    csv_path = './data/Book1.csv'
    df = pd.read_csv(csv_path)

    return gdf_countries, df

def spatial_join(gdf_points, gdf_countries):
    # Perform spatial join
    gdf_points = gpd.GeoDataFrame(gdf_points, geometry=gpd.points_from_xy(gdf_points.lon, gdf_points.lat))
    gdf_points.set_crs(epsg=4326, inplace=True)
    joined_gdf = gpd.sjoin(gdf_points, gdf_countries, how='inner', predicate='within')

    return joined_gdf

def aggregate_data(gdf_countries, joined_gdf):
    # Aggregate data by counting records per country
    aggregated_data = joined_gdf.groupby('ADMIN').size().reset_index(name='RecordCount')

    # Merge aggregated data with country geometries
    gdf_aggregated = pd.merge(gdf_countries, aggregated_data, how='left', left_on='ADMIN', right_on='ADMIN')

    # Fill NaN values with 0 (for countries without records)
    gdf_aggregated['RecordCount'].fillna(0, inplace=True)

    return gdf_aggregated

def filter_data(joined_gdf, selected_countries, selected_agencies, selected_branches, selected_personnel_types):
    # Filter the joined GeoDataFrame based on the selected filters
    filtered_gdf = joined_gdf[
        (joined_gdf['ADMIN'].isin(selected_countries) if selected_countries else (joined_gdf['ADMIN'] == joined_gdf['ADMIN'])) &
        (joined_gdf['Agency'].isin(selected_agencies) if selected_agencies else (joined_gdf['ADMIN'] == joined_gdf['ADMIN'])) &
        (joined_gdf['Branch'].isin(selected_branches) if selected_branches else (joined_gdf['ADMIN'] == joined_gdf['ADMIN'])) &
        (joined_gdf['PersonnelType'].isin(selected_personnel_types) if selected_personnel_types else (joined_gdf['ADMIN'] == joined_gdf['ADMIN']))
    ]

    return filtered_gdf

def get_filters(joined_gdf):
    # Add your logic to get filter values here
    selected_countries = st.sidebar.multiselect('Select countries:', joined_gdf['ADMIN'].unique(), default=[])
    selected_agencies = st.sidebar.multiselect('Select agencies:', joined_gdf['Agency'].unique(), default=[])
    selected_branches = st.sidebar.multiselect('Select branches:', joined_gdf['Branch'].unique(), default=[])
    selected_personnel_types = st.sidebar.multiselect('Select personnel types:', joined_gdf['PersonnelType'].unique(), default=[])

    return selected_countries, selected_agencies, selected_branches, selected_personnel_types

def create_choropleth_map(gdf):
    fig = px.choropleth_mapbox(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color="RecordCount",
        color_continuous_scale="Oranges",
        range_color=(1, 10),
        mapbox_style="carto-positron",
        center={"lat": 0, "lon": 0},
        zoom=1,
        hover_name="ADMIN",
        custom_data=["ADMIN"]
    )

    # Customize hover tooltips
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Record Count: %{z:,.0f}')

    return fig

def main():
    gdf_countries, df = load_data()

    # Create int of len(df) for metric
    total_rows_int = len(df)

    # Display Total PAX Metric
    st.metric(label="Total PAX", value=total_rows_int)

    # Perform spatial join
    joined_gdf = spatial_join(df, gdf_countries)

    # Aggregate data
    gdf_aggregated = aggregate_data(gdf_countries, joined_gdf)

    # Allow for multiple selections and set default to an empty list
    selected_countries = st.sidebar.multiselect('Select countries:', joined_gdf['ADMIN'].unique(), default=[])
    selected_agencies = st.sidebar.multiselect('Select agencies:', joined_gdf['Agency'].unique(), default=[])
    selected_branches = st.sidebar.multiselect('Select branches:', joined_gdf['Branch'].unique(), default=[])
    selected_personnel_types = st.sidebar.multiselect('Select personnel types:', joined_gdf['PersonnelType'].unique(), default=[])

    # Filter Data
    selected_countries, selected_agencies, selected_branches, selected_personnel_types = get_filters(joined_gdf)

    # Filtered Data
    filtered_gdf = filter_data(joined_gdf, selected_countries, selected_agencies, selected_branches, selected_personnel_types)

    # Aggregate Filtered Data
    filtered_aggregated_data = filtered_gdf.groupby('ADMIN').size().reset_index(name='RecordCount')
    filtered_gdf_aggregated = pd.merge(gdf_countries, filtered_aggregated_data, how='left', left_on='ADMIN', right_on='ADMIN')
    filtered_gdf_aggregated['RecordCount'].fillna(0, inplace=True)

    # Merge filtered aggregated data with country geometries
    filtered_gdf_aggregated = pd.merge(gdf_countries, filtered_aggregated_data, how='left', left_on='ADMIN', right_on='ADMIN')

    # Fill NaN values with 0 (for countries without records)
    filtered_gdf_aggregated['RecordCount'].fillna(0, inplace=True)

    # Create choropleth map using plotly.express on filtered data
    fig_filtered = px.choropleth_mapbox(filtered_gdf_aggregated, geojson=filtered_gdf_aggregated.geometry, 
                                         locations=filtered_gdf_aggregated.index,
                                         color="RecordCount", color_continuous_scale="Oranges",
                                         range_color=(1, 10),
                                         mapbox_style="carto-positron", center={"lat": 0, "lon": 0}, zoom=1,
                                         hover_name="ADMIN",  # Specify the column for hover information
                                         custom_data=["ADMIN"]
    )

    # Customize hover tooltips
    fig_filtered.update_traces(hovertemplate='<b>%{hovertext}</b><br>Record Count: %{z:,.0f}')

    # Streamlit Title
    st.title('Force Disposition')

    # Display the filtered map using Streamlit's st.plotly_chart function
    st.plotly_chart(fig_filtered)

    # Display filtered DataFrame
    st.write(f"Filtered Data (Total Records: {len(filtered_gdf)})")
    st.write(filtered_gdf)

    # Display additional information or statistics
    st.sidebar.write(f'Total Records in selection: {len(filtered_gdf)}')

if __name__ == "__main__":
    main()