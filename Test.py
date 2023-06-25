import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("SuDSlab UK", style={"text-align": "center"}),
    html.P("Data Viewer and Download", style={"text-align": "center"}),
    dcc.Graph(
        id="map",
        figure={
            "data": [
                go.Scattermapbox(
                    lat=[53.77114698979646],
                    lon=[-0.36430683784066786],
                    mode="markers",
                    marker=dict(size=10, color="red"),
                    text=["Hull University"]
                )
            ],
            "layout": go.Layout(
                mapbox=dict(
                    center=dict(lat=53.77114698979646, lon=-0.36430683784066786),
                    zoom=14
                ),
                margin=dict(l=0, r=0, t=30, b=0)
            )
        }
    ),
    # Add other components or controls as needed
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
