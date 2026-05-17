from reportlab.lib.units import cm

from ...config import PDFStyle
from ...templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig


def create_synthese_v2_page(c):
    layout = PageLayout(c, "Synthèse", config=LayoutConfig(part_title="7. SYNTHÈSE"))

    layout.add_question_block(
        "Si vous aviez plus d'argent, qu'est-ce que cela changerait vraiment pour vous ?",
        "v2_synth_1",
        config=QuestionConfig(box_height=4 * cm),
    )
    layout.add_question_block(
        "Qu'est-ce qui vous fait le plus peur dans le manque d'argent ? Et qu'est-ce qui pourrait vous mettre mal à l'aise dans le fait de gagner davantage ?",
        "v2_synth_2",
        config=QuestionConfig(box_height=4 * cm),
    )
    layout.add_question_block(
        "À partir de quoi vous sentez-vous « assez » en sécurité ? Est-ce que cet « assez » correspond à un chiffre concret, ou plutôt à une sensation intérieure difficile à atteindre ?",
        "v2_synth_3",
        config=QuestionConfig(box_height=4 * cm),
    )
    layout.render()
