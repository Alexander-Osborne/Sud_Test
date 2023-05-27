import streamlit as st
import folium
import pandas as pd
import geocoder
from folium import features
from streamlit_folium import folium_static

def get_user_location():
    if "gps" not in st.session_state:
        return None

    return st.session_state["gps"]

def set_user_location():
    if "gps" not in st.session_state:
        g = geocoder.ip('me')
        if g.latlng:
            st.session_state["gps"] = g.latlng

def create_map():
    user_location = get_user_location()

    # If user location is available, use it as the initial zoom location
    if user_location:
        map = folium.Map(location=user_location, zoom_start=10, tiles='CartoDB Positron')
    else:
        map = folium.Map(location=[53.7647, -0.3490], zoom_start=10, tiles='CartoDB Positron')

    # Read marker information from the CSV file
    markers_df = pd.read_csv("markers.csv")

    # Create markers for each row in the CSV with custom icons
    for index, row in markers_df.iterrows():
        # Create a custom marker icon with an image
        icon_image = row["marker_icon"]  # Column name in the CSV for marker icon image path
        icon = features.CustomIcon(icon_image, icon_size=(30, 30))

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f'<a href="{row["url"]}" target="_blank">{row["name"]}</a>',
            tooltip=row["name"],
            icon=icon
        ).add_to(map)

    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    set_user_location()  # Retrieve and store user's GPS coordinates

    map = create_map()
    folium_static(map)

if __name__ == "__main__":
    main()
