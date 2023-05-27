import streamlit as st
import folium
from streamlit_folium import folium_static

def create_map():
    map = folium.Map(location=[53.7647, -0.3490], zoom_start=10)

    site = {
        "name": "Hull University",
        "latitude": 53.7647,
        "longitude": -0.3490,
        "url": "https://www.hull.ac.uk/"
    }

    folium.Marker(
        location=[site["latitude"], site["longitude"]],
        popup=f'<a href="{site["url"]}" target="_blank">{site["name"]}</a>',
        tooltip=site["name"]
    ).add_to(map)

    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

if __name__ == "__main__":
    main()
