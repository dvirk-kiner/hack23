import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from DatabaseHandler import DatabaseHandler


st.set_page_config(page_title="Orders")
st.markdown("# Orders")

db = DatabaseHandler(r"../hack23_db.db")
table_1 = "routes"
table_2 = "distances"
table_3 = "locations"

q = f"SELECT improved_routes.company, {table_3}.lon AS starting_point_lot, {table_3}.lat AS starting_point_lat, {table_3}.lon AS ending_point_lot, {table_3}.lat AS ending_point_lat, \
      improved_routes.delivery_end_date, improved_routes.distance FROM (SELECT * FROM {table_1} WHERE is_deleted = 0) as improved_routes LEFT JOIN {table_3} \
          ON improved_routes.id_starting_point ={table_3}.id OR improved_routes.id_ending_point ={table_3}.id \
            LIMIT 1000;"

data = db.select(to_fetch_all= True, query=q)
data= pd.DataFrame(data, \
                   columns=['Company','Starting point-Lot','Starting point-Lan',\
                            'Ending point-Lot','Ending point-Lan','Delivery date','distance'])

st.dataframe(data)  




