import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# Sample rainfall data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
rainfall = [45, 62, 32, 14, 67, 78, 92, 85, 47, 32, 15, 23]

# Create a dataframe for the data
df = pd.DataFrame({'Month': months, 'Rainfall (mm)': rainfall})

# Adding current time and date in the top right corner as BST
nowTime = datetime.now()
bstTime = nowTime + timedelta(minutes=60)  # Adjust the time by adding 60 minutes (1 hour) for BST
dateStr = bstTime.strftime('%b %d, %Y %H:%M:%S')

# Display the initial bar chart using Streamlit
chart = st.bar_chart(df['Rainfall (mm)'])

# Display the current time and date
st.write(dateStr)

# Auto-update the bar chart every 10 seconds
while True:
    # Update the data
    df['Rainfall (mm)'] = [value + 5 for value in df['Rainfall (mm)']]

    # Update the chart
    chart.bar_chart(df['Rainfall (mm)'])

    # Wait for 10 seconds
    time.sleep(10)
