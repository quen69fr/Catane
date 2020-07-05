# coding: utf-8

from outils import *


class Joueur():
    def __init__(self, pseudo, couleur):
        self.pseudo = pseudo
        self.couleur = couleur
        self.listeColonies = []
        self.listeVilles = []
        self.listeRoutes = []
        # self.listeCartes = []
        self.dictionnaireCartesRessources = {RESSOURCE_BOIS: [], RESSOURCE_ARGILE: [], RESSOURCE_MOUTON: [],
                                             RESSOURCE_FOIN: [], RESSOURCE_PIERRE: []}
        self.listeCartesSpeciales = []
        self.nbPointsDeVictoire = 0
        self.xSecondaire = MARGES
        self.listeRessourcesPorts = []
        self.jeterCartes = False
        self.routeLaPlusLongue = False
        self.nbCartesChevaliersRetournees = 0
        self.points3chevaliers = False

        self.nom = 'w'
        if self.couleur == ROUGE:
            self.nom = 'r'
        elif self.couleur == ORANGE:
            self.nom = 'o'
        elif self.couleur == BLEU:
            self.nom = 'b'

    # ----------------------------------------------------
    def getMaRoute(self, id):
        for route in self.listeRoutes:
            if route.id == id:
                return route
        return None

    # ----------------------------------------------------
    def getMesVilleOuColonie(self, id):
        for colonie in self.listeColonies:
            if colonie.id == id:
                return colonie
        for ville in self.listeVilles:
            if ville.id == id:
                return ville
        return None

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
    def deselection_cartes(self, connexionServeur):
        for cle in self.dictionnaireCartesRessources.keys():
            for carte in self.dictionnaireCartesRessources[cle]:
                if carte.selectionner:
                    carte.selectionner = False
                    connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, carte.__dict__, 'select')

    # ----------------------------------------------------
    def cree_listeCartesSelectionnees(self):
        l = []
        for cle in self.dictionnaireCartesRessources.keys():
            for carte in self.dictionnaireCartesRessources[cle]:
                if carte.selectionner:
                    l.append(carte)
        return l

    # ----------------------------------------------------
    def carteSpecialesSelectionner(self):
        for carte in self.listeCartesSpeciales:
            if carte.selectionner == True:
                return carte
        return None

    # ----------------------------------------------------
    def suprimeCartesSelectionnes(self, connexionServeur):
        for carte in self.cree_listeCartesSelectionnees():
            self.dictionnaireCartesRessources[carte.ressource].remove(carte)
            connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, carte.__dict__, info=[self.nom, '-'])

    # ----------------------------------------------------
    def rendCarteConstruction(self, prix, id_carte, connexionServeur):
        for ressource in prix:
            c = Carte(ressource, id_carte)
            id_carte += 4
            self.dictionnaireCartesRessources[ressource].append(c)
            connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__, info=[self.nom, '+'])
        return id_carte

    # ----------------------------------------------------
    def afficheRoutes1(self):
        for route in self.listeRoutes:
            route.affiche1()

    # ----------------------------------------------------
    def afficheRoutes2(self):
        for route in self.listeRoutes:
            route.affiche2()

    # ----------------------------------------------------
    def afficheColoniesEtVilles(self):
        for colonie in self.listeColonies:
            colonie.affiche()
        for ville in self.listeVilles:
            ville.affiche()

    # ----------------------------------------------------
    def afficheCartes(self, x, y, listeCartes, angle_total):
        angle_min = 13
        angle_total = angle_total
        r = 200

        liste_cartes = listeCartes
        nb_cartes = len(liste_cartes)

        angle_entre_cartes = angle_min
        if nb_cartes > angle_total / angle_min:
            angle_entre_cartes = angle_total / nb_cartes

        for i in range(nb_cartes):
            a = (((nb_cartes - i - 1) + 0.5 - nb_cartes / 2) * angle_entre_cartes)
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
                SCREEN.blit(img,
                            (x + (LARGEUR_IMAGE_PETITE_COURONNE + m) * i, y + (HAUTEUR_IMAGE_PETITE_COURONNE + m) * j))

    # ----------------------------------------------------
    def afficheSecondaire(self, ySecondaire):
        rectangle(self.xSecondaire, ySecondaire, HAUTEUR_CARRE_JOUEUR_SECONDAIRE, HAUTEUR_CARRE_JOUEUR_SECONDAIRE)
        m = 3
        pygame.draw.rect(SCREEN, self.couleur,
                         (self.xSecondaire + m, ySecondaire + m, LARGEUR_IMAGE_JOUEUR, HAUTEUR_IMAGE_JOUEUR), 0)
        SCREEN.blit(IMAGE_JOUEUR, (self.xSecondaire + m, ySecondaire + m))
        c = self.couleur
        if c == BLANC:
            c = NOIR
        affiche_texte(self.pseudo.upper(), int(self.xSecondaire + m + LARGEUR_IMAGE_JOUEUR + (
                    HAUTEUR_CARRE_JOUEUR_SECONDAIRE - m - LARGEUR_IMAGE_JOUEUR) / 2),
                      int(ySecondaire + HAUTEUR_IMAGE_JOUEUR / 2 + m), None, 28, c, centrer=True)
        SCREEN.blit(IMAGE_CARTE_DOS, (self.xSecondaire + m - 2, ySecondaire + m + HAUTEUR_IMAGE_JOUEUR))
        affiche_texte(str(self.compte_nb_cartes()), int(self.xSecondaire + m - 2 + LARGEUR_IMAGE_CARTE_DOS / 2),
                      ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_CARTE_DOS / 2, None, 60, NOIR,
                      centrer=True)
        SCREEN.blit(IMAGE_COURONNE, (int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS + (
                    HAUTEUR_CARRE_JOUEUR_SECONDAIRE - LARGEUR_IMAGE_CARTE_DOS - m - 3) / 2 - LARGEUR_IMAGE_COURONNE / 2),
                                     ySecondaire + m + HAUTEUR_IMAGE_JOUEUR - 2))
        affiche_texte(str(self.nbPointsDeVictoire), int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS + (
                    HAUTEUR_CARRE_JOUEUR_SECONDAIRE - LARGEUR_IMAGE_CARTE_DOS - m) / 2 - 3),
                      int(ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_COURONNE / 2 - 2) + 3, None, 35, NOIR,
                      centrer=True)

        SCREEN.blit(IMAGE_PETITE_CARTE_DOS_SPECIALE, (int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS - 4),
                                                      ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_CARTE_DOS - HAUTEUR_IMAGE_PETITE_CARTE_SPECIALE))
        affiche_texte(str(len(self.listeCartesSpeciales)),
                      int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS - 4 + LARGEUR_IMAGE_PETITE_CARTE_SPECIALE / 2),
                      int(
                          ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_CARTE_DOS - HAUTEUR_IMAGE_PETITE_CARTE_SPECIALE / 2),
                      None, 35, NOIR, centrer=True)
        SCREEN.blit(IMAGE_PETITE_CARTE_CHEVALIER, (
        int(self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS - 4 - 5 + LARGEUR_IMAGE_PETITE_CARTE_SPECIALE),
        ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_CARTE_DOS - HAUTEUR_IMAGE_PETITE_CARTE_SPECIALE))
        affiche_texte(str(self.nbCartesChevaliersRetournees), int(
            self.xSecondaire + m + LARGEUR_IMAGE_CARTE_DOS - 4 - 5 + LARGEUR_IMAGE_PETITE_CARTE_SPECIALE + LARGEUR_IMAGE_PETITE_CARTE_SPECIALE / 2),
                      int(
                          ySecondaire + m + HAUTEUR_IMAGE_JOUEUR + HAUTEUR_IMAGE_CARTE_DOS - HAUTEUR_IMAGE_PETITE_CARTE_SPECIALE / 2),
                      None, 35, NOIR, centrer=True)

        p = 0
        if self.routeLaPlusLongue != False:
            p += 2
        if self.points3chevaliers:
            p += 2
        if p > 0:
            pygame.gfxdraw.filled_circle(SCREEN, self.xSecondaire + HAUTEUR_CARRE_JOUEUR_SECONDAIRE, ySecondaire, 22,
                                         NOIR)
            pygame.gfxdraw.filled_circle(SCREEN, self.xSecondaire + HAUTEUR_CARRE_JOUEUR_SECONDAIRE, ySecondaire, 20,
                                         BLANC)
            affiche_texte('+{}'.format(p), self.xSecondaire + HAUTEUR_CARRE_JOUEUR_SECONDAIRE, ySecondaire, None, 38,
                          NOIR, centrer=True)

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
        affiche_texte(f'Vous : {self.pseudo.upper()}', int(x + 2 * m + LARGEUR_IMAGE_JOUEUR),
                      int(y + m + HAUTEUR_IMAGE_JOUEUR / 2 - 34 / 4), None, 34, c)
        self.affichePointsDeVictoire(x + l, y)
        self.afficheCartes(x + l / 2, y + 310, self.cree_listeCartes(), 90)

        m2 = 10
        y2 = Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL + HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL + y
        h2 = h - y2 + y

        y_colonie = int(y2 + h2 / 5)
        y_ville = int(y2 + 2 * h2 / 5)
        y_route = int(y2 + 3 * h2 / 5)
        y_chevalier = int(y2 + 4 * h2 / 5)

        couleur_colonie_image(self.couleur, int(x + m2), int(y_colonie - HAUTEUR_IMAGE_COLONIE / 2))
        SCREEN.blit(IMAGE_COLONIE, (int(x + m2), int(y_colonie - HAUTEUR_IMAGE_COLONIE / 2)))
        couleur_ville_image(self.couleur, int(x + m2), int(y_ville - HAUTEUR_IMAGE_VILLE / 2))
        SCREEN.blit(IMAGE_VILLE, (int(x + m2), int(y_ville - HAUTEUR_IMAGE_VILLE / 2)))
        SCREEN.blit(IMAGE_PETITE_CARTE_CHEVALIER, (x + m2, int(y_chevalier - HAUTEUR_IMAGE_PETITE_CARTE_SPECIALE / 2)))
        affiche_texte(str(self.nbCartesChevaliersRetournees), x + 90, y_chevalier, None, 40, NOIR, centrer=True)

        affiche_route(x + m2 + 3, y_route + 2, x + m2 + 33, y_route - 8, self.couleur)

        c = NOIR
        if len(self.listeColonies) == NB_COLONIE_MAX:
            c = ROUGE
        affiche_texte('{}/{}'.format(len(self.listeColonies), NB_COLONIE_MAX), x + 90, y_colonie, None, 40, c,
                      centrer=True)
        c = NOIR
        if len(self.listeVilles) == NB_VILLE_MAX:
            c = ROUGE
        affiche_texte('{}/{}'.format(len(self.listeVilles), NB_VILLE_MAX), x + 90, y_ville, None, 40, c, centrer=True)
        c = NOIR
        if len(self.listeRoutes) == NB_ROUTE_MAX:
            c = ROUGE
        affiche_texte('{}/{}'.format(len(self.listeRoutes), NB_ROUTE_MAX), x + 90, y_route, None, 40, c, centrer=True)

        if len(self.listeCartesSpeciales) >= 1:
            self.afficheCartes(x + 126 + (l - 126) / 2, y2 + m2 + 260, self.listeCartesSpeciales, 50)

        p = 0
        if self.routeLaPlusLongue != False:
            p += 2
        if self.points3chevaliers:
            p += 2
        if p > 0:
            pygame.gfxdraw.filled_circle(SCREEN, x + l, y, 22, NOIR)
            pygame.gfxdraw.filled_circle(SCREEN, x + l, y, 20, BLANC)
            affiche_texte('+{}'.format(p), x + l, y, None, 38, NOIR, centrer=True)

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
    def clic_sur_cartes_speciales(self, x_souris, y_souris):
        r = None
        for carte in self.listeCartesSpeciales:
            if carte.clic(x_souris, y_souris):
                r = carte
        if r != None:
            if r.selectionner == True:
                r.selectionner = False
            else:
                r.selectionner = True
                for c in self.listeCartesSpeciales:
                    if c != r:
                        c.selectionner = False
        return r

    # ----------------------------------------------------
    def clicCarteSecondaire(self, x_souris, y_souris, ySecondaire):
        x_carte = self.xSecondaire + 3
        y_carte = ySecondaire + 3 + HAUTEUR_IMAGE_JOUEUR

        if x_carte <= x_souris <= x_carte + LARGEUR_IMAGE_CARTE_DOS and y_carte <= y_souris <= y_carte + HAUTEUR_IMAGE_CARTE_DOS:
            return True
        return False


