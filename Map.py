import streamlit as st
import folium
from streamlit_folium import folium_static
import random

def main():
    # Set up the sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Map", "Blank Page"])

    # Render the appropriate page based on the selection
    if page == "Map":
        render_map_page()
    elif page == "Blank Page":
        render_blank_page()

def render_map_page():
    st.title("Map Page")

    # Create a map object
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)  # London coordinates as an example

    # Generate random markers with classifications
    markers = []
    classes = ["Class A", "Class B", "Class C"]

    for _ in range(10):
        latitude = random.uniform(51.4, 51.6)
        longitude = random.uniform(-0.2, 0.2)
        classification = random.choice(classes)

        marker = folium.Marker(location=[latitude, longitude], popup='Random Location', tooltip=classification)

        # Create a feature group for each class
        feature_group = folium.FeatureGroup(name=classification)
        marker.add_to(feature_group)
        feature_group.add_to(m)

        markers.append((marker, feature_group))

    # Add layer control to toggle markers
    layer_control = folium.plugins.GroupedLayerControl(collapsed=False)
    layer_control.add_to(m)

    # Render the map
    folium_static(m)

    # Checkbox to toggle markers
    selected_classes = st.multiselect("Select Classes", classes, default=classes)

    # Filter and display markers based on selected classes
    for marker, feature_group in markers:
        if feature_group.name in selected_classes:
            feature_group.add_to(m)
        else:
            feature_group.get_root().remove_child(feature_group)

def render_blank_page():
    st.title("Blank Page")
    # Add content to your blank page here

if __name__ == "__main__":
    main()
