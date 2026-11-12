"""Tests de scripts/humanizer.py (contrat : specs/001-linkedin-coach-skill/contracts/scripts-cli.md)."""

import json
import re
import unittest

from helpers import FIXTURES, SCRIPTS, run

HUMANIZER = SCRIPTS / "humanizer.py"
FX = FIXTURES / "humanizer"
CRITERES = ("ponctuation", "vocabulaire", "tournures", "rythme", "voix")
INVISIBLES = ("​", "‌", "‍", "﻿")


def detect(name, *extra):
    proc = run(HUMANIZER, "detect", "--json", *extra, FX / name)
    if proc.returncode != 0:
        raise AssertionError(f"detect {name} a échoué : {proc.stderr}")
    return json.loads(proc.stdout)


def mots(texte):
    return re.findall(r"\w+", texte)


class DetectTests(unittest.TestCase):
    def test_structure_json(self):
        res = detect("fr-naturel.txt")
        self.assertIn(res["lang"], ("fr", "en"))
        self.assertEqual(set(res["criteres"]), set(CRITERES))
        total = 0
        for nom in CRITERES:
            c = res["criteres"][nom]
            self.assertEqual(c["max"], 20)
            self.assertTrue(0 <= c["score"] <= 20)
            self.assertIsInstance(c["constats"], list)
            total += c["score"]
        self.assertEqual(res["score"], total)
        self.assertTrue(0 <= res["score"] <= 100)

    def test_voix_francaise_reconnue(self):
        # SC-006 : un texte français avec « je » et « nous » ne doit pas être sous-noté.
        res = detect("fr-naturel.txt")
        self.assertGreaterEqual(res["criteres"]["voix"]["score"], 14)

    def test_texte_ia_moins_bien_note_fr(self):
        self.assertLess(detect("fr-ia.txt")["score"], detect("fr-naturel.txt")["score"])

    def test_texte_ia_moins_bien_note_en(self):
        self.assertLess(detect("en-ia.txt")["score"], detect("en-naturel.txt")["score"])

    def test_ecart_significatif(self):
        for ia, naturel in (("fr-ia.txt", "fr-naturel.txt"), ("en-ia.txt", "en-naturel.txt")):
            self.assertGreaterEqual(detect(naturel)["score"] - detect(ia)["score"], 25, ia)

    def test_paire_fr_en_comparable(self):
        fr = detect("fr-en-paire.fr.txt")["score"]
        en = detect("fr-en-paire.en.txt")["score"]
        self.assertLessEqual(abs(fr - en), 10, f"fr={fr} en={en}")

    def test_detection_langue_auto(self):
        self.assertEqual(detect("fr-naturel.txt", "--lang", "auto")["lang"], "fr")
        self.assertEqual(detect("en-naturel.txt", "--lang", "auto")["lang"], "en")
        self.assertEqual(detect("fr-ia.txt")["lang"], "fr")
        self.assertEqual(detect("en-ia.txt")["lang"], "en")

    def test_lang_force(self):
        self.assertEqual(detect("fr-naturel.txt", "--lang", "en")["lang"], "en")

    def test_vocabulaire_ia_signale(self):
        constats = " ".join(detect("fr-ia.txt")["criteres"]["vocabulaire"]["constats"])
        self.assertIn("incontournable", constats)
        constats = " ".join(detect("en-ia.txt")["criteres"]["vocabulaire"]["constats"])
        self.assertIn("delve", constats)

    def test_sortie_texte(self):
        proc = run(HUMANIZER, "detect", FX / "fr-naturel.txt")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertRegex(proc.stdout.strip().splitlines()[-1], r"^SCORE \d{1,3}/100$")

    def test_stdin(self):
        texte = (FX / "fr-naturel.txt").read_text(encoding="utf-8")
        proc = run(HUMANIZER, "detect", "--json", "-", stdin=texte)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["lang"], "fr")


class CleanTests(unittest.TestCase):
    def clean(self, name, *extra):
        proc = run(HUMANIZER, "clean", *extra, FX / name)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc

    def test_supprime_invisibles_et_tirets(self):
        proc = self.clean("invisibles.txt")
        for ch in INVISIBLES:
            self.assertNotIn(ch, proc.stdout)
        self.assertNotIn("—", proc.stdout)
        self.assertTrue(proc.stderr.strip(), "le résumé des changements doit aller sur stderr")

    def test_guillemets_droits_en(self):
        proc = self.clean("en-ia.txt", "--lang", "en")
        self.assertNotIn("“", proc.stdout)
        self.assertNotIn("—", proc.stdout)

    def test_aucun_mot_modifie(self):
        for name in ("fr-ia.txt", "en-ia.txt", "invisibles.txt", "fr-naturel.txt"):
            source = (FX / name).read_text(encoding="utf-8")
            for ch in INVISIBLES:
                source = source.replace(ch, "")
            self.assertEqual(mots(self.clean(name).stdout), mots(source), name)

    def test_texte_naturel_inchange(self):
        source = (FX / "fr-naturel.txt").read_text(encoding="utf-8")
        self.assertEqual(self.clean("fr-naturel.txt").stdout, source)


class ExitCodeTests(unittest.TestCase):
    def test_fichier_absent(self):
        self.assertEqual(run(HUMANIZER, "detect", FX / "absent.txt").returncode, 1)

    def test_usage_invalide(self):
        self.assertEqual(run(HUMANIZER).returncode, 2)
        self.assertEqual(run(HUMANIZER, "detect", "--lang", "de", FX / "fr-ia.txt").returncode, 2)


if __name__ == "__main__":
    unittest.main()
