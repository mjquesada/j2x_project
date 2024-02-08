import streamlit as st
from PIL import Image
import numpy as np
import base64

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

    
# def set_background_color_row2(background_color, padding, component, title_style='', fixed_height=False):
#     # Calculate the maximum height for the image to fit within the component
#     max_height = '200px' if fixed_height else 'auto'
    
#     # Read the image file and convert it to base64
#     with open(component['image_path'], 'rb') as img_file:
#         base64_image = base64.b64encode(img_file.read()).decode('utf-8')
    
#     # Format the image as a data URL
#     image_data_url = f"data:image/png;base64,{base64_image}"
    
#     # Construct the HTML for the component with the image
#     styled_component = f"""
#     <div style="background-color:{background_color}; border-radius:   10px; padding: {padding}px; height: {max_height}px;">
#         <h2 style="{title_style}">{component['title']}</h2>
#         <img src="{image_data_url}" alt="{component['title']}" style="max-width:   100%; height: auto;">
#         <p>{component['content']}</p>
#     </div>
#     """
#     return styled_component
    
# Function to apply custom styling for Row 2 with st.image in main.py
# def set_background_color_row2(color, padding, component, fixed_height=True):
#     height_style = "height: 300px;" if fixed_height else ""
#     st.image(
#         component["image_path"],
#         caption=component["title"],
#         use_column_width=True,  # Adjust as needed
#         width=100,
#         output_format="JPEG",  # Adjust based on image format
#     )
#     st.markdown(f"""
#         <div style="background-color:{color}; padding: {padding}px; border-radius: 10px; {height_style}">
#             <h2 style="font-size: 16px;">{component['title']}</h2>
#             <p>{component['content']}</p>
#         </div>
#     """, unsafe_allow_html=True)
    
# def resize_image(image_path, target_height):
#     image = Image.open(image_path)
#     aspect_ratio = image.width / image.height
#     target_width = int(target_height * aspect_ratio)
#     resized_image = image.resize((target_width, target_height))
#     return resized_image


def resize_image(image_path, target_height):
    image = Image.open(image_path)
    aspect_ratio = image.width / image.height
    target_width = int(target_height * aspect_ratio)
    resized_image = image.resize((target_width, target_height))
    # Convert the PIL Image object to a NumPy array
    resized_image_np = np.array(resized_image)
    return resized_image_np
