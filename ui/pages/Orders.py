import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="Orders")
st.markdown("# Orders")

data= pd.DataFrame(np.random.randn(50, 6),columns=['Company','Starting point','Ending point','Delivery date','Type of material','Weight'])

st.dataframe(data)  
