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

def main():
    render_data_viewer_page()

def render_data_viewer_page():
    # Load and display the logo image
    logo_image = Image.open("Logo.png")
    st.image(logo_image, use_column_width=True)

    # Define the coordinates for Hull University
    hull_uni_coordinates = (53.77114698979646, -0.36430683784066786)

    # Create a DataFrame with a single row containing Hull University coordinates
    df1 = pd.DataFrame({'lat': [hull_uni_coordinates[0]], 'lon': [hull_uni_coordinates[1]]})


    # Retrieve secrets from Streamlit Secrets
    secret_key = st.secrets["secret_key"]
    api_key = st.secrets["api_key"]
    station_id = st.secrets["station_id"]

    
    # Define the HTML code for the map
   map_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>UK Map with Markers</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.css" />
        <style>
            #map { height: 400px; }
            .popup-message {
                position: absolute;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                background-color: rgba(0, 0, 0, 0.8);
                color: #fff;
                padding: 10px;
                border-radius: 5px;
                z-index: 999;
                transition: opacity 0.5s;
            }
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div id="popup-message"></div>
    
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/papaparse@5.3.0"></script>
        <script>
            function copyToClipboard(elementId) {
                var copyText = document.getElementById(elementId).textContent;
                navigator.clipboard.writeText(copyText);
                alert("Copied the sensor ID: " + copyText);
            }
    
            var map = L.map('map').setView([53.771552, -0.36425564], 15);
    
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
                maxZoom: 18,
            }).addTo(map);
    
            fetch('https://raw.githubusercontent.com/Alexander-Osborne/Sud_Test/main/markers.csv')
                .then(response => response.text())
                .then(data => {
                    var parsedData = Papa.parse(data, { header: true }).data;
    
                    var iconBaseUrl = 'https://raw.githubusercontent.com/Alexander-Osborne/Sud_Test/main/marker_icons/';
    
                    parsedData.forEach(row => {
                        var lat = parseFloat(row.latitude);
                        var lng = parseFloat(row.longitude);
    
                        if (!isNaN(lat) && !isNaN(lng)) {
                            var iconUrl = iconBaseUrl + row.marker_icons.trim();
                            var markerIcon = L.icon({
                                iconUrl: iconUrl,
                                iconSize: [40, 40],
                            });
    
                            var popupContent = '<b>Name:</b> ' + row.name + '<br>' +
                                               '<b>Sensor ID:</b> <span id="sensor-id">' + row.sensor_id + '</span><br>' +
                                               '<button onclick="copyToClipboard(\'sensor-id\')">Copy Sensor ID</button><br>' +
                                               '<b>Additional Details:</b> ' + row.additional_details + '<br>' +
                                               '<img src="' + row.image_url + '" alt="Image" style="width:200px;height:auto;">';
    
                            L.marker([lat, lng], { icon: markerIcon }).addTo(map).bindPopup(popupContent);
                        }
                    });
                });
        </script>
    </body>
    </html>
    """
    # Insert map
    components.html(map_html, height=430)
      # Define the LSID and number of days inputs
    lsid_to_filter = st.text_input('Insert Sensor ID from Map Above')
    num_days = st.slider("Select the number of days of data to view", min_value=1, max_value=30, value=1)

    # Add a button to generate data
    if st.button('Generate'):
        try:
            lsid_to_filter = int(lsid_to_filter)
        except ValueError:
            st.write("Please enter a valid number")
        else:

            # Initialize an empty list to store the data frames for each day
            data_frames = []
    
            # Loop over the past 'num_days' to retrieve data for each day
            for i in range(num_days):
                # Calculate the start and end timestamps for the current day
                start_timestamp = str(int(time.time()) - (i + 1) * 86400)
                end_timestamp = str(int(time.time()) - i * 86400)
    
                # Step 1: Sort parameters by parameter name
                params = {
                    "api-key": api_key,
                    "end-timestamp": end_timestamp,
                    "start-timestamp": start_timestamp,
                    "station-id": station_id,
                    "t": str(int(time.time()))
                }
                sorted_params = sorted(params.items(), key=lambda x: x[0])
    
                # Step 2: Create concatenated string
                concatenated_string = "".join([f"{param}{value}" for param, value in sorted_params])
    
                # Step 3: Compute HMAC API Signature
                message = concatenated_string.encode()
                secret_key_bytes = secret_key.encode()
                hmac_signature = hmac.new(secret_key_bytes, message, hashlib.sha256).hexdigest()
    
                # Step 4: Generate API URL
                base_url = "https://api.weatherlink.com/v2/historic/"
                query_params = {
                    "api-key": api_key,
                    "t": str(int(time.time())),
                    "start-timestamp": start_timestamp,
                    "end-timestamp": end_timestamp
                }
                query_string = urlencode(query_params)
                url = f"{base_url}{station_id}?{query_string}&api-signature={hmac_signature}"
    
                # Step 5: Load JSON data from the API URL
                response = requests.get(url)
                json_data = response.json()
    
                # Function to filter the JSON tree based on "lsid"
                def filter_tree(data, lsid):
                    if isinstance(data, dict):
                        tree = {}
                        if "lsid" in data and data["lsid"] == lsid:
                            return data
                        else:
                            for key, value in data.items():
                                subtree = filter_tree(value, lsid)
                                if subtree:
                                    tree[key] = subtree
                            return tree
                    elif isinstance(data, list):
                        tree = []
                        for item in data:
                            subtree = filter_tree(item, lsid)
                            if subtree:
                                tree.append(subtree)
                        return tree
    
                # Convert the JSON data into a tree
                tree = json_data
    
                # Filter the JSON tree based on user input for "lsid"
                filtered_tree = filter_tree(tree, lsid_to_filter)
    
                # Extract the relevant information from the JSON
                sensor_data = filtered_tree['sensors'][0]['data']
    
                # Convert the data into a DataFrame
                df = pd.json_normalize(sensor_data)
    
                # Convert 'depth' from feet to meters
                if 'depth' in df.columns:
                    df['depth'] = df['depth'] * 0.3048
    
                # Convert 'ts' from Unix timestamp to datetime
                df['ts'] = pd.to_datetime(df['ts'], unit='s')
    
                # Convert 'temp' from Fahrenheit to Celsius
                if 'temp' in df.columns:
                    df['temp'] = (df['temp'] - 32) * 5 / 9
    
                # Append the extracted data to the list
                data_frames.append(df)
    
            # Concatenate all the data frames into a single data frame
            combined_df = pd.concat(data_frames)
          
        
        # Display the line chart for 'depth' if available
        if 'depth' in combined_df.columns:
            st.line_chart(combined_df[['ts', 'depth']].rename(columns={'ts': 'DateTime', 'depth': 'Depth (m)'}).set_index('DateTime'))

        # Display the line chart for 'temperature' if available
        if 'temp' in combined_df.columns:
            st.line_chart(combined_df[['ts', 'temp']].rename(columns={'ts': 'DateTime', 'temp': 'Temperature (\u00B0C)'}).set_index('DateTime'))

        # Display the line chart for 'salinity' if available
        if 'salinity' in combined_df.columns:
            st.line_chart(combined_df[['ts', 'salinity']].rename(columns={'ts': 'DateTime', 'salinity': 'Salinity'}).set_index('DateTime'))

        # Display the line chart for 'rainfall_mm' if available
        if 'rainfall_mm' in combined_df.columns:
            st.line_chart(combined_df[['ts', 'rainfall_mm']].rename(columns={'ts': 'DateTime', 'rainfall_mm': 'Rainfall'}).set_index('DateTime'))

        # Check if any of the 'moist_soil_last' columns exist in the combined DataFrame
        moist_soil_columns = [col for col in combined_df.columns if col.startswith('moist_soil_last_')]
        if len(moist_soil_columns) > 0:
            chart_data = combined_df[['ts'] + moist_soil_columns].rename(columns={'ts': 'DateTime'})
            st.line_chart(chart_data.set_index('DateTime'))

        # Check if any of the 'salinity_last' columns exist in the combined DataFrame
        salinity_columns = [col for col in combined_df.columns if col.startswith('salinity_last_')]
        if len(salinity_columns) > 0:
            chart_data = combined_df[['ts'] + salinity_columns].rename(columns={'ts': 'DateTime'})
            st.line_chart(chart_data.set_index('DateTime'))

        # Download button for CSV file
        csv_data = combined_df.to_csv(index=False)
        b64 = base64.b64encode(csv_data.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="SuDSlab_Data.csv">Download SuDSlab Data</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.warning("Please enter the Sensor ID to proceed.")

if __name__ == "__main__":
    main()
