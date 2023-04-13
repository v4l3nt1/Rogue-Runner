import pyxel as px

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
