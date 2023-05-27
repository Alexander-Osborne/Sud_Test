import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

# Create a scattermapbox plot
fig = go.Figure(go.Scattermapbox(
    lat=df['Latitude'],
    lon=df['Longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10,
        color='blue'
    ),
    text=df['Marker']
))

# Set the layout for the map
fig.update_layout(
    mapbox=dict(
        style='open-street-map',
        center=dict(lat=latitude, lon=longitude),
        zoom=zoom_level
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Render the map in Streamlit
st.plotly_chart(fig)

# Get the current map view
map_data = st.deck_gl_chart(viewport=st.pydeck_chart.get_view_state())

# Generate graphs based on the current map view
if map_data is not None:
    lat_range = [map_data["latitude"] - map_data["latitude_delta"] / 2,
                 map_data["latitude"] + map_data["latitude_delta"] / 2]
    lon_range = [map_data["longitude"] - map_data["longitude_delta"] / 2,
                 map_data["longitude"] + map_data["longitude_delta"] / 2]

    # Generate random data for the graph
    x = np.linspace(lat_range[0], lat_range[1], 100)
    y = np.sin(x)

    # Display the graph based on the current map view
    st.plotly_chart(go.Figure(data=go.Scatter(x=x, y=y), layout=go.Layout(height=400)))
