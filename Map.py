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

    m = folium.Map(location=[51.5074, -0.1278], zoom_start=12, tiles="CartoDB Positron")

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

        # Construct the path to the custom marker icon for the classification
        icon_path = icon_directory + f'icon_{classification.lower()}.png'

        # Create a custom icon
        custom_icon = folium.CustomIcon(icon_image=icon_path, icon_size=(30, 30))

        marker = folium.Marker(location=[latitude, longitude], popup=name, tooltip=classification, icon=custom_icon)
        marker.add_to(marker_clusters[classification])

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


    # Retrieve secrets from Streamlit Secrets
    secret_key = st.secrets["secret_key"]
    api_key = st.secrets["api_key"]
    station_id = st.secrets["station_id"]

    # Select the number of days
    num_days = st.slider("Select the number of days of data to view", min_value=1, max_value=30, value=1)

    lsid_options = [478072, 478073]  # Example lsid options, replace with your own values
    lsid_to_filter = st.selectbox("Select Sensor ID", options=lsid_options)

    if lsid_to_filter:
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
            df['depth'] = df['depth'] * 0.3048

            # Convert 'ts' from Unix timestamp to datetime
            df['ts'] = pd.to_datetime(df['ts'], unit='s')

            df['salinity'] = df['salinity']

            df['temp'] = (df['temp'] - 32) * 5 / 9

            # Append the extracted data to the list
            data_frames.append(df)

        # Concatenate all the data frames into a single data frame
        combined_df = pd.concat(data_frames)

        # Display the line chart for 'depth'
        st.line_chart(combined_df[['ts', 'depth']].rename(columns={'ts': 'DateTime', 'depth': 'Depth (m)'}).set_index('DateTime'))

        # Display the line chart for 'temperature'
        st.line_chart(combined_df[['ts', 'temp']].rename(columns={'ts': 'DateTime', 'temp': 'Temperature (\u00B0C)'}).set_index('DateTime'))

        # Display the line chart for 'salinity'
        st.line_chart(combined_df[['ts', 'salinity']].rename(columns={'ts': 'DateTime', 'salinity': 'Salinity'}).set_index('DateTime'))

        # Download button for CSV file
        csv_data = combined_df.to_csv(index=False)
        b64 = base64.b64encode(csv_data.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="SuDSlab_Data.csv">Download SuDSlab Data</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.warning("Please enter the lsid value to proceed.")

if __name__ == "__main__":
    main()

