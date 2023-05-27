import streamlit as st
import folium

def create_map():
    site = {
        "name": "Site 1",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "url": "https://example.com/site1"
    }
    
    map = folium.Map(location=[site["latitude"], site["longitude"]], zoom_start=10)
    
    folium.Marker(
        location=[site["latitude"], site["longitude"]],
        popup=site["name"],
        tooltip=site["name"]
    ).add_to(map)
    
    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

    site = {
        "name": "Site 1",
        "url": "https://example.com/site1"
    }

    if st.button(f"Click here for more info about {site['name']}"):
        st.markdown(f"Redirecting to [{site['url']}]({site['url']})")
        # Perform the redirection to site["url"]

if __name__ == "__main__":
    main()
