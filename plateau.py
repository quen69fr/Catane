# coding: utf-8

from joueur import *
from tuile import *
from sommet import *
from arete import *
from outils import *


class Plateau:
    def __init__(self, x, y):
        self.x = x + 35
        self.y = y
        self.listeTuile = []
        self.listeSommets = []
        self.listeAretes = []

    # ----------------------------------------------------
    def getSommet(self, id):
        for sommet in self.listeSommets:
            if sommet.id == id:
                return sommet

    # ----------------------------------------------------
    def getArete(self, id):
        for arete in self.listeAretes:
            if arete.id == id:
                return arete

    # ----------------------------------------------------
    def getTuile(self, id):
        for tuile in self.listeTuile:
            if tuile.id == id:
                return tuile

    # ----------------------------------------------------
    def creationPlateau(self):
        # Création des tuiles :
        id_tuile = 0
        id_sommet = 0
        id_arete = 0
        for coordonnnees_tuile in LISTE_COORDONNEES_TUILES:
            tx, ty = coordonnnees_tuile
            tx = self.x + (tx + 1) * largeur_tuile / 2
            ty = self.y + ty * (hauteur_tuile - hauteur_triangle_tuile)
            tuile = Tuile(id_tuile, int(tx), int(ty))
            id_tuile += 1
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
                if sommet is None:
                    sommet = Sommet(id_sommet, int(sx), int(sy))
                    id_sommet += 1
                    self.listeSommets.append(sommet)
                tuile.listeIdSommets.append(sommet.id)
                sommet.listeIdTuile.append(tuile.id)

                # Creation des aretes:
                if ancien_sommet is not None:
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
                            if sommet.id in a.listeIdSommets and sommet2.id in a.listeIdSommets:
                                arete = a
                                break
                        if arete is None:
                            arete = Arete(id_arete, sommet, sommet2)
                            id_arete += 1
                            self.listeAretes.append(arete)
                        tuile.listeIdAretes.append(arete.id)

                ancien_sommet = sommet

        for arete in self.listeAretes:
            for idSommet in arete.listeIdSommets:
                sommet = self.getSommet(idSommet)
                sommet.listeIdAretes.append(arete.id)
        for tuile in self.listeTuile:
            for idArete in tuile.listeIdAretes:
                arete = self.getArete(idArete)
                arete.listeIdTuiles.append(tuile.id)

    # ----------------------------------------------------
    def preparePlateau(self):
        self.repartiRessources()
        self.placeNumeros()
        self.placePorts()

    # ----------------------------------------------------
    def repartiRessources(self, ressource_hasard=False):
        liste_ressources = LISTE_RESSOURCES
        if ressource_hasard:
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

    # ----------------------------------------------------
    def placeNumeros(self, numero_hasard=False):
        liste_numeros = LISTE_NUMERO
        if numero_hasard:
            random.shuffle(liste_numeros)
        desert_passe = False
        for i in range (len(self.listeTuile)):
            tuile = self.listeTuile[i]
            if tuile.ressource == RESSOURCE_DESERT:
                desert_passe = True
            else:
                if not desert_passe:
                    tuile.numero = liste_numeros[i]
                else:
                    tuile.numero = liste_numeros[i-1]

    # ----------------------------------------------------
    def placePorts(self, port_hasard=False):
        listePort = LISTE_RESSOURCES_PORTS
        if port_hasard:
            random.shuffle(listePort)
        for i in range(len(listePort)):
            arete = self.getArete(LISTE_ID_ARETES_PORT_ET_ANGLE_PORT[i][0])
            arete.angle_image_port = LISTE_ID_ARETES_PORT_ET_ANGLE_PORT[i][1]
            arete.ressource_port = LISTE_RESSOURCES_PORTS[i]

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
            if tuile.voleur:
                return tuile

    # ---------------------------------------------------
    def placement_colonie_possible(self, sommet_clic):
        listeIdAretesSommetClic = sommet_clic.listeIdAretes
        for idArete in listeIdAretesSommetClic:
            arete = self.getArete(idArete)
            for idSommet in arete.listeIdSommets:
                sommet = self.getSommet(idSommet)
                if sommet.contenu is not None:
                    return False
        return True

    # ---------------------------------------------------
    def placement_colonie_possible2(self, sommet_clic, joueur):
        if len(joueur.listeColonies) >= NB_COLONIE_MAX:
            return False
        for idArete in sommet_clic.listeIdAretes:
            arete = self.getArete(idArete)
            if arete.contenu is not None:
                if joueur.getMaRoute(arete.contenu) is not None:
                    return True
        return False

    # ---------------------------------------------------
    def placement_ville_possible(self, sommet_clic, joueur):
        if len(joueur.listeVilles) >= NB_VILLE_MAX:
            return False
        if isinstance(joueur.getMesVilleOuColonie(sommet_clic.contenu), Colonie):
            return True
        return False

    # ---------------------------------------------------
    def placement_route_possible(self, arete_clic, joueur, deuxieme_colonie=False):
        if len(joueur.listeRoutes) >= NB_ROUTE_MAX:
            return False
        if arete_clic.contenu is None:
            for idSommet in arete_clic.listeIdSommets:
                sommet = self.getSommet(idSommet)
                if deuxieme_colonie:
                    if joueur.listeColonies[1].idSommet == sommet.id and \
                            joueur.listeColonies[1].couleur == joueur.couleur:
                        return True
                else:
                    if joueur.getMesVilleOuColonie(sommet.contenu) is not None:
                        return True
                    for idArete in sommet.listeIdAretes:
                        arete = self.getArete(idArete)
                        if joueur.getMaRoute(arete.contenu) is not None:
                            return True
        return False

    # ---------------------------------------------------
    def donne_ressource_premiere_colonie(self, colonie, joueur, id_carte, connexionServeur):
        sommet = self.getSommet(colonie.idSommet)
        for idTuile in sommet.listeIdTuile:
            tuile = self.getTuile(idTuile)
            r = tuile.ressource
            if r != RESSOURCE_DESERT:
                c = Carte(r, id_carte)
                id_carte += 4
                joueur.dictionnaireCartesRessources[r].append(c)
                connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__, [joueur.nom, '+'])
        return id_carte

    # ---------------------------------------------------
    def donne_ressource_des(self, nb_des, listeJoueur, id_carte, connexionServeur):
        for tuile in self.listeTuile:
            if tuile.numero == nb_des and tuile.voleur == False:
                for idSommet in tuile.listeIdSommets:
                    sommet = self.getSommet(idSommet)
                    if sommet.contenu is not None:
                        for joueur in listeJoueur:
                            p = joueur.getMesVilleOuColonie(sommet.contenu)
                            if p is not None:
                                n = 1
                                if isinstance(p, Ville):
                                    n = 2
                                for i in range(n):
                                    c = Carte(tuile.ressource, id_carte)
                                    id_carte += 4
                                    joueur.dictionnaireCartesRessources[tuile.ressource].append(c)
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__, [joueur.nom, '+'])
        return id_carte

    # ---------------------------------------------------
    def ajoute_si_port_creation_colonie(self, sommet, joueur):
        for idArete in sommet.listeIdAretes:
            arete = self.getArete(idArete)
            if arete.ressource_port is not None:
                joueur.listeRessourcesPorts.append(arete.ressource_port)
                return True
        return False

    # ---------------------------------------------------
    def trouve_extremitees_chemins(self, joueur, listeExtremitees, listeCheminsPossibles):
        for arete in self.listeAretes:
            if arete.contenu is not None and joueur.getMaRoute(arete.contenu) is not None:
                extremite1 = True
                extremite2 = True
                for i in range(2):
                    sommet = self.getSommet(arete.listeIdSommets[i])
                    if sommet.contenu is None or joueur.getMesVilleOuColonie(sommet.contenu) is not None:
                        for idArete in sommet.listeIdAretes:
                            if idArete != arete.id:
                                a = self.getArete(idArete)
                                if a.contenu is not None and joueur.getMaRoute(a.contenu) is not None:
                                    if i == 0:
                                        extremite1 = False
                                    else:
                                        extremite2 = False

                if (extremite1 and not extremite2) or (extremite2 and not extremite1):
                    listeExtremitees.append(arete)
                elif extremite1 and extremite2:
                    listeCheminsPossibles.append([arete])

    # ---------------------------------------------------
    def calcule_tous_les_chemins_possibles_finis(self, chemin, joueur, listeFinale):
        arete = chemin[-1]
        if len(chemin) == 1:
            sommet1 = self.getSommet(arete.listeIdSommets[0])
            sommet2 = self.getSommet(arete.listeIdSommets[1])
            sommet = sommet1

            if sommet2.contenu is None or joueur.getMesVilleOuColonie(sommet2.contenu) is not None:
                for idArete in sommet2.listeIdAretes:
                    if idArete != arete.id:
                        a = self.getArete(idArete)
                        if a.contenu is not None and joueur.getMaRoute(a.contenu) is not None:
                            sommet = sommet2
        else:
            sommet = self.getSommet(arete.listeIdSommets[0])
            for idArete in sommet.listeIdAretes:
                if idArete == chemin[-2].id:
                    sommet = self.getSommet(arete.listeIdSommets[1])

        listeAreteRoutesSommet = []
        if sommet.contenu is None or joueur.getMesVilleOuColonie(sommet.contenu) is not None:
            for idArete in sommet.listeIdAretes:
                if arete.id != idArete:
                    a = self.getArete(idArete)
                    if a.contenu is not None and joueur.getMaRoute(a.contenu) is not None:
                        if a not in chemin:
                            listeAreteRoutesSommet.append(a)

        if listeAreteRoutesSommet == []:
            listeFinale.append(chemin)
        else:
            listeCheminPossible = []
            for a in listeAreteRoutesSommet:
                c = chemin[:]
                c.append(a)
                listeCheminPossible.append(c)

            for c in listeCheminPossible:
                self.calcule_tous_les_chemins_possibles_finis(c, joueur, listeFinale)

        # affichage = ""
        # for chemin in listeFinale:
        #     affichage += "**"
        #     for arete in chemin:
        #         affichage += "-"+str(arete.id)
        # print(affichage)

    # ---------------------------------------------------
    def gere_route_la_plus_longue(self, joueur, listeJoueurs, connexionServeur):
        ancienJoueurRouteLaPlusLongue = None
        AncienNbRoutes = 4
        for j in listeJoueurs:
            if j.routeLaPlusLongue != False:
                ancienJoueurRouteLaPlusLongue = j
                AncienNbRoutes = j.routeLaPlusLongue

        listeRouteNonUtilisee = joueur.listeRoutes[:]
        listeCheminsPossibles = []
        listeExtremitees = []
        self.trouve_extremitees_chemins(joueur, listeExtremitees, listeCheminsPossibles)
        for areteExtremitee in listeExtremitees:
            self.calcule_tous_les_chemins_possibles_finis([areteExtremitee], joueur, listeCheminsPossibles)
        for chemin in listeCheminsPossibles:
            for arete in chemin:
                route = joueur.getMaRoute(arete.contenu)
                if route in listeRouteNonUtilisee:
                    listeRouteNonUtilisee.remove(route)

        while len(listeRouteNonUtilisee) > 0:
            for a in self.listeAretes:
                if a.contenu == listeRouteNonUtilisee[0].id:
                    self.calcule_tous_les_chemins_possibles_finis([a], joueur, listeCheminsPossibles)
                    break
            for chemin in listeCheminsPossibles:
                for arete in chemin:
                    route = joueur.getMaRoute(arete.contenu)
                    if route in listeRouteNonUtilisee:
                        listeRouteNonUtilisee.remove(route)

        for chemin in listeCheminsPossibles:
            if len(chemin) > AncienNbRoutes:
                if ancienJoueurRouteLaPlusLongue:
                    ancienJoueurRouteLaPlusLongue.routeLaPlusLongue = False
                    ancienJoueurRouteLaPlusLongue.nbPointsDeVictoire -= 2
                    connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                       ancienJoueurRouteLaPlusLongue.routeLaPlusLongue,
                                                       info=[ancienJoueurRouteLaPlusLongue.nom, 'routeLaPlusLongue'])
                    connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                       ancienJoueurRouteLaPlusLongue.nbPointsDeVictoire,
                                                       info=[ancienJoueurRouteLaPlusLongue.nom, 'nbPointsDeVictoire'])
                joueur.routeLaPlusLongue = len(chemin)
                joueur.nbPointsDeVictoire += 2
                connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR, joueur.routeLaPlusLongue,
                                                   info=[joueur.nom, 'routeLaPlusLongue'])
                connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR, joueur.nbPointsDeVictoire,
                                                   info=[joueur.nom, 'nbPointsDeVictoire'])
                return True
        return False

    # ---------------------------------------------------
    def gere_points3chevaliers(self, joueur, listeJoueurs, connexionServeur):
        ancien_joueur_points3chevaliers = None
        ancien_nbCartesChevaliersRetournees = 2
        for j in listeJoueurs:
            if j.points3chevaliers:
                if j == joueur:
                    return False
                ancien_joueur_points3chevaliers = j
                ancien_nbCartesChevaliersRetournees = j.nbCartesChevaliersRetournees
        if joueur.nbCartesChevaliersRetournees > ancien_nbCartesChevaliersRetournees:
            joueur.points3chevaliers = True
            joueur.nbPointsDeVictoire += 2
            connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR, joueur.points3chevaliers,
                                               info=[joueur.nom, 'points3chevaliers'])
            connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR, joueur.nbPointsDeVictoire,
                                               info=[joueur.nom, 'nbPointsDeVictoire'])
            if ancien_joueur_points3chevaliers is not None:
                ancien_joueur_points3chevaliers.points3chevaliers = False
                ancien_joueur_points3chevaliers.nbPointsDeVictoire -= 2
                connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                   ancien_joueur_points3chevaliers.points3chevaliers,
                                                   info=[ancien_joueur_points3chevaliers.nom, 'points3chevaliers'])
                connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                   ancien_joueur_points3chevaliers.nbPointsDeVictoire,
                                                   info=[ancien_joueur_points3chevaliers.nom, 'nbPointsDeVictoire'])
            return True
        return False

    # ---------------------------------------------------
    def affiche(self):
        for tuile in self.listeTuile:
            tuile.affiche()
        for arete in self.listeAretes:
            arete.affiche()
        for sommet in self.listeSommets:
            sommet.affiche()

    # ---------------------------------------------------
    def dump(self):
        dic = {'tuiles': [tuile.__dict__ for tuile in self.listeTuile],
               'aretes': [arete.__dict__ for arete in self.listeAretes],
               'sommets': [sommet.__dict__ for sommet in self.listeSommets]}

        return dic

    # ---------------------------------------------------
    def update(self, dic):
        self.listeTuile = []
        for dumpDicTuile in dic['tuiles']:
            tuile = Tuile(0, 0, 0)
            tuile.__dict__.update(dumpDicTuile)
            self.listeTuile.append(tuile)
        self.listeAretes = []
        s = Sommet(0, 0, 0) # Sommet fictif nécessaire pour créer les arètes qui sont mises à jour ensuite
        for dumpDicArete in dic['aretes']:
            arete = Arete(0, s, s)
            arete.__dict__.update(dumpDicArete)
            self.listeAretes.append(arete)
        self.listeSommets = []
        for dumpDicSommet in dic['sommets']:
            sommet = Sommet(0, 0, 0)
            sommet.__dict__.update(dumpDicSommet)
            self.listeSommets.append(sommet)

