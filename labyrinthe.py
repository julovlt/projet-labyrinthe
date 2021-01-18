# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
from plateau import *

# dictionnaire qui gère le nombre d'unités de peinture gagnées ou perdues en fonction des actions
POINTS = {"objet": 5, "couleur_joueur": 2, "couleur_neutre": -1, "couleur_adversaire": -2, "peindre_adversaire": 3,
          "ordre_errone": -1, }
# constantes indiquant les différents objets disponibles
BOMBE = 1
PISTOLET = 2
BOUCLIER = 3


def Labyrinthe(noms_joueurs, couleurs_joueurs, humain=False, nb_tours=100, duree_objet=10):
    """
    permet de créer un labyrinthe avec comme participants les joueurs dont les noms et les couleurs
    sont donnés sous forme de liste. Seul le joueur 1 peut être humain, les autre sont automatiques.
    un joueur courant est choisi aléatoirement.
    :param noms_joueurs: la liste des noms des joueurs participant à la partie
    :param couleurs_joueurs: la liste des couleurs choisies par chacun des joueurs
    :param humain: un caractère valant 'H' ou 'O' qui indique si le joueur 1 est humain ou ordinateur
    :param nb_tours: un entier indiquant le nombre de tours de la partie
    :param duree_objet: un entier indiquant la durée de validité d'un objet pris par un joueur
    :return: le labyrinthe crée
    """
    a=Plateau(noms_joueurs)
    b=Participants(noms_joueurs,couleurs_joueurs,humain)
    res = dict()
    if len(noms_joueurs) != len(couleurs_joueurs):
        return None
    for noms in noms_joueurs:
        for couleur in couleurs_joueurs:
            if noms not in res.keys():
                res[noms]=couleur
            else:
                if len(res[nom].values) > 0:
                    pass
    res["nb_tours"]=nb_tours
    res["duree_objet"]=duree_objet
    return res
    

def initialiser_labyrinthe(participants, plateau, carte_supplementaire, nb_tours, rangee_interdite, direction_interdite,
                           duree_objet):
    """
    Cette fonction permet d'initialiser un labyrinthe avec des valeurs bien précises (permettant de charger une partie
    en cours)

    :param participants: les participants à la partie
    :param plateau: le plateau dans son état actuel
    :param carte_supplementaire: la carte amovible qui est à l'extérieur du plateau
    :param nb_tours: le nombre de tours restants
    :param rangee_interdite: la rangée interdite pour la carte amovible
    :param direction_interdite: la colonne interdite pour la carte amovible
    :param duree_objet: la durée de vie des objets possédés par un joueur
    :return: retourne le labyrinthe avec les caractéristiques passées en paramètre
    """
    ...


def get_nb_tours_restants(labyrinthe):
    """
    donne le nombre de tours restants dans la partie

    :param labyrinthe: un labyrinthe
    :return: un entier donnant le nombre de tours restants
    """
    return labyrinthe["duree_objet"]


def get_plateau(labyrinthe):
    """
    retourne la matrice représentant le plateau de jeu

    :param labyrinthe: labyrinthe le labyrinthe considéré
    :return: la matrice représentant le plateau de ce labyrinthe
    """
    


def get_coordonnees_joueur_courant(labyrinthe):
    """
    donne les coordonnées du joueur courant sur le plateau

    :param labyrinthe: le labyrinthe considéré
    :return: les coordonnées du joueur courant ou None si celui-ci n'est pas sur le plateau
    """
    ...


def prendre_joueur_courant(labyrinthe, lig, col):
    """
    enlève le joueur courant de la carte qui se trouve sur la case lin,col du plateau
    si le joueur ne s'y trouve pas la fonction ne fait rien

    :param labyrinthe: le labyrinthe considéré
    :param lig: la ligne où se trouve la carte
    :param col: la colonne où se trouve la carte
    :return: la fonction ne retourne rien mais modifie le labyrinthe
    """
    ...


