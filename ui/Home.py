import streamlit as st
from PIL import Image

st.set_page_config(page_title="Hello")#, page_icon=🚛)
st.markdown("# Welcome to Hack Zurich!")

st.markdown(
    """
    ###the best bro
"""
)

image = Image.open('truck.jpg')

st.image(image, caption='Sunrise by the mountains')