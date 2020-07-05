# coding: utf-8

# ------------------------------------- IMPORTS --------------------------------------
from pip._vendor.distlib.compat import raw_input
import pygame.gfxdraw
from pygame.locals import FULLSCREEN
import math
import random
from reseauMessages import *

# ------------------------------------ CONSTANTES ------------------------------------

LARGEUR = 1360
HAUTEUR = 700

pygame.init()
f = open("FullScreen.txt", "r")
if f.read().upper() == 'OUI':
    SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR), FULLSCREEN)
else:
    SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR))

f = open("AdresseIP.txt", "r")
ADRESSE_IP = f.read()

pygame.display.set_caption("CATANE")

FPS = 100

MARGE_CLIC = 20

MARGES = 10
MARGES_PLATEAU = 50

Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL = 225
HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL = 40

HAUTEUR_TITRE = 130
HAUTEUR_BANDEAU_ACTIONS = 80

POLICE_NONE = 'Font/freesansbold.ttf'
COEF_POLICE = 1.5

IMAGE_FOND_EAU = pygame.image.load("Image/FondEau.png")

COTE_TUILE = 76
hauteur_tuile = 2 * COTE_TUILE
hauteur_triangle_tuile = COTE_TUILE / 2
largeur_tuile = math.sqrt(3) * COTE_TUILE

TAILLE_DES = 60

X_PLATEAU = int(LARGEUR - largeur_tuile * 5 - MARGES_PLATEAU)
Y_PLATEAU = int((HAUTEUR - 8 * COTE_TUILE) / 2)

X_CENTRE_AFFICHAGE_GAUCHE = int((X_PLATEAU - MARGES_PLATEAU - MARGES) / 2 + MARGES)
Y_CENTRE_BANDEAU_ACTIONS = int(MARGES * 2 + HAUTEUR_TITRE + HAUTEUR_BANDEAU_ACTIONS / 2)
X_CENTRE_BANDEAU_ACTIONS_DES = int(X_CENTRE_AFFICHAGE_GAUCHE + (HAUTEUR_BANDEAU_ACTIONS - TAILLE_DES) / 2 + TAILLE_DES)

HAUTEUR_CARRE_JOUEUR_SECONDAIRE = int((HAUTEUR - HAUTEUR_TITRE - 6 * MARGES - HAUTEUR_BANDEAU_ACTIONS) / 3)

# Voir creationPlateau pour comprendre (cf. tx et ty pour la création des tuiles):
LISTE_COORDONNEES_TUILES = [(2, 0), (4, 0), (6, 0),
                            (1, 1), (3, 1), (5, 1), (7, 1),
                            (0, 2), (2, 2), (4, 2), (6, 2), (8, 2),
                            (1, 3), (3, 3), (5, 3), (7, 3),
                            (2, 4), (4, 4), (6, 4)]
RESSOURCE_BOIS = 0
RESSOURCE_ARGILE = 1
RESSOURCE_MOUTON = 2
RESSOURCE_FOIN = 3
RESSOURCE_PIERRE = 4
RESSOURCE_DESERT = -1
LISTE_RESSOURCES = [0, 3, 0,
                    3, 1, 4, 2,
                    1, 4, -1, 3, 2,
                    2, 0, 4, 0,
                    1, 2, 3]

LISTE_NUMERO = [5, 2, 6,
                10, 9, 4, 3,
                8, 11, 5, 8,
                4, 3, 6, 10,
                11, 12, 9]

PORT_3_CONTRE_1 = -2
LISTE_ID_ARETES_PORT_ET_ANGLE_PORT = [(10, 120), (11, 60), (28, 0), (59, 0), (70, 300), (68, 240), (51, 240), (34, 180),
                                      (20, 120)]
LISTE_RESSOURCES_PORTS = [RESSOURCE_PIERRE, PORT_3_CONTRE_1, RESSOURCE_MOUTON, PORT_3_CONTRE_1, PORT_3_CONTRE_1,
                          RESSOURCE_ARGILE, RESSOURCE_BOIS, PORT_3_CONTRE_1, RESSOURCE_FOIN]

NB_COLONIE_MAX = 5
NB_VILLE_MAX = 4
NB_ROUTE_MAX = 15

PRIX_COLONIE = [RESSOURCE_BOIS, RESSOURCE_ARGILE, RESSOURCE_MOUTON, RESSOURCE_FOIN]
PRIX_ROUTE = [RESSOURCE_BOIS, RESSOURCE_ARGILE]
PRIX_VILLE = [RESSOURCE_FOIN, RESSOURCE_FOIN, RESSOURCE_PIERRE, RESSOURCE_PIERRE, RESSOURCE_PIERRE]
PRIX_CARTE_SPECIALE = [RESSOURCE_MOUTON, RESSOURCE_FOIN, RESSOURCE_PIERRE]

NB_POINT_DE_VICTOIRE = 10

POUVOIR_CHEVALIER = 10
POUVOIR_ROUTES_GRATUITES = 11
POUVOIR_POINT_VICTOIRE = 12
POUVOIR_MONOPOLE = 13
POUVOIR_RESSOURCES_GRATUITES = 14
LISTE_PIOCHE_CARTE_SPECIALE = [11, 11, 13, 13, 14, 14]
for i in range(14):
    LISTE_PIOCHE_CARTE_SPECIALE.append(10)
for i in range(5):
    LISTE_PIOCHE_CARTE_SPECIALE.append(12)

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

