import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import random
import hmac
import hashlib
from urllib.parse import urlencode
import time
import requests
import json
import pandas as pd
from PIL import Image
import base64

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Location Viewer", "Data Viewer"])

    if page == "Location Viewer":
        render_map_page()
    elif page == "Data Viewer":
        render_blank_page()

def render_map_page():
    st.title("Map Page")

    # Load markers data from CSV
    markers_data = pd.read_csv('markers.csv')  # Replace 'markers.csv' with your CSV file path

    # Coordinates of Hull
    hull_coordinates = (53.7701, -0.3672)

    m = folium.Map(location=hull_coordinates, zoom_start=12, tiles="openstreetmap", max_zoom=19)

    marker_clusters = {}

    # Create marker clusters for each class
    for classification in markers_data['classification'].unique():
        marker_clusters[classification] = MarkerCluster(name=classification)

    # Define the path to the directory containing custom marker icons
    icon_directory = 'marker_icons/'

    # Add markers to the map
    for _, row in markers_data.iterrows():
        latitude = row['latitude']
        longitude = row['longitude']
        classification = row['classification']
        name = row['name']
        image_url = row['image_url']  # Add the column name from your CSV that contains the image URL

        # Construct the path to the custom marker icon for the classification
        if classification == 'Swale':
            icon_path = icon_directory + 'Swale_Icon.png'
        elif classification == 'Planter':
            icon_path = icon_directory + 'Planter_Icon.png'
        else:
            # Use a default icon if no matching classification is found
            icon_path = icon_directory + 'default_icon.png'  # Replace 'default_icon.png' with your default icon path

        # Create a custom icon
        custom_icon = folium.CustomIcon(icon_image=icon_path, icon_size=(30, 30))
        additional_details = row['additional_details']
        # Construct the tooltip content with the name and thumbnail image
        thumbnail_html = f'<img src="{image_url}" alt="Thumbnail" width="300">'
        tooltip_content = f"<b>{name}</b><br>{thumbnail_html}<br><i>{additional_details}</i>"

        # Create the popup content with the name and larger image
        popup_html = f'<h4>{name}</h4><img src="{image_url}" alt="Image" width="300"><p>{additional_details}</p>'
        popup = folium.Popup(html=popup_html, max_width=400)

        marker = folium.Marker(location=[latitude, longitude], popup=popup, tooltip=tooltip_content, icon=custom_icon)
        marker.add_to(marker_clusters[classification])

    # Add marker clusters to the map
    for marker_cluster in marker_clusters.values():
        marker_cluster.add_to(m)

    # Add layer control to toggle marker clusters
    folium.LayerControl().add_to(m)

    # Render the map
    folium_static(m)

    
def render_blank_page():
    st.title('SuDS_lab_UK - Data Viewer')

    # Define the coordinates for Hull University
    hull_uni_coordinates = (53.77114698979646, -0.36430683784066786)

    # Create a DataFrame with a single row containing Hull University coordinates
    df1 = pd.DataFrame({'lat': [hull_uni_coordinates[0]], 'lon': [hull_uni_coordinates[1]]})


    # Retrieve secrets from Streamlit Secrets
    secret_key = st.secrets["secret_key"]
    api_key = st.secrets["api_key"]
    station_id = st.secrets["station_id"]

    # Select the number of days
    num_days = st.slider("Select the number of days of data to view", min_value=1, max_value=30, value=1)

    lsid_options = {
        478072: "Wilberforce 001",
        478073: "Wilberforce 002",
        570517: "Fenner's Field 001",
        570522: "Fenner's Field 002",
        599263: "Newland Science Park"
    }  # Example lsid options with corresponding titles

    lsid_to_filter = st.selectbox("Select Sensor ID", options=list(lsid_options.keys()), format_func=lambda x: lsid_options[x])

    if lsid_to_filter:
        # Update the page title based on the selected lsid
        st.title(lsid_options[lsid_to_filter])

        # Rest of the code...
        # Replace the rest of the code with your existing code block

    else:
        st.warning("Please enter the lsid value to proceed.")

if __name__ == "__main__":
    main()
