#!/usr/bin/python3
import unittest
import participants


class TestCaseParticipants(unittest.TestCase):
    def setUp(self):
        self.noms = [[], ["Marie", "Samir", "Paul", "Sonia"], ["Samir", "Paul", "Marie"], ["Sonia", "Marie"]]
        self.les_couleurs = [[], ["info", "gmp", "chimie", "gte"], ["chimie", "gea", "info"], ["qlio", "gmp"]]
        self.humains = [True, True, False, False]
        self.surfaces = {"info": 35, "gmp": 12, "chimie": 12, "gea": 8, "qlio": 4, "gte": 0}

    def test_nb_joueurs(self):
        partis = []
        for i in range(len(self.noms)):
            p = participants.Participants(self.noms[i], self.les_couleurs[i], self.humains[i])
            partis.append(p)
        for i in range(len(partis)):
            nb_attendus = len(self.noms[i])
            nb_retournes = participants.get_nb_joueurs(partis[i])
            self.assertEqual(nb_retournes, nb_attendus,
                             "Après avoir créé la liste des participants à partir des noms " + str(self.noms[i]) +
                             " le nombre de joueurs devrait être " + str(nb_attendus) +
                             " or la fonction get_nb_joueurs retourne " + str(nb_retournes) +
                             "\nCauses possibles: Participants, get_nb_joueurs")

    def test_get_joueur_par_num(self):
        partis = []
        for i in range(len(self.noms)):
            p = participants.Participants(self.noms[i], self.les_couleurs[i], self.humains[i])
            partis.append(p)
        for i in range(len(partis)):
            for j in range(len(self.noms[i])):
                le_joueur = participants.get_joueur_par_num(partis[i], j + 1)
                joueur_attendu = participants.Joueur(self.noms[i][j], self.les_couleurs[i][j])
                if j == 0 and self.humains[i]:
                    participants.set_type_joueur(joueur_attendu, "H")
                self.assertEqual(le_joueur, joueur_attendu,
                                 "Après avoir créé la liste des participants à partir des noms " + str(self.noms[i]) +
                                 " et des couleurs " + str(self.les_couleurs[i]) + " le joueur numéro " + str(j + 1) +
                                 " devrait être " + str(joueur_attendu) + " or il vaut " + str(le_joueur) +
                                 "\nCauses possibles: Participants, get_joueur_par_num, Joueur")

    def test_get_joueur_par_nom(self):
        partis = []
        for i in range(len(self.noms)):
            p = participants.Participants(self.noms[i], self.les_couleurs[i], self.humains[i])
            partis.append(p)
        for i in range(len(partis)):
            for j in range(len(self.noms[i])):
                le_joueur = participants.get_joueur_par_nom(partis[i], self.noms[i][j])
                joueur_attendu = participants.Joueur(self.noms[i][j], self.les_couleurs[i][j])
                if j == 0 and self.humains[i]:
                    participants.set_type_joueur(joueur_attendu, "H")
                self.assertEqual(le_joueur, joueur_attendu,
                                 "Après avoir créé la liste des participants à partir des noms " + str(self.noms[i]) +
                                 " et des couleurs " + str(self.les_couleurs[i]) + " le joueur de nom " +
                                 str(self.noms[i][j]) +
                                 " devrait être " + str(joueur_attendu) + " or il vaut " + str(le_joueur) +
                                 "\nCauses possibles: Participants, get_joueur_par_nom, Joueur")

    def test_joueur_courant(self):
        partis = []
        for i in range(len(self.noms)):
            p = participants.Participants(self.noms[i], self.les_couleurs[i], self.humains[i])
            partis.append(p)
        for i in range(1, len(partis)):
            for j in range(len(self.noms[i])):
                participants.set_joueur_courant(partis[i], j + 1)
                num_courant = participants.get_num_joueur_courant(partis[i])
                self.assertEqual(num_courant, j + 1,
                                 "Après avoir choisi le joueur courant avec la fonction set_joueur_courant à " +
                                 str(j + 1) +
                                 " la fonction get_num_joueur_courant retourne " + str(num_courant) +
                                 "\nCauses possibles: Participants, set_joueur_courant, get_joueur_courant")

    def test_premier_joueur(self):
        partis = []
        for i in range(len(self.noms)):
            p = participants.Participants(self.noms[i], self.les_couleurs[i], self.humains[i])
            partis.append(p)
        for i in range(1, len(partis)):
            for j in range(len(self.noms[i])):
                participants.init_premier_joueur(partis[i], j + 1)
                num_premier = participants.get_num_premier_joueur(partis[i])
                self.assertEqual(num_premier, j + 1,
                                 "Après avoir positionné le premier joueur avec la fonction init_premier_joueur à "
                                 + str(j + 1) +
                                 " la fonction get_num_premier_joueur retourne " + str(num_premier) +
                                 "\nCauses possibles: Participants, init_premier_joueur, get_num_premier_joueur")

    def test_ajouter_joueur(self):
        part = participants.Participants([], [])
        nb_part = participants.get_nb_joueurs(part)
        self.assertEqual(nb_part, 0,
                         "Après avoir créé la liste des participants à partir d'une liste vide de noms " +
                         " le nombre de joueurs devrait être 0 " +
                         " or la fonction get_nb_joueurs retourne " + str(nb_part) +
                         "\nCauses possibles: Participants, get_nb_joueurs")
        for i in range(len(self.noms[1])):
            le_joueur = participants.Joueur(self.noms[1][i], self.les_couleurs[1][i])
            participants.ajouter_joueur(part, le_joueur)
            nb_part = participants.get_nb_joueurs(part)
            self.assertEqual(nb_part, i + 1,
                             "Après avoir créé la liste des participants à partir d'une liste vide de noms " +
                             " et ajouté " + str(i + 1) + " joueurs, le nombre de joueurs devrait être " + str(i + 1) +
                             " or la fonction get_nb_joueurs retourne " + str(nb_part) +
                             "\nCauses possibles: Participants, ajouter_joueur, get_nb_joueurs")
            joueur_ret = participants.get_joueur_par_num(part, i + 1)
            self.assertEqual(joueur_ret, le_joueur,
                             "Après avoir créé la liste des participants à partir d'une liste vide de noms " +
                             " et ajouté le joueur " + str(le_joueur) + " en " + str(i + 1) + "eme" +
                             " la fonction get_joueur_par_num avec " + str(i + 1) + " retourne " + str(joueur_ret) +
                             "\nCauses possibles: Participants, ajouter_joueur, get_joueur_par_num")

    def test_changer_joueur_courant(self):
        partis = []
        premier = 2
        for i in range(1, len(self.noms)):
            p = participants.Participants(self.noms[i], self.les_couleurs[i], self.humains[i])
            partis.append(p)
        for i in range(len(partis)):
            participants.init_premier_joueur(partis[i], premier)
            participants.set_joueur_courant(partis[i], premier)
            num_j = participants.get_num_joueur_courant(partis[i])
            self.assertEqual(num_j, premier,
                             "Après avoir créé la liste des participants avec les noms " + str(self.noms[i + 1]) +
                             " et positionné le premier joueur à " + str(premier) +
                             " le numéro du joueur courant devrait être " + str(premier) +
                             " or la fonction get_num_joueur_courant retourne " + str(num_j) +
                             "\nCauses possibles: Participants, init_premier_joueur, get_num_joueur_courant")
            attendu = premier
            nb_joueurs = len(self.noms[i + 1])
            for j in range(2 * nb_joueurs):
                attendu += 1
                if attendu > nb_joueurs:
                    attendu = 1
                changement_tour = participants.changer_joueur_courant(partis[i])
                changement_attendu = j % nb_joueurs == nb_joueurs - 1
                self.assertEqual(changement_tour, changement_attendu,
                                 "Après avoir créé la liste des participants à partir des noms " + str(
                                     self.noms[i + 1]) +
                                 " positionné le premier joueur à " + str(premier) +
                                 " et changé " + str(j + 1) +
                                 " fois de joueur courant le changement de tour devrait être " +
                                 ("vrai" if changement_attendu else "faux") +
                                 " or la fonction changer_joueur_courant retourne " +
                                 ("vrai" if changement_tour else "faux") +
                                 "\nCauses possibles: Participants, changer_joueur_courant")
                retourne = participants.get_num_joueur_courant(partis[i])
                self.assertEqual(retourne, attendu,
                                 "Après avoir créé la liste des participants à partir des noms " + str(
                                     self.noms[i + 1]) +
                                 " positionné le premier joueur à " + str(premier) +
                                 " et changé " + str(j + 1) +
                                 " fois de joueur courant, le numéro de joueur courant devrait être " +
                                 str(attendu) + " or la fonction get_num_joueur_courant retourne " + str(retourne) +
                                 "\nCauses possibles: Participants, get_joueur_par_num, changer_joueur_courant")

    def test_mise_a_jour_surface(self):
        partis = []
        for i in range(len(self.noms)):
            p = participants.Participants(self.noms[i], self.les_couleurs[i], self.humains[i])
            partis.append(p)
        for i in range(len(partis)):
            participants.mise_a_jour_surface(partis[i], self.surfaces)
            for j in range(len(self.noms[i])):
                joueur = participants.get_joueur_par_num(partis[i], j + 1)
                surf = participants.get_surface(joueur)
                coul = participants.get_couleur_joueur(joueur)
                self.assertEqual(surf, self.surfaces[coul],
                                 str(partis[i]) + "\n" +
                                 "Après avoir créé la liste des participants à partir des noms " +
                                 str(self.noms[i]) + " et mis à jour les surfaces avec la liste " +
                                 str(self.surfaces) + " le joueur numéro " + str(j + 1) +
                                 " devrait avoir une surface de " + str(self.surfaces[coul]) +
                                 " or on retrouve une surface  de " + str(surf) +
                                 "\nCauses possibles: Participants, mise_a_jour_surface, get_joueur_par_num, " +
                                 "get_surface ou get_couleur_joueur")

    def test_classement_joueurs(self):
        partis = []
        for i in range(len(self.noms)):
            p = participants.Participants(self.noms[i], self.les_couleurs[i], self.humains[i])
            partis.append(p)
        for i in range(len(partis)):
            participants.mise_a_jour_surface(partis[i], self.surfaces)
            classement = participants.classement_joueurs(partis[i])
            if classement != None:
                self.assertEqual(len(classement), len(self.noms[i]),
                                 "Le classement des participants créés à partir de " + str(self.noms[i]) +
                                 " devrait contenir " + str(len(self.noms[i])) + " joueurs or il en contient " +
                                 str(len(classement)) +
                                 "\nCauses possibles: Participants, mise_a_jour_surface,classement_joueurs")
                for j in range(len(classement) - 1):
                    self.assertGreaterEqual(participants.comparer(classement[j], classement[j + 1]), 0,
                                            "Le classement des participants créés à partir de " + str(self.noms[i]) +
                                            " ayant pour couleur respective " + str(
                                                self.les_couleurs) + " et les surfaces " + str(self.surfaces) +
                                            " contient deux joueurs qui ne sont pas triés dans bon ordre " +
                                            "en position " + str(j) + "\n voici le classement " + str(classement) +
                                            "\nCauses possibles: Participants, mise_a_jour_surface, comparer, classement_joueurs"
                                            )


if __name__ == '__main__':
    unittest.main()
