#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
import labyrinthe as laby

noms=['j1','j2','j3','j4']
couleurs=['info','gea','gmp','chimie']
lab=laby.Labyrinthe(noms,couleurs)
dic_sauve = laby.labyrinthe_2_dico(lab)
lab_reconstitue = laby.labyrinthe_from_dico(dic_sauve)
assert lab == lab_reconstitue, "problème de sauvegarde/restitution"
print("ça marche!!!")
