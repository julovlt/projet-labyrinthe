# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
from carte import *
from participants import *
from matrice import *
from random import shuffle

def Plateau(les_joueurs, taille=7, nb_objets=3):
    """
    créer un nouveau plateau contenant les joueurs passés en paramètres

    :param les_joueurs: la liste des joueurs participant à la partie
    :param taille: un entier qqui donne la taille du labyrinthe
    :param nb_objets: un entier qui indique combien d'objets différents existent
    :return: un couple contenant
              * une matrice de taille taillextaill représentant un plateau de labyrinthe où les cartes
                ont été placée de manière aléatoire
              * la carte amovible qui n'a pas été placée sur le plateau
    """
    matrice=Matrice(taille,taille,0)
    #carte fixe
    liste_cartes_fixe=[9,1,1,3,8,8,1,2,8,4,2,2,12,4,4,6]
    indice_carte_fixe=0

    #carte pas fixe
    carte_pas_fixe=[]
    for a in range(12):
        carte_pas_fixe.append(5)
    for b in range(6):
        carte_pas_fixe.append(1)
    for c in range(16):
        carte_pas_fixe.append(9)
    random.shuffle(carte_pas_fixe)

    for i in range(len(matrice)):
        for j in range(get_nb_colonnes(matrice)):
            carte_cree=Carte(True,True,False,False)
            if j%2==0 and i%2==0:
                decoder_murs(carte_cree,liste_cartes_fixe[indice_carte_fixe])
                indice_carte_fixe=indice_carte_fixe+1
            else:
                azerty=carte_pas_fixe[0]
                decoder_murs(carte_cree,azerty)
                carte_pas_fixe.pop(0)
            set_valeur(matrice,i,j,carte_cree)
    
    player_index = 1
    for i in range(0, taille, taille-1):
        for j in range(0, taille, taille-1):
            if player_index <= get_nb_joueurs(les_joueurs):
                poser_joueur(get_valeur(matrice, i, j), get_joueur_par_num(les_joueurs, player_index))
                player_index += 1

    poser_les_objets(matrice, get_nb_joueurs(les_joueurs), nb_objets)
    carte_de_rechange=Carte(True,True,False,False)
    decoder_murs(carte_de_rechange,carte_pas_fixe[0])
    return (matrice, carte_de_rechange)
        

def creer_cartes_amovibles():
    """
    fonction utilitaire qui permet de créer les cartes amovibles du jeu 
    la fonction retourne la liste, mélangée aléatoirement, des cartes ainsi créées

    :return: la liste mélangée aléatoirement des cartes amovibles créees
    """
    res=[]
    carte_pas_fixe=[]
    for a in range(12):
        carte_pas_fixe.append(5)
    for b in range(6):
        carte_pas_fixe.append(1)
    for c in range(16):
        carte_pas_fixe.append(9)
    random.shuffle(carte_pas_fixe)
    for i in range(len(carte_pas_fixe)):
        res.append(Carte(decoder_murs(carte_pas_fixe[i])))
    return res

def poser_les_objets(plateau, nb_joueurs, nb_objets):
    """
    cette fonction va poser de manière aléatoire les objets sur le plateau, il y aura un objet de chaque types par joueur

    :param plateau: le plateau
    :param nb_joueurs: un entier indiquant le nombre de joueurs participant à la partie
    :param nb_objets: un entier le nombre de type d'objets différents
    :return: cette fonction ne retourne rien mais modifie le plateau
    """
    carte=None
    for objet in range(nb_objets):
        for joueur in range(nb_joueurs):
            carte=None
            while carte==None or get_objet(carte)!=0:
                carte=get_valeur(plateau,random.randint(0,6),random.randint(0,6))
            poser_objet(carte,objet+1)

def get_coordonnees_joueur(plateau, joueur):
    """
    retourne les coordonnées sous la forme (lig,col) du joueur passé en paramètre

    :param plateau: le plateau considéré
    :param joueur: le joueur à trouver
    :return: un couple d'entiers donnant les coordonnées du joueur ou None si le joueur n'est pas sur le plateau
    """
    res=(None,None)
    for i in range(get_nb_lignes(plateau)):
        for j in range(get_nb_colonnes(plateau)):
            a=plateau[i][j]
            if joueur in a["joueur_sur_la_carte"]:
                res=(i,j)
    return res
    

