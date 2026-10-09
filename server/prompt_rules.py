"""
The rules that guided the reference carnets, written for Gemini: one source for every
prompt (creation from notes, faithful layout of a support, customization, retouching).
Each section names the document it comes from; a rule added to the carnets is added here
too, and tests/test_prompts.py checks that each prompt carries the sections it needs, and
no other (a faithful layout gets the forbidden words, not the whole tone, which would have
it rewrite the support).

Sources: DA-workbook.md (section 7, tone), audit-carnets-2026-10/carte-parcours-unifie.md
(sections 3, 4 and 8), audit-carnets-2026-10/feuille-de-route-restructuration.md (sections 5
and 6: the conventions of each carnet), the field policy (PR #67, #68) and the safety
protocol of heavy questions (James Pennebaker's line).
"""

import json

from workbook_generator.spec import load_workbook

# --- Tone and vocabulary (DA-workbook.md, section 7; feuille de route, section 6) -----

# The forbidden words, also the only wording a faithful layout changes (FIDELITY_RULES)
VOCABULARY_RULES = """MOTS PROSCRITS (charte, section 7) :
- Le registre du développement personnel : « quête de sens », « retrouver votre élan », « espace d'écoute bienveillant », « croyances limitantes », « syndrome de l'imposteur », ennéagramme, « lâcher prise », « épanouissement ».
- Le métier : jamais « coach » ni « coaching ». Dire « consultant en transformation », « la personne qui vous accompagne » ou « la personne référente ». Jamais « cabinet » pour parler de Marge de Manœuvre. « Binôme » jamais d'une façon qui laisse croire que deux personnes sont en séance.
- Tout l'accompagnement se fait à distance : jamais « présentiel ».
- Le test du bilan s'appelle « test des fonctionnements cognitifs » : jamais « MBTI » ni type en quatre lettres (ISFJ…).
- Le tutoiement : toujours le vouvoiement.
- Le papier : tout se fait à l'écran. Jamais « imprimez », « sur papier », « apportez ce carnet » : la personne remplit son carnet chez elle et le renvoie complété avant la séance, où on le travaille ensemble.
Un mot cité entre guillemets (un message reçu, une parole rapportée : « épanouissement », « Si tu ne connaissais pas mon métier… ») n'est pas concerné.
"""

TONE_RULES = """TON ET VOCABULAIRE (charte de Marge de Manœuvre, pour TOUS les textes du document) :
- Vouvoiement. Un ton parlé, chaleureux et sérieux à la fois, qui donne de l'énergie : le plaisir de l'introspection, la clarté, le pouvoir d'agir sur sa vie. Phrases courtes, affirmatives et concrètes, tournées vers la décision et l'action.
- Une personne capable d'agir, jamais une personne fragile : aucune formule de précaution ou de soupçon (« prenez-le à votre rythme », « cela peut remuer », « trop lourd », « vos vrais doutes », « des domaines qui pèsent les uns sur les autres »). Un bilan n'est ni une thérapie ni une psychanalyse.
- Lexique à privilégier : action, décision, projet, livrable, marché, faisabilité, salaire, rythme de vie, arbitrage, « validé en séance », prise de conscience, héritages, pouvoir d'agir.
- N'invente aucun chiffre, témoignage, partenariat ni adresse web ; aucune statistique sans source ; aucun montant, salaire ni règle fiscale écrits en dur (renvoyer à la source officielle, ou « à voir en séance »).
- Formules non genrées : les amorces en « je » n'ont ni participe ni adjectif qui s'accorde avec la personne. Écrire « Ce qui m'étonne » (pas « Ce qui m'a surpris »), « ce qui m'a fait agir ainsi » (pas « ce qui m'a poussé »), « votre clientèle » (pas « vos clients »). Les exemples prennent des métiers au nom épicène (juriste, ergonome, géomètre).
- Titres de page : une affirmation ponctuée, en minuscules sauf la première lettre et les noms propres, terminée par un point, un « ? » ou un « ! » (« Votre situation actuelle. »). Le dernier mot s'affiche en corail ; pour un autre groupe de mots, l'entourer d'astérisques (« Mon rapport *à l'argent.* »). Un titre dont le premier mot finit par une apostrophe se marque en entier (« *L'exploration.* »). 25 à 45 caractères.
- Typographie française : guillemets « », espace avant : ; ! ?, « œ » (cœur, manœuvre). Aucun émoji ni pictogramme (la police du PDF ne les affiche pas).
""" + VOCABULARY_RULES

