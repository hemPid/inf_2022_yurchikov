import pygame
from pygame.draw import *
from random import randint
from math import *
pygame.init()

FPS = 30
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
level = 1

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

balls = list()
buttons = list()

def create_button(id, screen, value, fontsize, color, bg_color, pos):
	'''
	создаёт кнопку и добавляет её в buttons.
	id - идентификатор кнопки
	screen - экран, на котором рисуется кнопка
	value - текст кнопки
	fontsize - размер шрифта текста в кнопке
	color - цвет кнопки
	bg_color - цвет заднего фона
	pos - позиция кнопки
	'''
	#прорисовка фона кнопки
	size_in_px = floor((fontsize*4)/3)
	rect(screen, bg_color, (pos[0], pos[1], len(value)*size_in_px*0.6, size_in_px + 10))
	buttons.append((id, (pos[0], pos[1], len(value)*size_in_px*0.6, size_in_px + 10)))
	#прорисовка текста кнопки
	font = pygame.font.SysFont('arial', fontsize, True)
	text = font.render(str(value), True, color)
	screen.blit(text, (pos[0] + 10, pos[1] + 5))
	


def init_game():
	'''Запускает окно с выбором уровня сложности'''
	f1 = pygame.font.SysFont('arial', 80, True)
	text = f1.render(str('Сhoose difficulty level'), True, WHITE)
	screen.blit(text, (screen_width/2 - 450, 100))
	create_button(1, screen, 'EASY', 60, WHITE, GREEN, (400,300))
	create_button(2, screen, 'MEDIUM', 60, WHITE, YELLOW, (400,400))
	create_button(3, screen, 'HARD', 60, WHITE, RED, (400,500))

def new_ball():
    '''рисует новый шарик '''
    r = randint(10, 100)
    x = randint(r, screen_width - r)
    y = randint(r, screen_height - r)
    vel_x = randint(-90, 90)
    vel_y = randint(-90, 90)
    color = COLORS[randint(0, 5)]
    balls.append([x,y,r, color, vel_x, vel_y])
    circle(screen, color, (x, y), r)
    pygame.display.update()

def change_balls_position():
	'''меняет позицию шариков в соответствии с их скоростями'''
    
	for b in balls:
		#меняем положение по Ox
		if b[0] + (b[4]/FPS) > 1200 - b[2]:
			b[0] = 1200 - b[2]
		elif b[0] + (b[4]/FPS) < b[2]:
			b[0] = b[2]
		else:
			b[0] += (b[4]/FPS)
		#меняем положение по Oy
		if b[1] + (b[5]/FPS) > 800 - b[2]:
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
level_started = False
init_game()
while not finished:
    clock.tick(FPS)
    #screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not level_started:
            	print('click')
    pygame.display.update()

pygame.quit()
