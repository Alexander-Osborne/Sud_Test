import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# Sample rainfall data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
rainfall = [45, 62, 32, 14, 67, 78, 92, 85, 47, 32, 15, 23]

# Create a dataframe for the data
df = pd.DataFrame({'Month': months, 'Rainfall (mm)': rainfall})

# Initialize the current time
now_time = datetime.now()

# Display the initial bar chart using Streamlit
chart = st.bar_chart(df['Rainfall (mm)'])

# Auto-update the bar chart every 10 seconds
while True:
    # Update the data
    df['Rainfall (mm)'] = [value + 5 for value in df['Rainfall (mm)']]

    # Update the chart
    chart.bar_chart(df['Rainfall (mm)'])

    # Update the current time
    bst_time = now_time + timedelta(minutes=60)  # Adjust the time by adding 60 minutes (1 hour) for BST
    date_str = bst_time.strftime('%b %d, %Y %H:%M:%S')

    # Display the current time
    st.write(date_str)

    # Wait for 10 seconds
    time.sleep(10)
