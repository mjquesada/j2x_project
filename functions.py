import streamlit as st

# Function to apply custom styling for Row 1 in main.py
def set_background_color_row1(color, padding, title, content, fixed_height=False):
    height_style = "height: 200px;" if fixed_height else ""
    return f"""
        <div style="background-color:{color}; padding: {padding}px; border-radius: 5px; {height_style}">
            <h2 style="margin-top: 0; padding-top: 1px;">{title}</h2>
            <p>{content}</p>
        </div>
    """
    
# Function to apply custom styling for Row 2 with st.image in main.py
def set_background_color_row2(color, padding, component, fixed_height=True):
    height_style = "height: 300px;" if fixed_height else ""
    st.image(
        component["image_path"],
        caption=component["title"],
        use_column_width=True,  # Adjust as needed
        width=100,
        output_format="JPEG",  # Adjust based on image format
    )
    st.markdown(f"""
        <div style="background-color:{color}; padding: {padding}px; border-radius: 10px; {height_style}">
            <h2 style="font-size: 16px;">{component['title']}</h2>
            <p>{component['content']}</p>
        </div>
    """, unsafe_allow_html=True)