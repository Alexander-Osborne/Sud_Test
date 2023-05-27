import streamlit as st
import pandas as pd
import folium
import numpy as np
import matplotlib.pyplot as plt

# Generate random data for the map markers
def generate_random_data(num_markers):
    data = pd.DataFrame({
        'latitude': np.random.uniform(-90, 90, num_markers),
        'longitude': np.random.uniform(-180, 180, num_markers)
    })
    return data

# Create a map with markers
def create_map(data):
    # Create a map centered on a specific location
    map_center = [data['latitude'].mean(), data['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    # Add markers to the map
    for index, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            icon=folium.Icon(icon='cloud')
        ).add_to(m)

    return m

# Generate random data for the graph
def generate_random_graph():
    # Generate random data for the graph
    x = np.linspace(0, 10, 100)
    y = np.random.randn(100)

    # Create and display the graph
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig)

# Main function
def main():
    # Generate random data for the map markers
    data = generate_random_data(num_markers=10)

    # Create the map
    map = create_map(data)

    # Display the map
    st.title('Map with Markers')
    st.markdown(map._repr_html_(), unsafe_allow_html=True)

    # Handle marker click events
    if st.button('Click Marker'):
        generate_random_graph()

if __name__ == '__main__':
    main()
