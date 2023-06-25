import streamlit as st
import folium
from streamlit_folium import folium_static
import altair as alt
import json
import pandas as pd

def render_map_page():
    st.markdown('<h1 style="text-align: center;">Location Viewer with Vega Popups</h1>', unsafe_allow_html=True)

    # Create a sample DataFrame
    data = pd.DataFrame({
        'Location': ['Location 1', 'Location 2', 'Location 3'],
        'Value': [10, 20, 15],
        'Latitude': [53.7701, 53.772, 53.774],
        'Longitude': [-0.3672, -0.368, -0.369]
    })

    # Create a Vega bar chart
    vega_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "description": "Vega Bar Chart",
        "data": {"values": data.to_dict(orient='records')},
        "mark": "bar",
        "encoding": {
            "x": {"field": "Location", "type": "ordinal"},
            "y": {"field": "Value", "type": "quantitative"}
        }
    }

    # Convert the VegaLite specification to JSON
    chart_json = json.dumps(vega_spec)

    # Create the Folium map
    m = folium.Map(location=[53.7701, -0.3672], zoom_start=9)

    # Add markers to the map with Vega popups
    for _, row in data.iterrows():
        location = row['Location']
        latitude = row['Latitude']
        longitude = row['Longitude']

        # Create the Folium Vega popup
        folium.VegaLite(chart_json, width=420, height=320).add_to(folium.Marker([latitude, longitude], popup=folium.Popup()))

        # Add the marker to the map
        folium.Marker([latitude, longitude], popup=popup).add_to(m)

    # Render the map using folium_static
    folium_static(m)

def main():
    render_map_page()

if __name__ == "__main__":
    main()