# ==========================================================
class Carte():
    def __init__(self, ressource, id, selectionner=True):
        self.id = id
        self.ressource = ressource
        self.selectionner = selectionner
        self.x_centre = 0
        self.y_centre = 0
        self.angle = 0
        self.rayon = 0
        self.x_image = 0
        self.y_image = 0
        self.largeur_image = 0
        self.hauteur_image = 0
        self.nouvelleCarte = True  # Uniquement pour les cartes spéciales

    # ----------------------------------------------------
    def affiche(self, x, y, angle, rayon):
        self.angle = angle
        self.a_rad = self.angle * math.pi / 180
        self.rayon = rayon
        if self.selectionner == True:
            self.rayon += 15
        self.x_centre = x - math.sin(self.a_rad) * self.rayon
        self.y_centre = y - math.cos(self.a_rad) * self.rayon

        image = IMAGE_CARTE_BOIS
        if self.ressource == RESSOURCE_ARGILE:
            image = IMAGE_CARTE_ARGILE
        elif self.ressource == RESSOURCE_MOUTON:
            image = IMAGE_CARTE_MOUTON
        elif self.ressource == RESSOURCE_FOIN:
            image = IMAGE_CARTE_FOIN
        elif self.ressource == RESSOURCE_PIERRE:
            image = IMAGE_CARTE_PIERRE
        elif self.ressource == POUVOIR_CHEVALIER:
            image = IMAGE_CARTE_CHEVALIER
        elif self.ressource == POUVOIR_MONOPOLE:
            image = IMAGE_CARTE_MONOPOLE
        elif self.ressource == POUVOIR_POINT_VICTOIRE:
            image = IMAGE_CARTE_POINT_VICTOIRE
        elif self.ressource == POUVOIR_RESSOURCES_GRATUITES:
            image = IMAGE_CARTE_RESSOURCES_GRATUITES
        elif self.ressource == POUVOIR_ROUTES_GRATUITES:
            image = IMAGE_CARTE_ROUTES_GRATUITES

        image_tournee = pygame.transform.rotozoom(image, self.angle, 1)

        self.largeur_image = image_tournee.get_width()
        self.hauteur_image = image_tournee.get_height()
        self.x_image = int(self.x_centre - self.largeur_image / 2)
        self.y_image = int(self.y_centre - self.hauteur_image / 2)

        SCREEN.blit(image_tournee, (self.x_image, self.y_image))

    # ----------------------------------------------------
    def clic(self, x_souris, y_souris):
        image = IMAGE_CARTE_BOIS
        if self.ressource == RESSOURCE_ARGILE:
            image = IMAGE_CARTE_ARGILE
        elif self.ressource == RESSOURCE_MOUTON:
            image = IMAGE_CARTE_MOUTON
        elif self.ressource == RESSOURCE_FOIN:
            image = IMAGE_CARTE_FOIN
        elif self.ressource == RESSOURCE_PIERRE:
            image = IMAGE_CARTE_PIERRE

        image_tournee = pygame.transform.rotozoom(image, self.angle, 1)

        xp = x_souris - self.x_image
        yp = y_souris - self.y_image
        if 0 <= xp < self.largeur_image and 0 <= yp < self.hauteur_image:
            if image_tournee.get_at((xp, yp))[3] != 0:
                return True


