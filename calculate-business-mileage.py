import json
import datetime
import re
import csv
import os
import pandas as pd

# location = "placeVisit"
address = input("Address to search: ")
miles = int(float(input("Distance in miles to address: ")))


print(f"Checking trips to '{address}'...")

for filename in os.listdir('.'):
	if filename.endswith(".json"):
		print(filename)
		with open(filename, 'r') as json_file:
			json_data = json.load(json_file)
			# Convert the JSON to a Python dictionary:
			objects = json_data['timelineObjects']
			
			# Write the data to a CSV '{address}.csv'
			addressfile = address + '.csv'
			with open(addressfile, mode='a', newline='') as locations_file:
				article_writer = csv.writer(locations_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				for places in objects:
					    if 'placeVisit' in places:
					        if 'name' in places['placeVisit']['location']:
					        	if address in places['placeVisit']['location']['address']:
						            location = places['placeVisit']['location']['address'].replace("\n",", ")
						            location = re.sub('[^\x00-\x7F]+', '', location)
						            ms = int(places['placeVisit']['duration']['startTimestampMs'])
						            stamp = datetime.datetime.fromtimestamp(ms/1000)
						            cleandate = stamp.strftime("%m/%d/%Y")
						            # print(f"{cleandate}" + ", " + f"{location}")
						            article_writer.writerow([cleandate, location])

# Clean up the resulting spreadsheet
df = pd.read_csv(addressfile,encoding = "ISO-8859-1")
rawtrips = len(df)
print(f"Found {rawtrips} visits to {address}...")
print("Sorting dates and removing duplicate trips to location...")
df.columns = ['Date', 'Location']
df = df.sort_values(by=['Date'])
df.drop_duplicates(subset="Date",inplace=True)
trips = len(df)
print(f"Found {trips} unique trips to {address}...")
print(f"Saving to file: {addressfile}")
df.to_csv(addressfile, index=False)
print("Summary:")
# 2 trips per visit (to/from home, {miles} miles per trip, $.58 per mile)
writeoff = trips * 2 * miles * .58
print(f"{trips} trips to '{address}' from home, at {miles} miles per trip, and $.58 per mile = ${writeoff}.")
