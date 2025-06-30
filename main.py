import streamlit as st 
import pandas as pd
import sqlite3

db = sqlite3.connect('db3MLAHP.db')
df_Booking = pd.read_excel('3MLAHP.xlsx',sheet_name='Booking')
df_Boat_Plan = pd.read_excel('3MLAHP.xlsx',sheet_name='Boat_Plan')
df_Chopper_Plan = pd.read_excel('3MLAHP.xlsx',sheet_name='Chopper_Plan')
df_Field_Bed_Capacity = pd.read_excel('3MLAHP.xlsx',sheet_name='Field_Bed_Capacity')
df_Regular_Crew = pd.read_excel('3MLAHP.xlsx',sheet_name='Regular_Crew')

df_Regular_Crew.to_sql(
    name='Regular_Crew',
    con=db,
    if_exists='replace',
    index = False,
    dtype={
        'ID':'numeric',
        'Field':'text',
        'Date_Start':'numeric',
        'Date_End':'numeric',
        'Person_On_Board':'integer'
    }
)
db.execute('Drop View If Exists test')
db.execute(""" Create View test As Select * From Regular_Crew where Field = 'JAS' """)
st.title('3 Month Look Ahead Plan')


st.markdown('#### Booking')
st.dataframe(df_Booking)