# --- The common template of a carnet (carte, section 4; feuille de route, section 5) ---

TEMPLATE_RULES = """LE GABARIT COMMUN DE NOS CARNETS (carte du parcours, section 4) — tout document créé le suit, dans cet ordre :
1. Couverture ('cover') : le titre du document et sa promesse (3 à 8 mots, ce que le document apporte).
2. Ouverture ('summary') : son titre de page (« Préparer *l'échange.* »), le but en deux ou trois phrases ('intro_text'), puis la liste de ce que contient le document, un élément par ligne avec sa durée ('points') : « Météo · 2 min », « Exercice 1 · Nom court · 15 min », …, « Fin de carnet · 5 min ». 'duration' donne la durée d'écriture totale (« 1 h 15 ») : la somme des lignes. 'split' conseille un découpage en une phrase (« En deux fois : les exercices 1 et 2, puis la suite. »).
3. Météo de l'énergie, seulement si elle est demandée : une page 'composite' titrée « Avant de *commencer.* », sourcil « Météo · 2 min », avec le seul bloc {"type": "energy", "field_prefix": "<préfixe>_meteo"} (ses textes sont fixes).
4. Les exercices : une page 'composite' par exercice (deux pages pour un exercice long, coupées par un 'page_break'). Sourcil ('part_title') « Exercice N · nom court · durée » (« Exercice 2 · Vos contraintes · 15 min » ; « Exercice 3 · Nom · facultatif · 10 min » pour un exercice facultatif). La page s'ouvre sur une phrase qui dit à quoi sert l'exercice (bloc 'paragraphs').
5. Fin ('engagement'), titre « Votre livrable. », sourcil « Fin de carnet · 5 min » : 'livrable_title' (ce que le document produit, nommé), 'livrable_text' (une ou deux phrases : ce qu'il contient et ce qu'on en fait en séance), 'lines' (deux à quatre engagements concrets, en « je »), 'zones' : toujours ces trois-là, la deuxième précisée pour ce document : « Ce qui m'étonne en relisant mes réponses », « À aborder en séance : … », « Ce que j'ai laissé vierge, à reprendre ensemble ». 'field_prefix' : « <préfixe>_livrable ».
6. Dos ('closing') : 'messages', deux ou trois phrases courtes (90 caractères au plus) : la prochaine étape (« Prochaine étape : la séance 6. Renvoyez ce carnet complété d'ici là. »).
"""

# --- The exercises (carte, section 4; feuille de route, sections 5 and 6) -------------

# The room on a page (the measures of our carnets), also for a faithful layout
SPACE_RULES = """- La place (mesures de nos carnets) : une page d'exercice offre environ 23 cm sous son titre. Comptez 1 cm par ligne de consigne, 5 cm pour l'exemple contrasté, 3,7 cm pour une question et sa case d'une phrase (5 cm pour un paragraphe), 2,7 cm par rangée de 'fields_card' à deux cases d'une phrase côte à côte, 4 cm pour une 'rating_grid' d'une ligne. Un exercice qui dépasse une page se coupe entre deux blocs par un 'page_break', en deux pages à peu près égales : jamais une page « (suite) » qui ne porte qu'une case. Pour gagner de la place, mettez deux cases d'une phrase côte à côte dans une 'fields_card'.
"""

