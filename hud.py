from math import sqrt
from pygame import Surface, SRCALPHA, Rect
from pygame import draw as py_draw

class Selector():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 0
        self.color = (50,100,120)

    def unselect(self):
        self.size = 0
    
    def select(self,hover_block):
        bigger = 2
        self.x = hover_block.x - bigger ## Go left (will grow rigth afterwards)
        self.y = hover_block.y - bigger ## Go up (Will grow down afterwards)
        self.size = (hover_block.radius + bigger)*2 ## Grow down and rigth ## Square around circle. +2 so it doesn't overlap it.
    
    def draw(self,surface):
        if self.size == 0: ## self.size as 0 == hide
            return
        py_draw.rect(surface,self.color,Rect(self.x,self.y,self.size,self.size),3)

class Hover_Button():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        ##
        self.surface = Surface((radius*2,radius*2), SRCALPHA, 32)
        py_draw.circle(self.surface,self.color,(radius,radius),radius)
        ##
    
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
    planet_size = 2
    def planet_hud_scale(radius):
        return sqrt(radius) * Hud.planet_size # Re-size the planets to use as mini version for the hud. Must change the return value here to affect everywhere (including logic).

    def __init__(self,galaxy,margin=13,starting_margin=10,y=5):
        self.hover_blocks = []
        self.selected = 0
        self.margin = margin

        self.galaxy = galaxy
        x = starting_margin
        y += max([ Hud.planet_hud_scale(x.radius) for x in galaxy.planets]) # Get biggest size of all planets (re-scaled version) to determine how to center other planets
        for planet in galaxy.planets:
            r = Hud.planet_hud_scale(planet.radius) ## re-scaled radius
            h = Hover_Button(x=x, y=y-r, radius=r, color=planet.color) # text-align: center
            self.hover_blocks.append(h)
            x += r*2 + margin

        self.selector = Selector()
        self.selector.select(self.hover_blocks[self.selected])
    
    def hitbox(self):
        left = (self.hover_blocks[0].topleft())
        rigth = (self.hover_blocks[-1].bottomrigth())
        return [left,rigth] ## Top most of the whole box (First planet's topleft) and bottom most.
    
    def draw(self,surface):
        for hb in self.hover_blocks:
            hb.draw(surface)
        self.selector.draw(surface)
    
    def update(self,mouse_pos=[-1,-1]):
        hb = self.hitbox()
        ## Check big hitbox (1 collision detection instead of len(hover_blocks))
        if ((mouse_pos[0] >= hb[0][0] and mouse_pos[0] <= hb[1][0]) and (
             mouse_pos[1] >= hb[0][1] and mouse_pos[1] <= hb[1][1])):
            x = 0
            for hover in self.hover_blocks: ## Individual Hovers. Could be better and use more divisions, but unecessery as of now.
                if hover.is_hovering(mouse_pos):
                    self.selector.select(hover) ## Show Select box over the selected one
                    self.galaxy.set_reference(self.galaxy.planets[x]) ## Lock the camera onto the planet
                    return ## Unecessery check after this if, as it will all be false.
                x+=1
        ## Only will reach end if not hovering.
        self.selector.unselect() ## Hide selector
        self.galaxy.unset_reference() ## Unlock camera. Migth cause trouble if something else aside from hover sets the reference. Later one, it will be used clicking instead of hovering, so this should not happen anymore.
