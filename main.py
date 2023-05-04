import pyxel as px
from random import * 

WALLS = (1,0)
FROM_RIGHT = [(32,0),(48,0),(96,0),(128,0),(160,0),(192,0),(208,0),(224,0)]
FROM_LEFT = [(32,0),(64,0),(80,0),(128,0),(144,0),(176,0),(192,0),(224,0)]
FROM_UP = [(0,0),(16,0),(80,0),(96,0),(128,0),(176,0),(208,0),(224,0)]
FROM_DOWN = [(16,0),(32,0),(48,0),(64,0),(80,0),(96,0),(112,0),(128,0)]

class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.atk = 2
        self.vitesse = 1

    def move(self):
        if px.btn(px.KEY_Z):
            if px.tilemap(0).pget(self.x//8, (self.y-1)//8) != WALLS and px.tilemap(0).pget((self.x+7)//8, (self.y-1)//8) != WALLS:
                self.y -= self.vitesse 
        if px.btn(px.KEY_Q):
            if px.tilemap(0).pget((self.x-1)//8, self.y//8) != WALLS and px.tilemap(0).pget((self.x-1)//8, (self.y+7)//8) != WALLS:
                self.x -= self.vitesse
        if px.btn(px.KEY_S):
            if px.tilemap(0).pget(self.x//8, (self.y+8)//8) != WALLS and px.tilemap(0).pget((self.x+7)//8, (self.y+8)//8) != WALLS:
                self.y += self.vitesse
        if px.btn(px.KEY_D):
            if px.tilemap(0).pget((self.x+8)//8, self.y//8) != WALLS and px.tilemap(0).pget((self.x+8)//8, (self.y+7)//8) != WALLS:
                self.x += self.vitesse
        print(self.x, self.y, self.x//8, self.y//8)
       
    
    def changementSalle(self):
        if self.x==127:
            mapx, mapy = choice(FROM_LEFT)
            self.x=8                
        if self.x==0:
            mapx, mapy = choice(FROM_RIGHT)
            self.x=112              
        if self.y==0:
            mapx, mapy = choice(FROM_DOWN)
            self.y=112                
        if self.y==127:
            mapx, mapy = choice(FROM_UP)
            self.y=8
        return (mapx, mapy)

    def draw(self):
        px.blt(self.x, self.y, 0, 0, 16, 8, 8, 0)

class Jeu:
    def __init__(self, h, l, titre):
        px.init(h, l, title=titre)
        px.load("res.pyxres", True, True, False, False)
        self.salle = (0, 0)
        self.joueur = Hero(55, 55)
        self.menu = True
        px.run(self.update, self.draw)
        
    def update(self):
        if not self.menu:
            self.joueur.move()

    def draw(self):
        px.cls(0)
        px.bltm(0, 0, 0, self.salle[0], self.salle[1], 128, 128, 0)
        if self.menu == True:
            px.text(1, 50, "Appuyez sur ESPACE pour jouer", 6)
            if px.btn(px.KEY_SPACE):
                self.menu = False
        else:
            self.joueur.draw()
        if self.joueur.x==0 or self.joueur.x==127 or self.joueur.y==0 or self.joueur.y==127:
            self.salle = self.joueur.changementSalle()
            

Jeu(128, 128, "Rogue Runner")