IMAGE_CARTE_CHEVALIER = pygame.image.load("Image/CarteChevalier.png")
IMAGE_CARTE_MONOPOLE = pygame.image.load("Image/CarteMonopole.png")
IMAGE_CARTE_POINT_VICTOIRE = pygame.image.load("Image/CartePointVictoire.png")
IMAGE_CARTE_RESSOURCES_GRATUITES = pygame.image.load("Image/CarteRessourcesGratuites.png")
IMAGE_CARTE_ROUTES_GRATUITES = pygame.image.load("Image/CarteRoutesGratuites.png")

IMAGE_COLONIE = pygame.image.load("Image/Colonie.png")
LARGEUR_IMAGE_COLONIE = IMAGE_COLONIE.get_width()
HAUTEUR_IMAGE_COLONIE = IMAGE_COLONIE.get_height()


def couleur_colonie_image(couleur, x, y):
    pygame.draw.polygon(SCREEN, couleur,
                        ((x + 3, y + 9), (x + 15, y + 1), (x + 26, y + 9), (x + 26, y + 25), (x + 3, y + 25)), 0)


IMAGE_VILLE = pygame.image.load("Image/Ville.png")
LARGEUR_IMAGE_VILLE = IMAGE_VILLE.get_width()
HAUTEUR_IMAGE_VILLE = IMAGE_VILLE.get_height()


def couleur_ville_image(couleur, x, y):
    pygame.draw.polygon(SCREEN, couleur,
                        ((x + 3, y + 9), (x + 19, y + 1), (x + 34, y + 9), (x + 34, y + 33), (x + 3, y + 33)), 0)


LARGEUR_ROUTE = 12

IMAGE_JOUEUR = pygame.image.load("Image/Joueur.png")
LARGEUR_IMAGE_JOUEUR = IMAGE_JOUEUR.get_width()
HAUTEUR_IMAGE_JOUEUR = IMAGE_JOUEUR.get_height()

IMAGE_CARTE_DOS = pygame.image.load("Image/CarteDos.png")
LARGEUR_IMAGE_CARTE_DOS = IMAGE_CARTE_DOS.get_width()
HAUTEUR_IMAGE_CARTE_DOS = IMAGE_CARTE_DOS.get_height()

IMAGE_VOLEUR = pygame.image.load("Image/Voleur.png")
IMAGE_VOLEUR_NUMERO = pygame.image.load("Image/VoleurNumero.png")
LARGEUR_IMAGE_VOLEUR = IMAGE_VOLEUR.get_width()
HAUTEUR_IMAGE_VOLEUR = IMAGE_VOLEUR.get_height()
IMAGE_PETIT_VOLEUR = pygame.image.load("Image/PetitVoleur.png")
LARGEUR_IMAGE_PETIT_VOLEUR = IMAGE_PETIT_VOLEUR.get_width()
HAUTEUR_IMAGE_PETIT_VOLEUR = IMAGE_PETIT_VOLEUR.get_height()

IMAGE_COURONNE = pygame.image.load("Image/Couronne.png")
LARGEUR_IMAGE_COURONNE = IMAGE_COURONNE.get_width()
HAUTEUR_IMAGE_COURONNE = IMAGE_COURONNE.get_height()

IMAGE_PETITE_CARTE_DOS_SPECIALE = pygame.image.load("Image/CarteDosSpeciale.png")
IMAGE_PETITE_CARTE_CHEVALIER = pygame.image.load("Image/PetiteCarteChevalier.png")
LARGEUR_IMAGE_PETITE_CARTE_SPECIALE = IMAGE_PETITE_CARTE_DOS_SPECIALE.get_width()
HAUTEUR_IMAGE_PETITE_CARTE_SPECIALE = IMAGE_PETITE_CARTE_DOS_SPECIALE.get_height()

IMAGE_PETITE_COURONNE_DOREE = pygame.image.load("Image/PetiteCouronneDoree.png")
IMAGE_PETITE_COURONNE_GRISEE = pygame.image.load("Image/PetiteCouronneGrisee.png")
LARGEUR_IMAGE_PETITE_COURONNE = IMAGE_PETITE_COURONNE_DOREE.get_width()
HAUTEUR_IMAGE_PETITE_COURONNE = IMAGE_PETITE_COURONNE_DOREE.get_height()

IMAGE_GRAND_JOUEUR = pygame.image.load("Image/GrandJoueur.png")
LARGEUR_IMAGE_GRAND_JOUEUR = IMAGE_GRAND_JOUEUR.get_width()
HAUTEUR_IMAGE_GRAND_JOUEUR = IMAGE_GRAND_JOUEUR.get_height()

IMAGE_ADRESSE_IP = pygame.image.load("Image/AdresseIP.png")
LARGEUR_IMAGE_ADRESSE_IP = IMAGE_ADRESSE_IP.get_width()
HAUTEUR_IMAGE_ADRESSE_IP = IMAGE_ADRESSE_IP.get_height()
IMAGE_ADRESSE_IP_PETITE = pygame.transform.rotozoom(IMAGE_ADRESSE_IP, 1, 0.45)
LARGEUR_IMAGE_ADRESSE_IP_PETITE = IMAGE_ADRESSE_IP_PETITE.get_width()

IMAGE_PORT_BOIS__0 = pygame.image.load("Image/PortBois.png")
IMAGE_PORT_BOIS__60 = pygame.transform.rotozoom(IMAGE_PORT_BOIS__0, 60, 1)
IMAGE_PORT_BOIS__120 = pygame.transform.rotozoom(IMAGE_PORT_BOIS__0, 120, 1)
IMAGE_PORT_BOIS__180 = pygame.transform.rotozoom(IMAGE_PORT_BOIS__0, 180, 1)
IMAGE_PORT_BOIS__240 = pygame.transform.rotozoom(IMAGE_PORT_BOIS__0, 240, 1)
IMAGE_PORT_BOIS__300 = pygame.transform.rotozoom(IMAGE_PORT_BOIS__0, 300, 1)

