"""FR-052 : la bibliothèque contient au moins 16 formules d'accroche bien formées."""

import re
import unittest

from helpers import SKILL

FORMULES = SKILL / "references" / "formules-accroche.md"
LIGNE = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$")


def formules():
    return [m.groups() for l in FORMULES.read_text(encoding="utf-8").splitlines()
            if (m := LIGNE.match(l))]


class FormulesTests(unittest.TestCase):
    def test_au_moins_16(self):
        self.assertGreaterEqual(len(formules()), 16)

    def test_numeros_uniques_et_continus(self):
        numeros = [int(f[0]) for f in formules()]
        self.assertEqual(numeros, list(range(1, len(numeros) + 1)))

    def test_nom_modele_exemple(self):
        for numero, nom, modele, exemple in formules():
            with self.subTest(numero=numero):
                self.assertTrue(nom)
                self.assertIn("{", modele, "le modèle doit contenir des {variables}")
                self.assertTrue(exemple, "chaque formule a un exemple")
                self.assertFalse(exemple.rstrip().endswith("?"),
                                 "une accroche ne finit pas par une question")


if __name__ == "__main__":
    unittest.main()
