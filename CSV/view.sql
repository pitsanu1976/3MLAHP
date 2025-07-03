SELECT 
	Date, 
	(
	SELECT 
		max(Bed_Capacity) 
	FROM 
		Field_Bed_Capacity 
	WHERE 
		Field = "JAS"
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
				ba.Destination = "JAS" AND
				bd.Origin = "JAS" AND
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
	Vessel_Bed
FROM 
	Date_Calendar as d