import math
from random import randint
from random import choice
import numpy as np

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
ACCELERATION = np.array([0, 400])

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.pos = np.array([x, y],  dtype=np.float64)
        self.r = 10
        self.vel = np.array([0, 0])
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки.
        То есть, обновляет значения self.x и self.y
        с учетом скоростей self.vx и self.vy,
        силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.vel += dt*ACCELERATION
        self.pos += dt*self.vel
        if self.pos[0] + self.r >= WIDTH or self.pos[0] - self.r <= 0:
            self.vel[0] = -0.5*self.vel[0]
            if self.pos[0] + self.r >= WIDTH:
                self.pos[0] = WIDTH - self.r - 1
            else:
                self.pos[0] = self.r + 1
        if self.pos[1] - self.r <= 0 or self.pos[1] + self.r >= HEIGHT:
            self.vel[1] = -0.5*self.vel[1]
            if self.pos[1] + self.r >= HEIGHT:
                self.pos[1] = HEIGHT - self.r - 1
            else:
                self.pos[1] = self.r + 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            self.pos,
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью,
        описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели.
            В противном случае возвращает False.
        """
        s = self.pos - obj.pos
        return np.linalg.norm(s) <= self.r + obj.r


class Gun:
    def __init__(self, screen, x=20, y=450, width=50, height=10):
        """Создаёт пушку Gun

        Args:
        x - положение оси вращения по оси Ox
        y - положение оси вращения по оси Oy
        width - ширина пушки
        height - высота пушки
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.axis = np.array([x, y])
        self.width = width
        self.height = height

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча
        vx и vy зависят от положения мыши.
        """
        global balls, bullet
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.pos[1]),
                             (event.pos[0]-new_ball.pos[0]))
        new_ball.vel = 10 * np.array([self.f2_power * math.cos(self.an),
                                      self.f2_power * math.sin(self.an)])
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        a1 = np.array([(self.height/2)*math.cos(self.an - (math.pi/2)),
                       (self.height/2)*math.sin(self.an - (math.pi/2))])
        a4 = np.array([(self.height/2)*math.cos(self.an + (math.pi/2)),
                       (self.height/2)*math.sin(self.an + (math.pi/2))])
        a2 = a1 + np.array([(self.width/2)*math.cos(self.an),
                            (self.width/2)*math.sin(self.an)])
        a3 = a4 + np.array([(self.width/2)*math.cos(self.an),
                            (self.width/2)*math.sin(self.an)])
        pygame.draw.polygon(self.screen, self.color,
                            [self.axis + a1,
                             self.axis + a2,
                             self.axis + a3,
                             self.axis + a4])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 2
                self.width = 50 * (1 + (self.f2_power-10)/90)
            self.color = RED
        else:
            self.color = GREY
            self.width = 50


class Target:
    def __init__(self, screen):
        self.points = 0
        self.screen = screen
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.pos = np.array([randint(600, 780), randint(300, 550)])
        self.r = randint(2, 50)
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    dt = clock.tick(FPS)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move(dt)
        if b.hittest(target):
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
