from ...DatabaseHandler import DatabaseHandler
import streamlit as st
from datetime import datetime
import math
from distances import get_distances

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

submitted_btn = st.button('Submit')

if submitted_btn:
    TODO: # insert into db - AMIT
    # db = DatabaseHandler(r"../hack23_db.db")
    # table_1 = "routes"
    # table_2 = "distances"
    # table_3 = "locations"

    # a_id = db.insert(f"INSERT INTO {table_3} (lat, lon) VALUES ({starting_point_lat}, {starting_point_lon})")
    # b_id = db.insert(f"INSERT INTO {table_3} (lat, lon) VALUES ({ending_point_lat}, {ending_point_lon})")

    # delivery_day = datetime.strptime(delivery_day, "%d-%m-%Y")
    # distance =get_distances((starting_point_lat, starting_point_lon),(ending_point_lat, ending_point_lon))
    # start_day = distance / 50 / 10
    # start_day = delivery_day - math.ceil(distance / 50 / 10 ) if start_day >= 1 else delivery_day
    
    # q = f"INSERT INTO {table_1} (id_starting_point, id_ending_point, delivery_start_date, delivery_end_date, distance, company, is_deleted) \
    #     VALUES ({a_id}, {b_id}, '{start_day}', '{delivery_day}', {distance}, '{company_name}', 0);"



