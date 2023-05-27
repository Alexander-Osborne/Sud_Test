import streamlit as st
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

# Iterate through the dataframe and add markers based on types
for _, row in df.iterrows():
    if row['Type'] == 'swale':
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker'], icon=folium.Icon(color='blue')).add_to(m)
    elif row['Type'] == 'rain':
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker'], icon=folium.Icon(color='green')).add_to(m)

# Display the map in Streamlit
folium_static(m)

# Get the selected markers
selected_swales = st.checkbox("Swales", value=True)
selected_rain = st.checkbox("Rain", value=True)

# Update the map based on the selected checkboxes
if not selected_swales:
    for child in m.get_root().children:
        if child.layer_name == 'Swale':
           
