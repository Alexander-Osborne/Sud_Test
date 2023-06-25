import folium
import altair as alt
import pandas as pd

# Create a sample DataFrame
data = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [10, 20, 15, 12]
})

# Create the Vega chart
chart = alt.Chart(data).mark_bar().encode(
    x='category',
    y='value'
)

# Create the Folium map
m = folium.Map(location=[53.7701, -0.3672], zoom_start=9)

# Create a marker with a popup containing the Vega chart
marker = folium.Marker(
    location=[53.7701, -0.3672],
    popup=folium.Popup(chart.to_html(), max_width=400)
)

# Add the marker to the map
marker.add_to(m)

# Render the map
folium_static(m)
