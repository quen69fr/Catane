# coding: utf-8

from plateau import *
from outils import *
from flask import Flask, request, jsonify
import json

MODE_SAUVEGARDE = False
FICHIER_SAUVEGARDE = 'sauvegarde.json'

app = Flask(__name__)


class Evenement():
    id_max = 1

    def __init__(self, pseudo, type, contenu, info=None):
        self.id = Evenement.id_max
        Evenement.id_max += 1
        self.pseudo = pseudo
        self.type = type
        self.contenu = contenu
        self.info = info
        # print(f'--> Event : {self.id}    : {self.type}')

    def dump(self):
        return {PARAM_ID: self.id, PARAM_PSEUDO: self.pseudo, PARAM_TYPE: self.type, PARAM_CONTENU: self.contenu,
                PARAM_INFO: self.info}

# Variables globales nécessaires pour répondre aux requetes Flask
liste_clients_pseudos = []
nbJoueurs = 0
listeEvenements = []
dumpConditionsInitialesJeu = {}

if MODE_SAUVEGARDE:
    pygame.quit()
    with open(FICHIER_SAUVEGARDE, 'r') as fichier:
        dic_sauvegarde = json.load(fichier)
        liste_clients_pseudos = dic_sauvegarde['liste_clients_pseudos']
        nbJoueurs = dic_sauvegarde['nbJoueurs']
        dumpConditionsInitialesJeu = dic_sauvegarde['dumpConditionsInitialesJeu']
        if len(dic_sauvegarde['events']) > 0:
            for dic_event in dic_sauvegarde['events']:
                event = Evenement(None, None, None)
                event.__dict__.update(dic_event)
                listeEvenements.append(event)
            Evenement.id_max = len(listeEvenements) + 1


@app.route(f'/catane/{SAUVEGARDE}')
def sauvegarde():
    dic = {'liste_clients_pseudos': liste_clients_pseudos,
           'nbJoueurs': nbJoueurs,
           'dumpConditionsInitialesJeu' : dumpConditionsInitialesJeu,
           'events': [event.__dict__ for event in listeEvenements]}
    with open(FICHIER_SAUVEGARDE, "w") as fichier:
        json.dump(dic, fichier)
    return str(1)


@app.route(f'/catane/{LOGIN}')
def login():
    pseudo = request.args.get(PARAM_PSEUDO)
    # print(pseudo)
    if pseudo not in liste_clients_pseudos:
        if len(liste_clients_pseudos) >= nbJoueurs:
            return str(0)
        if pseudo not in liste_clients_pseudos:
            liste_clients_pseudos.append(pseudo)
    return str(1)


@app.route(f'/catane/{EVT_ACTION}', methods=['POST'])
def action():
    req_data = request.get_json()
    pseudo = req_data[PARAM_PSEUDO]
    type = req_data[PARAM_TYPE]
    contenu = req_data[PARAM_CONTENU]
    info = req_data[PARAM_INFO]
    event = Evenement(pseudo, type, contenu, info)
    listeEvenements.append(event)
    # print(event.dump())
    return '1'


@app.route(f'/catane/{EVT_GET_EVENT}')
def event():
    pseudo = request.args.get(PARAM_PSEUDO)
    id_str = request.args.get(PARAM_ID)
    # print(f'pseudo : {pseudo}, id : {id_str}')
    l = []
    if id_str is not None:
        try:
            id = int(id_str)
        except:
            pass
        else:
            if id == -1:
                id_utilisee = 0
            else:
                id_utilisee = id
            for i in range(id_utilisee, len(listeEvenements)):
                event = listeEvenements[i]
                if event.pseudo != pseudo or id == -1:
                    l.append(event.dump())
    return jsonify(l)


@app.route(f'/catane/{CONDITIONS_INIT_JEU}')
def getConditionsInitJeu():
    return dumpConditionsInitialesJeu


@app.route(f'/catane/{LISTE_JOUEURS}')
def getListeJoueurs():
    if len(liste_clients_pseudos) == nbJoueurs:
        return jsonify(liste_clients_pseudos)
    return str(0)


if __name__ == "__main__":
    port = 12800

    if not MODE_SAUVEGARDE:
        plateau = Plateau(X_PLATEAU, Y_PLATEAU)
        plateau.creationPlateau()
        plateau.preparePlateau()
        ecran_reglage = Ecran_reglages()

        boutonQuitter = Bouton(LARGEUR - MARGES - LARGEUR_IMAGE_BOUTON_MESSAGES, MARGES,
                               'sauvegarde', image=IMAGE_BOUTON_QUITTER)

        etat_partie = 'reglagesJoueurs'
        listeCouleurs = []

        clic_up_down = 0

        while etat_partie == 'reglagesJoueurs' or etat_partie == 'reglagePlateau':
            souris = pygame.mouse.get_pos()
            x_souris = souris[0]
            y_souris = souris[1]

            clic = False
            for event in pygame.event.get():
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

            affiche_ecran_principal(etat_partie)
            plateau.affiche()
            boutonQuitter.affiche()

            ecran_reglage.affiche(etat_partie)

            if clic:
                if boutonQuitter.clic(x_souris, y_souris):
                    pygame.quit()
                    exit(0)
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
                                if bouton.selectionner:
                                    c = BLEU
                                    if bouton.parametre == 'rouge':
                                        c = ROUGE
                                    elif bouton.parametre == 'blanc':
                                        c = BLANC
                                    elif bouton.parametre == 'orange':
                                        c = ORANGE
                                    listeCouleurs.append(c)

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
                            pygame.quit()
                            continue

            pygame.display.update()
            pygame.time.Clock().tick(FPS)

        random.shuffle(listeCouleurs)

        nbJoueurs = len(listeCouleurs)

        listePiocheCartesSpeciales = LISTE_PIOCHE_CARTE_SPECIALE
        random.shuffle(listePiocheCartesSpeciales)
        dumpConditionsInitialesJeu = {'plateau': plateau.dump(),
                                      'listeCouleurs': listeCouleurs,
                                      'listePiocheCartesSpeciales': listePiocheCartesSpeciales}

    app.run(host='0.0.0.0', port=port)