def poser_joueur_courant(labyrinthe, lin, col):
    """
    pose le joueur courant sur la case lin,col du plateau

    :param labyrinthe: le labyrinthe considéré
    :param lig: la ligne où se trouve la carte
    :param col: la colonne où se trouve la carte
    :return: la fonction ne retourne rien mais modifie le labyrinthe
    """
    ...


def get_participants(labyrinthe):
    """
    retourne la liste des participants (structure créée dans participants.py

    :param labyrinthe: le labyrinthe considéré
    :return: les joueurs sous la forme de la structure implémentée dans participants.py
    """
    ...


def get_carte_a_jouer(labyrinthe):
    """
    donne la carte à jouer celle qui est hors du plateau

    :param labyrinthe: le labyrinthe considéré
    :return: la carte à jouer
    """
    ...


def get_duree_objet(labyrinthe):
    """
    permet de connaitre la durée de validité des objets quand ils sont pris par un joueur

    :param labyrinthe: le labyrinthe considéré
    :return: un entier indiquant la durée de validité des objets
    """
    ...


def get_rangee_interdite(labyrinthe):
    """
    retourne le numéro de la rangée interdite

    :param labyrinthe: le labyrinthe considéré
    :return: un entier indiquant la rangée interdite
    """
    ...


def get_direction_interdite(labyrinthe):
    """
    retourne le numéro de la direction interdite

    :param labyrinthe: le labyrinthe considéré
    :return: un entier indiquant la direction interdite
    """
    ...


def coup_interdit(labyrinthe, direction, rangee):
    """
    retourne True si le coup proposé correspond au coup interdit elle retourne False sinon

    :param labyrinthe: le labyrinthe considéré
    :param direction: un caractère 'N', 'E', 'S' ou 'O' indiquant la direction choisie
    :param rangee: un entier indiquant la colonne ou la ligne choisie
    :return: un booléen indiquant si le coup est interdit ou non
    """
    ...


def lave_et_transfert_joueurs(carte_a_jouer, carte_inseree):
    """
    Permet de laver la carte à jouer (enlever la couleur) et de transférer la liste des joueurs
    qui se trouvent sur la carte_a_jouer vers la carte_inseree

    :param carte_a_jouer: la carte qui vient d'être expulsée du plateau
    :param carte_inseree: la carte qui vient d'être remuise sur le plateau
    :return: cette fonction ne retourne rien
    """
    ...


def jouer_carte(labyrinthe, direction, rangee):
    """
    fonction qui joue la carte amovible dans la direction et sur la rangée passées
    en paramètres. Cette fonction
       - met à jour le plateau du labyrinthe
       - met à jour la carte à jouer
       - met à jour la nouvelle direction interdite

    :param labyrinthe: le labyrinthe
    :param direction: un caractère qui indique la direction choisie ('N','S','E','O')
    :param rangee:  le numéro de la ligne ou de la colonne choisie
    :return: None si tout s'est bien passé ou une chaine de caractères indiquants le problème survenu.
    Voici les messages possibles
        * Carte insérée!
        * Rangée invalide
        * Direction invalide
        * Coup interdit
    """
    ...

def tourner_carte(labyrinthe, sens='H'):
    """
    Tourne la carte à jouer dans le sens indiqué en paramètre (H horaire A antihoraire)

    :param labyrinthe:  le labyrinthe considéré
    :param sens: un caractère indiquant le sens dans lequel tourner la carte ('A' ou 'H')
    :return: un chaine de caractères indiquant ce qui s'est passé
        * Carte tournée!
        * Ordre pour tourner la carte inconnu
    """
    ...

