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
              Streamlit.sendCustomMessage(JSON.stringify({ selectedMarkerId: selectedMarkerId }));
            }).on('popupclose', function(e) {
              selectedMarkerId = '';
              // Clear the selected marker ID in Streamlit
              Streamlit.sendCustomMessage(JSON.stringify({ selectedMarkerId: selectedMarkerId }));
            });
          }
        });
      });
  </script>
</body>
</html>
"""

# Display the map using CustomComponent
selected_marker_id = st.empty()
component_value = selected_marker_id.value

if component_value:
    selected_marker_id.write(f"Selected Marker ID: {component_value}")
else:
    selected_marker_id.write("No marker selected.")

# Define the JavaScript code for handling custom messages
custom_js_code = """
(function() {
  // Define the function to handle custom messages
  const handleCustomMessage = (event) => {
    const messageData = JSON.parse(event.data);
    if (messageData.selectedMarkerId) {
      // Update the value of the selected marker ID
      const selectedMarkerId = messageData.selectedMarkerId;
      const selectedMarkerIdElement = document.getElementById('streamlit-selected-marker-id');
      selectedMarkerIdElement.value = selectedMarkerId;
      selectedMarkerIdElement.dispatchEvent(new Event('change'));
    }
  };

  // Listen for custom messages from the Streamlit app
  window.addEventListener('message', handleCustomMessage);
})();
"""

# Display the HTML code with CustomComponent
components.html(map_html, height=600, scrolling=True)

# Display the selected marker ID using st.write
selected_marker_id_value = st.text_input("Selected Marker ID:", key='streamlit-selected-marker-id')

# Inject the JavaScript code for custom messages
st.write("<script>{}</script>".format(custom_js_code), unsafe_allow_html=True)
