import streamlit as st
import streamlit.components.v1 as components
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

class SessionState:
    def __init__(self):
        self.name = None

def main():
    session_state = SessionState()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Location Viewer", "Data Viewer"])

    if page == "Location Viewer":
        render_map_page(session_state)
    elif page == "Data Viewer":
        render_blank_page()

def render_map_page(session_state):
    st.markdown('<h1 style="text-align: center;">SuDS<span style="font-style: italic;">lab</span> UK</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px;">A Living Lab for Sustainable Drainage</p>', unsafe_allow_html=True)

    paragraph = """
    SuDS*lab* UK provides a unique research tool for the academic study of sustainable drainage. Increasing our understanding of how system components interact to influence the overall hydrological performance of a small catchment, as well as allowing us to examine in detail the effect of soil substrates in water attenuation. We share data from SuDS*lab* UK openly to help and encourage others to innovate new and better sustainable drainage solutions.
    """

    st.markdown(paragraph)


    # Load markers data from CSV
    markers_data = pd.read_csv('markers.csv')  # Replace 'markers.csv' with your CSV file path

    # Coordinates of Hull
    hull_coordinates = (53.7701, -0.3672)

    m = folium.Map(location=hull_coordinates, zoom_start=9, tiles="openstreetmap", max_zoom=19)

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
        elif classification == 'Weather':
            icon_path = icon_directory + 'Weather_Icon.png'
        else:
            # Use a default icon if no matching classification is found
            icon_path = icon_directory + 'default_icon.png'  #