IMAGE_PORT_ARGILE__0 = pygame.image.load("Image/PortArgile.png")
IMAGE_PORT_ARGILE__60 = pygame.transform.rotozoom(IMAGE_PORT_ARGILE__0, 60, 1)
IMAGE_PORT_ARGILE__120 = pygame.transform.rotozoom(IMAGE_PORT_ARGILE__0, 120, 1)
IMAGE_PORT_ARGILE__180 = pygame.transform.rotozoom(IMAGE_PORT_ARGILE__0, 180, 1)
IMAGE_PORT_ARGILE__240 = pygame.transform.rotozoom(IMAGE_PORT_ARGILE__0, 240, 1)
IMAGE_PORT_ARGILE__300 = pygame.transform.rotozoom(IMAGE_PORT_ARGILE__0, 300, 1)

IMAGE_PORT_MOUTON__0 = pygame.image.load("Image/PortMouton.png")
IMAGE_PORT_MOUTON__60 = pygame.transform.rotozoom(IMAGE_PORT_MOUTON__0, 60, 1)
IMAGE_PORT_MOUTON__120 = pygame.transform.rotozoom(IMAGE_PORT_MOUTON__0, 120, 1)
IMAGE_PORT_MOUTON__180 = pygame.transform.rotozoom(IMAGE_PORT_MOUTON__0, 180, 1)
IMAGE_PORT_MOUTON__240 = pygame.transform.rotozoom(IMAGE_PORT_MOUTON__0, 240, 1)
IMAGE_PORT_MOUTON__300 = pygame.transform.rotozoom(IMAGE_PORT_MOUTON__0, 300, 1)

IMAGE_PORT_FOIN__0 = pygame.image.load("Image/PortFoin.png")
IMAGE_PORT_FOIN__60 = pygame.transform.rotozoom(IMAGE_PORT_FOIN__0, 60, 1)
IMAGE_PORT_FOIN__120 = pygame.transform.rotozoom(IMAGE_PORT_FOIN__0, 120, 1)
IMAGE_PORT_FOIN__180 = pygame.transform.rotozoom(IMAGE_PORT_FOIN__0, 180, 1)
IMAGE_PORT_FOIN__240 = pygame.transform.rotozoom(IMAGE_PORT_FOIN__0, 240, 1)
IMAGE_PORT_FOIN__300 = pygame.transform.rotozoom(IMAGE_PORT_FOIN__0, 300, 1)

IMAGE_PORT_PIERRE__0 = pygame.image.load("Image/PortPierre.png")
IMAGE_PORT_PIERRE__60 = pygame.transform.rotozoom(IMAGE_PORT_PIERRE__0, 60, 1)
IMAGE_PORT_PIERRE__120 = pygame.transform.rotozoom(IMAGE_PORT_PIERRE__0, 120, 1)
IMAGE_PORT_PIERRE__180 = pygame.transform.rotozoom(IMAGE_PORT_PIERRE__0, 180, 1)
IMAGE_PORT_PIERRE__240 = pygame.transform.rotozoom(IMAGE_PORT_PIERRE__0, 240, 1)
IMAGE_PORT_PIERRE__300 = pygame.transform.rotozoom(IMAGE_PORT_PIERRE__0, 300, 1)

IMAGE_PORT_3_CONTRE_1__0 = pygame.image.load("Image/Port3contre1.png")
IMAGE_PORT_3_CONTRE_1__60 = pygame.transform.rotozoom(IMAGE_PORT_3_CONTRE_1__0, 60, 1)
IMAGE_PORT_3_CONTRE_1__120 = pygame.transform.rotozoom(IMAGE_PORT_3_CONTRE_1__0, 120, 1)
IMAGE_PORT_3_CONTRE_1__180 = pygame.transform.rotozoom(IMAGE_PORT_3_CONTRE_1__0, 180, 1)
IMAGE_PORT_3_CONTRE_1__240 = pygame.transform.rotozoom(IMAGE_PORT_3_CONTRE_1__0, 240, 1)
IMAGE_PORT_3_CONTRE_1__300 = pygame.transform.rotozoom(IMAGE_PORT_3_CONTRE_1__0, 300, 1)

LARGEUR_IMAGE_PORT__0 = IMAGE_PORT_3_CONTRE_1__0.get_width()
LARGEUR_IMAGE_PORT__60 = IMAGE_PORT_3_CONTRE_1__60.get_width()
LARGEUR_IMAGE_PORT__120 = IMAGE_PORT_3_CONTRE_1__120.get_width()
LARGEUR_IMAGE_PORT__180 = IMAGE_PORT_3_CONTRE_1__180.get_width()
LARGEUR_IMAGE_PORT__240 = IMAGE_PORT_3_CONTRE_1__240.get_width()
LARGEUR_IMAGE_PORT__300 = IMAGE_PORT_3_CONTRE_1__300.get_width()

HAUTEUR_IMAGE_PORT__0 = IMAGE_PORT_3_CONTRE_1__0.get_height()
HAUTEUR_IMAGE_PORT__60 = IMAGE_PORT_3_CONTRE_1__60.get_height()
HAUTEUR_IMAGE_PORT__120 = IMAGE_PORT_3_CONTRE_1__120.get_height()
HAUTEUR_IMAGE_PORT__180 = IMAGE_PORT_3_CONTRE_1__180.get_height()
HAUTEUR_IMAGE_PORT__240 = IMAGE_PORT_3_CONTRE_1__240.get_height()
HAUTEUR_IMAGE_PORT__300 = IMAGE_PORT_3_CONTRE_1__300.get_height()

