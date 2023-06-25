import streamlit as st
from dash import Dash
import dash_html_components as html
import dash_leaflet as dl
from dash_extensions import webcomponents as wc

# Set Streamlit app title and layout
st.set_page_config(page_title='University of Hull Map', layout='wide')

# Streamlit app content
st.title('University of Hull Map')

# Create a Dash app within Streamlit
app = Dash(__name__)

# Create a Dash Leaflet map component
map_component = dl.Map(center=[53.765, -0.335], zoom=15, children=[
    dl.TileLayer(),
    dl.Marker(position=[53.765, -0.335], children=[
        dl.Popup("University of Hull")
    ])
])

# Convert the Dash Leaflet map component to a web component
map_component_webcomponent = wc.Component(id="map", component_property="children", component_instance=map_component)

# Add the Dash Leaflet map web component to the Dash app layout
app.layout = html.Div(children=[
    wc.DashLeafletComponent(),
    map_component_webcomponent
])

# Run the Streamlit app with the Dash app embedded
if __name__ == '__main__':
    app.run_server(mode='inline')