EXERCISE_RULES = """LES EXERCICES (conventions de nos carnets) :
- Des formats variés, choisis pour ce qu'on demande : des questions ('question', 'questions_group'), des informations courtes côte à côte ('fields_card'), un choix exclusif en mots ('rating_grid' d'une ligne, suivie d'une case « Parce que… »), une échelle ('scale'), un tableau qui croise des données ('table' : une colonne par donnée, une ligne par critère), une liste à cocher ('checklist'), des étapes ou des questions à garder sous les yeux ('star_list'), un modèle de message ('callout').
- Une case, une information. Une question qui demande deux choses a deux cases (« Le scénario vers lequel je penche » · « Pourquoi lui ») ; une donnée et sa source vont dans deux cases côte à côte ; le lieu, le trajet, le télétravail prennent chacun une case d'une ligne, sous un titre de carte.
- Des amorces en « je », précises et actives : « Ce que je veux garder… », « Pour me lancer, je commence par… », « Les 5 mots que je veux associer au travail aujourd'hui » (pas « Cinq mots pour mon futur travail »).
- Un exemple contrasté par exercice qui demande une réponse rédigée : le bloc 'contrast_example', placé après la consigne et avant les cases. 'title' : un métier voisin de celui de la personne, jamais le sien (elle le recopierait), au nom épicène, le même au féminin (ergonome, juriste, géomètre, céramiste ; jamais « luthier », « conducteur de travaux », « statisticien »), différent à chaque exercice. L'exemple, sa situation, oui ; ses faits, non : il peut vivre la même situation que la personne (une reconversion, une évolution, une rupture), mais il raconte les faits du métier voisin, ni son parcours, ni son projet, ni les mots de ses notes (son « atelier », sa « fermeture du site »), qu'elle recopierait aussi. 'surface' : la réponse vague (« C'était intéressant. »). 'exploitable' : la réponse concrète, utilisable en séance, sans montant ni pourcentage (ni salaire, ni « 32 k€ », ni « 60 % » : un ordre de grandeur se voit en séance). Pas d'exemple sur un exercice de tri, un test ou une auto-évaluation (une notation, une échelle) : il orienterait la réponse. Un exemple de plus peut aller dans 'example' d'une question (90 caractères au plus, sans préfixe « Ex : »).
- Les irritants se retournent en critères : « Ce qui m'agace dans mon poste » → « donc mon prochain poste devra… ».
- Les cases restent vides : jamais de réponse, d'objectif ni d'action préremplis. Une feuille de route se fait avec un 'table' (une ligne par palier), jamais avec le gabarit 'roadmap'.
- Pas de tableau sans case à remplir : chaque cellule à remplir est une case {"field_id": …, "placeholder": …}.
- Questions courtes (120 caractères au plus), consignes en une ou deux phrases.
""" + SPACE_RULES

# --- Heavy questions: James Pennebaker's line, with a safety net ----------------------

CHARGE_RULES = """LES QUESTIONS FRANCHES (un bilan, pas une thérapie : retours de Nicolas sur le carnet 1, 9 octobre 2026) :
- Les questions franches sont posées (« Ma plus grande peur face à ce changement », « Ce que je n'ai jamais osé dire à mon manager ») : un bilan sert à décider, il nomme les contraintes et les doutes.
- Le droit de passer une question est dit une seule fois, dans l'ouverture de chaque carnet (texte fixe). Ne le répète jamais dans un exercice : ni « facultatif », ni « laissez la case vierge », ni « si vous le souhaitez ».
- Un exercice qui touche à l'intime (famille, argent personnel, peurs, échecs, conflits, épuisement) s'ouvre sur une annonce : un bloc {"type": "protocol", "text": "Cet exercice parle de … : ce que vous en tirez sert à …"}, une phrase factuelle qui dit de quoi il parle et à quoi il sert pour le bilan, sans formule de précaution. Il se clôt sur la phrase d'ancrage, tournée vers le présent : un bloc {"type": "anchor", "field_id": "<préfixe>_ancrage"} (« Aujourd'hui, avec le recul, je sais que… », texte fixe).
"""

# --- The boxes (field policy, PR #67 and #68; feuille de route, section 5) ----------

ANSWER_RULES = """LES CASES (les réponses se tapent en 11 pt, et une case pleine défile sans barre : sa taille vient de la réponse attendue) :
- Chaque question, case de 'fields_card', 'table' ou 'cards_grid' dit la réponse qu'elle attend : 'word' (un prénom, une date, un montant, un nombre, l'intitulé d'un métier : une ligne), 'sentence' (ce qui commence par « ce que », « pourquoi », « comment », une situation, une condition : 150 caractères), 'paragraph' (400 caractères), 'long' (un récit, 800 caractères).
- 'question' et 'questions_group' : 'answer' sur chaque question. 'fields_card' : chaque case est [libellé, field_id, réponse], plusieurs cases côte à côte forment une rangée ; "question_labels": true pour des libellés en phrases. 'table' : 'answer' pour tout le tableau, et chaque case {"field_id": …, "placeholder": "Ligne : colonne", "answer": "word"} si elle attend autre chose ; la première colonne nomme la ligne, en texte.
- Le libellé d'une ligne de 'rating_grid' tient en 30 caractères, les bornes d'une 'scale' en 20 : au-delà, le PDF les coupe. Quatre valeurs de 'rating_grid' au plus, d'une douzaine de caractères chacune.
- Identifiants de champs uniques dans tout le document, en minuscules avec des tirets bas, commençant par un préfixe court du document (« enq_metier », « enq_contrat »).
"""

