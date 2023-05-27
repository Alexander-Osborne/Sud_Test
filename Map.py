import streamlit as st
import folium

def main():
    # Set up the sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Map", "Blank Page"])

    # Render the appropriate page based on the selection
    if page == "Map":
        render_map_page()
    elif page == "Blank Page":
        render_blank_page()

def render_map_page():
    st.title("Map Page")

    # Create a map object
    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Add markers to the map
    marker1 = folium.Marker(location=[latitude1, longitude1], popup='Location 1')
    marker1.add_to(m)

    marker2 = folium.Marker(location=[latitude2, longitude2], popup='Location 2')
    marker2.add_to(m)

    # Render the map
    folium_static(m)

def render_blank_page():
    st.title("Blank Page")
    # Add content to your blank page here

if __name__ == "__main__":
    main()
