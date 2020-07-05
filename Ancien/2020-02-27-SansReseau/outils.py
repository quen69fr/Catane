# coding: utf-8

# --------------------------- IMPORTS ---------------------------
import pygame.gfxdraw
import math
import random

# ---------------------------- ECRAN ----------------------------
LARGEUR = 1300
HAUTEUR = 700

pygame.init()
SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("CATANE par Sarah PALAZON")

FPS = 100

# --------------------------- GENERAL ---------------------------
MARGE_CLIC = 20

MARGES = 10
MARGES_PLATEAU = 20

Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL = 225
HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL = 40

HAUTEUR_TITRE = 130
HAUTEUR_BANDEAU_ACTIONS = 80

# --------------------------- PLATEAU ---------------------------
IMAGE_FOND_EAU = pygame.image.load("Image/FondEau.png")

COTE_TULE = 76
hauteur_tuile = 2 * COTE_TULE
hauteur_triangle_tuile = COTE_TULE / 2
largeur_tuile = math.sqrt(3) * COTE_TULE

TAILLE_DES = 60

X_PLATEAU = int(LARGEUR - largeur_tuile * 5 - MARGES_PLATEAU)
Y_PLATEAU = int((HAUTEUR - 8 * COTE_TULE) / 2)

X_CENTRE_AFFICHAGE_GAUCHE = int((X_PLATEAU - MARGES_PLATEAU - MARGES) / 2 + MARGES)

Y_CENTRE_BANDEAU_ACTIONS = int(MARGES * 2 + HAUTEUR_TITRE + HAUTEUR_BANDEAU_ACTIONS / 2)

X_CENTRE_BANDEAU_ACTIONS_DES = int(X_CENTRE_AFFICHAGE_GAUCHE + (HAUTEUR_BANDEAU_ACTIONS - TAILLE_DES) / 2 + TAILLE_DES)

HAUTEUR_CARRE_JOUEUR_SECONDAIRE = int((HAUTEUR - HAUTEUR_TITRE - 6 * MARGES - HAUTEUR_BANDEAU_ACTIONS) / 3)

# Voir creationPlateau pour comprendre (cf. tx et ty pour la création des tuiles):
LISTE_COORDONNEES_TUILES = [        (2, 0), (4, 0), (6 ,0),
                                (1 ,1), (3 ,1), (5 ,1), (7 ,1),
                            (0 ,2), (2 ,2), (4 ,2), (6 ,2), (8 ,2),
                                (1 ,3), (3 ,3), (5 ,3), (7 ,3),
                                    (2, 4), (4, 4), (6 ,4)          ]
RESSOURCE_BOIS = 0
RESSOURCE_ARGILE = 1
RESSOURCE_MOUTON = 2
RESSOURCE_FOIN = 3
RESSOURCE_PIERRE = 4
RESSOURCE_DESERT = -1
LISTE_RESSOURCES = [    0 , 3 , 0,
                      3 , 1 , 4 , 2,
                    1 , 4 ,-1 , 3 , 2,
                      2 , 0 , 4 , 0,
                        1 , 2 , 3]

LISTE_NUMERO = [   5,  2,  6,
                10,  9,  4,  3,
               8, 11,      5,  8,
                 4,  3,  6, 10,
                  11, 12,  9]

NB_COLONIE_MAX = 5
NB_VILLE_MAX = 4
NB_ROUTE_MAX = 15

PRIX_COLONIE = [RESSOURCE_BOIS, RESSOURCE_ARGILE, RESSOURCE_MOUTON, RESSOURCE_FOIN]
PRIX_ROUTE = [RESSOURCE_BOIS, RESSOURCE_ARGILE]
PRIX_VILLE = [RESSOURCE_FOIN, RESSOURCE_FOIN, RESSOURCE_PIERRE, RESSOURCE_PIERRE, RESSOURCE_PIERRE]
PRIX_CARTE_SPECIALE = [RESSOURCE_MOUTON, RESSOURCE_FOIN, RESSOURCE_PIERRE]

NB_POINT_DE_VICTOIRE = 10