# --- The blocks Gemini may create (templates.py, BlockSpec) -------------------------

BLOCKS_DOC = """LES BLOCS D'UNE PAGE 'composite' (clé "blocks", dans l'ordre de lecture ; le moteur pagine seul et ajoute une page « (suite) » si un exercice déborde) :
- 'paragraphs' : {"type": "paragraphs", "items": ["Une phrase qui dit à quoi sert l'exercice."]} ; un élément qui commence par « • » devient une puce.
- 'heading' : {"type": "heading", "text": "Un intertitre"}
- 'star_list' : {"type": "star_list", "items": ["« Racontez-moi une semaine ordinaire. »", "« Comment y entre-t-on aujourd'hui ? »"]}
- 'question' : {"type": "question", "question": "Ce que je veux garder de mon poste actuel", "subtitle": "Une aide d'une ligne (facultatif)", "example": "Un exemple court (facultatif)", "field_id": "doc_garder", "answer": "sentence"}
- 'questions_group' : plusieurs questions qui se suivent, à mettre en dernier sur la page : {"type": "questions_group", "questions": [{"question": "…", "field_id": "doc_q1", "answer": "sentence"}, {"question": "…", "field_id": "doc_q2", "answer": "paragraph"}]}
- 'fields_card' : {"type": "fields_card", "title": "Entretien 1", "hint": "Une aide (facultatif)", "question_labels": true, "rows": [[["La personne", "doc_personne", "word"], ["Son métier", "doc_metier", "word"]], [["Ce qui confirme ce que je pensais", "doc_confirme", "sentence"], ["Ce qui contredit, ou m'étonne", "doc_contredit", "sentence"]]]}
- 'rating_grid' : {"type": "rating_grid", "title": "Face à mes critères", "items": [["Mon minimum est atteint", "doc_minimum"]], "values": ["Oui", "À terme", "Non", "À vérifier"]}
- 'scale' : {"type": "scale", "label": "Mon intérêt pour ce métier :", "min_val": 0, "max_val": 10, "min_label": "Aucun", "max_label": "Très fort", "field_id": "doc_interet"}
- 'table' : {"type": "table", "headers": ["", "Piste 1", "Piste 2"], "rows": [["Ce qui m'attire", {"field_id": "doc_p1_attire", "placeholder": "Piste 1 : ce qui m'attire"}, {"field_id": "doc_p2_attire", "placeholder": "Piste 2 : ce qui m'attire"}]], "answer": "sentence"}
- 'checklist' : {"type": "checklist", "title": "Ce que j'ai déjà", "items": ["Un CV à jour", "Un contact dans le métier"], "field_prefix": "doc_deja"}
- 'cards_grid' : {"type": "cards_grid", "columns": 2, "cards": [{"title": "Ce qui m'attire", "subtitle": "Dans ce métier, aujourd'hui"}, {"title": "Ce qui me freine", "subtitle": "Ce que je dois vérifier"}], "answer": "sentence", "field_prefix": "doc_attire"}
- 'callout' : {"type": "callout", "title": "Pour demander", "text": "« Je réfléchis à une évolution vers votre métier. Accepteriez-vous un échange d'une vingtaine de minutes ? »", "variant": "info"}
- 'link_card' : {"type": "link_card", "title": "Où chercher", "links": [["Nom de la ressource", "https://…", "ce qu'on y trouve (adresse courte)."]]} ; seulement des adresses données dans les notes.
- 'contrast_example' : {"type": "contrast_example", "title": "Ergonome", "surface": "C'était intéressant.", "exploitable": "Elle confirme les horaires connus à l'avance. La suite : rencontrer sa collègue."}
- 'protocol' : {"type": "protocol", "text": "Cette page parle de … ."} ; 'anchor' : {"type": "anchor", "field_id": "doc_ancrage"} ; 'energy' : {"type": "energy", "field_prefix": "doc_meteo"} (leurs autres textes sont fixes).
- 'annotation' : {"type": "annotation", "text": "Une note manuscrite courte."} : au plus une par document, dans un blanc.
- 'page_break' : {"type": "page_break"}, pour couper un long exercice en deux pages équilibrées.
Ne crée jamais toi-même : 'report' (il reporte une donnée d'un autre carnet), 'life_line', 'tree_of_life', 'frise', 'info_cards', 'numbered_lines', 'checklist_cards', 'fill_in_card', 'stat_boxes' (des chiffres sans source), 'text' (préférer 'paragraphs'), ni les gabarits de page 'meteo', 'quadrants', 'two_columns', 'enquete', 'roadmap', 'questions' et 'recap' : une page 'composite' fait mieux.
"""

