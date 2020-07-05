# coding: utf-8

import socket
import pickle
import select
import time

TEMPO_MSG = 0
AFFICHAGE_MESSAGE = True
NB_ENVOIE = 1

def date_actuelle():
    return time.asctime(time.localtime(time.time()))

# ----------------------------------------------------
def envoieAuServeur(cle, valeur, connexion_avec_serveur, info=None):
    if info == None:
        l = [cle, valeur]
    else:
        l = [cle, valeur, info]
    ld = pickle.dumps(l)
    message = ld + b' '
    for _ in range(NB_ENVOIE):
        if AFFICHAGE_MESSAGE:
            print(f'--> {l[0]}'.ljust(35) + f'envoyé à {date_actuelle()},'.ljust(40) + f'longeur : {len(message)},'.ljust(20) + f'dumps : {message}')
        connexion_avec_serveur.send(message)
    time.sleep(TEMPO_MSG)

# ----------------------------------------------------
def splitMessages(messages):
    # return messages.split(b'. ')
    listeMessage = []
    l = b''
    point_espace = 0
    for i in range(len(messages)):
        a = messages[i:i+1]
        l += a
        if point_espace == 0:
            if a == b'.':
                point_espace = 1

        elif point_espace == 1:
            point_espace = 0
            if a == b' ':
                listeMessage.append(l)
                l = b''
    # if AFFICHAGE_MESSAGE:
    #     if len(listeMessage) > 1:
    #         print(f'SPLIT in {len(listeMessage)}:')
    return listeMessage, l