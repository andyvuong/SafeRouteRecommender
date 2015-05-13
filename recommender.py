#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
' Note this file is the same as the algorithms script, just edits to make it work
' with the server and to take inputs. Also helps avoid conflicts on github.
'''
import googlemaps
from googlemaps import Client as client
import json
from pygeocoder import Geocoder
import math
import sys


def readInJSON():

    # reading in the crimes from the crimes.json file
    # ~/dev/courses/uiuc_cs410/SafeRouteRecommender/crimes.json
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
    extraloc = []
    extraloc.append(40.11403)
    extraloc.append(-88.224)
    aclocations.append(extraloc)
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


def createRoute(startpoint, endpoint, aclocations):
    client = \
        googlemaps.Client(key='AIzaSyDAszXFz4LjQQ6Itr4o7O90RUJhUhhnXXI')
    finalRoute = []
    directionsObject = client.directions(origin=startpoint,
            destination=endpoint, mode='walking')
    mainPath = decode(directionsObject[0]['overview_polyline']['points'])
    i = 0
    for point in mainPath:
        i = i+1
        if checkIfSafe(point, aclocations) == True:
            finalRoute.append(point)
            #print finalRoute
        else:
            '''
            print(aclocations)
            print("\n")
            print mainPath
            print("We have reached to point" + str(point))
            print("The point before this is: " + str(mainPath[i-2]))
            print("The point after this is: " + str(mainPath[i]))
            '''
            tup1 = []
            tup1.append(mainPath[i-2][1])
            tup1.append(mainPath[i-2][0])
            tup2 = []
            tup2.append(mainPath[i][1])
            tup2.append(mainPath[i][0])

            #print mainPath[i-1]
            #print mainPath[i+1]
            #finalRoute.append(createRoute(mainPath[point-1], mainPath[point+1], aclocations))
            #print("The point in the mainpoints that has an issue is: " + str(point))
            #finalRoute.append(createRoute(mainPath[i-2], mainPath[i], aclocations))
            directionsObject2 = client.directions(origin = tup1, destination = tup2, mode = 'walking', alternatives = True)
            routeAgain = decode(directionsObject2[0]['overview_polyline']['points'])
            for point in routeAgain:
                finalRoute.append(point)
    return finalRoute


# takes two arguments
# start address
# end address
# run: "recommender.py arg1 arg2"
def main():
    startAddress = sys.argv[1]
    endAddress = sys.argv[2]
    aclocations = []
    aclocations = readInJSON()
    theRoute = createRoute(startAddress, endAddress, aclocations) 
                                        #sp = '208 N. Harvey Urbana IL 61801'
                                        #ep = '201 N. Goodwin Avenue Urbana IL 61801'
                                        #this function will take in the startpoint and endpoint, convert them to lat/lon, call the google maps directions method,
                                        # which will return an encoded overview_polyline string of directions, the decode function will decode it and return a list
                                        #of waypoints. Then I will pass each waypoint to the checkIfSafe function which will do a lat/lon comparison to all the crime 
                                        #scene points. If the waypoint does not match the crime points, then the waypoint will be added to the finalRoute. However, if 
                                        #the waypoint does match one of the crime scenes, then we will try to find an alternate route between the previous point and next point,
                                        #hopefully avoiding the crime point. 
                                        #print aclocations
    # Leave this, returns a "message" to pythonshell
    print(theRoute)

if __name__ == '__main__':
    main()

        