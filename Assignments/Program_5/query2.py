import os
import sys
from mongo_helper import *
import pygame
from map_helper import *
def mercToLL(point):
   lng, lat = point
   lng = lng / 256.0 * 360.0 - 180.0
   n = math.pi - 2.0 * math.pi * lat / 256.0
   lat = (180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
   return (lng, lat)

def toLL(point):
   x, y = point
   y+=256
   return mercToLL((x / 4, y / 4))

DIRPATH = os.path.dirname(os.path.realpath(__file__))
mh = MongoHelper()
Things = []
Updated_List=[]
Updated_List_dict = {}
background_colour = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (70, 173, 212)
green = (76, 187, 23)
(width, height) = (1024, 512)
pygame.init()
bg = pygame.image.load(DIRPATH + "\\1024x512.png")
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption('Q2, Nearest Neighbor')
pygame.display.flip()

#if everything is passed but the lat and lon
if len(sys.argv)==7:
   feature = sys.argv[1]
   field = sys.argv[2]
   field_value = int(sys.argv[3])
   min_max = sys.argv[4]
   max_result = int(sys.argv[5])
   radius = int(sys.argv[6])
#only the radius is passed
if len(sys.argv) == 2:
       max_result = 20
       radius = int(sys.argv[1])

#needs to stop so we can click the map
mouse_click=False
screen.blit(bg,(0,0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.image.save(screen, DIRPATH + '/' + 'Query2.png')
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_click == False:
            point = pygame.mouse.get_pos()
            lon,lat = toLL(point)
            mouse_click = True
            print (lon,lat)


        if len(sys.argv) == 2 and mouse_click == True:
            features = ['volcanos', 'earthquakes','meteorites']
            for z in features:
                Things= mh.get_features_near_me(z, (lon, lat), radius)  
                extremes, points = change_points(Things, width, height)
                Updated_List= adjust_location_coords(extremes, points, width,height)
                Updated_List_dict[z]=Updated_List


        if len(sys.argv)==7 and mouse_click ==True:
            Things = mh.get_features_near_me(feature, (lon, lat), radius)
            features = [feature]
            for x in Things:
                if type(x['properties'][field])is int:
                    field_value = int(field_value)
                if type(x['properties'][field]) is str:
                    field_value=str(field_value)

                if min_max == 'min':
                    if (x['properties'][field]) > (field_value):
                        Updated_List.append(x)
                if min_max == 'max':
                    if (x['properties'][field]) < (field_value):
                        Updated_List.append(x)


            extremes, points = change_points(Updated_List, width, height)
            Updated_List = adjust_location_coords(extremes, points, width,height)
            Updated_List_dict[feature]=Updated_List

        if mouse_click ==True:
            for y in features:
                for x in Updated_List_dict[y]:
                    if y == 'volcanos':
                        pygame.draw.circle(screen,red,x, 2, 0)
                    if y == 'earthquakes':
                        pygame.draw.circle(screen,blue,x, 2, 0)
                    if y == 'meteorites':
                        pygame.draw.circle(screen,green,x, 2, 0)
        
                pygame.display.flip()
                mouse_click = False