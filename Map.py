import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import numpy as np

# Create a Streamlit app and set a title
st.title("Map App")

# Define the map location and zoom level
latitude = 51.5074  # London, UK
longitude = -0.1278
zoom_level = 10

# Create a sample dataframe with marker data
data = {
    'Marker': ['Marker 1', 'Marker 2'],
    'Latitude': [51.5074, 51.5072],
    'Longitude': [-0.1278, -0.1276],
}
df = pd.DataFrame(data)

# Create a folium map
m = folium.Map(location=[latitude, longitude], zoom_start=zoom_level)

# Add markers to the map
for i, row in df.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker']).add_to(m)

# Display the map in Streamlit
folium_static(m)

# Get the current map view
lat_range = st.slider("Latitude Range", min_value=-90.0, max_value=90.0, value=(latitude-1, latitude+1), step=0.1)
lon_range = st.slider("Longitude Range", min_value=-180.0, max_value=180.0, value=(longitude-1, longitude+1), step=0.1)

# Generate random data for the graph
x = np.linspace(lat_range[0], lat_range[1], 100)
y = np.sin(x)

# Plot the graph based on the current map view
plt.plot(x, y)
st.pyplot(plt)