IMAGE_GRANDE_COURONNE = pygame.image.load("Image/GrandeCouronne.png")
LARGEUR_IMAGE_GRANDE_COURONNE = IMAGE_GRANDE_COURONNE.get_width()
HAUTEUR_IMAGE_GRANDE_COURONNE = IMAGE_GRANDE_COURONNE.get_height()

IMAGE_TRANSPARANTE = pygame.Surface((LARGEUR, HAUTEUR))
IMAGE_TRANSPARANTE.set_alpha(200)
IMAGE_TRANSPARANTE.fill((255, 255, 255))

IMAGE_BOUTON_MESSAGES = pygame.image.load("Image/MessageBouton.png")
LARGEUR_IMAGE_BOUTON_MESSAGES = IMAGE_BOUTON_MESSAGES.get_width()
HAUTEUR_IMAGE_BOUTON_MESSAGES = IMAGE_BOUTON_MESSAGES.get_height()
IMAGE_BOUTON_SAUVEGARDE = pygame.image.load("Image/SauvegardeBouton.png")
IMAGE_BOUTON_STATS = pygame.image.load("Image/StatsBouton.png")
IMAGE_BOUTON_QUITTER = pygame.image.load("Image/QuitterBouton.png")

# Couleurs :
NOIR = [0, 0, 0]
GRIS_FONCE = [50, 50, 50]
GRIS_MOYEN = [90, 90, 90]
GRIS_CLAIR = [190, 190, 190]
BLANC = [255, 255, 255]
BLEU = [0, 0, 255]
# VERT = [52, 175, 0]
ROUGE = [255, 0, 0]
ORANGE = [255, 127, 0]


# JAUNE = [255, 255, 0]

# -------------------------------- FONCTIONS ET CLASS --------------------------------
def rectangle(x, y, largeur, hauteur):
    pygame.draw.rect(SCREEN, BLANC, (x, y, largeur, hauteur), 0)
    pygame.draw.rect(SCREEN, NOIR, (x, y, largeur, hauteur), 3)


# ------------------------
def affiche_texte(texte, x, y, font, taille, couleur, centrer=False):
    if font is None:
        font = POLICE_NONE
    police = pygame.font.Font(font, int(taille / COEF_POLICE))
    surface = police.render(texte, True, couleur)
    rect = surface.get_rect(topleft=(x, y))
    if centrer == True:
        rect = surface.get_rect(center=(x, y))
    SCREEN.blit(surface, rect)


# ------------------------
def affiche_point(x, y, r, c):
    pygame.gfxdraw.aacircle(SCREEN, int(x), int(y), r, c)
    pygame.gfxdraw.filled_circle(SCREEN, int(x), int(y), r, c)


# ------------------------
def affiche_de(x, y, taille, rayonPoints, margePoints, nombre, couleurFont=GRIS_CLAIR, couleurPoints=GRIS_FONCE):
    pygame.draw.rect(SCREEN, couleurFont, (x, y, taille, taille), 0)
    if nombre == 1 or nombre == 3 or nombre == 5:
        affiche_point(x + taille / 2, y + taille / 2, rayonPoints, couleurPoints)
    if nombre > 1:
        affiche_point(x + taille - margePoints, y + margePoints, rayonPoints, couleurPoints)
        affiche_point(x + margePoints, y + taille - margePoints, rayonPoints, couleurPoints)
    if nombre >= 4:
        affiche_point(x + margePoints, y + margePoints, rayonPoints, couleurPoints)
        affiche_point(x + taille - margePoints, y + taille - margePoints, rayonPoints, couleurPoints)
    if nombre == 6:
        affiche_point(x + margePoints, y + taille / 2, rayonPoints, couleurPoints)
        affiche_point(x + taille - margePoints, y + taille / 2, rayonPoints, couleurPoints)


# ------------------------
def affiche_bulle(x, y, r, n):
    affiche_point(x, y, r + 3, NOIR)
    affiche_point(x, y, r, BLANC)
    affiche_texte(str(n), x, y + 2, None, 30, NOIR, centrer=True)


# ------------------------
def affiche_numero(x, y, numero):
    x = int(x)
    y = int(y)
    rayon_numero = 20
    pygame.draw.circle(SCREEN, BLANC, (x, y), rayon_numero, 0)
    pygame.gfxdraw.aacircle(SCREEN, x, y, rayon_numero, NOIR)
    pygame.gfxdraw.aacircle(SCREEN, x, y, rayon_numero-2, NOIR)
    c = NOIR
    t = 35
    if numero == 6 or numero == 8:
        c = ROUGE
        t += 10
    elif numero == 5 or numero == 9:
        t += 10
    elif numero == 11 or numero == 3:
        t -= 5
    elif numero == 12 or numero == 2:
        t -= 10

    affiche_texte(str(numero), x, int(y + 2), None, t, c, centrer=True)


# ------------------------
def affiche_route(x1, y1, x2, y2, couleur):
    pygame.draw.line(SCREEN, NOIR, (x1, y1), (x2, y2), LARGEUR_ROUTE + 2 - 1)
    pygame.gfxdraw.filled_circle(SCREEN, x1, y1, int(LARGEUR_ROUTE / 2), NOIR)
    pygame.gfxdraw.filled_circle(SCREEN, x2, y2, int(LARGEUR_ROUTE / 2), NOIR)
    pygame.draw.line(SCREEN, couleur, (x1, y1), (x2, y2), LARGEUR_ROUTE - 2 - 1)
    pygame.gfxdraw.filled_circle(SCREEN, x1, y1, int(LARGEUR_ROUTE / 2) - 2, couleur)
    pygame.gfxdraw.filled_circle(SCREEN, x2, y2, int(LARGEUR_ROUTE / 2) - 2, couleur)


