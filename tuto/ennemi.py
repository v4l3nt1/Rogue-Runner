import pyxel as px
from random import *

class Ennemi:
    def __init__(self):
        self.x = randint(8, 120)
        self.y = randint(8, 120)
        self.h = 4

    def move(self):
        a = randint(1, 4)
        
        if a == 1:
            if self.y > 6:
                self.y -= 1
        if a == 2:
            if self.x > 6:
                self.x -= 1
        if a == 3:
            if self.y < 122:
                self.y += 1
        if a == 4:
            if self.x < 122:
                self.x += 1
 
    def draw(self):
        px.rect(self.x, self.y, 4, 4, 10)
