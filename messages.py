# coding: utf-8

from outils import *

class Messages():
    def __init__(self, x, y, font=POLICE_NONE, tailleTexte=30, couleurTexte=NOIR):
        self.x = x
        self.y = y
        self.largeur = 400
        self.hauteur = 500
        self.largeur_fleche = 10
        self.hauteur_fleche = 16
        self.largeur_trait_fleche = 5
        self.x_affichage = self.x + self.largeur_fleche
        self.y_affichage = MARGES
        self.tailleTexte = tailleTexte
        self.police = pygame.font.Font(font, int(self.tailleTexte / COEF_POLICE))
        self.couleurTexte = couleurTexte
        self.marge = 8
        self.x_texte = self.x_affichage + self.marge
        self.y_texte = self.y_affichage + self.hauteur - self.tailleTexte - self.marge
        self.largeur_bouton_envoyer = 60

        self.bouton_envoyer = Bouton(self.x_affichage + self.largeur - self.marge - self.largeur_bouton_envoyer, self.y_texte, 'envoyer', largeur=self.largeur_bouton_envoyer, hauteur=self.tailleTexte, texte='ENVOYER', tailleTexte=int(self.tailleTexte / 2))

        self.message = ''
        self.texte_surface = self.police.render(self.message, True, self.couleurTexte)
        self.actif = False

    def reinitialise(self):
        # self.message = ''
        # self.texte_surface = self.police.render(self.message, True, self.couleurTexte)
        self.actif = True

    def affiche(self, listeMessages, maCouleur):
        pygame.draw.polygon(SCREEN, NOIR, ((self.x, self.y), (self.x + self.largeur_fleche, self.y - self.hauteur_fleche / 2), (self.x + self.largeur_fleche, self.y + self.hauteur_fleche / 2)), 0)
        rectangle(self.x_affichage, self.y_affichage, self.largeur, self.hauteur)
        pygame.draw.polygon(SCREEN, BLANC, ((self.x + self.largeur_trait_fleche, self.y), (self.x + self.largeur_fleche + self.largeur_trait_fleche, self.y - self.hauteur_fleche / 2), (self.x + self.largeur_fleche + self.largeur_trait_fleche, self.y + self.hauteur_fleche / 2)), 0)

        SCREEN.blit(self.texte_surface, (self.x_texte + int(self.tailleTexte / 4), self.y_texte + int(self.tailleTexte / 4)))
        c = GRIS_CLAIR
        if self.actif:
            c = GRIS_FONCE
        pygame.draw.rect(SCREEN, c, (self.x_texte, self.y_texte, self.largeur - 3 * self.marge - self.largeur_bouton_envoyer, self.tailleTexte), 3)
        self.bouton_envoyer.affiche()
        l = listeMessages[:]
        l.reverse()
        y = self.y_texte
        acienne_couleur = None
        for message, couleur in l:
            if couleur == BLANC:
                c = NOIR
            else:
                c = couleur
            t_surface = self.police.render(message, True, c)
            if acienne_couleur == couleur:
                y += int(self.tailleTexte / 4)
            y -= self.tailleTexte
            if y <= self.y_affichage + self.marge:
                break
            if couleur == maCouleur:
                SCREEN.blit(t_surface, (self.x_affichage + self.largeur - self.marge - int(self.tailleTexte / 4) - t_surface.get_width(), y))
            else:
                SCREEN.blit(t_surface, (self.x_texte + int(self.tailleTexte / 4), y))
            acienne_couleur = couleur

    def gere_clavier(self, event):
        r = None
        if event.type == pygame.KEYDOWN:
            if self.actif:
                if event.key == pygame.K_RETURN or event.key == 271:
                    if self.message != '':
                        r = self.message
                        self.message = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.message = self.message[:-1]
                else:
                    self.message += event.unicode

                self.texte_surface = self.police.render(self.message, True, self.couleurTexte)
                while self.texte_surface.get_width() > self.largeur - 5 * self.marge - self.largeur_bouton_envoyer:
                    self.message = self.message[:-1]
                    self.texte_surface = self.police.render(self.message, True, self.couleurTexte)

        return r

    def gere_clic(self, x_souris, y_souris):
        if self.x_texte <= x_souris <= self.x_texte + self.largeur - 2 * self.marge and self.y_texte <= y_souris <= self.y_texte + self.tailleTexte:
            self.actif = True
        else:
            self.actif = False
        r = None
        if self.bouton_envoyer.clic(x_souris, y_souris):
            if self.message != '':
                r = self.message
                self.message = ''
                self.texte_surface = self.police.render(self.message, True, self.couleurTexte)
        return r