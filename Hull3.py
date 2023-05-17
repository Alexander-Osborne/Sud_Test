import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime

# Latitude and longitude coordinates of Hull University
hull_university_location = (53.767851, -0.366748)

# Create a DataFrame for the location of Hull University



# CKAN API endpoint URL
apiUrl = 'https://opendata.hullcc.gov.uk/api/3'

# Dataset resource ID
resourceId = '6a9bc5a3-9c5d-4b0c-87af-1a18f7c507ef'

# Number of rows to retrieve from the end of the dataset
numRows = 1000

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

    df_location = pd.DataFrame({
    'Latitude': [hull_university_location[0]],
    'Longitude': [hull_university_location[1]]
})

# Show Hull University on a map
st.map(df_location)
    
except:
    st.write('Error occurred while retrieving the dataset.')
