from math import sqrt
from pygame import Surface, SRCALPHA, Rect
from pygame import draw as py_draw

class Selector():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 0
        self.color = (50,100,120)
        self.draw_f = lambda dummy : dummy ## Rewritten in unselect() and select()

    def unselect(self):
        self.size = 0
        self.draw_f = lambda dummy : dummy
    
    def select(self,hover_block):
        bigger = 2
        self.x = hover_block.x - bigger
        self.y = hover_block.y - bigger
        self.size = (hover_block.radius + bigger)*2

        self.draw_f = lambda surface : py_draw.rect(surface,self.color,Rect(self.x,self.y,self.size,self.size),3)
    
    def draw(self,surface):
        self.draw_f(surface)

class Hover_Button():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.surface = Surface((radius*2,radius*2), SRCALPHA, 32)
        py_draw.circle(self.surface,self.color,(radius,radius),radius)
    
    def is_hovering(self,mouse_pos):
        hb = [self.topleft(),self.bottomrigth()]
        if ((mouse_pos[0] >= hb[0][0] and mouse_pos[0] <= hb[1][0]) and (
            mouse_pos[1] >= hb[0][1] and mouse_pos[1] <= hb[1][1])):
            return True
        return False

    def draw(self,surface):
        surface.blit(self.surface, (self.x,self.y))

    def topleft(self):
        return (self.x,self.y)

    def bottomrigth(self):
        return (self.x+self.radius*2,self.y+self.radius*2)
        
class Hud():
    def __init__(self,galaxy,margin=13,starting_margin=10,y=5):
        self.hover_blocks = []
        self.selected = 0
        self.margin = margin

        self.galaxy = galaxy
        x = starting_margin
        y += max([sqrt(x.radius)*3 for x in galaxy.planets])
        for planet in galaxy.planets:
            r = sqrt(planet.radius) * 3
            h = Hover_Button(x=x, y=y-r, radius=r, color=planet.color)
            self.hover_blocks.append(h)
            x += r*2 + margin

        self.selector = Selector()
        self.selector.select(self.hover_blocks[self.selected])
    
    def hitbox(self):
        left = (self.hover_blocks[0].topleft())
        rigth = (self.hover_blocks[-1].bottomrigth())
        return [left,rigth]
    
    def draw(self,surface):
        for hb in self.hover_blocks:
            hb.draw(surface)
        self.selector.draw(surface)
    
    def update(self,mouse_pos=[-1,-1]):
        hb = self.hitbox()
        if ((mouse_pos[0] >= hb[0][0] and mouse_pos[0] <= hb[1][0]) and (
             mouse_pos[1] >= hb[0][1] and mouse_pos[1] <= hb[1][1])):
            x = 0
            for hover in self.hover_blocks:
                if hover.is_hovering(mouse_pos):
                    self.selector.select(hover)
                    self.galaxy.set_reference(self.galaxy.planets[x])
                    return
                x+=1
        self.selector.unselect()
        self.galaxy.unset_reference()
 
    # def draw(self,surface,mouse_pos=[-1,-1]):
    #     for x in range(len(self.hover_blocks)):
    #         if self.hover_blocks[x].is_hovering(mouse_pos):
    #             self.series[x].draw(surface)
    #             self.draw_hud(surface)
    #             return
    #     for serie in self.series:
    #         serie.draw(surface)
    #     self.draw_hud(surface)
        
