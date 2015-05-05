import json
import xml.etree.ElementTree as ET
from math import radians, cos, sin, asin, sqrt

#make sure you have Python installed 



#This reads in the crimes.json file that contains the JSON data that was crawled from the UIUC crime map website 
#This creates two lists, one of assault crimes and one of vehicle crimes 
filepath = "C:\\Users\\Disha\\Desktop\\SafeRouteRecommender\\crimes.json"
crimes = open(filepath)
data = json.load(crimes)
i = 0
lat = []
lon = []
assaultCrimes =[]
vehicleTheftCrimes = []
while(i<len(data)):
	lat.append(data[i]["lat"])
	lon.append(data[i]["lng"])
	if(data[i]["type"]=="ASSAULT"):
		assaultCrimes.append(data[i])
	elif(data[i]["type"]=="VEHICLE THEFT"):
		vehicleTheftCrimes.append(data[i])
	i = i+1

print assaultCrimes

#finding the total range of the latitudes 
lat_min = lat[0]
lat_max = 0 
for i in lat:
	if(i>lat_max):
		lat_max = i
	if(i<lat_min):
		lat_min = i
	i= i+1


#finding the total range of longitudes 
lon_min = lon[0]
lon_max = lon[0] 
for i in lon:
	if(i>lon_max):
		lon_max = i
	if(i<lon_min):
		lon_min = i
	i= i+1



#we will find the range of the assault latitudes and longitudes 
assault_lats = []
assault_lons = []
j =0
while(j<len(assaultCrimes)):
	assault_lats.append(assaultCrimes[j]["lat"])
	assault_lons.append(assaultCrimes[j]["lng"])
	j = j+1


assault_lats_min = assault_lats[0]
assault_lats_max = 0 
for i in assault_lats:
	if(i>assault_lats_max):
		assault_lats_max = i
	if(i<assault_lats_min):
		assault_lats_min = i
	i= i+1



assault_lons_min = assault_lons[0]
assault_lons_max = assault_lons[0] 
for i in assault_lons:
	if(i>assault_lons_max):
		assault_lons_max = i
	if(i<assault_lons_min):
		assault_lons_min = i
	i= i+1


#print("The range of the assault latitudes is " + str(assault_lats_min)+  " to " + str(assault_lats_max))
#print("The range of the assault longitudes is " + str(assault_lons_min) + " to " + str(assault_lons_max))


#here we find the range of the vehicle theft latitudes and longitudes

VT_lats = []
VT_lons = []
k =0
while(k<len(vehicleTheftCrimes)):
	VT_lats.append(vehicleTheftCrimes[k]["lat"])
	VT_lons.append(vehicleTheftCrimes[k]["lng"])
	k = k+1


VT_lats_min = VT_lats[0]
VT_lats_max = 0 
for i in VT_lats:
	if(i>VT_lats_max):
		VT_lats_max = i
	if(i<VT_lats_min):
		VT_lats_min = i
	i= i+1



VT_lons_min = VT_lons[0]
VT_lons_max = VT_lons[0] 
for i in VT_lons:
	if(i>VT_lons_max):
		VT_lons_max = i
	if(i<VT_lons_min):
		VT_lons_min = i
	i= i+1


#print("The range of the vechicle theft latitudes is " + str(VT_lats_min)+  " to " + str(VT_lats_max))
#print("The range of the vehicle theft longitudes is " + str(VT_lons_min) + " to " + str(VT_lons_max))


# creating function to calculate distance between two GPS points, taken from here: http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    conversionFactorFromKMtoMiles = 0.62137
    miles = conversionFactorFromKMtoMiles*km
    return miles







'''
a = 0
templist = []
for key in locations:
	while(a<3):
		templist.append(locations[key])
		a = a+1


lat1= templist[0][0]
lon1 = templist[0][1]
lat2 = templist[1][0]
lon2 = templist[1][1]
#print type(lat1)

temp = haversine(float(lon1), float(lat1), float(lon2), float(lat2))
print temp
'''