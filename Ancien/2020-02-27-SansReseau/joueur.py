# coding: utf-8

from outils import *

class Joueur():
    def __init__(self, couleur):
        self.couleur = couleur
        self.listeColonies = []
        self.listeVilles = []
        self.listeRoutes = []
        self.listeCartes = []
        self.dictionnaireCartesRessources = {}
        self.dictionnaireCartesRessources[RESSOURCE_BOIS] = []
        self.dictionnaireCartesRessources[RESSOURCE_ARGILE] = []
        self.dictionnaireCartesRessources[RESSOURCE_MOUTON] = []
        self.dictionnaireCartesRessources[RESSOURCE_FOIN] = []
        self.dictionnaireCartesRessources[RESSOURCE_PIERRE] = []
        self.listeCartesSpeciales = []
        # TODO : Cartes spéciales
        self.nbPointsDeVictoire = 0
        # TODO : Route la plus longue
        self.xSecondaire = MARGES
        self.ySecondaire = 0

        self.nom = 'blancs'
        if self.couleur == ROUGE:
            self.nom = 'rouges'
        elif self.couleur == ORANGE:
            self.nom = 'oranges'
        elif self.couleur == BLEU:
            self.nom = 'bleus'

    # ----------------------------------------------------
    def compte_nb_cartes(self):
        nb = 0
        for cle in self.dictionnaireCartesRessources.keys():
            nb += len(self.dictionnaireCartesRessources[cle])
        return nb

    # ----------------------------------------------------
    def cree_listeCartes(self):
        liste_cartes = []
        for cle in self.dictionnaireCartesRessources.keys():
            liste_cartes.extend(self.dictionnaireCartesRessources[cle])
        return liste_cartes

    # ----------------------------------------------------
    def compte_nb_cartes_selectionnees(self):
        nb = 0
        for cle in self.dictionnaireCartesRessources.keys():
            for carte in self.dictionnaireCartesRessources[cle]:
                if carte.selectionner == True:
                    nb += 1
        return nb

    # ----------------------------------------------------
    def cree_listeRessourcesCartesSelectionnees(self):
        l = []
        for cle in self.dictionnaireCartesRessources.keys():
            for carte in self.dictionnaireCartesRessources[cle]:
                if carte.selectionner:
                    l.append(carte.ressource)
        return l

    # ----------------------------------------------------
    def carte_au_hasard(self):
        liste_cartes = self.cree_listeCartes()
        if len(liste_cartes) != 0:
            random.shuffle(liste_cartes)
            return liste_cartes[0]
        return None

    # ----------------------------------------------------
    def deselection_cartes(self):
        for cle in self.dictionnaireCartesRessources.keys():
            for carte in self.dictionnaireCartesRessources[cle]:
                carte.selectionner = False

    # ----------------------------------------------------
    def cree_listeCartesSelectionnees(self):
        l = []
        for cle in self.dictionnaireCartesRessources.keys():
            for carte in self.dictionnaireCartesRessources[cle]:
                if carte.selectionner:
                    l.append(carte)
        return l

    # ----------------------------------------------------
    def suprimeCartesSelectionnes(self):
        for carte in self.cree_listeCartesSelectionnees():
            self.dictionnaireCartesRessources[carte.ressource].remove(carte)

    # ----------------------------------------------------
    def rendCarteConstruction(self, prix):
        for ressource in prix:
            self.dictionnaireCartesRessources[ressource].append(Carte(self, ressource))

    # ----------------------------------------------------
    def affichePions(self):
        for route in self.listeRoutes:
            route.affiche()
        for colonie in self.listeColonies:
            colonie.affiche()
        for ville in self.listeVilles:
            ville.affiche()

    # ----------------------------------------------------
    def afficheCartes(self, x, y):
        angle_min = 10
        angle_total = 90
        r = 200

        liste_cartes = self.cree_listeCartes()
        nb_cartes = len(liste_cartes)

        angle_entre_cartes = angle_min
        if nb_cartes > angle_total / angle_min:
            angle_entre_cartes = angle_total / nb_cartes

        for i in range(nb_cartes):
            a = (((nb_cartes - i - 1) + 0.5 - nb_cartes / 2)*angle_entre_cartes)
            liste_cartes[i].affiche(x, y, a, r)

    # ----------------------------------------------------
    def affichePointsDeVictoire(self, x, y):
        m = 5
        n = 0
        x -= (LARGEUR_IMAGE_PETITE_COURONNE + m) * NB_POINT_DE_VICTOIRE / 2
        y += m
        for j in range(2):
            for i in range(int(NB_POINT_DE_VICTOIRE / 2)):
                n += 1
                img = IMAGE_PETITE_COURONNE_GRISEE
                if n <= self.nbPointsDeVictoire:
                    img = IMAGE_PETITE_COURONNE_DOREE
                SCREEN.blit(img, (x + (LARGEUR_IMAGE_PETITE_COURONNE + m) * i, y + (HAUTEUR_IMAGE_PETITE_COURONNE + m) * j))

    # ----------------------------------------------------
    def afficheSecondaire(self):
        rectangle(self.xSecondaire, self.ySecondaire, HAUTEUR_CARRE_JOUEUR_SECONDAIRE, HAUTEUR_CARRE_JOUEUR_SECONDAIRE)
        m = 3
        pygame.draw.rect(SCREEN, self.couleur, (self.xSecondaire + m, self.ySecondaire + m, LARGEUR_IMAGE_JOUEUR, HAUTEUR_IMAGE_JOUEUR), 0)
        SCREEN.blit(IMAGE_JOUEUR, (self.xSecondaire + m, self.ySecondaire + m))
        c = self.couleur
        if c == BLANC:
            c = NOIR
        affiche_texte(self.nom.upper(), int(self.xSecondaire + m + LARGEUR_IMAGE_JOUEUR + (HAUTEUR_CARRE_JOUEUR_SECONDAIRE - m - LARGEUR_IMAGE_JOUEUR) / 2), int(self.ySecondaire + HAUTEUR_IMAGE_JOUEUR / 2 + m), None, 28, c, centrer=True)
        SCREEN.blit(IMAGE_CARTE_DOS, (self.xSecondaire + m, self.ySecondaire + m + HAUTEUR_IMAGE_JOUEUR))
        affiche_texte(str(self.compte_nb_cartes()), int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS / 2), self.ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_CARTE_DOS / 2, None, 60, NOIR, centrer=True)
        SCREEN.blit(IMAGE_COURONNE, (int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS + (HAUTEUR_CARRE_JOUEUR_SECONDAIRE - LARGEUR_IMAGE_CARTE_DOS - m - 3) / 2 - LARGEUR_IMAGE_COURONNE / 2), self.ySecondaire + m + HAUTEUR_IMAGE_JOUEUR - 2))
        affiche_texte(str(self.nbPointsDeVictoire), int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS + (HAUTEUR_CARRE_JOUEUR_SECONDAIRE - LARGEUR_IMAGE_CARTE_DOS - m) / 2 - 3), int(self.ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_COURONNE / 2 - 2) + 3, None, 35, NOIR, centrer=True)
        SCREEN.blit(IMAGE_CARTE_DOS_SPECIALE, (int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS + (HAUTEUR_CARRE_JOUEUR_SECONDAIRE - LARGEUR_IMAGE_CARTE_DOS - m - 3) / 2 - LARGEUR_IMAGE_CARTE_DOS_SPECIALE / 2), self.ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_CARTE_DOS - HAUTEUR_IMAGE_CARTE_DOS_SPECIALE))
        affiche_texte(str(len(self.listeCartesSpeciales)), int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS + (HAUTEUR_CARRE_JOUEUR_SECONDAIRE - LARGEUR_IMAGE_CARTE_DOS - m - 3) / 2), int(self.ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_CARTE_DOS - HAUTEUR_IMAGE_CARTE_DOS_SPECIALE / 2), None, 35, NOIR, centrer=True)

    # ----------------------------------------------------
    def affichePrincipal(self):
        x = 2 * MARGES + HAUTEUR_CARRE_JOUEUR_SECONDAIRE
        y = 3 * MARGES + HAUTEUR_BANDEAU_ACTIONS + HAUTEUR_TITRE
        l = X_PLATEAU - MARGES_PLATEAU - 2 * MARGES - HAUTEUR_CARRE_JOUEUR_SECONDAIRE
        h = HAUTEUR - 4 * MARGES - HAUTEUR_TITRE - HAUTEUR_BANDEAU_ACTIONS
        rectangle(x, y, l, h)
        m = 3
        pygame.draw.rect(SCREEN, self.couleur, (x + m, y + m, LARGEUR_IMAGE_JOUEUR, HAUTEUR_IMAGE_JOUEUR), 0)
        SCREEN.blit(IMAGE_JOUEUR, (x + m, y + m))
        c = self.couleur
        if c == BLANC:
            c = NOIR
        affiche_texte('Vous : {}'.format(self.nom.upper()), int(x + 2 * m + LARGEUR_IMAGE_JOUEUR), int(y + m + HAUTEUR_IMAGE_JOUEUR / 2 - 34 / 4), None, 34, c)
        self.affichePointsDeVictoire(x + l, y)
        self.afficheCartes(x + l / 2, y + 310)

        m2 = 10
        y2 = Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL + HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL + y
        h2 = h - y2 + y

        y_colonie = y2 + h2 / 4
        y_ville = y2 + h2 / 2
        y_route = y2 + 3 * h2 / 4

        couleur_colonie_image(self.couleur, int(x + m2), int(y_colonie - HAUTEUR_IMAGE_COLONIE / 2))
        SCREEN.blit(IMAGE_COLONIE, (int(x + m2), int(y_colonie - HAUTEUR_IMAGE_COLONIE / 2)))
        couleur_ville_image(self.couleur, int(x + m2), int(y_ville - HAUTEUR_IMAGE_VILLE / 2))
        SCREEN.blit(IMAGE_VILLE, (int(x + m2), int(y_ville - HAUTEUR_IMAGE_VILLE / 2)))

        pygame.draw.line(SCREEN, NOIR, (x + m2, y_route + 5), (x + m2 + 30, y_route - 5), LARGEUR_ROUTE + 4)
        pygame.draw.line(SCREEN, self.couleur, (x + m2, y_route + 5), (x + m2 + 30, y_route - 5), LARGEUR_ROUTE)

        c = NOIR
        if len(self.listeColonies) == NB_COLONIE_MAX:
            c = ROUGE
        affiche_texte('{}/{}'.format(len(self.listeColonies), NB_COLONIE_MAX), x + 90, y_colonie, None, 40, c, centrer=True)
        c = NOIR
        if len(self.listeVilles) == NB_VILLE_MAX:
            c = ROUGE
        affiche_texte('{}/{}'.format(len(self.listeVilles), NB_VILLE_MAX), x + 90, y_ville, None, 40, c, centrer=True)
        c = NOIR
        if len(self.listeRoutes) == NB_ROUTE_MAX:
            c = ROUGE
        affiche_texte('{}/{}'.format(len(self.listeRoutes), NB_ROUTE_MAX), x + 90, y_route, None, 40, c, centrer=True)

    # ----------------------------------------------------
    def clic_sur_cartes(self, x_souris, y_souris):
        r = None
        for cle in self.dictionnaireCartesRessources.keys():
            for carte in self.dictionnaireCartesRessources[cle]:
                if carte.clic(x_souris, y_souris):
                    r = carte
        if r != None:
            if r.selectionner == True:
                r.selectionner = False
            else:
                r.selectionner = True
        return r

    # ----------------------------------------------------
    def clicCarteSecondaire(self, x_souris, y_souris):
        x_carte = self.xSecondaire + 3
        y_carte = self.ySecondaire + 3 + HAUTEUR_IMAGE_JOUEUR

        if x_carte <= x_souris <= x_carte + LARGEUR_IMAGE_CARTE_DOS and y_carte <= y_souris <= y_carte + HAUTEUR_IMAGE_CARTE_DOS:
            return True
        return False