# ------------------------
class CaseACocher():
    def __init__(self, x, y, parametre, texte, taille=30, policeTexte=None, tailleTexte=30, couleurTexte=GRIS_FONCE,
                 etat_initial=False, largeurTrai=1, couleurCase=GRIS_FONCE, couleurSelect=GRIS_MOYEN):
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
        affiche_texte(self.texte, self.x + int(self.taille * 1.3), self.y + self.taille / 2 - self.tailleTexte / 4,
                      self.policeTexte, self.tailleTexte, self.couleurTexte)

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
    def __init__(self, x, y, parametre, largeur=0, hauteur=0, texte=None, image=None, policeTexte=None, tailleTexte=30,
                 couleurTexte=GRIS_CLAIR, largeurContour=3, couleurRect=NOIR, couleurCountour=NOIR, selectionner=False,
                 couleurTexteSelec=NOIR, couleurRectSelec=GRIS_CLAIR, centrer=False):
        self.x = x
        self.y = y
        self.image = image
        if self.image is not None:
            self.largeur = self.image.get_width()
            self.hauteur = self.image.get_height()
        else:
            self.largeur = largeur
            self.hauteur = hauteur
        if centrer:
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
            pygame.draw.rect(SCREEN, self.couleurCountour, (self.x, self.y, self.largeur, self.hauteur),
                             self.largeurContour)
            affiche_texte(self.texte, self.x + int(self.largeur / 2), self.y + int(self.hauteur / 2), self.policeTexte,
                          self.tailleTexte, cTexte, True)
        else:
            pygame.draw.rect(SCREEN, self.couleurRect, (self.x, self.y, self.largeur, self.hauteur), 0)
            SCREEN.blit(self.image, (self.x, self.y))
            if self.selectionner or self.image == IMAGE_BOUTON_MESSAGES or self.image == IMAGE_BOUTON_SAUVEGARDE or\
                    self.image == IMAGE_BOUTON_STATS or self.image == IMAGE_BOUTON_QUITTER:
                pygame.draw.rect(SCREEN, self.couleurCountour, (self.x, self.y, self.largeur, self.hauteur),
                                 self.largeurContour)

    def clic(self, x_souris, y_souris):
        if self.x <= x_souris <= self.x + self.largeur and self.y <= y_souris <= self.y + self.hauteur:
            return True
        return False


# ------------------------
def affiche_ecran_principal(etat_partie):
    SCREEN.blit(IMAGE_FOND_EAU, (0, 0))
    rectangle(MARGES, MARGES, X_PLATEAU - MARGES_PLATEAU - MARGES, HAUTEUR_TITRE)
    affiche_texte('CATANE', X_CENTRE_AFFICHAGE_GAUCHE, HAUTEUR_TITRE / 2 - 3, None, 130, GRIS_FONCE, centrer=True)
    t = 'FIN !'
    if etat_partie == 'reglagesJoueurs':
        t = 'Sélection des joueurs'
    if etat_partie == 'reglagePlateau':
        t = 'Préparation du plateau'
    elif etat_partie == 'attenteJoueurs':
        t = "En attente d'autres joueurs"
    elif etat_partie == 'placement':
        t = 'Placement'
    elif etat_partie == 'jeu':
        t = "Jeu"
    elif etat_partie == 'fin':
        t = "Fin"
    affiche_texte(t, X_CENTRE_AFFICHAGE_GAUCHE, HAUTEUR_TITRE / 2 + 50, None, 52, GRIS_FONCE, centrer=True)

    if etat_partie != 'reglagesJoueurs' and etat_partie != 'reglagePlateau' and etat_partie != 'attenteJoueurs':
        rectangle(MARGES, HAUTEUR_TITRE + 2 * MARGES, X_PLATEAU - MARGES_PLATEAU - MARGES, HAUTEUR_BANDEAU_ACTIONS)