# --------------------------- TUILES ----------------------------
IMAGE_TUILE_BOIS = pygame.image.load("Image/TuileBois.png")
IMAGE_TUILE_ARGILE = pygame.image.load("Image/TuileArgile.png")
IMAGE_TUILE_MOUTON = pygame.image.load("Image/TuileMouton.png")
IMAGE_TUILE_FOIN = pygame.image.load("Image/TuileFoin.png")
IMAGE_TUILE_PIERRE = pygame.image.load("Image/TuilePierre.png")
IMAGE_TUILE_DESERT = pygame.image.load("Image/TuileDesert.png")

IMAGE_CARTE_BOIS = pygame.image.load("Image/CarteBois.png")
IMAGE_CARTE_ARGILE = pygame.image.load("Image/CarteArgile.png")
IMAGE_CARTE_MOUTON = pygame.image.load("Image/CarteMouton.png")
IMAGE_CARTE_FOIN = pygame.image.load("Image/CarteFoin.png")
IMAGE_CARTE_PIERRE = pygame.image.load("Image/CartePierre.png")

# ----------------------- JOUEURS + PIONS + VOLEUR -----------------------
IMAGE_COLONIE = pygame.image.load("Image/Colonie.png")
LARGEUR_IMAGE_COLONIE = IMAGE_COLONIE.get_width()
HAUTEUR_IMAGE_COLONIE = IMAGE_COLONIE.get_height()
def couleur_colonie_image(couleur, x, y):
    pygame.draw.polygon(SCREEN, couleur, ((x + 3 , y + 9), (x + 15, y + 1),  (x + 26, y + 9), (x + 26, y + 25), (x + 3, y + 25)), 0)

IMAGE_VILLE = pygame.image.load("Image/Ville.png")
LARGEUR_IMAGE_VILLE = IMAGE_VILLE.get_width()
HAUTEUR_IMAGE_VILLE = IMAGE_VILLE.get_height()
def couleur_ville_image(couleur, x, y) :
    pygame.draw.polygon(SCREEN, couleur,((x + 3, y + 9), (x + 19, y + 1), (x + 34, y + 9), (x + 34, y + 33), (x + 3, y + 33)), 0)

LARGEUR_ROUTE = 10

IMAGE_JOUEUR = pygame.image.load("Image/Joueur.png")
LARGEUR_IMAGE_JOUEUR = IMAGE_JOUEUR.get_width()
HAUTEUR_IMAGE_JOUEUR = IMAGE_JOUEUR.get_height()

IMAGE_CARTE_DOS = pygame.image.load("Image/CarteDos.png")
LARGEUR_IMAGE_CARTE_DOS = IMAGE_CARTE_DOS.get_width()
HAUTEUR_IMAGE_CARTE_DOS = IMAGE_CARTE_DOS.get_height()

IMAGE_VOLEUR = pygame.image.load("Image/Voleur.png")
LARGEUR_IMAGE_VOLEUR = IMAGE_VOLEUR.get_width()
HAUTEUR_IMAGE_VOLEUR = IMAGE_VOLEUR.get_height()

IMAGE_COURONNE = pygame.image.load("Image/Couronne.png")
LARGEUR_IMAGE_COURONNE = IMAGE_COURONNE.get_width()
HAUTEUR_IMAGE_COURONNE = IMAGE_COURONNE.get_height()

IMAGE_CARTE_DOS_SPECIALE = pygame.image.load("Image/CarteDosSpeciale.png")
LARGEUR_IMAGE_CARTE_DOS_SPECIALE = IMAGE_CARTE_DOS_SPECIALE.get_width()
HAUTEUR_IMAGE_CARTE_DOS_SPECIALE = IMAGE_CARTE_DOS_SPECIALE.get_height()

IMAGE_PETITE_COURONNE_DOREE = pygame.image.load("Image/PetiteCouronneDoree.png")
IMAGE_PETITE_COURONNE_GRISEE = pygame.image.load("Image/PetiteCouronneGrisee.png")
LARGEUR_IMAGE_PETITE_COURONNE = IMAGE_PETITE_COURONNE_DOREE.get_width()
HAUTEUR_IMAGE_PETITE_COURONNE = IMAGE_PETITE_COURONNE_DOREE.get_height()

IMAGE_GRAND_JOUEUR = pygame.image.load("Image/GrandJoueur.png")
LARGEUR_IMAGE_GRAND_JOUEUR = IMAGE_GRAND_JOUEUR.get_width()
HAUTEUR_IMAGE_GRAND_JOUEUR = IMAGE_GRAND_JOUEUR.get_height()

