#!/usr/bin/env python3
"""Régénère les fixtures d'archive LinkedIn anonymisées.

Usage : python tests/fixtures/archive/make_fixtures.py

Colonnes calquées sur l'export officiel « Obtenir une copie de vos données » (fichiers en
anglais, encodage UTF-8 avec BOM). Toutes les données sont fictives.
"""

import csv
import io
import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

ICI = Path(__file__).resolve().parent

PROFILE = [["First Name", "Last Name", "Maiden Name", "Address", "Birth Date", "Headline",
            "Summary", "Industry", "Zip Code", "Geo Location", "Twitter Handles", "Websites",
            "Instant Messengers"],
           ["Camille", "Exemple", "", "", "", "Architecte AEM | Adobe Experience Manager",
            "J'accompagne des équipes digitales sur AEM depuis 12 ans. Migration vers le cloud, "
            "performance, gouvernance des composants.", "IT Services", "", "Paris, Île-de-France",
            "", "[PORTFOLIO:https://exemple.invalid]", ""]]

POSITIONS = [["Company Name", "Title", "Description", "Location", "Started On", "Finished On"],
             ["Cabinet Exemple", "Architecte AEM", "Migration de 40 sites vers AEM as a Cloud "
              "Service pour une banque européenne.", "Paris", "Mar 2021", ""],
             ["ESN Fictive", "Développeur AEM senior", "Développement de composants et "
              "intégration continue.", "Lyon", "Sep 2016", "Feb 2021"],
             ["Agence Imaginaire", "Développeur Java", "", "Lyon", "Jul 2012", "Aug 2016"]]

SKILLS = [["Name"], ["Adobe Experience Manager"], ["Java"], ["Architecture cloud"],
          ["Apache Sling"], ["CI/CD"]]

CERTIFICATIONS = [["Name", "Url", "Authority", "Started On", "Finished On", "License Number"],
                  ["Adobe Certified Expert - AEM Sites Architect", "", "Adobe", "May 2023",
                   "May 2025", "XXXX"],
                  ["AWS Certified Solutions Architect - Associate", "", "Amazon Web Services",
                   "Jan 2024", "Jan 2027", "YYYY"]]

RECOMMANDATIONS = [["First Name", "Last Name", "Company", "Job Title", "Text", "Creation Date",
                    "Status"],
                   ["Dominique", "Fictif", "Banque Fictive", "Product Owner",
                    "Camille a mené la migration avec méthode et a réduit nos délais de publication.",
                    "06/12/24, 10:30 AM", "VISIBLE"],
                   ["Alex", "Imaginaire", "ESN Fictive", "Manager",
                    "Très bon développeur, toujours disponible.", "03/02/19, 09:15 AM", "VISIBLE"]]

EDUCATION = [["School Name", "Start Date", "End Date", "Notes", "Degree Name", "Activities"],
             ["École d'ingénieurs Exemple", "2007", "2012", "", "Diplôme d'ingénieur", ""]]


def shares():
    lignes = [["Date", "ShareLink", "ShareCommentary", "SharedUrl", "MediaUrl", "Visibility"]]
    debut = datetime(2026, 10, 30, 8, 15)
    for i in range(40):
        date = debut - timedelta(days=7 * i)
        texte = (f"Post n°{40 - i} : retour d'expérience AEM numéro {40 - i}. "
                 f"J'ai appris quelque chose de concret cette semaine.")
        if i == 3:
            texte += " Lien utile : https://exemple.invalid/article"
        lignes.append([date.strftime("%Y-%m-%d %H:%M:%S"),
                       f"https://www.linkedin.com/feed/update/urn:li:share:{1000 + i}",
                       texte, "", "", "MEMBER_NETWORK"])
    return lignes


def csv_bytes(lignes):
    tampon = io.StringIO(newline="")
    csv.writer(tampon, lineterminator="\r\n").writerows(lignes)
    return tampon.getvalue().encode("utf-8-sig")


def main():
    complete = {
        "Profile.csv": PROFILE, "Positions.csv": POSITIONS, "Skills.csv": SKILLS,
        "Certifications.csv": CERTIFICATIONS, "Recommendations_Received.csv": RECOMMANDATIONS,
        "Education.csv": EDUCATION, "Shares.csv": shares(),
    }
    with zipfile.ZipFile(ICI / "archive-complete.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for nom, lignes in complete.items():
            z.writestr(nom, csv_bytes(lignes))

    partielle = ICI / "archive-partielle"
    if partielle.exists():
        shutil.rmtree(partielle)
    sous = partielle / "Basic_LinkedIn_Data_2026"
    sous.mkdir(parents=True)
    for nom, lignes in (("profile.csv", PROFILE), ("POSITIONS.csv", POSITIONS),
                        ("Certifications.csv", CERTIFICATIONS), ("Education.csv", EDUCATION)):
        (sous / nom).write_bytes(csv_bytes(lignes))
    print("fixtures régénérées")


if __name__ == "__main__":
    main()
