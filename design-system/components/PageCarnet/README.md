# PageCarnet

Page d'un chapitre de carnet de bord, telle que le site la présente : numéro et titre, exercices, livrable validé en séance. C'est le modèle le plus proche d'une page de workbook.

**Fournir** : le numéro, le sous-titre, le titre et l'objectif du chapitre, ses 4 exercices, le titre et le texte du livrable.

**Règles**
- Page `surface-card`, `radius-carte`, posée sur `surface-alt`, marges intérieures `space-10`, trois colonnes (une sur mobile).
- Colonne 1 : NumeroChapitre, titre `titre-bloc`, objectif `corps` en `ink-muted`.
- Colonne 2 : `sourcil` « Exercices & protocoles » et ListeEtoiles.
- Colonne 3 : PostIt jasmin du livrable (rotation -1°) : `sourcil` « Livrable », titre `titre-element`, texte `corps-petit` en `ink`, Tampon.

**Ne pas faire** : présenter un carnet comme une séance, ajouter un second post-it sur la page.
