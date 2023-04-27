import pyxel as pxl
from random import randint, choice
from math import sqrt
from time import time, sleep

'''
Utiliser : -les flèches directionnelles pour se déplacer
           -la barre espace pour taper à l'épée

Les portes sont active seulement après la mort de l'intégralité des monstres de la salle

Lors de l'apparition dans une salle, un temps d'invincibilité vous est octroyé, mais vous ne pouvez plus utiliser votre épée

Si un monstre vous touche, vous mourez =)
'''

WALL = [(5, 3), (6, 3), (7, 3), (5, 4), (5, 5), (6, 5), (7, 5), (7, 4), (6, 2), (6, 6), (6, 7), (7, 7), (7, 6), (2, 6)]
FROM_RIGHT = [(128, 0), (256, 0), (512, 0), (512+128, 0), (512+256, 0), (1024, 0), (1024+128, 0), (1024+256, 0)]
FROM_LEFT = [(0, 0), (128, 0),(256, 0), (512, 0), (512+128, 0), (512+256, 0), (1024, 0), (1024+128, 0), (1024+256, 0)]
FROM_DOWN = [(0, 0), (128, 0), (256, 0), (512, 0), (512+128, 0), (512+256, 0), (1024, 0), (1024+128, 0), (1024+256, 0)]
FROM_UP = [(0, 0), (128, 0), (256, 0), (256+128, 0), (512, 0), (512+128, 0), (512+256, 0), (1024, 0), (1024+128, 0), (1024+256, 0)]
map_x = 0
map_y = 0
invincible = 0
terminate = False

def get_pixel(x, y):
    return pxl.tilemap(1).pget(x, y)

