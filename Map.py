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
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>

        <div id="myPlot" style="width:100%;max-width:700px"></div>

        <script>
        const xArray = [50,60,70,80,90,100,110,120,130,140,150];
        const yArray = [7,8,8,9,9,9,10,11,14,14,15];

        // Define Data
        const data = [{
          x:xArray,
          y:yArray,
          mode:"markers"
        }];

        // Define Layout
        const layout = {
          xaxis: {range: [40, 160], title: "Square Meters"},
          yaxis: {range: [5, 16], title: "Price in Millions"},  
          title: "House Prices vs. Size"
        };

        // Display using Plotly
        Plotly.newPlot("myPlot", data, layout);
        </script>

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
