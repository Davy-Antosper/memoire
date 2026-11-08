# -*- coding: utf-8 -*-
"""Restaure les proportions natives de chaque figure.

Les images etaient affichees avec des largeur/hauteur fixees a la main, ce qui
deformait celles dont le ratio differait. On recalcule la taille d'affichage
en respectant le ratio du PNG, borne par la largeur utile et une hauteur max.
"""
import io
import zipfile

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Cm
from PIL import Image

DOC = 'Rapport_stage_FOMI_canevas.docx'

MAX_W = 15.0   # cm : largeur utile (A4 21 - 3.0 - 2.5 = 15.5), marge de securite
MAX_H = 20.0   # cm : hauteur max pour laisser la place a la legende

d = Document(DOC)
z = zipfile.ZipFile(DOC)

print('%-13s %-11s %-9s -> %-9s %s' % ('media', 'pixels', 'avant', 'apres', 'legende'))


def txt(el):
    return ''.join(t.text or '' for t in el.iter(qn('w:t'))).strip()


kids = list(d.element.body.iterchildren())
fixed = 0

for i, el in enumerate(kids):
    if el.tag != qn('w:p') or not el.findall('.//' + qn('w:drawing')):
        continue

    cap = ''
    for nxt in kids[i + 1:i + 3]:
        t = txt(nxt)
        if t:
            cap = t[:40]
            break

    blip = el.findall('.//' + qn('a:blip'))[0]
    name = d.part.rels[blip.get(qn('r:embed'))].target_ref.split('/')[-1]
    im = Image.open(io.BytesIO(z.read('word/media/' + name)))
    ratio = im.width / im.height

    aspect = el.findall('.//' + qn('wp:extent'))[0].get('cx')
    cx_old = int(aspect) / 360000.0
    cy_old = int(el.findall('.//' + qn('wp:extent'))[0].get('cy')) / 360000.0

    # taille cible : le plus grand rectangle de ratio natif tenant dans la boite
    w = min(MAX_W, MAX_H * ratio)
    h = w / ratio

    # mettre a jour wp:extent ET a:ext (les deux doivent rester coherents)
    for ext in el.findall('.//' + qn('wp:extent')):
        ext.set('cx', str(int(w * 360000)))
        ext.set('cy', str(int(h * 360000)))
    for ext in el.findall('.//' + qn('a:ext')):
        ext.set('cx', str(int(w * 360000)))
        ext.set('cy', str(int(h * 360000)))

    fixed += 1
    print('%-13s %-11s %-9s -> %-9s %s' % (
        name, '%dx%d' % im.size, '%.1fx%.1f' % (cx_old, cy_old),
        '%.1fx%.1f' % (w, h), cap))

d.save(DOC)
print('\n%d figures remises aux bonnes proportions' % fixed)
