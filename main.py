import pyxel as px
from random import *

WALLS = (1,0)
FROM_RIGHT = [(32,0),(48,0),(96,0),(128,0),(160,0),(192,0),(208,0),(224,0)]
FROM_LEFT = [(32,0),(64,0),(80,0),(128,0),(144,0),(176,0),(192,0),(224,0)]
FROM_UP = [(0,0),(16,0),(80,0),(96,0),(128,0),(176,0),(208,0),(224,0)]
FROM_DOWN = [(16,0),(32,0),(48,0),(64,0),(80,0),(96,0),(112,0),(128,0)]

GRAVITY = 0.5  # Gravité appliquée au joueur
JUMP_POWER = 8  # Puissance du saut du joueur

class Joueur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.atk = 2
        self.vitesse = 1
        self.mapy = 0
        self.mapx = 0
        self.is_jumping = False
        self.jump_power = 0
    
    def move(self):
        if px.btn(px.KEY_Z):
            if px.tilemap(0).pget((self.mapx*8+self.x)//8, ((self.mapy*8+self.y)-1)//8) != WALLS and px.tilemap(0).pget(((self.mapx*8+self.x)+7)//8, ((self.mapy*8+self.y)-1)//8) != WALLS:
                self.y -= self.vitesse 
        if px.btn(px.KEY_Q):
            if px.tilemap(0).pget(((self.mapx*8+self.x)-1)//8, (self.mapy*8+self.y)//8) != WALLS and px.tilemap(0).pget(((self.mapx*8+self.x)-1)//8, ((self.mapy*8+self.y)+7)//8) != WALLS:
                self.x -= self.vitesse
        if px.btn(px.KEY_S):
            if px.tilemap(0).pget((self.mapx*8+self.x)//8, ((self.mapy*8+self.y)+8)//8) != WALLS and px.tilemap(0).pget(((self.mapx*8+self.x)+7)//8, ((self.mapy*8+self.y)+8)//8) != WALLS:
                self.y += self.vitesse
        if px.btn(px.KEY_D):
            if px.tilemap(0).pget(((self.mapx*8+self.x)+8)//8, (self.mapy*8+self.y)//8) != WALLS and px.tilemap(0).pget(((self.mapx*8+self.x)+8)//8, ((self.mapy*8+self.y)+7)//8) != WALLS:
                self.x += self.vitesse

        # Gestion du saut
        if px.btnp(px.KEY_SPACE) and not self.is_jumping:
            self.is_jumping = True
            self.jump_power = JUMP_POWER

        if self.is_jumping:
            if self.jump_power >= 0:
                self.y -= self.jump_power
                self.jump_power -= 1
            else:
                self.is_jumping = False

        # Appliquer la gravité
        if not self.is_jumping:
            if px.tilemap(0).pget((self.mapx*8+self.x)//8, ((self.mapy*8+self.y)+8)//8) != WALLS and px.tilemap(0).pget(((self.mapx*8+self.x)+7)//8, ((self.mapy*8+self.y)+8)//8) != WALLS:
                self.y += GRAVITY

        print(self.x, self.y, self.x//8, self.y//8)
    
    def draw(self):
        px.blt(self.x, self.y, 0, 0, 16, 8, 8, 0)

class Jeu:
    def __init__(self, h, l, titre):
        px.init(h, l, title=titre)
        px.load("res.pyxres", True, True, False, False)
        self.salle = [0, 0]
        self.joueur = Joueur(55, 55)
        self.menu = True
        px.run(self.update, self.draw)
        
    def update(self):
        if not self.menu:
            self.joueur.move()
        if self.joueur.x==0 or self.joueur.x==120 or self.joueur.y==0 or self.joueur.y==120:
            self.salle = self.changementSalle()
            
    def draw(self):
        px.bltm(0, 0, 0, self.salle[0]*8, self.salle[1]*8, 128, 128)
        if self.menu == True:
            px.text(1, 50, "Appuyez sur ESPACE pour jouer", 6)
            if px.btn(px.KEY_SPACE):
                self.menu = False
        else:
            self.joueur.draw()
    
    def changementSalle(self):
            if self.joueur.x==120:
                self.joueur.mapx, self.joueur.mapy = choice(FROM_LEFT)
                self.joueur.x=1                
            if self.joueur.x==0:
                self.joueur.mapx, self.joueur.mapy = choice(FROM_RIGHT)
                self.joueur.x=119             
            if self.joueur.y==0:
                self.joueur.mapx, self.joueur.mapy = choice(FROM_DOWN)
                self.joueur.y=112                
            if self.joueur.y==120:
                self.joueur.mapx, self.joueur.mapy = choice(FROM_UP)
                self.joueur.y=1
            return (self.joueur.mapx, self.joueur.mapy)
            

Jeu(128, 128, "Rogue Runner")
