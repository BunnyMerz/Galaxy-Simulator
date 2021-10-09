import pygame
from gravity import *
from random import randint as rng
# from math import pi

height = 600
width = 600

# font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()
window = pygame.display.set_mode((width,height), pygame.NOFRAME)

def Fps():
    ## Fps should be inside Hud
    pass
    # font_surface = font.render(str(int(clock.get_fps())), True, (200,200,200))
    # window.blit(font_surface, [width - 30, height - 30])

def Draw(galaxy,delta_time):
    galaxy.draw(window)

def Update(galaxy,delta_time):
    galaxy.update(delta_time,mouse.get_pos())
    galaxy.trace()

def Input(galaxy,delta_time):
    keys = pygame.key.get_pressed()
    galaxy.key_input(keys,delta_time)


def run(galaxy):
    dt = 0.001
    speed_up = 1
    while(1):
        delta_time = clock.tick(60) / 1000
        window.fill((0,0,0))
        event = pygame.event.get() ## Avoid freezing of window
        ##
        for _ in range(int(delta_time/dt * speed_up)):
            Update(galaxy,dt)
        ##
        Draw(galaxy,delta_time)
        Input(galaxy,delta_time)
        Fps()

        pygame.display.update()

if __name__ == "__main__":
    sun = Planet(mass=3500,radius=120,x=0,y=0,speed=Vector2(100,0),color=(200,200,100))
    blue = Planet(mass=10,radius=10,x=500,y=0,speed=Vector2(100,200),color=(20,100,200))
    green = Planet(mass=20,radius=15,x=1000,y=1000,speed=Vector2(120,-120),color=(30,200,100))
    hasmoon = Planet(mass=100,radius=60,x=4000,y=2000,speed=Vector2(120,-60),color=(37,100,150))
    hasmoonsmoon = Planet(mass=10,radius=9,x=4160,y=2000,speed=Vector2(120,-130),color=(100,120,120))
    hasmoonsmoon2 = Planet(mass=10,radius=7,x=4000-160,y=2000,speed=Vector2(120,20),color=(120,100,100))
    galaxy = Galaxy([sun,blue,green,hasmoon,hasmoonsmoon,hasmoonsmoon2],window,width,height,zoom=0.14)

    ###
    # p1 = Planet(mass=1000,radius=20,x=0,y=0,speed=Vector2(0,0),color=(200,200,100))
    # p2 = Planet(mass=10,radius=10,x=500,y=0,speed=Vector2(0,-100),color=(200,200,100))
    # p3 = Planet(mass=1,radius=3,x=540,y=0,speed=Vector2(0,-130),color=(200,200,100))
    # galaxy = Galaxy([p1,p2,p3],window,width,height,zoom=1)
    ###
    run(galaxy)