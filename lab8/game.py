import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

balls = list()

def new_ball():
    '''рисует новый шарик '''
    x = randint(100, 1100)
    y = randint(100, 800)
    r = randint(10, 100)
    vel_x = randint(-30, 30)
    vel_y = randint(-30, 30)
    color = COLORS[randint(0, 5)]
    balls.append([x,y,r, color, vel_x, vel_y])
    circle(screen, color, (x, y), r)
    pygame.display.update()
def change_balls_position():
	'''меняет позицию шариков в соответствии с их скоростями'''
    screen.fill(BLACK)
	for b in balls:
		#меняем положение по Ox
		if b[0] + (b[4]/FPS) > 1200 - b[2]:
			b[0] = 1200 - b[2]
		elif b[0] + (b[4]/FPS) < b[2]:
			b[0] = b[2]
		else:
			b[0] += (b[4]/FPS)
		#меняем положение по Oy
		if b[1] + (b[5]/FPS) > 900 - b[2]:
			b[1] = 900 - b[2]
		elif b[1] + (b[5]/FPS) < b[2]:
			b[1] = b[2]
		else:
			b[1] += (b[5]/FPS)
		circle(screen, b[3], (b[0], b[1]), b[2])
	pygame.display.update()


pygame.display.update()
clock = pygame.time.Clock()
finished = False
new_ball()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
    change_balls_position()

pygame.quit()
