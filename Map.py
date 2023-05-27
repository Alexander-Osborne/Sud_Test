import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Add a title to your app
st.title("Map App")

# Define the map location
location = [51.5074, -0.1278]  # London, UK

# Create a folium map object
m = folium.Map(location=location, zoom_start=13)

# Create a marker cluster group
marker_cluster = MarkerCluster()

# Register the click event handler
def on_click(e):
    lat, lon = e.latlng
    marker = folium.Marker([lat, lon], popup='Marker')
    marker.add_to(marker_cluster)

m.add_child(folium.ClickForMarker(callback=on_click))
m.add_child(marker_cluster)

# Render the map in Streamlit
folium_static(m)

# Get the selected marker's coordinates
selected_marker = st.selectbox("Select a marker", [marker.get_popup().replace('\n', '') for marker in marker_cluster._children])

if selected_marker:
    st.write("You selected the marker with coordinates:")
    st.write(selected_marker)
    # Add your Streamlit code for the selected marker
