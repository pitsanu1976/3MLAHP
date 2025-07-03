import streamlit as st 
import pandas as pd
import sqlite3
from view import Reg, pob

db = sqlite3.connect('db3MLAHP.db')
df_Booking = pd.read_excel('3MLAHP.xlsx',sheet_name='Booking')
df_Boat_Plan = pd.read_excel('3MLAHP.xlsx',sheet_name='Boat_Plan')
df_Chopper_Plan = pd.read_excel('3MLAHP.xlsx',sheet_name='Chopper_Plan')
df_Field_Bed_Capacity = pd.read_excel('3MLAHP.xlsx',sheet_name='Field_Bed_Capacity')
df_Regular_Crew = pd.read_excel('3MLAHP.xlsx',sheet_name='Regular_Crew')
df_Date_Calendar= pd.read_excel('3MLAHP.xlsx',sheet_name='Date_Calendar')
df_Boat_Chopper_Capacity= pd.read_excel('3MLAHP.xlsx',sheet_name='Boat_Chopper_Capacity')


df_Booking.to_sql(
    name='Booking',
    con=db,
    if_exists='replace',
    index = False,
    dtype={
        'Id':'integer',
        'Field':'text',
        'IAP_ID':'text',
        'SML_ID':'text',
        'Platform':'text',
        'Department':'text',
        'Project_Description':'text',
        'Project_Owner':'text',
        'Vendor':'text',
        'POB':'integer',
        'Date_End':'text',
        'PlanStart':'text',
        'PlanFinish':'text',
        'Duration':'integer',
        'InterField':'text',
        'MobCode':'text',
        'DeMobCode':'text',
        'Mob_By_Code':'text',
        'De-mob_By_Code':'text',
        'L_Remarks':'text'
    }
)

df_Boat_Plan.to_sql(
    name='Boat_Plan',
    con=db,
    if_exists='replace',
    index = False,
    dtype={
        'Id':'integer',
        'Type':'text',
        'Boat_Name':'text',
        'Direction':'text',
        'Origin':'text',
        'Destination':'text',
        'Dep_Date':'text',
        'Dep_Time':'integer',
        'Arr_Date':'text',
        'Arr_Time':'integer',
        'Code':'text',
        'Trip_Id':'text'
    }
)

df_Chopper_Plan.to_sql(
    name='Chopper_Plan',
    con=db,
    if_exists='replace',
    index = False,
    dtype={
        'Id':'integer',
        'Type':'text',
        'Vessel':'text',
        'Dir':'text',
        'Origin':'text',
        'Destination':'text',
        'Dep_Date':'text',
        'Arr_Date':'text',
        'Code':'text',
        'Trip_Id':'text'
    }
)

df_Field_Bed_Capacity.to_sql(
    name='Field_Bed_Capacity',
    con=db,
    if_exists='replace',
    index = False,
    dtype={
        'Id':'integer',
        'Field':'text',
        'Bed_Capacity':'integer'
    }
)

df_Date_Calendar.to_sql(
    name='Date_Calendar',
    con=db,
    if_exists='replace',
    index = False,
    dtype={
        'Id':'integer',
        'Date':'text'
    }
)

df_Regular_Crew.to_sql(
    name='Regular_Crew',
    con=db,
    if_exists='replace',
    index = False,
    dtype={
        'Id':'integer',
        'Field':'text',
        'Date_Start':'text',
        'Date_End':'text',
        'Person_On_Board':'integer'
    }
)

df_Boat_Chopper_Capacity.to_sql(
    name='Boat_Chopper_Capacity',
    con=db,
    if_exists='replace',
    index = False,
    dtype={
        'Id':'integer',
        'Vessel_Name':'text',
        'Bed_Capacity':'integer',
        'Seat_Capacity':'integer'
    }
)

db.execute('Drop View If Exists test')
db.execute(Reg)



df_view = pd.read_sql("select * from test",db)


st.title('3 Month Look Ahead Plan')


st.markdown('#### Booking')
st.markdown('### table booking')
st.dataframe(df_Booking)

field = st.radio(label='Field',options=['"JAS"','"G1"','"G11"','"G10"'])
pob2 = f"""
CREATE VIEW pob as
SELECT 
	Date, 
	(
	SELECT 
		max(Bed_Capacity) 
	FROM 
		Field_Bed_Capacity 
	WHERE 
		Field = {field}
	)AS 
	Field_Bed,
	coalesce
	(
		(SELECT 
			sum(bcc.Bed_Capacity)
		FROM(
			SELECT
				ba.Boat_Name,
				ba.Destination,
				ba.Arr_Date,
				bd.Dep_Date
			FROM
				Boat_Plan as ba
			LEFT JOIN
				Boat_Plan as bd
			ON
				ba.Boat_Name = bd.Boat_Name
			WHERE
				ba.Destination = {field} AND
				bd.Origin = {field} AND
				bd.Dep_Date > ba.Arr_Date
			GROUP by
				ba.Boat_Name,
				ba.Arr_Date
		) as 
		bt
		INNER JOIN
			Boat_Chopper_Capacity as bcc
		on
			bt.Boat_Name = bcc.Vessel_Name
		WHERE
			d.Date >= bt.Arr_Date AND
			d.Date <= bt.Dep_Date
		),0
	) as 
	Vessel_Bed,
	coalesce(
		(SELECT
			sum(POB)
		FROM
			Booking as bk
		WHERE
			bk.Field = {field} AND
			d.Date >= bk.PlanStart AND
			d.Date <= bk.PlanFinish),0
	) as ActivityPOB,
	(SELECT 
		max(rc.Person_On_Board)	
	FROM
		Regular_Crew as rc
	WHERE
		rc.Field = {field} AND
		d.Date >= rc.Date_Start AND
		d.Date <= rc.Date_End		
	) as RegularCrew
	
FROM 
	Date_Calendar as d
"""
run = st.button(label='run query')
if run:
    db.execute('Drop View If Exists pob')
    db.execute(pob2)
    df_pob = pd.read_sql("select * from pob",db)
    st.dataframe(df_pob)