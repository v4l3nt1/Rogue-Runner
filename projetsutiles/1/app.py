import pyxel
from random import randint

"""
-------- DUNGEON SIMULATOR --------
Appuyer sur les flèches directionnelles pour vous déplacer. "Espace" pour tirer, "D" pour acheter un boost de degat contre 250 d'argent, "A" pour acheter un boost d'argent contre 500 d'argent et
V pour acheter un boost de vitesse contre 500 d'argent (limité à 4 achat).

Le but est de faire le meilleur score tout en changeant de salle. Pour gagner du score il faut éliminer des ennemis mais attention à ne pas les touchers !

Appuyer sur R pour recommencer à tout moment et Q pour quitter.
"""

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du c0de 2022")
        pyxel.load("mirou.pyxres")
        pyxel.playm(0, loop=True)

        self.score = 0
        self.argent = 0
        self.liste_ennemi = []
        self.col = 12
        self.boost_dgt = 1
        self.boost_argent = 1
        self.boost_vitesse = 1
        self.liste_tire = []
        self.nouvelle_salle = True
        self.x = 60
        self.y = 60
        self.co_salle=[(128,128),(152,128)]
        self.salle_right=[(128,128),(152,128),(128,152),(176,128)]
        self.salle_left=[(128,128),(152,128),(128,152),(176,152)]
        self.salle_up=[(96,152),(128,128),(152,152),(152,128),(176,176),(176,152)]
        self.salle_down=[(96,128),(176,128),(152,128),(128,128),(152,152),(96,152)]
        self.i=0
        self.direction_visee = "H"
        self.compteur = 0
        self.menu = True
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.score = 0
            self.argent = 0
            self.co_salle=[(128,128),(152,128)]
            self.x = 60
            self.y = 60
            self.nouvelle_salle = True
            self.col = 12
            self.menu = True

        if self.compteur < 25:
            self.compteur += 1
        self.changement_salle()
        self.deplacement_perso()

    def draw(self):
        if self.menu == True:
            pyxel.bltm(0, 0, 0, self.co_salle[self.i][0]*8, self.co_salle[self.i][1]*8, 128, 128)
            pyxel.text(1, 10, "Appuyez sur ESPACE pour jouer", 6)
            pyxel.text(1, 30, "A : 500 argent pour + d'argent", 3)
            pyxel.text(1, 50, "D : 250 argent pour + de degat", 3)
            pyxel.text(1, 70, "V : 500 argent pour + de vitesse", 3)
            if pyxel.btn(pyxel.KEY_SPACE):
                self.menu = False
            
        else:    
            pyxel.bltm(0, 0, 0, self.co_salle[self.i][0]*8, self.co_salle[self.i][1]*8, 128, 128)
            personnage = pyxel.rect(self.x, self.y, 8, 8, self.col)
            pyxel.text(85-(self.score*0.01), 8, "Score :"+str(self.score), 13)

            self.tire()
            self.monnaie()
            self.ennemi()            

    def deplacement_perso(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and pyxel.tilemap(0).pget((self.x + 8) % pyxel.width//8+self.co_salle[self.i][0],self.y//8+self.co_salle[self.i][1]) in [(1,5),(4,4)] and pyxel.tilemap(0).pget((self.x + 8) % pyxel.width//8+self.co_salle[self.i][0],(self.y + 7) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4)]:
            self.x = (self.x + 1*self.boost_vitesse) % pyxel.width  
            self.direction_visee = "D"
            
        if pyxel.btn(pyxel.KEY_LEFT) and pyxel.tilemap(0).pget((self.x - 1) % pyxel.width//8+self.co_salle[self.i][0],self.y//8+self.co_salle[self.i][1])in [(1,5),(4,4)] and pyxel.tilemap(0).pget((self.x - 1) % pyxel.width//8+self.co_salle[self.i][0],(self.y + 7) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4)]:
            self.x = (self.x - 1*self.boost_vitesse) % pyxel.width
            self.direction_visee = "G"
            
        if pyxel.btn(pyxel.KEY_UP) and pyxel.tilemap(0).pget(self.x//8+self.co_salle[self.i][0],(self.y - 1) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4)] and pyxel.tilemap(0).pget((self.x + 7) % pyxel.width//8+self.co_salle[self.i][0],(self.y - 1) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4)]:
            self.y = (self.y - 1*self.boost_vitesse) % pyxel.width
            self.direction_visee = "H"
            
        if pyxel.btn(pyxel.KEY_DOWN) and pyxel.tilemap(0).pget(self.x//8+self.co_salle[self.i][0],(self.y + 8) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4)] and pyxel.tilemap(0).pget((self.x + 7) % pyxel.width//8+self.co_salle[self.i][0],(self.y + 8) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4)]:
            self.y = (self.y + 1*self.boost_vitesse) % pyxel.width
            self.direction_visee = "B"

        for i in self.liste_ennemi:
            if i["x"]-12 < self.x < i["x"]+6 and i["y"]-12 < self.y < i["y"]+6 and self.compteur >= 25:
                self.compteur = 0
                if self.col == 12:
                    self.col = 5
                elif self.col == 5:
                    self.col = 1
                elif self.col == 1:
                    self.score = 0
                    self.argent = 0
                    self.co_salle=[(128,128),(152,128)]
                    self.x = 60
                    self.y = 60
                    self.nouvelle_salle = True
                    self.col = 12
                    self.menu = True
            

    def tire(self):
        delete_list=[]
        if self.nouvelle_salle == True:
            self.liste_tire = []
            
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.liste_tire.append({"direction":self.direction_visee,"x":self.x+4, "y":self.y+4})

        for i in range(len(self.liste_tire)):     
                if self.liste_tire[i]["direction"] == "D":
                    self.liste_tire[i]["x"] += 3
                elif self.liste_tire[i]["direction"] == "G":
                    self.liste_tire[i]["x"] -= 3
                elif self.liste_tire[i]["direction"] == "H":
                    self.liste_tire[i]["y"] -= 3
                elif self.liste_tire[i]["direction"] == "B":
                    self.liste_tire[i]["y"] += 3
                pyxel.circb(self.liste_tire[i]["x"], self.liste_tire[i]["y"], 2, 6)
                for y in self.liste_ennemi:
                    if y["x"]-6 < self.liste_tire[i]["x"] < y["x"]+6 and y["y"]-6 < self.liste_tire[i]["y"] < y["y"]+6:
                        y["pv"] -= 1 * self.boost_dgt
                        y["col"] = 9
                
                if 8 > self.liste_tire[i]["x"] or self.liste_tire[i]["x"] > 112 or 8 > self.liste_tire[i]["y"] or self.liste_tire[i]["y"] > 112:
                    delete_list.append(i)

        if delete_list != []:
            delete_list.sort(reverse=True)
            for j in range(len(delete_list)):
                self.liste_tire.pop(j)
            delete_list=[]
            
    def ferme_salle(self,x,y):
        for i in range(2):
            if pyxel.tilemap(0).pget(self.co_salle[self.i][0]+7+i,self.co_salle[self.i][1]) in [(1,5),(5,6)]:
                pyxel.tilemap(0).pset(self.co_salle[self.i][0]+7+i,self.co_salle[self.i][1],(x,y))
            if pyxel.tilemap(0).pget(self.co_salle[self.i][0]+15,self.co_salle[self.i][1]+7+i) in [(1,5),(5,6)]:
                pyxel.tilemap(0).pset(self.co_salle[self.i][0]+15,self.co_salle[self.i][1]+7+i,(x,y))
            if pyxel.tilemap(0).pget(self.co_salle[self.i][0],self.co_salle[self.i][1]+7+i) in [(1,5),(5,6)]:
                pyxel.tilemap(0).pset(self.co_salle[self.i][0],self.co_salle[self.i][1]+7+i,(x,y))
            if pyxel.tilemap(0).pget(self.co_salle[self.i][0]+7+i,self.co_salle[self.i][1]+15) in [(1,5),(5,6)]:
                pyxel.tilemap(0).pset(self.co_salle[self.i][0]+7+i,self.co_salle[self.i][1]+15,(x,y))
                
    def ennemi(self):
        if self.nouvelle_salle == True:
            self.ferme_salle(5,6)
            self.nouvelle_salle = False
            self.liste_ennemi = []
            
            for i in range(randint(2,4)):
                if i == 0:
                    x_ennemi = randint(20, 50)
                    y_ennemi = randint(20, 50)
                elif i == 1:
                    x_ennemi = randint(50, 112)
                    y_ennemi = randint(50, 112)
                elif i == 2:
                    x_ennemi = randint(20, 50)
                    y_ennemi = randint(50, 112)
                elif i == 3:
                    x_ennemi = randint(50, 112)
                    y_ennemi = randint(20, 50)                    

                dictionnaire = {"pv":randint(10,25), "x":x_ennemi, "y":y_ennemi, "col":10}               
                self.liste_ennemi.append(dictionnaire) #creer un nombre aléatoire d'ennemis dans une liste avec des pv et coordonnée aléatoires
        else:
            for i in self.liste_ennemi:
                if i["pv"] > 0 :
                    
                    x_alea = randint(-2,2)
                    y_alea = randint(-2,2)
                    if 110 > i["x"]+x_alea > 10 and 110 > i["y"]+y_alea > 10:
                        mouvement = randint(1,5)
                        if mouvement == 1:
                            i["x"] += randint(-1,1)
                            i["y"] += randint(-1,1)
    
                    pyxel.circ(i["x"], i["y"], 4, i["col"])
                    i["col"] = 10
                    
                elif i["pv"] <= 0:
                    self.score += 10
                    self.argent += 20 * self.boost_argent
                    self.liste_ennemi.pop(self.liste_ennemi.index(i))
            if self.liste_ennemi == []:
                self.ferme_salle(1,5)

                
    def changement_salle(self):
        if self.x==0 or self.x==127 or self.y==0 or self.y==127:
            if self.x==127:
                print(self.x,self.y)
                self.co_salle=self.salle_right
                self.x=8
                self.i=randint(0,len(self.co_salle)-1)
            if self.x==0:
                self.co_salle=self.salle_left
                self.x=112
                self.i=randint(0,len(self.co_salle)-1)
                
            if self.y==0:
                self.co_salle=self.salle_down
                self.y=112
                self.i=randint(0,len(self.co_salle)-1)
                
            if self.y==127:
                self.co_salle=self.salle_up
                self.y=8
                self.i=randint(0,len(self.co_salle)-1)
                
            self.nouvelle_salle = True

    def monnaie(self):
        pyxel.text(8, 8, "Argent :"+str(self.argent), 3)
        if pyxel.btn(pyxel.KEY_D) and self.argent >= 250:
            self.boost_dgt =+ 2
            self.argent -= 250
        elif pyxel.btn(pyxel.KEY_A) and self.argent >= 500:
            self.boost_argent += 1
            self.argent -= 500
        elif pyxel.btn(pyxel.KEY_V) and self.argent >= 500 and self.boost_vitesse < 2:
            self.boost_vitesse += 0.25
            self.argent -= 500

App()