# coding: utf-8

from outils import *

class Sommet():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.listeIdTuile = []
        self.listeIdAretes = []
        self.contenu = None

    # ----------------------------------------------------
    def affiche(self):
        # pygame.draw.circle(SCREEN, ROUGE, (self.x, self.y), MARGE_CLIC, 1)
        pass

    # ----------------------------------------------------
    def clic(self, x_souris, y_souris):
        d = math.sqrt((x_souris - self.x)**2 + (y_souris - self.y)**2)
        if d < MARGE_CLIC:
            return True
        return False