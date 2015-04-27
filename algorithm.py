import json
import xml.etree.ElementTree as ET 

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



#Here we parse the XML data that I pulled from Open Street Map. I chose  a large portion of campus for sample data 
#The data was pushed to "smalldata.xml"



tree = ET.parse('smalldata.xml')
root = tree.getroot()

#create a dictionary of locations where the key is the node ID and the value is a tuple list of that nodes' latitude and longitude  
locations = {}
for childs in root:
	if(childs.tag == 'node'):
		lst = []
		lst.append(childs.attrib['lat'])
		lst.append(childs.attrib['lon'])
		locations[childs.attrib['id']] = lst
print locations


# create a dictionary called ways in which the key is the ID of the way, and the value is the list of nodes that are connected to form that way

ways = {}

for childs in root:

	if(childs.tag == 'way'):
		lst = []
		for children in childs:
			if(children.tag == 'nd'):
				lst.append(children.attrib['ref'])
		ways[childs.attrib['id']] = lst
#print ways




