from dbscan import *
from pymongo import mongo_client
import math
from math import radians, cos, sin, asin, sqrt
import sys,os
from mongo_helper import *
from map_helper import *
import pygame 

DIRPATH = os.path.dirname(os.path.realpath(__file__))
mh = MongoHelper()
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)
points=[]
new_list =[]
#Pygame initalization
pygame.init()
bg = pygame.image.load(DIRPATH+'/1024x512.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Query 3 ')
screen.fill(background_colour)
pygame.display.flip()

feature = sys.argv[1]
min_pts = int(sys.argv[2])
eps = int(sys.argv[3])

screen.blit(bg, (0, 0))
pygame.display.flip()
#gets the list of items, gets all of them
Results = mh.client['world_data'][feature].find()
#using modified code from program 3 you get the extreme values and the points
extremes,points = change_points(Results,width,height)
#using the extreme value and points we adjust where they are placed becasue json are lon lat and not x and y 
points = adjust_location_coords(extremes,points,width,height)
#code given to us by the proffessor in program 3
#json files points seem to be getting hung up here
mbrs = calculate_mbrs(points,eps,min_pts)
del mbrs[-1]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for p in points:
            pygame.draw.circle(screen,(0,0,225) , p, 2,0)
        for x in range(5):
            pygame.draw.polygon(screen,(128,0,128) , mbrs[x], 2)
            pygame.display.flip()
        pygame.image.save(screen, DIRPATH+'/Query3.png')