# coding: utf-8

from outils import *

class Arete():
    def __init__(self, sommet1, sommet2):
        self.listeSommets = [sommet1, sommet2]
        self.x1 = self.listeSommets[0].x
        self.y1 = self.listeSommets[0].y
        self.x2 = self.listeSommets[1].x
        self.y2 = self.listeSommets[1].y
        self.listeTuiles = []
        self.contenu = None

    # ----------------------------------------------------
    def affiche(self):
        pygame.draw.line(SCREEN, NOIR, (self.x1, self.y1), (self.x2, self.y2), 1)

    # ----------------------------------------------------
    def clic(self, x_souris, y_souris):
        xc = (self.x1 + self.x2) /2
        yc = (self.y1 + self.y2) /2
        d = math.sqrt((x_souris - xc)**2 + (y_souris - yc)**2)
        if d < MARGE_CLIC:
            return True
        return False