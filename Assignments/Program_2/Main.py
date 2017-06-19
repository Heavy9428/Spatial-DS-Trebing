"""
Program:
--------
    Program 2A - 

Description:
------------
    Reads in multiple files to get their x and y coordinates
    to then be stored in a dictonary to print out 
    
Name: Matthew Trebing
Date: 19 June 2017
"""
import pygame
import random
from dbscan import *
import sys,os
import pprint as pp
import read_crime_data
import math
DIRPATH = os.path.dirname(os.path.realpath(__file__))

def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    # for id,cpoints in clusters.items():
    #     xs = []
    #     ys = []
    #     for p in cpoints:
    #         xs.append(p[0])
    #         ys.append(p[1])
    #     max_x = max(xs) 
    #     max_y = max(ys)
    #     min_x = min(xs)
    #     min_y = min(ys)
    #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    # return mbrs

    """
    Using list index value to iterate over the clusters dictionary
    Does same as above
    """
    
    for id in range(len(clusters)-1):
        xs = []
        ys = []
        for p in clusters[id]:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs


def get_location(Crime_Location):
    """Get's the x and y coordinates from the files.
    Args:
        Crime_Locations:A list that contains info in a CSV file, not all of it is needed
    Returns:
        a list of floats to be used in calculations during a later part of the program
    """
    points=[]
    for i in Crime_Location:
        if i[19]!= "" or i[20] !="":
            x = i[19]
            y = i[20]
            x=float(x)
            y=float(y)
            points.append((x,y))
        else:
            pass
    return points

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
    MaxX = float(1067226)
    MaxY = float(271820)
    MinX = float(913357)
    MinY = float(121250)

    for x,y in Ney_york_list:
        New_X = float(((x - MinX) / (MaxX - MinX))*width)
        New_Y = float((1-(y - MinY)/(MaxY - MinY))*height)
        New_X = int(New_X)
        New_Y = int(New_Y)
        full_list.append((New_X, New_Y))
    return full_list


def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)


#RBG values for various colors to be used
background_colour = (255,255,255)
black = (0,0,0)
firebrick = (194,35,38)
tomato = (243,115,56)
goldenrod = (253,182,50)
teal = (2,120,120)
brown = (128,22,56)
(width, height) = (1000, 1000)

#list of locations names to be used in our file 
location =['bronx','brooklyn','manhattan','queens','staten_island']

#dictonary that will hold points from all the files
New_York_Map={}

pygame.init()
Display_Font = pygame.font.get_default_font()
DF = pygame.font.SysFont(Display_Font,30)
label = DF.render("Program 2A", 1, black)
label1=DF.render("Matthew Trebing",1,black)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Line')
screen.fill(background_colour)

pygame.display.flip()

epsilon = 20
min_pts = 5.0

#For loop the will use lists to hold data 
#from each file temporarly and get their
#x and y coordinates from the list until 
#it is placed in a dictonary that will hold all 5 of the files points
for i in location:
    points = []
    Updated_Points = []

    #Reads the data from a specific file from the read_crime_data
    # file and adds all of the data and place it into points 
    points = read_crime_data.read_crime_data_location('/'+'filtered_crimes_'+ i +'.csv')

    #Takes the points and removes them from the full CSV file
    # and returns a float representation of the x and y coord
    Updated_Points = get_location(points)

    #Updated_Points = MaxMin(Updated_Points,width,height)

    #Keeps each file's points in a dictonary and using the location,i,
    #to hold the correct location
    New_York_Map[i] = Updated_Points

#loop that uses the location names to normalize the points to our map
# to keep it bounded it in our window
for location in New_York_Map:
    New_York_Map[location] = normalize_points(New_York_Map[location],width,height)

    #loop that goes over the length of the dictonary of points
    #then uses the location "key" to print the point out in the correct 
    # color this continues through
    for i in range(len(New_York_Map[location])):
            if location == 'bronx':
                pygame.draw.circle(screen, teal, New_York_Map[location][i], 2, 0)
            if location == 'brooklyn':
                pygame.draw.circle(screen, brown, New_York_Map[location][i], 2, 0)
            if location == 'manhattan':
                pygame.draw.circle(screen, firebrick, New_York_Map[location][i], 2, 0)
            if location == 'queens':
                pygame.draw.circle(screen, tomato, New_York_Map[location][i], 2, 0)
            if location == 'staten_island':
                pygame.draw.circle(screen, goldenrod, New_York_Map[location][i], 2, 0)

#mbrs = calculate_mbrs(Updated_Points, epsilon, min_pts)

running = True
while running:
    screen.blit(label, (100, 100))
    screen.blit(label1,(100,120))
    #pygame.draw.circle(screen, (2,120,120), p, 3, 0)
    #for mbr in mbrs:
        #pygame.draw.polygon(screen, black, mbr, 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen,DIRPATH+"\\all_buroughs_screen_shot.png")
            running = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     clean_area(screen,(0,0),width,height,(255,255,255))
        #     points.append(event.pos)
        #     mbrs = calculate_mbrs(Updated_Points, epsilon, min_pts)
    pygame.display.flip()