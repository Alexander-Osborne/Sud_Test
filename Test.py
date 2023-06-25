import streamlit as st
import folium
from streamlit_folium import folium_static
import altair as alt
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
    chart = alt.Chart(data).mark_bar().encode(
        x='Location',
        y='Value'
    ).properties(
        width=400,
        height=300
    )

    # Create the Folium map
    m = folium.Map(location=[53.7701, -0.3672], zoom_start=9)

    # Add markers to the map with Vega popups
    for _, row in data.iterrows():
        location = row['Location']
        value = row['Value']
        latitude = row['Latitude']
        longitude = row['Longitude']

        # Create the Vega chart HTML
        chart_html = chart.to_html()

        # Create the Folium popup with the Vega chart
        popup = folium.Popup(chart_html, max_width=600)

        # Add the marker with the popup to the map
        folium.Marker(
            location=[latitude, longitude],
            popup=popup
        ).add_to(m)

    # Render the map
    folium_static(m)

def main():
    render_map_page()

if __name__ == "__main__":
    main()