# --- Existing blocks of the reference workbooks (customization, retouching) -----------

REFERENCE_BLOCKS_RULES = """BLOCS DÉJÀ PRÉSENTS DANS LE DOCUMENT :
- Garde le type de chaque bloc, ses clés, l'ordre de ses éléments, tous ses identifiants ('field_id', 'field_prefix', identifiants dans les listes) et la taille de ses cases ('answer', ou 'word', 'sentence'… dans une liste ; 'answer' d'une cellule de tableau {"field_id": …, "answer": "word"}) ; adapte seulement ses textes, sans les allonger.
- Ne modifie jamais les blocs 'protocol' (annonce d'un exercice qui touche à l'intime), 'anchor' (phrase d'ancrage qui le clôt), 'energy' (météo du jour) et 'report' (report d'une donnée écrite dans un autre carnet) : ils font partie du cadre, des annonces et des renvois entre carnets. Garde les clés 'data_id', 'fixed' et 'part' là où elles sont. Dans un 'contrast_example', tu peux réécrire 'title', 'surface' et 'exploitable', avec un exemple tiré d'un métier voisin de celui du bénéficiaire, jamais de son propre métier, au nom épicène, un métier différent à chaque exemple. Sa situation, oui ; ses faits, non : l'exemple peut vivre la même situation (une reconversion, une évolution), mais il raconte les faits du métier voisin (ni son parcours, ni son projet, ni les mots de son profil).
- Les libellés gardent leur longueur : une ligne de 'rating_grid' tient en 30 caractères, une borne d'échelle en 20 ; au-delà, le PDF les coupe.
- Dans une page 'summary', garde 'duration' et 'split' ; dans une page 'engagement', garde 'zones' et 'pistes'.
"""

# --- Customization (carte, section 8) ---------------------------------------------

PERSONALIZATION_RULES = """CE QUE LA PERSONNALISATION CHANGE (carte du parcours, section 8 ; niveaux relevés le 9 octobre 2026) :
- S'adaptent : les exemples, les consignes, sous-titres et questions pour qu'ils parlent de sa situation, le vocabulaire de son secteur, les intitulés de pistes, les ressources de son secteur.
- Les exemples : sa situation, oui ; ses faits, non. Un exemple peut vivre la même situation qu'elle (une reconversion, une évolution interne, un retour à l'emploi, son statut), mais il raconte les faits d'un métier voisin : ni son métier, ni son projet, ni son foyer, ni ses chiffres, ni les mots de son profil. Elle recopierait les siens.
- Ne changent jamais : ce qui porte "fixed": true, le cadre, les annonces des exercices qui touchent à l'intime, la météo, les reports et les renvois entre carnets, les définitions, les textes réglementaires, les identifiants et la taille des cases.
- Deux niveaux, selon le carnet ('carnet' en tête du document) :
  * moyen, carnets 1, 3 et 5 : tous les exemples réécrits ; la consigne et le sous-titre de chaque exercice prennent le vocabulaire de son secteur et nomment sa situation ; chaque question garde son sens, avec au plus une précision tirée de sa situation (« dans votre métier de… ») ; au carnet 3, ne touche jamais les questions du test des fonctionnements cognitifs, la restitution en serait faussée ;
  * fort, carnets 2, 4, 6 et 7, carnet de route et ses modules, business plan : le niveau moyen, et chaque page parle d'elle : consignes, sous-titres, amorces et questions tournés vers sa situation et son secteur, sans changer ce que la question demande ; pistes pré-intitulées ; ressources et interlocuteurs de son secteur nommés, sans adresse web inventée ; au carnet 4, son statut (salarié, indépendant, demandeur d'emploi), jamais un chiffre personnel.
- Ne préremplis jamais une case : la personne écrit ses réponses. N'ajoute ni ne retire de page, de bloc ou de question, sauf si le consultant le demande.
"""

