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

        // Store the selected marker name
        var selectedMarkerName = '';

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

            var popupContent = "<b>" + row.name + "</b><br>" + row.additional_details;
            var marker = L.marker([lat, lng], { icon: markerIcon }).addTo(map);
            marker.bindPopup(popupContent).on('popupopen', function(e) {
              selectedMarkerName = row.name;
              // Send the selected marker name to Streamlit
              sendSelectedMarkerName(selectedMarkerName);
              // Trigger immediate re-render of Streamlit app
              st.experimental_set_query_params(selectedMarkerName=selectedMarkerName);
            }).on('popupclose', function(e) {
              selectedMarkerName = '';
              // Clear the selected marker name in Streamlit
              sendSelectedMarkerName(selectedMarkerName);
              // Trigger immediate re-render of Streamlit app
              st.experimental_set_query_params(selectedMarkerName=selectedMarkerName);
            });
          }
        });
      });

    function sendSelectedMarkerName(name) {
      // Clear the selected marker name in Streamlit
      var nameElement = document.getElementById('selected-marker-name');
      if (nameElement === null) {
        nameElement = document.createElement('div');
        nameElement.id = 'selected-marker-name';
        document.body.appendChild(nameElement);
      }
      nameElement.innerHTML = "<h3>Selected Marker Name:</h3><p>" + name + "</p>";
    }
  </script>
</body>
</html>
"""

# Get the selected marker name from Streamlit's query parameters
selected_marker_name = st.experimental_get_query_params().get("selectedMarkerName", [None])[0]

# Display the map and selected marker name in Streamlit
components.html(map_html, height=600)

# Print the selected marker name in Streamlit
if selected_marker_name is not None:
    st.write("Selected Marker Name:", selected_marker_name)