# ==========================================================
class Route():
    def __init__(self, id, couleur, arete):
        self.id = id
        self.couleur = couleur
        self.idArete = arete.id
        self.x1 = arete.x1
        self.y1 = arete.y1
        self.x2 = arete.x2
        self.y2 = arete.y2

    # ----------------------------------------------------
    def affiche1(self):
        # affiche_route(self.x1, self.y1, self.x2, self.y2, self.couleur)
        pygame.draw.line(SCREEN, NOIR, (self.x1, self.y1), (self.x2, self.y2), LARGEUR_ROUTE + 2)
        pygame.gfxdraw.filled_circle(SCREEN, self.x1, self.y1, int(LARGEUR_ROUTE / 2), NOIR)
        pygame.gfxdraw.filled_circle(SCREEN, self.x2, self.y2, int(LARGEUR_ROUTE / 2), NOIR)

    def affiche2(self):
        pygame.draw.line(SCREEN, self.couleur, (self.x1, self.y1), (self.x2, self.y2), LARGEUR_ROUTE - 2)
        pygame.gfxdraw.filled_circle(SCREEN, self.x1, self.y1, int(LARGEUR_ROUTE / 2) - 2, self.couleur)
        pygame.gfxdraw.filled_circle(SCREEN, self.x2, self.y2, int(LARGEUR_ROUTE / 2) - 2, self.couleur)

