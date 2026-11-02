# -*- coding: utf-8 -*-
"""Restructure memoire_fomi_stock.docx selon le canevas du professeur."""
import copy
import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "memoire_fomi_stock.docx")
OUT = os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")

doc = Document(SRC)
body = doc.element.body
sectPr = body.find(qn('w:sectPr'))
elems = [c for c in body.iterchildren() if c is not sectPr]


def text(el):
    return ''.join(t.text or '' for t in el.iter(qn('w:t'))).strip()


def style(el):
    pPr = el.find(qn('w:pPr'))
    if pPr is None:
        return ''
    ps = pPr.find(qn('w:pStyle'))
    return ps.get(qn('w:val')) if ps is not None else ''


def slice_els(a, b):
    return list(elems[a:b])


def detach(obj):
    el = obj._element if hasattr(obj, '_element') else obj
    body.remove(el)
    return el


def H1(t):
    return detach(doc.add_heading(t, level=1))


def H2(t):
    return detach(doc.add_heading(t, level=2))


def H3(t):
    return detach(doc.add_heading(t, level=3))


def P(t, bold=False, italic=False, size=None, align=None):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.font.name = 'Times New Roman'
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    if align:
        p.alignment = align
    return detach(p)


def BUL(t):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(18)
    p.paragraph_format.first_line_indent = Pt(-9)
    r = p.add_run('— ' + t)
    r.font.name = 'Times New Roman'
    return detach(p)


def PB():
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)
    return detach(p)


