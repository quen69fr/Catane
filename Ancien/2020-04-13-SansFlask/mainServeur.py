# coding: utf-8

from plateau import *
from outils import *

MODE_SAUVEGARDE = False

if __name__ == "__main__":
    message_type_sauvegarde = False
    message_tronque = b''
    if MODE_SAUVEGARDE:
        fichier_sauv_message_plateau = open("sauvegarde_plateau.bin", "rb")
        fichier_sauv_message_tout = open("sauvegarde_tout.bin", "rb")
        sauv_message_plateau = fichier_sauv_message_plateau.read()
        print(sauv_message_plateau)
        sauv_message_tout = fichier_sauv_message_tout.read()
        print(sauv_message_tout)

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
    listePiocheCartesSpeciales = LISTE_PIOCHE_CARTE_SPECIALE
    random.shuffle(listePiocheCartesSpeciales)
    carte_speciale = None
    etapeEtJoueurEchange = [0, None]
    listeMessages = []

    liste_client = []
    liste_clients_pseudos = []

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
                if etat_partie == 'reglagePlateau':
                    r1, r2 = ecran_reglage.clic_plateau(plateau.clic_sur_tuile(x_souris, y_souris), plateau.clic_sur_aretes(x_souris, y_souris))
                    if r1 != None and r2 != None:
                        for c in ecran_reglage.listeCasesACaucherReglagePlateau:
                            if c.etat == 1:
                                if isinstance(r1, Tuile) and isinstance(r2, Tuile):
                                    if c.parametre == 'ressources':
                                        ressource1 = r1.ressource
                                        r1.ressource = r2.ressource
                                        r2.ressource = ressource1
                                    elif c.parametre == 'numeros':
                                        numero1 = r1.numero
                                        r1.numero = r2.numero
                                        r2.numero = numero1
                                else:
                                    if c.parametre == 'ports':
                                        ressource_port1 = r1.ressource_port
                                        r1.ressource_port = r2.ressource_port
                                        r2.ressource_port = ressource_port1


                parametre_bouton = ecran_reglage.clic_bouton(etat_partie, x_souris, y_souris)

                if parametre_bouton != None:

                    if etat_partie == 'reglagesJoueurs':
                        if parametre_bouton == 'valider':
                            for bouton in ecran_reglage.listeBoutonsJoueurs:
                                if bouton.selectionner == True:
                                    c = BLEU
                                    if bouton.parametre == 'rouge':
                                        c = ROUGE
                                    elif bouton.parametre == 'blanc':
                                        c = BLANC
                                    elif bouton.parametre == 'orange':
                                        c = ORANGE
                                    listeJoueurs.append(Joueur(c))

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
                            connexion_principale.listen(10)
                            if AFFICHAGE_MESSAGE:
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
                if MODE_SAUVEGARDE:
                    message = sauv_message_plateau
                else:
                    message = pickle.dumps(plateau)
                connexion_avec_client.send(message)
                if AFFICHAGE_MESSAGE:
                    print(f'Plateau'.ljust(35) + f'envoyé à {date_actuelle()},'.ljust(40) + f'longeur : {len(message)},'.ljust(20) + f'dumps : {message}')

                m = connexion_avec_client.recv(16384)
                if AFFICHAGE_MESSAGE:
                    print(f'Pseudo du client'.ljust(35) + f'  recu à {date_actuelle()},'.ljust(40) + f'longeur : {len(m)},'.ljust(20) + f'dumps : {m}')
                lm = pickle.loads(m)
                pseudo = lm[1]

                liste_clients_pseudos.append([connexion_avec_client, pseudo])


            if len(listeJoueurs) == len(liste_client):
                etat_partie = 'placement'
                random.shuffle(liste_clients_pseudos)
                for i in range(len(liste_client)):
                    clienti = liste_clients_pseudos[i][0]
                    listeJoueurs[i].pseudo = liste_clients_pseudos[i][1]
                for client, _ in liste_clients_pseudos:
                    if MODE_SAUVEGARDE:
                        message = sauv_message_tout
                    else:
                        message = pickle.dumps((etat_partie, listeJoueurs, listeCouleurJoueursPlacement, compteurJoueursPlacement, couleurJoueurTourJeu, sous_partie_jeu, nb_de1, nb_de2, voleur_etape, nature_clic, listePiocheCartesSpeciales, carte_speciale, etapeEtJoueurEchange, listeMessages))
                    client.send(message)
                    if AFFICHAGE_MESSAGE:
                        print(f'Toute la partie'.ljust(35) + f'envoyé à {date_actuelle()},'.ljust(40) + f'longeur : {len(message)},'.ljust(20) + f'dumps : {message}')
                    time.sleep(TEMPO_MSG)

        else:
            clients_a_lire = []
            try:
                clients_a_lire, wlist, xlist = select.select(liste_client, [], [], 0.05)
            except select.error:
                pass
            else:
                if message_type_sauvegarde:
                    for client in clients_a_lire:
                        msg_complet = client.recv(16384)
                        if msg_complet == b'':
                            liste_client.remove(client)
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
                                if m == 'sauv_plateau':
                                    print(pickle.dumps(message_client[1]))
                                    fichier_sauv_message_plateau = open("sauvegarde_plateau.bin", "wb")
                                    fichier_sauv_message_plateau.write(pickle.dumps(message_client[1]))
                                    fichier_sauv_message_plateau.close()
                                elif m == 'sauv_tout':
                                    print(pickle.dumps(message_client[1]))
                                    fichier_sauv_message_tout = open("sauvegarde_tout.bin", "wb")
                                    fichier_sauv_message_tout.write(pickle.dumps(message_client[1]))
                                    fichier_sauv_message_tout.close()

                else:
                    try:
                        for client in clients_a_lire:
                            msg_complet = client.recv(16384)
                            if AFFICHAGE_MESSAGE:
                                print()
                                print(f'Recu à {date_actuelle()},'.ljust(46) + f'longeur : {len(msg_complet)},'.ljust(20) + f'dumps : {msg_complet}')
                            if msg_complet == b'':
                                liste_client.remove(client)
                                message_type_sauvegarde = True
                                print("================== ERREUR SAUVEGARDE ENCLENCHEE ==================")
                            else:
                                for c in liste_client:
                                    if c != client:
                                        c.send(msg_complet)
                                        if AFFICHAGE_MESSAGE:
                                            print(f'  --> envoyé à {date_actuelle()},'.ljust(46) + f'longeur : {len(msg_complet)},'.ljust(20) + f'dumps : {msg_complet}')
                                        time.sleep(TEMPO_MSG)
                    except:
                        message_type_sauvegarde = True
                        print("================== ERREUR SAUVEGARDE ENCLENCHEE ==================")
