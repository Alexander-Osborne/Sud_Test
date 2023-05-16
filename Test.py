import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Create a Streamlit app
st.title("Random Graph Stream")

# Set up the figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Function to generate random data
def generate_data():
    x = np.linspace(0, 100, 100)
    y = np.random.randint(0, 100, size=(100,))
    return x, y

# Update the graph within a while loop
while True:
    # Generate random data
    x, y = generate_data()

    # Update the plot
    line.set_data(x, y)
    ax.relim()
    ax.autoscale_view(True, True, True)

    # Update the figure
    st.pyplot(fig)

    # Wait for a short duration before updating again
    st.experimental_rerun()

