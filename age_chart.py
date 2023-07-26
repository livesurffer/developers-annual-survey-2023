#!/usr/bin/python
import psycopg2
import requests
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Connect to PostgreSQL and retrieve data from table
connection = psycopg2.connect(
    host="127.0.0.1",
    database="postgres",
    user="barmin",
    password="barmin",
    port="5432"
)
cursor = connection.cursor()

query = "SELECT age, COUNT(*) AS count FROM devsurvey GROUP BY age ORDER BY count ASC;"

cursor.execute(query)
data = cursor.fetchall()

age, number = zip(*data)
cursor.close()
connection.close()

total_number = sum(number)
percentage = [(i/total_number)*100 for i in number]

plt.figure(figsize=(15,10))
plt.bar(age, number, color='blue', edgecolor='black')
plt.tight_layout()

for i, count in enumerate(percentage):
    plt.text(age[i], number[i], f'{count:.2f}%', ha='center', va='bottom', fontsize=8)


plt.savefig('/home/acronym/data_analysis/developers_data_2023/histogram_age_developers.png')
plt.xlabel('age')
plt.ylabel('amount')
plt.title('Developer age')
