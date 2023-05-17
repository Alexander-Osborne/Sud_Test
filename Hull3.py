import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime
from PIL import Image

st.title('SuDS'' _lab_ '' UK - Wilberforce 002')

# Define the coordinates for Hull University
hull_uni_coordinates = (53.77114698979646, -0.36430683784066786)

# Create a DataFrame with a single row containing Hull University coordinates
df1 = pd.DataFrame({'lat': [hull_uni_coordinates[0]], 'lon': [hull_uni_coordinates[1]]})

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

    # Load the image
    image = Image.open('Swale.jpg')

    # Display the last timestamp value
    last_timestamp = tsData[-1].strftime("%d, %B %Y, %H:%M:%S")
    st.write(f"Last timestamp value: {last_timestamp}")

    # Create a layout with two columns
    col1, col2 = st.columns(2)

    # In the first column, display the map
    with col1:
        st.subheader('Map')
        st.map(df1, zoom=15)

    # In the second column, display the image
    with col2:
        st.subheader('Image')
        st.image(image, caption='Outfall of Swale')

    # Create a single row layout for the three graphs
    st.subheader('Data Visualization')
    col1, col2, col3 = st.columns(3)

    # Create the three separate figures using Streamlit and Altair
    chart_temp = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',
        y=alt.Y('Temperature:Q', axis=alt.Axis(title='Temperature (\u00B0C)')),
        color=alt.value('red')
    )

    chart_depth = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',
        y=alt.Y('Depth:Q', axis=alt.Axis(title='Depth (m)')),
        color=alt.value('blue')
    )

    chart_salinity = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',
        y='Salinity:Q',
        color=alt.value('green')
    )

    # Create a slider to control the index of the graph to be displayed
    index = st.slider('Select Graph', min_value=0, max_value=2)

    # Display the graph based on the selected index
    if index == 0:
        col1.subheader('Temperature')
        col1.altair_chart(chart_temp, use_container_width=True)
    elif index == 1:
        col2.subheader('Depth')
        col2.altair_chart(chart_depth, use_container_width=True)
    elif index == 2:
        col3.subheader('Salinity')
        col3.altair_chart(chart_salinity, use_container_width=True)

except:
    st.write('Error occurred while retrieving the dataset.')
