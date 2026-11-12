"""Tests de tools/build_zip.py (archive importable dans l'app Claude)."""

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from helpers import ROOT, SKILL, TOOLS, run

BUILD = TOOLS / "build_zip.py"


class BuildZipTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        proc = run(BUILD, "--out", self.out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        version = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
        self.zip = self.out / f"linkedin-coach-v{version}.zip"

    def tearDown(self):
        self.tmp.cleanup()

    def noms(self):
        with zipfile.ZipFile(self.zip) as z:
            return z.namelist()

    def test_nom_versionne(self):
        self.assertTrue(self.zip.is_file(), list(self.out.iterdir()))

    def test_racine_est_le_dossier_du_skill(self):
        noms = self.noms()
        self.assertIn("linkedin-coach/SKILL.md", noms)
        self.assertEqual({n.split("/")[0] for n in noms}, {"linkedin-coach"})

    def test_contenu_attendu(self):
        # Tout fichier du skill (references/, scripts/, templates/…) est dans l'archive.
        noms = set(self.noms())
        attendus = {
            "linkedin-coach/" + p.relative_to(SKILL).as_posix()
            for p in SKILL.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
        }
        self.assertEqual(noms, attendus)
        self.assertIn("linkedin-coach/scripts/humanizer.py", noms)
        self.assertIn("linkedin-coach/references/humanizer.md", noms)

    def test_exclusions(self):
        for n in self.noms():
            for interdit in ("__pycache__", ".pyc", "tests/", ".specify", "specs/"):
                self.assertNotIn(interdit, n)


if __name__ == "__main__":
    unittest.main()
