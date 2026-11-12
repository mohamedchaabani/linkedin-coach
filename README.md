# LinkedIn Coach

*[English version](README.en.md)*

Un skill open source pour Claude qui vous aide à **être trouvé et contacté par des
recruteurs et des clients** sur LinkedIn : audit noté de votre profil et de vos posts,
réécritures prêtes à copier, posts courts qui ne sonnent pas « IA ».

Gratuit, sous licence MIT, sans service payant ni dépendance. Fonctionne avec Claude Code
(macOS, Windows, Linux) et dans l'app Claude (web, desktop, iPhone/iPad, Android).

## Ce que fait le skill

- **Audit** : note du profil sur 100 (12 critères), note des posts sur 20, incohérences
  repérées, 3 corrections prioritaires, progression depuis votre dernier audit.
- **Améliorer** : titre, section Infos, expériences, compétences, Sélection, bannière,
  demandes de recommandation. Avec votre accord, il peut appliquer une modification sur
  votre profil via votre navigateur connecté, **une validation par modification**.
- **Posts** : piliers de contenu, 3 accroches au choix, post de 700 à 900 caractères construit
  sur **vos** faits, fiche « POST PRÊT » et score humanizer avant/après.

## Ce qu'il ne fera jamais

- Scraper LinkedIn, vous demander votre mot de passe, lire des profils tiers ou votre fil.
- Publier, envoyer un message ou une invitation, ou modifier votre profil sans votre
  validation explicite, action par action.
- Inventer un chiffre, un client ou un résultat : ce qui manque devient `{{à confirmer}}`.
- Envoyer vos données ailleurs : votre positionnement reste sur votre poste (ou dans votre
  projet Claude). Aucune télémétrie.

## Installation rapide

Claude Code :

```
/plugin marketplace add mohamedchaabani/linkedin-coach
/plugin install linkedin-coach@linkedin-coach
```

Autres méthodes (`npx skills add`, copie manuelle, .zip pour l'app Claude) :
[docs/fr/installation.md](docs/fr/installation.md). Problème :
[docs/fr/depannage.md](docs/fr/depannage.md).

## Exemples de demandes

- « Audite mon profil LinkedIn » (avec votre archive LinkedIn, un export PDF ou un
  copier-coller)
- « Réécris mon titre pour des postes d'architecte solution à Genève »
- « Écris un post sur la migration qu'on a finie la semaine dernière »
- « Mets à jour mon positionnement »

## Pour contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md) : ajouter une formule d'accroche, un terme au
lexique de l'humanizer, ou corriger une règle. Le projet suit une
[constitution](.specify/memory/constitution.md) et le workflow
[Spec Kit](https://github.com/github/spec-kit).

## Crédits

LinkedIn Coach s'inspire de deux projets sous licence MIT, crédités dans
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) :

- [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) (Sergey
  Bulaev) : formules d'accroche et règles de publication.
- [Jakeschincariol/linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)
  (Jake Schincariol) : grille de notation du profil et humanizer.

## Licence

[MIT](LICENSE).
