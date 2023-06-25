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
            icon_path = icon_directory + 'default_icon.png'  # Replace 'default_icon.png' with your default icon path

        # Create a custom icon
        custom_icon = folium.CustomIcon(icon_image=icon_path, icon_size=(30, 30))
        additional_details = row['additional_details']
        # Construct the tooltip content with the name and thumbnail image
        thumbnail_html = f'<img src="{image_url}" alt="Thumbnail" width="300">'
        tooltip_content = f"<b>{name}</b><br>{thumbnail_html}<br><i>{additional_details}</i>"

        # Create the popup content with the name and larger image
        popup_html = f'<h4>{name}</h4><img src="{image_url}" alt="Image" width="200"><p>{additional_details}</p>'
        popup = folium.Popup(html=popup_html, max_width=400)

        def on_marker_click(e):
            session_state.name = name
            st.experimental_rerun()

        marker = folium.Marker(location=[latitude, longitude], popup=popup, tooltip=tooltip_content, icon=custom_icon)
        marker.add_to(marker_clusters[classification])

        marker.add_child(folium.ClickForMarker(popup, callback=on_marker_click))

    # Add marker clusters to the map
    for marker_cluster in marker_clusters.values():
        marker_cluster.add_to(m)

    # Add layer control to toggle marker clusters
    folium.LayerControl().add_to(m)

    # Render the map
    folium_static(m)

    if session_state.name:
        st.sidebar.success(f"Name '{session_state.name}' copied to clipboard!")

if __name__ == '__main__':
    main()
