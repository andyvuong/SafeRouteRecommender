from apiclient.discovery import build
import googlemaps
from googlemaps import Client as client
import json  


#be sure to install the Python client for the Google maps API, here is the link: https://developers.google.com/api-client-library/python/start/installation

#specifying the API key
client = googlemaps.Client(key="AIzaSyDAszXFz4LjQQ6Itr4o7O90RUJhUhhnXXI")
#reading in the crimes from the crimes.json file 
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

#created the list of lat/lon tuples of the assault crimes
aclocations =[]
for crime in assaultCrimes:
	loc = []
	loc.append(crime['lat'])
	loc.append(crime['lng'])
	aclocations.append(loc)


#created the list of lat/lon tuples of the vehicle theft crimes 
vtlocations =[]
for crime in vehicleTheftCrimes:
	loc = []
	loc.append(crime['lat'])
	loc.append(crime['lng'])
	vtlocations.append(loc)


#Google Maps API stores its' list of coordinates of a route in a unicode string so this function encodes a list of lat/lon points into a unicode string 
def encode_coords(coords):
    '''Encodes a polyline using Google's polyline algorithm
    
    See http://code.google.com/apis/maps/documentation/polylinealgorithm.html 
    for more information.
    
    :param coords: Coordinates to transform (list of tuples in order: latitude, 
    longitude).
    :type coords: list
    :returns: Google-encoded polyline string.
    :rtype: string    
    '''
    
    result = []
    
    prev_lat = 0
    prev_lng = 0
    
    for x, y in coords:        
        lat, lng = int(y * 1e5), int(x * 1e5)
        
        d_lat = _encode_value(lat - prev_lat)
        d_lng = _encode_value(lng - prev_lng)        
        
        prev_lat, prev_lng = lat, lng
        
        result.append(d_lat)
        result.append(d_lng)
    
    return ''.join(c for r in result for c in r)

#helper function used in _encode_coords
def _split_into_chunks(value):
    while value >= 32: #2^5, while there are at least 5 bits
        
        # first & with 2^5-1, zeros out all the bits other than the first five
        # then OR with 0x20 if another bit chunk follows
        yield (value & 31) | 0x20 
        value >>= 5
    yield value
 
 #helper function used in _encode_coords
def _encode_value(value):
    # Step 2 & 4
    value = ~(value << 1) if value < 0 else (value << 1)
    
    # Step 5 - 8
    chunks = _split_into_chunks(value)
    
    # Step 9-10
    return (chr(chunk + 63) for chunk in chunks)
 


#actually calling the directions method on the origin and destinatino 
directions = client.directions(origin = '201 N. Goodwin Avenue Urbana IL 61801', destination = '208 N. Harvey Urbana IL 61801', mode = "walking", alternatives = True)

#parsing the directions object (JSON) so we can return a list of lat/lon points 
point_str = (directions[0]['overview_polyline']['points'])
points = []

#function that decodes the unicode string that Google Maps returns as the encoded lat/lon route 
def decode(point_str):
    '''Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    
    This is a generic method that returns a list of (latitude, longitude) 
    tuples.
    
    :param point_str: Encoded polyline string.
    :type point_str: string
    :returns: List of 2-tuples where each tuple is (latitude, longitude)
    :rtype: list
    
    '''
            
    # sone coordinate offset is represented by 4 to 5 binary chunks
    coord_chunks = [[]]
    for char in point_str:
        
        # convert each character to decimal from ascii
        value = ord(char) - 63
        
        # values that have a chunk following have an extra 1 on the left
        split_after = not (value & 0x20)         
        value &= 0x1F
        
        coord_chunks[-1].append(value)
        
        if split_after:
                coord_chunks.append([])
        
    del coord_chunks[-1]
    
    coords = []
    
    for coord_chunk in coord_chunks:
        coord = 0
        
        for i, chunk in enumerate(coord_chunk):                    
            coord |= chunk << (i * 5) 
        
        #there is a 1 on the right if the coord is negative
        if coord & 0x1:
            coord = ~coord #invert
        coord >>= 1
        coord /= 100000.0
                    
        coords.append(coord)
    
    # convert the 1 dimensional list to a 2 dimensional list and offsets to 
    # actual values
    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue
        
        prev_x += coords[i + 1]
        prev_y += coords[i]
        # a round to 6 digits ensures that the floats are the same as when 
        # they were encoded
        points.append((round(prev_x, 6), round(prev_y, 6)))
    
    return points  



#prints out the list of points to go 
points = decode(point_str)
for point in points:
	print point


