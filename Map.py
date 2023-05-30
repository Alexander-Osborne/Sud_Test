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
    st.markdown('<h1 style="text-align: center;">SuDS<span style="font-style: italic;">lab</span> UK</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px;">Data Viewer and Download</p>', unsafe_allow_html=True)


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
        478072: "SuDSlab-UoH-Wilberforce-002 (Input)",
        478073: "SuDSlab-UoH-Wilberforce-002 (Output)",
        570520: "SuDSlab-UoH-Planter-001 (Input)",
        570521: "SuDSlab-UoH-Planter-001 (Output)",
        599263: "SuDSlab-UoH-Planter-001 (Soil)",
        570517: "SuDSlab-UoH-Planter-002 (Input)",
        570522: "SuDSlab-UoH-Planter-002 (Output)"
    }  # Example lsid options with corresponding titles

    lsid_to_filter = st.selectbox("Select Sensor ID", options=list(lsid_options.keys()), format_func=lambda x: lsid_options[x])

    if lsid_to_filter:
        # Update the page title based on the selected lsid
        st.markdown(f"<h2 style='text-align: center;'>{lsid_options[lsid_to_filter]}</h2>", unsafe_allow_html=True)


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
        st.warning("Please enter the lsid value to proceed.")

if __name__ == "__main__":
    main()
