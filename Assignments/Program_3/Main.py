import pygame
import sys,os
import json
import random
import time

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

if __name__=='__main__':
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    background_colour = (255,255,255)
    black = (0,0,0)

    (width, height) = (1024,512)
    pygame.init()
    bg=pygame.image.load(DIRPATH +"\\World Map.png" )
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MBRs')
    screen.fill(background_colour)
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    f = open(DIRPATH +'/'+'Adjusted_JSON_Files'+'/'+'quakes-adjusted.json','r')
    points = json.loads(f.read())
    orange=(255,165,0)

    running = True
    delay=1
    while running:
        for p in points[:delay]:
            pygame.draw.circle(screen, orange, p, 1,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.image.save(screen,DIRPATH+'/'+'screen_shot.png')
# '''            if event.type == pygame.MOUSEBUTTONDOWN:
#                 clean_area(screen,(0,0),width,height,(255,255,255))'''
        delay+=1
        pygame.display.flip()
        pygame.time.wait(45)