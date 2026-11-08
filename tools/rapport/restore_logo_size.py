# -*- coding: utf-8 -*-
"""Restaure le logo de la page de garde a sa taille d'origine (image1).
Seules les figures numerotees doivent etre redimensionnees."""
import zipfile

from docx import Document
from docx.oxml.ns import qn

DOC = 'Rapport_stage_FOMI_canevas.docx'
d = Document(DOC)
z = zipfile.ZipFile(DOC)

# taille d'origine mesuree avant le redimensionnement : 6.88 x 3.87 cm
ORIG = {'image1.png': (6.88, 3.87)}

kids = list(d.element.body.iterchildren())
for el in kids:
    if el.tag != qn('w:p') or not el.findall('.//' + qn('w:drawing')):
        continue
    blip = el.findall('.//' + qn('a:blip'))[0]
    name = d.part.rels[blip.get(qn('r:embed'))].target_ref.split('/')[-1]
    if name not in ORIG:
        continue
    w, h = ORIG[name]
    for ext in el.findall('.//' + qn('wp:extent')):
        ext.set('cx', str(int(w * 360000)))
        ext.set('cy', str(int(h * 360000)))
    for ext in el.findall('.//' + qn('a:ext')):
        ext.set('cx', str(int(w * 360000)))
        ext.set('cy', str(int(h * 360000)))
    print('%s restaure a %.2f x %.2f cm' % (name, w, h))

d.save(DOC)
print('ok')
