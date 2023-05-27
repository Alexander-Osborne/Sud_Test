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

# Add a custom JavaScript callback function for click events
callback = '''
function(e){
    var popup = L.popup()
        .setLatLng(e.latlng)
        .setContent("Marker")
        .openOn(map);

    var marker = L.marker(e.latlng)
        .addTo(markerCluster);

    marker.bindPopup(popup);
}
'''

# Add the JavaScript callback function to the map
m.add_child(folium.Element(callback))

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
