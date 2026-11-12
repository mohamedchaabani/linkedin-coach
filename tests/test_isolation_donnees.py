"""US7 / principe IV : les données de l'utilisateur vivent hors du dossier du skill."""

import re
import tempfile
import unittest
import zipfile
from pathlib import Path

from helpers import SKILL, TOOLS, run

FICHIERS_UTILISATEUR = ("positionnement.md", "historique-audits.md")


class IsolationTests(unittest.TestCase):
    def test_emplacement_documente_hors_du_skill(self):
        onboarding = (SKILL / "references" / "onboarding.md").read_text(encoding="utf-8")
        self.assertIn("~/.linkedin-coach/positionnement.md", onboarding)
        self.assertIn("LINKEDIN_COACH_HOME", onboarding)
        self.assertIn("dossier du skill", onboarding)

    def test_aucune_ecriture_dans_le_dossier_du_skill(self):
        # Les seules mentions de ces fichiers à l'intérieur du skill sont les modèles.
        motif = re.compile(r"(?:^|[\s`(])((?:\./|skills/linkedin-coach/)?(?:references|scripts)/"
                           r"(?:positionnement|historique-audits)\.md)")
        for md in SKILL.rglob("*.md"):
            with self.subTest(fichier=md.name):
                self.assertFalse(motif.findall(md.read_text(encoding="utf-8")))

    def test_modeles_vides(self):
        for nom in FICHIERS_UTILISATEUR:
            texte = (SKILL / "templates" / nom).read_text(encoding="utf-8")
            with self.subTest(modele=nom):
                self.assertIn("<!-- linkedin-coach:", texte)
                if nom == "positionnement.md":
                    valeurs = re.findall(r"^\s*- [^:]+ : (.+)$", texte, re.MULTILINE)
                    self.assertTrue(valeurs)
                    self.assertTrue(all(v == "{{à confirmer}}" for v in valeurs), valeurs)
                else:
                    self.assertNotRegex(texte, r"\|\s*\d{4}-\d{2}-\d{2}\s*\|")

    def test_archive_sans_donnees_utilisateur(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run(TOOLS / "build_zip.py", "--out", tmp).returncode, 0)
            archive = next(Path(tmp).glob("*.zip"))
            with zipfile.ZipFile(archive) as z:
                for nom in z.namelist():
                    if nom.endswith(FICHIERS_UTILISATEUR):
                        self.assertTrue(nom.startswith("linkedin-coach/templates/"), nom)


if __name__ == "__main__":
    unittest.main()
