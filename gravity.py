from math import sin,cos
from pygame import Surface, SRCALPHA, Vector2, Surface, transform
from pygame.constants import K_DOWN, K_LCTRL, K_UP, K_w, K_a, K_s, K_d, K_q
from pygame import draw as py_draw
from hud import *
from pygame import mouse


## grav force = G * m1*m2/d²
class Gravity():
    G = 6.67408 * 10**(-11) # Nm²/Kg²

    def gravity_force(p1,p2):
        try:
            return Gravity.G * p1.mass * p2.mass / Planet.distance(p1,p2)
        except:
            return 0

###############

class Planet():
    mass_unit = 10**23 # Kg * 10**23
    accel_decrease = 10**(-6)
    distance_unit = 10**(-6)

    last_id = 0
    def distance(p1,p2):
            return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**(1/2)

    def __init__(self,mass,radius,x=100,y=120,speed=Vector2(0,0),color=(100,100,100)):
        ### For debbuging
        self.id = Planet.last_id + 1
        Planet.last_id += 1
        ###
        self.x = x
        self.y = y
        self.speed = speed
        self.accel = Vector2(0,0)
        self.mass = mass * Planet.mass_unit
        self.radius = radius
        self.color = color
        
    def print_info(self):
        print("id:",self.id,end=" / ")
        print("Pos:",int(self.x),int(self.y),end=" / ")
        # print("x:",int(self.x),end=" / ")
        # print("y:",int(self.y),end=" / ")
        print("Speed:",list(map(int,self.speed)),end=" / ")
        print("Accel:",list(map(int,self.accel)),end=" / ")
        print("Norma Accel:", int(self.accel.length()*100)/100)

    def center(self):
        return [self.x,self.y]

    def pulled_by(self,p2):
        d = Planet.distance(self,p2)
        if d == 0:
            return Vector2(0,0)
        
        unit_vector = Vector2(
            (p2.x - self.x)/d,
            (p2.y - self.y)/d
        )
        force = (Gravity.G * p2.mass)/(d**2) * Planet.accel_decrease
        return force * unit_vector

    # def apply_force(self,f,self_mass):
    #     self.accel += f/self_mass

    def update(self,planets,delta_time):
        self.accel = Vector2(0,0)
        for planet in planets:
            if planet != self:
                f = self.pulled_by(planet) * delta_time
                self.accel += f
                # self.apply_force(f,1) ## 1 means mass doesn't affect the equation as pulled_by also ignores mass
                
        self.speed += self.accel * delta_time
        self.x += self.speed.x * delta_time
        self.y += self.speed.y * delta_time
    
    def apparent_pos(self,offset=[0,0],zoom=1):
        return (Vector2(self.center()) - Vector2(offset)) * zoom

    def draw(self,surface,window_center,offset=[0,0],zoom=1,show_speed=0,show_accel=0):
        wc = Vector2(window_center)
        obj = self.apparent_pos(offset,zoom)

        py_draw.circle(surface,self.color, obj + wc, max([self.radius * zoom,1]))
        if show_speed:
            py_draw.line(surface,(200,60,100),obj + wc,obj + (self.speed * zoom) + wc)
        if show_accel:
            py_draw.line(surface,(20,90,240),obj + wc,obj + (self.accel * zoom) + wc)

###############

class Galaxy():
    controlls = {
        "zoom":{
            "in":K_UP,
            "out":K_DOWN,
            "reset":K_LCTRL
        },
        "move":{
            "up" : K_w,
            "down" : K_s,
            "left" : K_a,
            "right" : K_d,
        },
        "tracer":{
            "show": K_q
        }
    }
    controlls_names = {
        "zoom":{
            "in":"Up",
            "out":"Down",
            "reset":"Left Control"
        },
        "move":{
            "up" : "W",
            "down" : "S",
            "left" : "A",
            "right" : "D",
        },
        "tracer":{
            "show": "Q"
        }
    }

    def __init__(self,planets,window,window_width,window_heigth,zoom=1):
        # params
        self.x = 0
        self.y = 0
        self.reference = lambda : [0,0]
        self.planet_reference = None
        self.zoom = zoom
        # objs
        self.planets = planets
        self.tracer = Trace(window_width*20)
        self.hud = Hud(self)
        # window
        self.window_center = (window_width/2,window_heigth/2)
        self.window = window

    def set_zoom(self,new_zoom):
        self.zoom = new_zoom
    def zoom_in(self,delta_zoom):
        self.zoom += delta_zoom
    def zoom_out(self,delta_zoom):
        self.zoom -= delta_zoom

    def xy(self):
        x,y = self.reference()
        return self.x+x,self.y+y

    def key_input(self,keys,delta_time):
        if keys[Galaxy.controlls["zoom"]["in"]]:
            self.zoom_in(1 * delta_time)
        if keys[Galaxy.controlls["zoom"]["out"]]:
            if (self.zoom > 1 * delta_time):
                self.zoom_out(1 * delta_time)
        if keys[Galaxy.controlls["zoom"]["reset"]]:
            self.set_zoom(1)

        if keys[Galaxy.controlls["tracer"]["show"]]:
            self.draw_tracer(self.window)

        move_speed = 200 * 1/self.zoom
        if keys[Galaxy.controlls["move"]["up"]]:
            self.y -= move_speed * delta_time
        if keys[Galaxy.controlls["move"]["down"]]:
            self.y += move_speed * delta_time
        if keys[Galaxy.controlls["move"]["right"]]:
            self.x += move_speed * delta_time
        if keys[Galaxy.controlls["move"]["left"]]:
            self.x -= move_speed * delta_time


    def set_reference(self,planet):
        if self.planet_reference == planet:
            return
        self.x = 0
        self.y = 0
        self.reference = lambda : planet.center()
        self.planet_reference = planet

    def unset_reference(self):
        self.x += self.reference()[0]
        self.y += self.reference()[1]
        self.reference = lambda : [0,0]
        self.planet_reference = None

    def update(self,delta_time,mouse_pos=[-1,-1]):
        self.hud.update(mouse_pos)
            
        for planet in self.planets:
            planet.update(self.planets,delta_time)
            # planet.print_info()
    
    def draw(self,surface):
        for planet in self.planets:
            planet.draw(surface,self.window_center,self.xy(),self.zoom)
        self.hud.draw(surface)
    
    def draw_tracer(self,surface):
        self.tracer.draw(surface,self.xy(),self.window_center,self.zoom)
    
    def trace(self):
        self.tracer.darken()
        for planet in self.planets:
            self.tracer.trace(planet)

###############

class Trace():
    def __init__(self,size):
        self.surface = Surface((size,size), SRCALPHA, 32)
        self.size = size
        self.last_scale = 1
        self.last_transform = transform.scale(self.surface,(size, size))

    def trace(self,planet):
        py_draw.circle(self.surface,planet.color,planet.center() + Vector2(self.size/2,self.size/2),1)
        
        sx,sy = (Vector2(self.size/2) + Vector2(planet.center())) * self.last_scale
        py_draw.rect(self.last_transform,planet.color,Rect([sx,sy],[1,1]))
        
    def darken(self):
        # self.last_transform.fill((0,0,0))
        # self.surface.fill((0,0,0))
        pass
        
    def draw(self,surface,xy,ws,scale=1):
        size = int(self.size * scale)
        if self.last_scale != scale:
            self.last_transform = transform.scale(self.surface,(size, size))
            self.last_scale = scale
        x = (-xy[0] * scale) + ws[0] - size/2
        y = (-xy[1] * scale) + ws[1] - size/2
        surface.blit(self.last_transform,(x, y))