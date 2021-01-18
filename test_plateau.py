#!/usr/bin/python3
import unittest
import plateau
import matrice


def plateau_to_str(plat):
    """
    affichage redimentaire d'un plateau

    :param plat: le plateau
    :return: rien mais affiche le plateau
    """
    res = '\n '

    for i in range(1, 7, 2):
        res += " " + str(i)
    res += '\n'

    for i in range(plateau.get_nb_lignes(plat)):
        if i % 2 == 0:
            res += ' '
        else:
            res += str(i)
        for j in range(plateau.get_nb_colonnes(plat)):
            res += plateau.to_char(plateau.get_valeur(plat, i, j))
        if i % 2 == 0:
            res += ' '
        else:
            res += str(i)
        res += '\n'
    res += ' '
    for i in range(1, 7, 2):
        res += " " + str(i)
    return res + '\n'


def forcer_cartes_from_str(plat, cartes):
    for i in range(len(cartes)):
        code = plateau.liste_cartes.index(cartes[i])
        plateau.decoder_murs(plateau.get_valeur(plat, i // 7, i % 7), code)


def nb_atteignables(plat, debut, pas, borne, liste_depart, liste_arrivee, mur):
    ici = debut
    cpt = 1
    fini = False
    while not fini:
        if ici <= borne <= ici + pas or ici >= borne >= ici + pas:
            fini = True
        elif plat[ici] not in liste_depart or plat[ici + pas] not in liste_arrivee:
            if mur:
                mur = False
                cpt += 1
            else:
                fini = True
        else:
            cpt += 1
        ici += pas
    return cpt


class TestPlateau(unittest.TestCase):

    def test_init_plateau_cartes(self):
        participants = plateau.Participants(["joueur1", "joueur2"], ["info", "gea"])
        mat, carte_sup = plateau.Plateau(participants)
        codes_attendus = [9, 3, 12, 6]
        noms_angle = ["supérieur gauche", "supérieur droit", "inférieur gauche", "inférieur droit"]
        num_angle = 0
        for lin in range(0, 7, 6):
            for col in range(0, 7, 6):
                code_obtenu = plateau.coder_murs(plateau.get_valeur(mat, lin, col))
                self.assertEqual(code_obtenu, codes_attendus[num_angle],
                                 "L'angle " + noms_angle[num_angle] + " de votre plateau n'est pas correct. " +
                                 "Ce devrait être " + plateau.liste_cartes[codes_attendus[num_angle]] +
                                 " or vous avez " + plateau.liste_cartes[code_obtenu] +
                                 plateau_to_str(mat) +
                                 "\nCauses possibles: Plateau, get_valeur, coder_murs ")
                num_angle += 1
        cartes_fixes = {1: [0, 2, 0, 4, 2, 4], 2: [2, 6, 4, 6, 4, 4], 4: [6, 2, 6, 4, 4, 2], 8: [2, 0, 4, 0, 2, 2]}
        for code_attendu in cartes_fixes:
            for i in range(0, len(cartes_fixes[code_attendu]), 2):
                code_obtenu = plateau.coder_murs(plateau.get_valeur(mat, cartes_fixes[code_attendu][i],
                                                                    cartes_fixes[code_attendu][i + 1]))
                self.assertEqual(code_obtenu, code_attendu,
                                 "La carte fixe en position " + str((cartes_fixes[code_attendu][i],
                                                                     cartes_fixes[code_attendu][i + 1])) +
                                 " de votre plateau n'est pas correcte. " +
                                 "Ce devrait être " + plateau.liste_cartes[code_attendu] +
                                 " or vous avez " + plateau.liste_cartes[code_obtenu] +
                                 plateau_to_str(mat) +
                                 "\nCauses possibles: Plateau, get_valeur, coder_murs")
        compteurs = {"angle": 0, "toute droite": 0, "jonction": 0, "inconnue": 0}
        for lin in range(7):
            for col in range(7):
                code_obtenu = plateau.coder_murs(plateau.get_valeur(mat, lin, col))
                if code_obtenu in [3, 6, 9, 12]:
                    compteurs["angle"] += 1
                elif code_obtenu in [1, 2, 4, 8]:
                    compteurs["jonction"] += 1
                elif code_obtenu in [5, 10]:
                    compteurs["toute droite"] += 1
                else:
                    compteurs["inconnu"] += 1
        cs = plateau.coder_murs(carte_sup)
        if cs in [3, 6, 9, 12]:
            compteurs["angle"] += 1
        elif cs in [1, 2, 4, 8]:
            compteurs["jonction"] += 1
        elif cs in [5, 10]:
            compteurs["toute droite"] += 1
        else:
            compteurs["inconnue"] += 1
        compteurs_attendus = {"angle": 20, "toute droite": 12, "jonction": 18, "inconnue": 0}
        self.assertEqual(compteurs, compteurs_attendus,
                         "Le nombre de cartes de chaque catégorie n'est pas correct. On attend " +
                         str(compteurs_attendus) + " or on obtient " + str(compteurs) +
                         plateau_to_str(mat) +
                         "\nCauses possibles: Plateau, get_valeur, coder_murs")

    def test_init_plateau_joueurs(self):
        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        for i in range(3, 5):
            participants = plateau.Participants(noms[:i], couleurs[:i])
            mat, carte_sup = plateau.Plateau(participants)
            noms_retrouves = []
            for lin in range(0, 7, 6):
                for col in range(0, 7, 6):
                    carte = plateau.get_valeur(mat, lin, col)
                    liste_joueurs = plateau.get_liste_joueurs(carte)
                    self.assertLess(len(liste_joueurs), 2,
                                    "Après avoir créer un plateau avec les joueurs " + str(noms) +
                                    " la carte fixe en position " + str((lin, col)) +
                                    " du plateau contient plus d'un joueur. " +
                                    "Voici la liste des joueurs " + str(liste_joueurs) +
                                    "\nCauses possibles: Plateau, get_valeur, get_liste_joueurs")
                    if liste_joueurs != []:
                        noms_retrouves.append(plateau.get_nom_joueur(liste_joueurs[0]))
            noms_retrouves.sort()
            self.assertEqual(noms_retrouves, noms[:i],
                             "Après avoir créer un plateau avec les joueurs " + str(noms) +
                             " on retrouve les joueurs suivant sur le plateau " + str(noms_retrouves) +
                             "\nCauses possibles: Plateau, get_valeur, get_liste_joueurs, get_nom_joueur")

    def test_init_plateau_objets(self):
        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        for i in range(3, 5):
            participants = plateau.Participants(noms[:i], couleurs[:i])
            mat, carte_sup = plateau.Plateau(participants)
            compteurs_obtenus = {0: 0, 1: 0, 2: 0, 3: 0}
            compteurs_attendus = {0: 49 - 3 * i, 1: i, 2: i, 3: i}
            for lin in range(7):
                for col in range(7):
                    carte = plateau.get_valeur(mat, lin, col)
                    objet = plateau.get_objet(carte)
                    self.assertIn(objet, [0, 1, 2, 3],
                                  "Après avoir créer un plateau avec les joueurs " + str(noms) +
                                  " la carte en position " + str((lin, col)) +
                                  " du plateau contient un objet inconnu " + str(objet) +
                                  "\nCauses possibles: Plateau, get_valeur, get_objet")
                    compteurs_obtenus[objet] += 1
            self.assertEqual(compteurs_obtenus, compteurs_attendus,
                             "Après avoir créer un plateau avec les joueurs " + str(noms) +
                             " on devrait avoir autant d'objets de chaque sorte or on trouve " +
                             str(compteurs_obtenus[1]) + " bombes, " + str(compteurs_obtenus[2]) + " pistolets et " +
                             str(compteurs_obtenus[3]) + " boucliers" +
                             "\nCauses possibles: Plateau, get_valeur, get_liste_joueurs, get_objet")

    def test_get_coordonnee_joueur(self):
        for lin, col in [(0, 3), (2, 4), (6, 5), (3, 6), (4, 0)]:
            noms = ["joueur1", "joueur2"]
            couleurs = ["info", "gea"]
            joueur_recherche = plateau.Joueur("Mister X", "chimie")
            part = plateau.Participants(noms, couleurs)
            mat, carte_sup = plateau.Plateau(part)
            plateau.poser_joueur(plateau.get_valeur(mat, lin, col), joueur_recherche)
            lin_trouvee, col_trouvee = plateau.get_coordonnees_joueur(mat, joueur_recherche)
            self.assertEqual((lin_trouvee, col_trouvee), (lin, col),
                             "Après avoir créer un plateau sur lequel on a posé le joueur " + str(joueur_recherche) +
                             " en position " + str((lin, col)) + " on recherche ce joueur mais on le trouve en " +
                             str((lin_trouvee, col_trouvee)) +
                             "\nCauses possibles: Plateau, get_valeur, poser_joueur, get_coordonnees_joueur")

    def test_passage_plateau(self):
        plateaux = [
            "╔║╦╚╦═╗" +
            "╦╚═╚║═║" +
            "╠╗╠║╦╣╣" +
            "║╚╔╝╦╝║" +
            "╠╦╩═╣╦╣" +
            "╝╗╠╗═╔╗" +
            "╚╔╩╝╩╔╝",
            "╔╔╦╠╦╔╗" +
            "╚══╝╝╝╔" +
            "╠╦╠╔╦╔╣" +
            "═║╝╔╗║╝" +
            "╠╝╩╠╣╦╣" +
            "║╚╝╣║═║" +
            "╚║╩╠╩║╝"]
        sud_libre = ['╦', '╗', '╣', '╠', '║', '╔']
        nord_libre = ['╣', '╩', '╝', '╠', '║', '╚']
        est_libre = ['╦', '╩', '═', '╠', '╔', '╚']
        ouest_libre = ['╦', '╣', '╗', '╩', '═', '╝']

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        participants = plateau.Participants(noms, couleurs)
        mat, carte_sup = plateau.Plateau(participants)
        for plat in plateaux:
            forcer_cartes_from_str(mat, plat)
            for rangee in range(7):
                res = plateau.passage_plateau(mat, 0, rangee, 'N')
                self.assertIsNone(res,
                                  "Sur le plateau ci-dessous il ne devrait pas y avoir de passage vers le nord en " +
                                  str((0, rangee)) + "or votre fonction passage_plateau retourne " + str(res) +
                                  plateau_to_str(mat) +
                                  "\nCauses possibles: Plateau, get_valeur, passage_plateau")
                res = plateau.passage_plateau(mat, 6, rangee, 'S')
                self.assertIsNone(res,
                                  "Sur le plateau ci-dessous il ne devrait pas y avoir de passage vers le sud en " +
                                  str((6, rangee)) + "or votre fonction passage_plateau retourne " + str(res) +
                                  plateau_to_str(mat) +
                                  "\nCauses possibles: Plateau, get_valeur, passage_plateau")
                res = plateau.passage_plateau(mat, rangee, 0, 'O')
                self.assertIsNone(res,
                                  "Sur le plateau ci-dessous il ne devrait pas y avoir de passage vers l'ouest en " +
                                  str((rangee, 0)) + "or votre fonction passage_plateau retourne " + str(res) +
                                  plateau_to_str(mat) +
                                  "\nCauses possibles: Plateau, get_valeur, passage_plateau")
                res = plateau.passage_plateau(mat, rangee, 6, 'E')
                self.assertIsNone(res,
                                  "Sur le plateau ci-dessous il ne devrait pas y avoir de passage vers l'est en " +
                                  str((rangee, 6)) + " or votre fonction passage_plateau retourne " + str(res) +
                                  plateau_to_str(mat) +
                                  "\nCauses possibles: Plateau, get_valeur, passage_plateau")
        for ligne in range(1, 6):
            for col in range(1, 6):
                carte_testee = plat[ligne * 7 + col]
                carte_dessus = plat[(ligne - 1) * 7 + col]
                carte_dessous = plat[(ligne + 1) * 7 + col]
                carte_gauche = plat[ligne * 7 + col - 1]
                carte_droite = plat[ligne * 7 + col + 1]
                attendu = {'N': None, 'S': None, 'E': None, 'O': None}
                if carte_testee in nord_libre and carte_dessus in sud_libre:
                    attendu['N'] = (ligne - 1, col)
                if carte_testee in sud_libre and carte_dessous in nord_libre:
                    attendu['S'] = (ligne + 1, col)
                if carte_testee in ouest_libre and carte_gauche in est_libre:
                    attendu['O'] = (ligne, col - 1)
                if carte_testee in est_libre and carte_droite in ouest_libre:
                    attendu['E'] = (ligne, col + 1)
                for direction in 'NESO':
                    obtenu = plateau.passage_plateau(mat, ligne, col, direction)
                    if attendu[direction] is None:
                        msg = 'il ne devrait pas y avoir de '
                    else:
                        msg = "il devrait y avoir un "
                    self.assertEqual(obtenu, attendu[direction],
                                     "Sur le plateau ci-dessous " + msg + "passage en direction " + direction +
                                     " à partir de la position " + str((ligne, col)) +
                                     " or votre fonction passage_plateau retourne " + str(obtenu) +
                                     plateau_to_str(mat) +
                                     "\nCauses possibles: Plateau, get_valeur, passage_plateau")

    def compter_les_cases(self, plat, mat, ligne, col, pas, borne, direction, reserve, liste_depart, liste_arrivee, mur):

        nom_direction = {"N": "le nord", "S": "le sud", "O": "l'ouest", "E": "l'est"}
        nb_attendus = nb_atteignables(plat, ligne * 7 + col, pas, borne, liste_depart, liste_arrivee, mur)
        nb_attendus = min(reserve,nb_attendus)
        _, nb_obtenus = plateau.peindre_direction_couleur(mat, ligne, col, direction, "info", reserve, mur)
        self.assertEqual(nb_obtenus, nb_attendus,
                         "Sur le plateau ci-dessous en peignant vers " + nom_direction[direction] +
                         " à partir de la position " + str((ligne, col)) + " avec une réserve de "+
                         str(reserve) + " on devrait obtenir " +
                         str(nb_attendus) + " cases peintes" +
                         " or votre fonction indique qu'elle en a peinte " + str(nb_obtenus) +
                         plateau_to_str(mat) +
                         "\nCauses possibles: Plateau, peindre_direction_couleur")

    def test_peindre_direction_couleur_nombre_cases(self):
        plateaux = [
            "╔║╦╚╦═╗" +
            "╦╚═╚║═║" +
            "╠╗╠║╦╣╣" +
            "║╚╔╝╦╝║" +
            "╠╦╩═╣╦╣" +
            "╝╗╠╗═╔╗" +
            "╚╔╩╝╩╔╝",
            "╔╔╦╠╦╔╗" +
            "╚══╝╝╝╔" +
            "╠╦╠╔╦╔╣" +
            "═║╝╔╗║╝" +
            "╠╝╩╠╣╦╣" +
            "║╚╝╣║═║" +
            "╚║╩╠╩║╝"]

        sud_libre = ['╦', '╗', '╣', '╠', '║', '╔']
        nord_libre = ['╣', '╩', '╝', '╠', '║', '╚']
        est_libre = ['╦', '╩', '═', '╠', '╔', '╚']
        ouest_libre = ['╦', '╣', '╗', '╩', '═', '╝']

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        participants = plateau.Participants(noms, couleurs)
        mat, carte_sup = plateau.Plateau(participants)
        for plat in plateaux:
            forcer_cartes_from_str(mat, plat)
            for ligne in range(7):
                for col in range(7):
                    self.compter_les_cases(plat, mat, ligne, col, -7, -1, 'N', 20, nord_libre, sud_libre, False)
                    self.compter_les_cases(plat, mat, ligne, col, 7, 49, 'S', 20, sud_libre, nord_libre, False)
                    self.compter_les_cases(plat, mat, ligne, col, -1, ligne * 7 - 1, 'O', 20, ouest_libre,
                                           est_libre, False)
                    self.compter_les_cases(plat, mat, ligne, col, 1, (ligne + 1) * 7, 'E', 20, est_libre,
                                           ouest_libre, False)
    def test_peindre_direction_couleur_nombre_cases_reserve3(self):
        plateaux = [
            "╔║╦╚╦═╗" +
            "╦╚═╚║═║" +
            "╠╗╠║╦╣╣" +
            "║╚╔╝╦╝║" +
            "╠╦╩═╣╦╣" +
            "╝╗╠╗═╔╗" +
            "╚╔╩╝╩╔╝",
            "╔╔╦╠╦╔╗" +
            "╚══╝╝╝╔" +
            "╠╦╠╔╦╔╣" +
            "═║╝╔╗║╝" +
            "╠╝╩╠╣╦╣" +
            "║╚╝╣║═║" +
            "╚║╩╠╩║╝"]

        sud_libre = ['╦', '╗', '╣', '╠', '║', '╔']
        nord_libre = ['╣', '╩', '╝', '╠', '║', '╚']
        est_libre = ['╦', '╩', '═', '╠', '╔', '╚']
        ouest_libre = ['╦', '╣', '╗', '╩', '═', '╝']

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        participants = plateau.Participants(noms, couleurs)
        mat, carte_sup = plateau.Plateau(participants)
        for plat in plateaux:
            forcer_cartes_from_str(mat, plat)
            for ligne in range(7):
                for col in range(7):
                    self.compter_les_cases(plat, mat, ligne, col, -7, -1, 'N', 3, nord_libre, sud_libre, False)
                    self.compter_les_cases(plat, mat, ligne, col, 7, 49, 'S', 3, sud_libre, nord_libre, False)
                    self.compter_les_cases(plat, mat, ligne, col, -1, ligne * 7 - 1, 'O', 3, ouest_libre,
                                           est_libre, False)
                    self.compter_les_cases(plat, mat, ligne, col, 1, (ligne + 1) * 7, 'E', 3, est_libre,
                                           ouest_libre, False)
    def test_peindre_direction_couleur_nombre_cases_traverser_un_mur(self):
        plateaux = [
            "╔║╦╚╦═╗" +
            "╦╚═╚║═║" +
            "╠╗╠║╦╣╣" +
            "║╚╔╝╦╝║" +
            "╠╦╩═╣╦╣" +
            "╝╗╠╗═╔╗" +
            "╚╔╩╝╩╔╝",
            "╔╔╦╠╦╔╗" +
            "╚══╝╝╝╔" +
            "╠╦╠╔╦╔╣" +
            "═║╝╔╗║╝" +
            "╠╝╩╠╣╦╣" +
            "║╚╝╣║═║" +
            "╚║╩╠╩║╝"]

        sud_libre = ['╦', '╗', '╣', '╠', '║', '╔']
        nord_libre = ['╣', '╩', '╝', '╠', '║', '╚']
        est_libre = ['╦', '╩', '═', '╠', '╔', '╚']
        ouest_libre = ['╦', '╣', '╗', '╩', '═', '╝']

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        participants = plateau.Participants(noms, couleurs)
        mat, carte_sup = plateau.Plateau(participants)
        for plat in plateaux:
            forcer_cartes_from_str(mat, plat)
            for ligne in range(7):
                for col in range(7):
                    self.compter_les_cases(plat, mat, ligne, col, -7, -1, 'N', 20, nord_libre, sud_libre, True)
                    self.compter_les_cases(plat, mat, ligne, col, 7, 49, 'S', 20, sud_libre, nord_libre, True)
                    self.compter_les_cases(plat, mat, ligne, col, -1, ligne * 7 - 1, 'O', 20, ouest_libre,
                                           est_libre, True)
                    self.compter_les_cases(plat, mat, ligne, col, 1, (ligne + 1) * 7, 'E', 20, est_libre,
                                           ouest_libre, True)

    def compter_la_couleur(self, plat, mat, ligne, col, pas, borne, direction, liste_depart, liste_arrivee, mur):
        nom_direction = {"N": "le nord", "S": "le sud", "O": "l'ouest", "E": "l'est"}
        nb_attendus = nb_atteignables(plat, ligne * 7 + col, pas, borne, liste_depart, liste_arrivee, mur)
        plateau.peindre_direction_couleur(mat, ligne, col, direction, "info", 20, mur)
        nb_coloriees = 0
        for i in range(7):
            for j in range(7):
                if plateau.get_couleur(plateau.get_valeur(mat, i, j)) == "info":
                    nb_coloriees += 1
        self.assertEqual(nb_coloriees, nb_attendus,
                         "Sur le plateau ci-dessous en peignant vers " + nom_direction[direction] +
                         " à partir de la position " + str((ligne, col)) + " on devrait obtenir " +
                         str(nb_attendus) + " cases effectivement peintes" +
                         " or votre fonction en a peinte " + str(nb_coloriees) +
                         plateau_to_str(mat) +
                         "\nCauses possibles: Plateau, get_valeur, get_couleur, peindre_direction_couleur")

    def test_peindre_direction_couleur_cases_peintes(self):
        plateaux = [
            "╔║╦╚╦═╗" +
            "╦╚═╚║═║" +
            "╠╗╠║╦╣╣" +
            "║╚╔╝╦╝║" +
            "╠╦╩═╣╦╣" +
            "╝╗╠╗═╔╗" +
            "╚╔╩╝╩╔╝",
            "╔╔╦╠╦╔╗" +
            "╚══╝╝╝╔" +
            "╠╦╠╔╦╔╣" +
            "═║╝╔╗║╝" +
            "╠╝╩╠╣╦╣" +
            "║╚╝╣║═║" +
            "╚║╩╠╩║╝"]

        sud_libre = ['╦', '╗', '╣', '╠', '║', '╔']
        nord_libre = ['╣', '╩', '╝', '╠', '║', '╚']
        est_libre = ['╦', '╩', '═', '╠', '╔', '╚']
        ouest_libre = ['╦', '╣', '╗', '╩', '═', '╝']

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        participants = plateau.Participants(noms, couleurs)

        for plat in plateaux:
            for ligne in range(7):
                for col in range(7):
                    mat, carte_sup = plateau.Plateau(participants)
                    forcer_cartes_from_str(mat, plat)
                    self.compter_la_couleur(plat, mat, ligne, col, -7, -1, 'N', nord_libre, sud_libre, False)
                    mat, carte_sup = plateau.Plateau(participants)
                    forcer_cartes_from_str(mat, plat)
                    self.compter_la_couleur(plat, mat, ligne, col, 7, 49, 'S', sud_libre, nord_libre, False)
                    mat, carte_sup = plateau.Plateau(participants)
                    forcer_cartes_from_str(mat, plat)
                    self.compter_la_couleur(plat, mat, ligne, col, -1, ligne * 7 - 1, 'O', ouest_libre, est_libre,
                                            False)
                    mat, carte_sup = plateau.Plateau(participants)
                    forcer_cartes_from_str(mat, plat)
                    self.compter_la_couleur(plat, mat, ligne, col, 1, (ligne + 1) * 7, 'E', est_libre, ouest_libre,
                                            False)

    def test_peindre_direction_couleur_cases_peintes_traverser_mur(self):
        plateaux = [
            "╔║╦╚╦═╗" +
            "╦╚═╚║═║" +
            "╠╗╠║╦╣╣" +
            "║╚╔╝╦╝║" +
            "╠╦╩═╣╦╣" +
            "╝╗╠╗═╔╗" +
            "╚╔╩╝╩╔╝",
            "╔╔╦╠╦╔╗" +
            "╚══╝╝╝╔" +
            "╠╦╠╔╦╔╣" +
            "═║╝╔╗║╝" +
            "╠╝╩╠╣╦╣" +
            "║╚╝╣║═║" +
            "╚║╩╠╩║╝"]

        sud_libre = ['╦', '╗', '╣', '╠', '║', '╔']
        nord_libre = ['╣', '╩', '╝', '╠', '║', '╚']
        est_libre = ['╦', '╩', '═', '╠', '╔', '╚']
        ouest_libre = ['╦', '╣', '╗', '╩', '═', '╝']

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        participants = plateau.Participants(noms, couleurs)

        for plat in plateaux:
            for ligne in range(7):
                for col in range(7):
                    mat, carte_sup = plateau.Plateau(participants)
                    forcer_cartes_from_str(mat, plat)
                    self.compter_la_couleur(plat, mat, ligne, col, -7, -1, 'N', nord_libre, sud_libre, True)
                    mat, carte_sup = plateau.Plateau(participants)
                    forcer_cartes_from_str(mat, plat)
                    self.compter_la_couleur(plat, mat, ligne, col, 7, 49, 'S', sud_libre, nord_libre, True)
                    mat, carte_sup = plateau.Plateau(participants)
                    forcer_cartes_from_str(mat, plat)
                    self.compter_la_couleur(plat, mat, ligne, col, -1, ligne * 7 - 1, 'O', ouest_libre, est_libre, True)
                    mat, carte_sup = plateau.Plateau(participants)
                    forcer_cartes_from_str(mat, plat)
                    self.compter_la_couleur(plat, mat, ligne, col, 1, (ligne + 1) * 7, 'E', est_libre, ouest_libre,
                                            True)

    def test_nb_cartes_par_couleur(self):

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        peinture = ["info", "info", "info", "gea", "gea", "gmp", "gmp",
                    "aucune", "aucune", "info", "gea", "info", "info", "gea",
                    "gea", "gea", "aucune", "aucune", "aucune", "aucune", "gea",
                    "gmp", "info", "info", "info", "aucune", "aucune", "aucune",
                    "aucune", "aucune", "aucune", "aucune", "info", "gea", "gea",
                    "gmp", "info", "info", "info", "aucune", "info", "info",
                    "gea", "gmp", "info", "aucune", "info", "gea", "gmp"
                    ]
        participants = plateau.Participants(noms, couleurs)
        mat, carte_sup = plateau.Plateau(participants)
        res_attendu = {}
        res_obtenu = plateau.nb_cartes_par_couleur(mat)
        self.assertEqual(res_obtenu, res_attendu,
                         "Après avoir créé un plateau avec les joueurs " + str(noms) +
                         " et peint aucune case votre fonction nb_cartes_par_couleur retourne " + str(res_obtenu) +
                         "\n Voici le plateau\n" + str(mat) +
                         "\nCauses possibles: Plateau, get_valeur, set_couleur, nb_cartes_par_couleur")
        for lig in range(7):
            for col in range(7):
                carte = plateau.get_valeur(mat, lig, col)
                plateau.set_couleur(carte, peinture[lig * 7 + col])
        res_attendu = {"info": peinture.count("info"), "gea": peinture.count("gea"), "gmp": peinture.count("gmp")}
        res_obtenu = plateau.nb_cartes_par_couleur(mat)
        self.assertEqual(res_obtenu, res_attendu,
                         "Après avoir créé un plateau avec les joueurs " + str(noms) +
                         " et peint des cases suivant cette répartition " + str(res_attendu) +
                         " votre fonction nb_cartes_par_couleur retourne " + str(res_obtenu) +
                         "\n Voici le plateau\n" + str(mat) +
                         "\nCauses possibles: Plateau, get_valeur, set_couleur, nb_cartes_par_couleur")

    def test_accessible(self):
        plat = \
            "╔║╦╚╦═╗" + \
            "╦╚═╚║═║" + \
            "╠╗╠║╦╣╣" + \
            "║╚╔╝╦╝║" + \
            "╠╦╩═╣╦╣" + \
            "╝╗╠╗═╔╗" + \
            "╚╔╩╝╩╔╝"

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        participants = plateau.Participants(noms, couleurs)
        mat, carte_sup = plateau.Plateau(participants)
        forcer_cartes_from_str(mat, plat)
        self.assertTrue(plateau.accessible(mat, 4, 3, 2, 3),
                        "Vous trouvez que la position (2,3) n'est pas accessible à partir de (4,3) or elle l'est " +
                        "sur le plateau " + plateau_to_str(mat) +
                        "\nCauses possibles: Plateau, accessible")
        self.assertTrue(plateau.accessible(mat, 1, 0, 2, 3),
                        "Vous trouvez que la position (2,3) n'est pas accessible à partir de (1,0) or elle l'est " +
                        "sur le plateau " + plateau_to_str(mat) +
                        "\nCauses possibles: Plateau, accessible")
        self.assertFalse(plateau.accessible(mat, 0, 6, 4, 3),
                         "Vous trouvez que la position (4,3) est accessible à partir de (0,6) or elle ne l'est pas " +
                         "sur le plateau " + plateau_to_str(mat) +
                         "\nCauses possibles: Plateau, accessible")
        self.assertFalse(plateau.accessible(mat, 6, 4, 1, 3),
                         "Vous trouvez que la position (1,3) est accessible à partir de (6,4) or elle ne l'est pas " +
                         "sur le plateau " + plateau_to_str(mat) +
                         "\nCauses possibles: Plateau, accessible")

    def test_compter_joueurs_touches(self):
        plat = \
            "╔║╦╚╦═╗" + \
            "╦╚═╚║═║" + \
            "╠╗╠║╦╣╣" + \
            "║╚╔╝╦╝║" + \
            "╠╦╩═╣╦╣" + \
            "╝╗╠╗═╔╗" + \
            "╚╔╩╝╩╔╝"

        noms = ["joueur1", "joueur2", "joueur3", "joueur4"]
        couleurs = ["info", "gea", "gmp", "chimie"]
        participants = plateau.Participants(noms, couleurs)
        mat, carte_sup = plateau.Plateau(participants)
        forcer_cartes_from_str(mat, plat)
        for ligne in range(0, 7, 6):
            for col in range(0, 7, 6):
                plateau.set_liste_joueurs(plateau.get_valeur(mat, ligne, col), list())
        liste1 = [plateau.get_joueur_par_num(participants, 1)]
        liste2 = [plateau.get_joueur_par_num(participants, 4), plateau.get_joueur_par_num(participants, 3)]
        liste3 = liste1 + liste2
        liste3.sort(key=plateau.get_nom_joueur)
        liste2.sort(key=plateau.get_nom_joueur)
        plateau.set_liste_joueurs(plateau.get_valeur(mat, 0, 5), liste1)
        plateau.set_liste_joueurs(plateau.get_valeur(mat, 0, 4), liste2)
        liste_touches, _ = plateau.peindre_direction_couleur(mat, 0, 3, 'E', "chimie", 20, False)
        liste_touches.sort(key=plateau.get_nom_joueur)
        self.assertListEqual(liste_touches, liste3,
                             "Après avoir créé un plateau avec les joueurs " + str(noms) +
                             " et positionné le joueur 1 en (0,5) et les joueurs 2 et 3 en (0,4)" +
                             " puis peint en direction de l'est à partir de (0,3), on devrait toucher les joueurs " +
                             str(liste3) + " or la fonction peindre_direction_couleur indique " + str(liste_touches) +
                             " voici le plateau " + plateau_to_str(mat) +
                             "\nCauses possibles: Plateau, get_joueur_par_num, set_liste_joueurs, get_valeur," +
                             " peindre_direction_couleur")
        liste_touches, _ = plateau.peindre_direction_couleur(mat, 0, 6, 'O', "chimie", 20, False)
        liste_touches.sort(key=plateau.get_nom_joueur)
        self.assertListEqual(liste_touches, liste3,
                             "Après avoir créé un plateau avec les joueurs " + str(noms) +
                             " et positionné le joueur 1 en (0,5) et les joueurs 2 et 3 en (0,4)" +
                             " puis peint en direction de l'ouest à partir de (0,6), on devrait toucher les joueurs " +
                             str(liste3) + " or la fonction peindre_direction_couleur indique " + str(liste_touches) +
                             " voici le plateau " + plateau_to_str(mat) +
                             "\nCauses possibles: Plateau, get_joueur_par_num, set_liste_joueurs, get_valeur," +
                             " peindre_direction_couleur")
        liste_touches, _ = plateau.peindre_direction_couleur(mat, 0, 5, 'O', "chimie", 20, False)
        liste_touches.sort(key=plateau.get_nom_joueur)
        self.assertListEqual(liste_touches, liste3,
                             "Après avoir créé un plateau avec les joueurs " + str(noms) +
                             " et positionné le joueur 1 en (0,5) et les joueurs 2 et 3 en (0,4)" +
                             " puis peint en direction de l'ouest à partir de (0,5), on devrait toucher les joueurs " +
                             str(liste3) + " or la fonction peindre_direction_couleur indique " + str(liste_touches) +
                             " voici le plateau " + plateau_to_str(mat) +
                             "\nCauses possibles: Plateau, get_joueur_par_num, set_liste_joueurs, get_valeur," +
                             " peindre_direction_couleur")
        liste_touches, _ = plateau.peindre_direction_couleur(mat, 1, 4, 'N', "chimie", 20, False)
        liste_touches.sort(key=plateau.get_nom_joueur)
        self.assertListEqual(liste_touches, liste2,
                             "Après avoir créé un plateau avec les joueurs " + str(noms) +
                             " et positionné le joueur 1 en (0,5) et les joueurs 2 et 3 en (0,4)" +
                             " puis peint en direction du nord à partir de (1,4), on devrait toucher les joueurs " +
                             str(liste2) + " or la fonction peindre_direction_couleur indique " + str(liste_touches) +
                             " voici le plateau " + plateau_to_str(mat) +
                             "\nCauses possibles: Plateau, get_joueur_par_num, set_liste_joueurs, get_valeur," +
                             " peindre_direction_couleur")

        liste_touches, _ = plateau.peindre_direction_couleur(mat, 1, 0, 'S', "chimie", 20, False)
        liste_touches.sort(key=plateau.get_nom_joueur)
        self.assertListEqual(liste_touches, [],
                             "Après avoir créé un plateau avec les joueurs " + str(noms) +
                             " et positionné le joueur 1 en (0,5) et les joueurs 2 et 3 en (0,4)" +
                             " puis peint en direction du sud à partir de (1,0), on ne devrait toucher aucun joueur " +
                             " or la fonction peindre_direction_couleur indique " + str(liste_touches) +
                             " voici le plateau " + plateau_to_str(mat) +
                             "\nCauses possibles: Plateau, get_joueur_par_num, set_liste_joueurs, get_valeur," +
                             " peindre_direction_couleur")


if __name__ == '__main__':
    unittest.main()
