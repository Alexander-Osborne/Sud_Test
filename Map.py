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

# Get the selected marker's index
selected_marker_idx = st.selectbox("Select a marker", range(len(df)), format_func=lambda i: df['Marker'][i])

# Define random data for the graph
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Add conditional statements based on the selected marker
if selected_marker_idx == 0:
    st.write("You selected Marker 1.")
    st.plotly_chart(go.Figure(data=go.Scatter(x=x, y=y), layout=go.Layout(height=400)))
elif selected_marker_idx == 1:
    st.write("You selected Marker 2.")
    st.plotly_chart(go.Figure(data=go.Scatter(x=x, y=-y), layout=go.Layout(height=400)))
