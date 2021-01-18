# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
from joueur import *


def Participants(noms_joueurs, liste_couleurs, humain=True):
    """
    crée une liste de participants dont les noms sont dans la liste de noms passés en paramètre.
    Les joueurs sont numéroté de 1 à N dans l'ordre de leur création
    Par défaut tous les joueurs sont des ordinateurs sauf le joueur 1 en fonction du paramètre humain
    Attention! il ne s'agit pas d'une simple liste de joueurs mais il faudra des informations permettant
    de gérer la notion de joueur courant, de tour de jeu (une fois que tous les joueurs ont joué)

    :param noms_joueurs: une liste de chaines de caractères
    :param liste_couleurs: la liste des couleurs choisis pour chaque joueur
    :param humain: un booléen indiquant si le joueur 1 est humain ou non
    :return: la structure que vous avez choisie pour représenter les participants
    """
    participants={"joueurs": [], "courant": 1, "tour": 1}
    h_ou_o="O"
    for i in range(len(noms_joueurs)):
        if i==0 and humain:
            h_ou_o='H'
        participants["joueurs"].append((i+1,Joueur(noms_joueurs[i],liste_couleurs[i],20,0,h_ou_o,0,0)))
        h_ou_o="O"
    return participants

def ajouter_joueur(participants, joueur):
    """
    ajoute un nouveau joueur

    :param participants: les participants actuels
    :param joueur: le joueur à ajouter
    :return: cette fonction ne retourne rien mais modifie la liste des participants
    """
    participants["joueurs"].append((len(participants)+1,joueur))
    
def init_aleatoire_premier_joueur(participants):
    """
    tire au sort le premier joueur courant

    :param participants: les participants
    :return: la fonction ne retourne rien mais modifie la liste des participants
    """
    a=random(1,len(participants)+1)
    participants["premier_joueur_courant"]=a


def get_num_joueur_courant(participants):
    """
    retourne le numéro du joueur courant

    :param participants: les participants
    :return: un nombre entre 1 et 4 indiquant le numéro du joueur courant
    """
    return participants["courant"]


def get_num_premier_joueur(participants):
    """
    return le numéro du joueur qui a joué en premier

    :param participants: les participants
    :return: un nombre entre 1 et 4 indiquant le numéro du joueur qui a joué en premier
    """
    return participants["premier_joueur_courant"]


def init_premier_joueur(participants, num_joueur):
    """
    initialialise le premier joueur courant au joueur qui porte le numéro num_joueur

    :param participants: les participants
    :param num_joueur: un nombre entre 1 et 4
    :return: rien cette fonction modifie la liste des participants
    """
    participants["premier_joueur_courant"]=num_joueur


def set_joueur_courant(participants, num_joueur):
    """
    force le joueur courant au joueur qui porte le numéro num_joueur

    :param participants: les participants
    :param num_joueur: un nombre entre 1 et 4
    :return: rien cette fonction modifie la liste des participants
    """
    participants["courant"]=num_joueur


def changer_joueur_courant(participants):
    """
    passe au joueur suivant (change le joueur courant donc)

    :param participants: les participants
    :return: cette fonction modifie la liste des participants et
             retourne un booléen indiquant si on est revenu au joueur qui a commencé la partie
    """
    a=get_num_premier_joueur(participants)
    res=False
    if participants["courant"]==len(participants["joueurs"]):
        participants["courant"]=1
    else:
        participants["courant"]+=1
        if participants["courant"]==a:
            res=True
    return res

def get_nb_joueurs(participants):
    """
    retourne le nombre de joueurs participant à la partie

    :param participants: les participants
    :return: le nombre de joueurs de la partie
    """
    return len(participants["joueurs"])

def get_joueur_par_num(participants, num_joueur):
    """
    retourne le joueur de numéro num_joueur

    :param participants: les participants
    :param num_joueur: le numéro du joueur souhaité
    :return: le joueur qui porte le numéro indiqué
    """
    a=participants["joueurs"]
    return a[num_joueur-1][1]


def get_joueur_par_nom(participants, nom_joueur):
    """
    retourne le joueur de numéro num_joueur

    :param participants: les participants
    :param nom_joueur: le nom du joueur souhaité
    :return: le joueur qui porte le nom indiqué, None si aucun joueur ne porte ce nom
    """
    a=participants["joueurs"]
    res=None
    for (_,joueur) in a:
        if joueur["nom"]==nom_joueur:
            res=joueur
    return res


def get_joueur_courant(participants):
    """
    retourne le joueur courant

    :param participants: les participants
    :return: cette fonction ne retourne rien mais modifie la liste des participants
    """
    return participants['joueur'][participants['courant']-1]


def mise_a_jour_surface(participants, couverture):
    """
    permet de mettre à jour la surface couverte par chaque joueur

    :param participants: les participants
    :param couverture: un dictionnaire qui indique pour chaque couleur le nombre de cases de cette couleur
    :return: cette fonction ne retourne rien mais modifie la liste des participants
    """
    for i in range(len(participants["joueurs"])):
        for (couleur,surface) in couverture.items():
            a=get_couleur_joueur(participants["joueurs"][i][1])
            if a==couleur:
                participants["joueurs"][i][1]["surface"]=surface

    
def classement_joueurs(participants):
    """
    Retourne une liste de participants triée suivant les critètres 1) la surface couverte 2) la réserve d'encre

    :param participants: les participants
    :return: une liste de joueurs triée dans l'ordre décroissant
    """
    joueurs = []
    for (_,player) in participants['joueurs']:
        joueurs.append(player)  
    j = 0
    continuer = True
    while continuer and j < len(joueurs) - 1:
        continuer = False
        for i in range(len(joueurs) - 1 - j):
            if comparer(joueurs[i], joueurs[i+1]) == 1:
                joueurs[i], joueurs[i + 1] = joueurs[i + 1], joueurs[i]
                continuer = True
        j += 1
    joueurs.reverse()
    return joueurs

#J'ai eu du mal a faire cette fonction je me suis donc aider de Julien et de Vincent. 