# --------------------------- COULEURS --------------------------
NOIR = (0, 0, 0)
GRIS_FONCE = (50, 50, 50)
GRIS_CLAIR = (190, 190, 190)
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
VERT = (52, 175, 0)
ROUGE = (255, 0, 0)
ORANGE = (255, 127, 0)
JAUNE = (255, 255, 0)


# ---------------------- FONCTIONS et CLASS ---------------------
def rectangle(x, y, largeur, hauteur):
    pygame.draw.rect(SCREEN, BLANC, (x, y, largeur, hauteur), 0)
    pygame.draw.rect(SCREEN, NOIR, (x, y, largeur, hauteur), 3)

# ------------------------
def affiche_texte(texte, x, y, font, taille, couleur, centrer=False):
    police = pygame.font.Font(font, taille)
    surface = police.render(texte, True, couleur)
    rect = surface.get_rect(topleft=(x, y))
    #print(surface.get_rect().centerx)
    if centrer == True:
        rect = surface.get_rect(center=(x, y))


    #print(surface)
    SCREEN.blit(surface, rect)

# ------------------------
def affiche_point_de(x, y, r, c):
    pygame.gfxdraw.aacircle(SCREEN, int(x), int(y), r, c)
    pygame.gfxdraw.filled_circle(SCREEN, int(x), int(y), r, c)

# ------------------------
def affiche_de(x, y, taille, rayonPoints, margePoints, nombre, couleurFont=GRIS_CLAIR, couleurPoints=GRIS_FONCE):
    pygame.draw.rect(SCREEN, couleurFont, (x, y, taille, taille), 0)
    if nombre == 1 or nombre == 3 or nombre == 5:
        affiche_point_de(x + taille / 2, y + taille / 2, rayonPoints, couleurPoints)
    if nombre > 1:
        affiche_point_de(x + taille - margePoints, y + margePoints, rayonPoints, couleurPoints)
        affiche_point_de(x + margePoints, y + taille - margePoints, rayonPoints, couleurPoints)
    if nombre >= 4:
        affiche_point_de(x + margePoints, y + margePoints, rayonPoints, couleurPoints)
        affiche_point_de(x + taille - margePoints, y + taille - margePoints, rayonPoints, couleurPoints)
    if nombre == 6:
        affiche_point_de(x + margePoints, y + taille / 2, rayonPoints, couleurPoints)
        affiche_point_de(x + taille - margePoints, y + taille / 2, rayonPoints, couleurPoints)

# ------------------------
class CaseACocher():
    def __init__(self, x, y, parametre, texte, taille=30, policeTexte=None, tailleTexte=30, couleurTexte=NOIR, etat_initial=False, largeurTrai=3, couleurCase=NOIR, couleurSelect=GRIS_FONCE):
        self.x = x
        self.y = y
        self.parametre = parametre
        self.texte = texte
        self.policeTexte = policeTexte
        self.tailleTexte = tailleTexte
        self.couleurTexte = couleurTexte
        self.etat = etat_initial
        self.taille = taille
        self.largeurTrai = largeurTrai
        self.couleurCase = couleurCase
        self.couleurSelect = couleurSelect

    def affiche(self):
        if self.etat == 1:
            pygame.draw.rect(SCREEN, self.couleurSelect, (self.x, self.y, self.taille, self.taille), 0)
        pygame.draw.rect(SCREEN, self.couleurCase, (self.x, self.y, self.taille, self.taille), self.largeurTrai)
        affiche_texte(self.texte, self.x + int(self.taille * 1.3), self.y + self.taille / 2 - self.tailleTexte / 4, self.policeTexte, self.tailleTexte, self.couleurTexte)

    def clic(self, x_souris, y_souris):
        if self.x <= x_souris and x_souris <= self.x + self.taille and self.y <= y_souris and y_souris <= self.y + self.taille:
            if self.etat == False:
                self.etat = True
            else:
                self.etat = False
            return True
        return False

