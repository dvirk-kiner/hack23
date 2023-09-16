import streamlit as st
from streamlit_folium import st_folium
import folium

m= folium.Map(location=[46.8139, 8.2242], zoom_start=8)
folium.Marker(location=[46.8139, 8.2242], popup="Zurich").add_to(m)

st_data = st_folium(m)

b= folium.Map(location=[48.8139, 4.2242], zoom_start=8)
folium.Marker(location=[46.8139, 8.2242], popup="ggggggggg").add_to(b)

st_data = st_folium(b)
