import streamlit as st
import folium
from streamlit_folium import folium_static

# Create a Streamlit app and set a title
st.title("Map App")

# Create a Folium map object
m = folium.Map(location=[51.5074, -0.1278], zoom_start=13)

# Add clickable markers to the map
marker1 = folium.Marker([51.5074, -0.1278], popup='Marker 1')
marker2 = folium.Marker([51.5072, -0.1276], popup='Marker 2')

marker1.add_to(m)
marker2.add_to(m)

# Render the map in Streamlit
folium_static(m)

# Add a selectbox to select a marker
selected_marker = st.selectbox("Select a marker", ["Marker 1", "Marker 2"])

# Add conditional statements based on the selected marker
if selected_marker == "Marker 1":
    st.write("You selected Marker 1. Add your Streamlit code here.")
    # Add your Streamlit code for Marker 1
elif selected_marker == "Marker 2":
    st.write("You selected Marker 2. Add your Streamlit code here.")
    # Add your Streamlit code for Marker 2
