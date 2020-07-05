# coding: utf-8

from outils import *


class Stats:
    def __init__(self, nomJoueurs):
        self.bouton = Bouton(X_PLATEAU - MARGES_PLATEAU + MARGES, HAUTEUR - HAUTEUR_IMAGE_BOUTON_MESSAGES - MARGES,
                             'stats', image=IMAGE_BOUTON_STATS)
        self.ecartNumeros = 48
        self.yNumero = self.bouton.y - 50
        self.largeur = int(11.5 * self.ecartNumeros)
        self.hauteur = 362
        self.x = int(self.bouton.x - self.largeur / 2 + self.bouton.largeur / 2)
        self.y = self.bouton.y - self.hauteur - 12
        self.dictionnaireNombre = {numero: {nom: 0 for nom in nomJoueurs} for numero in range(2, 13)}
        self.nomCouleursJoueurs = []
        for nom in nomJoueurs:
            couleur = NOIR
            if nom == 'r':
                couleur = ROUGE
            elif nom == 'o':
                couleur = ORANGE
            elif nom == 'b':
                couleur = BLEU
            self.nomCouleursJoueurs.append((nom, couleur))
        self.echelleCran = 100
        self.xc_fleche = self.x + self.largeur / 2
        self.yb_fleche = self.y + self.hauteur
        self.x_min = self.xc_fleche - self.largeur + 15
        self.x_max = self.xc_fleche - 15

    def affiche(self):
        self.bouton.affiche()
        if self.bouton.selectionner:
            pygame.draw.polygon(SCREEN, NOIR, [(self.xc_fleche, self.yb_fleche + 10),
                                               (self.xc_fleche + 12, self.yb_fleche - 9),
                                               (self.xc_fleche - 12, self.yb_fleche - 9)])
            rectangle(self.x, self.y, self.largeur, self.hauteur)
            pygame.draw.polygon(SCREEN, BLANC, [(self.xc_fleche, self.yb_fleche + 10 - 6),
                                                (self.xc_fleche + 12, self.yb_fleche - 9 - 6),
                                                (self.xc_fleche - 12, self.yb_fleche - 9 - 6)])
            x = self.x - int(1 / 4 * self.ecartNumeros)
            for numero in range(2, 13):
                x += self.ecartNumeros
                if numero == 7:
                    SCREEN.blit(IMAGE_PETIT_VOLEUR, (x - LARGEUR_IMAGE_PETIT_VOLEUR / 2,
                                                     self.yNumero - HAUTEUR_IMAGE_PETIT_VOLEUR / 2))
                else:
                    affiche_numero(x, self.yNumero, numero)
                y = int(self.yNumero - self.ecartNumeros / 4 * 3)
                for nom, couleur in self.nomCouleursJoueurs:
                    dy = int(self.dictionnaireNombre[numero][nom] * self.echelleCran)
                    if dy != 0:
                        pygame.draw.line(SCREEN, couleur, (x, y), (x, y - dy), 20)
                    y -= dy

    def ajouteNumero(self, nomJoueur, numero):
        self.dictionnaireNombre[numero][nomJoueur] += 1
        cran = (self.yNumero - self.y - self.ecartNumeros) / sum(self.dictionnaireNombre[numero].values())
        if cran < self.echelleCran:
            self.echelleCran = cran

    def clic(self, x_souris, y_souris):
        if self.bouton.clic(x_souris, y_souris):
            if self.bouton.selectionner:
                self.bouton.selectionner = False
            else:
                self.bouton.selectionner = True
            return True
        return False

    def gere_clavier(self, fleche_droite, fleche_gauche):
        if fleche_gauche:
            self.x -= 8
            if self.x < self.x_min:
                self.x = self.x_min
        if fleche_droite:
            self.x += 8
            if self.x > self.x_max:
                self.x = self.x_max
