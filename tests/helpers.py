"""Chemins et utilitaires partagés par les tests (stdlib seulement)."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "linkedin-coach"
SCRIPTS = SKILL / "scripts"
TOOLS = ROOT / "tools"
FIXTURES = ROOT / "tests" / "fixtures"


def run(script, *args, stdin=None, env_extra=None):
    """Lance un script Python dans un sous-processus et renvoie le CompletedProcess."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(script), *map(str, args)],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        cwd=str(ROOT),
    )
