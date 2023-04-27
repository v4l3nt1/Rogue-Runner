import pyxel as px
from heros import *

class Jeu:
    def __init__(self, h, l, titre):
        px.init(h, l, title=titre)
        px.load("res.pyxres", True, True, False, False)

        px.run(self.update, self.draw)
        
    def update(self):
        

    def draw(self):
        text(15, 15, "hello", 2)

Jeu(128, 128, "Rogue Runner")