# ==========================================================
class Carte():
    def __init__(self, joueur, ressource):
        self.joueur = joueur
        self.ressource = ressource
        self.selectionner = True
        #self.x_centre = 0
        #self.y_centre = 0
        #self.angle = 0
        #self.rayon = 0
        self.x_image = 0
        self.y_image = 0
        self.largeur_image = 0
        self.hauteur_image = 0

        self.image= IMAGE_CARTE_BOIS
        if self.ressource == RESSOURCE_ARGILE:
            self.image= IMAGE_CARTE_ARGILE
        elif self.ressource == RESSOURCE_MOUTON:
            self.image= IMAGE_CARTE_MOUTON
        elif self.ressource == RESSOURCE_FOIN:
            self.image = IMAGE_CARTE_FOIN
        elif self.ressource == RESSOURCE_PIERRE:
            self.image= IMAGE_CARTE_PIERRE

        self.image_tournee = self.image

    # ----------------------------------------------------
    def affiche(self, x, y, angle, rayon):
        self.angle = angle
        self.a_rad = self.angle * math.pi / 180
        self.rayon = rayon
        if self.selectionner == True:
            self.rayon += 15
        self.x_centre = x - math.sin(self.a_rad) * self.rayon
        self.y_centre = y - math.cos(self.a_rad) * self.rayon

        self.image_tournee = pygame.transform.rotozoom(self.image, self.angle, 1)

        self.largeur_image = self.image_tournee.get_width()
        self.hauteur_image = self.image_tournee.get_height()
        self.x_image = int(self.x_centre - self.largeur_image / 2)
        self.y_image = int(self.y_centre - self.hauteur_image / 2)

        SCREEN.blit(self.image_tournee, (self.x_image, self.y_image))

    # ----------------------------------------------------
    def clic(self, x_souris, y_souris):
        xp = x_souris - self.x_image
        yp = y_souris - self.y_image
        if 0 <= xp < self.largeur_image and 0 <= yp < self.hauteur_image:
            if self.image_tournee.get_at((xp, yp))[3] != 0:
                return True


