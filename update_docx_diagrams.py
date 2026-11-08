# -*- coding: utf-8 -*-
"""Remplace les figures du rapport par les versions régénérées.

Les PNG de `memoire_assets/` sont produits à partir des sources PlantUML de
`memoire_assets/puml_src/`. Ce script réinjecte ces PNG dans le rapport et
réajuste la taille d'affichage pour conserver les proportions (largeur max
15 cm, hauteur max 20 cm).

Usage :
    python update_docx_diagrams.py
"""
import os
import struct
import sys

from docx import Document
from docx.shared import Cm, Emu

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")
ASSETS = os.path.join(HERE, "memoire_assets")

# Les figures du rapport sont stockées dans cet ordre par python-docx.
MAPPING = {
    "image2.png": "distribution_circuit.png",
    "image3.png": "use_case_diagram.png",
    "image4.png": "activity_diagram.png",
    "image5.png": "architecture.png",
    "image6.png": "er_diagram.png",
    "image7.png": "class_diagram.png",
    "image8.png": "deployment_diagram.png",
    "image9.png": "sequence_ticket.png",
}

MAX_WIDTH = Cm(15)
MAX_HEIGHT = Cm(20)


def png_size(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("ce n'est pas un PNG")
    return struct.unpack(">II", data[16:24])


def main():
    doc = Document(DOC)
    remplaces = 0

    for shape in doc.inline_shapes:
        rid = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
        part = doc.part.related_parts[rid]
        name = os.path.basename(str(part.partname))
        asset = MAPPING.get(name)
        if not asset:
            continue

        path = os.path.join(ASSETS, asset)
        with open(path, "rb") as fh:
            data = fh.read()
        width_px, height_px = png_size(data)
        aspect = width_px / height_px

        # Remplace le binaire de l'image dans le paquet .docx.
        part._blob = data

        # Conserve les proportions : largeur 15 cm, hauteur plafonnée à 20 cm.
        width = MAX_WIDTH
        height = Emu(int(width / aspect))
        if height > MAX_HEIGHT:
            height = MAX_HEIGHT
            width = Emu(int(height * aspect))
        shape.width = width
        shape.height = height

        print(f"  ok  {asset} -> {name} ({width_px}x{height_px}, "
              f"{width.cm:.1f} x {height.cm:.1f} cm)")
        remplaces += 1

    doc.save(DOC)
    print(f"\nFigures remplacées : {remplaces}")
    print(f"Rapport enregistré : {DOC}")
    if remplaces != len(MAPPING):
        print("ATTENTION : toutes les figures n'ont pas été trouvées.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
