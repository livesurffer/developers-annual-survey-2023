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

query = "SELECT country, COUNT(*) AS count FROM devsurvey GROUP BY country ORDER BY count ASC;"

cursor.execute(query)
data = cursor.fetchall()

cursor.close()
connection.close()

#Extract country names and counts into separated lists 
countries, counts = zip(*data)

#Calculate sum of counts all developers
total_developers = sum(counts)

#Calculate percentages for each count
percentages = [count / total_developers * 100 for count in counts]

# Filter countries with percentages >= 2%. The reason: there are a lot of countires and no sence to show all of them on graphic
filtered_countries = []
filtered_percentages = []
excluded_countries = []

for country, percentage in zip(countries, percentages):
    if percentage >= 2:
        filtered_countries.append(country)
        filtered_percentages.append(percentage)
    else:
        excluded_countries.append((country, percentage))  #Store as tuple for sorting later

# Sort excluded countries by percentage in descending order and use lambda to apply sorting to second element - percentage
excluded_countries.sort(key=lambda x: x[1], reverse=True)

#Create the pie chart only with filtered data
#pie chart size 
plt.figure(figsize=(10, 10))  
plt.pie(filtered_percentages, labels=filtered_countries, autopct='%1.4f%%', startangle=140)

plt.title('Proportion of developers residing in each specific country based on developers-annual-survey-2023 StackOverFlow')
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

# Save the pie chart png format
plt.savefig('/home/acronym/data_analysis/developers_data_2023/csvdata/pie_chart_devel_country.png')

#excluded countries with percentages less than 2%
excluded_countries_text = "\n".join([f"{country}: {percentage:.4f}%" for country, percentage in excluded_countries])

# separate plot for the sorted list of excluded countries
plt.figure(figsize=(8, 4))
plt.text(0, 0, f"Countries with < 2%:\n{excluded_countries_text}", fontsize=10, ha='left')
#off axis
plt.axis('off')

# Save the sorted list of excluded countries png format
plt.savefig('/home/acronym/data_analysis/developers_data_2023/csvdata/excluded_countries_list.png', bbox_inches='tight')

