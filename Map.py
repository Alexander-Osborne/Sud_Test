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
    'Longitude': [-0.1278, -0.1276]
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

# Define the JavaScript code snippet
javascript_code = """
<script>
    var marker = document.getElementsByClassName('scattermapbox trace')[0].data[{selected_marker_idx}];
    marker.on('click', function() {
        window.open('https://www.google.com', '_blank');
    });
</script>
"""

# Embed the JavaScript code in the app using the component API
st.components.v1.html(javascript_code)

