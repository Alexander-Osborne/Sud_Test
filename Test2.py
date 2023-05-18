import hmac
import hashlib
from urllib.parse import urlencode
import time
import requests
import json
import pandas as pd
import streamlit as st

secret_key= st.secrets["secret_key"]

# Parameters
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
lsid_to_filter = 492303
filtered_tree = filter_tree(tree, lsid_to_filter)

# Convert the filtered tree to a DataFrame
df = pd.DataFrame(filtered_tree)

if 'ts' in df.columns and 'depth' in df.columns:
    # Extract the timestamp and depth columns
    timestamps = pd.to_datetime(df['ts'], unit='s')
    depths_feet = df['depth']

    # Convert depths from feet to meters
    depths_meters = depths_feet * 0.3048

    # Create a new DataFrame with timestamps and depths in meters
    data = pd.DataFrame({'Timestamp': timestamps, 'Depth': depths_meters})

    # Set the Timestamp column as the index
    data.set_index('Timestamp', inplace=True)

    # Plot the line chart using Streamlit
    st.line_chart(data)
else:
    st.write("Error: Required columns 'ts' and 'depth' not found in the data.")
