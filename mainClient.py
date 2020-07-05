# coding: utf-8


from plateau import *
from messages import *
from stats import *
from outils import *

if __name__ == "__main__":
    port = 12800
    connexionServeur = ReseauClient(port)
    monPseudo = ''
    hote = ''
    ecran_login = Ecran_login()
    clic_up_down = 0
    listeJoueurs = []

    boutonQuitter = Bouton(LARGEUR - MARGES - LARGEUR_IMAGE_BOUTON_MESSAGES, MARGES,
                           'sauvegarde', image=IMAGE_BOUTON_QUITTER)

    while hote == '' or monPseudo == '':
        souris = pygame.mouse.get_pos()
        x_souris = souris[0]
        y_souris = souris[1]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                r = ecran_login.gere_clavier(event)
                if r is not None:
                    if monPseudo == '':
                        monPseudo = r
                        ecran_login.etape = 1
                        ecran_login.msg = ADRESSE_IP
                        ecran_login.ts = ecran_login.p.render(ecran_login.msg, True, NOIR)
                    else:
                        hote = r
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if clic_up_down == 1:
                if event.type == pygame.MOUSEBUTTONUP:
                    clic_up_down = 0
                    if boutonQuitter.clic(x_souris, y_souris):
                        pygame.quit()
                        exit(0)
                    r = ecran_login.clic(x_souris, y_souris)
                    if r is not None:
                        if monPseudo == '':
                            monPseudo = r
                            ecran_login.etape = 1
                            ecran_login.msg = ADRESSE_IP
                            ecran_login.ts = ecran_login.p.render(ecran_login.msg, True, NOIR)
                        else:
                            hote = r
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clic_up_down = 1

        ecran_login.affiche()
        boutonQuitter.affiche()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

        if hote != '':
            connexionServeur.adresse_ip = hote
            if not connexionServeur.login(monPseudo):
                hote = ''
                ecran_login.reessayer = True

    plateau = Plateau(X_PLATEAU, Y_PLATEAU)
    dic = connexionServeur.getConditionsInitJeu()
    plateauDump = dic['plateau']
    # print(dic['plateau'])
    plateau.update(plateauDump)
    listeCouleurs = dic['listeCouleurs']
    listePiocheCartesSpeciales = dic['listePiocheCartesSpeciales']

    etat_partie = 'attenteJoueur'
    while etat_partie == 'attenteJoueur':
        souris = pygame.mouse.get_pos()
        x_souris = souris[0]
        y_souris = souris[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if clic_up_down == 1:
                if event.type == pygame.MOUSEBUTTONUP:
                    clic_up_down = 0
                    if boutonQuitter.clic(x_souris, y_souris):
                        pygame.quit()
                        exit(0)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clic_up_down = 1

        affiche_ecran_principal('attenteJoueurs')
        plateau.affiche()
        rectangle(MARGES, 2 * MARGES + HAUTEUR_TITRE, X_PLATEAU - MARGES - MARGES_PLATEAU,
                  HAUTEUR - 3 * MARGES - HAUTEUR_TITRE)
        boutonQuitter.affiche()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

        r = connexionServeur.getListeJoueurs()
        if r is not False:
            listeJoueurs = []
            for i, pseudo in enumerate(r):
                listeJoueurs.append(Joueur(pseudo, listeCouleurs[i]))
            etat_partie = 'placement'

    listeCouleurJoueursPlacement = listeCouleurs
    listeCouleurJoueursPlacementInverse = listeCouleurJoueursPlacement[:]
    listeCouleurJoueursPlacementInverse.reverse()
    listeCouleurJoueursPlacement.extend(listeCouleurJoueursPlacementInverse)

    couleurJoueurTourJeu = listeCouleurJoueursPlacement[0]
    sous_partie_jeu = 'des'
    compteurJoueursPlacement = 0
    nb_de1 = 0
    nb_de2 = 0
    voleur_etape = 0
    nature_clic = 'colonie'
    carte_speciale = None
    etapeEtJoueurEchange = [0, None]
    listeMessages = []
    message_a_lire = 0
    continue_voleur = False

    monJoueur = None
    monNom = None
    maCouleur = None
    for j in listeJoueurs:
        if j.pseudo == monPseudo:
            monJoueur = j
            monNom = j.nom
            maCouleur = monJoueur.couleur

    listeYAffichageJoueursSecondaire = []

    id_villes_colonies = 0
    id_route = 0
    id_carte = 0
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
    clic = False
    fleche_droite = False
    fleche_gauche = False

    listeBoutonsMonJoueurs = []
    m = 8
    x = 2 * MARGES + HAUTEUR_CARRE_JOUEUR_SECONDAIRE
    y = 3 * MARGES + HAUTEUR_BANDEAU_ACTIONS + HAUTEUR_TITRE
    l = int((X_PLATEAU - MARGES_PLATEAU - 2 * MARGES - HAUTEUR_CARRE_JOUEUR_SECONDAIRE - 4 * m) / 3)
    listeBoutonsMonJoueurs.append(Bouton(x + m, y + Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL, 'construction', largeur=l,
                                         hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='Construction'))
    listeBoutonsMonJoueurs.append(Bouton(x + l + 2 * m, y + Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL, 'banque', largeur=l,
                                         hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='Banque'))
    listeBoutonsMonJoueurs.append(
        Bouton(x + 2 * l + 3 * m, y + Y_BOUTON_DANS_AFFICHAGE_PRINCIPAL, 'echanges', largeur=l,
               hauteur=HAUTEUR_BOUTON_DANS_AFFICHAGE_PRINCIPAL, texte='Echanges'))

    boutonLancerDes = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'des', largeur=250, hauteur=40,
                             texte='Lancer les dés', centrer=True)
    boutonRecupererRessources = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'ressource', largeur=250,
                                       hauteur=40, texte='Récupérer les ressources', centrer=True)
    boutonFinTour = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'fin_tour', largeur=250, hauteur=40,
                           texte='Fin du tour', centrer=True)
    boutonJeterCartes = Bouton(X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, 'jeter_cartes', largeur=250,
                               hauteur=40, texte='Jeter les cartes', centrer=True)

    boutonUtiliserCartesSpeciale = Bouton(int(2 * MARGES + HAUTEUR_CARRE_JOUEUR_SECONDAIRE + 126 + (
            X_PLATEAU - MARGES_PLATEAU - 2 * MARGES - HAUTEUR_CARRE_JOUEUR_SECONDAIRE - 126) / 2),
                                          HAUTEUR - MARGES - 20 - m, 'utiliser_carte_speciale', largeur=100, hauteur=40,
                                          texte='Dévoiler', centrer=True)
    boutonMessages = Bouton(X_PLATEAU - MARGES_PLATEAU + MARGES, MARGES, 'messages', image=IMAGE_BOUTON_MESSAGES)

    boutonSauvegarde = Bouton(LARGEUR - MARGES - LARGEUR_IMAGE_BOUTON_MESSAGES,
                              HAUTEUR - MARGES - HAUTEUR_IMAGE_BOUTON_MESSAGES,
                              'sauvegarde', image=IMAGE_BOUTON_SAUVEGARDE)

    for bouton in listeBoutonsMonJoueurs:
        if bouton.parametre == 'banque':
            fenetreBanque = Fenetre_banque(bouton.x + bouton.largeur, int(bouton.y + bouton.hauteur / 2))
        elif bouton.parametre == 'echanges':
            fenetreEchanges = Fenetre_echanges(bouton.x + bouton.largeur, int(bouton.y + bouton.hauteur / 2), monJoueur,
                                               listeJoueurs)

    ecranMessages = Messages(boutonMessages.x + LARGEUR_IMAGE_BOUTON_MESSAGES,
                             int(boutonMessages.y + HAUTEUR_IMAGE_BOUTON_MESSAGES / 2))

    stats = Stats([joueur.nom for joueur in listeJoueurs])

    while True:
        listeEvents = connexionServeur.regardeEvenementsNonFait()
        for event in listeEvents:
            eventPseudo = event[PARAM_PSEUDO]
            eventType = event[PARAM_TYPE]
            eventContenu = event[PARAM_CONTENU]
            eventInfo = event[PARAM_INFO]

            if eventType == TYPE_MSG_TUILE:
                for tuile in plateau.listeTuile:
                    if tuile.id == eventInfo:
                        tuile.voleur = eventContenu
                        break
            elif eventType == TYPE_MSG_SOMMET:
                for sommet in plateau.listeSommets:
                    if sommet.id == eventInfo:
                        sommet.contenu = eventContenu
                        break
            elif eventType == TYPE_MSG_ARETE:
                for arete in plateau.listeAretes:
                    if arete.id == eventInfo:
                        arete.contenu = eventContenu
                        break

            elif eventType == TYPE_MSG_CARTE:
                if eventInfo == 'select':
                    for joueur in listeJoueurs:
                        if eventContenu['ressource'] > 5:
                            for carte in joueur.listeCartesSpeciales:
                                if carte.id == eventContenu['id']:
                                    carte.selectionner = eventContenu['selectionner']
                                    carte.nouvelleCarte = eventContenu['nouvelleCarte']
                                    break
                        else:
                            for carte in joueur.dictionnaireCartesRessources[eventContenu['ressource']]:
                                if carte.id == eventContenu['id']:
                                    # carte = obj
                                    carte.selectionner = eventContenu['selectionner']
                                    break
                else:
                    obj = Carte(0, 0)
                    obj.__dict__.update(eventContenu)
                    for joueur in listeJoueurs:
                        if joueur.nom == eventInfo[0]:
                            existe = False
                            if obj.ressource > 5:
                                for carte in joueur.listeCartesSpeciales:
                                    if carte.id == obj.id:
                                        existe = True
                                        if eventInfo[1] == '-':
                                            joueur.listeCartesSpeciales.remove(carte)
                                        break
                                if not existe:
                                    if eventInfo[1] == '+':
                                        joueur.listeCartesSpeciales.append(obj)
                                        id_carte += 4
                            else:
                                for carte in joueur.dictionnaireCartesRessources[obj.ressource]:
                                    if carte.id == obj.id:
                                        existe = True
                                        if eventInfo[1] == '-':
                                            joueur.dictionnaireCartesRessources[obj.ressource].remove(carte)
                                if not existe:
                                    if eventInfo[1] == '+':
                                        joueur.dictionnaireCartesRessources[obj.ressource].append(obj)
                                        id_carte += 4
                            break
            elif eventType == TYPE_MSG_ROUTE:
                s = Sommet(0, 0, 0)
                a = Arete(0, s, s)
                obj = Route(0, None, a)
                obj.__dict__.update(eventContenu)
                for joueur in listeJoueurs:
                    if joueur.couleur == obj.couleur:
                        existe = False
                        for r in joueur.listeRoutes:
                            if r.id == obj.id:
                                existe = True
                                break
                        if not existe:
                            joueur.listeRoutes.append(obj)
                            id_route += 4
            elif eventType == TYPE_MSG_VILLE:
                s = Sommet(0, 0, 0)
                obj = Ville(0, None, s)
                obj.__dict__.update(eventContenu)
                for joueur in listeJoueurs:
                    if joueur.couleur == obj.couleur:
                        existe = False
                        for v in joueur.listeVilles:
                            if v.id == obj.id:
                                existe = True
                                break
                        if not existe:
                            joueur.listeVilles.append(obj)
                            id_villes_colonies += 4
            elif eventType == TYPE_MSG_COLONIE:
                s = Sommet(0, 0, 0)
                obj = Colonie(0, None, s)
                obj.__dict__.update(eventContenu)
                for joueur in listeJoueurs:
                    if joueur.couleur == obj.couleur:
                        existe = False
                        for colonie in joueur.listeColonies:
                            if colonie.id == obj.id:
                                existe = True
                                if eventInfo == '-':
                                    joueur.listeColonies.remove(colonie)
                                break
                        if not existe:
                            if eventInfo == '+':
                                joueur.listeColonies.append(obj)
                                id_villes_colonies += 4
            elif eventType == TYPE_MSG_ATTR_JOUEUR:
                joueur = None
                for j in listeJoueurs:
                    if j.nom == eventInfo[0]:
                        joueur = j
                parametre = eventInfo[1]
                if parametre == 'nbPointsDeVictoire':
                    joueur.nbPointsDeVictoire = eventContenu
                elif parametre == 'listeRessourcesPorts':
                    joueur.listeRessourcesPorts = eventContenu
                elif parametre == 'jeterCartes':
                    joueur.jeterCartes = eventContenu
                elif parametre == 'routeLaPlusLongue':
                    joueur.routeLaPlusLongue = eventContenu
                elif parametre == 'nbCartesChevaliersRetournees':
                    joueur.nbCartesChevaliersRetournees = eventContenu
                elif parametre == 'points3chevaliers':
                    joueur.points3chevaliers = eventContenu

            elif eventType == 'etat_partie':
                etat_partie = eventContenu
            elif eventType == 'listeCouleurJoueursPlacement':
                listeCouleurJoueursPlacement = eventContenu
            elif eventType == 'compteurJoueursPlacement':
                compteurJoueursPlacement = eventContenu
            elif eventType == 'couleurJoueurTourJeu':
                couleurJoueurTourJeu = eventContenu
            elif eventType == 'sous_partie_jeu':
                sous_partie_jeu = eventContenu
            elif eventType == 'nb_des':
                nb_de1, nb_de2 = eventContenu
                joueurTour = None
                for j in listeJoueurs:
                    if j.couleur == couleurJoueurTourJeu:
                        joueurTour = j
                if joueurTour is not None:
                    s = nb_de1 + nb_de2
                    if s > 0:
                        stats.ajouteNumero(joueurTour.nom, s)
            elif eventType == 'voleur_etape':
                voleur_etape = eventContenu
            elif eventType == 'nature_clic':
                nature_clic = eventContenu
            elif eventType == 'supr_listePiocheCartesSpeciales':
                del listePiocheCartesSpeciales[0]
            elif eventType == 'carte_speciale':
                carte_speciale = eventContenu
            elif eventType == 'etapeEtJoueurEchange':
                etapeEtJoueurEchange = eventContenu
            elif eventType == 'message':
                listeMessages.append(eventContenu)
                message_a_lire += 1

        for joueur in listeJoueurs:
            if joueur.couleur == maCouleur:
                monJoueur = joueur

        souris = pygame.mouse.get_pos()
        x_souris = souris[0]
        y_souris = souris[1]

        clic = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    fleche_droite = True
                elif event.key == pygame.K_LEFT:
                    fleche_gauche = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    fleche_droite = False
                elif event.key == pygame.K_LEFT:
                    fleche_gauche = False

            if boutonMessages.selectionner:
                r = ecranMessages.gere_clavier(event)
                if r is not None:
                    listeMessages.append([r, maCouleur])
                    connexionServeur.envoie_au_serveur('message', [r, maCouleur])

            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if clic_up_down == 1:
                if event.type == pygame.MOUSEBUTTONUP:
                    clic_up_down = 0
                    clic = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clic_up_down = 1

        if stats.bouton.selectionner:
            stats.gere_clavier(fleche_droite, fleche_gauche)

        affiche_ecran_principal(etat_partie)
        plateau.affiche()

        for joueur in listeJoueurs:
            joueur.afficheRoutes1()
        for joueur in listeJoueurs:
            joueur.afficheRoutes2()

        monJoueur.affichePrincipal()
        i = 0
        for joueur in listeJoueurs:
            joueur.afficheColoniesEtVilles()
            if joueur == monJoueur:
                if clic:
                    if etapeEtJoueurEchange[0] == 0 or \
                            (etapeEtJoueurEchange[0] == 1 and maCouleur != couleurJoueurTourJeu) or \
                            (etapeEtJoueurEchange[0] == 2 and maCouleur != couleurJoueurTourJeu and
                             etapeEtJoueurEchange[1] != monNom):
                        carte = monJoueur.clic_sur_cartes(x_souris, y_souris)
                        if carte != None:
                            connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, carte.__dict__, 'select')
                            for bouton in listeBoutonsMonJoueurs:
                                if bouton.parametre == 'banque':
                                    bouton.selectionner = False
                                elif bouton.parametre == 'echanges':
                                    if couleurJoueurTourJeu == maCouleur:
                                        fenetreEchanges.reinitialise(True)
                        if carte_speciale == None:
                            carte = monJoueur.clic_sur_cartes_speciales(x_souris, y_souris)
                            if carte != None:
                                connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, carte.__dict__, 'select')
            else:
                joueur.afficheSecondaire(listeYAffichageJoueursSecondaire[i])
                i += 1

        for bouton in listeBoutonsMonJoueurs:
            bouton.affiche()

        boutonSauvegarde.affiche()
        boutonMessages.affiche()
        boutonQuitter.affiche()
        stats.affiche()
        if message_a_lire >= 1 and not boutonMessages.selectionner:
            affiche_bulle(boutonMessages.x + boutonMessages.largeur, 14, 10, message_a_lire)
        if clic:
            if boutonSauvegarde.clic(x_souris, y_souris):
                connexionServeur.sauvegarde_partie()
            elif stats.clic(x_souris, y_souris):
                pass
            elif boutonQuitter.clic(x_souris, y_souris):
                pygame.quit()
                exit(0)
            elif boutonMessages.clic(x_souris, y_souris):
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
                    connexionServeur.envoie_au_serveur('message', [r, maCouleur])
                if x_souris > X_PLATEAU - MARGES_PLATEAU:
                    clic = False  # On peut surement mieux faire : C'est pour ne pas cliquer sur le plateau quand
                    # on est sur les messages...

        if etat_partie == 'placement':
            if listeCouleurJoueursPlacement[compteurJoueursPlacement] == maCouleur:
                couleur = maCouleur
                if couleur == BLANC:
                    couleur = NOIR
                affiche_texte(f'Vous devez placer une {nature_clic}.', X_CENTRE_AFFICHAGE_GAUCHE,
                              Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)

                if clic:
                    if nature_clic == 'colonie':
                        sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                        if sommet is not None:
                            if plateau.placement_colonie_possible(sommet):
                                c = Colonie(id_villes_colonies, maCouleur, sommet)
                                sommet.contenu = id_villes_colonies
                                id_villes_colonies += 4
                                monJoueur.nbPointsDeVictoire += 1
                                monJoueur.listeColonies.append(c)
                                connexionServeur.envoie_au_serveur(TYPE_MSG_COLONIE, c.__dict__, info='+')
                                connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                                   monJoueur.nbPointsDeVictoire,
                                                                   info=[monNom, 'nbPointsDeVictoire'])
                                if plateau.ajoute_si_port_creation_colonie(sommet, monJoueur):
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                                       monJoueur.listeRessourcesPorts,
                                                                       info=[monNom, 'listeRessourcesPorts'])
                                if compteurJoueursPlacement < len(listeCouleurJoueursPlacement) / 2:
                                    # Eventuellement l'inverse : ça dépend des règles
                                    id_carte = plateau.donne_ressource_premiere_colonie(c, monJoueur, id_carte,
                                                                                        connexionServeur)
                                nature_clic = 'route'

                                connexionServeur.envoie_au_serveur('nature_clic', nature_clic)
                                connexionServeur.envoie_au_serveur(TYPE_MSG_SOMMET, sommet.contenu, sommet.id)

                    elif nature_clic == 'route':
                        arete = plateau.clic_sur_aretes(x_souris, y_souris)
                        if arete is not None:
                            deuxieme_colonie = False
                            d_c = True
                            if compteurJoueursPlacement < len(listeCouleurJoueursPlacement) / 2:
                                d_c = False
                            if plateau.placement_route_possible(arete, monJoueur, deuxieme_colonie=d_c):
                                r = Route(id_route, maCouleur, arete)
                                arete.contenu = id_route
                                monJoueur.listeRoutes.append(r)
                                id_route += 4
                                connexionServeur.envoie_au_serveur(TYPE_MSG_ROUTE, r.__dict__)
                                compteurJoueursPlacement += 1
                                nature_clic = 'colonie'
                                if compteurJoueursPlacement >= len(listeCouleurJoueursPlacement):
                                    etat_partie = 'jeu'
                                    nature_clic = None

                                connexionServeur.envoie_au_serveur('nature_clic', nature_clic)
                                connexionServeur.envoie_au_serveur(TYPE_MSG_ARETE, arete.contenu, arete.id)
                                if etat_partie == 'jeu':
                                    connexionServeur.envoie_au_serveur('etat_partie', etat_partie)
                                else:
                                    connexionServeur.envoie_au_serveur('compteurJoueursPlacement',
                                                                       compteurJoueursPlacement)

            else:
                joueurTour = None
                for j in listeJoueurs:
                    if j.couleur == listeCouleurJoueursPlacement[compteurJoueursPlacement]:
                        joueurTour = j
                couleur = listeCouleurJoueursPlacement[compteurJoueursPlacement]
                if couleur == BLANC:
                    couleur = NOIR
                affiche_texte(f"C'est à {joueurTour.pseudo} de placer une {nature_clic}.", X_CENTRE_AFFICHAGE_GAUCHE,
                              Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur, centrer=True)

        elif etat_partie == 'jeu':

            m = int((HAUTEUR_BANDEAU_ACTIONS - TAILLE_DES) / 2)
            affiche_de(MARGES + m, 2 * MARGES + HAUTEUR_TITRE + m, TAILLE_DES, int(TAILLE_DES / 12),
                       int(TAILLE_DES / 4), nb_de1)
            affiche_de(MARGES + 2 * m + TAILLE_DES, 2 * MARGES + HAUTEUR_TITRE + m, TAILLE_DES, int(TAILLE_DES / 12),
                       int(TAILLE_DES / 4), nb_de2)

            if monJoueur.jeterCartes:
                nb_selec = monJoueur.compte_nb_cartes_selectionnees()
                nb_a_selec = math.floor(monJoueur.compte_nb_cartes() / 2)
                if nb_selec >= nb_a_selec:
                    boutonJeterCartes.affiche()
                    if nb_selec > nb_a_selec:
                        carte = monJoueur.clic_sur_cartes(x_souris, y_souris)
                        if carte != None:
                            connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, carte.__dict__, 'select')
                    elif clic:
                        if boutonJeterCartes.clic(x_souris, y_souris):
                            monJoueur.jeterCartes = False
                            connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR, monJoueur.jeterCartes,
                                                               info=[monNom, 'jeterCartes'])
                            monJoueur.suprimeCartesSelectionnes(connexionServeur)
                else:
                    affiche_texte(f"Vous devez jeter {math.floor(monJoueur.compte_nb_cartes() / 2)} cartes.",
                                  X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)

            if couleurJoueurTourJeu == maCouleur:
                if carte_speciale == None:
                    carte_speciale_selectionner = monJoueur.carteSpecialesSelectionner()
                    if carte_speciale_selectionner != None:
                        if (sous_partie_jeu != 'des' or (nb_de1 == 0 and nb_de2 == 0)) \
                                and not carte_speciale_selectionner.nouvelleCarte:
                            boutonUtiliserCartesSpeciale.affiche()
                            if clic:
                                if boutonUtiliserCartesSpeciale.clic(x_souris, y_souris):
                                    if carte_speciale_selectionner.ressource == POUVOIR_POINT_VICTOIRE:
                                        monJoueur.nbPointsDeVictoire += 1
                                        monJoueur.listeCartesSpeciales.remove(carte_speciale_selectionner)
                                        connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                                           monJoueur.nbPointsDeVictoire,
                                                                           info=[monNom, 'nbPointsDeVictoire'])
                                        connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE,
                                                                           carte_speciale_selectionner.__dict__,
                                                                           info=[monNom, '-'])
                                    else:
                                        carte_speciale = carte_speciale_selectionner.ressource
                                        if carte_speciale == POUVOIR_MONOPOLE:
                                            fenetreBanqueMonopole = Fenetre_banque(carte_speciale_selectionner.x_centre,
                                                                                   carte_speciale_selectionner.y_centre)
                                        elif carte_speciale == POUVOIR_RESSOURCES_GRATUITES:
                                            nb_ressources_prises = 0
                                            fenetreBanqueRessourceGratuite = Fenetre_banque(
                                                carte_speciale_selectionner.x_centre,
                                                carte_speciale_selectionner.y_centre)
                                        elif carte_speciale == POUVOIR_ROUTES_GRATUITES:
                                            nb_routes_consrtuites = 0
                                        elif carte_speciale == POUVOIR_CHEVALIER:
                                            voleur_etape = 0
                                            monJoueur.nbCartesChevaliersRetournees += 1
                                            connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                                               monJoueur.nbCartesChevaliersRetournees,
                                                                               info=[monNom,
                                                                                     'nbCartesChevaliersRetournees'])
                                            plateau.gere_points3chevaliers(monJoueur, listeJoueurs, connexionServeur)
                                            connexionServeur.envoie_au_serveur('voleur_etape', voleur_etape)
                                        connexionServeur.envoie_au_serveur('carte_speciale', carte_speciale)

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
                                            connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__,
                                                                               info=[j.nom, '-'])
                                        j.dictionnaireCartesRessources[ressource] = []
                                for carte in listeCarte:
                                    carte.selectionner = True
                                    monJoueur.dictionnaireCartesRessources[ressource].append(carte)
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, carte.__dict__,
                                                                       info=[monNom, '+'])
                                carte_speciale = None
                                c = monJoueur.carteSpecialesSelectionner()
                                monJoueur.listeCartesSpeciales.remove(c)
                                connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__, info=[monNom, '-'])
                                connexionServeur.envoie_au_serveur('carte_speciale', carte_speciale)

                    elif carte_speciale == POUVOIR_RESSOURCES_GRATUITES:
                        fenetreBanqueRessourceGratuite.affiche()
                        if clic:
                            ressource = fenetreBanqueRessourceGratuite.clicSurCarte(x_souris, y_souris)
                            if ressource != None:
                                nb_ressources_prises += 1
                                c = Carte(ressource, id_carte)
                                monJoueur.dictionnaireCartesRessources[ressource].append(c)
                                id_carte += 4
                                connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__, info=[monNom, '+'])
                                if nb_ressources_prises >= 2:
                                    carte_speciale = None
                                    c = monJoueur.carteSpecialesSelectionner()
                                    monJoueur.listeCartesSpeciales.remove(c)
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__, info=[monNom, '-'])
                                    connexionServeur.envoie_au_serveur('carte_speciale', carte_speciale)

                    elif carte_speciale == POUVOIR_ROUTES_GRATUITES:
                        if clic:
                            arete = plateau.clic_sur_aretes(x_souris, y_souris)
                            if arete != None:
                                if plateau.placement_route_possible(arete, monJoueur):
                                    r = Route(id_route, maCouleur, arete)
                                    arete.contenu = id_route
                                    monJoueur.listeRoutes.append(r)
                                    id_route += 4
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_ROUTE, r.__dict__)
                                    nb_routes_consrtuites += 1
                                    if nb_routes_consrtuites >= 2:
                                        carte_speciale = None
                                        c = monJoueur.carteSpecialesSelectionner()
                                        monJoueur.listeCartesSpeciales.remove(c)
                                        connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__,
                                                                           info=[monNom, '-'])
                                        connexionServeur.envoie_au_serveur('carte_speciale', carte_speciale)
                                    plateau.gere_route_la_plus_longue(monJoueur, listeJoueurs, connexionServeur)
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_ARETE, arete.contenu, arete.id)

                if sous_partie_jeu == 'des' or carte_speciale == POUVOIR_CHEVALIER:
                    if (nb_de1 == 0 or nb_de2 == 0) and carte_speciale != POUVOIR_CHEVALIER:
                        boutonLancerDes.affiche()
                        if clic:
                            if boutonLancerDes.clic(x_souris, y_souris):
                                for joueur in listeJoueurs:
                                    joueur.deselection_cartes(connexionServeur)
                                nb_de1 = random.randint(1, 6)
                                nb_de2 = random.randint(1, 6)
                                stats.ajouteNumero(monNom, nb_de1 + nb_de2)
                                connexionServeur.envoie_au_serveur('nb_des', (nb_de1, nb_de2))
                                if nb_de1 + nb_de2 == 7:
                                    voleur_etape = 0
                                    a = False
                                    for joueur in listeJoueurs:
                                        if joueur.compte_nb_cartes() > 7:
                                            joueur.jeterCartes = True
                                            connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR, joueur.jeterCartes,
                                                                               info=[joueur.nom, 'jeterCartes'])
                                            a = True
                                    if not a:
                                        voleur_etape = 1
                                    connexionServeur.envoie_au_serveur('voleur_etape', voleur_etape)

                    else:
                        if nb_de1 + nb_de2 == 7 or carte_speciale == POUVOIR_CHEVALIER:
                            if voleur_etape == 0:
                                if carte_speciale == POUVOIR_CHEVALIER:
                                    voleur_etape += 1
                                    connexionServeur.envoie_au_serveur('voleur_etape', voleur_etape)
                                else:
                                    l = []
                                    for joueur in listeJoueurs:
                                        if joueur.jeterCartes == True:
                                            l.append(joueur.pseudo)
                                    if l == []:
                                        voleur_etape += 1
                                        connexionServeur.envoie_au_serveur('voleur_etape', voleur_etape)
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
                                            affiche_texte(t, X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS,
                                                          None, 35, NOIR, centrer=True)

                            elif voleur_etape == 1:
                                affiche_texte('Vous devez déplacer le voleur.', X_CENTRE_BANDEAU_ACTIONS_DES,
                                              Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)
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
                                                            if monJoueur.getMesVilleOuColonie(sommet.contenu) is None:
                                                                for j in listeJoueurs:
                                                                    if j.getMesVilleOuColonie(
                                                                            sommet.contenu) is not None \
                                                                            and j.compte_nb_cartes() != 0:
                                                                        continue_voleur = True

                                                    connexionServeur.envoie_au_serveur('voleur_etape', voleur_etape)
                                                    connexionServeur.envoie_au_serveur(TYPE_MSG_TUILE, t.voleur, t.id)
                                                    connexionServeur.envoie_au_serveur(TYPE_MSG_TUILE, tuile.voleur,
                                                                                       tuile.id)

                            else:
                                affiche_texte('Vous devez voler une carte.', X_CENTRE_BANDEAU_ACTIONS_DES,
                                              Y_CENTRE_BANDEAU_ACTIONS, None, 35, NOIR, centrer=True)
                                if clic:
                                    i = 0
                                    for joueur in listeJoueurs:
                                        if joueur != monJoueur:
                                            if joueur.clicCarteSecondaire(x_souris, y_souris,
                                                                          listeYAffichageJoueursSecondaire[i]):
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
                                                        joueur.dictionnaireCartesRessources[carte.ressource].remove(
                                                            carte)
                                                        monJoueur.dictionnaireCartesRessources[carte.ressource].append(
                                                            carte)
                                                        connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE,
                                                                                           carte.__dict__,
                                                                                           info=[joueur.nom, '-'])
                                                        connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE,
                                                                                           carte.__dict__,
                                                                                           info=[monNom, '+'])
                                                        continue_voleur = False
                                            i += 1

                                if continue_voleur == False:
                                    if carte_speciale == POUVOIR_CHEVALIER:
                                        carte_speciale = None
                                        c = monJoueur.carteSpecialesSelectionner()
                                        monJoueur.listeCartesSpeciales.remove(c)
                                        connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__,
                                                                           info=[monNom, '-'])
                                        connexionServeur.envoie_au_serveur('carte_speciale', carte_speciale)
                                    else:
                                        sous_partie_jeu = 'jeu'
                                        connexionServeur.envoie_au_serveur('sous_partie_jeu', sous_partie_jeu)

                        else:
                            boutonRecupererRessources.affiche()
                            if clic:
                                if boutonRecupererRessources.clic(x_souris, y_souris):
                                    id_carte = plateau.donne_ressource_des(nb_de1 + nb_de2, listeJoueurs, id_carte,
                                                                           connexionServeur)
                                    sous_partie_jeu = 'jeu'
                                    connexionServeur.envoie_au_serveur('sous_partie_jeu', sous_partie_jeu)

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
                                        monJoueur.suprimeCartesSelectionnes(connexionServeur)
                                        c = Carte(ressource, id_carte)
                                        id_carte += 4
                                        monJoueur.dictionnaireCartesRessources[ressource].append(c)
                                        connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__,
                                                                           info=[monNom, '+'])
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
                                            joueurEchange.suprimeCartesSelectionnes(connexionServeur)
                                            l2 = monJoueur.cree_listeCartesSelectionnees()
                                            monJoueur.suprimeCartesSelectionnes(connexionServeur)
                                            for c in l1:
                                                monJoueur.dictionnaireCartesRessources[c.ressource].append(c)
                                                connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__,
                                                                                   info=[monNom, '+'])
                                            for c in l2:
                                                joueurEchange.dictionnaireCartesRessources[c.ressource].append(c)
                                                connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__,
                                                                                   info=[joueurEchange.nom, '+'])
                                            etapeEtJoueurEchange = [0, None]
                                            bouton.selectionner = False
                                            fenetreEchanges.reinitialise(False)
                                            connexionServeur.envoie_au_serveur('etapeEtJoueurEchange',
                                                                               etapeEtJoueurEchange)
                                        elif r == 'refuser':
                                            fenetreEchanges.etape = 1
                                            etapeEtJoueurEchange[0] = 1
                                            connexionServeur.envoie_au_serveur('etapeEtJoueurEchange',
                                                                               etapeEtJoueurEchange)
                                        else:
                                            etapeEtJoueurEchange = [1, r]
                                            connexionServeur.envoie_au_serveur('etapeEtJoueurEchange',
                                                                               etapeEtJoueurEchange)

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
                                        id_carte = monJoueur.rendCarteConstruction(prix, id_carte, connexionServeur)
                                        nature_clic = None
                                        bouton.selectionner = False

                            for carte in monJoueur.listeCartesSpeciales:
                                if carte.nouvelleCarte:
                                    carte.nouvelleCarte = False
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, carte.__dict__, 'select')

                            sous_partie_jeu = 'fin'
                            connexionServeur.envoie_au_serveur('sous_partie_jeu', sous_partie_jeu)

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
                                            elif sorted(listeRessourcesCartesSelctionees) == sorted(
                                                    PRIX_CARTE_SPECIALE) and len(listePiocheCartesSpeciales) > 0:
                                                c = Carte(listePiocheCartesSpeciales[0], id_carte, selectionner=False)
                                                id_carte += 4
                                                monJoueur.listeCartesSpeciales.append(c)
                                                connexionServeur.envoie_au_serveur(TYPE_MSG_CARTE, c.__dict__,
                                                                                   info=[monNom, '+'])
                                                del listePiocheCartesSpeciales[0]
                                                connexionServeur.envoie_au_serveur('supr_listePiocheCartesSpeciales',
                                                                                   None)
                                                monJoueur.suprimeCartesSelectionnes(connexionServeur)
                                            if nature_clic == None:
                                                bouton.selectionner = False
                                            else:
                                                monJoueur.suprimeCartesSelectionnes(connexionServeur)

                                        else:
                                            prix = []
                                            if nature_clic == 'colonie':
                                                prix = PRIX_COLONIE
                                            elif nature_clic == 'route':
                                                prix = PRIX_ROUTE
                                            elif nature_clic == 'ville':
                                                prix = PRIX_VILLE
                                            id_carte = monJoueur.rendCarteConstruction(prix, id_carte, connexionServeur)
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
                                                connexionServeur.envoie_au_serveur('etapeEtJoueurEchange',
                                                                                   etapeEtJoueurEchange)

                        if nature_clic == 'colonie':
                            sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                            if sommet != None:
                                if plateau.placement_colonie_possible(sommet) and plateau.placement_colonie_possible2(
                                        sommet, monJoueur):
                                    c = Colonie(id_villes_colonies, maCouleur, sommet)
                                    monJoueur.nbPointsDeVictoire += 1
                                    monJoueur.listeColonies.append(c)
                                    sommet.contenu = id_villes_colonies
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_COLONIE, c.__dict__, info='+')
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                                       monJoueur.nbPointsDeVictoire,
                                                                       info=[monNom, 'nbPointsDeVictoire'])
                                    id_villes_colonies += 4
                                    if plateau.ajoute_si_port_creation_colonie(sommet, monJoueur):
                                        connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                                           monJoueur.listeRessourcesPorts,
                                                                           info=[monNom, 'listeRessourcesPorts'])
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_SOMMET, sommet.contenu, sommet.id)
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner == True:
                                            bouton.selectionner = False

                        elif nature_clic == 'route':
                            arete = plateau.clic_sur_aretes(x_souris, y_souris)
                            if arete != None:
                                if plateau.placement_route_possible(arete, monJoueur):
                                    r = Route(id_route, maCouleur, arete)
                                    arete.contenu = id_route
                                    monJoueur.listeRoutes.append(r)
                                    id_route += 4
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_ROUTE, r.__dict__)
                                    plateau.gere_route_la_plus_longue(monJoueur, listeJoueurs, connexionServeur)
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_ARETE, arete.contenu, arete.id)
                                    nature_clic = None
                                    for bouton in listeBoutonsMonJoueurs:
                                        if bouton.selectionner:
                                            bouton.selectionner = False

                        elif nature_clic == 'ville':
                            sommet = plateau.clic_sur_sommets(x_souris, y_souris)
                            if sommet != None:
                                if plateau.placement_ville_possible(sommet, monJoueur):
                                    colonie = monJoueur.getMesVilleOuColonie(sommet.contenu)
                                    monJoueur.listeColonies.remove(colonie)
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_COLONIE, colonie.__dict__, info='-')
                                    v = Ville(id_villes_colonies, maCouleur, sommet)
                                    monJoueur.nbPointsDeVictoire += 1
                                    monJoueur.listeVilles.append(v)
                                    sommet.contenu = id_villes_colonies
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_VILLE, v.__dict__)
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_ATTR_JOUEUR,
                                                                       monJoueur.nbPointsDeVictoire,
                                                                       info=[monNom, 'nbPointsDeVictoire'])
                                    id_villes_colonies += 4
                                    connexionServeur.envoie_au_serveur(TYPE_MSG_SOMMET, sommet.contenu, sommet.id)
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

                    connexionServeur.envoie_au_serveur('nb_des', (nb_de1, nb_de2))
                    connexionServeur.envoie_au_serveur('sous_partie_jeu', sous_partie_jeu)
                    connexionServeur.envoie_au_serveur('couleurJoueurTourJeu', couleurJoueurTourJeu)

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
                            connexionServeur.envoie_au_serveur('etapeEtJoueurEchange', etapeEtJoueurEchange)
                        elif r == 'refuser':
                            etapeEtJoueurEchange = [0, None]
                            connexionServeur.envoie_au_serveur('etapeEtJoueurEchange', etapeEtJoueurEchange)

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
                            affiche_texte(t, X_CENTRE_BANDEAU_ACTIONS_DES, Y_CENTRE_BANDEAU_ACTIONS, None, 35, couleur,
                                          centrer=True)

            if monJoueur.nbPointsDeVictoire >= 10:
                etat_partie = 'fin'
                connexionServeur.envoie_au_serveur('etat_partie', etat_partie)

        else:
            if etat_partie == 'fin':
                if clic:
                    etat_partie = 'fin2'
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
                affiche_texte(str(monJoueur.nbPointsDeVictoire), int(LARGEUR / 2),
                              int(m + HAUTEUR_IMAGE_GRANDE_COURONNE / 2 + 27), None, 450, NOIR, centrer=True)
                affiche_texte(t, LARGEUR / 2, int(HAUTEUR - (HAUTEUR - m - HAUTEUR_IMAGE_GRANDE_COURONNE) / 2), None,
                              150,
                              c, centrer=True)

            elif etat_partie == 'fin2':
                pass

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
