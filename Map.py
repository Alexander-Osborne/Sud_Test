import streamlit as st
import folium
import pandas as pd
from folium import features
from streamlit_folium import folium_static

def create_map():
    # Create the map object with the CartoDB Positron tileset and set the initial zoom location to England
    map = folium.Map(location=[53.0, -1.0], zoom_start=6, tiles='CartoDB Positron')

    # Read marker information from the CSV file
    markers_df = pd.read_csv("markers.csv")

    # Create markers for each row in the CSV with custom icons
    for index, row in markers_df.iterrows():
        # Create a custom marker icon with an image
        icon_image = row["marker_icon"]  # Column name in the CSV for marker icon image path
        icon = features.CustomIcon(icon_image, icon_size=(30, 30))

        # Define the JavaScript code to be executed on marker click
        js_code = f'''
            var checkbox = document.getElementById('checkbox{index}');
            checkbox.checked = true;
            
            // Add your code here to run when the marker is clicked
            // Import the necessary libraries and execute the desired code
            import hmac
            import hashlib
            from urllib.parse import urlencode
            import time
            import requests
            import json
            import pandas as pd
            from PIL import Image
            
            st.title('SuDS'' _lab_ '' UK - Wilberforce 001')
            
            # Rest of your code...
        '''

        # Create a popup with checkbox and JavaScript code
        popup_content = f'''
            <input type="checkbox" id="checkbox{index}" onclick="{js_code}">Click Me
        '''

        # Add the marker to the map with the custom popup
        marker = folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_content,
            tooltip=row["name"],
            icon=icon
        ).add_to(map)

    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

if __name__ == "__main__":
    main()
