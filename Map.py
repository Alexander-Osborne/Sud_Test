import streamlit as st
import folium
from folium import plugins
from streamlit_folium import folium_static

def create_map():
    # Create the map object with a different tileset
    map = folium.Map(location=[37.7749, -122.4194], zoom_start=10, tiles='Stamen Terrain')
    
    site = {
        "name": "Site 1",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "url": "https://example.com/site1"
    }
    
    # Create a custom marker icon with an image
    icon_image = 'Swale_image.png'  # Path to the custom marker image
    icon = folium.features.CustomIcon(icon_image, icon_size=(30, 30))
    
    folium.Marker(
        location=[site["latitude"], site["longitude"]],
        popup=f'<a href="{site["url"]}" target="_blank">{site["name"]}</a>',
        tooltip=site["name"],
        icon=icon
    ).add_to(map)
    
    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

if __name__ == "__main__":
    main()
