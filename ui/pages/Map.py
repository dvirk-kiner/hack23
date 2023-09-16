import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Map")
st.markdown("# Map")

point_a_lat= 25.6085
point_a_lon = -100.86183 
point_b_lat = 26.0520019
point_b_lon = -97.952103
point_c_lat = 25.671039
point_c_lon = -100.1758128 
point_d_lat = 26.0508406
point_d_lon = -98.2978951

a = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyC3MZiMTmpfuAhD3JCyiVtghDEJzUiQmfk&origin={point_a_lat},{point_a_lon}&destination={point_d_lat},{point_d_lon}&waypoints={point_b_lat},{point_b_lon}|{point_c_lat},{point_c_lon}"
components.iframe(src=a,width=650, height=350, scrolling=True)
