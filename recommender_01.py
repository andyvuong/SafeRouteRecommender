#!/usr/bin/python
# -*- coding: utf-8 -*-
import googlemaps
from googlemaps import Client as client
import json
from pygeocoder import Geocoder
import math
from array import array 
import sys


def readInJSON():

    # reading in the crimes from the crimes.json file

    filepath ="crimes.json"
    crimes = open(filepath)
    data = json.load(crimes)
    i = 0
    lat = []
    lon = []
    assaultCrimes = []
    vehicleTheftCrimes = []
    while i < len(data):
        lat.append(data[i]['lat'])
        lon.append(data[i]['lng'])
        if data[i]['type'] == 'ASSAULT':
            assaultCrimes.append(data[i])
        elif data[i]['type'] == 'VEHICLE THEFT':
            vehicleTheftCrimes.append(data[i])
        i = i + 0x1

    # created the list of lat/lon tuples of the assault crimes

    aclocations = []
    for crime in assaultCrimes:
        loc = []
        loc.append(crime['lat'])
        loc.append(crime['lng'])
        aclocations.append(loc)
    
    '''
    extraloc = []
    extraloc.append(40.11403)
    extraloc.append(-88.224)
    aclocations.append(extraloc)
    '''
    return aclocations


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

        split_after = not value & 0x20
        value &= 0x1F

        coord_chunks[-0x1].append(value)

        if split_after:
            coord_chunks.append([])

    del coord_chunks[-0x1]

    coords = []

    for coord_chunk in coord_chunks:
        coord = 0

        for (i, chunk) in enumerate(coord_chunk):
            coord |= chunk << i * 5

        # there is a 1 on the right if the coord is negative

        if coord & 0x1:
            coord = ~coord  # invert
        coord >>= 0x1
        coord /= 100000.0

        coords.append(coord)

    # convert the 1 dimensional list to a 2 dimensional list and offsets to
    # actual values

    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 0x1, 2):
        if coords[i] == 0 and coords[i + 0x1] == 0:
            continue

        prev_x += coords[i + 0x1]
        prev_y += coords[i]

        # a round to 6 digits ensures that the floats are the same as when
        # they were encoded

        points.append((round(prev_x, 6), round(prev_y, 6)))

    return points


def checkIfSafe(point, crimes):
    for crime in crimes:
        if crime[1] == point[0] and crime[0] == point[1]:
            return False
    return True

def lonlatdist(lon1,lat1,lon2,lat2):
    R = 6371; #in km
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    #print(type(dlon))
    #print(type(dlat))
    a = math.pow((math.sin(dlat/2)),2) + math.cos(lat1) * math.cos(lat2) * math.pow((math.sin(dlon/2)),2)
    #print(type(a))
    #print(a)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) ) 
    d = R * c 
    #'''(where R is the radius of the Earth)'''
    return d;

def getdistfm(lon, lat, r, dir):   
    xdir, ydir = dir;
    iny = 111111 #in meters for 1 degree of lat
    inx = iny*math.cos(lat) #in meters for 1 degree of lon
    lat_y = r/float(iny);
    lon_x = r/float(inx);
    #print("The lon change is -> ")
    #print(lon_x)
    #print("The lat change is -> ")
    #print(lat_y)    
    return (lat+(ydir*lat_y), lon+(xdir*lon_x))
    #earth_r = 6371;
    #d = r/earth_r;
    #c = d/2; #c is math.tan2(math.sqrt(a), math.sqrt(1-a))
    #math.at

def choose_best_path(listpaths, dangerpoint, waypointslist):
    max_closest_dist = -1;
    max_closest_pathindx = -1;
    for indx in range(len(listpaths)):
        closest_dist = 100000;
        for point in listpaths[indx]:
            dist = lonlatdist(point[0],point[1],dangerpoint[0],dangerpoint[1])
            if(dist < closest_dist):
                closest_dist = dist 
        if(closest_dist > max_closest_dist):
            max_closest_dist = closest_dist
            max_closest_pathindx = indx

    #print(max_closest_dist)
    return listpaths[max_closest_pathindx], waypointslist[max_closest_pathindx]

def checkPathSafe(mainPath, aclocations):
    for i in range(len(mainPath)):
        #print(lonlatdist(mainPath[i][0],mainPath[i][1],mainPath[i-1][0],mainPath[i-1][1]))
        if checkIfSafe(mainPath[i], aclocations) == True:
                #print("The point: " + str(mainPath[i]) + "was added to the route")
                continue;
        else:
            return (i, False);

    return (len(mainPath), True);
        
def createRoutewithwaypoints(client, dangerpoint, waypoints, aclocations, sp, ep):
    #print("WE ARE CURRENTLY ENTERING CREATEROUTEWWAYP")
    k = 25 # in meters
    dirs = []  
    pathlist = []
    waypoints_inner = []
    waypointslist = []
    dirs.append((1,1))
    dirs.append((1,-1))
    dirs.append((-1,1))
    dirs.append((1,-1))
    for dir in dirs:
        #print("This is the dangerpoint")
        #print(dangerpoint)        
        adj_point = getdistfm(dangerpoint[0],dangerpoint[1],k,dir)
        waypoints_inner = waypoints + [adj_point]
        waypointslist.append(waypoints_inner);
        #print("This is the waypoints")
        #print(waypoints_inner)
        directionsObject = client.directions(origin=sp, destination=ep, mode='walking', waypoints=waypoints_inner, alternatives = True)
        if(len(directionsObject) >= 1):           
           pathlist.append(decode(directionsObject[0]['overview_polyline']['points']))
           #print("The pathlist is -----------------------------------------------------------------------------------------> \n")
           #print(pathlist)
        else:
            print("WE ARE GETTING 000000! ---------------------------------------------------------------------------------->\n")

    newpath, wp = choose_best_path(pathlist,dangerpoint,waypointslist)
    #print("This is NEW PATH -----------------------------------------------************************************************---------------->")
    #print(newpath)
    return createRoute(client, sp, ep, newpath, wp , aclocations)

def createRoute(client, startpoint, endpoint, mainPath, waypoints, aclocations):
    i, succ = checkPathSafe(mainPath, aclocations);
    if(succ):
        #print("This is the FINAL PATH:")
        #print(mainPath);
        return mainPath
    else:
        #print("The point: " + str(mainPath[i]) + "was not added to the route")
        return createRoutewithwaypoints(client,mainPath[i], waypoints, aclocations, startpoint, endpoint)

def main():
    startAddress = sys.argv[1]
    endAddress = sys.argv[2]
    aclocations = []
    aclocations = readInJSON()
    aclocations = aclocations + [[40.11351,-88.22807]] + [[40.11449,-88.2243]];

    client = \
        googlemaps.Client(key='AIzaSyDAszXFz4LjQQ6Itr4o7O90RUJhUhhnXXI')
    finalRoute = []
    waypoints = []
    directionsObject = client.directions(origin=startAddress,
            destination=endAddress, mode='walking', alternatives = True)
    mainPath = decode(directionsObject[0]['overview_polyline']['points'])
    theRoute = createRoute(client, startAddress, endAddress, mainPath, [], aclocations)
    print (theRoute)                                 



if __name__ == '__main__':
    main()

        