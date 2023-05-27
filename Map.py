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
        marker.add_to(m)
        markers.append((marker, classification))

    # Get unique classes
    unique_classes = list(set([c for _, c in markers]))

    # Checkbox to toggle markers
    selected_classes = st.multiselect("Select Classes", unique_classes, default=unique_classes)

    # Filter and display markers based on selected classes
    for marker, classification in markers:
        if classification in selected_classes:
            marker.add_to(m)

    # Render the map
    folium_static(m)

def render_blank_page():
    st.title("Blank Page")
    # Add content to your blank page here

if __name__ == "__main__":
    main()
