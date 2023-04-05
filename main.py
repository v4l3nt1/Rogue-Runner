import pyxel

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 10
        self.height = 16
        self.jump_force = -4
        self.gravity = 0.2
        self.is_on_ground = False

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if pyxel.btn(pyxel.KEY_LEFT):
            self.vx = -2
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.vx = 2
        else:
            self.vx = 0

        self.vy += self.gravity

        if pyxel.btn(pyxel.KEY_SPACE) and self.is_on_ground:
            self.vy = self.jump_force

        self.is_on_ground = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 11)

class Ground:
    def __init__(self, y):
        self.y = y

    def draw(self):
        pyxel.rect(0, self.y, pyxel.width, pyxel.height - self.y, 3)

    def collides_with(self, player):
        return (player.y + player.height >= self.y
                and player.y + player.height - player.vy < self.y
                and player.x + player.width > 0
                and player.x < pyxel.width)

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Platformer")
        self.player = Player(80, 60)
        self.ground = Ground(100)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

        if self.ground.collides_with(self.player):
            self.player.y = self.ground.y - self.player.height
            self.player.vy = 0
            self.player.is_on_ground = True

        if self.player.y + self.player.height > pyxel.height:
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_P):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        self.ground.draw()
        self.player.draw()

if __name__ == "__main__":
    App()