# -----------------------
class Ecran_login():
    def __init__(self):
        self.actif = True
        self.l = 350
        self.h = 50
        self.x = int((LARGEUR - self.l) / 2)
        self.y = int((HAUTEUR - self.h) / 2 + 100)
        self.m = 5
        self.msg = ''
        SCREEN.blit(IMAGE_VOLEUR, (20, 20))
        self.p = pygame.font.Font(POLICE_NONE, int((self.h * 2 - 7 * self.m) / COEF_POLICE))
        self.ts = self.p.render(self.msg, True, NOIR)
        self.b = Bouton(self.x, self.y + self.h + 15, '', self.l, self.h, texte='Valider', tailleTexte=50)
        self.etape = 0
        self.reessayer = False

    def clic(self, x_souris, y_souris):
        if self.x < x_souris < self.x + self.l and self.y < y_souris < self.y + self.h:
            self.actif = True
        else:
            if self.b.clic(x_souris, y_souris):
                if self.msg != '':
                    return self.msg
            self.actif = False
        return None

    def gere_clavier(self, event):
        if self.actif:
            if event.key == pygame.K_RETURN or event.key == 271:
                if self.msg != '':
                    return self.msg
            elif event.key == pygame.K_BACKSPACE:
                self.msg = self.msg[:-1]
            else:
                self.msg += event.unicode
            self.ts = self.p.render(self.msg, True, NOIR)
        return None

    def affiche(self):
        SCREEN.blit(IMAGE_FOND_EAU, (0, 0))
        rectangle(MARGES, MARGES, LARGEUR - 2 * MARGES, HAUTEUR_TITRE)
        affiche_texte('CATANE', LARGEUR / 2 - MARGES, HAUTEUR_TITRE / 2 - 3, None, 130, GRIS_FONCE, centrer=True)
        t = "Rentrez votre pseudo"
        if self.etape == 1:
            t = "Rentrez l'adresse IP du serveur"
        affiche_texte(t, LARGEUR / 2 - MARGES, HAUTEUR_TITRE / 2 + 50, None, 52, GRIS_FONCE, centrer=True)
        rectangle(MARGES, 2 * MARGES + HAUTEUR_TITRE, LARGEUR - 2 * MARGES, HAUTEUR - 3 * MARGES - HAUTEUR_TITRE)
        c = GRIS_CLAIR
        if self.actif:
            c = GRIS_FONCE
        pygame.draw.rect(SCREEN, c, (self.x, self.y, self.l, self.h), 3)
        SCREEN.blit(self.ts, (int(self.x + self.l / 2 - self.ts.get_width() / 2), self.y + self.m))
        self.b.affiche()
        if self.etape == 0:
            SCREEN.blit(IMAGE_GRAND_JOUEUR,
                        (int((LARGEUR - LARGEUR_IMAGE_GRAND_JOUEUR) / 2), self.y - HAUTEUR_IMAGE_GRAND_JOUEUR - 15 + 9))
        else:
            if self.reessayer:
                affiche_texte("La connection avec le serveur", LARGEUR / 2, self.y - 85, None, 34, ROUGE, centrer=True)
                affiche_texte("n'a pas pu être effectuée.", LARGEUR / 2, self.y - 56, None, 34, ROUGE, centrer=True)
                affiche_texte("Veuillez réessayer :", LARGEUR / 2, self.y - 23, None, 34, ROUGE, centrer=True)
                SCREEN.blit(IMAGE_ADRESSE_IP_PETITE, (
                int((LARGEUR - LARGEUR_IMAGE_ADRESSE_IP_PETITE) / 2), self.y - HAUTEUR_IMAGE_ADRESSE_IP - 15 + 9))
            else:
                SCREEN.blit(IMAGE_ADRESSE_IP,
                            (int((LARGEUR - LARGEUR_IMAGE_ADRESSE_IP) / 2), self.y - HAUTEUR_IMAGE_ADRESSE_IP - 15 + 9))


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
        self.listeBoutonsJoueurs.append(
            Bouton(self.x + self.marge_x, self.y + self.marge_y, 'bleu', image=IMAGE_GRAND_JOUEUR, couleurRect=BLEU,
                   largeurContour=5))
        self.listeBoutonsJoueurs.append(
            Bouton(self.x + self.marge_x * 2 + LARGEUR_IMAGE_GRAND_JOUEUR, self.y + self.marge_y, 'rouge',
                   image=IMAGE_GRAND_JOUEUR, couleurRect=ROUGE, largeurContour=5))
        self.listeBoutonsJoueurs.append(
            Bouton(self.x + self.marge_x, self.y + self.marge_y * 2 + HAUTEUR_IMAGE_GRAND_JOUEUR, 'orange',
                   image=IMAGE_GRAND_JOUEUR, couleurRect=ORANGE, largeurContour=5))
        self.listeBoutonsJoueurs.append(Bouton(self.x + self.marge_x * 2 + LARGEUR_IMAGE_GRAND_JOUEUR,
                                               self.y + self.marge_y * 2 + HAUTEUR_IMAGE_GRAND_JOUEUR, 'blanc',
                                               image=IMAGE_GRAND_JOUEUR, couleurRect=BLANC, largeurContour=5))
        m = 20
        h = 80
        self.boutonsValider = Bouton(X_CENTRE_AFFICHAGE_GAUCHE, HAUTEUR - MARGES - h / 2 - m, 'valider',
                                     largeur=self.largeur - 2 * m, hauteur=h, texte='Valider', tailleTexte=80,
                                     centrer=True)

        self.listeBoutonsSelectionnes = []

        self.listeBoutonsReglagePlateau = []
        self.listeBoutonsReglagePlateau.append(
            Bouton(X_CENTRE_AFFICHAGE_GAUCHE, HAUTEUR - MARGES - h / 2 - m, 'jouer', largeur=self.largeur - 2 * m,
                   hauteur=h, texte='JOUER', tailleTexte=80, centrer=True))
        h2 = 80
        m2 = int((self.hauteur - self.x - 3 * h2 - h - 2 * m) / 4)
        l = 450
        self.listeBoutonsReglagePlateau.append(
            Bouton(X_CENTRE_AFFICHAGE_GAUCHE, int(self.y + m2 / 4 + h2 / 2), 'ressources', largeur=l, hauteur=h2,
                   texte='Replacer les ressources', tailleTexte=55, couleurTexte=GRIS_FONCE, couleurRect=GRIS_CLAIR,
                   couleurCountour=GRIS_CLAIR, centrer=True))
        self.listeBoutonsReglagePlateau.append(
            Bouton(X_CENTRE_AFFICHAGE_GAUCHE, int(self.y + 7 * m2 / 4 + h2 * 3 / 2), 'numeros', largeur=l, hauteur=h2,
                   texte='Replacer les numéros', tailleTexte=55, couleurTexte=GRIS_FONCE, couleurRect=GRIS_CLAIR,
                   couleurCountour=GRIS_CLAIR, centrer=True))
        self.listeBoutonsReglagePlateau.append(
            Bouton(X_CENTRE_AFFICHAGE_GAUCHE, int(self.y + 13 * m2 / 4 + h2 * 5 / 2), 'ports', largeur=l, hauteur=h2,
                   texte='Replacer les ports', tailleTexte=55, couleurTexte=GRIS_FONCE, couleurRect=GRIS_CLAIR,
                   couleurCountour=GRIS_CLAIR, centrer=True))

        self.listeCasesACaucherReglagePlateau = []
        m3 = 5
        self.listeCasesACaucherReglagePlateau.append(
            CaseACocher(X_CENTRE_AFFICHAGE_GAUCHE - l / 2 + m3, int(self.y + m2 / 4 + h2 + m3), 'ressources',
                        'Replacer manuellement les ressources'))
        self.listeCasesACaucherReglagePlateau.append(
            CaseACocher(X_CENTRE_AFFICHAGE_GAUCHE - l / 2 + m3, int(self.y + 7 * m2 / 4 + h2 * 2 + m3), 'numeros',
                        'Replacer manuellement les numéros'))
        self.listeCasesACaucherReglagePlateau.append(
            CaseACocher(X_CENTRE_AFFICHAGE_GAUCHE - l / 2 + m3, int(self.y + 13 * m2 / 4 + h2 * 3 + m3), 'ports',
                        'Replacer manuellement les ports'))

        self.tuile_clic = None
        self.port_clic = None

    def affiche(self, etat_partie):
        rectangle(self.x, self.y, self.largeur, self.hauteur)
        if etat_partie == 'reglagesJoueurs':
            listeBouton = self.listeBoutonsJoueurs[:]
            if len(self.listeBoutonsSelectionnes) >= 2:
                listeBouton.append(self.boutonsValider)
        else:
            listeBouton = self.listeBoutonsReglagePlateau + self.listeCasesACaucherReglagePlateau
        for bouton in listeBouton:
            bouton.affiche()

    def clic_bouton(self, etat_partie, x_souris, y_souris):
        if etat_partie == 'reglagesJoueurs':
            listeBouton = self.listeBoutonsJoueurs[:]
            if len(self.listeBoutonsSelectionnes) >= 2:
                listeBouton.append(self.boutonsValider)
        else:
            listeBouton = self.listeBoutonsReglagePlateau
            for case in self.listeCasesACaucherReglagePlateau:
                if case.clic(x_souris, y_souris):
                    self.tuile_clic = None
                    self.port_clic = None
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

    def clic_plateau(self, tuile, arete):
        for case in self.listeCasesACaucherReglagePlateau:
            if case.etat == 1:
                if case.parametre == 'ports':
                    if arete == None or arete.ressource_port == None:
                        self.port_clic = None
                    else:
                        if self.port_clic == None:
                            self.port_clic = arete
                        else:
                            arete2 = self.port_clic
                            self.port_clic = None
                            return arete, arete2
                        return None, None

        for case in self.listeCasesACaucherReglagePlateau:
            if case.etat == 1:
                if case.parametre != 'ports':
                    if tuile == None or tuile.ressource == RESSOURCE_DESERT:
                        self.tuile_clic = None
                    else:
                        if self.tuile_clic == None:
                            self.tuile_clic = tuile
                        else:
                            tuile2 = self.tuile_clic
                            self.tuile_clic = None
                            return tuile, tuile2
                    return None, None

        return None, None


