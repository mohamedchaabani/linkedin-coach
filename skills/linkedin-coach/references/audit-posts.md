# Audit des posts et historique des audits

## Données nécessaires

Pour chaque post : date, texte, impressions, réactions, commentaires, republications, et le
nombre d'abonnés (au moment du post si connu). Sources : `references/sources-profil.md`.
Idéalement les 10 à 30 derniers posts.

## Indicateurs (montrer le calcul)

- **Taux d'engagement** = (réactions + commentaires + republications) / impressions
- **Ratio commentaires** = commentaires / réactions
- **Multiple de portée** = impressions / abonnés

Une division par zéro (ex. 0 impression) ou une donnée manquante donne
**« non calculable »**. Jamais d'estimation, jamais de 0 % par défaut.

## Analyse

1. Classer les posts selon ces indicateurs, pas selon les impressions brutes.
2. Comparer le top 5 et le flop 5 sur : type d'accroche (affirmation, chiffre, question…),
   thème, spécificité (chiffres, noms, faits vécus), longueur, réponses dans la 1re heure si
   connues. Le jour et l'heure se regardent en dernier.
3. **Moins de 10 posts** : le dire franchement, « aucune tendance n'est fiable », et se
   limiter à des observations post par post.

## Note du contenu, sur 20

| Critère | Pts | 5/5 si… |
|---|---|---|
| Accroche | 5 | Ligne 1 = affirmation ou chiffre, jamais une question ; tient sur mobile (~140 caractères). |
| Spécificité | 5 | Chiffres, noms (techno, outil, version), détail vécu à la 1re personne. |
| Cohérence | 5 | Les posts servent le positionnement et la cible ; piliers reconnaissables. |
| Régularité | 5 | 3 à 5 posts par semaine sur la période, sans trou de plus de 2 semaines. |

## Historique des audits

Format exact : `templates/historique-audits.md`. Stocké à côté du positionnement :
`~/.linkedin-coach/historique-audits.md` (ou dossier de `LINKEDIN_COACH_HOME`), ou bloc
`<!-- linkedin-coach:historique v1 -->` dans les instructions du projet Claude.

**Après chaque audit**, ajouter **une** ligne en fin de tableau :

| Colonne | Valeur |
|---|---|
| Date | date du jour `AAAA-MM-JJ` |
| Profil | `points/maximum atteignable` (ex. `41/88`), ou `—` si aucun critère évalué |
| Critères évalués | `N/12` |
| Posts | `note/20`, ou `—` si aucun post fourni |
| Corrections prioritaires | les 3 corrections, en quelques mots, séparées par ` ; ` |

Règles :

- Ne jamais modifier une ligne passée.
- **Aucun** extrait du profil ou des posts dans l'historique.
- Mode local : demander l'accord la première fois, puis ajouter la ligne au fichier.
- Mode projet : donner le **bloc complet** mis à jour, à coller à la place de l'ancien.
- Historique absent ou illisible : faire l'audit sans comparaison et le dire en une ligne.

**Comparaison** avec la dernière ligne, en fin d'audit :

```
PROGRESSION   41/88 → 58/88 (+17) depuis le 2026-09-15
              corrections traitées : titre, Infos ; restante : recommandations
```

Si le nombre de critères évalués diffère, l'écrire : la comparaison n'est pas directe
(« 5/12 → 10/12 critères évalués »).
