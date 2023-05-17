import streamlit as st
from PIL import Image

image = Image.open('swale.jpg')

st.image(image, caption='Swale')
