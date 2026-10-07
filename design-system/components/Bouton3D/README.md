# Bouton3D

Bouton à double calque (fond blanc décalé, contour décalé) : l'action principale d'un écran.

**Fournir** : un libellé court en minuscules, un lien, la variante (rouge par défaut, bleue pour l'action secondaire), éventuellement une pastille (durée, nombre de questions).

**Règles**
- Calque `surface-card` décalé de +3/+3 px, contour 1 px `brand-red` décalé de -3/-3 px ; au survol et au focus, les calques s'écartent à 6 px et la flèche avance de 7 px (0,2 s).
- Libellé DM Sans 900 en minuscules, `brand-red` (ou `brand-blue`), avec la flèche pleine.
- 62 px de haut (`radius-bouton`) ; compact : 48 px (`radius-bouton-compact`). Cible tactile de 44 px au moins.
- Pastille : `pastille` sur `surface-card`, bordure 1 px de la couleur du bouton, à cheval sur le contour (12 px au-dessus).
- Focus : contour `brand-red` de 2 px décalé de 4 px.
- Seulement sur `surface` ou `surface-card` : le rouge ne tient pas sur un pastel.

**Ne pas faire** : de bouton plein coloré, de majuscules, deux boutons rouges côte à côte. Sur papier, ce bouton n'a pas de sens : utiliser LienFleche.
