import streamlit as st
import folium
from streamlit_folium import folium_static

# Dummy data for random markers (latitude, longitude, and location name)
random_markers = [
    (37.7749, -122.4194, "San Francisco"),
    (40.7128, -74.0060, "New York"),
    (51.5074, -0.1278, "London"),
    (48.8566, 2.3522, "Paris"),
    (-33.8688, 151.2093, "Sydney"),
]

def handle_click(location_name):
    st.session_state.selected_marker = location_name

def main():
    st.title("Random Marker Map")

    # Create a sidebar for displaying the selected marker name
    st.sidebar.title("Selected Marker")
    if "selected_marker" in st.session_state:
        st.sidebar.write(st.session_state.selected_marker)

    # Create a Folium map centered on a random location
    map_center = random_markers[0][:2]
    m = folium.Map(location=map_center, zoom_start=3)

    # Add markers to the map
    for lat, lon, location_name in random_markers:
        marker = folium.Marker(location=[lat, lon], popup=location_name, tooltip=location_name)
        marker.add_to(m)

    # Handle marker clicks
    for lat, lon, location_name in random_markers:
        folium.Marker(
            location=[lat, lon],
            popup=location_name,
            tooltip=location_name,
            icon=folium.Icon(icon="cloud"),
            ).add_to(m).add_child(folium.Popup(location_name))
    
    # Display the map in Streamlit using folium_static
    folium_static(m)

if __name__ == "__main__":
    main()
