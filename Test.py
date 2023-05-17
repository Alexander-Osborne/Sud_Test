import streamlit as st
from PIL import Image

image = Image.open('Swale.JPG')

st.image(image, caption='Swale')
