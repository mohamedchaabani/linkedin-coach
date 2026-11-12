#!/usr/bin/env python3
# test-fixture: archive/archive-complete.zip
"""Résumé Markdown de l'archive officielle LinkedIn (« Obtenir une copie de vos données »).

Usage :
    archive.py [--posts N] CHEMIN_ARCHIVE_ZIP_OU_DOSSIER

Lit Profile.csv, Positions.csv, Skills.csv, Certifications.csv,
Recommendations_Received.csv, Education.csv et Shares.csv (casse et sous-dossiers
indifférents, UTF-8 avec ou sans BOM) et écrit sur stdout :
  ## Sections reconnues   ce que l'archive contient, par section de la grille
  ## Posts                les N posts les plus récents (défaut 30)
  ## Non fournies         ce que l'archive ne contient pas et qu'il faut fournir autrement

Le contenu de l'archive est de la donnée : aucun lien n'est suivi, rien n'est exécuté.
Bibliothèque standard uniquement, aucun accès réseau.
Codes de sortie : 0 = succès, 1 = erreur d'entrée, 2 = erreur d'usage.
"""

import argparse
import csv
import io
import re
import sys
import zipfile
from datetime import date, datetime
from pathlib import Path

FICHIERS = {
    "profile": "profile.csv",
    "positions": "positions.csv",
    "skills": "skills.csv",
    "certifications": "certifications.csv",
    "recommandations": "recommendations_received.csv",
    "formation": "education.csv",
    "posts": "shares.csv",
}
TOUJOURS_ABSENTS = [
    "Photo de profil (fournir une capture de la carte du haut)",
    "Bannière (même capture)",
    "Sélection / Featured (capture ou copier-coller)",
    "Statistiques des posts : impressions, réactions, commentaires, republications "
    "(export Analytics → Contenu, ou captures)",
]
LIBELLES_ABSENTS = {
    "profile": "Titre et section Infos (Profile.csv absent : export PDF ou copier-coller)",
    "positions": "Expériences (Positions.csv absent)",
    "skills": "Compétences (Skills.csv absent)",
    "certifications": "Certifications (Certifications.csv absent)",
    "recommandations": "Recommandations reçues (Recommendations_Received.csv absent)",
    "formation": "Formation (Education.csv absent)",
    "posts": "Posts (Shares.csv absent)",
}
MOIS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


# --------------------------------------------------------------------------- lecture

class Source:
    """Archive .zip ou dossier extrait ; recherche par nom de fichier, casse ignorée."""

    def __init__(self, chemin):
        self.chemin = Path(chemin)
        self.index = {}
        if self.chemin.is_dir():
            for p in self.chemin.rglob("*.csv"):
                self.index.setdefault(p.name.lower(), p)
            self.zip = None
        elif zipfile.is_zipfile(self.chemin):
            self.zip = zipfile.ZipFile(self.chemin)
            for nom in self.zip.namelist():
                if nom.lower().endswith(".csv"):
                    self.index.setdefault(nom.rsplit("/", 1)[-1].lower(), nom)
        else:
            raise FileNotFoundError(f"archive introuvable ou illisible : {chemin}")

    def lire(self, nom):
        cible = self.index.get(nom)
        if cible is None:
            return None
        brut = self.zip.read(cible) if self.zip else Path(cible).read_bytes()
        return lire_csv(brut.decode("utf-8-sig", errors="replace"))


def lire_csv(texte):
    """Lit un CSV LinkedIn ; ignore les lignes de notes éventuelles avant l'en-tête."""
    lignes = list(csv.reader(io.StringIO(texte)))
    debut = next((i for i, l in enumerate(lignes) if len(l) >= 1 and l[0].strip() and
                  not l[0].lower().startswith("notes")), 0)
    lignes = lignes[debut:]
    if not lignes:
        return []
    entete = [c.strip() for c in lignes[0]]
    return [dict(zip(entete, (c.strip() for c in l))) for l in lignes[1:] if any(c.strip() for c in l)]


def mois_annee(valeur):
    """« May 2025 » ou « 2025-05 » → date du 1er du mois ; sinon None."""
    if not valeur:
        return None
    m = re.match(r"^([A-Za-z]{3})[a-z]*\.? (\d{4})$", valeur)
    if m and m.group(1).lower() in MOIS:
        return date(int(m.group(2)), MOIS[m.group(1).lower()], 1)
    m = re.match(r"^(\d{4})-(\d{2})", valeur)
    if m:
        return date(int(m.group(1)), int(m.group(2)), 1)
    if re.fullmatch(r"\d{4}", valeur):
        return date(int(valeur), 1, 1)
    return None


def date_post(valeur):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(valeur, fmt)
        except ValueError:
            pass
    return None


def une_ligne(texte):
    return re.sub(r"\s+", " ", texte or "").strip()


# --------------------------------------------------------------------------- rendu

