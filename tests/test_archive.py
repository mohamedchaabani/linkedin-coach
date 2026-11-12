"""Tests de scripts/archive.py (résumé Markdown de l'archive officielle LinkedIn)."""

import re
import unittest

from helpers import FIXTURES, SCRIPTS, run

ARCHIVE = SCRIPTS / "archive.py"
FX = FIXTURES / "archive"
POST = re.compile(r"^- \*\*(\d{4}-\d{2}-\d{2})\*\*", re.MULTILINE)


def section(texte, titre):
    m = re.search(rf"^## {re.escape(titre)}\n(.*?)(?=^## |\Z)", texte, re.MULTILINE | re.DOTALL)
    return m.group(1) if m else None


class ArchiveCompleteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = run(ARCHIVE, FX / "archive-complete.zip")
        assert proc.returncode == 0, proc.stderr
        cls.sortie = proc.stdout

    def test_trois_sections(self):
        for titre in ("Sections reconnues", "Posts", "Non fournies"):
            self.assertIsNotNone(section(self.sortie, titre), titre)

    def test_sections_reconnues(self):
        reconnues = section(self.sortie, "Sections reconnues")
        for attendu in ("Architecte AEM | Adobe Experience Manager",   # titre
                        "J'accompagne des équipes digitales",          # Infos
                        "Cabinet Exemple", "Adobe Experience Manager", "AWS Certified",
                        "Dominique Fictif", "École d'ingénieurs Exemple"):
            self.assertIn(attendu, reconnues)

    def test_accents_utf8(self):
        self.assertIn("Île-de-France", self.sortie)
        self.assertIn("Développeur AEM senior", self.sortie)

    def test_certification_expiree_signalee(self):
        reconnues = section(self.sortie, "Sections reconnues")
        ligne = next(l for l in reconnues.splitlines() if "AEM Sites Architect" in l)
        self.assertIn("expirée", ligne)
        ligne = next(l for l in reconnues.splitlines() if "AWS Certified" in l)
        self.assertNotIn("expirée", ligne)

    def test_trente_posts_les_plus_recents(self):
        dates = POST.findall(section(self.sortie, "Posts"))
        self.assertEqual(len(dates), 30)
        self.assertEqual(dates[0], "2026-10-30")
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_non_fournies(self):
        manque = section(self.sortie, "Non fournies").lower()
        for attendu in ("photo", "bannière", "sélection", "statistiques"):
            self.assertIn(attendu, manque)
        self.assertNotIn("compétences", manque)

    def test_url_rendue_comme_texte(self):
        self.assertIn("https://exemple.invalid/article", self.sortie)


class ArchiveOptionsTests(unittest.TestCase):
    def test_nombre_de_posts(self):
        proc = run(ARCHIVE, "--posts", "5", FX / "archive-complete.zip")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(len(POST.findall(section(proc.stdout, "Posts"))), 5)

    def test_archive_partielle(self):
        proc = run(ARCHIVE, FX / "archive-partielle")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Architecte AEM", section(proc.stdout, "Sections reconnues"))
        manque = section(proc.stdout, "Non fournies").lower()
        self.assertIn("compétences", manque)
        self.assertIn("recommandations", manque)
        self.assertIn("posts", manque)

    def test_chemin_inexistant(self):
        self.assertEqual(run(ARCHIVE, FX / "absent.zip").returncode, 1)

    def test_usage_invalide(self):
        self.assertEqual(run(ARCHIVE).returncode, 2)


if __name__ == "__main__":
    unittest.main()
