import numpy as np
import pandas as pd
import streamlit as st
import sys, os, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from DatabaseHandler import DatabaseHandler
from optimizer import Optimizer


db_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "db", "hack23_db.db"))

db_path = db_abs_path
db = DatabaseHandler(db_path)
table_1 = "routes"
table_2 = "distances"
table_3 = "locations"

# self.db_path = db_path
# self.conn = sqlite3.connect(self.db_path)
# self.cursor = self.conn.cursor()

possible_date_end = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")

# q = f"SELECT improved_routes.company, {table_3}.lon AS starting_point_lot, {table_3}.lat AS starting_point_lat, {table_3}.lon AS ending_point_lot, {table_3}.lat AS ending_point_lat, \
#       improved_routes.delivery_end_date, improved_routes.distance FROM (SELECT * FROM {table_1} WHERE delivery_start_date = {possible_date_end}) as improved_routes LEFT JOIN {table_3} \
#           ON improved_routes.id_starting_point ={table_3}.id OR improved_routes.id_ending_point ={table_3}.id;"
q = f"SELECT improved_routes.id, improved_routes.company, \
l_1.lon AS starting_point_lot, \
l_1.lat AS starting_point_lan, l_2.lon AS ending_point_lot, \
l_2.lat AS ending_point_lan, improved_routes.delivery_end_date, improved_routes.distance \
FROM ( \
SELECT * \
FROM {table_1} \
WHERE delivery_start_date = \"{possible_date_end}\"\
) AS improved_routes \
LEFT JOIN {table_3} AS l_1 \
ON improved_routes.id_starting_point =l_1.id \
LEFT JOIN {table_3} AS l_2 \
ON improved_routes.id_ending_point =l_2.id ;"


data = db.select(to_fetch_all= True, query=q)

st.set_page_config(page_title="Tomorrow's Not Optimized Orders")
st.markdown("# Tomorrow's Not Optimized Orders")

# data= pd.DataFrame(np.random.randn(10, 6),columns=['Company','Starting point','Ending point','Delivery date','Type of material','Weight'])
data= pd.DataFrame(data,columns=['id', 'Company','Starting point-Lot','Starting point-Lan',\
                            'Ending point-Lot','Ending point-Lan','Delivery date','Distance'])
st.dataframe(data)

opt_btn = st.button('Optimize')

if opt_btn:
    opt = Optimizer(db_path)
    opt.optimize_routes()

    db = DatabaseHandler(db_path)
    table_4 = "optimizations"

    # Display all the routes that are optimized in a table
    query = f"SELECT * FROM {table_4};"

    data = db.select(to_fetch_all= True, query=query)
    data= pd.DataFrame(data,columns=['id', 'start_date', 'A_lot','A_lan',\
                                'B_lot','B_lan','C_lot','C_lan','D_lot','D_lan'])
    
    # Add a column that links to ./map.py with id as a GET argument
    # data['Map'] = [f'<a href="http://localhost:8501/Map?id={i}">Map</a>' for i in data['id']]
    data['Map'] = [f"http://localhost:8501/Map?id={i}" for i in data['id']]

    st.data_editor(
    data,
    column_config={
        "Map": st.column_config.LinkColumn(
            "Map",
            max_chars=1000,
        )
    },
    hide_index=True,
    )
    # st.dataframe(data)

    # validate="^https://[a-z]+\.streamlit\.app$",


