# -*- coding: utf-8 -*-
"""Corrige l'incoherence sur le nombre de niveaux de stockage : FOMI dispose
de TROIS niveaux de stockage fixes et permanents (usine, provincial, zonal).
Le niveau collinaire n'est PAS un depot : c'est une livraison ephemere.
"""
from docx import Document

DOC = 'Rapport_stage_FOMI_canevas.docx'
d = Document(DOC)


def rewrite(par, text):
    runs = par.runs
    if not runs:
        par.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ''


n = 0
for p in d.paragraphs:
    t = p.text

    # 1) "quatre niveaux de stockage fixes" -> trois niveaux fixes
    if 'implique une chaîne d’approvisionnement en quatre niveaux de stockage fixes' in t:
        rewrite(p,
                'La distribution des engrais FOMI suit un circuit logistique et administratif '
                'hiérarchisé, depuis l’usine de Maramvya jusqu’aux agriculteurs bénéficiaires '
                '(Figure I.1). Ce circuit, restructuré en conformité avec l’organisation '
                'territoriale du pays, repose sur trois niveaux de stockage fixes et permanents, '
                'complétés par une distribution finale organisée au niveau de chaque colline.')
        n += 1

    # 2) Le niveau 4 ne doit pas etre presente comme un depot
    elif t.startswith('Niveau 4 : Les points de distribution de colline'):
        rewrite(p,
                'Distribution finale : les points de distribution de colline (livraison éphémère)')
        n += 1

    # 3) la suite du niveau 4 : preciser l'absence de depot
    elif t.startswith('À ce stade, la logistique lourde s\'arrête.'):
        rewrite(p,
                'À ce stade, la logistique lourde s’arrête : il ne s’agit pas d’un dépôt mais '
                'd’une opération de distribution ponctuelle. Sous la coordination de '
                'l’administration locale et des comités collinaires, les engrais sont transférés '
                'depuis le dépôt de zone vers les collines de destination. Faute d’infrastructures '
                'de stockage permanentes, des sites communautaires éphémères (hangars, églises, '
                'écoles) sont réquisitionnés uniquement le jour de la distribution pour décharger '
                'temporairement les volumes (20 à 100 tonnes) et servir immédiatement les '
                'producteurs.')
        n += 1

    # 4) Chapitre II : etat de l'art mentionne "quatre niveaux de stockage fixes"
    elif 'articulée autour de quatre niveaux de stockage fixes' in t:
        rewrite(p, t.replace(
            'une architecture logistique articulée autour de quatre niveaux de stockage fixes',
            'une architecture logistique articulée autour de trois niveaux de stockage fixes '
            'et d’une distribution finale au niveau collinaire'))
        n += 1

d.save(DOC)
print('paragraphes corriges :', n)
