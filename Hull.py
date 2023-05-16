import streamlit as st
import requests
import pandas as pd
from datetime import datetime

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

    # Display the line charts using Streamlit
    st.line_chart(df.set_index('Timestamp'))

except:
    st.write('Error occurred while retrieving the dataset.')
