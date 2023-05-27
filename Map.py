import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
import numpy as np

def create_map():
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)
    fg = folium.FeatureGroup(name="State bounds")
    fg.add_child(folium.features.GeoJson(bounds))

    capitals = STATE_DATA

    for capital in capitals.itertuples():
        fg.add_child(
            folium.Marker(
                location=[capital.latitude, capital.longitude],
                popup=f"{capital.capital}, {capital.state}",
                tooltip=f"{capital.capital}, {capital.state}",
                icon=folium.Icon(color="green")
                if capital.state == st.session_state.get("selected_state")
                else None,
            )
        )

    m.add_child(fg)
    return m

def main():
    st.title("State Capitals Map")
    st.markdown("Map showing state capitals")

    m = create_map()
    out = st_folium(
        m,
        width=1200,
        height=500,
    )

    selected_state = st.session_state.get("selected_state")

    # Display graph below the map when a marker is clicked
    if selected_state is not None:
        st.write(f"You clicked state: {selected_state}. Here is additional content.")

        # Generate example data for the line chart
        np.random.seed(hash(selected_state) % 100)
        data = np.random.randn(100).cumsum()

        # Display the line chart below the map
        st.line_chart(data)

if __name__ == "__main__":
    main()
