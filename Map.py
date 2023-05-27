import streamlit as st
import folium
import pandas as pd
from folium import features
from streamlit_folium import folium_static
import numpy as np
import hmac
import hashlib
from urllib.parse import urlencode
import time
import requests
import json
import pandas as pd
import streamlit as st
from PIL import Image



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

        # Add the marker to the map
        marker = folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=row["name"],
            tooltip=row["name"],
            icon=icon
        ).add_to(map)

        # Add the marker index as a button on the sidebar
        button = st.sidebar.button(f"Marker {index + 1}")

        # Set the selected_marker value when the button is clicked
        if button:
            st.session_state.selected_marker = index

    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

    selected_marker = st.session_state.get("selected_marker")

    # Display graph below the map when a marker is clicked
    if selected_marker is not None:
        st.write(f"You clicked marker {selected_marker + 1}. Here is additional content.")

        # Generate example data for the line chart
        # Retrieve secrets from Streamlit Secrets
secret_key = st.secrets["secret_key"]
api_key = st.secrets["api_key"]
station_id = st.secrets["station_id"]

# Define the number of days to retrieve data for
num_days = 1

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
        st.line_chart(depth_data.rename(columns={'ts': 'DateTime', 'depth': 'Depth (m)'}).set_index('DateTime'))
                     
        # Display the line chart for 'temperature'
        st.line_chart(temperature_data.rename(columns={'ts': 'DateTime', 'temp': 'Temperature (\u00B0C)'}).set_index('DateTime'))

        # Display the line chart for 'salinity'
        st.line_chart(salinity_data.rename(columns={'ts': 'DateTime', 'salinity': 'Salinity'}).set_index('DateTime'))

if __name__ == "__main__":
    main()
