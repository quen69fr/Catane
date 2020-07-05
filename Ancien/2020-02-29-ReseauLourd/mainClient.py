# coding: utf-8

from plateau import *
from outils import *

if __name__=="__main__":
    hote = "127.0.0.1"
    port = 12800
    connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_serveur.connect((hote, port))
    print("Connexion établie avec le serveur sur le port {}".format(port))

    monJoueur = connexion_avec_serveur.recv(1024)
    monJoueur = pickle.loads(monJoueur)
    maCouleur = monJoueur.couleur


    listeYAffichageJoueursSecondaire = []
    listeJoueurs = demandeAServeur('listeJoueurs', connexion_avec_serveur)

    y = 3 * MARGES + HAUTEUR_TITRE + HAUTEUR_BANDEAU_ACTIONS
    n = 0
    for joueur in listeJoueurs:
        if joueur.couleur != maCouleur:
            listeYAffichageJoueursSecondaire.append(y)
            y += HAUTEUR_CARRE_JOUEUR_SECONDAIRE + MARGES
            n += 1000
        else:
            id_villes_colonies = n
            id_route = n

    listeCouleurJoueursPlacement = demandeAServeur('listeCouleurJoueursPlacement', connexion_avec_serveur)

    clic_up_down = 0
    nature_clic = None

    listeBoutonsMonJoueurs = []
    m = 8
    x = 2 * MARGES + HAUTEUR_CARRE_JOUEUR_SECONDAIRE
    y = 3 * MARGES + HAUTEUR_BANDEAU_ACTIONS + HAUTEUR_TITRE
    l = int((X_PLATEAU - MARGES_PLATEAU - 2 * MARGES - HAUTEUR_CARRE_JOUEUR_SECONDAIRE - 3 * m) / 2)
    listeBoutonsMonJoueurs.append(Bouton(x + m, y + 225, 'construction', largeur=l, hauteur=40, texte='Construction'))
    listeBoutonsMonJoueurs.append(Bouton(x + l + 2 * m, y + 225, 'echanges', largeur=l, hauteur=40, texte='Echanges'))

    boutonLancerDes = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'des', largeur=250, hauteur=40, texte='Lancer les dés', centrer=True)
    boutonRecupererRessources = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'ressource', largeur=250, hauteur=40, texte='Récupérer les ressources', centrer=True)
    boutonFinEchanges = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'fin_echanges', largeur=250, hauteur=40, texte='Fin des échanges', centrer=True)
    boutonFinTour = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'fin_tour', largeur=250, hauteur=40, texte='Fin du tour', centrer=True)
    boutonJeterCartes = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'jeter_cartes', largeur=250, hauteur=40, texte='Jeter les catres', centrer=True)

    while True:
        etat_partie = demandeAServeur('etat_partie', connexion_avec_serveur)
        listeJoueurs = demandeAServeur('listeJoueurs', connexion_avec_serveur)
        plateau = demandeAServeur('plateau', connexion_avec_serveur)
        if etat_partie == 'placement':
            compteurJoueursPlacement = demandeAServeur('compteurJoueursPlacement', connexion_avec_serveur)
            nature_clic = demandeAServeur('nature_clic', connexion_avec_serveur)
        elif etat_partie == 'jeu':
            sous_partie_jeu = demandeAServeur('sous_partie_jeu', connexion_avec_serveur)
            nb_de1, nb_de2 = demandeAServeur('nb_des', connexion_avec_serveur)
            voleur_etape = demandeAServeur('voleur_etape', connexion_avec_serveur)
            couleurJoueurTourJeu = demandeAServeur('couleurJoueurTourJeu', connexion_avec_serveur)

        for joueur in listeJoueurs:
            if joueur.couleur == maCouleur:
                monJoueur = joueur

        souris = pygame.mouse.get_pos()
        x_souris = souris[0]
        y_souris = souris[1]

        clic = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                # print(event.key)
                # Q
                if event.key == 97:
                    pygame.quit()
                    exit(0)
            if clic_up_down == 1:
                if event.type == pygame.MOUSEBUTTONUP:
                    clic_up_down = 0
                    clic = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clic_up_down = 1

        affiche_ecran_principal(etat_partie)
        plateau.affiche()

        i = 0
        for joueur in listeJoueurs:
            joueur.affichePions()
            if joueur == monJoueur:
                joueur.affichePrincipal()
                if clic:
                    if monJoueur.clic_sur_cartes(x_souris, y_souris) != None:
                        envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)
            else:
                joueur.afficheSecondaire(listeYAffichageJoueursSecondaire[i])
                i += 1

        for bouton in listeBoutonsMonJoueurs:
            bouton.affiche()

        if etat_partie == 'placement':    # On fait comme si on pouvait placer tous les joueur

            if listeCouleurJoueursPlacement[compteurJoueursPlacement] == maCouleur:
                couleur = monJoueur.couleur
                if couleur == BLANC:
                    couleur = NOIR
                affiche_texte("Vous devez placer une {}.".format(nature_clic), X_CENTRE_AFFICHAGE_GAUCHE, Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)

                if clic:
                    if nature_clic == 'colonie':
                        sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                        if sommet != None:
                            if plateau.placement_colonie_possible(sommet):
                                c = Colonie(id_villes_colonies, monJoueur, sommet)
                                id_villes_colonies += 1
                                monJoueur.listeColonies.append(c)
                                if compteurJoueursPlacement < len(listeCouleurJoueursPlacement) / 2:
                                    plateau.donne_ressource_premiere_colonie(c, monJoueur)
                                nature_clic = 'route'

                                envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)
                                envoieAuServeur('nature_clic', nature_clic, connexion_avec_serveur)
                                envoieAuServeur('plateau', plateau, connexion_avec_serveur)

                    elif nature_clic == 'route':
                        arete = plateau.clic_sur_aretes(x_souris, y_souris)
                        if arete != None:
                            if plateau.placement_route_possible(arete, monJoueur):
                                monJoueur.listeRoutes.append(Route(id_route, monJoueur, arete))
                                id_route += 1
                                compteurJoueursPlacement += 1
                                nature_clic = 'colonie'
                                if compteurJoueursPlacement >= len(listeCouleurJoueursPlacement):
                                    etat_partie = 'jeu'
                                    nature_clic = None

                                envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)
                                envoieAuServeur('nature_clic', nature_clic, connexion_avec_serveur)
                                envoieAuServeur('plateau', plateau, connexion_avec_serveur)
                                if etat_partie == 'jeu':
                                    envoieAuServeur('etat_partie', etat_partie, connexion_avec_serveur)
                                else:
                                    envoieAuServeur('compteurJoueursPlacement', compteurJoueursPlacement, connexion_avec_serveur)

            else:
                for j in listeJoueurs:
                    if j.couleur == listeCouleurJoueursPlacement[compteurJoueursPlacement]:
                        joueurTour = j
                couleur = listeCouleurJoueursPlacement[compteurJoueursPlacement]
                if couleur == BLANC:
                    couleur = NOIR
                affiche_texte("C'est aux {} de placer une {}.".format(joueurTour.nom, nature_clic), X_CENTRE_AFFICHAGE_GAUCHE, Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)

        elif etat_partie == 'jeu':

            m = int((HAUTEUR_BANDEAU_ACTIONS - TAILLE_DES) / 2)
            affiche_de(MARGES + m, 2 * MARGES + HAUTEUR_TITRE + m, TAILLE_DES, int(TAILLE_DES / 12), int(TAILLE_DES / 4), nb_de1)
            affiche_de(MARGES + 2 * m + TAILLE_DES, 2 * MARGES + HAUTEUR_TITRE + m, TAILLE_DES, int(TAILLE_DES / 12), int(TAILLE_DES / 4), nb_de2)

            if couleurJoueurTourJeu == maCouleur:

                if sous_partie_jeu == 'des':
                    if nb_de1 == 0 or nb_de2 == 0:
                        boutonLancerDes.affiche()
                        if clic:
                            if boutonLancerDes.clic(x_souris, y_souris):
                                for joueur in listeJoueurs:
                                    joueur.deselection_cartes()
                                envoieAuServeur('listeJoueurs', listeJoueurs, connexion_avec_serveur)
                                nb_de1 = random.randint(1, 6)
                                nb_de2 = random.randint(1, 6)
                                envoieAuServeur('nb_des', (nb_de1, nb_de2), connexion_avec_serveur)
                                if nb_de1 + nb_de2 == 7:
                                    voleur_etape = 0
                                    envoieAuServeur('voleur_etape', voleur_etape, connexion_avec_serveur)

                    else:
                        if nb_de1 + nb_de2 == 7:
                            if voleur_etape == 0:
                                if monJoueur.compte_nb_cartes() <= 7:
                                    voleur_etape += 1
                                    envoieAuServeur('voleur_etape', voleur_etape, connexion_avec_serveur)

                                else:
                                    nb_selec = monJoueur.compte_nb_cartes_selectionnees()
                                    nb_a_selec = math.floor(monJoueur.compte_nb_cartes() / 2)
                                    if nb_selec >= nb_a_selec:
                                        boutonJeterCartes.affiche()
                                        if nb_selec > nb_a_selec:
                                            monJoueur.clic_sur_cartes(x_souris, y_souris)
                                        elif clic:
                                            if boutonJeterCartes.clic(x_souris, y_souris):
                                                voleur_etape += 1
                                                for carte in monJoueur.cree_listeCartes():
                                                    if carte.selectionner == True:
                                                        monJoueur.dictionnaireCartesRessources[carte.ressource].remove(carte)
                                        envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)
                                    else:
                                        affiche_texte("Vous devez jeter {} cartes.".format(math.floor(monJoueur.compte_nb_cartes() / 2)), X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)

                            elif voleur_etape == 1:
                                affiche_texte('Vous devez déplacer le voleur.', X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)
                                if clic:
                                    tuile = plateau.clic_sur_tuile(x_souris, y_souris)
                                    if tuile != None:
                                        for t in plateau.listeTuile:
                                            if t.voleur == True:
                                                if t != tuile:
                                                    t.voleur = False
                                                    tuile.voleur = True
                                                    voleur_etape += 1
                                                    sous_partie_jeu = 'jeu'
                                                    for idSommet in tuile.listeIdSommets:
                                                        sommet = plateau.getSommet(idSommet)
                                                        if sommet.contenu != None:
                                                            if monJoueur.getMesVilleOuColonie(sommet.contenu) == None:
                                                                for j in listeJoueurs:
                                                                    if j.getMesVilleOuColonie(sommet.contenu) != None and j.compte_nb_cartes:
                                                                        sous_partie_jeu = 'des'

                                                    envoieAuServeur('sous_partie_jeu', sous_partie_jeu, connexion_avec_serveur)
                                                    envoieAuServeur('voleur_etape', voleur_etape, connexion_avec_serveur)
                                                    envoieAuServeur('plateau', plateau, connexion_avec_serveur)
                            else:
                                affiche_texte('Vous devez voler une carte.', X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)
                                if clic:
                                    i = 0
                                    for joueur in listeJoueurs:
                                        if joueur != monJoueur:
                                            if joueur.clicCarteSecondaire(x_souris, y_souris, listeYAffichageJoueursSecondaire[i]):
                                                i += 1
                                                listeJoueursPossibles = []
                                                for idSommet in plateau.renvoie_tuile_voleur().listeIdSommets:
                                                    sommet = plateau.getSommet(idSommet)
                                                    for j in listeJoueurs:
                                                        if j.getMesVilleOuColonie(sommet.contenu) != None:
                                                            listeJoueursPossibles.append(j)
                                                if joueur.compte_nb_cartes() != 0 and joueur in listeJoueursPossibles:
                                                    carte = joueur.carte_au_hasard()
                                                    if carte != None:
                                                        carte.selectionner = True
                                                        joueur.dictionnaireCartesRessources[carte.ressource].remove(carte)
                                                        monJoueur.dictionnaireCartesRessources[carte.ressource].append(carte)
                                                        sous_partie_jeu = 'jeu'
                                                        envoieAuServeur('sous_partie_jeu', sous_partie_jeu, connexion_avec_serveur)
                                                        envoieAuServeur('listeJoueurs', listeJoueurs, connexion_avec_serveur)

                        else:
                            boutonRecupererRessources.affiche()
                            if clic:
                                if boutonRecupererRessources.clic(x_souris, y_souris):
                                    plateau.donne_ressource_des(nb_de1 + nb_de2, listeJoueurs)
                                    envoieAuServeur('listeJoueurs', listeJoueurs, connexion_avec_serveur)
                                    sous_partie_jeu = 'jeu'
                                    envoieAuServeur('sous_partie_jeu', sous_partie_jeu, connexion_avec_serveur)

                elif sous_partie_jeu == 'jeu':
                    boutonFinTour.affiche()
                    if clic:
                        if boutonFinTour.clic(x_souris, y_souris):
                            sous_partie_jeu = 'fin'
                            envoieAuServeur('sous_partie_jeu', sous_partie_jeu, connexion_avec_serveur)

                        for bouton in listeBoutonsMonJoueurs:
                            if bouton.clic(x_souris, y_souris):
                                if bouton.parametre == 'construction':
                                    if bouton.selectionner == False:
                                        bouton.selectionner = True
                                        listeRessourcesCartesSelctionees = monJoueur.cree_listeRessourcesCartesSelectionnees()
                                        if sorted(listeRessourcesCartesSelctionees) == sorted(PRIX_COLONIE):
                                            nature_clic = 'colonie'
                                        elif sorted(listeRessourcesCartesSelctionees) == sorted(PRIX_ROUTE):
                                            nature_clic = 'route'
                                        elif sorted(listeRessourcesCartesSelctionees) == sorted(PRIX_VILLE):
                                            nature_clic = 'ville'
                                        if nature_clic == None:
                                            bouton.selectionner = False
                                        else:
                                            monJoueur.suprimeCartesSelectionnes()
                                            envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)

                                    else:
                                        prix = []
                                        if nature_clic == 'colonie':
                                            prix = PRIX_COLONIE
                                        elif nature_clic == 'route':
                                            prix = PRIX_ROUTE
                                        elif nature_clic == 'ville':
                                            prix = PRIX_VILLE
                                        monJoueur.rendCarteConstruction(prix)
                                        envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)
                                        nature_clic = None
                                        bouton.selectionner = False

                    if nature_clic == 'colonie':
                        if clic:
                            sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                            if sommet != None:
                                if plateau.placement_colonie_possible(sommet) and plateau.placement_colonie_possible2(sommet, monJoueur):
                                    monJoueur.listeColonies.append(Colonie(id_villes_colonies, monJoueur, sommet))
                                    id_villes_colonies += 1
                                    envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False


                    elif nature_clic == 'route':
                        if clic:
                            arete = plateau.clic_sur_aretes(x_souris, y_souris)
                            if arete != None:
                                if plateau.placement_route_possible(arete, monJoueur):
                                    monJoueur.listeRoutes.append(Route(id_route, monJoueur, arete))
                                    id_route += 1
                                    envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False

                    elif nature_clic == 'ville':
                        if clic:
                            sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                            if sommet != None:
                                if plateau.placement_ville_possible(sommet, monJoueur):
                                    monJoueur.listeVilles.append(Ville(id_villes_colonies, monJoueur, sommet))
                                    id_villes_colonies += 1
                                    envoieAuServeur('listeJoueurs.' + monJoueur.nom, monJoueur, connexion_avec_serveur)
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False

                elif sous_partie_jeu == 'fin':
                    nb_de1 = 0
                    nb_de2 = 0
                    t = False
                    for joueur in listeJoueurs:
                        if t == False:
                            if joueur == monJoueur:
                                t = True
                        else:
                            couleurJoueurTourJeu = joueur.couleur
                            t = False
                            break
                    if t == True:
                        couleurJoueurTourJeu = listeJoueurs[0].couleur

                    sous_partie_jeu = 'des'

                    envoieAuServeur('nb_des', (nb_de1, nb_de2), connexion_avec_serveur)
                    envoieAuServeur('sous_partie_jeu', sous_partie_jeu, connexion_avec_serveur)
                    envoieAuServeur('couleurJoueurTourJeu', couleurJoueurTourJeu, connexion_avec_serveur)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
