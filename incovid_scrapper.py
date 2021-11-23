import pandas
import requests
import itertools
from datetime import date
from pandas import ExcelWriter
from rich.progress import track

url 	= 'https://data.incovid19.org/v4/min/timeseries.min.json'
writer 	= ExcelWriter(f'InCoVID_output_{str(date.today())}.xlsx')

try:
	response 	= requests.get(url , timeout = 200)
	data 		= response.json()
except Exception:
	print('URL not working try again later')

states  = list(data.keys())

# Get the starting date and ending date
dates = []
for i in states:
	dates.append(list(data[i]['dates'].keys()))

dates = list(itertools.chain(*dates))
date_range = pandas.date_range(start = min(dates), end = max(dates))


# Getting all possible values for the delta
type_of_cases = data['TT']['dates'][max(dates)]['delta'].keys()

# Entering the values into the dataframe
for case in type_of_cases:
	# Creating a dataframe with the dates in rows and states in columns
	output_df = pandas.DataFrame(index = date_range, columns = states)
	for i in track(states, description = f"Generating data for {case} cases"):
		for j in date_range:
			curr_date = str(j.date())
			try:
				output_df.loc[curr_date][i] = data[i]['dates'][curr_date]['delta'][case]
			except:
				output_df.loc[curr_date][i] = 0
	output_df.to_excel(writer, case, header = True)

writer.save()

	
