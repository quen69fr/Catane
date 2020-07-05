# coding: utf-8



from plateau import *
from messages import *
from outils import *


if __name__=="__main__":
    port = 12800
    connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_serveur_done = False
    monPseudo = ''
    hote = ''
    # hote = raw_input('Adresse IP du serveur : ')
    ecran_login = Ecran_login()
    clic_up_down = 0
    while hote == '' or monPseudo == '':
        souris = pygame.mouse.get_pos()
        x_souris = souris[0]
        y_souris = souris[1]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                r = ecran_login.gere_clavier(event)
                if r != None:
                    if monPseudo == '':
                        monPseudo = r
                        ecran_login.etape = 1
                        ecran_login.msg = ''
                        ecran_login.ts = ecran_login.p.render(ecran_login.msg, True, NOIR)
                    else:
                        hote = r
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if clic_up_down == 1:
                if event.type == pygame.MOUSEBUTTONUP:
                    clic_up_down = 0
                    r = ecran_login.clic(x_souris, y_souris)
                    if r != None:
                        if monPseudo == '':
                            monPseudo = r
                            ecran_login.etape = 1
                            ecran_login.msg = ''
                            ecran_login.ts = ecran_login.p.render(ecran_login.msg, True, NOIR)
                        else:
                            hote = r
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clic_up_down = 1
                    
        ecran_login.affiche()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

        if hote != '':
            try:
                connexion_avec_serveur.connect((hote, port))
            except select.error:
                hote = ''
                ecran_login.reessayer = True
            else:
                connexion_avec_serveur_done = True
    if not connexion_avec_serveur_done:
        connexion_avec_serveur.connect((hote, port))

    if AFFICHAGE_MESSAGE:
        print("Connexion établie avec le serveur sur le port {}".format(port))

    message = connexion_avec_serveur.recv(16384)
    plateau = pickle.loads(message)
    if AFFICHAGE_MESSAGE:
        print(f'Plateau'.ljust(35) + f'  recu à {date_actuelle()},'.ljust(40) + f'longeur : {len(message)},'.ljust(20) + f'dumps : {message}')
    time.sleep(0.1)
    envoieAuServeur('pseudo', monPseudo, connexion_avec_serveur)

    etat_partie = 'attenteJoueur'

    affiche_ecran_principal('attenteJoueurs')
    plateau.affiche()
    rectangle(MARGES, 2 * MARGES + HAUTEUR_TITRE, X_PLATEAU - MARGES - MARGES_PLATEAU, HAUTEUR - 3 * MARGES - HAUTEUR_TITRE)
    pygame.display.update()

    message = connexion_avec_serveur.recv(16384)
    etat_partie, listeJoueurs, listeCouleurJoueursPlacement, compteurJoueursPlacement, couleurJoueurTourJeu, sous_partie_jeu, nb_de1, nb_de2, voleur_etape, nature_clic, listePiocheCartesSpeciales, carte_speciale, etapeEtJoueurEchange, listeMessages = pickle.loads(message)
    if AFFICHAGE_MESSAGE:
        print(f'Toute la partie'.ljust(35) + f'  recu à {date_actuelle()},'.ljust(40) + f'longeur : {len(message)},'.ljust(20) + f'dumps : {message}')

    monJoueur = None
    monNom = None
    maCouleur = None
    for j in listeJoueurs:
        if j.pseudo == monPseudo:
            monJoueur = j
            monNom = j.nom
            maCouleur = monJoueur.couleur

    listeYAffichageJoueursSecondaire = []

    y = 3 * MARGES + HAUTEUR_TITRE + HAUTEUR_BANDEAU_ACTIONS
    n = 0
    for joueur in listeJoueurs:
        if joueur != monJoueur:
            listeYAffichageJoueursSecondaire.append(y)
            y += HAUTEUR_CARRE_JOUEUR_SECONDAIRE + MARGES
            n += 1
        else:
            id_villes_colonies = n
            id_route = n
            id_carte = n

    clic_up_down = 0

    listeBoutonsMonJoueurs = []
    m = 8
    x = 2 * MARGES + HAUTEUR_CARRE_JOUEUR_SECONDAIRE
    y = 3 * MARGES + HAUTEUR_BANDEAU_ACTIONS + HAUTEUR_TITRE
    l = int((X_PLATEAU - MARGES_PLATEAU - 2 * MARGES - HAUTEUR_CARRE_JOUEUR_SECONDAIRE - 4 * m) / 3)
    listeBoutonsMonJoueurs.append(Bouton(x + m, y + Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL, 'construction', largeur=l, hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='Construction'))
    listeBoutonsMonJoueurs.append(Bouton(x + l + 2 * m, y + Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL, 'banque', largeur=l, hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='Banque'))
    listeBoutonsMonJoueurs.append(Bouton(x + 2 * l + 3 * m, y + Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL, 'echanges', largeur=l, hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='Echanges'))

    boutonLancerDes = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'des', largeur=250, hauteur=40, texte='Lancer les dés', centrer=True)
    boutonRecupererRessources = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'ressource', largeur=250, hauteur=40, texte='Récupérer les ressources', centrer=True)
    boutonFinTour = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'fin_tour', largeur=250, hauteur=40, texte='Fin du tour', centrer=True)
    boutonJeterCartes = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'jeter_cartes', largeur=250, hauteur=40, texte='Jeter les cartes', centrer=True)

    boutonUtiliserCartesSpeciale = Bouton(int(2 * MARGES + HAUTEUR_CARRE_JOUEUR_SECONDAIRE + 126 + (X_PLATEAU - MARGES_PLATEAU - 2 * MARGES - HAUTEUR_CARRE_JOUEUR_SECONDAIRE - 126) / 2), HAUTEUR - MARGES - 20 - m, 'utiliser_carte_speciale', largeur=100, hauteur=40, texte='Dévoiler', centrer=True)
    boutonMessages = Bouton(X_PLATEAU - MARGES_PLATEAU + MARGES, MARGES, 'messages', image=IMAGE_BOUTON_MESSAGES)

    for bouton in listeBoutonsMonJoueurs:
        if bouton.parametre == 'banque':
            fenetreBanque = Fenetre_banque(bouton.x + bouton.largeur, int(bouton.y + bouton.hauteur / 2))
        elif bouton.parametre == 'echanges':
            fenetreEchanges = Fenetre_echanges(bouton.x + bouton.largeur, int(bouton.y + bouton.hauteur / 2), monJoueur, listeJoueurs)

    ecranMessages = Messages(boutonMessages.x + LARGEUR_IMAGE_BOUTON_MESSAGES, int(boutonMessages.y + HAUTEUR_IMAGE_BOUTON_MESSAGES / 2))

    message_a_lire = 0
    message_tronque = b''

    if AFFICHAGE_MESSAGE:
        print()

    while True:
        try:
            liste_serveur, wlist, xlist = select.select([connexion_avec_serveur], [], [], 0.05)
        except select.error:
            pass
        else:
            for serveur in liste_serveur:
                msg_complet = serveur.recv(16384)
                if AFFICHAGE_MESSAGE:
                    print()
                    print(f'MESSAGE_COMPLET : recu à {date_actuelle()}'.ljust(56) + f'longeur : {len(msg_complet)},'.ljust(20) + f'dumps : {msg_complet}')
                split_messages, message_tronque = splitMessages(message_tronque + msg_complet)
                for message_client_dumps in split_messages:
                    try:
                        message_client = pickle.loads(message_client_dumps)
                    except select.error:
                        pass
                    else:
                        m = message_client[0]
                        if AFFICHAGE_MESSAGE:
                            print(f'          > {m}'.ljust(56) + f'longeur : {len(message_client_dumps)},'.ljust(20) + f'dumps : {message_client_dumps}')

                        if m == 'plateau':
                            obj = message_client[1]
                            if isinstance(obj, Plateau):
                                plateau = obj
                            elif isinstance(obj, Tuile):
                                for tuile in plateau.listeTuile:
                                    if tuile.id == obj.id:
                                        # tuile = obj
                                        tuile.voleur = obj.voleur
                            elif isinstance(obj, Sommet):
                                for sommet in plateau.listeSommets:
                                    if sommet.id == obj.id:
                                        # sommet = obj
                                        sommet.contenu = obj.contenu
                            elif isinstance(obj, Arete):
                                for arete in plateau.listeAretes:
                                    if arete.id == obj.id:
                                        # arete = obj
                                        arete.contenu = obj.contenu

                        elif m == 'joueur':
                            obj = message_client[1]
                            if isinstance(obj, Joueur):
                                for joueur in listeJoueurs:
                                    if joueur.couleur == obj.couleur:
                                        joueur = obj

                            elif isinstance(obj, Carte):
                                if len(message_client) == 2:
                                    for joueur in listeJoueurs:
                                        if obj.ressource > 5:
                                            for carte in joueur.listeCartesSpeciales:
                                                if carte.id == obj.id:
                                                    # carte = obj
                                                    carte.selectionner = obj.selectionner
                                                    carte.nouvelleCarte = obj.nouvelleCarte
                                                    break
                                        else:
                                            for carte in joueur.dictionnaireCartesRessources[obj.ressource]:
                                                if carte.id == obj.id:
                                                    # carte = obj
                                                    carte.selectionner = obj.selectionner
                                                    break


                                else:
                                    info = message_client[2]
                                    for joueur in listeJoueurs:
                                        if joueur.nom == info[0]:
                                            existe = False
                                            if obj.ressource > 5:
                                                for carte in joueur.listeCartesSpeciales:
                                                    if carte.id == obj.id:
                                                        existe = True
                                                        if info[1] == '-':
                                                            joueur.listeCartesSpeciales.remove(carte)
                                                        break
                                                if not existe:
                                                    if info[1] == '+':
                                                        joueur.listeCartesSpeciales.append(obj)
                                            else:
                                                for carte in joueur.dictionnaireCartesRessources[obj.ressource]:
                                                    if carte.id == obj.id:
                                                        existe = True
                                                        if info[1] == '-':
                                                            joueur.dictionnaireCartesRessources[obj.ressource].remove(carte)
                                                if not existe:
                                                    if info[1] == '+':
                                                        joueur.dictionnaireCartesRessources[obj.ressource].append(obj)
                                            break

                            elif isinstance(obj, Route):
                                for joueur in listeJoueurs:
                                    if joueur.couleur == obj.couleur:
                                        existe = False
                                        for r in joueur.listeRoutes:
                                            if r.id == obj.id:
                                                existe = True
                                                break
                                        if not existe:
                                            joueur.listeRoutes.append(obj)

                            elif isinstance(obj, Ville):
                                for joueur in listeJoueurs:
                                    if joueur.couleur == obj.couleur:
                                        existe = False
                                        for v in joueur.listeVilles:
                                            if v.id == obj.id:
                                                existe = True
                                                break
                                        if not existe:
                                            joueur.listeVilles.append(obj)

                            elif isinstance(obj, Colonie):
                                for joueur in listeJoueurs:
                                    if joueur.couleur == obj.couleur:
                                        existe = False
                                        for colonie in joueur.listeColonies:
                                            if colonie.id == obj.id:
                                                existe = True
                                                if message_client[2] == '-':
                                                    joueur.listeColonies.remove(colonie)
                                                break
                                        if not existe:
                                            if message_client[2] == '+':
                                                joueur.listeColonies.append(obj)

                            else:
                                joueur = None
                                for j in listeJoueurs:
                                    if j.nom == message_client[2][0]:
                                        joueur = j
                                parametre = message_client[2][1]
                                if parametre == 'nbPointsDeVictoire':
                                    joueur.nbPointsDeVictoire = obj
                                elif parametre == 'listeRessourcesPorts':
                                    joueur.listeRessourcesPorts = obj
                                elif parametre == 'jeterCartes':
                                    joueur.jeterCartes = obj
                                elif parametre == 'routeLaPlusLongue':
                                    joueur.routeLaPlusLongue = obj
                                elif parametre == 'nbCartesChevaliersRetournees':
                                    joueur.nbCartesChevaliersRetournees = obj
                                elif parametre == 'points3chevaliers':
                                    joueur.points3chevaliers = obj

                        elif m == 'etat_partie':
                            etat_partie = message_client[1]
                        elif m == 'listeCouleurJoueursPlacement':
                            listeCouleurJoueursPlacement = message_client[1]
                        elif m == 'compteurJoueursPlacement':
                            compteurJoueursPlacement = message_client[1]
                        elif m == 'couleurJoueurTourJeu':
                            couleurJoueurTourJeu = message_client[1]
                        elif m == 'sous_partie_jeu':
                            sous_partie_jeu = message_client[1]
                        elif m == 'nb_des':
                            nb_de1, nb_de2 = message_client[1]
                        elif m == 'voleur_etape':
                            voleur_etape = message_client[1]
                        elif m == 'nature_clic':
                            nature_clic = message_client[1]
                        elif m == 'supr_listePiocheCartesSpeciales':
                            del listePiocheCartesSpeciales[0]
                        elif m == 'carte_speciale':
                            carte_speciale = message_client[1]
                        elif m == 'etapeEtJoueurEchange':
                            etapeEtJoueurEchange = message_client[1]
                        elif m == 'message':
                            listeMessages.append(message_client[1])
                            message_a_lire += 1
                if AFFICHAGE_MESSAGE:
                    if message_tronque != b'':
                        print(f' tronqué  > {m}'.ljust(56) + f'longeur : {len(message_tronque)},'.ljust(20) + f'dumps : {message_tronque}')
                    print()

        for joueur in listeJoueurs:
            if joueur.couleur == maCouleur:
                monJoueur = joueur

        souris = pygame.mouse.get_pos()
        x_souris = souris[0]
        y_souris = souris[1]

        clic = False
        for event in pygame.event.get():
            tape_texte = False
            if boutonMessages.selectionner:
                r = ecranMessages.gere_clavier(event)
                if r != None:
                    listeMessages.append([r, maCouleur])
                    envoieAuServeur('message', [r, maCouleur], connexion_avec_serveur)
                    tape_texte = True

            if event.type == pygame.QUIT:
                connexion_avec_serveur.close()
                pygame.quit()
                exit(0)

            if clic_up_down == 1:
                if event.type == pygame.MOUSEBUTTONUP:
                    clic_up_down = 0
                    clic = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clic_up_down = 1

            if event.type == pygame.KEYDOWN and not tape_texte:
                # S
                if event.key == 115:
                    envoieAuServeur('sauv_plateau', plateau, connexion_avec_serveur)
                    envoieAuServeur('sauv_tout', (etat_partie, listeJoueurs, listeCouleurJoueursPlacement, compteurJoueursPlacement, couleurJoueurTourJeu, sous_partie_jeu, nb_de1, nb_de2, voleur_etape, nature_clic, listePiocheCartesSpeciales, carte_speciale,  etapeEtJoueurEchange, listeMessages), connexion_avec_serveur)

        affiche_ecran_principal(etat_partie)
        plateau.affiche()

        for joueur in listeJoueurs:
            joueur.afficheRoutes()

        monJoueur.affichePrincipal()
        i = 0
        for joueur in listeJoueurs:
            joueur.afficheColoniesEtVilles()
            if joueur == monJoueur:
                if clic:
                    if etapeEtJoueurEchange[0] == 0 or (etapeEtJoueurEchange[0] == 1 and maCouleur != couleurJoueurTourJeu) or (etapeEtJoueurEchange[0] == 2 and maCouleur != couleurJoueurTourJeu and etapeEtJoueurEchange[1] != monNom):
                        carte = monJoueur.clic_sur_cartes(x_souris, y_souris)
                        if carte != None:
                            envoieAuServeur('joueur', carte, connexion_avec_serveur)
                            for bouton in listeBoutonsMonJoueurs:
                                if bouton.parametre == 'banque':
                                    bouton.selectionner = False
                                elif bouton.parametre == 'echanges':
                                    if couleurJoueurTourJeu == maCouleur:
                                        fenetreEchanges.reinitialise(True)
                        if carte_speciale == None:
                            carte = monJoueur.clic_sur_cartes_speciales(x_souris, y_souris)
                            if carte != None:
                                envoieAuServeur('joueur', carte, connexion_avec_serveur)
            else:
                joueur.afficheSecondaire(listeYAffichageJoueursSecondaire[i])
                i += 1

        for bouton in listeBoutonsMonJoueurs:
            bouton.affiche()

        boutonMessages.affiche()
        if message_a_lire >= 1 and not boutonMessages.selectionner:
            affiche_bulle(boutonMessages.x + boutonMessages.largeur, 14, 10, message_a_lire)
        if clic:
            if boutonMessages.clic(x_souris, y_souris):
                if boutonMessages.selectionner:
                    boutonMessages.selectionner = False
                else:
                    boutonMessages.selectionner = True
                    ecranMessages.reinitialise()

        if boutonMessages.selectionner:
            ecranMessages.affiche(listeMessages, maCouleur)
            message_a_lire = 0
            if clic:
                r = ecranMessages.gere_clic(x_souris, y_souris)
                if r != None:
                    listeMessages.append([r, maCouleur])
                    envoieAuServeur('message', [r, maCouleur], connexion_avec_serveur)
                if x_souris > X_PLATEAU - MARGES_PLATEAU:
                    clic = False    # On peut surement mieux faire : C'est pour ne pas cliquer sur le plateau quand on est sur les messages...

        if etat_partie == 'placement':    # On fait comme si on pouvait placer tous les joueur

            if listeCouleurJoueursPlacement[compteurJoueursPlacement] == maCouleur:
                couleur = maCouleur
                if couleur == BLANC:
                    couleur = NOIR
                affiche_texte(f'Vous devez placer une {nature_clic}.', X_CENTRE_AFFICHAGE_GAUCHE, Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)

                if clic:
                    if nature_clic == 'colonie':
                        sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                        if sommet != None:
                            if plateau.placement_colonie_possible(sommet):
                                c = Colonie(id_villes_colonies, monJoueur, sommet)
                                id_villes_colonies += 4
                                monJoueur.listeColonies.append(c)
                                envoieAuServeur('joueur', c, connexion_avec_serveur, info='+')
                                envoieAuServeur('joueur', monJoueur.nbPointsDeVictoire, connexion_avec_serveur, info=[monNom, 'nbPointsDeVictoire'])
                                if plateau.ajoute_si_port_creation_colonie(sommet, monJoueur):
                                    envoieAuServeur('joueur', monJoueur.listeRessourcesPorts, connexion_avec_serveur, info=[monNom, 'listeRessourcesPorts'])
                                if compteurJoueursPlacement < len(listeCouleurJoueursPlacement) / 2:
                                    id_carte = plateau.donne_ressource_premiere_colonie(c, monJoueur, id_carte, connexion_avec_serveur)
                                nature_clic = 'route'

                                envoieAuServeur('nature_clic', nature_clic, connexion_avec_serveur)
                                envoieAuServeur('plateau', sommet, connexion_avec_serveur)

                    elif nature_clic == 'route':
                        arete = plateau.clic_sur_aretes(x_souris, y_souris)
                        if arete != None:
                            if plateau.placement_route_possible(arete, monJoueur):
                                r = Route(id_route, monJoueur, arete)
                                monJoueur.listeRoutes.append(r)
                                id_route += 4
                                envoieAuServeur('joueur', r, connexion_avec_serveur)
                                compteurJoueursPlacement += 1
                                nature_clic = 'colonie'
                                if compteurJoueursPlacement >= len(listeCouleurJoueursPlacement):
                                    etat_partie = 'jeu'
                                    nature_clic = None

                                envoieAuServeur('nature_clic', nature_clic, connexion_avec_serveur)
                                envoieAuServeur('plateau', arete, connexion_avec_serveur)
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
                affiche_texte(f"C'est à {joueurTour.pseudo} de placer une {nature_clic}.", X_CENTRE_AFFICHAGE_GAUCHE, Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)

        elif etat_partie == 'jeu':

            m = int((HAUTEUR_BANDEAU_ACTIONS - TAILLE_DES) / 2)
            affiche_de(MARGES + m, 2 * MARGES + HAUTEUR_TITRE + m, TAILLE_DES, int(TAILLE_DES / 12), int(TAILLE_DES / 4), nb_de1)
            affiche_de(MARGES + 2 * m + TAILLE_DES, 2 * MARGES + HAUTEUR_TITRE + m, TAILLE_DES, int(TAILLE_DES / 12), int(TAILLE_DES / 4), nb_de2)

            if monJoueur.jeterCartes == True:
                nb_selec = monJoueur.compte_nb_cartes_selectionnees()
                nb_a_selec = math.floor(monJoueur.compte_nb_cartes() / 2)
                if nb_selec >= nb_a_selec:
                    boutonJeterCartes.affiche()
                    if nb_selec > nb_a_selec:
                        carte = monJoueur.clic_sur_cartes(x_souris, y_souris)
                        if carte != None:
                            envoieAuServeur('joueur', carte, connexion_avec_serveur)
                    elif clic:
                        if boutonJeterCartes.clic(x_souris, y_souris):
                            monJoueur.jeterCartes = False
                            envoieAuServeur('joueur', monJoueur.jeterCartes, connexion_avec_serveur, info=[monNom, 'jeterCartes'])
                            monJoueur.suprimeCartesSelectionnes(connexion_avec_serveur)
                else:
                    affiche_texte(f"Vous devez jeter {math.floor(monJoueur.compte_nb_cartes() / 2)} cartes.", X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)

            if couleurJoueurTourJeu == maCouleur:
                if carte_speciale == None:
                    carte_speciale_selectionner = monJoueur.carteSpecialesSelectionner()
                    if carte_speciale_selectionner != None:
                        if (sous_partie_jeu != 'des' or (nb_de1 == 0 and nb_de2 == 0)) and not carte_speciale_selectionner.nouvelleCarte:
                            boutonUtiliserCartesSpeciale.affiche()
                            if clic:
                                if boutonUtiliserCartesSpeciale.clic(x_souris, y_souris):
                                    if carte_speciale_selectionner.ressource == POUVOIR_POINT_VICTOIRE:
                                        monJoueur.nbPointsDeVictoire += 1
                                        monJoueur.listeCartesSpeciales.remove(carte_speciale_selectionner)
                                        envoieAuServeur('joueur', monJoueur.nbPointsDeVictoire, connexion_avec_serveur, info=[monNom, 'nbPointsDeVictoire'])
                                        envoieAuServeur('joueur', carte_speciale_selectionner, connexion_avec_serveur, info=[monNom, '-'])
                                    else:
                                        carte_speciale = carte_speciale_selectionner.ressource
                                        if carte_speciale == POUVOIR_MONOPOLE:
                                            fenetreBanqueMonopole = Fenetre_banque(carte_speciale_selectionner.x_centre, carte_speciale_selectionner.y_centre)
                                        elif carte_speciale == POUVOIR_RESSOURCES_GRATUITES:
                                            nb_ressources_prises = 0
                                            fenetreBanqueRessourceGratuite = Fenetre_banque(carte_speciale_selectionner.x_centre, carte_speciale_selectionner.y_centre)
                                        elif carte_speciale == POUVOIR_ROUTES_GRATUITES:
                                            nb_routes_consrtuites = 0
                                        elif carte_speciale == POUVOIR_CHEVALIER:
                                            voleur_etape = 0
                                            monJoueur.nbCartesChevaliersRetournees += 1
                                            envoieAuServeur('joueur', monJoueur.nbCartesChevaliersRetournees, connexion_avec_serveur, info=[monNom, 'nbCartesChevaliersRetournees'])
                                            plateau.gere_points3chevaliers(monJoueur, listeJoueurs, connexion_avec_serveur)
                                            envoieAuServeur('voleur_etape', voleur_etape, connexion_avec_serveur)
                                        envoieAuServeur('carte_speciale', carte_speciale, connexion_avec_serveur)

                else:
                    if carte_speciale == POUVOIR_MONOPOLE:
                        fenetreBanqueMonopole.affiche()
                        if clic:
                            ressource = fenetreBanqueMonopole.clicSurCarte(x_souris, y_souris)
                            if ressource != None:
                                listeCarte = []
                                for j in listeJoueurs:
                                    if j != monJoueur:
                                        for c in j.dictionnaireCartesRessources[ressource]:
                                            listeCarte.append(c)
                                for j in listeJoueurs:
                                    if j != monJoueur:
                                        for c in j.dictionnaireCartesRessources[ressource]:
                                            envoieAuServeur('joueur', c, connexion_avec_serveur, info=[j.nom, '-'])
                                        j.dictionnaireCartesRessources[ressource] = []
                                for carte in listeCarte:
                                    carte.selectionner = True
                                    monJoueur.dictionnaireCartesRessources[ressource].append(carte)
                                    envoieAuServeur('joueur', carte, connexion_avec_serveur, info=[monNom, '+'])
                                carte_speciale = None
                                c = monJoueur.carteSpecialesSelectionner()
                                monJoueur.listeCartesSpeciales.remove(c)
                                envoieAuServeur('joueur', c, connexion_avec_serveur, info=[monNom, '-'])
                                envoieAuServeur('carte_speciale', carte_speciale, connexion_avec_serveur)

                    elif carte_speciale == POUVOIR_RESSOURCES_GRATUITES:
                        fenetreBanqueRessourceGratuite.affiche()
                        if clic:
                            ressource = fenetreBanqueRessourceGratuite.clicSurCarte(x_souris, y_souris)
                            if ressource != None:
                                nb_ressources_prises += 1
                                c = Carte(ressource, id_carte)
                                monJoueur.dictionnaireCartesRessources[ressource].append(c)
                                id_carte += 4
                                envoieAuServeur('joueur', c, connexion_avec_serveur, info=[monNom, '+'])
                                if nb_ressources_prises >= 2:
                                    carte_speciale = None
                                    c = monJoueur.carteSpecialesSelectionner()
                                    monJoueur.listeCartesSpeciales.remove(c)
                                    envoieAuServeur('joueur', c, connexion_avec_serveur, info=[monNom, '-'])
                                    envoieAuServeur('carte_speciale', carte_speciale, connexion_avec_serveur)

                    elif carte_speciale == POUVOIR_ROUTES_GRATUITES:
                        if clic:
                            arete = plateau.clic_sur_aretes(x_souris, y_souris)
                            if arete != None:
                                if plateau.placement_route_possible(arete, monJoueur):
                                    r = Route(id_route, monJoueur, arete)
                                    monJoueur.listeRoutes.append(r)
                                    id_route += 4
                                    envoieAuServeur('joueur', r, connexion_avec_serveur)
                                    nb_routes_consrtuites += 1
                                    if nb_routes_consrtuites >= 2:
                                        carte_speciale = None
                                        c = monJoueur.carteSpecialesSelectionner()
                                        monJoueur.listeCartesSpeciales.remove(c)
                                        envoieAuServeur('joueur', c, connexion_avec_serveur, info=[monNom, '-'])
                                        envoieAuServeur('carte_speciale', carte_speciale, connexion_avec_serveur)
                                    plateau.gere_route_la_plus_longue(monJoueur, listeJoueurs, connexion_avec_serveur)
                                    envoieAuServeur('plateau', arete, connexion_avec_serveur)

                if sous_partie_jeu == 'des' or carte_speciale == POUVOIR_CHEVALIER:
                    if (nb_de1 == 0 or nb_de2 == 0) and carte_speciale != POUVOIR_CHEVALIER:
                        boutonLancerDes.affiche()
                        if clic:
                            if boutonLancerDes.clic(x_souris, y_souris):
                                for joueur in listeJoueurs:
                                    joueur.deselection_cartes(connexion_avec_serveur)
                                nb_de1 = random.randint(1, 6)
                                nb_de2 = random.randint(1, 6)
                                envoieAuServeur('nb_des', (nb_de1, nb_de2), connexion_avec_serveur)
                                if nb_de1 + nb_de2 == 7:
                                    voleur_etape = 0
                                    a = False
                                    for joueur in listeJoueurs:
                                        if joueur.compte_nb_cartes() > 7:
                                            joueur.jeterCartes = True
                                            envoieAuServeur('joueur', joueur.jeterCartes, connexion_avec_serveur, info=[joueur.nom, 'jeterCartes'])
                                            a = True
                                    if not a:
                                        voleur_etape = 1
                                    envoieAuServeur('voleur_etape', voleur_etape, connexion_avec_serveur)

                    else:
                        if nb_de1 + nb_de2 == 7 or carte_speciale == POUVOIR_CHEVALIER:
                            if voleur_etape == 0:
                                if carte_speciale == POUVOIR_CHEVALIER:
                                    voleur_etape += 1
                                    envoieAuServeur('voleur_etape', voleur_etape, connexion_avec_serveur)
                                else:
                                    l = []
                                    for joueur in listeJoueurs:
                                        if joueur.jeterCartes == True:
                                            l.append(joueur.pseudo)
                                    if l == []:
                                        voleur_etape += 1
                                        envoieAuServeur('voleur_etape', voleur_etape, connexion_avec_serveur)
                                    else:
                                        if monPseudo not in l:
                                            t = ''
                                            for i in range(len(l)):
                                                t += l[i]
                                                if i == len(l) - 1:
                                                    t += ' '
                                                elif i == len(l) - 2:
                                                    t += ' et '
                                                else:
                                                    t += ', '
                                            if len(l) == 1:
                                                t += 'doit'
                                            else:
                                                t += 'doivent'
                                            t += ' jeter des cartes.'
                                            affiche_texte(t, X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)

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
                                                    continue_voleur = False
                                                    for idSommet in tuile.listeIdSommets:
                                                        sommet = plateau.getSommet(idSommet)
                                                        if sommet.contenu != None:
                                                            if monJoueur.getMesVilleOuColonie(sommet.contenu) == None:
                                                                for j in listeJoueurs:
                                                                    if j.getMesVilleOuColonie(sommet.contenu) != None and j.compte_nb_cartes() != 0:
                                                                        continue_voleur = True

                                                    envoieAuServeur('voleur_etape', voleur_etape, connexion_avec_serveur)
                                                    envoieAuServeur('plateau', t, connexion_avec_serveur)
                                                    envoieAuServeur('plateau', tuile, connexion_avec_serveur)

                            else:
                                affiche_texte('Vous devez voler une carte.', X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)
                                if clic:
                                    i = 0
                                    for joueur in listeJoueurs:
                                        if joueur != monJoueur:
                                            if joueur.clicCarteSecondaire(x_souris, y_souris, listeYAffichageJoueursSecondaire[i]):
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
                                                        envoieAuServeur('joueur', carte, connexion_avec_serveur, info=[joueur.nom, '-'])
                                                        envoieAuServeur('joueur', carte, connexion_avec_serveur, info=[monNom, '+'])
                                                        continue_voleur = False
                                            i += 1

                                if continue_voleur == False:
                                    if carte_speciale == POUVOIR_CHEVALIER:
                                        carte_speciale = None
                                        c = monJoueur.carteSpecialesSelectionner()
                                        monJoueur.listeCartesSpeciales.remove(c)
                                        envoieAuServeur('joueur', c, connexion_avec_serveur, info=[monNom, '-'])
                                        envoieAuServeur('carte_speciale', carte_speciale, connexion_avec_serveur)
                                    else:
                                        sous_partie_jeu = 'jeu'
                                        envoieAuServeur('sous_partie_jeu', sous_partie_jeu, connexion_avec_serveur)

                        else:
                            boutonRecupererRessources.affiche()
                            if clic:
                                if boutonRecupererRessources.clic(x_souris, y_souris):
                                    id_carte = plateau.donne_ressource_des(nb_de1 + nb_de2, listeJoueurs, id_carte, connexion_avec_serveur)
                                    sous_partie_jeu = 'jeu'
                                    envoieAuServeur('sous_partie_jeu', sous_partie_jeu, connexion_avec_serveur)

                elif sous_partie_jeu == 'jeu':
                    boutonFinTour.affiche()

                    clic_sur_banque = False
                    for bouton in listeBoutonsMonJoueurs:
                        if bouton.parametre == 'banque':
                            if bouton.selectionner:
                                fenetreBanque.affiche()
                                if clic:
                                    ressource = fenetreBanque.clicSurCarte(x_souris, y_souris)
                                    if ressource != None:
                                        monJoueur.suprimeCartesSelectionnes(connexion_avec_serveur)
                                        c = Carte(ressource, id_carte)
                                        id_carte += 4
                                        monJoueur.dictionnaireCartesRessources[ressource].append(c)
                                        envoieAuServeur('joueur', c, connexion_avec_serveur, info=[monNom, '+'])
                                        bouton.selectionner = False
                                        clic_sur_banque = True

                        elif bouton.parametre == 'echanges':
                            if bouton.selectionner:
                                if fenetreEchanges.etape != 0:
                                    if etapeEtJoueurEchange[0] == 0:
                                        fenetreEchanges.etape = 0
                                        for b in fenetreEchanges.listeBoutonJoueurs:
                                            b.selectionner = False
                                if fenetreEchanges.etape == 1:
                                    if etapeEtJoueurEchange[0] == 2:
                                        fenetreEchanges.etape = 2
                                joueurEchange = None
                                for j in listeJoueurs:
                                    if j.nom == etapeEtJoueurEchange[1]:
                                        joueurEchange = j
                                fenetreEchanges.affiche(monJoueur, joueurEchange)
                                if boutonMessages.selectionner:
                                    boutonMessages.selectionner = False
                                if clic:
                                    r = fenetreEchanges.clic(x_souris, y_souris)
                                    if r != None:
                                        if r == 'valider':
                                            joueurEchange = None
                                            for j in listeJoueurs:
                                                if j.nom == etapeEtJoueurEchange[1]:
                                                    joueurEchange = j
                                            l1 = joueurEchange.cree_listeCartesSelectionnees()
                                            joueurEchange.suprimeCartesSelectionnes(connexion_avec_serveur)
                                            l2 = monJoueur.cree_listeCartesSelectionnees()
                                            monJoueur.suprimeCartesSelectionnes(connexion_avec_serveur)
                                            for c in l1:
                                                monJoueur.dictionnaireCartesRessources[c.ressource].append(c)
                                                envoieAuServeur('joueur', c, connexion_avec_serveur, info=[monNom, '+'])
                                            for c in l2:
                                                joueurEchange.dictionnaireCartesRessources[c.ressource].append(c)
                                                envoieAuServeur('joueur', c, connexion_avec_serveur, info=[joueurEchange.nom, '+'])
                                            etapeEtJoueurEchange = [0, None]
                                            bouton.selectionner = False
                                            fenetreEchanges.reinitialise(False)
                                            envoieAuServeur('etapeEtJoueurEchange', etapeEtJoueurEchange, connexion_avec_serveur)
                                        elif r == 'refuser':
                                            fenetreEchanges.etape = 1
                                            etapeEtJoueurEchange[0] = 1
                                            envoieAuServeur('etapeEtJoueurEchange', etapeEtJoueurEchange, connexion_avec_serveur)
                                        else:
                                            etapeEtJoueurEchange = [1, r]
                                            envoieAuServeur('etapeEtJoueurEchange', etapeEtJoueurEchange, connexion_avec_serveur)

                            else:
                                fenetreEchanges.principal = False

                    if clic:
                        if boutonFinTour.clic(x_souris, y_souris):
                            for bouton in listeBoutonsMonJoueurs:
                                if bouton.selectionner == True:
                                    bouton.selectionner = False
                                    if bouton.parametre == 'construction':
                                        prix = []
                                        if nature_clic == 'colonie':
                                            prix = PRIX_COLONIE
                                        elif nature_clic == 'route':
                                            prix = PRIX_ROUTE
                                        elif nature_clic == 'ville':
                                            prix = PRIX_VILLE
                                        id_carte = monJoueur.rendCarteConstruction(prix, id_carte, connexion_avec_serveur)
                                        nature_clic = None
                                        bouton.selectionner = False

                            for carte in monJoueur.listeCartesSpeciales:
                                if carte.nouvelleCarte:
                                    carte.nouvelleCarte = False
                                    envoieAuServeur('joueur', carte, connexion_avec_serveur)

                            sous_partie_jeu = 'fin'
                            envoieAuServeur('sous_partie_jeu', sous_partie_jeu, connexion_avec_serveur)

                        for bouton in listeBoutonsMonJoueurs:
                            if bouton.clic(x_souris, y_souris):
                                continuer = True
                                for b in listeBoutonsMonJoueurs:
                                    if b != bouton and b.selectionner:
                                        continuer = False
                                if continuer:
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
                                            elif sorted(listeRessourcesCartesSelctionees) == sorted(PRIX_CARTE_SPECIALE) and len(listePiocheCartesSpeciales) > 0:
                                                c = Carte(listePiocheCartesSpeciales[0], id_carte, selectionner=False)
                                                id_carte += 4
                                                monJoueur.listeCartesSpeciales.append(c)
                                                envoieAuServeur('joueur', c, connexion_avec_serveur, info=[monNom, '+'])
                                                del listePiocheCartesSpeciales[0]
                                                envoieAuServeur('supr_listePiocheCartesSpeciales', None, connexion_avec_serveur)
                                                monJoueur.suprimeCartesSelectionnes(connexion_avec_serveur)
                                            if nature_clic == None:
                                                bouton.selectionner = False
                                            else:
                                                monJoueur.suprimeCartesSelectionnes(connexion_avec_serveur)

                                        else:
                                            prix = []
                                            if nature_clic == 'colonie':
                                                prix = PRIX_COLONIE
                                            elif nature_clic == 'route':
                                                prix = PRIX_ROUTE
                                            elif nature_clic == 'ville':
                                                prix = PRIX_VILLE
                                            id_carte = monJoueur.rendCarteConstruction(prix, id_carte, connexion_avec_serveur)
                                            nature_clic = None
                                            bouton.selectionner = False

                                    elif bouton.parametre == 'banque':
                                        if bouton.selectionner == False:
                                            l = monJoueur.cree_listeRessourcesCartesSelectionnees()
                                            if len(l) == 4:
                                                if l[0] == l[1] == l[2] == l[3]:
                                                    bouton.selectionner = True
                                            elif PORT_3_CONTRE_1 in monJoueur.listeRessourcesPorts and len(l) == 3:
                                                if l[0] == l[1] == l[2]:
                                                    bouton.selectionner = True
                                            elif len(l) == 2:
                                                if l[0] == l[1] and l[0] in monJoueur.listeRessourcesPorts:
                                                    bouton.selectionner = True

                                        else:
                                            bouton.selectionner = False

                                    elif bouton.parametre == 'echanges':
                                        if clic_sur_banque == False:
                                            if bouton.selectionner == False:
                                                fenetreEchanges.reinitialise(True)
                                                bouton.selectionner = True
                                            else:
                                                bouton.selectionner = False
                                                fenetreEchanges.reinitialise(False)
                                                etapeEtJoueurEchange = [0, None]
                                                envoieAuServeur('etapeEtJoueurEchange', etapeEtJoueurEchange, connexion_avec_serveur)

                        if nature_clic == 'colonie':
                            sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                            if sommet != None:
                                if plateau.placement_colonie_possible(sommet) and plateau.placement_colonie_possible2(sommet, monJoueur):
                                    c = Colonie(id_villes_colonies, monJoueur, sommet)
                                    monJoueur.listeColonies.append(c)
                                    envoieAuServeur('joueur', c, connexion_avec_serveur, info='+')
                                    envoieAuServeur('joueur', monJoueur.nbPointsDeVictoire, connexion_avec_serveur, info=[monNom, 'nbPointsDeVictoire'])
                                    id_villes_colonies += 4
                                    if plateau.ajoute_si_port_creation_colonie(sommet, monJoueur):
                                        envoieAuServeur('joueur', monJoueur.listeRessourcesPorts, connexion_avec_serveur, info=[monNom, 'listeRessourcesPorts'])
                                    envoieAuServeur('plateau', sommet, connexion_avec_serveur)
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False

                        elif nature_clic == 'route':
                            arete = plateau.clic_sur_aretes(x_souris, y_souris)
                            if arete != None:
                                if plateau.placement_route_possible(arete, monJoueur):
                                    r = Route(id_route, monJoueur, arete)
                                    monJoueur.listeRoutes.append(r)
                                    id_route += 4
                                    envoieAuServeur('joueur', r, connexion_avec_serveur)
                                    plateau.gere_route_la_plus_longue(monJoueur, listeJoueurs, connexion_avec_serveur)
                                    envoieAuServeur('plateau', arete, connexion_avec_serveur)
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False

                        elif nature_clic == 'ville':
                            sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                            if sommet != None:
                                if plateau.placement_ville_possible(sommet, monJoueur):
                                    colonie = monJoueur.getMesVilleOuColonie(sommet.contenu)
                                    monJoueur.listeColonies.remove(colonie)
                                    envoieAuServeur('joueur', colonie, connexion_avec_serveur, info='-')
                                    v = Ville(id_villes_colonies, monJoueur, sommet)
                                    monJoueur.listeVilles.append(v)
                                    envoieAuServeur('joueur', v, connexion_avec_serveur)
                                    envoieAuServeur('joueur', monJoueur.nbPointsDeVictoire, connexion_avec_serveur, info=[monNom, 'nbPointsDeVictoire'])
                                    id_villes_colonies += 4
                                    envoieAuServeur('plateau', sommet, connexion_avec_serveur)
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

            else:
                if etapeEtJoueurEchange[1] == monNom and etapeEtJoueurEchange[0] == 1:
                    for j in listeJoueurs:
                        if j.couleur == couleurJoueurTourJeu:
                            joueurTour = j
                    fenetreEchanges.affiche(joueurTour, monJoueur)
                    if boutonMessages.selectionner:
                        boutonMessages.selectionner = False
                    if clic:
                        r = fenetreEchanges.clic(x_souris, y_souris)
                        if r == 'valider':
                            etapeEtJoueurEchange[0] = 2
                            fenetreEchanges.reinitialise(False)
                            envoieAuServeur('etapeEtJoueurEchange', etapeEtJoueurEchange, connexion_avec_serveur)
                        elif r == 'refuser':
                            etapeEtJoueurEchange = [0, None]
                            envoieAuServeur('etapeEtJoueurEchange', etapeEtJoueurEchange, connexion_avec_serveur)

                else:
                    fenetreEchanges.reinitialise(False)

                if not monJoueur.jeterCartes:
                    for j in listeJoueurs:
                        if j.couleur == couleurJoueurTourJeu:
                            couleur = couleurJoueurTourJeu
                            if couleur == BLANC:
                                couleur = NOIR
                            t = f"{j.pseudo} est en train de jouer."
                            if carte_speciale == POUVOIR_MONOPOLE:
                                t = 'MONOPOLE !'
                            elif carte_speciale == POUVOIR_CHEVALIER:
                                t = 'CHEVALIER !'
                            affiche_texte(t, X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)

            if monJoueur.nbPointsDeVictoire >= 10:
                etat_partie = 'fin'
                envoieAuServeur('etat_partie', etat_partie, connexion_avec_serveur)

        else:
            if monJoueur.nbPointsDeVictoire >= 10:
                t = 'Vous avez gagné !'
                c = maCouleur
            else:
                for joueur in listeJoueurs:
                    if joueur.nbPointsDeVictoire >= 10:
                        t = '{} a gagné !'.format(joueur.pseudo)
                        c = joueur.couleur
            if c == BLANC:
                c = NOIR

            SCREEN.blit(IMAGE_TRANSPARANTE, (0, 0))
            m = 10
            SCREEN.blit(IMAGE_GRANDE_COURONNE, (int(LARGEUR / 2 - LARGEUR_IMAGE_GRANDE_COURONNE / 2), m))
            affiche_texte(str(monJoueur.nbPointsDeVictoire), int(LARGEUR / 2), int(m + HAUTEUR_IMAGE_GRANDE_COURONNE / 2 + 27), None, 450, NOIR, centrer=True)
            affiche_texte(t, LARGEUR / 2, int(HAUTEUR - (HAUTEUR - m - HAUTEUR_IMAGE_GRANDE_COURONNE) / 2), None, 150, c, centrer=True)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)