def peindre(labyrinthe, direction):
    """
    Permet de peindre de la couleur du joueur courant toutes les cases atteignables dans la direction choisie.
    Si direction vaut 'X' la fonction ne fait rien (le joueur courant ne veut pas peindre)
    Cette fonction va donc
        * peindre toutes les cartes atteignables à partir de la position du joueur courant dans la direction choisie
        * enlever au joueur courant le nombre d'unités de peinture correspond au nombre de cases peintes
        * enlever aux joueurs ne possedant pas de bouclier et touchés par le jet de peinture le nombre d'unités
          prévu par POINTS["peindre_adversaire"]
        * ajouter au joueur courant le nombre d'unités de peinture enlevés aux adversaires
    De plus si le joueur courant possède un pistolet son jet de peinture doit traverser un mur et si il possède une
    bombe le jet de peinture doit aller dans toutes les directions en commençant par direction et en allant dans le
    sens des aiguilles d'une montre

    :param labyrinthe: le labyrinthe considéré
    :param direction: un caractère qui indique la direction choisie ('X', 'N','S','E','O')
    :return: un chaine de caractères indiquant ce qui s'est passé
        * Le joueur ne veut pas peindre
        * Le joueur a peint dans la direction ...
        * Direction inconnue
    """
    ...


def deplacer(labyrinthe, direction):
    """
    Déplace le joueur courant dans la direction souhaitée si c'est possible. Cette fonction va notamment:
    * verifier que le déplacement est possible
    * déplacer le joueur
    * donner au joueur courant l'objet qu'il y a sur la carte d'arrivée (si elle possède un objet) en augmentant
      la réserve de peinture du jouieur de POINTS["objet"]
    * mettre à jour la réserve de peinture du joueur en fonction de la couleur de la case d'arrivée
      (POINTS["couleur_joueur"], POINTS["couleur_neutre"] ou POINTS["couleur_adversaire"]
    Si le joueur donne un ordre erroné ou un déplacement impossible il perd POINTS["ordre_errone"] unité de peinture

    :param labyrinthe: le labyrinthe considéré
    :param direction: un caractère qui indique la direction choisie ('N','S','E','O')
    :return: un chaine de caractères indiquant ce qui s'est passé
        * La direction est inconnue
        * Le déplacement est impossible
        * Le joueur s'est déplacé vers ...
        * Le joueur s'est déplacé vers ... et un trouvé un objet
    """
    ...

    
def interpreter_ordre(labyrinthe, ordre):
    """
    Cette fonction executes les ordres fournie sous la forme d'une chaine de caractères commençant par l'ordre de
    peinture puis l'ordre de déplacement ou l'ordre de modification du labyrinthe. Tous les ordres commencent par un P
    suivi d'une des lettre X N O S ou E indiquant la direction où peindre (X indiquant que le joueur ne souhaite pas
    peindre) . La seconde partie de l'ordre est
        * soit un D (pour déplacement) suivi d'une des lettres N O S ou E
        * soit un T (pour tourner) suivi d'une suite de H ou de A suivi une des lettres N O S ou E suivi d'un chiffre
    Par exemple:
        * "PODE" indique que le joueur peint vers l'ouest et se déplace vers l'est
        * "PXTAAN3" indique que le joueur ne souhaite pas peindre et qu'il tourne la carte amovible deux fois dans le
            sens antihoraire puis insère la carte amovible au nord dans la colonne 3

    :param labyrinthe: le labyrinthe considéré
    :param ordre: un chaine de caractère comme indiquée ci-dessus
    :return: une chaine de caractères indiquant ce qui s'est passé
    """
    ...

    
def finir_tour(labyrinthe):
    """
     met a jour les différentes informations sur les joueurs
     * le temps restant de l'objet du joueur courant
     * la surface couverte par chaque joueur
     change le joueur courant (et met à jour le compteur de tour si nécessaire
    vérifie si la partie est terminée, si ce n'est pas le cas passe au joueur suivant

    :param labyrinthe: labyrinthe considéré
    :return: Cette fonction retourne rien mais elle modifie le labyrinthe
    """
    ...