# ==========================================================
class Route():
    def __init__(self, joueur, arete):
        self.joueur = joueur
        self.arete = arete
        self.arete.contenu = self

    # ----------------------------------------------------
    def affiche(self):
        pygame.draw.line(SCREEN, NOIR, (self.arete.x1, self.arete.y1), (self.arete.x2, self.arete.y2), LARGEUR_ROUTE + 2)
        pygame.draw.line(SCREEN, self.joueur.couleur, (self.arete.x1, self.arete.y1), (self.arete.x2, self.arete.y2), LARGEUR_ROUTE - 2)

# ==========================================================
class Colonie():
    def __init__(self, joueur, sommet):
        self.joueur = joueur
        self.joueur.nbPointsDeVictoire += 1
        self.sommet = sommet
        self.x = self.sommet.x
        self.y = self.sommet.y
        l = LARGEUR_IMAGE_COLONIE / 2
        self.listePointsAffichage = [(self.x, self.y - HAUTEUR_IMAGE_COLONIE + l),
                                     (self.x + l, self.y - l),
                                     (self.x + l, self.y + l),
                                     (self.x - l, self.y + l),
                                     (self.x - l, self.y - l)]

        self.sommet.contenu = self

    # ----------------------------------------------------
    def affiche(self):
        couleur_colonie_image(self.joueur.couleur, self.x - LARGEUR_IMAGE_COLONIE / 2, self.y - HAUTEUR_IMAGE_COLONIE / 2)
        SCREEN.blit(IMAGE_COLONIE, (self.x - LARGEUR_IMAGE_COLONIE / 2, self.y - HAUTEUR_IMAGE_COLONIE / 2))


# ==========================================================
class Ville():
    def __init__(self, joueur, sommet):
        self.joueur = joueur
        self.joueur.nbPointsDeVictoire += 1
        self.sommet = sommet
        self.x = self.sommet.x
        self.y = self.sommet.y
        l = LARGEUR_IMAGE_VILLE / 2
        self.listePointsAffichage = [(self.x, self.y - HAUTEUR_IMAGE_VILLE + l),
                                     (self.x + l, self.y - l),
                                     (self.x + l, self.y + l),
                                     (self.x - l, self.y + l),
                                     (self.x - l, self.y - l)]
        self.sommet.contenu = self

    # ----------------------------------------------------
    def affiche(self):
        couleur_ville_image(self.joueur.couleur, self.x - LARGEUR_IMAGE_VILLE / 2, self.y - HAUTEUR_IMAGE_VILLE / 2)
        SCREEN.blit(IMAGE_VILLE, (self.x - LARGEUR_IMAGE_VILLE / 2, self.y - HAUTEUR_IMAGE_VILLE / 2))