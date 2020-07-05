# coding: utf-8

from joueur import *
from tuile import *
from sommet import *
from arete import *
from outils import *

class Plateau():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.listeTuile = []
        self.listeSommets = []
        self.listeAretes = []

    # ----------------------------------------------------
    def creationPlateau(self):
        # Création des tuiles :
        for coordonnnees_tuile in LISTE_COORDONNEES_TUILES:
            tx, ty = coordonnnees_tuile
            tx = self.x + (tx + 1) * largeur_tuile / 2
            ty = self.y + ty * (hauteur_tuile - hauteur_triangle_tuile)
            tuile = Tuile(int(tx), int(ty))
            self.listeTuile.append(tuile)

            # Creation des sommets:
            liste_coordonnees_sommets = [(tx,                     ty),
                                         (tx + largeur_tuile / 2, ty + hauteur_triangle_tuile),
                                         (tx + largeur_tuile / 2, ty + hauteur_tuile - hauteur_triangle_tuile),
                                         (tx,                     ty + hauteur_tuile),
                                         (tx - largeur_tuile / 2, ty + hauteur_tuile - hauteur_triangle_tuile),
                                         (tx - largeur_tuile / 2, ty + hauteur_triangle_tuile)]

            ancien_sommet = None
            for coordonnnees_sommet in liste_coordonnees_sommets:
                sx, sy = coordonnnees_sommet
                sommet = None
                for s in self.listeSommets:
                    if s.x == int(sx) and s.y == int(sy):
                        sommet = s
                        break
                if sommet == None:
                    sommet = Sommet(int(sx), int(sy))
                    self.listeSommets.append(sommet)
                tuile.listeSommets.append(sommet)
                sommet.listeTuile.append(tuile)

                # Creation des aretes:
                if ancien_sommet != None:
                    k = 1
                    if sommet.x == int(liste_coordonnees_sommets[len(liste_coordonnees_sommets) - 1][0]) \
                            and sommet.y == int(liste_coordonnees_sommets[len(liste_coordonnees_sommets) - 1][1]):
                        k = 2
                    for i in range(k):
                        sommet2 = ancien_sommet
                        if i == 1:
                            for s2 in self.listeSommets:
                                if s2.x == int(tx) and s2.y == int(ty):
                                    sommet2 = s2
                                    break
                        arete = None
                        for a in self.listeAretes:
                            if sommet in a.listeSommets and sommet2 in a.listeSommets:
                                arete = a
                                break
                        if arete == None:
                            arete = Arete(sommet, sommet2)
                            self.listeAretes.append(arete)
                        tuile.listeAretes.append(arete)

                ancien_sommet = sommet

        for arete in self.listeAretes:
            for sommet in arete.listeSommets:
                sommet.listeAretes.append(arete)
        for tuile in self.listeTuile:
            for arete in tuile.listeAretes:
                arete.listeTuiles.append(tuile)

    # ----------------------------------------------------
    def preparePlateau(self):
        self.repartiRessources()
        self.placeNumeros()
        self.placePorts()

    # ----------------------------------------------------
    def repartiRessources(self, ressource_hasard=False):
        liste_ressources = LISTE_RESSOURCES
        if ressource_hasard == True:
            random.shuffle(liste_ressources)
            n = liste_ressources.index(RESSOURCE_DESERT)
            m = int(len(liste_ressources) / 2 - 0.5)
            liste_ressources[n] = liste_ressources[m]
            liste_ressources[m] = RESSOURCE_DESERT
        for i in range(len(self.listeTuile)):
            tuile = self.listeTuile[i]
            ressource = liste_ressources[i]
            tuile.ressource = ressource
            if ressource == RESSOURCE_DESERT:
                tuile.voleur = True
            if ressource == RESSOURCE_BOIS:
                tuile.image = IMAGE_TUILE_BOIS
            elif ressource == RESSOURCE_ARGILE:
                tuile.image = IMAGE_TUILE_ARGILE
            elif ressource == RESSOURCE_MOUTON:
                tuile.image = IMAGE_TUILE_MOUTON
            elif ressource == RESSOURCE_FOIN:
                tuile.image = IMAGE_TUILE_FOIN
            elif ressource == RESSOURCE_PIERRE:
                tuile.image = IMAGE_TUILE_PIERRE
            else:
                tuile.image = IMAGE_TUILE_DESERT

    # ----------------------------------------------------
    def placeNumeros(self, numero_hasard=False):
        liste_numeros = LISTE_NUMERO
        if numero_hasard == True:
            random.shuffle(liste_numeros)
        desert_passe = False
        for i in range (len(self.listeTuile)):
            tuile = self.listeTuile[i]
            if tuile.ressource == RESSOURCE_DESERT:
                desert_passe = True
            else:
                if desert_passe == False:
                    tuile.numero = liste_numeros[i]
                else:
                    tuile.numero = liste_numeros[i-1]

    # ----------------------------------------------------
    def placePorts(self, port_hasard=False):
        pass

    # ---------------------------------------------------
    def clic_sur_sommets(self, x_souris, y_souris):
        for sommet in self.listeSommets:
            if sommet.clic(x_souris, y_souris):
                return sommet
        return None

    # ---------------------------------------------------
    def clic_sur_aretes(self, x_souris, y_souris):
        for arete in self.listeAretes:
            if arete.clic(x_souris, y_souris):
                return arete
        return None

    # ---------------------------------------------------
    def clic_sur_tuile(self, x_souris, y_souris):
        for tuile in self.listeTuile:
            if tuile.clic(x_souris, y_souris):
                return tuile
        return None

    # ---------------------------------------------------
    def renvoie_tuile_voleur(self):
        for tuile in self.listeTuile:
            if tuile.voleur == True:
                return tuile

    # ---------------------------------------------------
    def placement_colonie_possible(self, sommet_clic):
        listeAretesSommetClic = sommet_clic.listeAretes
        for arete in listeAretesSommetClic:
            for sommet in arete.listeSommets:
                if sommet.contenu != None:
                    return False
        return True

    # ---------------------------------------------------
    def placement_colonie_possible2(self, sommet_clic, joueur):
        for arete in sommet_clic.listeAretes:
            if arete.contenu != None:
                if arete.contenu.joueur == joueur:
                    return True
        return False

    # ---------------------------------------------------
    def placement_ville_possible(self, sommet_clic, joueur):
        if isinstance(sommet_clic.contenu, Colonie):
            if sommet_clic.contenu.joueur == joueur:
                return True
        return False

    # ---------------------------------------------------
    def placement_route_possible(self, arete_clic, joueur):
        if arete_clic.contenu == None:
            for sommet in arete_clic.listeSommets:
                if sommet.contenu != None:
                    if sommet.contenu.joueur == joueur:
                        return True
                for arete in sommet.listeAretes:
                    if arete.contenu != None:
                        if arete.contenu.joueur == joueur:
                            return True
        return False

    # ---------------------------------------------------
    def donne_ressource_premiere_colonie(self, colonie):
        for tuile in colonie.sommet.listeTuile:
            r = tuile.ressource
            if r != RESSOURCE_DESERT:
                colonie.joueur.dictionnaireCartesRessources[r].append(Carte(colonie.joueur, r))

    # ---------------------------------------------------
    def donne_ressource_des(self, nb_des):
        for tuile in self.listeTuile:
            if tuile.numero == nb_des and tuile.voleur == False:
                for sommet in tuile.listeSommets:
                    if sommet.contenu != None:
                        n = 1
                        if isinstance(sommet.contenu, Ville):
                            n = 2
                        for i in range(n):
                            sommet.contenu.joueur.dictionnaireCartesRessources[tuile.ressource].append(Carte(sommet.contenu.joueur, tuile.ressource))

    # ---------------------------------------------------
    def affiche(self):
        for tuile in self.listeTuile:
            tuile.affiche()
        for arete in self.listeAretes:
            arete.affiche()
        for sommet in self.listeSommets:
            sommet.affiche()