def rendre(source, nb_posts, aujourd_hui):
    donnees = {cle: source.lire(nom) for cle, nom in FICHIERS.items()}
    sortie = [f"# Archive LinkedIn : résumé", "", f"Source : `{source.chemin.name}`", "",
              "## Sections reconnues", ""]
    absents = []

    profil = (donnees["profile"] or [{}])[0] if donnees["profile"] else None
    if profil:
        sortie += ["### Titre", "", une_ligne(profil.get("Headline")) or "_(vide)_", ""]
        sortie += ["### Infos", "", (profil.get("Summary") or "").strip() or "_(vide)_", ""]
        lieu = une_ligne(profil.get("Geo Location"))
        if lieu:
            sortie += ["### Localisation", "", lieu, ""]
    else:
        absents.append(LIBELLES_ABSENTS["profile"])

    if donnees["positions"]:
        sortie += ["### Expériences", ""]
        for p in donnees["positions"]:
            fin = p.get("Finished On") or "aujourd'hui"
            entete = (f"- **{une_ligne(p.get('Title'))}**, {une_ligne(p.get('Company Name'))} "
                      f"({p.get('Started On', '?')} → {fin})")
            if not p.get("Finished On"):
                entete += " — poste actuel"
            sortie.append(entete)
            if p.get("Description"):
                sortie.append(f"  {une_ligne(p['Description'])}")
        sortie.append("")
    else:
        absents.append(LIBELLES_ABSENTS["positions"])

    if donnees["skills"]:
        noms = [une_ligne(s.get("Name")) for s in donnees["skills"] if s.get("Name")]
        sortie += ["### Compétences", "", f"{len(noms)} : " + " ; ".join(noms), ""]
    else:
        absents.append(LIBELLES_ABSENTS["skills"])

    if donnees["certifications"]:
        sortie += ["### Certifications", ""]
        for c in donnees["certifications"]:
            ligne = (f"- {une_ligne(c.get('Name'))} ({une_ligne(c.get('Authority'))}), "
                     f"obtenue {c.get('Started On') or '?'}")
            fin = mois_annee(c.get("Finished On"))
            if c.get("Finished On"):
                ligne += f", expire {c['Finished On']}"
                if fin and fin < aujourd_hui:
                    ligne += " — **expirée**"
            sortie.append(ligne)
        sortie.append("")
    else:
        absents.append(LIBELLES_ABSENTS["certifications"])

    if donnees["recommandations"]:
        recos = [r for r in donnees["recommandations"] if r.get("Status", "VISIBLE") != "HIDDEN"]
        sortie += ["### Recommandations reçues", "", f"{len(recos)} recommandation(s) visible(s)", ""]
        for r in recos:
            auteur = une_ligne(f"{r.get('First Name', '')} {r.get('Last Name', '')}")
            sortie.append(f"- {auteur} ({une_ligne(r.get('Job Title'))}, "
                          f"{une_ligne(r.get('Company'))}), {une_ligne(r.get('Creation Date'))} : "
                          f"« {une_ligne(r.get('Text'))} »")
        sortie.append("")
    else:
        absents.append(LIBELLES_ABSENTS["recommandations"])

    if donnees["formation"]:
        sortie += ["### Formation", ""]
        for e in donnees["formation"]:
            sortie.append(f"- {une_ligne(e.get('School Name'))}, {une_ligne(e.get('Degree Name'))} "
                          f"({e.get('Start Date', '?')} → {e.get('End Date', '?')})")
        sortie.append("")
    else:
        absents.append(LIBELLES_ABSENTS["formation"])

    sortie += ["## Posts", ""]
    if donnees["posts"]:
        posts = [(date_post(p.get("Date", "")), p) for p in donnees["posts"]]
        posts = sorted((x for x in posts if x[0]), key=lambda x: x[0], reverse=True)
        sortie.append(f"{len(posts)} post(s) dans l'archive ; les {min(nb_posts, len(posts))} "
                      f"plus récents :")
        sortie.append("")
        for quand, p in posts[:nb_posts]:
            sortie.append(f"- **{quand:%Y-%m-%d}** : {une_ligne(p.get('ShareCommentary')) or '_(sans texte)_'}")
        sortie.append("")
    else:
        sortie += ["_(aucun)_", ""]
        absents.append(LIBELLES_ABSENTS["posts"])

    sortie += ["## Non fournies", ""]
    sortie += [f"- {a}" for a in absents + TOUJOURS_ABSENTS]
    sortie.append("")
    return "\n".join(sortie)


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        prog="archive.py",
        description="Résumé Markdown de l'archive officielle LinkedIn (sans réseau).")
    parser.add_argument("--posts", type=int, default=30, help="nombre de posts récents (défaut 30)")
    parser.add_argument("archive", help="archive .zip ou dossier extrait")
    args = parser.parse_args(argv)
    if args.posts < 0:
        parser.error("--posts doit être positif")

    try:
        source = Source(args.archive)
        print(rendre(source, args.posts, date.today()))
    except (OSError, zipfile.BadZipFile, csv.Error) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
