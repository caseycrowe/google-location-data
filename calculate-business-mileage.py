# Script to count how many times a person went to a specific address
# and on which date. Data is from Google Takeout. Export "Location History"
# and drop this script in the folder with the YYYY_MONTH.json files and
# run. It will prompt you for address and miles from home to location.

import json
import datetime
import re
import csv
import os
import pandas as pd

# location = "placeVisit"
address = input("Enter address to search: ")
miles = int(input("Enter distance in miles to address: "))



print(f"Checking trips to '{address}'...")

for filename in os.listdir('.'):
	if filename.endswith(".json"):
		print(filename)
		with open(filename, 'r') as json_file:
			json_data = json.load(json_file)
			# Convert the JSON to a Python dictionary:
			objects = json_data['timelineObjects']
			
			# Write the data to a CSV 'locations.csv'
			with open('locations.csv', mode='a', newline='') as locations_file:
				article_writer = csv.writer(locations_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				for places in objects:
					    if 'placeVisit' in places:
					        if 'name' in places['placeVisit']['location']:
					        	if address in places['placeVisit']['location']['name']:
						            location = places['placeVisit']['location']['name']
						            location = re.sub('[^\x00-\x7F]+', '', location)
						            ms = int(places['placeVisit']['duration']['startTimestampMs'])
						            stamp = datetime.datetime.fromtimestamp(ms/1000)
						            cleandate = stamp.strftime("%m/%d/%Y")
						            # print(f"{cleandate}" + ", " + f"{location}")
						            article_writer.writerow([cleandate, location])

# Clean up the resulting spreadsheet
df = pd.read_csv('locations.csv',encoding = "ISO-8859-1")
rawtrips = len(df)
print(f"Found {rawtrips} visits to {address}...")
print("Sorting dates and removing duplicate trips to location...")
df.columns = ['Date', 'Location']
df = df.sort_values(by=['Date'])
df.drop_duplicates(subset="Date",inplace=True)
trips = len(df)
print(f"Found {trips} unique trips to {address}...")
print("Saving to file: locations.csv")
df.to_csv('locations.csv', index=False)
print("Summary:")
# 2 trips per visit (to/from home, {miles} miles per trip, $.58 per mile)
writeoff = trips * 2 * miles * .58
print(f"{trips} trips to '{address}' from home, at {miles} miles per trip, and $.58 per mile = ${writeoff}.")


