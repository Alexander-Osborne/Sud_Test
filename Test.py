import streamlit as st
from streamlit import components as stc

# Define the HTML code for the map
map_html = """
<!DOCTYPE html>
<html>
<head>
  <title>UK Map with Markers</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.css" />
  <style>
    #map { height: 400px; }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/papaparse@5.3.0"></script>
  <script>
    var map = L.map('map').setView([53.771552, -0.36425564], 15); // Set initial view to the first marker

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      maxZoom: 18,
    }).addTo(map);

    // Fetch the CSV file
    fetch('https://raw.githubusercontent.com/Alexander-Osborne/Sud_Test/main/markers.csv')
      .then(response => response.text())
      .then(data => {
        // Parse the CSV data
        var parsedData = Papa.parse(data, { header: true }).data;

        // Define the base URL for marker icons
        var iconBaseUrl = 'https://raw.githubusercontent.com/Alexander-Osborne/Sud_Test/main/marker_icons/';

        // Store the selected marker name
        var selectedMarkerId = '';

        // Iterate through the parsed data and add markers to the map
        parsedData.forEach(row => {
          var lat = parseFloat(row.latitude);
          var lng = parseFloat(row.longitude);

          if (!isNaN(lat) && !isNaN(lng)) {
            var iconUrl = iconBaseUrl + row.marker_icons.trim();
            var markerIcon = L.icon({
              iconUrl: iconUrl,
              iconSize: [32, 32],
              iconAnchor: [16, 32],
              popupAnchor: [0, -32]
            });

            var popupContent = "<b>" + row.sensor_id + "</b><br>" + row.additional_details;
            var marker = L.marker([lat, lng], { icon: markerIcon }).addTo(map);
            marker.bindPopup(popupContent).on('popupopen', function(e) {
              selectedMarkerId = row.sensor_id;
              // Send the selected marker ID to Streamlit
              Streamlit.setComponentValue(selectedMarkerId);
              Streamlit.reportChangedFormElement('selectedMarkerId');
            }).on('popupclose', function(e) {
              selectedMarkerId = '';
              // Clear the selected marker ID in Streamlit
              Streamlit.setComponentValue(selectedMarkerId);
              Streamlit.reportChangedFormElement('selectedMarkerId');
            });
          }
        });
      });
  </script>
</body>
</html>
"""

# Define the Streamlit component
class MapComponent(stc.ComponentBase):
    def __init__(self, **kwargs):
        self.selected_marker_id = None

    def _update(self):
        # Retrieve the selected marker ID from Streamlit
        session_state = st.session_state.get(self.session_id)
        if session_state is not None:
            self.selected_marker_id = session_state.get('selected_marker_id')

    def write(self, **kwargs):
        self._update()

        # Display the map using CustomComponent
        stc.html(map_html, height=600, scrolling=True)

        # Display the selected marker ID using st.write
        if self.selected_marker_id:
            st.write(f"Selected Marker ID: {self.selected_marker_id}")
        else:
            st.write("No marker selected.")

    def generate_hash(self, args):
        return ""

    def get_args(self, hash):
        return {}

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value

# Register the Streamlit component
stc.register(MapComponent)

# Use the Streamlit component in your app
map_component = MapComponent()
map_component.write()

# Retrieve the selected marker ID
selected_marker_id = st.session_state.get('selected_marker_id')
if selected_marker_id:
    st.write(f"Selected Marker ID: {selected_marker_id}")
else:
    st.write("No marker selected.")
