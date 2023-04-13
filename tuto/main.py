import pyxel as px
from random import *
from joueur import *
from tir import *
from ennemi import *

class Jeu:
    def __init__(self, h, l, titre):
        px.init(h, l, title=titre)
        self.joueur = Joueur(64, 64)
        self.ennemi = Ennemi()
        self.liste_tirs = [] 	

        px.run(self.update, self.draw)
        
    def update(self):
        v = self.joueur.move()
        if v is not None:
            self.liste_tirs.append(Tir(v[0], v[1]))
        for tir in self.liste_tirs:
            tir.move()
            if not tir.estEnVol():
                self.liste_tirs.remove(tir)

        self.ennemi.move()

    def draw(self):
        px.cls(0)
        self.joueur.draw()
        self.ennemi.draw()
        for tir in self.liste_tirs:
            tir.draw()

Jeu(128, 128, "v1")