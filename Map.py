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

        # Filter the JSON tree based on "lsid" equal to 459397
        lsid_to_filter = 478072
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

if __name__ == "__main__":
    main()
