import pyxel as px

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
            if self.y > 8:
                self.y -= self.vitesse
        if px.btn(px.KEY_Q):
            if self.x > 8:
                self.x -= self.vitesse
        if px.btn(px.KEY_S):
            if self.y < 120:
                self.y += self.vitesse
        if px.btn(px.KEY_D):
            if self.x < 120:
                self.x += self.vitesse
        if px.btnr(px.KEY_SPACE):
            return self.x+4, self.y-2
        return None
    
    def draw(self):
        px.blt(self.x, self.y, 0, 0, 16, 8, 8, 0)

class Jeu:
    def __init__(self, h, l, titre):
        px.init(h, l, title=titre)
        px.load("res.pyxres", True, True, False, False)
        self.joueur = Hero(55, 55)
        self.menu = True
        px.run(self.update, self.draw)
        
    def update(self):
        if not self.menu:
            self.joueur.move()

    def draw(self):
        px.cls(0)
        px.bltm(0, 0, 0, 0, 0, 128, 128, 0)
        if self.menu == True:
            px.text(1, 50, "Appuyez sur ESPACE pour jouer", 6)
            if px.btn(px.KEY_SPACE):
                self.menu = False
        else:
            self.joueur.draw()

Jeu(128, 128, "Rogue Runner")