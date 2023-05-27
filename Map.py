import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

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

# Get the selected marker
selected_marker = st.selectbox("Select a marker", df['Marker'])

# Perform actions based on the selected marker
if selected_marker == 'Marker 1':
    st.write("You selected Marker 1.")
    # Add your Streamlit code for Marker 1
elif selected_marker == 'Marker 2':
    st.write("You selected Marker 2.")
    # Add your Streamlit code for Marker 2