# --- A faithful layout of a finished support (choices of 9 October 2026) --------------

FIDELITY_RULES = """MISE EN PAGE FIDÈLE D'UN SUPPORT DÉJÀ ÉCRIT :
- Le support est fini : tu le mets en page dans nos carnets, tu ne le réécris pas. Chaque titre, consigne, question, libellé à compléter et option est repris, dans l'ordre du support, mot pour mot.
- Ne changent que :
  * la typographie française : guillemets « », apostrophes, espaces, « œ » ; un texte écrit tout en capitales passe en minuscules, sauf la première lettre, les sigles et les noms propres ; un titre de page finit par un point (« Comprendre la réalité du métier. ») ;
  * les mots proscrits (liste ci-dessous), remplacés au plus près (« présentiel » → « sur place », « coach » → « la personne qui vous accompagne »), et le tutoiement, passé au vouvoiement ;
  * la taille des cases : 'answer' selon la réponse attendue (règles des cases ci-dessous).
- Ce qui n'est pas du contenu disparaît : les en-têtes et pieds de page répétés (logo, « marge de manœuvre »), les numéros de page.
- Un élément du support, un bloc :
  * une question suivie d'une case → 'question', ou 'questions_group' pour plusieurs questions qui se suivent ;
  * un libellé à compléter (« Date : », « Métier exploré : ») → une case de 'fields_card', deux libellés courts côte à côte par rangée ; sans les deux-points ;
  * une question ou un libellé suivi d'options (une par ligne, ou après des cases ☐) → 'checklist' : son 'title' est la question, ses 'items' les options, dans l'ordre ;
  * une suite de nombres (1 2 3 … 10) sous une question → 'scale' de ces bornes, la question en 'label' ;
  * un tableau → 'table', chaque cellule à remplir étant une case ;
  * une consigne → 'paragraphs' ; une liste de conseils → 'star_list'.
- Une page du document par page ou par section du support : son titre devient le titre de la page ('title'), son surtitre éventuel le sourcil ('part_title', tel quel ; "" s'il n'y en a pas). Une section trop longue pour une page se coupe par un 'page_break', en deux pages équilibrées (la place, ci-dessous).
- N'ajoute rien : ni exemple contrasté, ni protocole, ni météo, ni durée, ni page d'ouverture ou de livrable, ni question, ni consigne de ton cru. N'en retire rien, ne fusionne pas deux questions, n'en reformule aucune.
- Ce qui rapprocherait le support de nos carnets va dans 'suggestions', une consigne par ajout, rédigée pour que le consultant l'applique telle quelle avec « Ajuster » : un exemple contrasté tiré d'un métier voisin, une annonce avant un exercice qui touche à l'intime, une durée par page, une page d'ouverture, une page de livrable, une formule genrée à tourner autrement (« Ajoute un exemple contrasté à la page 3, tiré d'un métier voisin. »).
"""


def _example_page():
    """An exercise page of carnet 7 as it is in our files: the model Gemini follows."""
    spec = load_workbook("carnet-7")
    page = next(p for p in spec.pages if (p.part_title or "").startswith("Exercice 6"))
    data = page.model_dump(exclude_unset=True, exclude_none=True)
    data.pop("part", None)
    for block in data.get("blocks") or []:
        block.pop("data_id", None)
    return json.dumps(data, ensure_ascii=False)


EXAMPLE_PAGE = f"""UNE PAGE D'EXERCICE DE NOS CARNETS (carnet 7, exercice 6, telle qu'elle est dans nos fichiers) :
{_example_page()}
"""
