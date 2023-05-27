import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, TapTool, OpenURL
from bokeh.tile_providers import get_provider, Vendors
from streamlit.bokeh_events import streamlit_bokeh_events

# Define the map location and zoom level
location = (51.5074, -0.1278)  # London, UK
zoom_level = 12

# Create a Bokeh figure and set the tile provider
tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)
p = figure(x_range=(-200000, 2000000), y_range=(-200000, 7000000),
           x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(tile_provider)

# Create a ColumnDataSource to store marker data
source = ColumnDataSource(data=dict(lat=[], lon=[], names=[]))

# Add clickable markers to the map
p.circle(x='lon', y='lat', size=10, source=source, alpha=0.7)

# Add a TapTool to handle click events on markers
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url="@names")

# Define a Streamlit app and set the title
st.title("Map App")

# Render the Bokeh figure using streamlit.bokeh_events
bokeh_event_data = streamlit_bokeh_events(figure=p, events="tap", key="map")

# Handle the click event and update the marker data
if bokeh_event_data:
    if "map_tap" in bokeh_event_data:
        lon, lat = bokeh_event_data["map_tap"]["x"], bokeh_event_data["map_tap"]["y"]
        source.data = dict(lat=[lat], lon=[lon], names=["Marker"])

# Display the map in Streamlit
st.bokeh_chart(p)

# Get the selected marker's coordinates
selected_marker = st.selectbox("Select a marker", ["Marker"])

if selected_marker:
    st.write("You selected the marker:", selected_marker)
    # Add your Streamlit code for the selected marker
