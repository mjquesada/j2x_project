import streamlit as st
from PIL import Image
import numpy as np
import base64
import geopandas as gpd
import plotly.express as px
import pandas as pd

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

def get_filters(joined_gdf):
    # Add your logic to get filter values here
    selected_countries = st.sidebar.multiselect('Select countries:', joined_gdf['ADMIN'].unique(), default=[])
    selected_agencies = st.sidebar.multiselect('Select agencies:', joined_gdf['Agency'].unique(), default=[])
    selected_branches = st.sidebar.multiselect('Select branches:', joined_gdf['Branch'].unique(), default=[])
    selected_personnel_types = st.sidebar.multiselect('Select personnel types:', joined_gdf['PersonnelType'].unique(), default=[])

    return selected_countries, selected_agencies, selected_branches, selected_personnel_types

def create_choropleth_map(data):
    fig = px.choropleth_mapbox(data, geojson=data.geometry, locations=data.index,
                               color="RecordCount", color_continuous_scale="Oranges",
                               range_color=(1, 10),
                               mapbox_style="carto-positron", center={"lat": 0, "lon": 0}, zoom=1,
                               hover_name="ADMIN", custom_data=["ADMIN"])

    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Record Count: %{z:,.0f}')

    return fig