import streamlit as st
import folium
from streamlit_folium import folium_static
import altair as alt
import pandas as pd
from vega_datasets import data as vega_data

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
    chart = alt.Chart(data).mark_bar().encode(
        x='Location',
        y='Value'
    ).properties(
        width=400,
        height=300
    ).to_dict()

    # Create the Folium map
    m = folium.Map(location=[53.7701, -0.3672], zoom_start=9)

    # Add markers to the map with Vega popups
    for _, row in data.iterrows():
        location = row['Location']
        value = row['Value']
        latitude = row['Latitude']
        longitude = row['Longitude']

        # Create the Vega chart specification
        vega_spec = {
            "$schema": "https://vega.github.io/schema/vega/v5.json",
            "width": 400,
            "height": 300,
            "description": "Vega Bar Chart",
            "data": {"name": "source"},
            "mark": "bar",
            "encoding": {
                "x": {"field": "Location", "type": "ordinal"},
                "y": {"field": "Value", "type": "quantitative"}
            }
        }

        # Embed the Vega chart specification as a VegaLite JSON string
        chart_json = alt.vegalite(vgjson=vega_spec, data=data).to_json()

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
