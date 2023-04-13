import pyxel as px

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
