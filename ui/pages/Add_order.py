import streamlit as st
import datetime

st.set_page_config(page_title="New order")
st.markdown("# New order")

company_name = st.text_input('Company', 'Waht is your company name?')

st.write("Starting point")
col1, col2 = st.columns(2)
with col1:
    starting_point_lon = st.text_input('lon', ' ')
with col2:
    starting_point_lat = st.text_input('lat', ' ')

st.write("Ending point")
colA, colB = st.columns(2)
with colA:
    ending_point_lon = st.text_input('lon', ' ', key="endPoint")
with colB:
    ending_point_lat = st.text_input('lat', ' ', key="endPointlat")

delivery_day = st.date_input("Delivery date")

type_of_material = st.selectbox('Type of material' ,('other','material1', 'material2', 'material3'))

weight = st.number_input('weight')

st.button('Submit')