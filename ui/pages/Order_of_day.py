import numpy as np
import pandas as pd
import streamlit as st

delivery_day = st.date_input("Delivery date")


data= pd.DataFrame(np.random.randn(10, 6),columns=['Company','Starting point','Ending point','Delivery date','Type of material','Weight'])
st.dataframe(data)