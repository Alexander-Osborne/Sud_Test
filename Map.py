import streamlit as st

def create_map():
    site = {
        "name": "Site 1",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "url": "https://example.com/site1"
    }
    
    map_data = {
        "name": [site["name"]],
        "latitude": [site["latitude"]],
        "longitude": [site["longitude"]],
        "url": [site["url"]]
    }
    
    return map_data

def main():
    st.title("Monitoring Sites Map")
    st.markdown("Map showing the location of monitoring sites")

    map_data = create_map()
    st.map(map_data)
    
    site = {
        "name": "Site 1",
        "url": "https://example.com/site1"
    }
    
    if st.button(f"Click here for more info about {site['name']}"):
        st.write("Redirecting to", site["url"])
        # Perform the redirection to site["url"]

if __name__ == "__main__":
    main()