# ------------------------
class Bouton():
    def __init__(self, x, y, parametre, largeur=0, hauteur=0, texte=None, image=None, policeTexte=None, tailleTexte=30, couleurTexte=GRIS_CLAIR, largeurContour=3, couleurRect=NOIR, couleurCountour=NOIR, selectionner=False, couleurTexteSelec=NOIR, couleurRectSelec=GRIS_CLAIR, centrer=False):
        self.x = x
        self.y = y
        self.image = image
        if self.image != None:
            self.largeur = self.image.get_width()
            self.hauteur = self.image.get_height()
        else:
            self.largeur = largeur
            self.hauteur = hauteur
        if centrer == True:
            self.x -= int(self.largeur / 2)
            self.y -= int(self.hauteur / 2)
        self.parametre = parametre
        self.texte = texte
        self.policeTexte = policeTexte
        self.tailleTexte = tailleTexte
        self.couleurTexte = couleurTexte
        self.largeurContour = largeurContour
        self.couleurRect = couleurRect
        self.couleurCountour = couleurCountour
        self.selectionner = selectionner
        self.couleurRectSelec = couleurRectSelec
        self.couleurTexteSelec = couleurTexteSelec

    def affiche(self):
        if self.image == None:
            cRect = self.couleurRect
            cTexte = self.couleurTexte
            if self.selectionner == True:
                cRect = self.couleurRectSelec
                cTexte = self.couleurTexteSelec
            pygame.draw.rect(SCREEN, cRect, (self.x, self.y, self.largeur, self.hauteur), 0)
            pygame.draw.rect(SCREEN, self.couleurCountour, (self.x, self.y, self.largeur, self.hauteur), self.largeurContour)
            affiche_texte(self.texte, self.x + int(self.largeur / 2), self.y + int(self.hauteur / 2), self.policeTexte, self.tailleTexte, cTexte, True)
        else:
            pygame.draw.rect(SCREEN, self.couleurRect, (self.x, self.y, self.largeur, self.hauteur), 0)
            SCREEN.blit(self.image, (self.x, self.y))
            if self.selectionner:
                pygame.draw.rect(SCREEN, self.couleurCountour, (self.x, self.y, self.largeur, self.hauteur), 5)

    def clic(self, x_souris, y_souris):
        if self.x <= x_souris and x_souris <= self.x + self.largeur and self.y <= y_souris and y_souris <= self.y + self.hauteur:
            return True
        return False

# ------------------------
def affiche_ecran_principal(etat_partie):
    SCREEN.blit(IMAGE_FOND_EAU, (0, 0))
    rectangle(MARGES, MARGES, X_PLATEAU - MARGES_PLATEAU - MARGES, HAUTEUR_TITRE)
    affiche_texte('CATANE', X_CENTRE_AFFICHAGE_GAUCHE, HAUTEUR_TITRE / 2 - 3, None, 130, GRIS_FONCE, centrer=True)
    t = 'Erreur'
    if etat_partie == 'reglagesJoueurs':
        t = 'Sélection des joueurs'
    if etat_partie == 'reglagePlateau':
        t = 'Préparation du plateau'
    elif etat_partie == 'placement':
        t = 'Placement des joueurs'
    elif etat_partie == 'jeu':
        t = "C'est à vous de jouer"
    affiche_texte(t, X_CENTRE_AFFICHAGE_GAUCHE, HAUTEUR_TITRE / 2 + 50, None, 52, GRIS_FONCE, centrer=True)

    if etat_partie != 'reglagesJoueurs' and etat_partie != 'reglagePlateau':
        rectangle(MARGES, HAUTEUR_TITRE + 2 * MARGES, X_PLATEAU - MARGES_PLATEAU - MARGES, HAUTEUR_BANDEAU_ACTIONS)

