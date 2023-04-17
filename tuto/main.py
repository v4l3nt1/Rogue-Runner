import pyxel as px
from random import *
from joueur import *
from tir import *
from ennemi import *

class Jeu:
    def __init__(self, h, l, titre):
        px.init(h, l, title=titre)
        px.load("ressources.pyxres", True, False, False, False)
        self.joueur = Joueur(64, 64)
        self.liste_ennemis = []
        for i in range(5):
            self.liste_ennemis.append(Ennemi())
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

        for ennemi in self.liste_ennemis:
            ennemi.move()

        for ennemi in self.liste_ennemis:
            for tir in self.liste_tirs:
                if ennemi.x <= tir.x <= ennemi.x + ennemi.w and tir.y < ennemi.y + ennemi.h:
                    if ennemi.y < self.joueur.y:
                        if ennemi in self.liste_ennemis:
                            self.liste_ennemis.remove(ennemi)
                        if tir in self.liste_tirs:
                            self.liste_tirs.remove(tir)

    def draw(self):
        px.cls(0)
        self.joueur.draw()
        for ennemi in self.liste_ennemis:
            ennemi.draw()
        for tir in self.liste_tirs:
            tir.draw()

Jeu(128, 128, "v1")