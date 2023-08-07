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

# Create a Streamlit session state
if "selected_marker" not in st.session_state:
    st.session_state.selected_marker = None

def handle_click(location_name):
    st.session_state.selected_marker = location_name
    st.experimental_rerun()

def main():
    st.title("Random Marker Map")
    
    # Create a Folium map centered on a random location
    map_center = random_markers[0][:2]
    m = folium.Map(location=map_center, zoom_start=3)

    # Add markers to the map
    for lat, lon, location_name in random_markers:
        marker = folium.Marker(location=[lat, lon], popup=location_name, tooltip=location_name)
        marker.add_to(m)

    # Display the map in Streamlit using folium_static
    folium_static(m)

    # Show the selected marker name on a new page
    if st.session_state.selected_marker:
        st.title("Selected Marker")
        st.write(f"You clicked on the marker in {st.session_state.selected_marker}.")

if __name__ == "__main__":
    main()
