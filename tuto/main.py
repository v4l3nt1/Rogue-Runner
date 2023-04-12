import pyxel as px
from random import *

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

class Joueur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 8
        self.w = 12
        self.vitesse = 1

    def move(self):
        if px.btn(px.KEY_Z):
            if self.y > 6:
                self.y -= self.vitesse
        if px.btn(px.KEY_Q):
            if self.x > 6:
                self.x -= self.vitesse
        if px.btn(px.KEY_S):
            if self.y < 122 - self.w:
                self.y += self.vitesse
        if px.btn(px.KEY_D):
            if self.x < 122 - self.h:
                self.x += self.vitesse
        if px.btnr(px.KEY_SPACE):
            return self.x+4, self.y-2
        return None
        

    def draw(self):
        px.rect(self.x, self.y, self.h, self.w, 9)

class Tir:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.enVol = True

    def estEnVol(self):
        return self.enVol
    
    def move(self):
        if self.y > 6:
            self.y = self.y - 1
        else:
            self.enVol = False
    
    def draw(self):
        px.rect(self.x, self.y, 1, 4, 10)

class Ennemi:
    def __init__(self):
        self.x = randint(8, 120)
        self.y = randint(8, 120)

    def move(self):
        
        
    def draw(self):
        px.rect(self.x, self.y, 4, 4, 10)



Jeu(128, 128, "v1")