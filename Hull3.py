import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime
import streamlit as st
from PIL import Image

# Define the coordinates for Hull University
hull_uni_coordinates = (53.77114698979646, -0.36430683784066786)

# Create a DataFrame with a single row containing Hull University coordinates
df = pd.DataFrame({'lat': [hull_uni_coordinates[0]], 'lon': [hull_uni_coordinates[1]]})

# Display the map centered at Hull University
st.map(df, zoom=15)


image = Image.open('Swale.jpg')
image = image.rotate(90)  # Rotate the image by 90 degrees clockwise

st.image(image, caption='Swale')


# CKAN API endpoint URL
apiUrl = 'https://opendata.hullcc.gov.uk/api/3'

# Dataset resource ID
resourceId = 'f4f85e47-f8d9-4f13-8138-4bec4afde84d'

# Number of rows to retrieve from the end of the dataset
numRows = 2000

# Create the API request URL
apiRequestUrl = f'{apiUrl}/action/datastore_search?resource_id={resourceId}&fields=ts,temp,salinity,depth&sort=_id desc&limit={numRows}'

try:
    # Send API request to retrieve the dataset
    response = requests.get(apiRequestUrl)
    data = response.json()
    records = data['result']['records']

    # Extract the 'ts' and 'temp' columns from the records
    tsData = [record['ts'] for record in records]
    tempData = [record['temp'] for record in records]
    depthData = [record['depth'] for record in records]
    salinityData = [record['salinity'] for record in records]
    

    # Convert timestamps to datetime objects
    tsData = [datetime.fromtimestamp(ts) for ts in tsData]

    # Create a dataframe for the data
    df = pd.DataFrame({'Timestamp': tsData, 'Temperature': tempData, 'Depth': depthData, 'Salinity': salinityData})

   
    # Create three separate figures using Streamlit and Altair
    st.subheader('Temperature')
    chart_temp = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',
        y='Temperature:Q',
        color=alt.value('red')
    )
    st.altair_chart(chart_temp, use_container_width=True)

    st.subheader('Depth')
    chart_depth = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',
        y='Depth:Q',
        color=alt.value('blue')
    )
    st.altair_chart(chart_depth, use_container_width=True)

    st.subheader('Salinity')
    chart_salinity = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',
        y='Salinity:Q',
        color=alt.value('green')
    )
    st.altair_chart(chart_salinity, use_container_width=True)

    
except:
    st.write('Error occurred while retrieving the dataset.')
