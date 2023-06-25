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
    .popup-message {
      position: absolute;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      background-color: rgba(0, 0, 0, 0.8);
      color: #fff;
      padding: 10px;
      border-radius: 5px;
      z-index: 999;
      transition: opacity 0.5s;
    }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="popup-message"></div>

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
            marker.bindPopup(popupContent).on('click', function(e) {
              // Copy the sensor ID to the clipboard
              navigator.clipboard.writeText(row.sensor_id)
                .then(function() {
                  showPopupMessage("Copied to Clipboard");
                  console.log('Sensor ID copied to clipboard: ' + row.sensor_id);
                })
                .catch(function(error) {
                  console.error('Unable to copy sensor ID to clipboard: ', error);
                });
            });
          }
        });
      });

    function showPopupMessage(message) {
      var popupMessageElement = document.getElementById('popup-message');
      if (popupMessageElement !== null) {
        popupMessageElement.innerText = message;
        popupMessageElement.style.opacity = 1;
        setTimeout(function() {
          popupMessageElement.style.opacity = 0;
        }, 2000);
      }
    }
  </script>
</body>
</html>
"""

# Display the map in Streamlit
components.html(map_html, height=600)
