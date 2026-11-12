---
type: llm
weight: 1
---

Le profil fourni ne contient ni photo, ni bannière, ni sélection, ni recommandations,
ni activité. La réponse réussit si TOUTES ces conditions sont vraies :

1. Photo, bannière (et les autres sections absentes) sont marquées « non évaluée » et ne
   reçoivent aucun point.
2. La note du profil est affichée sur le maximum atteignable (par ex. `24/70`), pas sur 100,
   avec le nombre de critères non évalués.
3. Chaque critère noté a une justification d'une ligne.
4. La note est sévère : titre réduit à un intitulé de poste, Infos avec « Passionné »,
   « Rigoureux », « orienté résultats », expériences sans résultat chiffré sont pénalisés.
5. Exactement 3 corrections prioritaires, classées par points perdus.
6. Aucun chiffre ou résultat n'est inventé pour l'utilisateur.
