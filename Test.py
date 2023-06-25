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
    .popup-contents { margin-top: 10px; }
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

        // Define an array to store the popup contents
        var popupContents = [];

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
            popupContents.push(popupContent); // Store the popup content in the array

            var marker = L.marker([lat, lng], { icon: markerIcon }).addTo(map);
            marker.bindPopup(popupContent).on('popupopen', function(e) {
              var popup = e.popup;
              var contentElement = document.createElement('div');
              contentElement.className = 'popup-contents';
              contentElement.innerHTML = popupContent;
              document.body.appendChild(contentElement);
            });
          }
        });

        // Function to send the popup content to Streamlit
        function sendPopupContent(content) {
          // Print the popup content below the map in Streamlit
          var contentElement = document.createElement('div');
          contentElement.innerHTML = content;
          document.body.appendChild(contentElement);
        }

        // Add event listeners to markers to send popup content to Streamlit
        var markers = document.querySelectorAll('.leaflet-marker-icon');
        markers.forEach(function(marker, index) {
          marker.addEventListener('click', function() {
            sendPopupContent(popupContents[index]);
          });
        });
      });
  </script>
</body>
</html>
"""

# Display the map and popup contents in Streamlit
components.html(map_html, height=600)