# -----------------------
class Fenetre_banque():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.marge = 5
        self.largeur = 5 * LARGEUR_IMAGE_CARTE_DOS + 6 * self.marge
        self.hauteur = HAUTEUR_IMAGE_CARTE_DOS + 2 * self.marge
        self.largeur_fleche = 10
        self.hauteur_fleche = 16
        self.largeur_trait_fleche = 5
        self.x_affichage = self.x + self.largeur_fleche
        self.y_affichage = self.y - self.hauteur / 2
        self.ressources_cartes = [RESSOURCE_BOIS, RESSOURCE_ARGILE, RESSOURCE_MOUTON, RESSOURCE_FOIN, RESSOURCE_PIERRE]

    def affiche(self):
        pygame.draw.polygon(SCREEN, NOIR, (
        (self.x, self.y), (self.x + self.largeur_fleche, self.y - self.hauteur_fleche / 2),
        (self.x + self.largeur_fleche, self.y + self.hauteur_fleche / 2)), 0)
        rectangle(self.x_affichage, self.y_affichage, self.largeur, self.hauteur)
        pygame.draw.polygon(SCREEN, BLANC, ((self.x + self.largeur_trait_fleche, self.y), (
        self.x + self.largeur_fleche + self.largeur_trait_fleche, self.y - self.hauteur_fleche / 2), (
                                            self.x + self.largeur_fleche + self.largeur_trait_fleche,
                                            self.y + self.hauteur_fleche / 2)), 0)

        listeImageCarteAAfficher = []
        for ressource in self.ressources_cartes:
            image = IMAGE_CARTE_BOIS
            if ressource == RESSOURCE_ARGILE:
                image = IMAGE_CARTE_ARGILE
            elif ressource == RESSOURCE_MOUTON:
                image = IMAGE_CARTE_MOUTON
            elif ressource == RESSOURCE_FOIN:
                image = IMAGE_CARTE_FOIN
            elif ressource == RESSOURCE_PIERRE:
                image = IMAGE_CARTE_PIERRE
            listeImageCarteAAfficher.append(image)

        for i in range(5):
            SCREEN.blit(listeImageCarteAAfficher[i], (
            self.x_affichage + self.marge + i * (LARGEUR_IMAGE_CARTE_DOS + self.marge), self.y_affichage + self.marge))

    def clicSurCarte(self, x_souris, y_souris):
        y = self.y_affichage + self.marge
        if y <= y_souris <= y + HAUTEUR_IMAGE_CARTE_DOS:
            for i in range(5):
                x = self.x_affichage + self.marge + i * (LARGEUR_IMAGE_CARTE_DOS + self.marge)
                if x <= x_souris <= x + LARGEUR_IMAGE_CARTE_DOS:
                    return self.ressources_cartes[i]
        return None


