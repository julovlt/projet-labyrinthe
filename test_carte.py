#!/usr/bin/python3
import unittest

import copy

import carte
import joueur


class TestCarte(unittest.TestCase):
    def setUp(self):
        self.O = 8
        self.S = 4
        self.E = 2
        self.N = 1
        self.liste_cartes = []
        self.liste_cartes_droite = []
        for i in range(16):
            self.liste_cartes.append(
                carte.Carte(i & self.N == self.N, i & self.E == self.E, i & self.S == self.S, i & self.O == self.O))
            self.liste_cartes_droite.append(
                carte.Carte(i & self.O == self.O, i & self.N == self.N, i & self.E == self.E, i & self.S == self.S))

    def test_est_valide(self):
        for i in range(16):
            if i in [7, 11, 13, 14, 15]:
                self.assertFalse(carte.est_valide(self.liste_cartes[i]), "la carte " + str(self.liste_cartes[i]) +
                                 "ne devrait pas être valide car elle ne possède qu'une ou 0 ouverture")
            else:
                self.assertTrue(carte.est_valide(self.liste_cartes[i]), "la carte " + str(self.liste_cartes[i]) +
                                "devrait être valide car elle possède 2, 3 ou 4 ouvertures")

    def test_mur_nord(self):
        for i in range(13):
            if i not in (7, 11):
                if i & self.N == self.N:
                    self.assertTrue(carte.mur_nord(self.liste_cartes[i]),
                                    "la carte " + str(self.liste_cartes[i]) + " devrait posséder un mur au nord")
                else:
                    self.assertFalse(carte.mur_nord(self.liste_cartes[i]), "la carte " + str(
                        self.liste_cartes[i]) + " ne devrait pas posséder de mur au nord")

    def test_mur_sud(self):
        for i in range(13):
            if i not in (7, 11):
                if i & self.S == self.S:
                    self.assertTrue(carte.mur_sud(self.liste_cartes[i]),
                                    "la carte " + str(self.liste_cartes[i]) + " devrait posséder un mur au sud")
                else:
                    self.assertFalse(carte.mur_sud(self.liste_cartes[i]),
                                     "la carte " + str(self.liste_cartes[i]) + " ne devrait pas posséder de mur au sud")

    def test_mur_ouest(self):
        for i in range(13):
            if i not in (7, 11):
                if i & self.O == self.O:
                    self.assertTrue(carte.mur_ouest(self.liste_cartes[i]),
                                    "la carte " + str(self.liste_cartes[i]) + " devrait posséder un mur à l'ouest")
                else:
                    self.assertFalse(carte.mur_ouest(self.liste_cartes[i]), "la carte " + str(
                        self.liste_cartes[i]) + " ne devrait pas posséder de mur à l'ouest")

    def test_mur_est(self):
        for i in range(13):
            if i not in (7, 11):
                if i & self.E == self.E:
                    self.assertTrue(carte.mur_est(self.liste_cartes[i]),
                                    "la carte " + str(self.liste_cartes[i]) + " devrait posséder un mur à l'est")
                else:
                    self.assertFalse(carte.mur_est(self.liste_cartes[i]), "la carte " + str(
                        self.liste_cartes[i]) + " ne devrait pas posséder de mur à l'est")

    def test_liste_joueurs(self):
        j1 = joueur.Joueur("joueur1", "gea")
        j2 = joueur.Joueur("joueur2", "info")
        l1 = [j1, j2]
        l2 = [j2]
        liste_tests = [[], l1, l2]
        liste_cartes = []
        for l in liste_tests:
            c = carte.Carte(True, False, True, False)
            if l != []:
                carte.set_liste_joueurs(c, l)
            liste_cartes.append(c)

        for i in range(len(liste_cartes)):
            joueurs_obtenus = carte.get_liste_joueurs(liste_cartes[i])
            joueurs_attendus = liste_tests[i]
            self.assertEqual(joueurs_obtenus, joueurs_attendus,
                             "la carte " + str(liste_cartes[i]) + " à laquelle on a attribué la liste de joueurs" +
                             str(joueurs_attendus) + " possède la liste de joueurs " + str(joueurs_obtenus) +
                             "\nCauses possibles: Joueur, Carte, set_liste_joueurs, get_liste_joueurs")

    def test_possede_joueur(self):
        j1 = joueur.Joueur("joueur1", "gea")
        j2 = joueur.Joueur("joueur2", "info")
        l1 = [j1, j2]
        l2 = [j2]
        liste_tests = [[], l1, l2]
        liste_cartes = []
        for l in liste_tests:
            c = carte.Carte(True, True, True, False)
            if l != []:
                carte.set_liste_joueurs(c, l)
            liste_cartes.append(c)
        for i in range(len(liste_cartes)):
            for jo in l2:
                attendu = jo in liste_tests[i]
                obtenu = carte.possede_joueur(liste_cartes[i], jo)
                if attendu:
                    msg = " devrait posséder le joueur " + str(jo) + " or la fonction possede_joueur retourne False"
                else:
                    msg = " ne devrait pas posséder le joueur " + str(
                        jo) + " or la fonction possede_joueur retourne True"
                self.assertEqual(obtenu, attendu,
                                 "la carte " + str(liste_cartes[i]) + " à laquelle on a attribué la liste de joueurs" +
                                 str(liste_tests[i]) + msg +
                                 "\nCauses possibles: Joueur, Carte, set_liste_joueurs, possede_joueur")

    def test_possede_pendre_joueur(self):
        j1 = joueur.Joueur("joueur1", "gea")
        j2 = joueur.Joueur("joueur2", "info")
        l1 = [j1, j2]
        l2 = [j2]
        liste_tests = [[], l1, l2]
        liste_cartes = []
        for l in liste_tests:
            c = carte.Carte(True, True, True, False)
            if l != []:
                carte.set_liste_joueurs(c, l)
            liste_cartes.append(c)
        for i in range(len(liste_cartes)):
            carte.prendre_joueur(liste_cartes[i], j2)
            attendu = False
            obtenu = carte.possede_joueur(liste_cartes[i], j2)
            msg = " ne devrait pas posséder le joueur " + str(j2) + " or la fonction possede_joueur retourne True"
            self.assertEqual(obtenu, attendu,
                             "la carte " + str(liste_cartes[i]) + " à laquelle on a attribué la liste de joueurs" +
                             str(liste_tests[i]) + " et à qui on a enlevé " + str(j2) + msg +
                             "\nCauses possibles: Joueur, Carte, set_liste_joueurs, possede_joueur, prendre_joueur")

    def test_possede_poser_joueur(self):
        j1 = joueur.Joueur("joueur1", "gea")
        j2 = joueur.Joueur("joueur2", "info")
        j3 = joueur.Joueur("joueur3", "gmp")
        l1 = [j1, j2]
        l2 = [j2]
        liste_tests = [[], l1, l2]
        liste_cartes = []
        for l in liste_tests:
            c = carte.Carte(True, True, True, False)
            if l != []:
                carte.set_liste_joueurs(c, l)
            liste_cartes.append(c)
        for i in range(len(liste_cartes)):
            carte.poser_joueur(liste_cartes[i], j3)
            attendu = True
            obtenu = carte.possede_joueur(liste_cartes[i], j3)
            msg = " devrait posséder le joueur " + str(j3) + " or la fonction possede_joueur retourne False"
            self.assertEqual(obtenu, attendu,
                             "la carte " + str(liste_cartes[i]) + " à laquelle on a attribué la liste de joueurs" +
                             str(liste_tests[i]) + " et à qui on a ajouté " + str(j3) + msg +
                             "\nCauses possibles: Joueur, Carte, set_liste_joueurs, possede_joueur, ajouter_joueur")

    def test_tourner_horaire(self):
        for i in range(13):
            if i not in (7, 11):
                c = copy.deepcopy(self.liste_cartes[i])
                carte.tourner_horaire(c)
                self.assertEqual(c, self.liste_cartes_droite[i], "problème avec la fonction l'appel tourner_horaire(" +
                                 str(self.liste_cartes[i]) + ")\nRésultat attendu " + str(self.liste_cartes_droite[i]) +
                                 "\nRésultat obtenu " + str(c))

    def test_tourner_antihoraire(self):
        for i in range(13):
            if i not in (7, 11):
                c = copy.deepcopy(self.liste_cartes_droite[i])
                carte.tourner_antihoraire(c)
                self.assertEqual(c, self.liste_cartes[i], "problème avec la fonction l'appel tourner_antihoraire(" +
                                 str(self.liste_cartes_droite[i]) + ")\nRésultat attendu " + str(self.liste_cartes[i]) +
                                 "\nRésultat obtenu " + str(c))

    def test_get_objet(self):
        c1 = carte.Carte(True, False, True, False)
        c2 = carte.Carte(True, False, True, False, 2)
        self.assertEqual(carte.get_objet(c1), 0,
                         "la carte " + str(c1) + " ne possède aucun objet => valeur attendue 0\n" +
                         "Le problème vient sans doute de la fonction Carte ou de la fonction get_objet")
        self.assertEqual(carte.get_objet(c2), 2,
                         "la carte " + str(c2) + " possède l'objet 2 => valeur attendue 2\n" +
                         "Le problème vient sans doute de la fonction Carte ou de la fonction get_objet")

    def test_get_objet_poser_objet(self):
        c = carte.Carte(True, True, True, False, 2)
        for i in range(3):
            carte.poser_objet(c, i)
            obj = carte.get_objet(c)
            self.assertEqual(obj, i, "la carte " + str(c) + " sur laquelle on a posé l'objet " + str(i) +
                             " devrait posséder cet objet or la fonction get_objet retourne " + str(obj) +
                             "\nCauses possibles: Carte, poser_objet, get_objet"
                             )

    def test_get_set_couleur(self):
        c = carte.Carte(True, True, True, False, 2)
        for coul in ["gea", "gmp", "aucune", "info"]:
            carte.set_couleur(c, coul)
            obtenue = carte.get_couleur(c)
            self.assertEqual(coul, obtenue, "la carte " + str(c) + " dont la couleur a été mise à " + str(coul) +
                             " devrait avoir cette couleur or la fonction get_couleur retourne " + str(obtenue) +
                             "\nCauses possibles: Carte, set_couleur, get_couleur")

    def test_get_objet_prendre_objet(self):
        liste_cartes = []
        for i in range(4):
            c = carte.Carte(False, True, True, False, i)
            liste_cartes.append(c)
        for c in liste_cartes:
            carte.prendre_objet(c)
            obj = carte.get_objet(c)
            self.assertEqual(obj, 0, "la carte " + str(c) + " à laquelle on a enlevé son objet " +
                             " ne devrait posséder aucun objet or la fonction get_objet retourne " + str(obj) +
                             "\nCauses possibles: Carte, prendre_objet, get_objet"
                             )

    def test_coder_murs(self):
        for i in range(16):
            res = carte.coder_murs(self.liste_cartes[i])
            self.assertEqual(res, i, "la carte " + str(self.liste_cartes[i]) +
                             " devrait avoir pour code " + str(i) + " mais coder_mur a retourné " + str(res))

    def test_decoder_murs(self):
        c = carte.Carte(True, True, True, True)
        for i in range(16):
            carte.decoder_murs(c, i)
            self.assertEqual(c, self.liste_cartes[i], "le resultat de decoder_mur avec le code " + str(i) +
                             " aurait du donner " + str(self.liste_cartes[i]) + " mais on a obtenu " + str(c))

    def test_to_char(self):
        for i in range(16):
            carac = carte.to_char(self.liste_cartes[i])
            self.assertEqual(carac, carte.liste_cartes[i], "la carte " + str(self.liste_cartes[i]) +
                             " devrait avoir pour caractère " + carte.liste_cartes[i] + " mais to_char retourne " + str(
                carac))

    def message_passage(self, direction, existe, c1, c2):
        commun = " passage direction " + direction + " entre " + str(c1) + " et " + str(
            c2) + " mais la fonction passage" + \
                 direction + " "
        if existe:
            return "il existe un" + commun + "ne le trouve pas"
        else:
            return "il n'existe pas de" + commun + "en trouve un"

    def test_passage_nord(self):
        for i in range(13):
            if i not in (7, 11):
                for j in range(13):
                    if j not in (7, 11):
                        passage = i & self.N == 0 and j & self.S == 0
                        self.assertEqual(carte.passage_nord(self.liste_cartes[i], self.liste_cartes[j]), passage,
                                         self.message_passage("Nord", passage, self.liste_cartes[i],
                                                              self.liste_cartes[j]))

    def test_passage_sud(self):
        for i in range(13):
            if i not in (7, 11):
                for j in range(13):
                    if j not in (7, 11):
                        passage = i & self.S == 0 and j & self.N == 0
                        self.assertEqual(carte.passage_sud(self.liste_cartes[i], self.liste_cartes[j]), passage,
                                         self.message_passage("Sud", passage, self.liste_cartes[i],
                                                              self.liste_cartes[j]))

    def test_passage_est(self):
        for i in range(13):
            if i not in (7, 11):
                for j in range(13):
                    if j not in (7, 11):
                        passage = i & self.E == 0 and j & self.O == 0
                        self.assertEqual(carte.passage_est(self.liste_cartes[i], self.liste_cartes[j]), passage,
                                         self.message_passage("Est", passage, self.liste_cartes[i],
                                                              self.liste_cartes[j]))

    def test_passage_ouest(self):
        for i in range(13):
            if i not in (7, 11):
                for j in range(13):
                    if j not in (7, 11):
                        passage = i & self.O == 0 and j & self.E == 0
                        self.assertEqual(carte.passage_ouest(self.liste_cartes[i], self.liste_cartes[j]), passage,
                                         self.message_passage("Ouest", passage, self.liste_cartes[i],
                                                              self.liste_cartes[j]))


if __name__ == '__main__':
    unittest.main()
