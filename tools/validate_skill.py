#!/usr/bin/env python3
"""Valide le skill linkedin-coach avant une PR ou une release.

Usage :
    validate_skill.py [--strict] [--root RACINE] [CHEMIN_SKILL]

Vérifie :
  - frontmatter de SKILL.md : `name` (^[a-z0-9-]{1,64}$, égal au nom du dossier) et
    `description` (1 à 200 caractères, limite de l'import dans l'app Claude) ;
  - SKILL.md ≤ 150 lignes (principe IX) ;
  - chemins `references/…`, `scripts/…`, `templates/…` cités dans les .md du skill : existants ;
  - aucun import réseau dans les scripts Python du skill (principe IV) ;
  - version identique dans .claude-plugin/plugin.json et la 1re entrée `## [X.Y.Z]` du
    CHANGELOG.md. Sans --strict, un fichier absent produit un avertissement ; avec --strict,
    une erreur.

Codes de sortie : 0 = valide, 1 = invalide, 2 = erreur d'usage.
Bibliothèque standard uniquement.
"""

import argparse
import ast
import json
import re
import sys
from pathlib import Path

MAX_LIGNES = 150
MAX_DESCRIPTION = 200
MODULES_INTERDITS = {"socket", "urllib", "http", "ssl", "ftplib", "smtplib", "requests"}
CHEMIN_CITE = re.compile(r"(?<![\w/.-])((?:references|scripts|templates)/[\w./-]*[\w-])")
ENTREE_CHANGELOG = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)


def lire_frontmatter(texte):
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != "---":
        return None
    champs = {}
    for ligne in lignes[1:]:
        if ligne.strip() == "---":
            return champs
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", ligne)
        if m:
            valeur = m.group(2).strip()
            if len(valeur) >= 2 and valeur[0] == valeur[-1] and valeur[0] in "\"'":
                valeur = valeur[1:-1]
            champs[m.group(1)] = valeur
    return None


def verifier_skill(skill, erreurs):
    skill_md = skill / "SKILL.md"
    if not skill_md.is_file():
        erreurs.append(f"{skill_md} introuvable")
        return
    texte = skill_md.read_text(encoding="utf-8")

    fm = lire_frontmatter(texte)
    if fm is None:
        erreurs.append("SKILL.md : frontmatter YAML absent ou non fermé (---)")
    else:
        nom = fm.get("name", "")
        if not nom:
            erreurs.append("SKILL.md : champ `name` absent")
        elif not re.fullmatch(r"[a-z0-9-]{1,64}", nom):
            erreurs.append(f"SKILL.md : `name` invalide « {nom} » (minuscules, chiffres, tirets, ≤ 64)")
        elif nom != skill.name:
            erreurs.append(f"SKILL.md : `name` « {nom} » différent du dossier « {skill.name} »")
        desc = fm.get("description", "")
        if not desc:
            erreurs.append("SKILL.md : champ `description` absent")
        elif len(desc) > MAX_DESCRIPTION:
            erreurs.append(f"SKILL.md : `description` de {len(desc)} caractères (max {MAX_DESCRIPTION})")

    nb = len(texte.splitlines())
    if nb > MAX_LIGNES:
        erreurs.append(f"SKILL.md : {nb} lignes (max {MAX_LIGNES})")

    for md in sorted(skill.rglob("*.md")):
        for chemin in CHEMIN_CITE.findall(md.read_text(encoding="utf-8")):
            if not (skill / chemin).exists():
                rel = md.relative_to(skill).as_posix()
                erreurs.append(f"{rel} : chemin cité introuvable « {chemin} »")

    for py in sorted(skill.rglob("*.py")):
        try:
            arbre = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
        except SyntaxError as exc:
            erreurs.append(f"{py.name} : erreur de syntaxe ({exc})")
            continue
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.Import):
                noms = [a.name for a in noeud.names]
            elif isinstance(noeud, ast.ImportFrom):
                noms = [noeud.module or ""]
            else:
                continue
            for n in noms:
                if n.split(".")[0] in MODULES_INTERDITS:
                    erreurs.append(f"{py.name} : import réseau interdit « {n} » (principe IV)")


def verifier_versions(racine, strict, erreurs, avertissements):
    plugin = racine / ".claude-plugin" / "plugin.json"
    changelog = racine / "CHANGELOG.md"
    manquants = [p.name for p in (plugin, changelog) if not p.is_file()]
    if manquants:
        message = "fichier(s) absent(s) : " + ", ".join(manquants) + " (versions non comparées)"
        (erreurs if strict else avertissements).append(message)
        return
    try:
        version_plugin = json.loads(plugin.read_text(encoding="utf-8")).get("version")
    except json.JSONDecodeError as exc:
        erreurs.append(f"plugin.json : JSON invalide ({exc})")
        return
    m = ENTREE_CHANGELOG.search(changelog.read_text(encoding="utf-8"))
    if not version_plugin:
        erreurs.append("plugin.json : champ `version` absent")
    if not m:
        erreurs.append("CHANGELOG.md : aucune entrée `## [X.Y.Z]`")
    if version_plugin and m and version_plugin != m.group(1):
        erreurs.append(f"versions différentes : plugin.json {version_plugin}, CHANGELOG.md {m.group(1)}")

    marketplace = racine / ".claude-plugin" / "marketplace.json"
    if marketplace.is_file() and version_plugin:
        try:
            data = json.loads(marketplace.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            erreurs.append(f"marketplace.json : JSON invalide ({exc})")
            return
        for entree in data.get("plugins", []):
            v = entree.get("version")
            if v and v != version_plugin:
                erreurs.append(f"marketplace.json : version {v} différente de plugin.json {version_plugin}")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    racine_defaut = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Valide le skill linkedin-coach.")
    parser.add_argument("skill", nargs="?", help="dossier du skill (défaut : skills/linkedin-coach)")
    parser.add_argument("--root", default=str(racine_defaut), help="racine du dépôt")
    parser.add_argument("--strict", action="store_true",
                        help="plugin.json et CHANGELOG.md obligatoires (CI, release)")
    args = parser.parse_args(argv)

    racine = Path(args.root).resolve()
    skill = Path(args.skill).resolve() if args.skill else racine / "skills" / "linkedin-coach"

    erreurs, avertissements = [], []
    verifier_skill(skill, erreurs)
    verifier_versions(racine, args.strict, erreurs, avertissements)

    for a in avertissements:
        print(f"Avertissement : {a}")
    for e in erreurs:
        print(f"Erreur : {e}")
    if erreurs:
        print(f"✘ {len(erreurs)} erreur(s)")
        return 1
    print("✔ Skill valide")
    return 0


if __name__ == "__main__":
    sys.exit(main())
