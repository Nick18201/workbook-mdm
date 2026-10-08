# Audit des carnets · octobre 2026

Audit pédagogique et ergonomique des carnets 0 à 6, du livret de compétences et du livret projet « Mon business plan ». Il est daté du 8 octobre 2026 et porte sur le commit `0bda048` de `main`. Il identifie les manques et ce qui rend la complétion difficile pour la personne accompagnée, qui remplit seule entre deux séances.

## Contenu du dossier

| Fichier | Contenu |
|---|---|
| `synthese.html` | La synthèse complète, à ouvrir dans un navigateur : l'essentiel, 8 constats transversaux, charge de travail, fil rouge, un verdict par document, conditions de remplissage, architecture, plan par lots, décisions. Les 9 rapports détaillés y sont repris en fin de page. |
| `rapports/00-chap0.md` … `06-chap6.md` | Un rapport par carnet. |
| `rapports/07-livret.md` | Le livret de compétences. |
| `rapports/08-business_plan.md` | Le livret projet « Mon business plan », avec une section sur l'exactitude réglementaire. |
| `methode/grille.md` | La grille d'audit commune (9 axes, charte de ton, protocole de sécurité émotionnelle, priorités). |
| `methode/transversal-technique.md` | Les constats techniques sur les champs de formulaire et l'architecture des deux chaînes. |

Chaque rapport suit la même structure : synthèse, exercice par exercice, charge émotionnelle, fil rouge, écart avec l'app web, recommandations classées P1 / P2 / P3 (correction rapide ou refonte). Les références `fichier:ligne` renvoient à `Scripts/workbook_generator/chapters/`.

## L'essentiel

1. **Aucun filet de sécurité.** Aucun document ne permet de laisser une question vierge, de reporter ce qui est trop lourd ou d'écrire une phrase d'ancrage. Le cadre (confidentialité, droit de passer) n'est posé nulle part.
2. **Une charge de travail au-dessus de la promesse.** Les estimations donnent 21 à 27 h pour les carnets et le livret, contre 10 à 20 h annoncées dans le programme. Il faut compter 15 à 17 h de plus pour le business plan. Une seule durée est affichée, celle du carnet 5, et elle est sous-estimée de moitié.
3. **Un fil rouge promis, pas tenu.** Les carnets ne se citent presque jamais. Des données sont saisies plusieurs fois (les 3 valeurs, le type MBTI®). Trois carnets promettent d'« évaluer chaque piste », et rien ne le permet.
4. **Des questions ouvertes sans appui.** Aucun exemple contrasté dans les carnets. Les irritants ne deviennent jamais des critères. La compétence n'est jamais croisée avec l'énergie.
5. **Deux chaînes devenues deux programmes.** L'app web propose un autre parcours que les PDF. La synthèse recommande une source unique.

## À noter

- Les durées sont estimées exercice par exercice, ce ne sont pas des mesures. La saisie n'a pas été testée dans de vrais logiciels PDF.
- La formule « Ce qui m'a surpris » impose un genre : le participe s'accorde avec « m' ». Elle a été remplacée par « Ce qui m'étonne » dans tous les rapports.
- Le livret de compétences contient 28 exemples qui décrivent un seul profil très précis. Il faut vérifier qu'ils ne viennent pas d'un dossier réel.
