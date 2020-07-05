# coding: utf-8

from plateau import *
from outils import *

if __name__=="__main__":
    plateau = Plateau(X_PLATEAU, Y_PLATEAU)
    plateau.creationPlateau()
    plateau.preparePlateau()
    ecran_reglage = Ecran_reglages()
    etat_partie = 'reglagesJoueurs'
    sous_partie_jeu = 'des'
    nbJoueur = 0
    monJoueur = None
    listeJoueurs = []
    clic_up_down = 0
    listeJoueursPlacement = []
    compteurJoueursPlacement = 0
    nature_clic = 'colonie'
    nb_de1 = 0
    nb_de2 = 0
    voleur_etape = 0

    listeBoutonsMonJoueurs = []
    # listeBoutonsMonJoueurs.append(Bouton(90, 270, 'colonie', largeur=200, hauteur=32, texte='Cree une colonie', tailleTexte=25))
    # listeBoutonsMonJoueurs.append(Bouton(90, 310, 'ville', largeur=200, hauteur=32, texte='Cree une ville', tailleTexte=25))
    # listeBoutonsMonJoueurs.append(Bouton(90, 350, 'route', largeur=200, hauteur=32, texte='Cree une route', tailleTexte=25))
    m = 8
    x = 2 * MARGES + HAUTEUR_CARRE_JOUEUR_SECONDAIRE
    y = 3 * MARGES + HAUTEUR_BANDEAU_ACTIONS + HAUTEUR_TITRE
    l = int((X_PLATEAU - MARGES_PLATEAU - 2 * MARGES - HAUTEUR_CARRE_JOUEUR_SECONDAIRE - 3 * m) / 2)
    listeBoutonsMonJoueurs.append(Bouton(x + m, y + Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL, 'construction', largeur=l, hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='Construction'))
    listeBoutonsMonJoueurs.append(Bouton(x + l + 2 * m, y + Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL, 'echanges', largeur=l, hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='Echanges'))


    boutonLancerDes = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'des', largeur=250, hauteur=40, texte='Lancer les dés', centrer=True)
    boutonRecupererRessources = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'ressource', largeur=250, hauteur=40, texte='Récupérer les ressources', centrer=True)
    boutonFinEchanges = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'fin_echanges', largeur=250, hauteur=40, texte='Fin des échanges', centrer=True)
    boutonFinTour = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'fin_tour', largeur=250, hauteur=40, texte='Fin du tour', centrer=True)
    boutonJeterCartes = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'jeter_cartes', largeur=250, hauteur=40, texte='Jeter les catres', centrer=True)



    while True:
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

        if etat_partie == 'reglagesJoueurs' or etat_partie == 'reglagePlateau':

            ecran_reglage.affiche(etat_partie)

            if clic:
                parametre_bouton = ecran_reglage.clic_bouton(etat_partie, x_souris, y_souris)

                if parametre_bouton != None:

                    if etat_partie == 'reglagesJoueurs':
                        if parametre_bouton == 'valider':
                            n = 0
                            for bouton in ecran_reglage.listeBoutonsJoueurs:
                                if bouton.selectionner == True:
                                    c = BLEU
                                    if bouton.parametre == 'rouge':
                                        c = ROUGE
                                    elif bouton.parametre == 'blanc':
                                        c = BLANC
                                    elif bouton.parametre == 'orange':
                                        c = ORANGE
                                    if n == 0:
                                        monJoueur = Joueur(c)
                                        listeJoueurs.append(monJoueur)
                                    else:
                                        listeJoueurs.append(Joueur(c))
                                    n += 1

                            y = 3 * MARGES + HAUTEUR_TITRE + HAUTEUR_BANDEAU_ACTIONS
                            for joueur in listeJoueurs:
                                if joueur != monJoueur:
                                    joueur.ySecondaire = y
                                    y += HAUTEUR_CARRE_JOUEUR_SECONDAIRE + MARGES

                            etat_partie = 'reglagePlateau'


                    elif etat_partie == 'reglagePlateau':
                        if parametre_bouton == 'ressources':
                            plateau.repartiRessources(True)
                        elif parametre_bouton == 'numeros':
                            plateau.placeNumeros(True)
                        elif parametre_bouton == 'ports':
                            plateau.placePorts(True)
                        else:
                            etat_partie = 'placement'
                            listeJoueursPlacement = listeJoueurs[:]
                            random.shuffle(listeJoueursPlacement)
                            listeJoueursPlacementInverse = listeJoueursPlacement[:]
                            listeJoueursPlacementInverse.reverse()
                            listeJoueursPlacement.extend(listeJoueursPlacementInverse)

        else:

            for joueur in listeJoueurs:
                joueur.affichePions()
                if joueur == monJoueur:
                    joueur.affichePrincipal()
                    if clic:
                        monJoueur.clic_sur_cartes(x_souris, y_souris)
                else:
                    joueur.afficheSecondaire()

            for bouton in listeBoutonsMonJoueurs:
                bouton.affiche()

            if etat_partie == 'placement':    # On fait comme si on pouvait placer tous les joueur
                joueurTour = listeJoueursPlacement[compteurJoueursPlacement]
                if joueurTour == monJoueur:
                    couleur = monJoueur.couleur
                    if couleur == BLANC:
                        couleur = NOIR
                    affiche_texte("Vous devez placer une {}.".format(nature_clic), X_CENTRE_AFFICHAGE_GAUCHE, Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)
                else:
                    couleur = joueurTour.couleur
                    if couleur == BLANC:
                        couleur = NOIR
                    affiche_texte("C'est aux {} de placer une {}.".format(joueurTour.nom, nature_clic), X_CENTRE_AFFICHAGE_GAUCHE, Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)

                if clic:
                    if nature_clic == 'colonie':
                        sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                        if sommet != None:
                            if plateau.placement_colonie_possible(sommet):
                                c = Colonie(joueurTour, sommet)
                                joueurTour.listeColonies.append(c)
                                if compteurJoueursPlacement < len(listeJoueursPlacement)/2:
                                    plateau.donne_ressource_premiere_colonie(c)
                                nature_clic = 'route'

                    elif nature_clic == 'route':
                        arete = plateau.clic_sur_aretes(x_souris, y_souris)
                        if arete != None:
                            if plateau.placement_route_possible(arete, joueurTour):
                                joueurTour.listeRoutes.append(Route(joueurTour, arete))
                                compteurJoueursPlacement += 1
                                nature_clic = 'colonie'
                                if compteurJoueursPlacement >= len(listeJoueursPlacement):
                                    etat_partie = 'jeu'
                                    nature_clic = None

            elif etat_partie == 'jeu':          # On fait comme si c'était toujours à nous de jouer

                m = int((HAUTEUR_BANDEAU_ACTIONS - TAILLE_DES) / 2)
                affiche_de(MARGES + m, 2 * MARGES + HAUTEUR_TITRE + m, TAILLE_DES, int(TAILLE_DES / 12), int(TAILLE_DES / 4), nb_de1)
                affiche_de(MARGES + 2 * m + TAILLE_DES, 2 * MARGES + HAUTEUR_TITRE + m, TAILLE_DES, int(TAILLE_DES / 12), int(TAILLE_DES / 4), nb_de2)

                if sous_partie_jeu == 'des':
                    if nb_de1 == 0:
                        boutonLancerDes.affiche()
                        if clic:
                            if boutonLancerDes.clic(x_souris, y_souris):
                                nb_de1 = random.randint(1, 6)
                                nb_de2 = random.randint(1, 6)
                                monJoueur.deselection_cartes()
                                if nb_de1 + nb_de2 == 7:
                                    voleur_etape = 0

                    else:
                        if nb_de1 + nb_de2 == 7:
                            if voleur_etape == 0:
                                if monJoueur.compte_nb_cartes() <= 7:
                                    voleur_etape += 1
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
                                                    for sommet in tuile.listeSommets:
                                                        if sommet.contenu != None:
                                                            if sommet.contenu.joueur.compte_nb_cartes() != 0 and sommet.contenu.joueur != monJoueur:
                                                                sous_partie_jeu = 'des'

                            else:
                                affiche_texte('Vous devez voler une carte.', X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)
                                if clic:
                                    for joueur in listeJoueurs:
                                        if joueur != monJoueur:
                                            if joueur.clicCarteSecondaire(x_souris, y_souris):
                                                listeJoueursPossibles = []
                                                for sommet in plateau.renvoie_tuile_voleur().listeSommets:
                                                    if sommet.contenu != None:
                                                        listeJoueursPossibles.append(sommet.contenu.joueur)
                                                if joueur.compte_nb_cartes() != 0 and joueur in listeJoueursPossibles:
                                                    carte = joueur.carte_au_hasard()
                                                    if carte != None:
                                                        carte.joueur = monJoueur
                                                        joueur.dictionnaireCartesRessources[carte.ressource].remove(carte)
                                                        monJoueur.dictionnaireCartesRessources[carte.ressource].append(carte)
                                                        sous_partie_jeu = 'jeu'

                        else:
                            boutonRecupererRessources.affiche()
                            if clic:
                                if boutonRecupererRessources.clic(x_souris, y_souris):
                                    plateau.donne_ressource_des(nb_de1 + nb_de2)
                                    sous_partie_jeu = 'jeu'

                # elif sous_partie_jeu == 'echanges':
                #     boutonFinEchanges.affiche()
                #     # TODO
                #     if clic:
                #         if boutonFinEchanges.clic(x_souris, y_souris):
                #             sous_partie_jeu = 'constructions'

                elif sous_partie_jeu == 'jeu':
                    boutonFinTour.affiche()
                    if clic:
                        if boutonFinTour.clic(x_souris, y_souris):
                            sous_partie_jeu = 'des'
                            nb_de1 = 0
                            nb_de2 = 0

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

                                    else:
                                        prix = []
                                        if nature_clic == 'colonie':
                                            prix = PRIX_COLONIE
                                        elif nature_clic == 'route':
                                            prix = PRIX_ROUTE
                                        elif nature_clic == 'ville':
                                            prix = PRIX_VILLE
                                        monJoueur.rendCarteConstruction(prix)
                                        nature_clic = None
                                        bouton.selectionner = False

                        # for bouton in listeBoutonsMonJoueurs:
                        #     if bouton.clic(x_souris, y_souris):
                        #         if bouton.selectionner == False:
                        #             if nature_clic != None:
                        #                 for b in listeBoutonsMonJoueurs:
                        #                     if b.selectionner == True:
                        #                         plateau.rend_ressources(nature_clic, monJoueur)
                        #                         b.selectionner = False
                        #             bouton.selectionner = True
                        #             nature_clic = bouton.parametre
                        #             if plateau.prend_ressources(nature_clic, monJoueur) == False:
                        #                 nature_clic = None
                        #                 bouton.selectionner = False
                        #         else:
                        #             plateau.rend_ressources(nature_clic, monJoueur)
                        #             nature_clic = None
                        #             bouton.selectionner = False

                    if nature_clic == 'colonie':
                        if clic:
                            sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                            if sommet != None:
                                if plateau.placement_colonie_possible(sommet) and plateau.placement_colonie_possible2(sommet, monJoueur):
                                    monJoueur.listeColonies.append(Colonie(monJoueur, sommet))
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False

                    elif nature_clic == 'route':
                        if clic:
                            arete = plateau.clic_sur_aretes(x_souris, y_souris)
                            if arete != None:
                                if plateau.placement_route_possible(arete, monJoueur):
                                    monJoueur.listeRoutes.append(Route(monJoueur, arete))
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False

                    elif nature_clic == 'ville':
                        if clic:
                            sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                            if sommet != None:
                                if plateau.placement_ville_possible(sommet, monJoueur):
                                    monJoueur.listeVilles.append(Ville(monJoueur, sommet))
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False

            elif etat_partie == 'fin':
                pass

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
