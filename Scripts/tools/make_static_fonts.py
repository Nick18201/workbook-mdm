"""Produit les TTF statiques de la DA « Éditorial & Affirmé » à partir des polices variables de Google.

ReportLab ne lit pas les polices variables : chaque graisse utilisée est figée une fois avec
fontTools, qui n'est pas une dépendance du projet (`pip install fonttools` le temps de la commande).
Les fichiers sources à télécharger et leurs licences sont listés dans assets/fonts/README.md.

Usage : python Scripts/tools/make_static_fonts.py <dossier_des_sources> assets/fonts
"""
import os
import sys
import time

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

src, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)

# (fichier source, coordonnées, famille, style, nom PostScript, fichier de sortie)
INSTANCES = [
    ("DMSans-VF.ttf", {"wght": 700, "opsz": 18}, "DM Sans", "Bold", "DMSans-Bold", "DMSans-Bold.ttf"),
    ("DMSans-VF.ttf", {"wght": 800, "opsz": 40}, "DM Sans", "ExtraBold", "DMSans-ExtraBold", "DMSans-ExtraBold.ttf"),
    ("DMSans-Italic-VF.ttf", {"wght": 400, "opsz": 18}, "DM Sans", "Italic", "DMSans-Italic", "DMSans-Italic.ttf"),
    ("Manrope-VF.ttf", {"wght": 400}, "Manrope", "Regular", "Manrope-Regular", "Manrope-Regular.ttf"),
    ("Manrope-VF.ttf", {"wght": 600}, "Manrope", "SemiBold", "Manrope-SemiBold", "Manrope-SemiBold.ttf"),
    ("Manrope-VF.ttf", {"wght": 800}, "Manrope", "ExtraBold", "Manrope-ExtraBold", "Manrope-ExtraBold.ttf"),
    (
        "MaterialSymbolsOutlined-VF.ttf",
        {"FILL": 0, "GRAD": 0, "opsz": 24, "wght": 400},
        "Material Symbols Outlined",
        "Regular",
        "MaterialSymbolsOutlined-Regular",
        "MaterialSymbolsOutlined.ttf",
    ),
]


def set_names(font, family, style, ps_name):
    name = font["name"]
    full = f"{family} {style}"
    for rec in list(name.names):
        if rec.nameID in (16, 17, 25) or rec.nameID >= 256:
            name.removeNames(nameID=rec.nameID)
    for name_id, value in ((1, family), (2, style), (3, f"{ps_name};static"), (4, full), (6, ps_name)):
        name.setName(value, name_id, 3, 1, 0x409)
        name.setName(value, name_id, 1, 0, 0)


for src_file, coords, family, style, ps_name, out_file in INSTANCES:
    t0 = time.time()
    font = TTFont(os.path.join(src, src_file))
    static = instancer.instantiateVariableFont(font, coords)
    for table in ("STAT", "MVAR", "HVAR", "avar", "fvar", "gvar", "cvar"):
        if table in static:
            del static[table]
    set_names(static, family, style, ps_name)
    path = os.path.join(out, out_file)
    static.save(path)
    print(f"{out_file}: {os.path.getsize(path)} octets ({time.time() - t0:.1f} s)")
