A script to count how many times a person went to a specific address and on which date. Data is from Google Takeout. 

How to use:

3rd party libraries required: Pandas

1. Go to your own Google Takeout page: https://www.google.com/settings/takeout
2. Export "Location History" only
3. Once they email you the zip file, download and extract it
4. File structure/path will look like this:
  D:\takeout-20200710T233325Z-001\Takeout\Location History\Semantic Location History\2019
5. Drop this script in the folder with the YYYY_MONTH.json files (\Semantic Location History\YYY)
6. From that folder, run the file. 
7. It will prompt you for the address, and distance in miles from your house
8. It will then generate a .csv named after the address searched, and save it in that folder and print your results to the console.
