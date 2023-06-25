import folium
import jinja2

location_center = [45.5236, -122.6750]
locations = [[45.5012, -122.6655],[45.5132, -122.6708],[45.5275, -122.6692],[45.5318, -122.6745]]

m = folium.Map(location_center, zoom_start=13)
for location in locations:
    folium.Marker(
        location=location,
        popup = f'<input type="text" value="{location[0]}, {location[1]}" id="myInput"><button onclick="myFunction()">Copy location</button>'
    ).add_to(m)
    
el = folium.MacroElement().add_to(m)
el._template = jinja2.Template("""
    {% macro script(this, kwargs) %}
    function myFunction() {
      /* Get the text field */
      var copyText = document.getElementById("myInput");

      /* Select the text field */
      copyText.select();
      copyText.setSelectionRange(0, 99999); /* For mobile devices */

      /* Copy the text inside the text field */
      document.execCommand("copy");
    }
    {% endmacro %}
""")

display(m)
