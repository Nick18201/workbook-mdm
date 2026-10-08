# Volet transversal : technique et architecture (notes)

## Champs (forms.py, tous carnets)
- 316 champs texte sur 8 documents ; tous en `doNotScroll`, 296 en police automatique (fontSize 0). Les autres : 11 pt fixe (champs une ligne hauts, chap5/chap6).
- Effet : la police rapetisse à mesure qu'on écrit (Acrobat), puis la saisie se bloque (doNotScroll). Ailleurs, le comportement varie. Une longue réponse devient illisible à l'impression.
- Aucun champ sans drapeau Imprimer (bien). Apparences générées par ReportLab, pas de NeedAppearances, DA `/Helv 0 Tf` : la saisie s'affiche en Helvetica, pas dans la police du carnet.
- Ordre de tabulation : pas de clé /Tabs ; sauts d'ordre visibles : chap5 (8), chap6 (1).
- Champs trop bas pour l'écriture manuscrite (≤ 1 ligne à 8 mm) : chap1 p8 (4 champs de 31 pt), chap2 p9 frise (5 × 38 pt) + p11 arbre, chap4 p7 (4 × 43 pt) + p12, chap5 p8 (choix difficiles, 6+ champs de 37 pt) — 32 champs au total.
- Page livrable : une zone « notes » de 476 × 345-377 pt (~2 700 caractères tapés) à la fin de chaque carnet ; chap1 p3 météo : 450 × 377 pt.
- Pas de /Lang fr dans le catalogue (lecteurs d'écran en voix anglaise). Titre du PDF chap0 incohérent (« chapitre 0 : Le prélude », sans la marque).
- Infobulles présentes sur quasi tous les champs (7 manquent : chap0 2, chap2 5).
- Test réel dans la visionneuse Chromium du navigateur intégré : impossible (clics non transmis dans le cadre PDF).

## Architecture (predefined_workbooks.py vs chapters/)
- Les carnets CLI sont déjà quasi déclaratifs : ~170 appels de blocs PageLayout (add_paragraphs 44, add_question_block 34, add_questions_group 23, add_text 14, add_heading 13, add_fields_card 12…) et quelques pages dessinées (frise et arbre de vie chap2, pages concept, couverture).
- Le web ne connaît que 8 types de blocs (callout, cards_grid, scale, checklist, table, stat_boxes, question, text) et 10 gabarits ; 12 blocs utilisés par les carnets n'existent pas côté web (heading, paragraphs, fields_card, annotation, link_card, numbered_lines, info_cards, frise, checklist_cards, rating_grid, star_list, page_break).
- La copie web diverge déjà sur le fond (ex. chap0 web : bienvenue, trois règles, objectif ; CLI : engagement, faire le point, domaines de vie, entourage).

## Business plan (ajout)
- 273 champs texte (112 multilignes, 161 d'une ligne), tous en `doNotScroll`, 258 en police automatique ; 19 trop bas pour l'écriture manuscrite (p. 20 prix, p. 33 feuille de route…) ; 3 sauts d'ordre de tabulation.
- Total des neuf documents : 589 champs texte, 51 trop bas pour l'écriture manuscrite.