def passage_plateau(plateau, lig, col, direction):
    """
    indique si il y a bien un passage dans le direction passée en paramètre à partir de la position
    lig,col sur le plateau. La fonction retourne None si il n'y a pas de passage ou les coordonnées
    de la case où on arrive en prenant le passage s'il y en a un

    :param plateau: le plateau
    :param lig: un entier donnant le numéro de la ligne
    :param col: un entier donnant le numéro de la colonne
    :param direction: un caractère 'N', 'S', 'O' ou 'E' indiquant la direction où on veut aller
    :return: None s'il n'y a pas de passage possible
             (x,y) les coordonnées où on arrive en prenant le passage s'il existe (un couple d'entiers)
    """
    res=None
    if direction=="N" and lig-1>=0 and passage_nord(get_valeur(plateau,lig,col),get_valeur(plateau,lig-1,col))==True:
        res=(lig-1,col)
    elif direction=="O" and col-1>=0 and passage_ouest(get_valeur(plateau,lig,col),get_valeur(plateau,lig,col-1))==True:
        res=(lig,col-1)
    elif direction=="S" and lig+1<len(plateau) and passage_sud(get_valeur(plateau,lig,col),get_valeur(plateau,lig+1,col))==True:
        res=(lig+1,col)
    elif direction=="E" and col+1<get_nb_colonnes(plateau) and passage_est(get_valeur(plateau,lig,col),get_valeur(plateau,lig,col+1))==True:
        res=(lig,col+1)
    return res

def accessible(plateau, lig_depart, col_depart, lig_arrivee, col_arrivee):
    """
    indique si il y a un chemin entre la case lig_depart,col_depart et la case lig_arrivee,col_arrivee du labyrinthe

    :param plateau: le plateau considéré
    :param lig_depart: la ligne de la case de départ
    :param col_depart: la colonne de la case de départ
    :param lig_arrivee: la ligne de la case d'arrivée
    :param col_arrivee: la colonne de la case d'arrivée
    :return: un boolean indiquant s'il existe un chemin entre la case de départ
              et la case d'arrivée
    """
    matrice_bis=Matrice(get_nb_lignes(plateau),get_nb_colonnes(plateau), -1)
    cpt = 0
    set_valeur(matrice_bis,lig_depart,col_depart,cpt)
    voisin = [(lig_depart, col_depart)]
    tester = [(lig_depart, col_depart)]
    while len(tester) != 0 and (lig_arrivee,col_arrivee) not in voisin:
        cpt += 1
        li = []
        for l, c in tester:
            nouveau = [(l-1,c), (l+1,c), (l,c-1), (l,c+1)]
            nouveau = [(lig, col) for lig, col in nouveau if lig >= 0 and col >= 0 and lig <= get_nb_lignes(plateau) -1 and col <= get_nb_colonnes(plateau)-1 and (lig, col) not in voisin]
            for lig, col in nouveau:
                if lig == l-1 and passage_nord(get_valeur(plateau, l, c), get_valeur(plateau, lig, col)):
                    li.append((lig, col))
                    set_valeur(matrice_bis, lig, col, cpt)
                if lig == l+1 and passage_sud(get_valeur(plateau, l, c), get_valeur(plateau, lig, col)):
                    li.append((lig, col))
                    set_valeur(matrice_bis, lig, col, cpt)                    
                if col == c-1 and passage_ouest(get_valeur(plateau, l, c), get_valeur(plateau, lig, col)):
                    li.append((lig, col))
                    set_valeur(matrice_bis, lig, col, cpt)
                if col == c+1 and passage_est(get_valeur(plateau, l, c), get_valeur(plateau, lig, col)):
                    li.append((lig, col))
                    set_valeur(matrice_bis, lig, col, cpt)
            voisin += li
        tester = li
    return (lig_arrivee, col_arrivee) in voisin
 

