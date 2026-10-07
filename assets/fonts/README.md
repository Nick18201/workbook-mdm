# Polices

## DA « Éditorial & Affirmé » (voir `DA-workbook.md`, section 4)

| Fichier | Police | Graisse | Rôle | Licence |
|---|---|---|---|---|
| `DMSans-Bold.ttf` | DM Sans | 700 (opsz 18) | Titres courants, titres de carte | OFL |
| `DMSans-ExtraBold.ttf` | DM Sans | 800 (opsz 40) | Grands titres | OFL |
| `DMSans-Italic.ttf` | DM Sans | italique 400 (opsz 18) | 2e partie d'un titre | OFL |
| `Manrope-Regular.ttf` | Manrope | 400 | Texte courant | OFL |
| `Manrope-SemiBold.ttf` | Manrope | 600 | Gras dans le texte | OFL |
| `Manrope-ExtraBold.ttf` | Manrope | 800 | Logotype | OFL |
| `PTMono-Regular.ttf` | PT Mono | 400 | Repères : sourcils, étiquettes, numéros, folio | OFL |
| `InstrumentSerif-Italic.ttf` | Instrument Serif | italique 400 | Post-it, annotations | OFL |
| `MaterialSymbolsOutlined.ttf` | Material Symbols Outlined | FILL 0, GRAD 0, opsz 24, wght 400 | Icônes | Apache 2.0 |

- Les textes des licences sont dans `licenses/`.
- Aucune de ces polices n'a l'espace fine insécable (U+202F) : la typographie française utilise l'espace insécable U+00A0.
- Les icônes se dessinent par leur point de code : `MaterialSymbolsOutlined.codepoints` associe chaque nom (`menu_book`, `fact_check`…) à son point de code.

### Origine

Dépôts GitHub de Google, téléchargés le 2026-10-07 :
- `google/fonts` : `ofl/dmsans/DMSans[opsz,wght].ttf` et `DMSans-Italic[opsz,wght].ttf`, `ofl/manrope/Manrope[wght].ttf`, `ofl/ptmono/PTM55FT.ttf` (renommé `PTMono-Regular.ttf`), `ofl/instrumentserif/InstrumentSerif-Italic.ttf`, et le `OFL.txt` de chaque dossier.
- `google/material-design-icons` : `variablefont/MaterialSymbolsOutlined[FILL,GRAD,opsz,wght].ttf` et `.codepoints`, et `LICENSE`.

PT Mono et Instrument Serif sont déjà statiques. Les autres sont des polices variables, que ReportLab ne sait pas lire. Elles sont figées par `Scripts/tools/make_static_fonts.py`, qui attend les sources renommées `DMSans-VF.ttf`, `DMSans-Italic-VF.ttf`, `Manrope-VF.ttf` et `MaterialSymbolsOutlined-VF.ttf`. Pour une autre graisse, ajouter une ligne à `INSTANCES`.

## Ancienne DA

Montserrat, Lato et Amatic SC servent aux documents actuels, en attendant la refonte.
