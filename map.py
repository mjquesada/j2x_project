import streamlit as st
import folium
from streamlit_folium import folium_static

def main():
    # Put your map tab content here
    st.title("Map Tab")
    st.write("This is the content of the Map Tab.")

    # Layout setup
    col1, col2 = st.columns([1, 3])  # 25% width for col1, 75% width for col2

    # Components in Column 1
    with col1:
        # Placeholder values
        per_stat_value = 1000
        count_by_tsoc_value = 500
        duty_status_chart = "Placeholder Duty Status Bar Chart"
        count_by_component_chart = "Placeholder Count by Component Bar Chart"

        # Per Stat Component
        st.metric("Per Stat", per_stat_value)

        # Count by TSOC Component
        st.metric("Count by TSOC", count_by_tsoc_value)

        # Duty Status Breakout Component with Bar Chart
        st.subheader("Duty Status Breakout")
        st.bar_chart({"Placeholder": [50, 30, 20]}, use_container_width=True)  # Placeholder bar chart

        # Count by Component Component with Bar Chart
        st.subheader("Count by Component")
        st.bar_chart({"Placeholder": [30, 40, 10, 20]}, use_container_width=True)  # Placeholder bar chart

    # Components in Column 2
    with col2:
        # Filter row
        st.subheader("Filters")
        aor_filter = st.selectbox("AOR", ["Placeholder AOR1", "Placeholder AOR2"])
        country_filter = st.selectbox("Country", ["Placeholder Country1", "Placeholder Country2"])
        branch_filter = st.selectbox("Branch", ["Placeholder Branch1", "Placeholder Branch2"])
        type_filter = st.selectbox("Type", ["Placeholder Type1", "Placeholder Type2"])
        service_skill_filter = st.selectbox("Service Skill", ["Placeholder Skill1", "Placeholder Skill2"])

        # Map row
        st.subheader("Map")
        # Placeholder coordinates for Shanghai
        map_center = [31.2304, 121.4737]
        folium_map = folium.Map(location=map_center, zoom_start=10)
        folium_static(folium_map)

# This allows your map.py to be run as a standalone app
if __name__ == "__main__":
    main()