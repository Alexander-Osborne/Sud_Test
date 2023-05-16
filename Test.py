import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Sample rainfall data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
rainfall = [45, 62, 32, 14, 67, 78, 92, 85, 47, 32, 15, 23]

# Create a dataframe for the data
df = pd.DataFrame({'Month': months, 'Rainfall (mm)': rainfall})

# Plotting the rainfall data
fig, ax = plt.subplots()
ax.bar(df['Month'], df['Rainfall (mm)'])
ax.set_xlabel('Month')
ax.set_ylabel('Rainfall (mm)')
ax.set_title('Monthly Rainfall')

# Adding labels to the top of each bar
for i, v in enumerate(df['Rainfall (mm)']):
    ax.text(i, v, str(v), ha='center', va='bottom')

# Adding current time and date in the top right corner as BST
nowTime = datetime.now()
bstTime = nowTime + timedelta(minutes=60)  # Adjust the time by adding 60 minutes (1 hour) for BST
dateStr = bstTime.strftime('%b %d, %Y %H:%M:%S')
fig.text(0.9, 0.9, dateStr, ha='right')

# Render the plot using Streamlit
st.pyplot(fig)

