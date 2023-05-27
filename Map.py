import streamlit as st
import pydeck as pdk
from streamlit_folium import folium_static
import folium

def create_map():
    site = {
        "name": "Site 1",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "url": "https://example.com/site1"
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
        map_style="mapbox://styles/mapbox/light-v9"
    )
    
    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    
    # Render the map using folium_static
    folium_map = folium.Map(location=[0, 0], zoom_start=1)
    folium_static(folium_map)
    
    # Render the PyDeck map as an HTML string
    html = map.to_html()
    
    # Inject the HTML string into the folium_map
    folium_element = folium.Element().add_to(folium_map)
    folium_element._parent = folium_map
    folium_element._template = folium_template
    folium_element.html.add_child(folium.Html(html))
    
    # Use Streamlit's write_html function to write the modified folium_map
    st.write(folium_map._repr_html_(), unsafe_allow_html=True)
    
    # Handle click events manually
    clicked = folium_element._children.get('clicks')
    if clicked:
        location = clicked['location']
        if location and 'lat' in location and 'lng' in location:
            latitude = location['lat']
            longitude = location['lng']
            if latitude == site["latitude"] and longitude == site["longitude"]:
                st.write("Redirecting to", site["url"])
                # Perform the redirection to site["url"]

if __name__ == "__main__":
    main()
