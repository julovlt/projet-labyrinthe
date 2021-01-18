#!/usr/bin/python3
import unittest
import joueur


class TestCaseJoueur(unittest.TestCase):
    def setUp(self):
        self.les_joueurs = [
            ("joueur1", "info", 10, 5, 'O', 0, 0, joueur.dummy_ai),
            ("joueur2", "info", 7, 4, 'H', 1, 5, joueur.dummy_ai),
            ("joueur3", "gmp", 14, 4, 'H', 2, 10, joueur.dummy_ai),
            ("joueur4", "gmp", 3, 4, 'H', 2, 10, joueur.dummy_ai),
            ("joueur5", "gte", 2, 0, 'O', 3, 7, len),
            ("joueur6", "info", 2, 0, 'O', 3, 7, joueur.dummy_ai)
        ]
        self.objets = [(1, 10), (2, 12), (3, 6), (2, 12), (3, 6), (2, 13)]

    def test_ajouter_objet(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            j_apres = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            joueur.ajouter_objet(j_apres, self.objets[i][0], self.objets[i][1])
            resultat = joueur.get_objet_joueur(j_apres)
            self.assertEqual(resultat,
                             self.objets[i][0],
                             "Après avoir ajouté l'objet " + str(self.objets[i][0]) + " au joueur "
                             + str(j_avant) + "la fonction get_objet_joueur devrait retourner " + str(
                                 self.objets[i][0]) +
                             " or elle retourne " + str(resultat) +
                             "\nCauses possibles: Joueur, ajouter_objet, get_objet_joueur")

    def test_mise_a_jour_temps_complet(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            j_apres = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            joueur.ajouter_objet(j_avant, self.objets[i][0], self.objets[i][1])
            joueur.ajouter_objet(j_apres, self.objets[i][0], self.objets[i][1])

            for nb in range(self.objets[i][1] + 1):
                joueur.mise_a_jour_temps(j_apres)
            resultat = joueur.get_objet_joueur(j_apres)
            self.assertEqual(resultat,
                             0,
                             "Après avoir ajouté l'objet " + str(self.objets[i][0]) + " au joueur "
                             + str(j_avant) + " avec une durée de valité " + str(self.objets[i][1]) +
                             " puis avoir appeler " + str(self.objets[i][1] + 1) + " la fonction mise_a_jour_temps " +
                             " le joueur ne devrait plus avoir l'objet or on obtient " + str(resultat) +
                             "\nCauses possibles: Joueur, ajouter_objet, get_objet_joueur, mise_a_jour_temps")

    def test_mise_a_jour_temps(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            j_apres = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)

            joueur.mise_a_jour_temps(j_apres)
            resultat = joueur.get_temps_restant(j_apres)
            self.assertEqual(resultat, max(temps-1,0),
                             "Après avoir appliqué mise_a_jour_temps au joueur "
                             + str(j_avant) + " la fonction get_temps_restant retourne "+ str(resultat) +
                             " or elle devrait retourner "+str(max(temps-1,0))+
                             "\nCauses possibles: Joueur, mise_a_jour_temps, get_temps_restant")

    def test_set_type_joueur(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            for type_j in 'OH':
                j_apres = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
                joueur.set_type_joueur(j_apres, type_j)
                resultat = joueur.get_type_joueur(j_apres)
                self.assertEqual(resultat,
                                 type_j,
                                 "Après avoir positionné le type du joueur "
                                 + str(j_avant) + " à " + type_j + " la fonction get_type_joueur retourne " +
                                 str(resultat) + "\nCauses possibles: Joueur, get_type_joueur, set_type_joueur")

    def test_set_surface(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            for surf in [12, 8, 6]:
                j_apres = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
                joueur.set_surface(j_apres, surf)
                resultat = joueur.get_surface(j_apres)
                self.assertEqual(resultat,
                                 surf,
                                 "Après avoir affecté la surface du joueur "
                                 + str(j_avant) + " à " + str(surf) + " la fonction get_surface retourne " +
                                 str(resultat) + "\nCauses possibles: Joueur, get_surface, set_surface")

    def test_get_couleur_joueur(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            resultat = joueur.get_couleur_joueur(j_avant)
            self.assertEqual(resultat,
                             couleur,
                             "La couleur du joueur " + str(j_avant) + " devrait être " + couleur +
                             " or la fonction get_couleur_joueur retourne " + str(resultat) +
                             "\nCauses possibles: Joueur, get_couleur_joueur")

    def test_get_nom_joueur(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            resultat = joueur.get_nom_joueur(j_avant)
            self.assertEqual(resultat,
                             nom,
                             "Le nom du joueur " + str(j_avant) + " devrait être " + nom +
                             " or la fonction get_nom_joueur retourne " + str(resultat) +
                             "\nCauses possibles: Joueur, get_nom_joueur")

    def test_get_reserve_peinture(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            resultat = joueur.get_reserve_peinture(j_avant)
            self.assertEqual(resultat,
                             reserve,
                             "La réserve du joueur " + str(j_avant) + " devrait être " + str(reserve) +
                             " or la fonction get_reserve_peinture retourne " + str(resultat) +
                             "\nCauses possibles: Joueur, get_reserve_peinture")

    def test_get_temps_restant(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            resultat = joueur.get_temps_restant(j_avant)
            self.assertEqual(resultat,
                             temps,
                             "Le temps restant de l'objet du joueur " + str(j_avant) + " devrait être " + str(temps) +
                             " or la fonction get_temps_restant retourne " + str(resultat) +
                             "\nCauses possibles: Joueur, get_temps_restant")

    def test_get_objet_joueur(self):
        i = 0
        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            j_avant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            resultat = joueur.get_objet_joueur(j_avant)
            self.assertEqual(resultat,
                             objet,
                             "Le temps restant de l'objet du joueur " + str(j_avant) + " devrait être " + str(objet) +
                             " or la fonction get_temps_restant retourne " + str(resultat) +
                             "\nCauses possibles: Joueur, get_objet_joueur")

    def test_comparer_joueur(self):
        joueur_prec = None
        reserve_prec = None
        surface_prec = None

        for nom, couleur, reserve, surface, type_j, objet, temps, ia in self.les_joueurs:
            joueur_courant = joueur.Joueur(nom, couleur, reserve, surface, type_j, objet, temps, ia)
            if joueur_prec is not None:
                resultat = joueur.comparer(joueur_prec, joueur_courant)
                if surface_prec > surface:
                    attendu = 1
                elif surface_prec < surface:
                    attendu = -1
                elif reserve_prec > reserve:
                    attendu = 1
                elif reserve_prec < reserve:
                    attendu = -1
                else:
                    attendu = 0

                self.assertEqual(resultat,attendu,
                                 "La comparaison entre "+str(joueur_prec)+ " et "+str(joueur_courant)+
                                 " devrait donner "+ str(attendu) + " or elle retourne "+ str(resultat) +
                                 "\nCauses possibles: Joueur, comparer")
            joueur_prec=joueur_courant
            reserve_prec=reserve
            surface_prec=surface


if __name__ == '__main__':
    unittest.main()
