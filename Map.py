import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster, ClickCallback

# Add a title to your app
st.title("Map App")

# Define the map location
location = [51.5074, -0.1278]  # London, UK

# Create a folium map object
m = folium.Map(location=location, zoom_start=13)

# Create a FastMarkerCluster group
marker_cluster = FastMarkerCluster()

# Register the click event handler
def on_click(event, **kwargs):
    lat, lon = event["latlng"]
    marker = folium.Marker([lat, lon], popup='Marker')
    marker_cluster.add_child(marker)

click_callback = ClickCallback(callback=on_click)
m.add_child(click_callback)

m.add_child(marker_cluster)
m.add_child(folium.LatLngPopup())

# Render the map in Streamlit
folium_static(m)

# Get the selected marker's coordinates
selected_marker = st.selectbox("Select a marker", marker_cluster._children.keys(), format_func=lambda x: x.get_name() if x else None)

if selected_marker:
    st.write("You selected the marker with coordinates:")
    st.write(f"Latitude: {selected_marker.location[0]}")
    st.write(f"Longitude: {selected_marker.location[1]}")
    # Add your Streamlit code for the selected marker
