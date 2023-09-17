import streamlit as st
from PIL import Image

st.set_page_config(page_title="Hello", page_icon="🚛")
st.markdown("# Welcome to Carbon Saver Brothers!")

st.markdown(
    """
In today's landscape, a striking 92% of heavy trucks return empty, a glaring inefficiency that not only drains resources but also contributes significantly to environmental harm, particularly in terms of CO2 emissions.

Our innovative AI-driven solution is set to reimagine the transportation conundrum without the need for a full-scale revolution. We tackle the issue head-on by focusing on optimizing empty truck travel time.

Our approach is simple yet effective: Users input their routes into our platform, and we employ AI algorithms to intelligently match and optimize these journeys. Instead of needlessly duplicating routes, we identify opportunities for trucks to share trips, minimizing the distance they travel with no cargo onboard.

The results are twofold: We cut costs significantly and make a substantial dent in CO2 emissions.

Join us in taking transportation to the next level, one step at a time, as we strive to make a meaningful impact on efficiency and sustainability in the transportation sector through our hackathon project.   
"""
)

image = Image.open('images/truck.jpg')

st.image(image, caption='The Siblings & Others')