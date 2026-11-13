# Installer LinkedIn Coach

Quatre méthodes, au choix. Comptez moins de 2 minutes.

## 1. Claude Code : marketplace (recommandé)

Dans une session Claude Code :

```
/plugin marketplace add mohamedchaabani/linkedin-coach
/plugin install linkedin-coach@linkedin-coach
```

Ou dans un terminal :

```
claude plugin marketplace add mohamedchaabani/linkedin-coach
claude plugin install linkedin-coach@linkedin-coach
```

Vérifiez avec `claude plugin list` : `linkedin-coach@linkedin-coach` doit être `enabled`.
Le skill se déclenche tout seul quand vous écrivez par exemple « audite mon profil
LinkedIn ». Le plugin ajoute aussi quatre commandes : `/linkedin-coach:audit`,
`/linkedin-coach:improve`, `/linkedin-coach:post` et `/linkedin-coach:positioning`.

## 2. Une commande, pour Claude Code et les autres agents

```
npx skills add mohamedchaabani/linkedin-coach
```

Demande Node.js. Fonctionne avec les agents qui lisent le format SKILL.md.

## 3. Copie manuelle

Copiez le dossier `skills/linkedin-coach/` du dépôt dans votre dossier de skills :

| Système | Dossier |
|---|---|
| macOS, Linux | `~/.claude/skills/linkedin-coach/` |
| Windows | `%USERPROFILE%\.claude\skills\linkedin-coach\` |

Redémarrez Claude Code.

## 4. App Claude (web, desktop, iPhone/iPad, Android)

1. Téléchargez `linkedin-coach-vX.Y.Z.zip` dans la dernière release GitHub du dépôt.
2. Dans l'app Claude : **Customize → Skills → + → Create skill → Upload a skill**, puis
   choisissez le .zip.
3. Activez le skill. Il est alors disponible sur tous vos appareils.

Conseil : créez un **projet Claude** dédié (« LinkedIn Coach »). Au premier usage, le skill
vous donnera un bloc « positionnement » à coller dans les instructions de ce projet, pour
ne pas répondre aux mêmes questions à chaque conversation.

## Mettre à jour

Utilisez la même méthode qu'à l'installation :

| Méthode | Mise à jour |
|---|---|
| Marketplace | `claude plugin marketplace update linkedin-coach` puis `claude plugin update linkedin-coach@linkedin-coach`, et redémarrer la session |
| `npx skills add` | relancer `npx skills add mohamedchaabani/linkedin-coach` |
| Copie manuelle | remplacer le dossier `linkedin-coach/` par celui de la nouvelle version |
| App Claude | supprimer l'ancien skill, importer le nouveau .zip |

Votre positionnement et votre historique ne sont **pas** touchés : ils sont dans
`~/.linkedin-coach/` ou dans votre projet Claude, jamais dans le dossier du skill. Si le
format évolue un jour, le skill vous proposera la migration et vous montrera le résultat ;
il ne change rien en silence.

## Python (optionnel)

Le score « humanizer » et l'import de l'archive LinkedIn utilisent Python ≥ 3.9 (sans
paquet à installer). Sans Python, le skill fonctionne quand même : il fait la passe à la
main et vous le dit.

- macOS, Linux : en général déjà présent (`python3 --version`).
- Windows : `winget install Python.Python.3.12`, ou https://www.python.org/downloads/.

## Où sont mes données ?

Votre positionnement et l'historique de vos audits sont enregistrés **hors du dossier du
skill**, pour qu'une mise à jour ne les efface jamais :

- Claude Code : `~/.linkedin-coach/` (Windows : `%USERPROFILE%\.linkedin-coach\`), ou le
  dossier indiqué par la variable d'environnement `LINKEDIN_COACH_HOME`.
- App Claude : dans les instructions de votre projet Claude dédié.

Problème ? Voir [depannage.md](depannage.md).
