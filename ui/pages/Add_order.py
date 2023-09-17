import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from DatabaseHandler import DatabaseHandler
import streamlit as st
from datetime import datetime

db_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "db", "hack23_db.db"))
db_path = db_abs_path

dh = DatabaseHandler(db_path)
st.set_page_config(page_title="New order")
st.markdown("# New order")

company_name = st.text_input('Company', 'HOLCIM')

st.write("Starting point")
col1, col2 = st.columns(2)
with col1:
    starting_point_lon = st.number_input('lon')
with col2:
    starting_point_lat = st.number_input('lat')

st.write("Ending point")
colA, colB = st.columns(2)
with colA:
    ending_point_lon = st.number_input('lon',  key="endPoint")
with colB:
    ending_point_lat = st.number_input('lat', key="endPointlat")


delivery_day = st.date_input("Delivery date",format="DD/MM/YYYY")
# delivery_day = datetime(delivery_day).strftime("%d/%m/%Y")

type_of_material = st.selectbox('Type of material' ,('other','material1', 'material2', 'material3'))

weight = st.number_input('weight')

submitted_btn = st.button('Submit')

if submitted_btn:
    if starting_point_lon == ending_point_lon and starting_point_lat == ending_point_lat:
        st.error("Starting point and ending point cannot be the same")
        st.stop()
    # print("=====================================")
    # print(company_name)
    # print(starting_point_lon)
    # print(starting_point_lat)
    # print(ending_point_lon)
    # print(ending_point_lat)
    # print(delivery_day)
    # print(type_of_material)
    # print(weight)
    # print("=====================================")
    dh.add_new_route(starting_point_lon, starting_point_lat, ending_point_lon, ending_point_lat, delivery_day, company_name)
    st.write("Order submitted successfully")



