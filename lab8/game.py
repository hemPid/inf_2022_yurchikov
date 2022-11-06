import pygame
from pygame.draw import *
from random import randint
from math import *
import pygame_textinput
import os.path

pygame.init()

FPS = 30
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
level = 1
points = 0
player = 1

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
    vel_x = randint(-10, 10)*level
    vel_y = randint(-10, 10)*level
    color = COLORS[randint(0, 5)]
    balls.append([x,y,r, color, vel_x, vel_y])
    circle(screen, color, (x, y), r)
    pygame.display.update()

def change_balls_position():
	'''меняет позицию шариков в соответствии с их скоростями'''
    
	for b in balls:
		#меняем положение по Ox
		if b[0] + (b[4]/FPS) > screen_width - b[2]:
			b[4] = randint(-10, 0)*level #отражение от правой границы
			b[0] += (b[4]/FPS)
		elif b[0] + (b[4]/FPS) < b[2]:
			b[4] = randint(0, 10)*level #отражение от левой границы
			b[0] += (b[4]/FPS)
		else:
			b[0] += (b[4]/FPS) #движение по Ox без столкновений
		#меняем положение по Oy
		if b[1] + (b[5]/FPS) > screen_height - b[2]:
			b[5] = randint(-10,0)*level #отражение от нижней границы
			b[1] += (b[5]/FPS)
		elif b[1] + (b[5]/FPS) < b[2]:
			b[5] = randint(0, 10)*level #отражение от верхней границы
			b[1] += (b[5]/FPS)
		else:
			b[1] += (b[5]/FPS) #движение по Oy
		circle(screen, b[3], (b[0], b[1]), b[2])
	pygame.display.update()

def is_mouse_in_position(ev, t, pos):
	'''
	Возвращает True, если мышь находится в заданной области
	ev - событие мыши
	t - тип области (1 - Прямоугольник, 2 - окружность)
	pos - координаты области (При t = 1, (x,y,w,h), при t = 2 (x, y, r))
	'''
	m_x = ev.pos[0]
	m_y = ev.pos[1]
	if t == 1:
		if pos[0] <= m_x and m_x <= pos[0] + pos[2] and pos[1] <= m_y and m_y <= pos[1] + pos[3]:
			return True
	if t == 2:
		if (m_x - pos[0]) ** 2 + (m_y - pos[1]) ** 2 <= pos[2] ** 2:
			return True
	return False

def gameover():
	'''Показывает экран с количеством очков и вводом имени, возвращает inputbox'''
	f1 = pygame.font.SysFont('arial', 80, True)
	text1 = f1.render(str('GAME OVER'), True, WHITE)
	screen.blit(text1, (screen_width/2 - 450, 100))
	text2 = f1.render(str('Your score: ' + str(points)), True, WHITE)
	screen.blit(text2, (screen_width/2 - 450, 200))
	f2 = pygame.font.SysFont('arial', 40, True)
	text3 = f2.render(str('Enter your name and press enter (20 сhars max):'), True, WHITE)
	screen.blit(text3, (screen_width/2 - 450, 300))
	manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 20)
	tmp = pygame_textinput.TextInputVisualizer(manager=manager)
	tmp.font_color = (255,255,255)
	return tmp

def write_record(name, score):
	'''
	делает запись в файл с количеством очков и именем игрока
	name - имя игрока
	score - его очки
	'''
	output = list()
	if not os.path.exists('players.txt'): #создаём рейтинговый файл, если он отсутствует
		with open('players.txt', 'w') as f:
			f.write(name + ' ' + score + '\n')
		return None
	with open('players.txt', 'r') as f:
		st = f.readlines()
		if len(st) == 0:
			data.append(name + ' ' + score + '\n')
		else:
			data = list(map(lambda x: x.rstrip().split(), st))
			found = False
			#Добавляем запись с игроком в рейтинг
			for person in data:
				if person[0] == name:
					found = True
					if int(person[1]) < int(score):
						data.remove(person)
						data.append([name, score])
					break
			if not found:
				data.append([name, score])
			data = sorted(data, key = lambda x: -int(x[1]))
			output = ''.join(list(map(lambda x: ' '.join(x) + '\n', data)))
	with open('players.txt', 'w') as f:
		f.write(output)



pygame.display.update()
clock = pygame.time.Clock()
finished = False
level_started = False
lost = False
textinput = None
i = 0
init_game()
while not finished:
    clock.tick(FPS)
    if level_started:
    	screen.fill(BLACK)
    	if i == floor(600/level):
    		if len(balls) < 5:
    			new_ball()
    		else:
    			#засчитано поражение создаётся окно ввода имени
    			level_started = False
    			lost = True
    			screen.fill(BLACK)
    			textinput = gameover()
    		i = 0
    	if not lost:
    		change_balls_position()
    	i+=1
    events = pygame.event.get()
    if lost:
    	rect(screen, BLACK, (screen_width/2 - 450, 400, 500, 500))
    	screen.blit(textinput.surface, (screen_width/2 - 450, 400))
    	textinput.update(events)
    for event in events:
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not level_started:
            	l = 0
            	for b in buttons:
            		if is_mouse_in_position(event, 1, b[1]):
            			l = b[0]
            			break
            	if l:
            		level = 10 * (2 ** (l-1))
            		print(level)
            		level_started = True
            		buttons.clear()
            if level_started:
            	for b in balls:
            		if is_mouse_in_position(event, 2, (b[0], b[1], b[2])):
            			balls.remove(b)
            			points += 1
            			break
        elif event.type == pygame.KEYDOWN and lost:
        	if event.key == pygame.K_RETURN:
        		#Обнуляем очки, делаем запись в файл
        		lost = False
        		balls.clear()
        		screen.fill(BLACK)
        		write_record(textinput.value, str(points))
        		points = 0
        		init_game()


    pygame.display.update()

pygame.quit()
