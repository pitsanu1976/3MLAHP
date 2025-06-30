import streamlit as st 
import pandas as pd

st.markdown('### Boat Plan')
df_Boat_Plan = pd.read_excel('3MLAHP.xlsx',sheet_name='Boat_Plan')

st.dataframe(df_Boat_Plan)