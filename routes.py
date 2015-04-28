from apiclient.discovery import build
import googlemaps
from googlemaps import Client as client
import json  

client = googlemaps.Client(key="AIzaSyDAszXFz4LjQQ6Itr4o7O90RUJhUhhnXXI")
#service = build('api_name', 'api_version', ...)


#mapService = Client()

directions = client.directions('201 N. Goodwin Avenue Urbana IL', '208 N. Harvey Urbana IL 61801 ', )

print directions

#listDir = json.load(directions)
#print listDir
#for step in directions['Directions']['Routes'][0]['Steps']:
#for step in directions:
#	print step[html_instructions]