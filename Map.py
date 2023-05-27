import streamlit as st
import pydeck as pdk

def create_map():
    site = {
        "name": "Site 1",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "url": "https://google.com"
    }
    
    view_state = pdk.ViewState(
        latitude=site["latitude"],
        longitude=site["longitude"],
        zoom=10,
        pitch=0
    )
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[site],
        get_position="[longitude, latitude]",
        get_radius=500,
        get_fill_color="[255, 0, 0]",
        pickable=True
    )
    
    map = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9",
        onClick="[{longitude},{latitude}]".format(**site)
    )
    
    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    st.pydeck_chart(map)

if __name__ == "__main__":
    main()
