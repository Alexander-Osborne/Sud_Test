import streamlit as st
import folium
from streamlit_folium import st_folium

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    site = {
        "name": "Site 1",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "url": "https://example.com/site1"
    }
    
    map = folium.Map(location=[site["latitude"], site["longitude"]], zoom_start=10)

    folium.Marker(
        location=[site["latitude"], site["longitude"]],
        popup=f'<a href="{site["url"]}" target="_blank">{site["name"]}</a>',
        tooltip=site["name"]
    ).add_to(map)

    st_folium(map)

if __name__ == "__main__":
    main()
