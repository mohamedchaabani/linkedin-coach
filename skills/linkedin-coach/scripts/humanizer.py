#!/usr/bin/env python3
# test-fixture: humanizer/fr-naturel.txt detect --json
"""Humanizer bilingue FR/EN de LinkedIn Coach.

Sous-commandes :
    detect [--lang fr|en|auto] [--json] [FICHIER | -]   score sur 100 (5 critères /20)
    clean  [--lang fr|en|auto] [FICHIER | -]            corrections mécaniques sûres

Critères : ponctuation, vocabulaire, tournures, rythme, voix.
Idée d'origine : detect.py de li-human (Jakeschincariol/linkedin-agent-skill, MIT,
Copyright (c) 2026 Jake Schincariol). Réécrit pour traiter le français et l'anglais à
égalité ; le critère « voix » reconnaît « je », « j' », « nous », « on ».

Bibliothèque standard uniquement, aucun accès réseau.
Codes de sortie : 0 = succès, 1 = erreur d'entrée, 2 = erreur d'usage.
"""

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"

MAX = 20
INVISIBLES = "​‌‍⁠﻿"
EMOJIS_GENERIQUES = "🚀🔥💡✨🎯👇💪🙌✅📈⚡🌟"
APOSTROPHES = "’ʼ"

MOTS_OUTILS = {
    "fr": {"le", "la", "les", "de", "des", "du", "et", "est", "un", "une", "je", "nous",
           "que", "qui", "pas", "pour", "dans", "avec", "sur", "ce", "en", "à", "il", "on",
           "au", "aux", "mais", "ou", "sont", "elle", "vous", "mon", "ma", "mes", "c", "j",
           "n", "d", "l", "qu", "s", "plus", "très", "cette", "ces", "être", "avoir"},
    "en": {"the", "and", "is", "of", "to", "a", "an", "in", "that", "it", "we", "i",
           "you", "for", "with", "on", "was", "not", "be", "this", "are", "but", "or",
           "my", "our", "they", "have", "has", "what", "at", "by", "from", "as", "s",
           "t", "d", "ll", "ve", "re", "m", "if", "nobody", "no", "one"},
}

PREMIERE_PERSONNE = {
    "fr": {"je", "j", "me", "m", "moi", "mon", "ma", "mes", "nous", "notre", "nos", "on"},
    "en": {"i", "me", "my", "mine", "we", "us", "our", "ours"},
}
CONTRACTIONS_EN = re.compile(r"\b\w+'(?:s|t|d|ll|ve|re|m)\b", re.IGNORECASE)

CONTRASTES = {
    "fr": re.compile(r"\bn'est pas (?:qu'un |qu'une |juste |seulement )?[^.!?\n]{1,60}?"
                     r"[,—–:;]\s*c'est\b", re.IGNORECASE),
    "en": re.compile(r"\b(?:is|are|was|it's|that's|this is|it is) not (?:just |only |merely )?"
                     r"[^.!?\n]{1,60}?[,—–:;]\s*(?:it's|it is|they're|this is|that's)\b",
                     re.IGNORECASE),
}
FORMULES = {
    "fr": ["le résultat ?", "le résultat :", "plot twist", "voici ce que", "voici pourquoi :",
           "spoiler :", "laissez-moi vous expliquer"],
    "en": ["the result?", "plot twist", "here's the thing", "here's what", "let that sink in",
           "spoiler:", "let me explain"],
}
MOT = r"[\w'-]+"
TRIADE = {
    "fr": re.compile(rf"\b{MOT}(?:\s{MOT}){{0,2}},\s{MOT}(?:\s{MOT}){{0,2}},?\s(?:et|ou)\s{MOT}",
                     re.IGNORECASE),
    "en": re.compile(rf"\b{MOT}(?:\s{MOT}){{0,2}},\s{MOT}(?:\s{MOT}){{0,2}},?\s(?:and|or)\s{MOT}",
                     re.IGNORECASE),
}


# --------------------------------------------------------------------------- utilitaires

def normaliser(texte):
    for a in APOSTROPHES:
        texte = texte.replace(a, "'")
    return texte


def mots(texte):
    return re.findall(r"[^\W_]+(?:'[^\W_]+)*", normaliser(texte).lower())


def jetons(texte):
    """Mots découpés aux apostrophes : « j'ai » → j, ai ; « I'd » → i, d."""
    return [j for m in mots(texte) for j in m.split("'") if j]


def phrases(texte):
    morceaux = []
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        if not ligne or est_puce(ligne):
            continue
        morceaux += [p for p in re.split(r"(?<=[.!?…])\s+", ligne) if mots(p)]
    return morceaux


def est_puce(ligne):
    return bool(re.match(r"^\s*(?:[-•*]|\d+[.)])\s+", ligne))


