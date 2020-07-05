# coding: utf-8

import requests
import time

LOGIN = 'login'
CONDITIONS_INIT_JEU = 'conditionsInitJeu'
LISTE_JOUEURS = 'listeJoueurs'
SAUVEGARDE = 'sauvegarde'

EVT_ACTION = 'action'
EVT_GET_EVENT = 'event'

PARAM_PSEUDO = 'pseudo'
PARAM_TYPE = 'type'
PARAM_CONTENU = 'contenu'
PARAM_INFO = 'info'
PARAM_ID = 'id'

TYPE_MSG_SOMMET = 'sommet'
TYPE_MSG_ARETE = 'arete'
TYPE_MSG_TUILE = 'tuile'
TYPE_MSG_CARTE = 'carte'
TYPE_MSG_VILLE = 'ville'
TYPE_MSG_COLONIE = 'colonie'
TYPE_MSG_ROUTE = 'route'
TYPE_MSG_ATTR_JOUEUR = 'attribut'

DELAY_SERVEUR_REQUESTS = 0.1


class ReseauClient:
    def __init__(self, port):
        self.pseudoJoueur = None
        self.adresse_ip = None
        self.port = port
        self.id_actuelle = -1
        self.time_last_request = 0

    def envoie_au_serveur(self, cle, valeur, info=None):
        url = f'http://{self.adresse_ip}:{self.port}/catane/{EVT_ACTION}'
        paramjson = {PARAM_PSEUDO: self.pseudoJoueur, PARAM_TYPE: cle, PARAM_CONTENU: valeur, PARAM_INFO: info}
        reponse = requests.post(url, json=paramjson)
        # print(reponse)

    def sauvegarde_partie(self):
        url = f'http://{self.adresse_ip}:{self.port}/catane/{SAUVEGARDE}'
        reponse = requests.get(url).json()

    def login(self, pseudo):
        url = f'http://{self.adresse_ip}:{self.port}/catane/{LOGIN}?{PARAM_PSEUDO}={pseudo}'
        try:
            reponse = requests.get(url).json()
        except:
            pass
        else:
            # print(reponse)
            self.pseudoJoueur = pseudo
            if reponse == 1:
                return True
        return False

    def getConditionsInitJeu(self):
        url = f'http://{self.adresse_ip}:{self.port}/catane/{CONDITIONS_INIT_JEU}'
        # print(url)
        reponse = requests.get(url).json()
        return reponse

    def getListeJoueurs(self):
        url = f'http://{self.adresse_ip}:{self.port}/catane/{LISTE_JOUEURS}'
        reponse = requests.get(url).json()
        if reponse == 0:
            return False
        return reponse

    def regardeEvenementsNonFait(self):
        if self.id_actuelle == -1 or time.time() - self.time_last_request > DELAY_SERVEUR_REQUESTS:
            url = f'http://{self.adresse_ip}:{self.port}/catane/{EVT_GET_EVENT}?{PARAM_PSEUDO}={self.pseudoJoueur}' \
                  f'&{PARAM_ID}={self.id_actuelle}'
            reponse = requests.get(url).json()
            if len(reponse) != 0:
                self.id_actuelle = reponse[-1][PARAM_ID]
            elif self.id_actuelle == -1:
                self.id_actuelle = 0
            self.time_last_request = time.time()
            return reponse
        return []