# ------------------------
class Ecran_reglages():
    def __init__(self):
        self.x = MARGES
        self.y = 2 * MARGES + HAUTEUR_TITRE
        self.largeur = X_PLATEAU - MARGES - MARGES_PLATEAU
        self.hauteur = HAUTEUR - 3 * MARGES - HAUTEUR_TITRE
        self.marge_x = int((self.largeur - 2 * LARGEUR_IMAGE_GRAND_JOUEUR) / 3)
        self.marge_y = 20
        self.listeBoutonsJoueurs = []
        self.listeBoutonsJoueurs.append(Bouton(self.x + self.marge_x, self.y + self.marge_y, 'bleu', image=IMAGE_GRAND_JOUEUR, couleurRect=BLEU))
        self.listeBoutonsJoueurs.append(Bouton(self.x + self.marge_x * 2 + LARGEUR_IMAGE_GRAND_JOUEUR, self.y + self.marge_y, 'rouge', image=IMAGE_GRAND_JOUEUR, couleurRect=ROUGE))
        self.listeBoutonsJoueurs.append(Bouton(self.x + self.marge_x, self.y + self.marge_y * 2 + HAUTEUR_IMAGE_GRAND_JOUEUR, 'orange', image=IMAGE_GRAND_JOUEUR, couleurRect=ORANGE))
        self.listeBoutonsJoueurs.append(Bouton(self.x + self.marge_x * 2 + LARGEUR_IMAGE_GRAND_JOUEUR, self.y + self.marge_y * 2 + HAUTEUR_IMAGE_GRAND_JOUEUR, 'blanc', image=IMAGE_GRAND_JOUEUR, couleurRect=BLANC))
        m = 20
        h = 80
        self.boutonsValider = Bouton(X_CENTRE_AFFICHAGE_GAUCHE, HAUTEUR - MARGES - h / 2 - m, 'valider', largeur=self.largeur - 2 * m, hauteur=h, texte='Valider', tailleTexte=80, centrer=True)

        self.listeBoutonsSelectionnes = []

        self.listeBoutonsReglagePlateau = []
        self.listeBoutonsReglagePlateau.append(Bouton(X_CENTRE_AFFICHAGE_GAUCHE, HAUTEUR - MARGES - h / 2 - m, 'jouer', largeur=self.largeur - 2 * m, hauteur=h, texte='JOUER', tailleTexte=80, centrer=True))
        h2 = 80
        m2 = int((self.hauteur - 3 * h2 - h - m) / 4)
        self.listeBoutonsReglagePlateau.append(Bouton(X_CENTRE_AFFICHAGE_GAUCHE, self.y + m2 + h2 / 2, 'ressources', largeur=450, hauteur=h2, texte='Replacer les ressources', tailleTexte=55, couleurTexte=GRIS_FONCE, couleurRect=GRIS_CLAIR, couleurCountour=GRIS_CLAIR, centrer=True))
        self.listeBoutonsReglagePlateau.append(Bouton(X_CENTRE_AFFICHAGE_GAUCHE, self.y + 2 * m2 + h2 * 3 / 2, 'numeros', largeur=450, hauteur=h2, texte='Replacer les numéros', tailleTexte=55, couleurTexte=GRIS_FONCE, couleurRect=GRIS_CLAIR, couleurCountour=GRIS_CLAIR, centrer=True))
        self.listeBoutonsReglagePlateau.append(Bouton(X_CENTRE_AFFICHAGE_GAUCHE, self.y + 3 * m2 + h2 * 5 / 2, 'ports', largeur=450, hauteur=h2, texte='Replacer les ports', tailleTexte=55, couleurTexte=GRIS_FONCE, couleurRect=GRIS_CLAIR, couleurCountour=GRIS_CLAIR, centrer=True))

    def affiche(self, etat_partie):
        rectangle(self.x, self.y, self.largeur, self.hauteur)
        if etat_partie == 'reglagesJoueurs':
            listeBouton = self.listeBoutonsJoueurs[:]
            if len(self.listeBoutonsSelectionnes) >= 2:
                listeBouton.append(self.boutonsValider)
        else:
            listeBouton = self.listeBoutonsReglagePlateau
        for bouton in listeBouton:
            bouton.affiche()

    def clic_bouton(self, etat_partie, x_souris, y_souris):
        if etat_partie == 'reglagesJoueurs':
            listeBouton = self.listeBoutonsJoueurs[:]
            if len(self.listeBoutonsSelectionnes) >= 2:
                listeBouton.append(self.boutonsValider)
        else:
            listeBouton = self.listeBoutonsReglagePlateau
        for bouton in listeBouton:
            if bouton.clic(x_souris, y_souris):
                if etat_partie == 'reglagesJoueurs':
                    if bouton.selectionner == False:
                        bouton.selectionner = True
                        self.listeBoutonsSelectionnes.append(bouton)
                    else:
                        bouton.selectionner = False
                        self.listeBoutonsSelectionnes.remove(bouton)
                return bouton.parametre
        return None