def TABLE(headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ''
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.name = 'Times New Roman'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sh = OxmlElement('w:shd')
        sh.set(qn('w:val'), 'clear')
        sh.set(qn('w:color'), 'auto')
        sh.set(qn('w:fill'), 'D9E2F3')
        c._tc.get_or_add_tcPr().append(sh)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = t.rows[ri + 1].cells[ci]
            c.text = ''
            p = c.paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(9)
            r.font.name = 'Times New Roman'
    return detach(t)


def rename(el, new_text):
    """Replace paragraph text, keeping the first run's formatting."""
    if el is None:
        return
    runs = el.findall('.//' + qn('w:r'))
    if not runs:
        return
    first = runs[0]
    for r in runs[1:]:
        r.getparent().remove(r)
    for t in first.findall(qn('w:t')):
        first.remove(t)
    t = OxmlElement('w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = new_text
    first.append(t)


def find_in(els, prefix):
    for el in els:
        if el.tag == qn('w:p') and text(el).startswith(prefix):
            return el
    return None


def rename_in(els, prefix, new_text):
    el = find_in(els, prefix)
    if el is not None:
        rename(el, new_text)
        return True
    return False


def set_style(el, sid):
    if el is None:
        return
    pPr = el.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        el.insert(0, pPr)
    ps = pPr.find(qn('w:pStyle'))
    if ps is None:
        ps = OxmlElement('w:pStyle')
        pPr.insert(0, ps)
    ps.set(qn('w:val'), sid)


def bold_normal(el):
    if el is None:
        return
    set_style(el, 'Normal')
    for r in el.findall('.//' + qn('w:r')):
        rPr = r.find(qn('w:rPr'))
        if rPr is None:
            rPr = OxmlElement('w:rPr')
            r.insert(0, rPr)
        if rPr.find(qn('w:b')) is None:
            rPr.append(OxmlElement('w:b'))


def add_toc_field():
    p = doc.add_paragraph()
    r1 = p.add_run(); x = OxmlElement('w:fldChar'); x.set(qn('w:fldCharType'), 'begin'); r1._r.append(x)
    r2 = p.add_run(); x = OxmlElement('w:instrText'); x.set(qn('xml:space'), 'preserve'); x.text = 'TOC \\o "1-3" \\h \\z \\u'; r2._r.append(x)
    r3 = p.add_run(); x = OxmlElement('w:fldChar'); x.set(qn('w:fldCharType'), 'separate'); r3._r.append(x)
    p.add_run("Table des matières — mettre à jour les champs (Ctrl+A puis F9)")
    r5 = p.add_run(); x = OxmlElement('w:fldChar'); x.set(qn('w:fldCharType'), 'end'); r5._r.append(x)
    return detach(p)


# ---------------- slices ----------------
cover = slice_els(0, 18)
ded = slice_els(18, 24)
rem = slice_els(24, 32)
resume = slice_els(32, 44)
toc_head = slice_els(44, 47)
toc_break = slice_els(67, 68)
ctx = slice_els(72, 113)
ch2_hist = slice_els(116, 120)
ch2_circuit = slice_els(121, 131)
ch2_defis = slice_els(132, 147)
etat_art = slice_els(156, 162)
prob_table = slice_els(167, 172)
cons = slice_els(175, 186)
obj = slice_els(187, 193)
ch4 = slice_els(204, 229)
ch5 = slice_els(230, 313)
ch6 = slice_els(314, 336)
ch7 = slice_els(340, 378)
ch8 = slice_els(379, 395)
ch9 = slice_els(399, 422)
biblio = slice_els(450, 481)
annexes = slice_els(482, len(elems))

# ---------------- renames ----------------
rename_in(ctx, '1.1 ', '1.1 Le contexte géographique et économique du Burundi')
rename_in(ctx, '1.2 ', '1.2 La fertilité des sols et l’usage des engrais')
rename_in(ctx, '1.3 ', '1.3 Le Programme National de Subvention des Engrais (PNSEB)')
rename_in(ctx, '1.4 ', '1.4 La réforme administrative de 2023')
rename_in(ctx, 'Tableau 1.3', 'Tableau 1 — Prix subventionnés des engrais FOMI')

hist_p1 = ch2_hist[1]
geo_p = ch2_hist[2]
mono_p = ch2_hist[3]

circuit_head = find_in(ch2_circuit, '2.2 ')
rename(circuit_head, 'Le circuit actuel de distribution des engrais')
bold_normal(circuit_head)

defis_head = find_in(ch2_defis, '2.4 ')
rename(defis_head, 'Les dysfonctionnements observés sur le terrain')
bold_normal(defis_head)

# Chapter III sections (reused chapters become sections of chapter III)
ch4_head = find_in(ch4, 'Chapitre 4')
rename(ch4_head, 'III.1 Analyse des besoins')
set_style(ch4_head, 'Heading2')
for i, label in [(1, 'Besoins fonctionnels'), (2, 'Règles métier'),
                 (3, 'Cas d’utilisation'), (4, 'Besoins non fonctionnels')]:
    el = find_in(ch4, '4.%d ' % i)
    rename(el, 'III.1.%d %s' % (i, label))
    set_style(el, 'Heading3')

ch5_head = find_in(ch5, 'Chapitre 5')
rename(ch5_head, 'III.2 Conception du système')
set_style(ch5_head, 'Heading2')
for i, label in [(1, 'Architecture logicielle'), (2, 'Modèle de données'),
                 (3, 'Diagrammes de séquence'), (4, 'Machine à états du ticket'),
                 (5, 'Algorithme FIFO'), (6, 'Sécurité et RBAC')]:
    el = find_in(ch5, '5.%d ' % i)
    rename(el, 'III.2.%d %s' % (i, label))
    set_style(el, 'Heading3')

ch7_head = find_in(ch7, 'Chapitre 7')
rename(ch7_head, 'III.3 Implémentation')
set_style(ch7_head, 'Heading2')
for i, label in [(1, 'Structure du projet'), (2, 'Gestion des stocks FIFO'),
                 (3, 'Système d’alertes'), (4, 'Workflow de validation des tickets'),
                 (5, 'Annulation des mouvements'), (6, 'Statistiques et tableaux de bord'),
                 (7, 'Piste d’audit')]:
    el = find_in(ch7, '7.%d ' % i)
    rename(el, 'III.3.%d %s' % (i, label))
    set_style(el, 'Heading3')

ch8_head = find_in(ch8, 'Chapitre 8')
rename(ch8_head, 'III.4 Tests et déploiement')
set_style(ch8_head, 'Heading2')
for i, label in [(1, 'Stratégie de test'), (2, 'Tests d’intégration'),
                 (3, 'Intégration et déploiement continus'), (4, 'Résultats')]:
    el = find_in(ch8, '8.%d ' % i)
    rename(el, 'III.4.%d %s' % (i, label))
    set_style(el, 'Heading3')

ch9_head = find_in(ch9, 'Chapitre 9')
rename(ch9_head, 'III.5 Évaluation des résultats')
set_style(ch9_head, 'Heading2')
for i, label in [(1, 'Conformité au cahier des charges'), (2, 'Performance'),
                 (3, 'Maintenabilité'), (4, 'Sécurité')]:
    el = find_in(ch9, '9.%d ' % i)
    rename(el, 'III.5.%d %s' % (i, label))
    set_style(el, 'Heading3')

# ---------------- build new order ----------------
order = []
order += cover
order += ded
order += rem
order += resume
order += toc_head
order += [add_toc_field()]
order += toc_break

# ================= INTRODUCTION GENERALE =================
order += [PB(), H1('INTRODUCTION GÉNÉRALE')]
order += [H2('1. Contexte et justification')]
order += ctx

order += [H2('2. Problématique')]
order += [H3('2.1 Problèmes identifiés et impacts')]
order += [P("L’analyse du fonctionnement actuel du système de gestion des stocks de FOMI a permis "
            "d’identifier onze problèmes majeurs, regroupés en quatre catégories : gestion des stocks, "
            "distribution, suivi et transparence, et gouvernance. Ces problèmes ont été recensés à "
            "travers les entretiens avec les responsables de FOMI, l’observation directe sur le terrain "
            "et l’analyse des documents de suivi existants (registres papier, tableurs Excel).")]
order += prob_table
order += [H3('2.2 Conséquences pour les parties prenantes')]
order += [P("Ces dysfonctionnements affectent directement les trois catégories d’acteurs du dispositif. "
            "Pour les agriculteurs, les ruptures de stock et les retards de distribution compromettent "
            "les calendriers culturaux et réduisent les rendements. Pour FOMI, l’absence de traçabilité "
            "engendre des pertes d’exploitation, des vols de lots et des difficultés de planification. "
            "Pour l’État et le PNSEB, le manque de visibilité en temps réel affaiblit le pilotage de la "
            "subvention et la confiance des bénéficiaires.")]
order += [P("En définitive, la conjugaison de ces problèmes montre que le dispositif actuel ne permet "
            "ni un pilotage fiable des stocks, ni une traçabilité effective des distributions. C’est "
            "ce constat qui justifie la conception d’un système d’information centralisé, sécurisé et "
            "auditable pour la gestion des stocks d’engrais de FOMI.")]

order += [H2('3. Objectifs')]
order += [H3('3.1 Objectif global')]
order += [P("L’objectif global de ce travail est de concevoir et de réaliser un système d’information "
            "centralisé pour la gestion des stocks d’engrais de la société FOMI, afin de garantir la "
            "disponibilité des intrants, la traçabilité des mouvements et la transparence de la "
            "distribution aux agriculteurs bénéficiaires du PNSEB.")]
order += [H3('3.2 Objectifs spécifiques')]
order += [P("De manière spécifique, ce travail vise à :")]
order += obj[2:]

order += [H2('4. Hypothèses de recherche')]
order += [P("Pour guider notre démarche, nous avons formulé les hypothèses suivantes :")]
for h in [
    "H1 : L’absence de suivi centralisé et en temps réel des stocks constitue la principale cause des ruptures et des retards de distribution.",
    "H2 : Un système fondé sur des rôles et sur une piste d’audit complète réduit significativement les risques de fraude et de détournement des intrants.",
    "H3 : Un algorithme FIFO associé à une gestion rigoureuse des lots améliore la rotation des stocks et limite les pertes par péremption.",
    "H4 : Un workflow de validation des tickets garantit le respect des quotas et des droits des agriculteurs bénéficiaires.",
    "H5 : Des alertes automatiques permettent une gestion proactive des ruptures, des stocks bas et des retards.",
    "H6 : Une architecture API REST découplée facilite l’intégration de clients web et mobiles ainsi que l’évolution du système.",
]:
    order += [BUL(h)]

order += [H2('5. Méthodologie de recherche')]
order += [P("La méthodologie adoptée combine une approche qualitative et une démarche d’ingénierie logicielle. "
            "La collecte des données s’est appuyée sur des entretiens semi-directifs avec les responsables de "
            "FOMI, sur l’observation directe du circuit de distribution et sur l’analyse documentaire des "
            "registres, tableurs et tickets utilisés sur le terrain. La modélisation a été réalisée avec UML "
            "et le développement a suivi un cycle de vie incrémental : analyse des besoins, conception, "
            "implémentation, tests et déploiement. La méthodologie est détaillée au chapitre II.")]

order += [H2('6. Intérêt du sujet')]
order += [P("Sur le plan scientifique, ce travail contribue à la réflexion sur la digitalisation de la chaîne "
            "d’approvisionnement en intrants agricoles dans les pays en développement, en proposant une "
            "architecture reproductible et documentée.")]
order += [P("Sur le plan pratique, il dote FOMI d’un outil centralisé de suivi des stocks et des distributions, "
            "réduisant les ruptures, les pertes et les risques de fraude, et facilitant la prise de décision.")]
order += [P("Sur le plan social, l’amélioration de la distribution des engrais contribue directement à la "
            "productivité agricole, à la sécurité alimentaire et au bien-être des ménages ruraux burundais.")]
order += [P("Sur le plan personnel, ce stage nous a permis de mettre en pratique les connaissances acquises en "
            "programmation, bases de données, génie logiciel, architecture et sécurité informatique.")]

order += [H2('7. Délimitation du sujet')]
order += [P("Délimitation spatiale : l’étude porte sur la société FOMI, son usine de Maramvya et son réseau de "
            "distribution (provinces, zones et collines) au Burundi.")]
order += [P("Délimitation temporelle : les travaux ont été menés durant l’année académique 2025-2026, sur la "
            "base des données de la campagne agricole en cours.")]
order += [P("Délimitation thématique : le travail couvre la gestion des stocks, les mouvements inter-dépôts, les "
            "tickets de distribution, les alertes et l’audit. Les aspects comptables, la paie, les ressources "
            "humaines et l’intégration des paiements mobiles ne sont pas traités.")]

order += [H2('8. Articulations du travail')]
order += [P("Outre l’introduction générale et la conclusion générale, ce rapport s’articule autour de trois "
            "chapitres. Le chapitre I présente le lieu de stage : historique, situation géographique, vision, "
            "missions, structure organisationnelle, déroulement du stage et étude de l’existant. Le chapitre II "
            "expose les concepts théoriques mobilisés et la méthodologie de l’étude. Le chapitre III présente "
            "les résultats : analyse des besoins, conception, implémentation, tests, déploiement et évaluation. "
            "Le rapport se termine par les critiques, suggestions et recommandations, puis la bibliographie et "
            "les annexes.")]

# ================= CHAPITRE I =================
order += [PB(), H1('CHAPITRE I : PRÉSENTATION DU LIEU DE STAGE')]
order += [H2('I.1 Introduction')]
order += [P("Le présent chapitre présente le cadre institutionnel de notre stage de fin d’études effectué au "
            "sein de la société FOMI — Fertilisants Organo-Minéraux Industries. Il retrace l’historique de "
            "l’entreprise, sa situation géographique, sa vision, ses missions et ses objectifs, sa structure "
            "organisationnelle, avant de décrire le déroulement du stage, les activités réalisées, l’étude de "
            "l’existant et la corrélation entre les activités du stage et les éléments constitutifs des unités "
            "d’enseignement suivies au cours de notre formation.")]
order += [H2('I.2 Historique de l’institution')]
order += [hist_p1, mono_p]
order += [H2('I.3 Situation géographique')]
order += [geo_p]
order += [P("L’implantation de l’usine à Maramvya s’explique par la proximité des axes de communication, du lac "
            "Tanganyika et de l’aéroport international Melchior Ndadaye. Cette localisation facilite à la fois "
            "l’importation des matières premières minérales complémentaires et l’acheminement des produits finis "
            "vers les dépôts provinciaux et zonaux du pays.")]
order += [H2('I.4 Vision, missions et objectifs de l’institution')]
order += [P("FOMI a pour vision de devenir le leader de la production et de la distribution des engrais "
            "organo-minéraux dans la région des Grands Lacs, en garantissant aux agriculteurs burundais un accès "
            "permanent à des intrants de qualité, à un prix abordable et en quantité suffisante.")]
order += [P("Ses missions consistent notamment à produire localement des engrais organo-minéraux, à sécuriser "
            "l’approvisionnement du PNSEB, à assurer la qualité et la traçabilité des produits, à réduire la "
            "dépendance du pays aux importations d’engrais et à contribuer à la sécurité alimentaire nationale.")]
order += [P("Les objectifs poursuivis sont l’amélioration des rendements agricoles, la réduction des pertes, la "
            "professionnalisation du circuit de distribution, la digitalisation de la gestion des stocks et le "
            "renforcement de la transparence dans l’attribution des intrants subventionnés.")]
order += [P("Le tableau ci-dessous présente les principaux produits commercialisés par FOMI.")]
order += [TABLE(
    ['Produit', 'Formule', 'Conditionnement', 'Usage principal'],
    [['FOMI-IMBURA', 'NPK 9-22-4', '25 kg', 'Céréales et cultures de base'],
     ['FOMI-BAGARA', 'NK 11-0-22', '25 kg', 'Tubercules et bananiers'],
     ['FOMI-TOTAHAZA', 'NK 21-0-8', '25 kg', 'Maraîchage et céréales'],
     ['Chaux agricole', 'Amendement calcique', '50 kg', 'Correction de l’acidité des sols']])]
order += [P('Tableau I.1 — Produits FOMI', italic=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)]

order += [H2('I.5 Structure organisationnelle')]
order += [P("FOMI est organisée autour d’une direction générale qui coordonne plusieurs directions et services "
            "complémentaires. La direction commerciale joue un rôle central dans la planification des ventes, la "
            "gestion des commandes et la relation avec les bénéficiaires du PNSEB. La direction de production "
            "assure la fabrication des engrais, tandis que le service qualité contrôle la conformité des lots. "
            "Le service logistique et distribution organise l’acheminement des produits de l’usine vers les "
            "dépôts provinciaux, zonaux et collinaires. Les services financier, des ressources humaines et "
            "informatique apportent leur appui transversal.")]
order += [TABLE(
    ['Direction / Service', 'Rôle principal'],
    [['Direction générale', 'Pilotage stratégique et représentation de l’entreprise'],
     ['Direction commerciale', 'Ventes, commandes, relation avec le PNSEB et les bénéficiaires'],
     ['Direction de production', 'Fabrication des engrais et gestion des matières premières'],
     ['Service qualité', 'Contrôle de conformité des lots et des produits finis'],
     ['Service logistique et distribution', 'Acheminement et gestion des dépôts'],
     ['Service financier', 'Trésorerie, facturation et suivi des subventions'],
     ['Service des ressources humaines', 'Gestion du personnel et formation'],
     ['Service informatique', 'Systèmes d’information et sécurité']])]
order += [P('Tableau I.2 — Structure organisationnelle simplifiée', italic=True, size=9,
            align=WD_ALIGN_PARAGRAPH.CENTER)]

order += [H2('I.6 Déroulement du stage')]
order += [H3('I.6.1 Introduction')]
order += [P("Notre stage s’est déroulé au sein de la Direction Commerciale de FOMI. Encadrés par le Directeur "
            "Commercial, nous avons participé à l’analyse du circuit de distribution, à la collecte des besoins "
            "des utilisateurs et à la conception d’un système informatisé de gestion des stocks d’engrais. Le "
            "stage a alterné des périodes d’observation sur le terrain et des phases de travail technique au "
            "bureau.")]
order += [H3('I.6.2 Activités réalisées')]
for a in [
    "Immersion dans l’entreprise et entretiens avec le Directeur Commercial et les agents de distribution ;",
    "Observation du circuit de distribution, de l’usine de Maramvya jusqu’aux points de distribution collinaires ;",
    "Analyse des documents existants : registres papier, tableurs Excel, tickets de distribution et rapports ;",
    "Rédaction du cahier des charges : besoins fonctionnels et non fonctionnels, règles métier et cas d’utilisation ;",
    "Modélisation UML : cas d’utilisation, classes, séquences, activités, machine à états et déploiement ;",
    "Développement de l’API REST avec Java 21 et Spring Boot 3.3.5 ;",
    "Conception du modèle de données PostgreSQL et des migrations Flyway ;",
    "Mise en place de la sécurité JWT, du contrôle d’accès par rôles et de la piste d’audit ;",
    "Écriture et exécution des tests d’intégration avec Testcontainers et JUnit 5 ;",
    "Développement de deux clients prototypes : une application web React et une application mobile Expo/React Native ;",
    "Documentation de l’API avec Swagger/OpenAPI et mise en place du pipeline d’intégration continue.",
]:
    order += [BUL(a)]

order += [H3('I.6.3 Étude de l’existant')]
order += [P("L’étude de l’existant a consisté à décrire le fonctionnement actuel de la gestion des stocks et de "
            "la distribution, puis à en dégager les limites et à proposer une solution adaptée.")]
order += [H3('I.6.3.1 Description du système existant')]
order += [P("Avant la mise en place du système proposé, la gestion des stocks et des distributions reposait "
            "essentiellement sur des registres papier et des tableurs Excel décentralisés. Les mouvements "
            "étaient enregistrés manuellement par les agents, puis consolidés au niveau central avec des délais "
            "importants.")]
order += ch2_circuit
order += ch2_defis
order += [H3('I.6.3.2 Critique de l’existant')]
order += [P("La critique du système existant met en évidence plusieurs limites structurelles : absence de "
            "visibilité en temps réel, multiplication des supports, risques d’erreurs et de pertes "
            "d’information, difficulté d’audit et de contrôle des quotas. Les conséquences pour les parties "
            "prenantes sont détaillées ci-après.")]
order += cons[1:]
order += [H3('I.6.3.3 Solution proposée')]
order += [P("La solution proposée est un système d’information centralisé composé de trois briques "
            "complémentaires : une API REST sécurisée qui porte la logique métier et la persistance, une "
            "application web destinée aux administrateurs et superviseurs, et une application mobile destinée "
            "aux agents de terrain. L’API couvre la gestion des référentiels (engrais, géographie, dépôts, "
            "agriculteurs), les réceptions et transferts de stock, la distribution FIFO, les tickets et leur "
            "workflow de validation, les alertes automatiques, les statistiques et la piste d’audit.")]
order += [P("Le système retenu repose sur une architecture en couches, une base de données PostgreSQL, des "
            "migrations versionnées avec Flyway, une authentification JWT et un contrôle d’accès basé sur les "
            "rôles (RBAC). Il intègre également une documentation Swagger et une suite de tests d’intégration.")]

order += [H3('I.6.4 Corrélation du stage avec les Éléments Constitutifs des Unités d’Enseignement')]
order += [P("Le tableau ci-dessous met en relation les activités réalisées durant le stage avec les éléments "
            "constitutifs des unités d’enseignement (ECU) suivies au cours de notre formation.")]
order += [TABLE(
    ['Élément constitutif d’UE', 'Contenu mobilisé', 'Application dans le stage'],
    [['Programmation orientée objet', 'Classes, objets, encapsulation, héritage, polymorphisme', 'Développement de l’API en Java'],
     ['Bases de données', 'Modèle relationnel, normalisation, SQL, transactions', 'Modèle PostgreSQL, migrations Flyway'],
     ['Génie logiciel', 'Cycle de vie, UML, analyse des besoins, tests', 'Cahier des charges, diagrammes, tests'],
     ['Architecture logicielle', 'Architecture en couches, API REST, design patterns', 'Architecture trois tiers de l’API'],
     ['Sécurité informatique', 'Authentification, autorisation, hachage, JWT', 'Sécurité de l’API et RBAC'],
     ['Réseaux et systèmes distribués', 'Protocoles HTTP, services web, client-serveur', 'API REST et clients web/mobile'],
     ['Méthodologie de recherche', 'Entretiens, observation, analyse documentaire', 'Collecte des besoins sur le terrain'],
     ['Gestion de projet', 'Planification, suivi, gestion des versions', 'Organisation du travail et Git/GitHub']])]
order += [P('Tableau I.3 — Corrélation stage / ECU', italic=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)]

# ================= CHAPITRE II =================
order += [PB(), H1('CHAPITRE II : CONCEPTS THÉORIQUES ET MÉTHODOLOGIE DE L’ÉTUDE')]
order += [P("Ce chapitre présente les concepts théoriques sur lesquels repose notre travail ainsi que la "
            "méthodologie adoptée pour mener l’étude. Les concepts couvrent la gestion des stocks, la "
            "traçabilité, l’architecture logicielle, la sécurité et les technologies utilisées. La méthodologie "
            "précise la démarche, les phases du projet, les outils et les modalités de validation.")]
order += [H2('II.1 Concepts théoriques')]
order += [H3('II.1.1 Gestion des stocks et méthode FIFO')]
order += [P("La gestion des stocks consiste à suivre en permanence les quantités disponibles par produit, par "
            "dépôt et par lot, afin de garantir la disponibilité des intrants et d’éviter aussi bien les "
            "ruptures que les surstocks. La méthode FIFO (First-In, First-Out) consiste à consommer en priorité "
            "les lots les plus anciens. Dans le cas des engrais, dont la durée de conservation est limitée, ce "
            "principe doit être combiné à un contrôle de la date de péremption afin de distribuer d’abord les "
            "lots les plus proches de leur date limite. Le système retenu applique ce principe lors des sorties "
            "de stock et enregistre chaque décrément sous forme de mouvement traçable.")]
order += [H3('II.1.2 Traçabilité et piste d’audit')]
order += [P("La traçabilité est la capacité à reconstituer, pour chaque lot et chaque ticket, l’ensemble des "
            "opérations effectuées, leur auteur et leur date. Elle repose sur une piste d’audit (audit trail) "
            "qui enregistre les actions critiques dans une table dédiée : création, validation, distribution, "
            "annulation et modification des référentiels. Une piste d’audit fiable est indispensable dans un "
            "dispositif subventionné, car elle permet de contrôler les quotas, de détecter les anomalies et de "
            "répondre aux demandes des autorités de tutelle.")]
order += [H3('II.1.3 Architecture logicielle en couches')]
order += [P("L’architecture en couches sépare les responsabilités en plusieurs niveaux : présentation "
            "(contrôleurs REST), sécurité (filtres d’authentification et d’autorisation), métier (services), "
            "persistance (repositories et entités JPA) et stockage (base de données). Cette séparation facilite "
            "les tests, la maintenance et l’évolution du système. Elle est complétée par une architecture trois "
            "tiers dans laquelle les clients web et mobile consomment l’API, qui s’appuie elle-même sur une base "
            "PostgreSQL.")]
order += [H3('II.1.4 Sécurité : authentification JWT et contrôle d’accès par rôles')]
order += [P("L’authentification vérifie l’identité de l’utilisateur, tandis que l’autorisation détermine les "
            "actions qu’il peut effectuer. Le système retenu utilise des jetons JWT signés avec l’algorithme "
            "HMAC-SHA256 pour une authentification sans état, et un contrôle d’accès basé sur les rôles (RBAC) "
            "pour restreindre les opérations selon le profil : administrateur, superviseur, agent de zone, agent "
            "de colline et agent logistique. Les mots de passe sont hachés avec BCrypt et les échanges sont "
            "protégés par HTTPS en production.")]
order += [H3('II.1.5 Technologies et outils utilisés')]
for el in ch6[2:]:
    if el.tag == qn('w:p') and style(el) == 'Heading2':
        set_style(el, 'Normal')
        for r in el.findall('.//' + qn('w:r')):
            rPr = r.find(qn('w:rPr'))
            if rPr is None:
                rPr = OxmlElement('w:rPr')
                r.insert(0, rPr)
            if rPr.find(qn('w:b')) is None:
                rPr.append(OxmlElement('w:b'))
order += ch6[2:]
order += [H3('II.1.6 État de l’art : systèmes de référence en Afrique de l’Est')]
order += etat_art[1:]

order += [H2('II.2 Méthodologie de l’étude')]
order += [H3('II.2.1 Démarche méthodologique')]
order += [P("Nous avons adopté une démarche qualitative et participative articulée autour de quatre axes : "
            "l’analyse documentaire, les entretiens semi-directifs, l’observation directe et la modélisation. "
            "L’analyse documentaire a porté sur les rapports internes, les registres de stock, les tableurs et "
            "les tickets. Les entretiens ont été menés auprès du Directeur Commercial et des agents de "
            "distribution afin de comprendre les besoins réels et les difficultés opérationnelles. "
            "L’observation directe nous a permis de suivre le circuit des engrais et d’identifier les goulets "
            "d’étranglement. Enfin, la modélisation UML a servi de support de communication entre les besoins "
            "exprimés et la solution technique.")]
order += [H3('II.2.2 Phases du projet')]
for ph in [
    "Phase 1 — Analyse de l’existant : compréhension du circuit, des acteurs et des documents ;",
    "Phase 2 — Analyse des besoins : identification des besoins fonctionnels et non fonctionnels, des règles métier et des cas d’utilisation ;",
    "Phase 3 — Conception : architecture, modèle de données, diagrammes UML et choix technologiques ;",
    "Phase 4 — Implémentation : développement de l’API, des clients web et mobile, de la sécurité et de l’audit ;",
    "Phase 5 — Tests : tests d’intégration, tests de sécurité et validation fonctionnelle ;",
    "Phase 6 — Déploiement et documentation : conteneurisation, déploiement, documentation Swagger et rédaction du rapport.",
]:
    order += [BUL(ph)]
order += [H3('II.2.3 Outils de développement et de validation')]
order += [P("Les principaux outils utilisés sont : Java 21, Spring Boot 3.3.5, Maven, PostgreSQL 16, Flyway, "
            "Spring Security et JJWT, Spring Data JPA/Hibernate, SpringDoc OpenAPI, JUnit 5, Testcontainers, "
            "Git et GitHub, Docker, Railway, React/Vite et Expo/React Native pour les clients, ainsi que "
            "Swagger UI et Postman pour la validation des endpoints.")]
order += [H3('II.2.4 Méthode de validation des résultats')]
order += [P("La validation repose sur plusieurs niveaux : la revue du cahier des charges avec le maître de "
            "stage, la vérification de la conformité des endpoints aux besoins, l’exécution des tests "
            "d’intégration sur une base PostgreSQL réelle via Testcontainers, les tests de sécurité RBAC et "
            "l’intégration continue avec GitHub Actions. Les résultats sont présentés au chapitre III.")]

# ================= CHAPITRE III =================
order += [PB(), H1('CHAPITRE III : PRÉSENTATION DES RÉSULTATS')]
order += [P("Ce chapitre présente les résultats du travail : l’analyse des besoins, la conception du système, "
            "l’implémentation, les tests et le déploiement, l’évaluation des résultats ainsi que les clients "
            "web et mobile développés.")]
order += ch4
order += ch5
order += ch7
order += ch8
order += ch9

order += [H2('III.6 Clients web et mobile')]
order += [P("Deux clients ont été développés pour consommer l’API. L’application web, développée avec React et "
            "Vite, comporte douze pages couvrant le tableau de bord, les dépôts, les tickets, les distributions, "
            "les agriculteurs, les mouvements, les lots, les alertes, les utilisateurs, les journaux d’audit et "
            "le suivi public des tickets. Elle est configurée comme une application web progressive (PWA) et "
            "déployée via GitHub Pages.")]
order += [P("L’application mobile, développée avec Expo et React Native, comporte treize écrans et reprend les "
            "principales fonctionnalités de terrain : tableau de bord, tickets, stocks, alertes, agriculteurs, "
            "distributions, mouvements, lots, utilisateurs, audit et suivi public. Elle utilise React Navigation "
            "et AsyncStorage pour la session.")]
order += [P("Ces deux clients constituent des prototypes fonctionnels : ils illustrent l’intégration de l’API "
            "mais ne bénéficient pas encore de tests automatisés et présentent quelques écarts de contrat avec "
            "certains endpoints. Les tests présentés dans ce mémoire portent donc exclusivement sur l’API.")]

# ================= CONCLUSION =================
order += [PB(), H1('CONCLUSION GÉNÉRALE')]
order += [P("Ce travail avait pour objectif de concevoir et de réaliser un système d’information centralisé pour "
            "la gestion des stocks d’engrais de la société FOMI au Burundi. Partant du constat d’une gestion "
            "manuelle, dispersée et peu traçable, nous avons analysé l’existant, formalisé les besoins et conçu "
            "une solution logicielle complète.")]
order += [P("Les résultats obtenus sont les suivants : une API REST documentée exposant soixante endpoints, "
            "couvrant les référentiels, les réceptions, les transferts, la distribution FIFO, les tickets et "
            "leur workflow, les alertes, les statistiques, les exports CSV et la piste d’audit ; un modèle de "
            "données relationnel de seize tables géré par onze migrations Flyway ; un mécanisme de sécurité "
            "JWT avec cinq rôles et un hachage BCrypt ; un système d’alertes automatiques ; et une suite de "
            "deux cent sept tests automatisés, dont deux cent quatre tests d’intégration sur PostgreSQL réel "
            "et trois tests unitaires.")]
order += [P("Sur le plan technique, le système repose sur Java 21, Spring Boot 3.3.5, PostgreSQL 16, Flyway, "
            "Spring Security, Spring Data JPA, SpringDoc OpenAPI et Testcontainers. Deux clients prototypes, "
            "l’un web (React) et l’autre mobile (Expo/React Native), ont également été développés pour "
            "illustrer l’utilisation de l’API.")]
order += [P("Les hypothèses de recherche sont globalement confirmées : la centralisation des données, la "
            "traçabilité des mouvements, le contrôle d’accès par rôles et les alertes automatiques apportent "
            "une réponse pertinente aux dysfonctionnements observés. Le travail comporte néanmoins des limites, "
            "notamment l’absence de notifications SMS, de paiement mobile, de mode hors-ligne et de tests "
            "automatisés pour les clients. Ces limites ouvrent la voie à plusieurs perspectives d’amélioration "
            "présentées ci-après.")]

# ================= CRITIQUES / SUGGESTIONS / RECOMMANDATIONS =================
order += [PB(), H1('CRITIQUES, SUGGESTIONS ET RECOMMANDATIONS')]
order += [H2('1. Critiques')]
order += [P("Malgré les résultats obtenus, plusieurs critiques peuvent être formulées à l’égard du système et de "
            "sa mise en œuvre.")]
order += [P('1.1 Critiques techniques', bold=True)]
for c in [
    "L’algorithme FIFO est ordonné par date de réception FOMI et non par date de péremption ; de plus, le chemin avec lot imposé ne vérifie pas la péremption.",
    "L’annulation d’une distribution ne restaure pas le stock du dépôt, ce qui peut entraîner un écart entre le stock physique et le stock logique.",
    "La règle RBAC relative à l’annulation des mouvements est contournée par l’ordre des règles de sécurité, permettant à tout utilisateur authentifié de l’appeler.",
    "L’alerte INACTIVITE peut être créée sans type d’engrais, alors que le schéma impose une contrainte NOT NULL.",
    "L’expiration automatique des tickets existe dans le code mais n’est reliée à aucune tâche planifiée ni à aucun endpoint.",
    "Les clients web et mobile présentent des écarts de contrat avec l’API (champs obligatoires manquants, endpoints inexistants) et ne disposent pas de tests automatisés.",
]:
    order += [BUL(c)]
order += [P('1.2 Critiques organisationnelles', bold=True)]
for c in [
    "La qualité des données historiques est variable, ce qui limite la comparaison avant/après.",
    "La couverture réseau et l’équipement informatique des agents de terrain restent insuffisants dans certaines zones.",
    "L’appropriation du système par les agents nécessite une formation et un accompagnement dans la durée.",
]:
    order += [BUL(c)]

order += [H2('2. Suggestions')]
order += [P("Pour améliorer le système, nous suggérons de :")]
for s in [
    "Corriger l’ordonnancement FIFO pour retenir la date de péremption et contrôler systématiquement la péremption, y compris pour les lots imposés.",
    "Restaurer le stock lors de l’annulation d’une distribution et recalculer correctement le statut du ticket.",
    "Réordonner les règles de sécurité afin que l’annulation des mouvements soit réservée aux profils autorisés.",
    "Rendre le type d’engrais facultatif dans la table des alertes ou adapter la contrainte pour les alertes d’inactivité.",
    "Planifier l’expiration automatique des tickets et ajouter les tests correspondants.",
    "Aligner les contrats des clients web et mobile sur l’API et ajouter des tests de non-régression.",
    "Compléter la couverture de tests unitaires et mettre en place un rapport de couverture.",
]:
    order += [BUL(s)]

order += [H2('3. Recommandations')]
order += [P("À l’endroit de FOMI, nous recommandons un déploiement progressif du système, la désignation d’un "
            "administrateur fonctionnel, la formation des agents, la mise en place de sauvegardes automatiques "
            "et l’instauration d’indicateurs de suivi (taux de service, ruptures, péremptions).")]
order += [P("À l’endroit des autorités publiques et du PNSEB, nous recommandons l’intégration du système au "
            "circuit officiel de distribution, la sécurisation des données et des accès, ainsi que la "
            "généralisation progressive à l’ensemble des provinces.")]
order += [P("Pour les travaux futurs, plusieurs perspectives sont envisageables : notifications SMS, intégration "
            "du paiement mobile (Lumicash, EcoCash), mode hors-ligne avec synchronisation, tableaux de bord en "
            "temps réel (WebSocket), et modèles prédictifs d’estimation de la demande.")]

# ================= BIBLIO / ANNEXES =================
order += [PB()]
order += biblio
order += [PB()]
order += annexes

# ---------------- rebuild body ----------------
for child in list(body.iterchildren()):
    if child is not sectPr:
        body.remove(child)
for el in order:
    sectPr.addprevious(el)

# update fields on open
settings = doc.settings.element
for old in settings.findall(qn('w:updateFields')):
    settings.remove(old)
uf = OxmlElement('w:updateFields')
uf.set(qn('w:val'), 'true')
settings.append(uf)

doc.save(OUT)
print('saved', OUT)
print('elements', len(order))
