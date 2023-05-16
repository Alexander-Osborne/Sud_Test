import streamlit as st
import numpy as np

# Create a Streamlit app
st.title("Random Graph Stream")

# Function to generate random data
def generate_data():
    x = np.linspace(0, 100, 100)
    y = np.random.randint(0, 100, size=(100,))
    return x, y

# Initialize the chart data
data = {'x': [], 'y': []}

# Update the graph within a while loop
while True:
    # Generate random data
    x, y = generate_data()

    # Update the chart data
    data['x'] = x
    data['y'] = y

    # Display the line chart
    st.line_chart(data)

    # Wait for a short duration before updating again
    st.experimental_rerun()