def peindre_direction_couleur(plateau, lig, col, direction, couleur, reserve_peinture, traverser_mur, tester=False):
    """
    Permet de peindre d'un couleur les cases accessibles à partir de lig,col dans la direction direction avec la reserve
    de peinture disponible.
    La fonction retourne la liste des joueurs touchés et le nombre de cases peintes.
    Attention si le paramètre tester est à True les cases ne sont pas réellement peintes (on teste juste combien de
    cases seraient peintes)

    :param plateau: un plateau
    :param lig: ligne de départ
    :param col: colonne de départ
    :param direction: un caractère valeur 'N','E','S' ou 'O'
    :param couleur: une couleur de peinture
    :param reserve_peinture: le nombre maximum de cases pouvant être peinte
    :param traverser_mur: booléen permettant de traverser une fois un mur (pouvoir du pistolet)
    :param tester: booléen indiquant si on souhaite vraiment peindre les cases ou juste tester combien on peut en peindre
    :return: un couple contenant la liste des joueurs touchés lors de l'action de peindre et le nombre de cases peintes
    """
    #pour cette fonction vincent m'a grandement aider. J'avais vraiment beaucoup de mal.
    liste_joueur=[]
    nombre=0
    mur=traverser_mur
    case=(lig,col)
    while case!=None:
        carte=get_valeur(plateau,case[0],case[1])
        if reserve_peinture>nombre:
            if tester==False:
                set_couleur(carte,couleur)
            nombre=nombre+1
        for joueur in get_liste_joueurs(carte):
            liste_joueur.append(joueur)

        if direction=="N" and case[0]-1>=0:
            if passage_nord(get_valeur(plateau,case[0],case[1]),get_valeur(plateau,case[0]-1,case[1])):
                case=(case[0]-1,case[1])
            elif mur==True:
                case=(case[0]-1,case[1])
                mur=False
            else:
                case=None
        elif direction=="O" and case[1]-1>=0:
            if passage_ouest(get_valeur(plateau, case[0], case[1]), get_valeur(plateau,case[0], case[1]-1)):
                case = (case[0], case[1]-1)
            elif mur==True:
                case= (case[0],case[1]-1)
                mur=False
            else:
                case=None
        elif direction=="S" and case[0]+1<get_nb_lignes(plateau):
            if passage_sud(get_valeur(plateau,case[0],case[1]), get_valeur(plateau,case[0]+ 1,case[1])):
                case=(case[0]+1,case[1])
            elif mur==True:
                case=(case[0]+1,case[1])
                mur=False
            else:
                case=None
        elif direction=="E" and case[1]+1<get_nb_colonnes(plateau):
            if passage_est(get_valeur(plateau,case[0],case[1]),get_valeur(plateau,case[0],case[1]+1)):
                case=(case[0],case[1]+1)
            elif mur==True:
                case=(case[0],case[1]+1)
                mur=False
            else:
                case=None
        else:
            case=None
    return(liste_joueur,nombre)
        
def nb_cartes_par_couleur(plateau):
    """
    calcule le nombre de cartes coloriées pour chaque couleur

    :param plateau: le plateau
    :return: un dictionnaire contenant pour chaque couleur présente sur le plateau le nombre de carte de cette couleur
    """
    res={}
    for i in range(get_nb_lignes(plateau)):
        for j in range(get_nb_colonnes(plateau)):
            couleur=get_couleur(plateau[i][j])
            if couleur!="aucune":
                if couleur not in res.keys():
                    res[couleur]=1
                else:
                    res[couleur]+=1
    return res


def affiche_plateau(plateau):
    """
    affichage redimentaire d'un plateau

    :param plateau: le plateau
    :return: rien mais affiche le plateau
    """
    remplissage = ' ' * 30
    print(remplissage, end='')
    for i in range(1, 7, 2):
        print(" " + str(i), sep='', end='')
    print()
    for i in range(get_nb_lignes(plateau)):
        print(remplissage, end='')
        if i % 2 == 0:
            print(' ', sep='', end='')
        else:
            print(str(i), sep='', end='')
        for j in range(get_nb_colonnes(plateau)):
            print(to_char(get_valeur(plateau, i, j)), end='')
        if i % 2 == 0:
            print(' ', sep='', end='')
        else:
            print(str(i), sep='', end='')
        print()
    print(' ', sep='', end='')
    print(remplissage, end='')
    for i in range(1, 7, 2):
        print(" " + str(i), sep='', end='')
    print()