# ==========================================================
class Colonie():
    def __init__(self, id, couleur, sommet):
        self.id = id
        self.couleur = couleur
        self.idSommet = sommet.id
        self.x = sommet.x
        self.y = sommet.y
        l = LARGEUR_IMAGE_COLONIE / 2
        self.listePointsAffichage = [(self.x, self.y - HAUTEUR_IMAGE_COLONIE + l),
                                     (self.x + l, self.y - l),
                                     (self.x + l, self.y + l),
                                     (self.x - l, self.y + l),
                                     (self.x - l, self.y - l)]

    # ----------------------------------------------------
    def affiche(self):
        couleur_colonie_image(self.couleur, self.x - LARGEUR_IMAGE_COLONIE / 2, self.y - HAUTEUR_IMAGE_COLONIE / 2)
        SCREEN.blit(IMAGE_COLONIE, (self.x - LARGEUR_IMAGE_COLONIE / 2, self.y - HAUTEUR_IMAGE_COLONIE / 2))


# ==========================================================
class Ville():
    def __init__(self, id, couleur, sommet):
        self.id = id
        self.couleur = couleur
        self.idSommet = sommet.id
        self.x = sommet.x
        self.y = sommet.y
        l = LARGEUR_IMAGE_VILLE / 2
        self.listePointsAffichage = [(self.x, self.y - HAUTEUR_IMAGE_VILLE + l),
                                     (self.x + l, self.y - l),
                                     (self.x + l, self.y + l),
                                     (self.x - l, self.y + l),
                                     (self.x - l, self.y - l)]

    # ----------------------------------------------------
    def affiche(self):
        couleur_ville_image(self.couleur, self.x - LARGEUR_IMAGE_VILLE / 2, self.y - HAUTEUR_IMAGE_VILLE / 2)
        SCREEN.blit(IMAGE_VILLE, (self.x - LARGEUR_IMAGE_VILLE / 2, self.y - HAUTEUR_IMAGE_VILLE / 2))