###################################################
### Fonctions utilitaires qui permettent de transmettre l'état du labyrinthe à une intelligence artificielle
###################################################

def joueur_2_dico(joueur):
    return {
        "nom": get_nom_joueur(joueur), "objet": get_objet_joueur(joueur), "couleur": get_couleur_joueur(joueur),
        "reserve_peinture": get_reserve_peinture(joueur), "surface": get_surface(joueur),
        "type_joueur": get_type_joueur(joueur), "temps_restant": get_temps_restant(joueur)
    }


def participants_2_dico(participants):
    nb_participants = get_nb_joueurs(participants)
    liste_joueurs = [joueur_2_dico(get_joueur_par_num(participants, i)) for i in range(1, nb_participants + 1)]
    return {"liste_joueurs": liste_joueurs, "joueur_courant": get_num_joueur_courant(participants),
            "premier_joueur": get_num_premier_joueur(participants)
            }


def carte_2_dico(carte):
    return {"murs": coder_murs(carte), "pions": [get_nom_joueur(joueur) for joueur in get_liste_joueurs(carte)],
            "objet": get_objet(carte), "couleur": get_couleur(carte)}


def matrice_2_dico(matrice):
    nb_lig = get_nb_lignes(matrice)
    nb_col = get_nb_colonnes(matrice)
    res = {"nb_lignes": nb_lig, "nb_colonnes": nb_col,
           "les_valeurs": [carte_2_dico(get_valeur(matrice, i, j)) for i in range(nb_lig) for j in range(nb_col)]}
    return res


def labyrinthe_2_dico(labyrinthe):
    return {
        "les_joueurs": participants_2_dico(get_participants(labyrinthe)),
        "plateau": matrice_2_dico(get_plateau(labyrinthe)),
        "carte": carte_2_dico(get_carte_a_jouer(labyrinthe)),
        "nb_tours": get_nb_tours_restants(labyrinthe),
        "rangee_interdite": get_rangee_interdite(labyrinthe),
        "direction_interdite": get_direction_interdite(labyrinthe),
        "duree_objet": get_duree_objet(labyrinthe)
    }


def labyrinthe_from_dico(dico_lab):
    participants = Participants([], [])
    for dico_joueur in dico_lab["les_joueurs"]["liste_joueurs"]:
        joueur = Joueur(dico_joueur["nom"], dico_joueur["couleur"], dico_joueur["reserve_peinture"],
                        dico_joueur["surface"], dico_joueur["type_joueur"],dico_joueur["objet"],
                        dico_joueur["temps_restant"])
        ajouter_joueur(participants, joueur)
    init_premier_joueur(participants, dico_lab["les_joueurs"]["premier_joueur"])
    set_joueur_courant(participants, dico_lab["les_joueurs"]["joueur_courant"])
    nb_lig = dico_lab["plateau"]["nb_lignes"]
    nb_col = dico_lab["plateau"]["nb_colonnes"]
    plateau = Matrice(nb_lig, nb_col)
    for i in range(nb_lig * nb_col):
        carte_dico = dico_lab["plateau"]["les_valeurs"][i]
        carte = Carte(True, True, True, True)
        decoder_murs(carte, carte_dico["murs"])
        poser_objet(carte, carte_dico["objet"])
        set_couleur(carte, carte_dico["couleur"])
        pions = [get_joueur_par_nom(participants, nom) for nom in carte_dico["pions"]]
        set_liste_joueurs(carte, pions)
        set_valeur(plateau,i//nb_col,i%nb_col,carte)
    carte = Carte(True, True, True, True)
    decoder_murs(carte, dico_lab["carte"]["murs"])
    poser_objet(carte, dico_lab["carte"]["objet"])
    return initialiser_labyrinthe(participants, plateau, carte, dico_lab["nb_tours"], dico_lab["rangee_interdite"],
                                  dico_lab["direction_interdite"], dico_lab["duree_objet"])


