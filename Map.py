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

# Add markers to the map
marker1 = folium.Marker([51.5074, -0.1278], popup='Marker 1')
marker2 = folium.Marker([51.5072, -0.1276], popup='Marker 2')

marker_cluster.add_child(marker1)
marker_cluster.add_child(marker2)

# Add the marker cluster group to the map
m.add_child(marker_cluster)

# Render the map in Streamlit using st.map()
st.map(m)

# Get the selected marker's coordinates
selected_marker = st.selectbox("Select a marker", ["Marker 1", "Marker 2"])

if selected_marker == "Marker 1":
    st.write("You selected Marker 1. Add your Streamlit code here.")
