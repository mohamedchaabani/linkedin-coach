"""Principe IV : aucun appel réseau dans les outils du skill.

Chaque script de skills/linkedin-coach/scripts/ est découvert automatiquement et exécuté
avec socket.socket bloqué. Un script peut déclarer une fixture par une ligne d'en-tête :
    # test-fixture: <chemin relatif à tests/fixtures/> [arguments supplémentaires]
"""

import ast
import os
import re
import tempfile
import unittest
from pathlib import Path

from helpers import FIXTURES, SCRIPTS, SKILL, run

MODULES_INTERDITS = {"socket", "urllib", "http", "ssl", "ftplib", "smtplib", "requests"}

SITECUSTOMIZE = '''
import socket

def _bloque(*args, **kwargs):
    raise RuntimeError("accès réseau interdit (principe IV)")

socket.socket = _bloque
socket.create_connection = _bloque
socket.getaddrinfo = _bloque
'''


def scripts():
    return sorted(p for p in SCRIPTS.glob("*.py") if not p.name.startswith("_"))


def fixture_declaree(script):
    for ligne in script.read_text(encoding="utf-8").splitlines()[:30]:
        m = re.match(r"#\s*test-fixture:\s*(\S+)(.*)$", ligne)
        if m:
            return m.group(1), m.group(2).split()
    return None


class NoNetworkRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        Path(self.tmp.name, "sitecustomize.py").write_text(SITECUSTOMIZE, encoding="utf-8")
        chemin = self.tmp.name
        if os.environ.get("PYTHONPATH"):
            chemin += os.pathsep + os.environ["PYTHONPATH"]
        self.env = {"PYTHONPATH": chemin}

    def tearDown(self):
        self.tmp.cleanup()

    def test_le_blocage_fonctionne(self):
        sonde = Path(self.tmp.name, "sonde.py")
        sonde.write_text("import socket\nsocket.socket()\n", encoding="utf-8")
        self.assertNotEqual(run(sonde, env_extra=self.env).returncode, 0)

    def test_scripts_sans_reseau(self):
        trouves = scripts()
        self.assertTrue(trouves, "aucun script trouvé dans skills/linkedin-coach/scripts/")
        for script in trouves:
            with self.subTest(script=script.name):
                proc = run(script, "--help", env_extra=self.env)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                decl = fixture_declaree(script)
                if decl:
                    fixture, extra = decl
                    proc = run(script, *extra, FIXTURES / fixture, env_extra=self.env)
                    self.assertEqual(proc.returncode, 0, proc.stderr)


class NoNetworkStaticTests(unittest.TestCase):
    def test_aucun_import_reseau(self):
        for fichier in sorted(SKILL.rglob("*.py")):
            arbre = ast.parse(fichier.read_text(encoding="utf-8"), filename=str(fichier))
            for noeud in ast.walk(arbre):
                if isinstance(noeud, ast.Import):
                    noms = [a.name for a in noeud.names]
                elif isinstance(noeud, ast.ImportFrom):
                    noms = [noeud.module or ""]
                else:
                    continue
                for nom in noms:
                    with self.subTest(fichier=fichier.name, module=nom):
                        self.assertNotIn(nom.split(".")[0], MODULES_INTERDITS)


if __name__ == "__main__":
    unittest.main()
