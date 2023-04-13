import pyxel as px
from random import *


class Ennemi:
    def __init__(self):
        self.x = randint(8, 120)
        self.y = randint(8, 120)
        self.h = 4
        self.w = 4
        self.vitesse = 1

    def move(self):
        if px.frame_count % 5 == 0:	
            a = randint(1,4)
            if a == 1:
                if self.y > 6:
                    self.y -= self.vitesse
            if a == 2:
                if self.x > 6:
                    self.x -= self.vitesse
            if a == 3:
                if self.y < 122 - self.w:
                    self.y += self.vitesse
            if a == 4:
                if self.x < 122 - self.w:
                    self.x += self.vitesse
 
    def draw(self):
        px.rect(self.x, self.y, 4, 4, 10)
