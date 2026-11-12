"""Tests de tools/validate_skill.py."""

import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import ROOT, SKILL, TOOLS, run

VALIDATE = TOOLS / "validate_skill.py"


class ValidateSkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.racine = Path(self.tmp.name)
        shutil.copytree(SKILL, self.racine / "skills" / "linkedin-coach",
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / ".claude-plugin", self.racine / ".claude-plugin")
        shutil.copy(ROOT / "CHANGELOG.md", self.racine / "CHANGELOG.md")
        self.skill = self.racine / "skills" / "linkedin-coach"
        self.skill_md = self.skill / "SKILL.md"

    def tearDown(self):
        self.tmp.cleanup()

    def valider(self, *args):
        return run(VALIDATE, *args, "--root", self.racine, self.skill)

    def remplacer(self, avant, apres):
        texte = self.skill_md.read_text(encoding="utf-8")
        self.assertIn(avant, texte)
        self.skill_md.write_text(texte.replace(avant, apres, 1), encoding="utf-8")

    def test_skill_du_depot_valide(self):
        proc = run(VALIDATE, "--strict")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_copie_valide(self):
        self.assertEqual(self.valider("--strict").returncode, 0)

    def test_name_absent(self):
        self.remplacer("name: linkedin-coach\n", "")
        self.assertEqual(self.valider().returncode, 1)

    def test_name_majuscules(self):
        self.remplacer("name: linkedin-coach", "name: LinkedIn-Coach")
        self.assertEqual(self.valider().returncode, 1)

    def test_description_trop_longue(self):
        texte = self.skill_md.read_text(encoding="utf-8")
        debut = texte.index("description:")
        fin = texte.index("\n", debut)
        self.skill_md.write_text(texte[:debut] + "description: " + "x" * 201 + texte[fin:],
                                 encoding="utf-8")
        self.assertEqual(self.valider().returncode, 1)

    def test_skill_md_trop_long(self):
        with self.skill_md.open("a", encoding="utf-8") as f:
            f.write("\nligne\n" * 160)
        self.assertEqual(self.valider().returncode, 1)

    def test_lien_casse(self):
        with self.skill_md.open("a", encoding="utf-8") as f:
            f.write("\nVoir [absent](references/absent.md).\n")
        self.assertEqual(self.valider().returncode, 1)

    def test_import_reseau(self):
        (self.skill / "scripts" / "fuite.py").write_text("import urllib.request\n", encoding="utf-8")
        self.assertEqual(self.valider().returncode, 1)

    def test_versions_differentes(self):
        cl = self.racine / "CHANGELOG.md"
        cl.write_text(cl.read_text(encoding="utf-8").replace("[0.1.0]", "[9.9.9]"), encoding="utf-8")
        self.assertEqual(self.valider().returncode, 1)

    def test_plugin_absent_tolere_sans_strict(self):
        shutil.rmtree(self.racine / ".claude-plugin")
        proc = self.valider()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("avertissement", (proc.stdout + proc.stderr).lower())
        self.assertEqual(self.valider("--strict").returncode, 1)


if __name__ == "__main__":
    unittest.main()
