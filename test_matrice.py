#!/usr/bin/python3
import unittest
import matrice


def creer_matrice_test(nb_lig, nb_col, dir='X', rg=-1, val=-1):
    m = matrice.Matrice(nb_lig, nb_col)
    ejecte = val
    for l in range(nb_lig):
        for c in range(nb_col):
            if dir == 'N' and rg == c:
                if l == 0:
                    matrice.set_valeur(m, l, c, val)
                    ejecte = nb_col * (nb_lig - 1) + c
                else:
                    matrice.set_valeur(m, l, c, (l - 1) * nb_col + c)
            elif dir == 'S' and rg == c:
                if l == nb_lig - 1:
                    matrice.set_valeur(m, l, c, val)
                    ejecte = c
                else:
                    matrice.set_valeur(m, l, c, (l + 1) * nb_col + c)
            elif dir == 'O' and rg == l:
                if c == 0:
                    matrice.set_valeur(m, l, c, val)
                    ejecte = (l + 1) * nb_col - 1
                else:
                    matrice.set_valeur(m, l, c, l * nb_col + c - 1)
            elif dir == 'E' and rg == l:
                if c == nb_col - 1:
                    matrice.set_valeur(m, l, c, val)
                    ejecte = l * nb_col
                else:
                    matrice.set_valeur(m, l, c, l * nb_col + c + 1)
            else:
                matrice.set_valeur(m, l, c, l * nb_col + c)
    return m, ejecte


# Affichage d'une matrice
def ligne_separatrice(mat, taille_cellule=4):
    """
    fonction annexe pour créer les lignes séparatrices
    paramètres: matrice la matrice à afficher
                taille_cellule la taille en nb de caractères d'une cellule
    résultat: cette fonction ne retourne rien mais fait un affichage
    """
    res = '\n'
    for i in range(matrice.get_nb_colonnes(mat) + 1):
        res += '-' * taille_cellule + '+'
    return res + '\n'


def matrice_to_str(mat, taille_cellule=4):
    """
    affiche le contenue d'une matrice présenté sous le format d'une grille
    paramètres: matrice la matrice à afficher
                taille_cellule la taille en nb de caractères d'une cellule
    résultat: cette fonction ne retourne rien mais fait un affichage
    """

    nb_colonnes = matrice.get_nb_colonnes(mat)
    nb_lignes = matrice.get_nb_lignes(mat)
    res = ' ' * taille_cellule + '|'
    for i in range(nb_colonnes):
        res += str(i).center(taille_cellule) + '|'
    res += ligne_separatrice(mat, taille_cellule)
    for i in range(nb_lignes):
        res += str(i).rjust(taille_cellule) + '|'
        for j in range(nb_colonnes):
            res += str(matrice.get_valeur(mat, i, j)).rjust(taille_cellule) + '|'
        res += ligne_separatrice(mat, taille_cellule)
    return res + '\n'


class TestMatrice(unittest.TestCase):

    def test_decalage_ligne_a_gauche(self):
        tests = [(7, 7), (3, 8)]
        for nb_lig, nb_col in tests:
            m_depart, _ = creer_matrice_test(nb_lig, nb_col)
            for l in range(nb_lig):
                m_travail, _ = creer_matrice_test(nb_lig, nb_col)
                m_attendu, e_attendue = creer_matrice_test(nb_lig, nb_col, 'E', l)
                e_travail = matrice.decalage_ligne_a_gauche(m_travail, l, -1)
                self.assertEqual(e_travail, e_attendue,
                                 "Le décalage à gauche en ligne " + str(l) + " pose problème sur la matrice \n" +
                                 matrice_to_str(m_depart) +
                                 "\n Résultat attendu : valeur ejectée " + str(e_attendue) + "\n" +
                                 matrice_to_str(m_attendu) +
                                 "\n Résultat obtenu : valeur ejectée " + str(e_travail) + "\n" +
                                 matrice_to_str(m_travail)
                                 )

    def test_decalage_ligne_a_droite(self):
        tests = [(7, 7), (3, 8)]
        for nb_lig, nb_col in tests:
            m_depart, _ = creer_matrice_test(nb_lig, nb_col)
            for l in range(nb_lig):
                m_travail, _ = creer_matrice_test(nb_lig, nb_col)
                m_attendu, e_attendue = creer_matrice_test(nb_lig, nb_col, 'O', l)
                e_travail = matrice.decalage_ligne_a_droite(m_travail, l, -1)
                self.assertEqual(e_travail, e_attendue,
                                 "Le décalage à droite en ligne " + str(l) + " pose problème sur la matrice \n" +
                                 matrice_to_str(m_depart) +
                                 "\n Résultat attendu : valeur ejectée " + str(e_attendue) + "\n" +
                                 matrice_to_str(m_attendu) +
                                 "\n Résultat obtenu : valeur ejectée " + str(e_travail) + "\n" +
                                 matrice_to_str(m_travail)
                                 )

    def test_decalage_ligne_en_haut(self):
        tests = [(7, 7), (3, 8)]
        for nb_lig, nb_col in tests:
            m_depart, _ = creer_matrice_test(nb_lig, nb_col)
            for l in range(nb_col):
                m_travail, _ = creer_matrice_test(nb_lig, nb_col)
                m_attendu, e_attendue = creer_matrice_test(nb_lig, nb_col, "S", l)
                e_travail = matrice.decalage_colonne_en_haut(m_travail, l, -1)
                self.assertEqual(e_travail, e_attendue,
                                 "Le décalage en haut en colonne " + str(l) + " pose problème sur la matrice \n" +
                                 matrice_to_str(m_depart) +
                                 "\n Résultat attendu : valeur ejectée " + str(e_attendue) + "\n" +
                                 matrice_to_str(m_attendu) +
                                 "\n Résultat obtenu : valeur ejectée " + str(e_travail) + "\n" +
                                 matrice_to_str(m_travail)
                                 )

    def test_decalage_ligne_en_bas(self):
        tests = [(7, 7), (3, 8)]
        for nb_lig, nb_col in tests:
            m_depart, _ = creer_matrice_test(nb_lig, nb_col)
            for l in range(nb_col):
                m_travail, _ = creer_matrice_test(nb_lig, nb_col)
                m_attendu, e_attendue = creer_matrice_test(nb_lig, nb_col, 'N', l)
                e_travail = matrice.decalage_colonne_en_bas(m_travail, l, -1)
                self.assertEqual(e_travail, e_attendue,
                                 "Le décalage en bas en colonne " + str(l) + " pose problème sur la matrice \n" +
                                 matrice_to_str(m_depart) +
                                 "\n Résultat attendu : valeur ejectée " + str(e_attendue) + "\n" +
                                 matrice_to_str(m_attendu) +
                                 "\n Résultat obtenu : valeur ejectée " + str(e_travail) + "\n" +
                                 matrice_to_str(m_travail)
                                 )


if __name__ == '__main__':
    unittest.main()
