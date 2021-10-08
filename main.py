import pygame
from gravity import *
# from random import randint as rng
# from math import pi

pygame.init()
height = 600
width = 600


font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()
window = pygame.display.set_mode((width,height), pygame.NOFRAME)

sun = Planet(mass=3500,radius=120,x=0,y=0,speed=Vector2(100,0),color=(200,200,100))
blue = Planet(mass=10,radius=10,x=500,y=0,speed=Vector2(100,200),color=(20,100,200))
green = Planet(mass=20,radius=15,x=1000,y=1000,speed=Vector2(120,-120),color=(30,200,100))
hasmoon = Planet(mass=40,radius=15,x=4000,y=2000,speed=Vector2(120,-60),color=(37,100,150))
hasmoonsmoon = Planet(mass=5,radius=4,x=4100,y=2000,speed=Vector2(120,-120),color=(100,100,100))
galaxy = Galaxy([sun,blue,green,hasmoon,hasmoonsmoon],window,width,height,zoom=0.14)


def Fps(delta_time):
    font_surface = font.render(str(int(clock.get_fps())), True, (200,200,200))
    window.blit(font_surface, [width - 30, height - 30])

def Draw(delta_time):
    galaxy.draw(window)

def Update(delta_time):
    galaxy.update(delta_time,mouse.get_pos())
    galaxy.trace()

def Input(delta_time):
    global z, x_offset, y_offset
    keys = pygame.key.get_pressed()
    galaxy.key_input(keys,delta_time)

dt = 0.001
speed_up = 1
while(1):
    delta_time = clock.tick(60) / 1000
    window.fill((0,0,0))
    event = pygame.event.get()
    ##
    for x in range(int(delta_time/dt * speed_up)):
        Update(dt)
    ##
    Draw(delta_time)
    Input(delta_time)
    Fps(delta_time)

    pygame.display.update()
