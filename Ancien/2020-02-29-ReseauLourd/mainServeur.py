# coding: utf-8

from plateau import *
from outils import *


if __name__=="__main__":

    hote = ''
    port = 12800
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, port))

    plateau = Plateau(X_PLATEAU, Y_PLATEAU)
    plateau.creationPlateau()
    plateau.preparePlateau()
    ecran_reglage = Ecran_reglages()
    etat_partie = 'reglagesJoueurs'
    sous_partie_jeu = 'des'
    listeJoueurs = []
    clic_up_down = 0
    listeCouleurJoueursPlacement = []
    compteurJoueursPlacement = 0
    couleurJoueurTourJeu = None
    nb_de1 = 0
    nb_de2 = 0
    voleur_etape = 0
    nature_clic = 'colonie'

    liste_client = []

    while True:

        if etat_partie == 'reglagesJoueurs' or etat_partie == 'reglagePlateau':
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

                            etat_partie = 'reglagePlateau'


                    elif etat_partie == 'reglagePlateau':
                        if parametre_bouton == 'ressources':
                            plateau.repartiRessources(True)
                        elif parametre_bouton == 'numeros':
                            plateau.placeNumeros(True)
                        elif parametre_bouton == 'ports':
                            plateau.placePorts(True)
                        else:
                            etat_partie = 'attenteJoueurs'
                            random.shuffle(listeJoueurs)
                            listeCouleurJoueursPlacement = []
                            for joueur in listeJoueurs:
                                listeCouleurJoueursPlacement.append(joueur.couleur)
                            listeCouleurJoueursPlacementInverse = listeCouleurJoueursPlacement[:]
                            listeCouleurJoueursPlacementInverse.reverse()
                            listeCouleurJoueursPlacement.extend(listeCouleurJoueursPlacementInverse)
                            couleurJoueurTourJeu = listeJoueurs[0].couleur
                            connexion_principale.listen(5)
                            print("Le serveur écoute à présent sur le port {}".format(port))
                            pygame.quit()
                            continue

            pygame.display.update()
            pygame.time.Clock().tick(FPS)

        elif etat_partie == 'attenteJoueurs':

            connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
            for connexion in connexions_demandees:
                connexion_avec_client, infos_connexion = connexion.accept()
                liste_client.append(connexion_avec_client)

            if len(listeJoueurs) == len(liste_client):
                etat_partie = 'placement'
                random.shuffle(liste_client)
                for i in range(len(liste_client)):
                    liste_client[i].send(pickle.dumps(listeJoueurs[i]))

        else:
            clients_a_lire = []
            try:
                clients_a_lire, wlist, xlist = select.select(liste_client, [], [], 0.05)
            except select.error:
                pass
            else:
                for client in clients_a_lire:
                    message_client_dumps = client.recv(102400)
                    #print('Recu à', date_actuelle(), 'de', client,':      longeur :', len(message_client),'message : ', message_client)
                    message_client = pickle.loads(message_client_dumps)
                    if isinstance(message_client, list):
                        message_client_modif = True
                        print(message_client[0], '        recu à', date_actuelle(), ', longeur :', len(message_client_dumps), ', dumps :', message_client_dumps)
                        m = message_client[0]
                    else:
                        message_client_modif = False
                        m = message_client

                    if m == 'plateau':
                        if message_client_modif:
                            plateau = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(plateau))
                    elif m == 'etat_partie':
                        if message_client_modif:
                            etat_partie = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(etat_partie))
                    elif m == 'listeJoueurs':
                        if message_client_modif:
                            listeJoueurs = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(listeJoueurs))
                    elif m == 'listeJoueurs.bleus':
                        if message_client_modif:
                            for i in range(len(listeJoueurs)):
                                if listeJoueurs[i].nom == 'bleus':
                                    listeJoueurs[i] = message_client[1]
                                    # client.send('1')
                    elif m == 'listeJoueurs.oranges':
                        if message_client_modif:
                            for i in range(len(listeJoueurs)):
                                if listeJoueurs[i].nom == 'oranges':
                                    listeJoueurs[i] = message_client[1]
                                    # client.send('1')
                    elif m == 'listeJoueurs.rouges':
                        if message_client_modif:
                            for i in range(len(listeJoueurs)):
                                if listeJoueurs[i].nom == 'rouges':
                                    listeJoueurs[i] = message_client[1]
                                    # client.send('1')
                    elif m == 'listeJoueurs.blancs':
                        if message_client_modif:
                            for i in range(len(listeJoueurs)):
                                if listeJoueurs[i].nom == 'blancs':
                                    listeJoueurs[i] = message_client[1]
                                    # client.send('1')
                    elif m == 'listeCouleurJoueursPlacement':
                        if message_client_modif:
                            listeCouleurJoueursPlacement = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(listeCouleurJoueursPlacement))
                    elif m == 'compteurJoueursPlacement':
                        if message_client_modif:
                            compteurJoueursPlacement = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(compteurJoueursPlacement))
                    elif m == 'couleurJoueurTourJeu':
                        if message_client_modif:
                            couleurJoueurTourJeu = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(couleurJoueurTourJeu))
                    elif m == 'sous_partie_jeu':
                        if message_client_modif:
                            sous_partie_jeu = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(sous_partie_jeu))
                    elif m == 'nb_des':
                        if message_client_modif:
                            nb_de1, nb_de2 = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps((nb_de1, nb_de2)))
                    elif m == 'voleur_etape':
                        if message_client_modif:
                            voleur_etape = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(voleur_etape))
                    elif m == 'nature_clic':
                        if message_client_modif:
                            nature_clic = message_client[1]
                            # client.send('1')
                        else:
                            client.send(pickle.dumps(nature_clic))
