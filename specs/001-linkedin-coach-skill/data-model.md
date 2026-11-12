# Modèle de données : LinkedIn Coach

**Feature** : `001-linkedin-coach-skill` | **Date** : 2026-11-12 | **Plan** : [plan.md](plan.md)

Pas de base de données. Deux entités sont **persistées** chez l'utilisateur (fichiers
Markdown, voir [contracts/user-files.md](contracts/user-files.md)) ; les autres n'existent que
dans la conversation ou sont des données de référence livrées avec le skill.

| Entité | Persistance | Où |
|---|---|---|
| Positionnement | Oui | `~/.linkedin-coach/positionnement.md` ou instructions du projet Claude |
| Historique des audits | Oui | `~/.linkedin-coach/historique-audits.md` ou instructions du projet Claude |
| Profil importé, Post, Audit, Réécriture, Modification de profil, Fiche POST PRÊT, Score humanizer | Non (conversation) | — |
| Formule d'accroche, Critère de grille, Lexique IA | Référence (lecture seule) | `skills/linkedin-coach/references/` |

Convention : `{{à confirmer}}` marque toute valeur inconnue (principe III). Une valeur
`{{à confirmer}}` n'est jamais remplacée par une supposition.

---

## Positionnement

| Champ | Type | Règles |
|---|---|---|
| `version_format` | entier | `1` ; permet de migrer le format plus tard |
| `langue` | `fr` \| `en` | obligatoire ; défaut des textes produits (FR-080) |
| `role_seniorite` | texte | ex. « Architecte AEM, 12 ans » |
| `expertises` | liste de 3 à 5 textes | |
| `certifications` | liste de `{nom, date_obtention, date_expiration?}` | dates ISO `AAAA-MM` ; expirée si `date_expiration` < aujourd'hui (FR-034) |
| `url_profil` | URL | `https://www.linkedin.com/in/...` ou site |
| `cible` | `{postes[], contrats[], villes[], remote: oui/non/hybride}` | sert aux mots-clés recruteurs (FR-040) |
| `terrain_reel` | liste de faits | projets, outils, chiffres vrais ; matière des posts (FR-051) |
| `references_clients` | liste de textes | anonymisés par défaut (FR-070) |
| `piliers` | liste de 4 à 5 `{nom, description}` | rempli par le mode POSTS (FR-050) |
| `mis_a_jour_le` | date ISO | |

- **Création** : onboarding, 7 questions maximum (FR-020). Réponse vide → `{{à confirmer}}`.
- **Modification** : à la demande (FR-022) ; seuls les champs changés sont réécrits.
- **États** : `absent` → onboarding ; `partiel` (au moins un `{{à confirmer}}`) → utilisable,
  champs signalés ; `complet` ; `illisible` → onboarding qui propose de reprendre les valeurs
  encore lisibles.

## Historique des audits

Liste ordonnée chronologiquement d'**entrées d'audit** :

| Champ | Type | Règles |
|---|---|---|
| `date` | date ISO | |
| `note_profil` | entier 0–100 ou `null` | `null` si aucun critère évalué |
| `criteres_evalues` | entier 0–12 | nombre de critères notés (les autres sont « non évalués ») |
| `note_posts` | entier 0–20 ou `null` | `null` si aucun post fourni |
| `corrections` | liste de 3 textes courts | les 3 corrections prioritaires |

- **Interdit** : texte du profil ou des posts (FR-035).
- **Ajout** : une entrée après chaque audit (FR-035). Jamais de modification d'une entrée
  passée.
- **Comparaison** (FR-036) : avec la dernière entrée ; si `criteres_evalues` diffère,
  l'écart de note est affiché avec cette réserve.

## Profil importé (conversation)

- `source` : `archive` | `pdf` | `copier-coller` | `navigateur`.
- `sections` : pour chacun des 12 critères de la grille, `fournie` / `non fournie` + contenu.
- `instructions_suspectes` : liste des instructions trouvées dans le contenu, signalées et
  ignorées (FR-014).

## Post et statistiques (conversation)

`texte`, `date`, `impressions`, `reactions`, `commentaires`, `republications`, `abonnes`
(au moment du post si connu). Indicateurs (FR-032) :

- taux d'engagement = (réactions + commentaires + republications) / impressions
- ratio commentaires = commentaires / réactions
- multiple de portée = impressions / abonnés
- division par zéro ou donnée manquante → indicateur « non calculable », jamais estimé.

## Audit (conversation)

- `criteres` : 12 × `{nom, points_max, points | "non évalué", justification}` ; barème dans
  `references/grille-profil.md` (total des `points_max` = 100).
- `note_profil` = somme des points des critères évalués, **affichée avec le maximum
  atteignable** (ex. `41/88 (bannière et photo non évaluées)`) pour ne jamais noter ce qui n'a
  pas été vu (FR-031).
- `note_posts` : 4 × 5 points (accroche, spécificité, cohérence, régularité) ; mention
  « tendance non fiable » si moins de 10 posts.
- `incoherences`, `corrections_prioritaires` (3, triées par points perdus).

## Réécriture (conversation)

`section`, `texte_avant` (si fourni), `texte_propose`, `longueur`, `limite` (titre 220,
Infos 1 400, accroche Infos ~265), `a_confirmer[]`, `gain_estime`.

## Modification de profil (conversation)

Cycle de vie strict (FR-013, FR-015) :

```
proposée → montrée (avant/après) → validée | refusée
validée → appliquée → vérifiée (conforme | écart signalé)
validée → échec (arrêt + texte à copier)
```

- Une validation porte sur **une** modification identifiée ; elle n'est jamais réutilisée.
- `annonce_reseau` : toujours `désactivée` sauf accord explicite séparé.

## Fiche POST PRÊT (conversation)

`pilier`, `accroche` (n° de formule), `longueur` (caractères), `creneau`, `premier_commentaire`,
`a_verifier[]`, `humanizer` (`{mode: manuel|outillé, avant, après}`).

## Données de référence

- **Formule d'accroche** : `{numero, nom, modele, exemple?}` ; au moins 16 (FR-052).
- **Critère de grille** : `{nom, points_max, conditions_note_max}`.
- **Lexique IA** : un terme ou une expression par ligne, par langue ; lignes `#` = commentaires.
