import hmac
import hashlib
from urllib.parse import urlencode
import time
import requests
import json
import pandas as pd
import os
import streamlit as st

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

def main():
    # Retrieve secrets from Streamlit Secrets
    secret_key = st.secrets["secret_key"]
    api_key = st.secrets["api_key"]
    station_id = st.secrets["station_id"]

    t = str(int(time.time()))
    start_timestamp = str(int(time.time() - 2000))
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

    # Convert the JSON data into a tree
    tree = json_data

    # Filter the JSON tree based on "lsid" equal to 459397
    lsid_to_filter = 492303
    filtered_tree = filter_tree(tree, lsid_to_filter)

    # Print the filtered tree structure
    st.json(filtered_tree)

    # Save the filtered tree as JSON to a file
    filtered_file_name = "filtered_tree.json"
    with open(filtered_file_name, "w") as file:
        json.dump(filtered_tree, file, indent=2)

    st.write(f"Filtered tree saved as {filtered_file_name}")

    # Read JSON data from file
    with open('filtered_tree.json', 'r') as file:
        json_data = json.load(file)

    # Extract the relevant information from the JSON
    sensor_data = json_data['sensors'][0]['data']

    # Convert the data into a DataFrame
    df = pd.json_normalize(sensor_data)

# Save the DataFrame as a CSV file
    df.to_csv('table.csv', index=False)

# Add a button to download the CSV file
    st.download_button(label="Download CSV", data=df.to_csv(), file_name='table.csv', mime='text/csv')

if __name__ == "__main__":
    main()
