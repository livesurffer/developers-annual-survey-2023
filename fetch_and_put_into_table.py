#!/usr/bin/python
import csv
import psycopg2

db_params={"host":"127.0.0.1","database":"postgres","user":"barmin","password":"barmin"}

conn=psycopg2.connect(**db_params)
cur=conn.cursor()

csv_file='/home/acronym/data_analysis/developers_data_2023/csvdata/survey_results_public.csv'
table_name='devsurvey'

query = f"SELECT column_name FROM information_schema.columns WHERE table_name = 'devsurvey'"
cur.execute(query)
column_names = cur.fetchall()
column_names = [column[0] for column in column_names]
column_names_fin=column_names[1:]

columns_skip=[0,1,29,30,45,46,47,48,49,50]
columns_conv_int=[11,12,20,83]
data_for_insert=[]

with open(csv_file,newline='') as csvf:
	thereader=csv.reader(csvf)
	skipheader=next(thereader)
	for row in thereader:
		for i in columns_conv_int:
			try:
				if row[i]!='NA':
					row[i]=int(row[i])
				else:
					row[i]=None
			except ValueError:
				row[i]=None
		filter_row = [row[i] for i in range(len(row)) if i not in columns_skip]		
		data_for_insert.append(filter_row)
	column_placeholder = ','.join(['%s'] * len(filter_row))

	insert_query = f"INSERT INTO {table_name} ({','.join(column_names_fin)}) VALUES ({column_placeholder})"
	cur.executemany(insert_query, data_for_insert)
	
conn.commit()

cur.close()
conn.close()		
