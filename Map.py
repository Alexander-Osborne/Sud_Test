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
    # Set up the sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Map", "Blank Page"])

    # Render the appropriate page based on the selection
    if page == "Map":
        render_map_page()
    elif page == "Blank Page":
        render_blank_page()

def render_map_page():
    st.title("Map Page")

    # Create a map object with CartoDB Positron basemap
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=12, tiles="CartoDB Positron")

    # Generate random markers with classifications
    markers = []
    classes = ["Class A", "Class B", "Class C"]

    # Create marker clusters for each class
    marker_clusters = {classification: MarkerCluster(name=classification) for classification in classes}

    for _ in range(10):
        latitude = random.uniform(51.4, 51.6)
        longitude = random.uniform(-0.2, 0.2)
        classification = random.choice(classes)

        marker = folium.Marker(location=[latitude, longitude], popup='Random Location', tooltip=classification)

        # Add marker to the corresponding marker cluster
        marker.add_to(marker_clusters[classification])

        markers.append(marker)

    # Add marker clusters to the map
    for marker_cluster in marker_clusters.values():
        marker_cluster.add_to(m)

    # Add layer control to toggle marker clusters
    folium.LayerControl().add_to(m)

    # Render the map
    folium_static(m)

def render_blank_page():
    st.title('SuDS_lab_UK - Wilberforce 001')

    # Define the coordinates for Hull University
    hull_uni_coordinates = (53.77114698979646, -0.36430683784066786)

    # Create a DataFrame with a single row containing Hull University coordinates
    df1 = pd.DataFrame({'lat': [hull_uni_coordinates[0]], 'lon': [hull_uni_coordinates[1]]})

    # Load the image
    image = Image.open('Swale.jpg')

    st.subheader('Image')
    st.image(image, caption='Outfall of Swale')

    # Retrieve secrets from Streamlit Secrets
    secret_key = st.secrets["secret_key"]
    api_key = st.secrets["api_key"]
    station_id = st.secrets["station_id"]

    # Select the number of days
    num_days = st.slider("Select the number of days", min_value=1, max_value=30, value=1)

    # Dropdown menu for lsid_to_filter
    lsid_options = [478072, 123456, 789012]  # Example lsid options, replace with your own values
    lsid_to_filter = st.selectbox("Select the lsid to filter", options=lsid_options)

    if lsid_to_filter:
        # Initialize an empty list to store the data frames for each day
        data_frames = []

        # Loop over the past 'num_days' to retrieve data for each day
        for i in range(num_days):
            # ...

            # Filter the JSON tree based on user input for "lsid"
            filtered_tree = filter_tree(tree, lsid_to_filter)

            # ...

            # Append the extracted data to the list
            data_frames.append(df)

        # Concatenate all the data frames into a single data frame
        combined_df = pd.concat(data_frames)

        # ...

    else:
        st.warning("Please select the lsid value to proceed.")

if __name__ == "__main__":
    main()

