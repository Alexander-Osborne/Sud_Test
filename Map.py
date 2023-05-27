import streamlit as st
import pandas as pd
import plotly.express as px

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

# Create a scatter_geo plot
fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', hover_name='Marker')

# Update the layout for the map
fig.update_geos(
    center=dict(lat=latitude, lon=longitude),
    projection_type="natural earth",
    showcountries=True,
    countrycolor="gray",
    showland=True,
    landcolor="lightgray",
    showocean=True,
    oceancolor="lightblue",
    showrivers=True,
    rivercolor="blue",
)

# Set the map zoom level
fig.update_geos(fitbounds="locations", visible=False)

# Render the map in Streamlit
st.plotly_chart(fig)

# Get the selected marker's coordinates
selected_marker = st.selectbox("Select a marker", df['Marker'])

# Add conditional statements based on the selected marker
if selected_marker == "Marker 1":
    st.write("You selected Marker 1. Add your Streamlit code here.")
    # Add your Streamlit code for Marker 1
elif selected_marker == "Marker 2":
    st.write("You selected Marker 2. Add your Streamlit code here.")
    # Add your Streamlit code for Marker 2
