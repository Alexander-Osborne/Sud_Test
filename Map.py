import streamlit as st
import folium
import pandas as pd
from folium import features
from streamlit_folium import folium_static

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

        # Define the JavaScript code to be executed on marker click
        js_code = f'''
            var checkbox = document.getElementById('checkbox{index}');
            checkbox.checked = true;
            Streamlit.setComponentValue("selected_marker", {index});
        '''

        # Add the marker to the map and attach the JavaScript code to the marker's onclick event
        marker = folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=row["name"],
            tooltip=row["name"],
            icon=icon
        ).add_to(map)

        marker.add_child(folium.Popup(f'<input type="checkbox" id="checkbox{index}" onclick="{js_code}">Click Me'))

    return map

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

    selected_marker = st.session_state.get("selected_marker")

    # Display additional content when a marker is clicked
    if selected_marker is not None:
        st.write(f"You clicked marker {selected_marker}. Here is additional content.")

if __name__ == "__main__":
    main()
