import pygame
import math
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

def crect(sc, col, center, w, h, ang):
	polygon(sc, col, [(center[0] + (w/2)*math.cos(math.radians(ang)) + (h/2)*math.cos(math.radians(ang+90)), center[1] - (w/2)*math.sin(math.radians(ang)) - (h/2)*math.sin(math.radians(ang+90))),
	(center[0] - (w/2)*math.cos(math.radians(ang)) + (h/2)*math.cos(math.radians(ang+90)), center[1] + (w/2)*math.sin(math.radians(ang)) - (h/2)*math.sin(math.radians(ang+90))),
	(center[0] - (w/2)*math.cos(math.radians(ang)) - (h/2)*math.cos(math.radians(ang+90)), center[1] + (w/2)*math.sin(math.radians(ang)) + (h/2)*math.sin(math.radians(ang+90))),
	(center[0] + (w/2)*math.cos(math.radians(ang)) - (h/2)*math.cos(math.radians(ang+90)), center[1] - (w/2)*math.sin(math.radians(ang)) + (h/2)*math.sin(math.radians(ang+90)))], 0)

# changes here

rect(screen, (255,255,255), (0, 0, 400, 400), 0)

circle(screen, (255,255,0), (200,200), 150, 0) #face
rect(screen, (0,0,0), (125, 275, 150, 25) ,0) #mouth
#eyes init
circle(screen, (255,0,0), (125, 150), 30, 0) #left eye
circle(screen, (0,0,0), (125, 150), 12, 0)

circle(screen, (255,0,0), (275, 150), 25, 0) #right eye
circle(screen, (0,0,0), (275, 150), 12, 0)

#eyebrows
crect(screen, (0,0,0), (120,110), 125, 10, -30) # left
crect(screen, (0,0,0), (280,115), 115, 12, 30) #right

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
