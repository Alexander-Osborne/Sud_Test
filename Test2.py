import hmac
import hashlib
from urllib.parse import urlencode
import time
import requests
import json
import pandas as pd
import streamlit as st

# Read secret key from configuration file
config_file_path = "config.json"

with open(config_file_path) as config_file:
    config = json.load(config_file)

secret_key = config["secret_key"]

# Parameters
api_key = config["api_key"]
station_id = config["station_id"]
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

# Extract the relevant information from the JSON
sensor_data = filtered_tree['sensors'][0]['data']

# Convert the data into a DataFrame
df = pd.DataFrame(sensor_data)

# Display the DataFrame
st.write(df)

# Extract the timestamp and depth columns
timestamps = df['ts']
depths = df['depth']

# Combine the timestamps and depths into a new DataFrame
data = pd.DataFrame({'Timestamp': timestamps, 'Depth': depths})

# Plot the line chart using Streamlit
st.line_chart(data)
