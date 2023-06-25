import streamlit as st
import streamlit.components.v1 as components

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

        // Store the selected sensor_id
        var selectedSensorId = '';

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
              selectedSensorId = row.sensor_id;
              // Send the selected sensor_id to Streamlit
              window.parent.postMessage(selectedSensorId, '*');
            }).on('popupclose', function(e) {
              selectedSensorId = '';
              // Clear the selected sensor_id in Streamlit
              window.parent.postMessage(selectedSensorId, '*');
            });
          }
        });
      });
  </script>
</body>
</html>
"""

# Display the map
st.html(map_html, height=600)

# Store the selected sensor_id in session state
if "selected_sensor_id" not in st.session_state:
    st.session_state.selected_sensor_id = ""

# Listen for messages from the map
selected_sensor_id = st._get_widget_value("__input__")
if selected_sensor_id:
    # Update the selected sensor_id in session state
    st.session_state.selected_sensor_id = selected_sensor_id

# Use the selected sensor_id elsewhere in your Streamlit app
if st.session_state.selected_sensor_id:
    st.write("Selected Sensor ID:", st.session_state.selected_sensor_id)
