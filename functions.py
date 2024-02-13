import streamlit as st
from PIL import Image
import numpy as np
import base64
import geopandas as gpd
import plotly.express as px
import pandas as pd
from pandas import DataFrame

# Function to apply custom styling for Row  1 in main.py
def set_background_color_row1(color, padding, title, content, fixed_height=False):
    # Determine the height style based on whether a fixed height is required
    height_style = "height:  230px;" if fixed_height else ""
    return f"""
        <div style="background-color:{color}; padding: {padding}px; border-radius:  5px; {height_style}">
            <h2 style="margin-top:  0; padding-top:  1px;">{title}</h2>
            <p>{content}</p>
        </div>
    """
    

def set_background_color_row2(background_color, padding, component, title_style='', fixed_height=False):
    # Calculate the maximum height for the component
    height_style = f"height: {fixed_height}px;" if fixed_height else ""
    
    # Read the image file and convert it to base64
    with open(component['image_path'], 'rb') as img_file:
        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
    
    # Format the image as a data URL
    image_data_url = f"data:image/png;base64,{base64_image}"
    
    # Construct the HTML for the component with the image
    styled_component = f"""
    <div style="background-color:{background_color}; border-radius:   10px; padding: {padding}px; {height_style}">
        <h2 style="{title_style}">{component['title']}</h2>
        <img src="{image_data_url}" alt="{component['title']}" style="max-width:   100%; height: auto;">
        <p>{component['content']}</p>
    </div>
    """
    return styled_component


def resize_image(image_path, target_height):
    image = Image.open(image_path)
    aspect_ratio = image.width / image.height
    target_width = int(target_height * aspect_ratio)
    resized_image = image.resize((target_width, target_height))
    # Convert the PIL Image object to a NumPy array
    resized_image_np = np.array(resized_image)
    return resized_image_np


def load_data():
    # Load GeoJSON file with country boundaries
    geojson_path = './data/countries.geojson'
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

# def get_filters(joined_gdf):
#     selected_countries = st.sidebar.multiselect('Select countries:', joined_gdf['ADMIN'].unique(), default=[])
#     selected_agencies = st.sidebar.multiselect('Select agencies:', joined_gdf['Agency'].unique(), default=[])
#     selected_branches = st.sidebar.multiselect('Select branches:', joined_gdf['Branch'].unique(), default=[])
#     selected_personnel_types = st.sidebar.multiselect('Select personnel types:', joined_gdf['PersonnelType'].unique(), default=[])

#     return selected_countries, selected_agencies, selected_branches, selected_personnel_types

def get_filters(joined_gdf):
    # Create a horizontal layout for the filter row
    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)

    with filter_col1:
        selected_countries = st.multiselect('AOR:', joined_gdf['AOR'].unique(), default=[])

    with filter_col2:
        selected_agencies = st.multiselect('Country', joined_gdf['Country'].unique(), default=[])

    with filter_col3:
        selected_branches = st.multiselect('Branch:', joined_gdf['Branch'].unique(), default=[])

    with filter_col4:
        selected_personnel_types = st.multiselect('Personnel Types:', joined_gdf['PersonnelType'].unique(), default=[])

    with filter_col5:
        selected_service_skill = st.multiselect('Service Skill:', joined_gdf['ServiceSkill'].unique(), default=[])

    return selected_countries, selected_agencies, selected_branches, selected_personnel_types, selected_service_skill

def create_choropleth_map(data):
    fig = px.choropleth_mapbox(data, geojson=data.geometry, locations=data.index,
                               color="RecordCount", color_continuous_scale="Oranges",
                               range_color=(1, 10),
                               mapbox_style="carto-positron", center={"lat": 0, "lon": 0}, zoom=1,
                               hover_name="ADMIN", custom_data=["ADMIN"])

    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Record Count: %{z:,.0f}')

    return fig


## Luis's Code

def get_session_state():
    session_state = st.session_state
    if not hasattr(session_state, 'reset'):
        session_state.reset = False
    return session_state

def get_total_personnel(df: DataFrame):
    return df.shape[0]

def get_AOR_main_personnel_count(df: DataFrame):
    counts = df["AOR"].value_counts()
    return counts

def get_last_refresh_date(df: DataFrame):
    return df.iloc[len(df.index)-1]["RefreshDate"]

def get_unique_values(df: DataFrame, column_name):
    return df[column_name].unique()

def get_personnel_count_per_column(df: DataFrame, column_name):
    counts = df[column_name].value_counts()
    counts_index = counts.index.tolist()
    counts_values = counts.values.tolist()
    return counts_index, counts_values

# Can do one query at a time
def make_queries(df: DataFrame, filter_dict: dict) -> pd.DataFrame:
    query_string = ""
    for column, values in filter_dict.items():
        # Assuming values is a list, join the values with '|' for OR condition
        query_part = f"{column} == {str(values)[1:-1]}"
        
        # Add the query part to the main query string, 
        # separating with '&' for AND condition
        query_string += query_part + " & "
    
    # Remove the last '&' from the query string
    query_string = query_string[:-3]
    
    filtered_df = df.query(query_string)
    return filtered_df