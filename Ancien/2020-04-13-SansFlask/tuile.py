# coding: utf-8

from outils import *

class Tuile():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.x_affiche = int(self.x - largeur_tuile / 2)
        self.ressource = 0
        # self.image = None
        self.numero = 0
        self.listeIdSommets = []
        self.listeIdAretes = []
        self.voleur = False

    # ----------------------------------------------------
    def affiche(self):
        if self.ressource == RESSOURCE_BOIS:
            image = IMAGE_TUILE_BOIS
        elif self.ressource == RESSOURCE_ARGILE:
            image = IMAGE_TUILE_ARGILE
        elif self.ressource == RESSOURCE_MOUTON:
            image = IMAGE_TUILE_MOUTON
        elif self.ressource == RESSOURCE_FOIN:
            image = IMAGE_TUILE_FOIN
        elif self.ressource == RESSOURCE_PIERRE:
            image = IMAGE_TUILE_PIERRE
        else:
            image = IMAGE_TUILE_DESERT
        SCREEN.blit(image, (self.x_affiche, self.y))
        if self.ressource != RESSOURCE_DESERT:
            self.affiche_numero()
        if self.voleur == True:
            img = IMAGE_VOLEUR_NUMERO
            if self.ressource == RESSOURCE_DESERT:
                img = IMAGE_VOLEUR
            SCREEN.blit(img, (self.x - LARGEUR_IMAGE_VOLEUR / 2, self.y + hauteur_tuile / 2 - HAUTEUR_IMAGE_VOLEUR / 2))

    # ----------------------------------------------------
    def affiche_numero(self):
        rayon_numero = 20
        pygame.draw.circle(SCREEN, BLANC, (self.x, int(self.y + hauteur_tuile / 2)), rayon_numero, 0)
        pygame.gfxdraw.aacircle(SCREEN, self.x, int(self.y + hauteur_tuile / 2), rayon_numero, NOIR)
        pygame.gfxdraw.aacircle(SCREEN, self.x, int(self.y + hauteur_tuile / 2), rayon_numero-2, NOIR)
        c = NOIR
        t = 35
        if self.numero == 6 or self.numero == 8:
            c = ROUGE
            t += 10
        elif self.numero == 5 or self.numero == 9:
            t += 10
        elif self.numero == 11 or self.numero == 3:
            t -= 5
        elif self.numero == 12 or self.numero == 2:
            t -= 10

        affiche_texte(str(self.numero), self.x, int(self.y + hauteur_tuile / 2 + 2), None, t, c, centrer=True)

    # ----------------------------------------------------
    def clic(self, x_souris, y_souris):
        xc = self.x
        yc = self.y + hauteur_tuile / 2
        d = math.sqrt((x_souris - xc)**2 + (y_souris - yc)**2)
        if d < largeur_tuile / 2:
            return True
        return False
