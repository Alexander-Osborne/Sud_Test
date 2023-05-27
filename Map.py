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
            import streamlit as st
            from PIL import Image

            st.title('SuDS'' _lab_ '' UK - Wilberforce 001')


            # Define the coordinates for Hull University
            hull_uni_coordinates = (53.77114698979646, -0.36430683784066786)

            # Create a DataFrame with a single row containing Hull University coordinates
            df1 = pd.DataFrame({'lat': [hull_uni_coordinates[0]], 'lon': [hull_uni_coordinates[1]]})



            # Load the image
            image = Image.open('Swale.jpg')


    

            st.subheader('Map')
            st.map(df1, zoom=15)

            st.subheader('Image')
            st.image(image, caption='Outfall of Swale')
    


            # Retrieve secrets from Streamlit Secrets
            secret_key = st.secrets["secret_key"]
            api_key = st.secrets["api_key"]
            station_id = st.secrets["station_id"]

            t = str(int(time.time()))
            start_timestamp = str(int(time.time() - 86400))
            end_timestamp = str(int(time.time()))

            # Step 1: Sort parameters by parameter name
            params = {
              "api-key": api_key,
              "end-timestamp": end_timestamp,
              "start-timestamp": start_timestamp,
              "station-id": station_id,
                "t": t
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
                "t": t,
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

            df['salinity']=df['salinity']

            df['temp'] = (df['temp'] - 32) * 5/9

            depth_data = df[['ts', 'depth']]
            salinity_data = df[['ts', 'salinity']]
            temperature_data= df[['ts','temp']]

            # Display the line chart for 'depth'
            st.line_chart(depth_data.rename(columns={'ts': 'DateTime', 'depth': 'Depth (m)'}).set_index('DateTime'))
                     
            # Display the line chart for 'temperature'
            st.line_chart(temperature_data.rename(columns={'ts': 'DateTime', 'temp': 'Temperature (\u00B0C)'}).set_index('DateTime'))

            # Display the line chart for 'salinity'
            st.line_chart(salinity_data.rename(columns={'ts': 'DateTime', 'salinity': 'Salinity'}).set_index('DateTime'))

            
            
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
