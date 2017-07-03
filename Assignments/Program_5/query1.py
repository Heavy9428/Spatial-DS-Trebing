import os,sys
import math
from pymongo import MongoClient
import pygame
import json
from math import radians, cos, sin, asin, sqrt


class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()


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

    def get_doc_by_keyword(self,collection,field_name,search_key,like=True):
        """
        Finds "documents" with some keyword in some field.
        Params:
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
            res = self.client['world_data'][collection].find(({field_name : {'$regex' : ".*"+search_key+".*"}}))
        else:
            # This finds the records in which the field is equal to the search_key
            res = self.client['world_data'][collection].find({field_name : search_key})

        return self._make_result_list(res)


    def get_feature_in_poly(self,collection,poly):
        """
        Get features that are "in" a polygon
        Params:
            collection_name: e.g airports or meteors etc.
            poly: geojson polygon
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_feature_in_poly('airports',country['coordinates'])
            # Returns all airports in the given country polygon.
        """
        res = self.client['world_data'][collection].find( { 'geometry' : { '$geoWithin' : { '$geometry' : {'type': "Polygon", 'coordinates': poly }} } })

        print(dir(res))
        print(res.count())
        sys.exit()
        return self._make_result_list(res)

    def get_poly_by_point(self,collection,point):
        """
        Get a polygon that a point is within
        Params:
            collection_name: e.g airports or meteors etc.
            point: geojson point
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_poly_by_point('countries',[44.2968750,24.6669864])
            # Returns the country that point([44.2968750,24.6669864]) is within (Saudi Arabia)
        """
        return self.client['world_data'][collection].find_one({'geometry':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    def _make_result_list(self,res):
        """
        private method to turn a pymongo result into a list
        """
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_state_poly(self,state):
        """
        Send in a state name (e.g. Texas) or code (e.g. tx) and it returns the geometry
        """
        state = state.lower()
        if len(state) == 2:
            field = 'properties.code'
        else:
            state = state.capitalize()
            field = 'properties.name'

        state_poly = self.client['world_data']['states'].find_one({field : state})
        return state_poly['geometry']

    def get_country_poly(self,key):
        """
        Send in a country name (e.g. Belarus) or code (e.g. BLR) and it returns the geometry
        """
        if len(key) == 3:
            country_poly = self.client['world_data']['countries'].find_one({'properties.ISO_A3' : key})
        return country_poly['geometry']

    def _haversine(self,lon1, lat1, lon2, lat2):
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
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r

def run_tests():
    """
    Ok, not really "tests" but mostly just exmaples....
    """
    mh = mongoHelper()

    print("Getting airports near within 200 miles of: (-98.5034180, 33.9382331)")
    res = mh.get_features_near_me('airports',(-98.5034180, 33.9382331),200)
    print("Found %d airports" % len(res))
    print("")

    print("Getting countries that have 'High income' in the INCOME_GRP field.")
    res = mh.get_doc_by_keyword('countries','properties.INCOME_GRP','High income')
    print("Found %d countries" % len(res))
    print("")

    print("Getting earthquakes that had a magnitude of 5.5 (not a partial match like above), and don't pass in 5.5 as a string!")
    res = mh.get_doc_by_keyword('earthquakes','properties.mag',5.5,False)
    print("Found %d earthquakes" % len(res))
    print("")

    print("Getting a state polygon.")
    state = mh.get_state_poly('co')
    print("Found %d polygon in the result." % len(state['coordinates']))
    print("")

############################################
# Not 100% for those below. Going for beer, will work again tomorrow.

    print("Getting all airports within the state poly from the previous query.")
    res = mh.get_feature_in_poly('airports',state['coordinates'])
    print("Found %d airports in the polygon." % len(res))
    print("")
   
    country = mh.get_country_poly('DEU')

    print("Getting all airports within the country poly from the previous query.")
    res = mh.get_feature_in_poly('airports',country['coordinates'])
    print("Found %d airports in the polygon." % len(res))
    print("")

    res = mh.get_feature_in_poly('airports',country['coordinates'])
    print(len(res))

    res = mh.get_poly_by_point('countries',[44.2968750,24.6669864])
    print(res)


def mercator_projection(latlng,zoom=0,tile_size=256):
    x = (latlng[0] + 180) / 360 * tile_size
    y = ((1 - math.log(math.tan(latlng[1] * math.pi / 180) + 1 / math.cos(latlng[1] * math.pi / 180)) / math.pi) / 2 * pow(2, 0)) * tile_size
   
    return (x,y)

def mercX(lon):
    """
    Mercator projection from longitude to X coord
    """
    zoom = 1.0
    lon = math.radians(lon)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = lon + math.pi
    return int(a * b)


def mercY(lat):
    """
    Mercator projection from latitude to Y coord
    """
    zoom = 1.0
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return int(a * c)

def adjust_location_coords(extremes,points,width,height):
    """
    Adjust your point data to fit in the screen. 
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    maxx = float(extremes['max_x']) # The max coords from bounding rectangles
    minx = float(extremes['min_x'])
    maxy = float(extremes['max_y'])
    miny = float(extremes['min_y'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted = []

    for p in points:
        x,y = p
        x = float(x)
        y = float(y)
        xprime = (x - minx) / deltax         # val (0,1)
        yprime = ((y - miny) / deltay) # val (0,1)
        adjx = int(xprime*width)
        adjy = int(yprime*height)
        adjusted.append((adjx,adjy))
    return adjusted


if __name__=='__main__':
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    mh = mongoHelper()
    (width, height) = (1024,512)
    background_colour = (255,255,255)
    pygame.init()
    bg=pygame.image.load(DIRPATH +"\\World Map.png" )
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query')
    screen.fill(background_colour)
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    # Refresh screen
    '''Start = sys.argv[1]
    End =sys.argv[2]
    Miles = sys.argv[3]'''
    Start = 'DFW'
    Miles = 500
    start = mh.get_doc_by_keyword('airports','properties.ap_iata',Start)
    lat = start[0]['geometry']['coordinates'][0]#what the fuck is this shit i was stuck on this for hours
    lon = start[0]['geometry']['coordinates'][1]#basically everything is in one big list at [0] so you have to go through this shit
    lat = float(lat)
    lon = float(lon)
    point = lat,lon #this is the lat and lon for DFW

    #now we get all the shit that is close to us lets say 500 miles
    near = mh.get_features_near_me('earthquakes',point,Miles)
    near1 = mh.get_features_near_me('volcanos',point,Miles)
    closest_ap = mh.get_features_near_me('airports',point,Miles)

    points=[]
    allx=[]
    ally=[]
    for x in range(len(near)):
        lon=near[x]['geometry']['coordinates'][0]
        lat=near[x]['geometry']['coordinates'][1]
        x = mercX(lon)
        y = mercY(lat)
        allx.append(x)
        ally.append(y)
        point = (x,y)
        points.append(point)
    extremes = {}
    extremes['max_x'] = max(allx)
    extremes['min_x'] = min(allx)
    extremes['max_y'] = max(ally)
    extremes['min_y'] = min(ally)
    screen_width = 1024
    screen_height = 512
    point = adjust_location_coords(extremes,points,screen_width,screen_height)



    for y in range(len(near1)):
        print(near1[y]['properties']['Name'])
    
    for z in range(len(closest_ap)):
        print(closest_ap[z]['properties']['ap_name'])

    

    


    #now we need to look for a ait port that is 500 miles away
    running = True
    while running:
        for p in points:
            pygame.draw.circle(screen, (255,165,0), p, 1,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.display.flip()
    