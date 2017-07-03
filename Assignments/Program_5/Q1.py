import os
import sys
import math
from pymongo import MongoClient
import pygame
import json
from math import radians, cos, sin, asin, sqrt


class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()
    def get_doc_by_keyword(self, collection, field_name, search_key, like=True):
        """
        Finds "documents" with some keyword in some field.
        Pams:
        collection_name: e.g airports or meteors etc.
        field_name: key name of the field to search. e.g. 'place_id' or 'magnitude' 
        search_key: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
        mh = mongoHelper()
        feature_list = mh.get_doc_by_keyword('earthquakes','properties.type','shakemap')
        # Returns all earthquakes that have the word 'shakemap' somewhere in the 'type' field
        """
        if like:
            # This finds the records in which the field just "contains" the search_key
            res = self.client['world_data'][collection].find(({field_name: {'$regex': ".*" + search_key + ".*"}}))
        else:
            # This finds the records in which the field is equal to the search_key
            res = self.client['world_data'][collection].find({field_name: search_key})
        return self._make_result_list(res)
    
    def get_features_near_me(self,collection,point,radius,earth_radius=3963.2): #km = 6371
        """
        Finds "features" within some radius of a given point.
        Params:
            collection_name: e.g airports or meteors etc.
            point: e.g (-98.5034180, 33.9382331)
            radius: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            loc = (-98.5034180, 33.9382331)
            miles = 200
            feature_list = mh.get_features_near_me('airports', loc, miles)
        """
        x,y = point


        res = self.client['world_data'][collection].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , radius/earth_radius ] } }} )
        
        return self._make_result_list(res)

    def _make_result_list(self,res):
        """
        private method to turn a pymongo result into a list
        """
        res_list = []
        for r in res:
            res_list.append(r)
        return res_list



    #Had to swith because geo json does lon lat
    def calculate_initial_compass_bearing(self,pointA, pointB):
        """
        Calculates the bearing between two points.

        The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
        cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

        :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

        :Returns:
        The bearing in degrees

        :Returns Type:
        float
        """
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])

        diffLong = math.radians(pointB[1] - pointA[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)* math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing

if __name__=='__main__':

    ap_Visited=[]
    updated_list =[]
    new_ap=[]
    ap_lvl_list =[]
    ap_lvl_list_secondary=[]

    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    mh = mongoHelper()
    Current_airport = 'DFW'
    End = 'MNL'
    Distance = 500


    Current_airport = mh.get_doc_by_keyword('airports','properties.ap_iata',Current_airport)
    End = mh.get_doc_by_keyword('airports','properties.ap_iata',End)

    #gets inital airport and adds it to the list 
    #so it is not found again
    current= Current_airport[0]['properties']['ap_iata']
    current_lon = Current_airport[0]['geometry']['coordinates'][0] 
    current_lat = Current_airport[0]['geometry']['coordinates'][1] 

    End_airport = End[0]['properties']['ap_iata']
    End_lon = End[0]['geometry']['coordinates'][0]
    End_lat = End[0]['geometry']['coordinates'][1]

    current_lon = float(current_lon)
    current_lat = float(current_lat)
    current_point = current_lon,current_lat

    End_lon = float(End_lon)
    End_lat = float(End_lat)
    End_Point = End_lon , End_lat
    direction = mh.calculate_initial_compass_bearing(current_point,End_Point) # calculate the end point to find direction?

    while current != End_airport:

        Current_airport = mh.get_doc_by_keyword('airports','properties.ap_iata',current)
        current_lon = Current_airport[0]['geometry']['coordinates'][0] 
        current_lat = Current_airport[0]['geometry']['coordinates'][1] 
        current_lon = float(current_lon)
        current_lat = float(current_lat)
        current_point = current_lon,current_lat
        ap_Visited.append(Current_airport[0])
        #gets all the airports within 500 mile -radius
        Other_Airports = mh.get_features_near_me('airports',current_point,Distance)

        #find the next airport
        for x in range(len(Other_Airports)):
            if Other_Airports[x]['properties']['ap_iata'] != current:
                updated_list.append(Other_Airports[x])
            else:
                pass

        for z in range(len(updated_list)):
            Other_AP_lon = updated_list[z]['geometry']['coordinates'][0] 
            Other_Ap_lat = updated_list[z]['geometry']['coordinates'][1]
            Other_AP_lon = float(Other_AP_lon)
            Other_Ap_lat = float(Other_Ap_lat)
            Other_AP_Point = Other_AP_lon,Other_Ap_lat
            #print(Other_Airports[x]['properties']['ap_iata'])
            travel_path = mh.calculate_initial_compass_bearing(current_point,Other_AP_Point)
            #print(travel_path)
            if direction > travel_path:
                new_ap.append(updated_list[z])
            else: #thhink this is messing up
                pass

        for u in range(len(new_ap)):
            ap_lvl = new_ap[u]['properties']['ap_level']
            if int(ap_lvl) == 1:
                ap_lvl_list.append(new_ap[u])
            else:
                ap_lvl_list_secondary.append(new_ap[u])



       #find the highest elevation
        if (len(ap_lvl_list)) != 0:
            if (len(ap_lvl_list)) <1:
                for g in range(len(ap_lvl_list)):
                    Current_airport = min(ap_lvl_list[g]['properties']['elevation'])
            else:
                Previous_airport = Current_airport
                current = ap_lvl_list[0]['properties']['ap_iata']


        if(len(ap_lvl_list)) == 0:

            if(len(ap_lvl_list_secondary)) < 1:
                for p in range(len(ap_lvl_list_secondary)):
                    Current_airport=min(ap_lvl_list_secondary[p]['properties']['elevation'])
            else:
                current = ap_lvl_list_secondary[0]['properties']['ap_iata']

        ap_lvl_list.clear()
        ap_lvl_list_secondary.clear()
        updated_list.clear()
        new_ap.clear()
        print(current)
