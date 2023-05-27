import streamlit as st
import folium
from streamlit_folium import folium_static, CustomJSElement
from folium.plugins import MarkerCluster

# Add a title to your app
st.title("Map App")

# Define the map location
location = [51.5074, -0.1278]  # London, UK

# Create a folium map object
m = folium.Map(location=location, zoom_start=13)

# Create a marker cluster group
marker_cluster = MarkerCluster()

# Add a custom JavaScript callback function for click events
callback = '''
function(e){
    var marker = L.marker(e.latlng)
        .bindPopup("Marker")
        .addTo(markerCluster);
}

map.on("click", callback);
'''

# Add the JavaScript callback function to the map using CustomJSElement
CustomJSElement(callback).add_to(m)

# Add the marker cluster group to the map
m.add_child(marker_cluster)

# Render the map in Streamlit
folium_static(m)

# Get the selected marker's coordinates
selected_marker = st.selectbox("Select a marker", [marker.get_popup().replace('\n', '') for marker in marker_cluster._children])

if selected_marker:
    st.write("You selected the marker with coordinates:")
    st.write(selected_marker)
    # Add your Streamlit code for the selected marker
