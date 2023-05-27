import streamlit as st
import streamlit.components.v1 as components

# Add a title to your app
st.title("Map App")

# Define the map location
location = [51.5074, -0.1278]  # London, UK

# Add the map to your app
map_html = """
<div id="map" style="width: 100%; height: 500px;"></div>
<script>
var map = L.map('map').setView([51.5074, -0.1278], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

L.marker([51.5074, -0.1278]).addTo(map)
    .bindPopup('Marker 1');

L.marker([51.5072, -0.1276]).addTo(map)
    .bindPopup('Marker 2');

</script>
"""
components.html(map_html, height=600)

# Add a sub-window for the selected marker
selected_marker = st.selectbox("Select a marker", ["Marker 1", "Marker 2"])

if selected_marker == "Marker 1":
    st.write("You selected Marker 1. Add your Streamlit code here.")
    # Add your Streamlit code for Marker 1
elif selected_marker == "Marker 2":
    st.write("You selected Marker 2. Add your Streamlit code here.")
    # Add your Streamlit code for Marker 2
