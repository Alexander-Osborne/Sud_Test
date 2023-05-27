import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    'URL': ['https://www.google.com', 'https://www.openai.com']
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
    text=df['Marker'],
    customdata=df['URL'],
    hovertemplate='<b>%{text}</b><br><a href="%{customdata}" target="_blank">Click here</a> to open URL'
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
