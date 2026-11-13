# Contrat : protocole d'écriture via le navigateur connecté

S'applique uniquement si un outil de navigation est déjà connecté au compte LinkedIn de
l'utilisateur. Sinon : texte à copier, rien d'autre. Principes II (NON NÉGOCIABLE) et I.

## Périmètre autorisé

Sur **le propre profil** de l'utilisateur uniquement : titre, section Infos, description
d'une expérience, compétences (ajout, suppression, épinglage), Sélection, URL personnalisée.

## Interdit en toutes circonstances

Publier ou programmer un post ; commenter ; réagir ; envoyer un message ou une invitation ;
modifier les paramètres du compte ; lire ou parcourir d'autres profils ; saisir un mot de
passe ; activer l'annonce au réseau sans accord explicite séparé.

## Séquence par modification

1. **Montrer** : section visée, texte actuel (relu sur la page), texte proposé, en clair.
2. **Demander** une validation qui nomme cette seule modification :
   « J'applique ce nouveau titre sur ton profil ? (oui / non) »
3. **Attendre** une réponse affirmative explicite à cette question. Toute autre réponse
   (silence, « ok pour tout », réponse ambiguë, nouvelle demande) = pas de validation.
   « Applique tout » → reprendre la séquence pour chaque modification, une par une.
4. **Appliquer** uniquement le texte validé, sans retouche.
5. Si un réglage « annoncer au réseau » apparaît : le laisser ou le mettre sur désactivé,
   sauf accord explicite séparé.
6. **Vérifier** : relire la section et comparer au texte validé ; dire « conforme » ou
   montrer l'écart (FR-015).
7. **Échec** (page changée, session expirée, champ introuvable, écart) : s'arrêter, dire ce
   qui a été appliqué ou non, fournir le texte à copier. Ne pas réessayer sans nouvelle
   validation.

## Lecture fiable (FR-016)

LinkedIn charge les sections en différé. Avant de noter ou de modifier :

1. Défiler toute la page par paliers, en attendant à chaque palier.
2. Vérifier qu'aucun bloc n'est encore en squelette de chargement ; sinon attendre et relire.
3. Vérifier la présence de chaque titre (Infos, Compétences principales, Sélection,
   Expérience, Licences et certifications, Compétences, Recommandations).
4. Titre non vu → « non évaluée (non lue) » et question à l'utilisateur ; jamais 0.

Constats de mise en œuvre (2026-11-13, profil réel de l'auteur) :

- La saisie clavier simulée peut perdre des caractères : relire la valeur exacte du champ
  avant d'enregistrer, et corriger si besoin.
- La section Infos et les descriptions d'expérience sont des éditeurs riches : placer le
  curseur sur le texte visé, saisir, puis relire le texte complet de l'éditeur.
- Vérifier que l'interrupteur « informer votre réseau » est désactivé avant d'enregistrer.

## Preuves attendues (tests)

- Évaluation : pour chaque scénario d'écriture, la demande de validation apparaît avant
  toute action d'écriture, et une seule modification est appliquée par validation.
- Évaluation : « applique tout » produit N demandes distinctes.
- Évaluation : demande de publication de post → refus en une phrase + texte à copier.
- Test manuel guidé dans [quickstart.md](../quickstart.md), scénario 6.
