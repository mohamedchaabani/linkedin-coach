#!/usr/bin/env python3
"""Construit l'archive du skill pour l'app Claude (Customize → Skills → Upload a skill).

Usage :
    build_zip.py [--out DOSSIER]   # défaut : dist/

Produit linkedin-coach-v<version>.zip dont la racine est le dossier `linkedin-coach/`
(contenant SKILL.md), comme l'exige l'import de l'app Claude. La version est lue dans
.claude-plugin/plugin.json. Bibliothèque standard uniquement.
"""

import argparse
import json
import sys
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SKILL = RACINE / "skills" / "linkedin-coach"
EXCLUS_DOSSIERS = {"__pycache__", ".pytest_cache"}
EXCLUS_SUFFIXES = {".pyc", ".pyo"}
EXCLUS_NOMS = {".DS_Store", "Thumbs.db"}


def fichiers_du_skill():
    for chemin in sorted(SKILL.rglob("*")):
        if not chemin.is_file():
            continue
        rel = chemin.relative_to(SKILL)
        if set(rel.parts) & EXCLUS_DOSSIERS or chemin.suffix in EXCLUS_SUFFIXES \
                or chemin.name in EXCLUS_NOMS:
            continue
        yield chemin, rel


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Construit le .zip du skill linkedin-coach.")
    parser.add_argument("--out", default=str(RACINE / "dist"), help="dossier de sortie")
    args = parser.parse_args(argv)

    try:
        version = json.loads((RACINE / ".claude-plugin" / "plugin.json")
                             .read_text(encoding="utf-8"))["version"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"Erreur : version illisible dans .claude-plugin/plugin.json ({exc})", file=sys.stderr)
        return 1
    if not (SKILL / "SKILL.md").is_file():
        print(f"Erreur : {SKILL / 'SKILL.md'} introuvable", file=sys.stderr)
        return 1

    sortie = Path(args.out)
    sortie.mkdir(parents=True, exist_ok=True)
    archive = sortie / f"linkedin-coach-v{version}.zip"
    nb = 0
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for chemin, rel in fichiers_du_skill():
            z.write(chemin, "linkedin-coach/" + rel.as_posix())
            nb += 1
    print(f"✔ {archive} ({nb} fichiers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
