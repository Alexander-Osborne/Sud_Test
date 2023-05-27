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

# Create a sample dataframe with marker data and types
data = {
    'Marker': ['Marker 1', 'Marker 2', 'Marker 3'],
    'Latitude': [51.5074, 51.5072, 51.5080],
    'Longitude': [-0.1278, -0.1276, -0.1280],
    'Type': ['swale', 'rain', 'swale']
}
df = pd.DataFrame(data)

# Create a folium map
m = folium.Map(location=[latitude, longitude], zoom_start=zoom_level)

# Create separate feature groups for different marker types
swale_group = folium.FeatureGroup(name='Swale')
rain_group = folium.FeatureGroup(name='Rain')

# Add markers to the respective feature groups based on types
for i, row in df.iterrows():
    if row['Type'] == 'swale':
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker']).add_to(swale_group)
    elif row['Type'] == 'rain':
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker']).add_to(rain_group)

# Add feature groups to the map
swale_group.add_to(m)
rain_group.add_to(m)

# Display the map in Streamlit
folium_static(m)

# Get the selected markers
selected_swales = st.checkbox("Swales", value=True)
selected_rain = st.checkbox("Rain", value=True)

# Add or remove marker groups based on selected checkboxes
if not selected_swales:
    if swale_group.get_name() in m._children:
        m.remove_child(swale_group)

if not selected_rain:
    if rain_group.get_name() in m._children:
        m.remove_child(rain_group)
