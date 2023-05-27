import streamlit as st
import folium
import pandas as pd
from folium import features
from streamlit_folium import folium_static
import numpy as np

def create_map():
    # Create the map object with the CartoDB Positron tileset and set the initial zoom location to England
    map = folium.Map(location=[53.0, -1.0], zoom_start=6, tiles='CartoDB Positron')

    # Read marker information from the CSV file
    markers_df = pd.read_csv("markers.csv")

    # Create markers for each row in the CSV with custom icons
    for index, row in markers_df.iterrows():
        # Create a custom marker icon with an image
        icon_image = row["marker_icon"]  # Column name in the CSV for marker icon image path
        icon = features.CustomIcon(icon_image, icon_size=(30, 30))

        # Add the marker to the map
        marker = folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=row["name"],
            tooltip=row["name"],
            icon=icon
        ).add_to(map)

        # Add the marker index as a button on the map
        map.add_child(folium.Popup(f'<button onclick="Streamlit.setComponentValue(\'selected_marker\', {index})">Marker {index + 1}</button>', parse_html=True))

    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

    selected_marker = st.session_state.get("selected_marker")

    # Display graph below the map when a marker is clicked
    if selected_marker is not None:
        st.write(f"You clicked marker {selected_marker + 1}. Here is additional content.")

        # Generate example data for the line chart
        np.random.seed(selected_marker)
        data = np.random.randn(100).cumsum()

        # Display the line chart below the map
        st.line_chart(data)

if __name__ == "__main__":
    main()
