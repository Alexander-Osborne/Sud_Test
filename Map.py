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

        # Generate the HTML for the graph
        graph_html = generate_graph_html(row["name"])  # Replace "generate_graph_html" with your function to generate the graph HTML

        # Create a popup with the graph HTML
        popup_content = folium.Popup(graph_html, max_width=800)

        # Add the marker to the map with the custom popup
        marker = folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_content,
            tooltip=row["name"],
            icon=icon
        ).add_to(map)

    return map

def generate_graph_html(marker_name):
    # Replace this function with your code to generate the HTML for the graph
    # You can use Streamlit components or any other plotting library to generate the graph and return the HTML
    html = f"""
        <html>
        <head>
            <title>{marker_name} Graph</title>
        </head>
        <body>
            <h1>{marker_name} Graph</h1>
            <p>Replace this with your graph HTML</p>
        </body>
        </html>
    """
    return html

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map = create_map()
    folium_static(map)

if __name__ == "__main__":
    main()