class Jeu:
    def __init__(self):
        pxl.init(128, 128, title="Nuit du c0de 2022")
        pxl.load("1v12.pyxres")
        invincible = 0
        pxl.run(self.update, self.draw)
    
    def add_ennemi(self):
        global ennemi
        global map_x
        global map_y
        for i in range(randint(1, 5)):
            x_ = randint(8, 120)
            y_ = randint(8, 120)
            print(joueur.x, x_+map_x, joueur.y, y_+map_y)
            while get_pixel(x_//8, y_//8) in WALL and sqrt((joueur.x - x_+map_x)**2 + (joueur.y - y_+map_y)**2) < 100:
                x_ = randint(8, 120)
                y_ = randint(8, 120)
            ennemi.append(Ennemi(x_, y_))
    
    def update(self):
        global terminate
        if not terminate:
            global invincible
            if time() - invincible > 1:
                coll = joueur.collisions(0, 0)
                for e in ennemi:
                    if e in coll:
                        joueur.vie -= 1
                if joueur.vie <= 0:
                    terminate = True
            tmp = None
            if ennemi == []:
                if joueur.x%128 >= 120:
                    tmp = FROM_RIGHT
                    f = (20, 64)
                elif joueur.x%128 <= 0:
                    tmp = FROM_LEFT
                    f = (112, 64)
                elif joueur.y%128 >= 120:
                    tmp = FROM_DOWN
                    f = (64, 20)
                elif joueur.y%128 <= 0:
                    tmp = FROM_UP
                    f = (64, 112)
            if tmp is not None:
                global map_x
                global map_y
                map_x, map_y = choice(tmp)
                joueur.x = f[0] + map_x
                joueur.y = f[1] + map_y
                self.add_ennemi()
                invincible = time()
        
            joueur.maj_mouvements()
            for en in ennemi:
                en.maj_mouvements()
        else:
            pass
    
    def draw(self):
        if not terminate:
            pxl.bltm(0, 0, 1, map_x, map_y, 128, 128)
            joueur.draw()
            for en in ennemi:
                en.draw()
        else:
            pxl.bltm(0, 0, 2, 0, 0, 128, 128, 2)
            pxl.text(32, 64, "VOUS ETES MORT :)", 8)
            
class Entite:
    def __init__(self, x, y, w=8, h=8):
        self.x = x + map_x
        self.y = y + map_y
        self.h = h
        self.w = w
    
    def maj_mouvements(self, dx, dy):
        m_x = 0
        m_y = 0
        tmp_m_x = -1
        tmp_m_y = -1
        while (dx != 0 or dy != 0) and (m_x, m_y) != (tmp_m_x, tmp_m_y):
            coll = self.collisions(dx, dy)
            tmp_m_x = m_x
            tmp_m_y = m_y
            if dx > 0 and "x+" not in coll:
                m_x += 1
                dx -= 1
            elif dx < 0 and "x-" not in coll:
                m_x -= 1
                dx += 1
            if dy > 0 and "y+" not in coll: 
                m_y += 1
                dy -= 1
            elif dy < 0 and "y-" not in coll:
                m_y -= 1
                dy += 1
        self.x += m_x
        self.y += m_y
    
    def draw(self, x, y, u, v, w=8, h=8):
        pxl.blt(x - map_x, y - map_y, 0, u, v, w, h, 2)
    
    def collisions(self, dx, dy):
        res = []
        if dx != 0:
            if dx > 0:
                sign = self.w
                tmp = "+"
            else:
                sign = -1
                tmp = "-"
            for y in range(self.y, self.y + self.h):
                if get_pixel((self.x + sign)//8, y//8) in WALL:
                    res.append("x"+tmp)
            
        if dy != 0:
            if dy > 0:
                sign = self.h
                tmp = "+"
            else:
                sign = -1
                tmp = "-"
            for x in range(self.x, self.x + self.w):
                if get_pixel(x//8, (self.y + sign)//8) in WALL:
                    res.append("y"+tmp)
                    
        global invincible
        if time() - invincible > 1:
            for e in ennemi + [joueur]:
                if e.x == self.x and e.y == self.y:
                    continue
                x_ = None
                y_ = None
                
                if e.x < self.x + self.w < e.x + 8:
                    x_ = "x+"
                elif e.x < self.x < e.x + 8:
                    x_ = "x-"
                if e.y < self.y + self.h < e.y + 8:
                    y_ = "y+"
                elif e.y < self.y < e.y + 8:
                    y_ = "y-"
                if (x_ is not None or y_ is not None) and sqrt((e.x-self.x)**2 + (e.y-self.y)**2) < max(self.w, self.h):
                    res.append(x_)
                    res.append(y_)
                    res.append(e)
        
        return res

class Joueur(Entite):
    def __init__(self):
        super().__init__(64, 64)
        self.last_dir = "x+"
        self.epee = None
        self.last_epee = 0
        self.vie = 1
    
    def maj_mouvements(self):
        if time() - self.last_epee > 0.2:
            dx = 0
            dy = 0
            if pxl.btn(pxl.KEY_UP) and self.y%128 > 0:
                dy -= 2
                self.last_dir = "y-"
            elif pxl.btn(pxl.KEY_DOWN) and self.y%128 < 120:
                dy += 2
                self.last_dir = "y+"
            if pxl.btn(pxl.KEY_RIGHT) and self.x%128 < 120:
                dx += 2
                self.last_dir = "x+"
            elif pxl.btn(pxl.KEY_LEFT) and self.x%128 > 0:
                dx -= 2
                self.last_dir = "x-"
            super().maj_mouvements(dx, dy)
            if pxl.btn(pxl.KEY_SPACE):
                self.attaque()
    
    def draw(self):
        if self.epee is not None and time() - self.last_epee < 0.2:
            if self.last_dir == "x+":
                self.epee.draw(self.epee.x, self.epee.y, 48, 96, 16, 8)
            elif self.last_dir == "x-":
                self.epee.draw(self.epee.x, self.epee.y, 48, 96, -16, -8)
            elif self.last_dir == "y+":
                self.epee.draw(self.epee.x, self.epee.y, 48, 80, -8, -16)
            elif self.last_dir == "y-":
                self.epee.draw(self.epee.x, self.epee.y, 48, 80, 8, 16)
        super().draw(self.x, self.y, 0, 16)
    
    def attaque(self):
        if time() - self.last_epee > 0.4:
            self.att = True
            if self.last_dir == "x+":
                self.epee = Entite(self.x + 8 - map_x, self.y  - map_y, 16, 8)
            elif self.last_dir == "x-":
                self.epee = Entite(self.x - 16  - map_x, self.y, 16, 8)
            elif self.last_dir == "y+":
                self.epee = Entite(self.x - map_x, self.y + 8 - map_y, 8, 16)
            elif self.last_dir == "y-":
                self.epee = Entite(self.x - map_x, self.y - 16 - map_y, 8, 16)
            self.last_epee = time()
            
            for i in self.epee.collisions(0, 0):
                if isinstance(i, Ennemi):
                    i.vie -= 1
        
class Ennemi(Entite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vie = 1
    
    def maj_mouvements(self):
        if 1 == 1:
            x_ = self.x - joueur.x
            y_ = self.y - joueur.y
            dx = 0
            dy = 0
            if abs(y_) > abs(x_):
                if y_ > 0:
                    dy -= 1
                else:
                    dy += 1
            else:
                if x_ > 0:
                    dx -= 1
                else:
                    dx += 1
            super().maj_mouvements(dx, dy)
    
    def draw(self):
        if self.vie > 0:
            super().draw(self.x, self.y, 0, 24)
        else:
            i = ennemi.index(self)
            del ennemi[i]

ennemi = []
joueur = Joueur()
Jeu()