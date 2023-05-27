import streamlit as st
import folium
from folium import plugins
from streamlit_folium import folium_static

def create_map():
    map = folium.Map(location=[37.7749, -122.4194], zoom_start=10)
    
    site = {
        "name": "Site 1",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "url": "https://example.com/site1"
    }
    
    # Create a custom marker icon
    icon = folium.features.CustomIcon("Swale_image.png", icon_size=(30, 30))
    
    folium.Marker(
        location=[site["latitude"], site["longitude"]],
        popup=f'<a href="{site["url"]}" target="_blank">{site["name"]}</a>',
        tooltip=site["name"],
        icon=icon  # Set the custom icon
    ).add_to(map)
    
    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

if __name__ == "__main__":
    main()
