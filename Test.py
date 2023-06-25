import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

def main():
    render_map_page()

def render_map_page():
    st.markdown('<h1 style="text-align: center;">SuDS<span style="font-style: italic;">lab</span> UK</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px;">Location Viewer</p>', unsafe_allow_html=True)

    # Load markers data from CSV
    markers_data = pd.read_csv('markers.csv')  # Replace 'markers.csv' with your CSV file path

    # Initialize the map HTML template
    map_html = """
    <div id="map" style="height: 500px;"></div>
    <script>
        // Initialize the map
        var map = L.map('map').setView([53.7701, -0.3672], 9);

        // Add the OpenStreetMap tiles layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Create marker clusters
        var markerClusters = L.markerClusterGroup();

        // Iterate over the markers data
        {marker_js}

        // Add marker clusters to the map
        map.addLayer(markerClusters);
    </script>
    """

    # Generate the JavaScript code for markers and marker clusters
    marker_js = ""
    for _, row in markers_data.iterrows():
        latitude = row['latitude']
        longitude = row['longitude']
        classification = row['classification']
        name = row['name']
        image_url = row['image_url']  # Add the column name from your CSV that contains the image URL

        marker_js += f"""
        var markerIcon = L.icon({{ iconUrl: '{get_icon_url(classification)}', iconSize: [30, 30] }});

        var popupContent = "<b>{name}</b><br><img src='{image_url}' alt='Image' width='200'>";
        var marker = L.marker([{latitude}, {longitude}], {{ icon: markerIcon }}).bindPopup(popupContent);

        markerClusters.addLayer(marker);
        """

    # Replace the marker_js placeholder in the map HTML template
    map_html = map_html.replace("{marker_js}", marker_js)

    # Render the map using Leaflet
    html(map_html, height=600)

def get_icon_url(classification):
    icon_directory = 'marker_icons/'

    if classification == 'Swale':
        return icon_directory + 'Swale_Icon.png'
    elif classification == 'Planter':
        return icon_directory + 'Planter_Icon.png'
    elif classification == 'Weather':
        return icon_directory + 'Weather_Icon.png'
    else:
        return icon_directory + 'default_icon.png'

if __name__ == "__main__":
    main()
