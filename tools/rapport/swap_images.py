# -*- coding: utf-8 -*-
"""Remplace les images du rapport par les PNG fraichement telecharges.

Les images sont stockees dans word/media/imageN.png. On identifie, pour chaque
InlineShape, le fichier media correspondant via sa relation, puis on remplace
le contenu binaire par le nouveau PNG en conservant le nom de media.
"""
import os
import re
import shutil
import zipfile

from docx import Document
from docx.oxml.ns import qn

DOC = 'Rapport_stage_FOMI_canevas.docx'
ASSETS = 'memoire_assets'

# --- ordre d'apparition des figures dans le document -> fichier PNG
# 1 image de couverture (logo) + 8 figures
MAPPING = [
    None,                          # image 1 : logo de la page de garde (inchange)
    'distribution_circuit.png',    # Figure I.1
    'use_case_diagram.png',        # Figure III.1
    'activity_diagram.png',        # Figure III.2
    'architecture.png',            # Figure III.3
    'er_diagram.png',              # Figure III.4
    'class_diagram.png',           # Figure III.5
    'deployment_diagram.png',      # Figure III.6
    'sequence_ticket.png',         # Figure III.7
]

d = Document(DOC)
part = d.part

# --- retrouver, dans l'ordre, les noms de media utilises par les inlines
media_names = []
for shape in d.inline_shapes:
    blip = shape._inline.graphic.graphicData.pic.blipFill.blip
    rid = blip.get(qn('r:embed'))
    target = part.rels[rid].target_ref      # ex. 'media/image1.png'
    media_names.append(os.path.basename(target))
print('images trouvees dans l\'ordre :', media_names)

if len(media_names) != len(MAPPING):
    raise SystemExit('nombre d\'images inattendu : %d (attendu %d)' % (len(media_names), len(MAPPING)))

# --- preparer les remplacements dans le zip
tmp = DOC + '.tmp'
with zipfile.ZipFile(DOC) as zin:
    names = zin.namelist()
    blobs = {n: zin.read(n) for n in names}

replaced = []
for name, png in zip(media_names, MAPPING):
    if png is None:
        continue
    src = os.path.join(ASSETS, png)
    if not os.path.exists(src):
        print('  ! absent :', src)
        continue
    new_bytes = open(src, 'rb').read()
    key = 'word/media/' + name
    old = len(blobs[key])
    blobs[key] = new_bytes
    replaced.append((name, png, old, len(new_bytes)))

with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for n in names:
        zout.writestr(n, blobs[n])
shutil.move(tmp, DOC)

print('\nimages remplacees :')
for name, png, old, new in replaced:
    print('  %-14s <- %-26s %7.1f -> %7.1f Ko' % (name, png, old / 1024, new / 1024))
print('\n%d remplacements' % len(replaced))
