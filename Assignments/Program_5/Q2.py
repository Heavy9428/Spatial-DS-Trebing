import os
import sys
from mongo_helper import *
import pygame
from map_helper import *


def mercX(lon, zoom=1):
    """
    """
    lon = math.radians(lon)
    a = (256 / math.pi) * pow(2, zoom)
    b = lon + math.pi
    return a * b


def mercY(lat, zoom=1):
    """
    """
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return (a * c)


def mercToLL(point):
    lng, lat = point
    lng = lng / 256.0 * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * lat / 256.0
    lat = (180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
    return (lng, lat)


def toLL(point):
    x, y = point
    return mercToLL((x / 4, y / 4))

def get_location(points):
    pointz=[]
    for x in range(len(points)):
        lon = points[x]['geometry']['coordinates'][0]
        lat = points[x]['geometry']['coordinates'][1]
        lon = float(lon)
        lat = float(lat)
        pointz.append((lon,lat))
    return pointz

def normalize_points(Ney_york_list,width,height):
    """
    Corrects the data we retrived and sets it to fit in our
    pygame screen
    Args:
        New_York_List:A list that contains x and y coordinats of floating point variables
        Width and Height: The size of the screen
    Returns:
        a list of ints containing the corrected values to fit on our x and y screen
    """


    full_list=[]
    MaxX = float(-999999999)
    MaxY = float(-9999999999)
    MinX = float(9999999999)
    MinY = float(9999999999)

    for point in Ney_york_list:
        x,y=point
        if x > MaxX:
            MaxX = x
        if y > MaxY:
            MaxY = y
        if x< MinX:
            MinX = x
        if y < MinY:
            MinY = y
        
    
    for point in Ney_york_list:
        x,y=point
        New_X = float(((x - MinX) / (MaxX - MinX))*width)
        New_Y = float((1-(y - MinY)/(MaxY - MinY))*height)
        New_X = int(New_X)
        New_Y = int(New_Y)
        full_list.append((New_X, New_Y))
    return full_list
                      


DIRPATH = os.path.dirname(os.path.realpath(__file__))
mh = MongoHelper()
Things = []
Updated_List = []
background_colour = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (70, 173, 212)
green = (76, 187, 23)
(width, height) = (1024, 512)
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
bg = pygame.image.load(DIRPATH + "\\World Map.png")
pygame.display.set_caption('Q2, Nearest Neighbor')
pygame.display.flip()
screen.blit(bg, (0, 0))
features = ['volcanos', 'meteorite', 'earthquakes']
running = True
world={}
a=1
while running:
    for event in pygame.event.get():
        if a== 1:
            radius = 2000
            x= 140
            y = 72
            #radius = int(sys.argv[0])
            max_result = 500
            #x, y = pygame.mouse.get_pos()  # need to get a x and y
            lon,lat = toLL((x, y))
        for f in features:
            points =[]
            updated_points =[] 
            points = mh.get_features_near_me(f,(lon, lat),radius)
            updated_points = get_location(points)
            world[f] = updated_points
        for featurez in world:
           world[featurez] = normalize_points(world[featurez],width,height)

        if len(sys.argv) == 5:
            feature = sys.argv[0]
            field = sys.argv[1]
            field_value = sys.argv[2]
            min_max = sys.argv[3]
            max_result = int(sys.argv[4])
            radius = int(sys.argv[5])
            lon, lat = eval(sys.argv[6])
            # Test Cases
            # feature = "volcanos"
            # field = 'Altitude'
            # field_value = 3000
            # min_max = "min"
            # max_result = 20
            # radius = 1000
            # lon,lat = 42.9,40.75
            Things = mh.get_features_near_me(feature, (lon, lat), radius)
            for x in Things:
                if min_max == 'min':
                    if (x['properties'][field]) > str(field_value):
                        Updated_List.append(x)
                if min_max == 'max':
                    if (x['properties'][field]) < str(field_value):
                        Updated_List.append(x)
            extremes, points = change_points(Updated_List, width, height)
            Update[feature] = adjust_location_coords(extremes, points, width, height)

        for p in range(len(world[features])):
            if feature == 'volcanos':
                pygame.draw.circle(screen, red, p, 2, 0)
            if features == 'earthquakes':
                pygame.draw.circle(screen, blue, world[features][p], 2, 0)
            if feature == 'meteorite':
                pygame.draw.circle(screen, green, p, 2, 0)
        if event.type == pygame.QUIT:
            running = False
            pygame.image.save(screen, DIRPATH + '/' + 'screen_shot.png')
        pygame.display.flip()
