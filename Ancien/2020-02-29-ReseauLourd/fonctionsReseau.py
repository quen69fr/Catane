import socket
import pickle
import select
import time

def date_actuelle():
    return time.asctime(time.localtime(time.time()))

def demandeAServeur(cle, connexion_avec_serveur):
    dump = pickle.dumps(cle)
    #print('Envoie à', date_actuelle(), ':      longeur :', len(dump), 'message : ', dump)
    connexion_avec_serveur.send(dump)
    valeur = connexion_avec_serveur.recv(102400)
    #print('Recu à', date_actuelle(), ':      longeur :', len(valeur), 'message : ', valeur)
    # TODO ?
    return pickle.loads(valeur)

def envoieAuServeur(cle, valeur, connexion_avec_serveur):
    l = [cle, valeur]
    ld = pickle.dumps(l)
    print(l[0], '         envoier à', date_actuelle(), ', longeur :', len(ld), ', dumps :', ld)
    connexion_avec_serveur.send(ld)
    # connexion_avec_serveur.recv(102400)