# -----------------------
class Fenetre_echanges():
    def __init__(self, x, y, joueur, listeJoueurs):
        self.x = x
        self.y = y
        marge = 5
        self.hauteur = 6 * marge + 5 * HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL
        self.largeur_fleche = 10
        self.hauteur_fleche = 16
        self.largeur_trait_fleche = 5
        self.x_affichage = self.x + self.largeur_fleche
        self.y_affichage = self.y - self.hauteur / 2
        self.largeur = int((LARGEUR - self.x_affichage - MARGES) / 2) * 2
        self.principal = False
        self.etape = 0

        self.boutonValider = Bouton(self.x_affichage + marge,
                                    self.y + self.hauteur / 2 - marge - HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL,
                                    'valider', largeur=int((self.largeur - 2 * marge - marge) / 2),
                                    hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='VALIDER',
                                    couleurTexte=GRIS_FONCE, couleurRect=GRIS_CLAIR, couleurCountour=GRIS_CLAIR)
        self.boutonRefuser = Bouton(self.x_affichage + 2 * marge + int((self.largeur - 2 * marge - marge) / 2),
                                    self.y + self.hauteur / 2 - marge - HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL,
                                    'refuser', largeur=int((self.largeur - 2 * marge - marge) / 2),
                                    hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='REFUSER',
                                    couleurTexte=GRIS_FONCE, couleurRect=GRIS_CLAIR, couleurCountour=GRIS_CLAIR)

        self.listeBoutonJoueurs = []
        nb_bouton = len(listeJoueurs) - 1
        x_bouton = self.x + self.largeur / 2 - 75
        y_bouton = int(self.y - (nb_bouton * HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL) / 2 - (nb_bouton - 1) * marge)
        for j in listeJoueurs:
            if j != joueur:
                self.listeBoutonJoueurs.append(
                    Bouton(x_bouton, y_bouton, j.nom, largeur=150, hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL,
                           texte=j.pseudo))
                y_bouton += HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL + marge

    def reinitialise(self, principal):
        for bouton in self.listeBoutonJoueurs:
            bouton.selectionner = False
        self.etape = 0
        self.principal = principal

    def affiche(self, joueur, joueurEchange):
        pygame.draw.polygon(SCREEN, NOIR, (
        (self.x, self.y), (self.x + self.largeur_fleche, self.y - self.hauteur_fleche / 2),
        (self.x + self.largeur_fleche, self.y + self.hauteur_fleche / 2)), 0)
        rectangle(self.x_affichage, self.y_affichage, self.largeur, self.hauteur)
        pygame.draw.polygon(SCREEN, BLANC, ((self.x + self.largeur_trait_fleche, self.y), (
        self.x + self.largeur_fleche + self.largeur_trait_fleche, self.y - self.hauteur_fleche / 2), (
                                            self.x + self.largeur_fleche + self.largeur_trait_fleche,
                                            self.y + self.hauteur_fleche / 2)), 0)

        affiche_texte('Echanger', self.x + self.largeur / 2, self.y_affichage + 25, None, 40, NOIR, centrer=True)

        if self.principal == True:
            joueur.afficheCartes(self.x + 120, self.y + 210, joueur.cree_listeCartesSelectionnees(), 40)
            affiche_texte('avec', self.x + 250, self.y, None, 30, NOIR, centrer=True)
            for bouton in self.listeBoutonJoueurs:
                bouton.affiche()
            if self.etape >= 1:
                affiche_texte('contre', self.x + self.largeur - 250, self.y, None, 30, NOIR, centrer=True)
                if self.etape >= 2:
                    joueur.afficheCartes(self.x + self.largeur - 110, self.y + 210,
                                         joueurEchange.cree_listeCartesSelectionnees(), 40)
                    self.boutonValider.affiche()
                    self.boutonRefuser.affiche()
        else:
            joueur.afficheCartes(self.x + 120, self.y + 210, joueur.cree_listeCartesSelectionnees(), 40)
            affiche_texte(f'avec {joueur.pseudo} contre', self.x + self.largeur / 2, self.y, None, 30, NOIR,
                          centrer=True)
            joueur.afficheCartes(self.x + self.largeur - 110, self.y + 210,
                                 joueurEchange.cree_listeCartesSelectionnees(), 40)
            self.boutonValider.affiche()
            self.boutonRefuser.affiche()

    def clic(self, x_souris, y_souris):
        if self.principal == True:
            if self.etape == 0:
                for bouton in self.listeBoutonJoueurs:
                    if bouton.clic(x_souris, y_souris):
                        bouton.selectionner = True
                        self.etape = 1
                        return bouton.parametre
            elif self.etape == 2:
                if self.boutonValider.clic(x_souris, y_souris):
                    return self.boutonValider.parametre
                elif self.boutonRefuser.clic(x_souris, y_souris):
                    return self.boutonRefuser.parametre
        else:
            if self.boutonValider.clic(x_souris, y_souris):
                return self.boutonValider.parametre
            elif self.boutonRefuser.clic(x_souris, y_souris):
                return self.boutonRefuser.parametre
