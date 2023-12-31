import os
import streamlit as st
import streamlit.components.v1 as components
from DatabaseHandler import DatabaseHandler

st.set_page_config(page_title="Map")
st.markdown("# Map")

args = st.experimental_get_query_params()
if args:

    optimized_id = int(args["id"][0])

    db_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "db", "hack23_db.db"))

    db_path = db_abs_path
    db = DatabaseHandler(db_path)
    table_1 = "optimizations"
    query = f"SELECT * FROM {table_1} WHERE id={optimized_id}"
    result = db.select(query, to_fetch_all=True)[0]
    db.close()

    point_a_lat = result[1]
    point_a_lon = result[2]
    point_b_lat = result[3]
    point_b_lon = result[4]
    point_c_lat = result[5]
    point_c_lon = result[6]
    point_d_lat = result[7]
    point_d_lon = result[8]

else:
    point_a_lat= 25.6085
    point_a_lon = -100.86183
    point_b_lat = 26.0520019
    point_b_lon = -97.952103
    point_c_lat = 25.671039
    point_c_lon = -100.1758128
    point_d_lat = 26.0508406
    point_d_lon = -98.2978951

a = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyC3MZiMTmpfuAhD3JCyiVtghDEJzUiQmfk&origin={point_a_lat},{point_a_lon}&destination={point_d_lat},{point_d_lon}&waypoints={point_b_lat},{point_b_lon}|{point_c_lat},{point_c_lon}"

# do zoom to the map

components.iframe(src=a, width=650, height=350, scrolling=True)
