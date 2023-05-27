import streamlit as st
import folium
import numpy as np
import matplotlib.pyplot as plt

# Create a map with Hull University marker
def create_map():
    # Create a map centered on Hull University
    map_center = [53.7677, -0.3665]  # Hull University coordinates
    m = folium.Map(location=map_center, zoom_start=15)

    # Add marker for Hull University
    folium.Marker(
        location=[53.7677, -0.3665],  # Hull University coordinates
        popup="Hull University",
        icon=folium.Icon(icon='cloud')
    ).add_to(m)

    return m

# Generate random data for the graph
def generate_random_data():
    # Generate random data for the graph
    x = np.linspace(0, 10, 100)
    y = np.random.randn(100)

    return x, y

# Generate and display the graph
def display_graph(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig)

# Main function
def main():
    # Create the map
    map = create_map()

    # Display the map
    st.title('Map with Markers')
    folium_static(map)

    # Handle marker click events
    if st.button('Click Marker'):
        # Generate random data for the graph
        x, y = generate_random_data()
        # Display the graph
        display_graph(x, y)

if __name__ == '__main__':
    main()
