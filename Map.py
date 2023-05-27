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
        markers.append((marker, classification))

    # Get unique classes
    unique_classes = list(set([c for _, c in markers]))

    # Create feature groups for each class
    feature_groups = {classification: folium.FeatureGroup(name=classification) for classification in unique_classes}

    # Add markers to the corresponding feature group
    for marker, classification in markers:
        marker.add_to(feature_groups[classification])

    # Add feature groups to the map
    for feature_group in feature_groups.values():
        feature_group.add_to(m)

    # Checkbox to toggle markers
    selected_classes = st.multiselect("Select Classes", unique_classes, default=unique_classes)

    # Render the map
    folium_static(m)

    # Execute JavaScript to control marker visibility based on selected classes
    visible_classes = [f"'.leaflet-pane .leaflet-feature-group[name=\"{c}\"]'" for c in selected_classes]
    visible_classes_js = " + ".join(visible_classes)
    hide_js = f"document.querySelectorAll({visible_classes_js}).forEach(function(g) {{ g.style.display = 'none'; }});"
    show_js = f"document.querySelectorAll(':not({visible_classes_js})').forEach(function(g) {{ g.style.display = 'initial'; }});"
    script = f"<script>{hide_js}{show_js}</script>"
    st.components.v1.html(script, height=0)

def render_blank_page():
    st.title("Blank Page")
    # Add content to your blank page here

if __name__ == "__main__":
    main()
