# coding: utf-8

from outils import *

class Arete():
    def __init__(self, id, sommet1, sommet2):
        self.id = id
        self.listeIdSommets = [sommet1.id, sommet2.id]
        self.x1 = sommet1.x
        self.y1 = sommet1.y
        self.x2 = sommet2.x
        self.y2 = sommet2.y
        self.listeIdTuiles = []
        self.contenu = None
        self.ressource_port = None
        self.angle_image_port = 0

    # ----------------------------------------------------
    def affiche(self):
        pygame.draw.line(SCREEN, NOIR, (self.x1, self.y1), (self.x2, self.y2), 1)
        # affiche_texte(str(self.id), int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2), None, 30, NOIR, centrer=True)

        if self.ressource_port != None:
            r = '3_CONTRE_1'
            if self.ressource_port == RESSOURCE_BOIS:
                r = 'BOIS'
            elif self.ressource_port == RESSOURCE_ARGILE:
                r = 'ARGILE'
            elif self.ressource_port == RESSOURCE_MOUTON:
                r = 'MOUTON'
            elif self.ressource_port == RESSOURCE_FOIN:
                r = 'FOIN'
            elif self.ressource_port == RESSOURCE_PIERRE:
                r = 'PIERRE'

            image = eval('IMAGE_PORT_' + r + '__' + str(self.angle_image_port))
            largeur = eval('LARGEUR_IMAGE_PORT__' + str(self.angle_image_port))
            hauteur = eval('HAUTEUR_IMAGE_PORT__' + str(self.angle_image_port))

            x = (self.x1 + self.x2) / 2 + math.cos(self.angle_image_port * math.pi / 180) * COTE_TUILE / 2 - largeur / 2
            y = (self.y1 + self.y2) / 2 - math.sin(self.angle_image_port * math.pi / 180) * COTE_TUILE / 2 - hauteur / 2

            SCREEN.blit(image, (int(x), int(y)))

    # ----------------------------------------------------
    def clic(self, x_souris, y_souris):
        xc = (self.x1 + self.x2) /2
        yc = (self.y1 + self.y2) /2
        d = math.sqrt((x_souris - xc)**2 + (y_souris - yc)**2)
        if d < MARGE_CLIC:
            return True
        return False