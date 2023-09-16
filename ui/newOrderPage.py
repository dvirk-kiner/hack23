from unicodedata import name
import streamlit as st
import datetime

st.set_page_config(
    page_title="NewOrder",
)

st.write("new order")

company_name = st.text_input('Company', 'Waht is your company name?')

st.write("starting point")
col1, col2 = st.columns(2)
with col1:
    starting_point_lon = st.text_input('lon', ' ')
with col2:
    starting_point_lat = st.text_input('lat', ' ')

# st.write("ending point")
# col1, col2 = st.columns(2)
# with col1:
#     ending_point_lon = st.text_input('lon', ' ')
# with col2:
#     ending_point_lat = st.text_input('lat', ' ')

delivery_day = st.date_input("Delivery date", datetime.date(2019, 7, 6))

type_of_material = st.selectbox('Type of material' ,('material1', 'material2', 'material3'))
