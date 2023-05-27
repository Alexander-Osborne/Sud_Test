import streamlit as st
import folium

# Add a title to your app
st.title("Map App")

# Define the map location
location = [51.5074, -0.1278]  # London, UK

# Create a folium map object
m = folium.Map(location=location, zoom_start=13)

# Add markers to the map
marker1 = folium.Marker([51.5074, -0.1278], popup='Marker 1')
marker2 = folium.Marker([51.5072, -0.1276], popup='Marker 2')

# Add the markers to the map
m.add_child(marker1)
m.add_child(marker2)

# Display the map using Folium's iframe method
folium_static = folium.Figure(width=800, height=500)
folium_static.add_child(m)

# Render the map in Streamlit
st.markdown(folium_static._repr_html_(), unsafe_allow_html=True)

# Add a sub-window for the selected marker
selected_marker = st.selectbox("Select a marker", ["Marker 1", "Marker 2"])

if selected_marker == "Marker 1":
    st.write("You selected Marker 1. Add your Streamlit code here.")
    # Add your Streamlit code for Marker 1
elif selected_marker == "Marker 2":
    st.write("You selected Marker 2. Add your Streamlit code here.")
    # Add your Streamlit code for Marker 2