def charger_lexique(langue):
    termes = []
    fichier = DATA / f"lexique-ia.{langue}.txt"
    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        ligne = normaliser(ligne.strip().lower())
        if ligne and not ligne.startswith("#"):
            termes.append(ligne)
    return termes


def detecter_langue(texte):
    compte = {lang: 0 for lang in MOTS_OUTILS}
    for j in jetons(texte):
        for lang, outils in MOTS_OUTILS.items():
            if j in outils:
                compte[lang] += 1
    total = sum(compte.values()) or 1
    if min(compte.values()) / total >= 0.35:
        return "mixte"
    return "fr" if compte["fr"] >= compte["en"] else "en"


def langues_de(langue):
    return ("fr", "en") if langue == "mixte" else (langue,)


# --------------------------------------------------------------------------- critères

def critere_ponctuation(texte, langue):
    score, constats = MAX, []
    nb_mots = max(len(mots(texte)), 1)
    tirets = texte.count("—") + len(re.findall(r"\s–\s", texte))
    permis = max(1, nb_mots // 100)
    if tirets > permis:
        score -= 4 * (tirets - permis)
        constats.append(f"{tirets} tirets cadratins pour {nb_mots} mots (max {permis})")
    if "en" in langues_de(langue):
        courbes = sum(texte.count(c) for c in "“”")
        if courbes:
            score -= min(6, 2 * courbes)
            constats.append(f"{courbes} guillemets courbes")
    invisibles = sum(texte.count(c) for c in INVISIBLES)
    if invisibles:
        score -= 6
        constats.append(f"{invisibles} caractère(s) invisible(s)")
    emojis = [c for c in texte if c in EMOJIS_GENERIQUES]
    if emojis:
        score -= min(9, 3 * len(emojis))
        constats.append("emojis génériques : " + "".join(emojis))
    hashtags = len(re.findall(r"(?<!\w)#\w+", texte))
    if hashtags > 3:
        score -= 4
        constats.append(f"{hashtags} hashtags (max 3)")
    return max(score, 0), constats


def critere_vocabulaire(texte, langue):
    bas = normaliser(texte).lower()
    trouves = []
    for lang in langues_de(langue):
        for terme in charger_lexique(lang):
            n = len(re.findall(r"(?<!\w)" + re.escape(terme) + r"(?!\w)", bas))
            if n:
                trouves.append((terme, n))
    total = sum(n for _, n in trouves)
    return max(MAX - 3 * total, 0), [f"« {t} »" + (f" ×{n}" if n > 1 else "") for t, n in trouves]


def critere_tournures(texte, langue):
    score, constats = MAX, []
    bas = normaliser(texte).lower()
    contrastes = sum(len(CONTRASTES[lang].findall(bas)) for lang in langues_de(langue))
    if contrastes > 1:
        score -= 5 * (contrastes - 1)
        constats.append(f"{contrastes} contrastes « ce n'est pas X, c'est Y » (max 1)")
    for lang in langues_de(langue):
        for formule in FORMULES[lang]:
            if formule in bas:
                score -= 5
                constats.append(f"formule toute faite « {formule} »")
    triades = sum(len(TRIADE[lang].findall(p)) for lang in langues_de(langue)
                  for p in phrases(normaliser(texte)))
    if triades > 1:
        score -= 4 * (triades - 1)
        constats.append(f"{triades} énumérations par trois (max 1)")
    premiere = next((l.strip() for l in texte.splitlines() if l.strip()), "")
    if premiere.endswith("?"):
        score -= 4
        constats.append("la première ligne est une question")
    return max(score, 0), constats


def coefficient_variation(longueurs):
    if len(longueurs) < 2:
        return None
    moyenne = statistics.mean(longueurs)
    return statistics.pstdev(longueurs) / moyenne if moyenne else None


def critere_rythme(texte, langue):
    constats = []
    longueurs = [len(mots(p)) for p in phrases(texte)]
    if len(longueurs) < 4:
        score = MAX
        constats.append("texte trop court pour juger le rythme")
    else:
        cv = coefficient_variation(longueurs)
        score = round(4 + (min(max(cv, 0.2), 0.6) - 0.2) / 0.4 * 16)
        if score < 14:
            constats.append(f"phrases de longueur trop régulière ({min(longueurs)} à "
                            f"{max(longueurs)} mots, variation {cv:.2f})")
    puces = [len(mots(l)) for l in texte.splitlines() if est_puce(l)]
    cv_puces = coefficient_variation(puces) if len(puces) >= 3 else None
    if cv_puces is not None and cv_puces < 0.25:
        score -= 6
        constats.append(f"{len(puces)} puces de longueur presque identique")
    return max(min(score, MAX), 0), constats


def critere_voix(texte, langue):
    js = jetons(texte)
    nb_mots = max(len(mots(texte)), 1)
    marqueurs = sum(1 for j in js for lang in langues_de(langue) if j in PREMIERE_PERSONNE[lang])
    contractions = len(CONTRACTIONS_EN.findall(normaliser(texte))) if "en" in langues_de(langue) else 0
    # Les contractions anglaises comptent peu : le français n'a pas d'équivalent, et la
    # 1re personne doit peser autant dans les deux langues (principe VII).
    taux = (marqueurs + 0.25 * contractions) * 100 / nb_mots
    score = min(MAX, round(4 + taux * 4))
    constats = [f"1re personne : {marqueurs} occurrence(s)"]
    if contractions:
        constats.append(f"contractions : {contractions}")
    if marqueurs == 0:
        constats.append("aucune 1re personne : texte impersonnel")
    return score, constats


CRITERES = (
    ("ponctuation", critere_ponctuation),
    ("vocabulaire", critere_vocabulaire),
    ("tournures", critere_tournures),
    ("rythme", critere_rythme),
    ("voix", critere_voix),
)


def analyser(texte, langue="auto"):
    if langue == "auto":
        langue = detecter_langue(texte)
    resultats = {}
    for nom, fonction in CRITERES:
        score, constats = fonction(texte, langue)
        resultats[nom] = {"score": score, "max": MAX, "constats": constats}
    return {
        "lang": langue,
        "score": sum(r["score"] for r in resultats.values()),
        "criteres": resultats,
    }


# --------------------------------------------------------------------------- nettoyage

def nettoyer(texte, langue="auto"):
    if langue == "auto":
        langue = detecter_langue(texte)
    changements = []

    n = sum(texte.count(c) for c in INVISIBLES)
    if n:
        texte = re.sub(f"[{INVISIBLES}]", "", texte)
        changements.append(f"{n} caractère(s) invisible(s) supprimé(s)")

    tirets = 0

    def remplacer_tiret(m):
        nonlocal tirets
        tirets += 1
        suite = m.string[m.end():m.end() + 1]
        if not suite or suite == "\n":
            return "."
        return ". " if suite.isupper() else ", "

    # Tiret cadratin (ou demi-cadratin entouré d'espaces) après un mot, hors début de ligne.
    texte = re.sub(r"(?<=[^\s])[ \t]*(?:—|[ \t]–)[ \t]*", remplacer_tiret, texte)
    if tirets:
        changements.append(f"{tirets} tiret(s) cadratin(s) remplacé(s)")

    if langue == "en":
        n = sum(texte.count(c) for c in "“”‘’")
        if n:
            texte = (texte.replace("“", '"').replace("”", '"')
                     .replace("‘", "'").replace("’", "'"))
            changements.append(f"{n} guillemet(s) ou apostrophe(s) courbe(s) redressé(s)")

    lignes, espaces = [], 0
    for ligne in texte.split("\n"):
        debut = re.match(r"^[ \t]*", ligne).group(0)
        corps = ligne[len(debut):]
        nouveau = re.sub(r"[ \t]{2,}", " ", corps).rstrip(" \t")
        if nouveau != corps:
            espaces += 1
        lignes.append(debut + nouveau if nouveau else "")
    texte = "\n".join(lignes)
    if espaces:
        changements.append(f"espaces superflus corrigés sur {espaces} ligne(s)")

    return texte, changements


# --------------------------------------------------------------------------- CLI

def lire_entree(chemin):
    if chemin == "-":
        return sys.stdin.read()
    fichier = Path(chemin)
    if not fichier.is_file():
        raise FileNotFoundError(f"fichier introuvable : {chemin}")
    return fichier.read_text(encoding="utf-8")


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="humanizer.py",
        description="Humanizer bilingue FR/EN de LinkedIn Coach (score et nettoyage).")
    sous = parser.add_subparsers(dest="commande", required=True)
    for nom, aide in (("detect", "score sur 100 (5 critères notés sur 20)"),
                      ("clean", "corrections mécaniques sûres, sans changer les mots")):
        p = sous.add_parser(nom, help=aide)
        p.add_argument("--lang", choices=("fr", "en", "auto"), default="auto")
        if nom == "detect":
            p.add_argument("--json", action="store_true", help="sortie JSON")
        p.add_argument("fichier", nargs="?", default="-", help="fichier texte ou - (stdin)")
    return parser


def main(argv=None):
    for flux in (sys.stdout, sys.stderr, sys.stdin):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8")
    args = construire_parser().parse_args(argv)
    try:
        texte = lire_entree(args.fichier)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    if not texte.strip():
        print("Erreur : texte vide", file=sys.stderr)
        return 1

    if args.commande == "detect":
        res = analyser(texte, args.lang)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"langue      {res['lang']}")
            for nom, c in res["criteres"].items():
                detail = " ; ".join(c["constats"])
                print(f"{nom:<12}{c['score']:>2}/{c['max']}  {detail}".rstrip())
            print(f"SCORE {res['score']}/100")
    else:
        propre, changements = nettoyer(texte, args.lang)
        sys.stdout.write(propre)
        print("; ".join(changements) if changements else "aucun changement", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
