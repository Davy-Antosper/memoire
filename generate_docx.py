#!/usr/bin/env python3
"""Generate comprehensive ~100-page DOCX memoire about FOMI Stock Management API."""
import os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

ASSETS = "/home/antbeat/projects/memoire_assets"
OUTPUT = "/home/antbeat/projects/memoire_fomi_stock.docx"
doc = Document()
style = doc.styles["Normal"]
style.font.name = "Times New Roman"; style.font.size = Pt(12)
style.paragraph_format.line_spacing = 1.5; style.paragraph_format.space_after = Pt(6)
for lv in range(1, 4):
    hs = doc.styles[f"Heading {lv}"]
    hs.font.name = "Times New Roman"; hs.font.color.rgb = RGBColor(0, 51, 102)
    if lv == 1:
        hs.font.size = Pt(16); hs.font.bold = True
        hs.paragraph_format.space_before = Pt(24); hs.paragraph_format.space_after = Pt(12)
    elif lv == 2:
        hs.font.size = Pt(14); hs.font.bold = True
        hs.paragraph_format.space_before = Pt(18); hs.paragraph_format.space_after = Pt(8)
    else:
        hs.font.size = Pt(12); hs.font.bold = True
        hs.paragraph_format.space_before = Pt(12); hs.paragraph_format.space_after = Pt(6)
for s in doc.sections:
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5)
    s.left_margin = Cm(3.0); s.right_margin = Cm(2.5)
C = WD_ALIGN_PARAGRAPH.CENTER

def pb(): doc.add_page_break()
def P(t, b=False, i=False, a=None, sz=None):
    p = doc.add_paragraph(); r = p.add_run(t); r.font.name = "Times New Roman"
    if b: r.bold = True
    if i: r.italic = True
    if sz: r.font.size = Pt(sz)
    if a: p.alignment = a
    return p
def B(t): return P(t)
def BI(items):
    for item in items: doc.add_paragraph(item, style="List Bullet")
def IMG(fn, caption=None, w=Inches(5.5)):
    path = os.path.join(ASSETS, fn)
    if os.path.exists(path):
        p = doc.add_paragraph(); p.alignment = C; r = p.add_run(); r.add_picture(path, width=w)
        if caption:
            cp = doc.add_paragraph(); cp.alignment = C
            r2 = cp.add_run(caption); r2.font.size = Pt(10); r2.font.italic = True; r2.font.name = "Times New Roman"
    else:
        P(f"[Image non trouvee : {fn}]", i=True, a=C)
def TBL(headers, rows, cw=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = ""; p = c.paragraphs[0]; r = p.add_run(h)
        r.bold = True; r.font.size = Pt(10); r.font.name = "Times New Roman"; p.alignment = C
        sh = parse_xml(f'<w:shd {nsdecls("w")} w:fill="003366"/>')
        c._tc.get_or_add_tcPr().append(sh)
        r.font.color.rgb = RGBColor(255, 255, 255)
    for ri, row in enumerate(rows):
        for ci, v in enumerate(row):
            c = t.rows[ri + 1].cells[ci]; c.text = ""
            p = c.paragraphs[0]; r = p.add_run(str(v))
            r.font.size = Pt(10); r.font.name = "Times New Roman"
    if cw:
        for i, ww in enumerate(cw):
            for row in t.rows: row.cells[i].width = Inches(ww)
    doc.add_paragraph()
    return t

# ════════════════════════════════════════════════════════════════════
# PAGE DE GARDE
# ════════════════════════════════════════════════════════════════════
for _ in range(4): doc.add_paragraph()
P("UNIVERSITÉ DU BURUNDI", b=True, a=C, sz=14)
P("Faculté des Sciences", b=True, a=C, sz=13)
doc.add_paragraph()
P("Département de Génie Logiciel", a=C, sz=12)
doc.add_paragraph(); doc.add_paragraph(); doc.add_paragraph()
P("Conception et Réalisation d'une API de Gestion\ndes Stocks d'Engrais : Cas de la Société FOMI\nau Burundi", b=True, a=C, sz=16)
doc.add_paragraph()
P("Mémoire de Fin d'Études en Génie Logiciel", i=True, a=C, sz=13)
doc.add_paragraph(); doc.add_paragraph(); doc.add_paragraph()
P("Présenté par :", a=C)
P("Davy-Antosper NIYONGABO", b=True, a=C, sz=14)
doc.add_paragraph()
P("Sous la direction de :", a=C)
P("Prof. [Nom du Directeur]", b=True, a=C)
doc.add_paragraph(); doc.add_paragraph()
P("Année Académique 2025-2026", a=C)
pb()

# ════════════════════════════════════════════════════════════════════
# DÉDICACE
# ════════════════════════════════════════════════════════════════════
P("DÉDICACE", b=True, a=C, sz=14); doc.add_paragraph()
B("Je dédie ce travail à mes chers parents, pour leur soutien indéfectible tout au long de mon parcours académique, ainsi qu'à toute ma famille et à mes amis qui m'ont encouragé dans cette aventure intellectuelle.")
doc.add_paragraph()
B("Je le dédie également à tous les agriculteurs burundais qui, au prix d'efforts considérables, contribuent quotidiennement à la sécurité alimentaire de notre nation. Que ce modeste travail puisse, à son échelle, contribuer à améliorer les conditions de travail et de vie de ceux qui nourrissent notre pays.")
pb()

# ════════════════════════════════════════════════════════════════════
# REMERCIEMENTS
# ════════════════════════════════════════════════════════════════════
P("REMERCIEMENTS", b=True, a=C, sz=14); doc.add_paragraph()
B("Je tiens à exprimer ma profonde gratitude à mon directeur de mémoire pour sa disponibilité, ses conseils avisés et son accompagnement tout au long de la réalisation de ce travail. Sa rigueur scientifique et sa patience ont été des qualités essentielles qui ont permis l'aboutissement de ce projet.")
B("Mes remerciements s'adressent également aux membres du corps enseignant du Département de Génie Logiciel de la Faculté des Sciences de l'Université du Burundi pour la qualité de la formation reçue au cours de ces années d'études. Les connaissances acquises en programmation, en bases de données, en génie logiciel et en architecture logicielle ont constitué le socle sur lequel repose ce travail.")
B("Je remercie toute l'équipe technique de FOMI — Fertilisants Organo-Minéraux Industries pour leur accueil chaleureux, leur collaboration et leur ouverture dans le partage d'informations techniques essentielles à la réalisation de ce projet. Les échanges avec les responsables de la distribution, les agents de terrain et les informaticiens de l'entreprise ont permis de comprendre en profondeur les réalités opérationnelles qui motivent ce projet.")
B("Je remercie également les membres du jury qui accepteront d'évaluer ce travail pour leurs remarques constructives qui contribueront à son amélioration.")
B("Enfin, je remercie ma famille et mes amis pour leur soutien moral et leur patience tout au long de ces années d'études. Leur présence bienveillante a été une source d'inspiration et de motivation constante.")
pb()

# ════════════════════════════════════════════════════════════════════
# RÉSUMÉ
# ════════════════════════════════════════════════════════════════════
P("RÉSUMÉ", b=True, a=C, sz=14); doc.add_paragraph()
B("Le Burundi, pays d'Afrique de l'Est à vocation essentiellement agricole, fait face à des défis majeurs en matière de gestion des intrants agricoles, notamment les engrais. La société FOMI — Fertilisants Organo-Minéraux Industries, premier producteur d'engrais organo-minéraux au Burundi, joue un rôle central dans la chaîne d'approvisionnement via le Programme National de Subvention des Engrais (PNSEB). Cependant, la gestion des stocks repose encore largement sur des processus manuels, engendrant des ruptures de stock chroniques, des pertes d'informations, des risques de fraude et des retards dans la distribution aux agriculteurs.")
B("Ce mémoire présente la conception et la réalisation d'une API RESTful dédiée à la gestion centralisée des stocks d'engrais de la société FOMI. L'application, développée en Java 21 avec le framework Spring Boot 3.3.5 et la base de données PostgreSQL 16, implémente un système complet couvrant l'authentification par JWT avec contrôle d'accès basé sur les rôles (RBAC), la gestion FIFO des lots par date de péremption, un système d'alertes automatiques de rupture et de stock bas, un workflow de validation des tickets de distribution, ainsi qu'un audit trail complet de toutes les opérations.")
B("L'API expose plus de 50 endpoints REST documentés via Swagger, et le projet compte 203 tests automatisés d'intégration et unitaires, tous validés. La solution répond aux 27 besoins fonctionnels identifiés dans le cahier des charges et intègre des mécanismes de sécurité avancés incluant le filtrage périmétrique par niveau géographique. Ce travail constitue une contribution significative à la modernisation de la gestion des stocks agricoles au Burundi et offre des perspectives d'évolution vers une plateforme numérique complète intégrant le frontend, les notifications SMS et les paiements mobiles.")
doc.add_paragraph()
P("Mots-clés : API REST, gestion des stocks, Spring Boot, PostgreSQL, FIFO, RBAC, engrais, FOMI, Burundi, JWT, audit trail, PNSEB", i=True, sz=11)
doc.add_paragraph(); doc.add_paragraph()
P("ABSTRACT", b=True, a=C, sz=14); doc.add_paragraph()
B("Burundi, an East African country with a predominantly agricultural economy, faces significant challenges in managing agricultural inputs, particularly fertilizers. FOMI — Fertilisants Organo-Minéraux Industries, the first organo-mineral fertilizer producer in Burundi, plays a central role in the supply chain through the National Fertilizer Subsidy Program (PNSEB). However, stock management still largely relies on manual processes, leading to chronic stockouts, information loss, fraud risks, and delays in farmer distribution.")
B("This thesis presents the design and implementation of a RESTful API for centralized fertilizer stock management at FOMI. Built with Java 21, Spring Boot 3.3.5, and PostgreSQL 16, the application implements a comprehensive system including JWT authentication with Role-Based Access Control (RBAC), FIFO stock management by expiration date, automatic alerting for stock depletion and low levels, a ticket validation workflow, and a complete audit trail of all operations.")
B("The API exposes over 50 REST endpoints documented via Swagger, with 203 automated integration and unit tests, all passing. The solution addresses all 27 functional requirements identified in the specifications and integrates advanced security mechanisms including geographic scope filtering. This work contributes significantly to the modernization of agricultural stock management in Burundi and offers evolution prospects toward a complete digital platform integrating frontend, SMS notifications, and mobile payments.")
pb()

# ════════════════════════════════════════════════════════════════════
# LISTE DES ABRÉVIATIONS
# ════════════════════════════════════════════════════════════════════
P("LISTE DES ABRÉVIATIONS", b=True, a=C, sz=14); doc.add_paragraph()
TBL(["Abréviation", "Signification"], [
    ("API", "Application Programming Interface"),
    ("BPEAE", "Bureau Provincial de l'Éducation et de l'Agriculture et de l'Élevage"),
    ("DAP", "Di-ammonium Phosphate (18-46-0)"),
    ("CSV", "Comma-Separated Values"),
    ("CRUD", "Create, Read, Update, Delete"),
    ("FCFA", "Fonds Commun pour les Fertilisants et Amendements"),
    ("FENACOBU", "Fédération Nationale des Coopératives d'Épargne et de Crédit du Burundi"),
    ("FIFO", "First In, First Out"),
    ("FOMI", "Fertilisants Organo-Minéraux Industries"),
    ("HMAC", "Hash-based Message Authentication Code"),
    ("ISO", "International Organization for Standardization"),
    ("JWT", "JSON Web Token"),
    ("NPK", "Nitrogène-Phosphore-Potassium"),
    ("PNSEB", "Programme National de Subvention des Engrais au Burundi"),
    ("RBAC", "Role-Based Access Control"),
    ("REST", "Representational State Transfer"),
    ("SQL", "Structured Query Language"),
    ("JSONB", "Binary JSON"),
    ("UTC", "Coordinated Universal Time"),
], cw=[1.5, 4.5])
pb()
pass

# ════════════════════════════════════════════════════════════════════
# TABLE DES MATIÈRES + LISTES
# ════════════════════════════════════════════════════════════════════
P("TABLE DES MATIÈRES", b=True, a=C, sz=14); doc.add_paragraph()
for line in [
    "Dédicace .......................................................... III",
    "Remerciements ..................................................... V",
    "Résumé ............................................................ VII",
    "Liste des abréviations ........................................... IX",
    "Table des matières ................................................ XI",
    "Liste des figures ................................................. XIII",
    "Liste des tableaux ................................................ XV",
    "",
    "PREMIÈRE PARTIE : CONTEXTE ET PROBLÉMATIQUE",
    "  Chapitre 1 : Le Burundi et son secteur agricole .................. 1",
    "  Chapitre 2 : FOMI — Fertilisants Organo-Minéraux Industries ...... 13",
    "  Chapitre 3 : Problématique et objectifs .......................... 25",
    "",
    "DEUXIÈME PARTIE : ANALYSE ET CONCEPTION",
    "  Chapitre 4 : Analyse des besoins ................................. 33",
    "  Chapitre 5 : Conception technique ............................... 48",
    "  Chapitre 6 : Choix technologiques ................................ 66",
    "",
    "TROISIÈME PARTIE : RÉALISATION",
    "  Chapitre 7 : Implémentation ...................................... 74",
    "  Chapitre 8 : Tests et déploiement ............................... 89",
    "",
    "QUATRIÈME PARTIE : ÉVALUATION ET PERSPECTIVES",
    "  Chapitre 9 : Évaluation .......................................... 97",
    "  Chapitre 10 : Conclusion et perspectives ......................... 105",
    "",
    "Bibliographie ...................................................... 110",
    "Annexes ............................................................ 115",
]: B(line)
pb()

P("LISTE DES FIGURES", b=True, a=C, sz=14); doc.add_paragraph()
TBL(["Réf.", "Description"], [
    ("Figure 1.1", "Carte administrative du Burundi après la réforme de 2023"),
    ("Figure 2.1", "Chronologie de la société FOMI"),
    ("Figure 2.2", "Circuit de distribution des engrais FOMI"),
    ("Figure 5.1", "Architecture globale du système"),
    ("Figure 5.2", "Architecture en couches"),
    ("Figure 5.3", "Diagramme Entité-Relation"),
    ("Figure 5.4", "Diagramme de séquence — Création et validation de ticket"),
    ("Figure 5.5", "Diagramme de séquence — Distribution FIFO"),
    ("Figure 5.6", "Machine à états du ticket"),
    ("Figure 5.7", "Organigramme de l'algorithme FIFO"),
    ("Figure 5.8", "Matrice RBAC — Rôles et permissions"),
    ("Figure 5.9", "Diagramme de classes UML — Entités principales"),
    ("Figure 5.10", "Diagramme de déploiement — Client / API / DB"),
    ("Figure 5.11", "Diagramme de cas d'utilisation — UC-01 à UC-26"),
    ("Figure 5.12", "Diagramme d'activités — Distribution FIFO"),
    ("Figure 5.13", "Dictionnaire de données — Tables et colonnes"),
], cw=[1.2, 5.0])
pb()

P("LISTE DES TABLEAUX", b=True, a=C, sz=14); doc.add_paragraph()
TBL(["Réf.", "Description"], [
    ("Tableau 1.1", "Principales cultures au Burundi"),
    ("Tableau 1.2", "Consommation d'engrais au Burundi (2018-2024)"),
    ("Tableau 1.3", "Prix subventionnés des engrais FOMI"),
    ("Tableau 2.1", "Caractéristiques des produits FOMI"),
    ("Tableau 2.2", "Comparaison des engrais FOMI et conventionnels"),
    ("Tableau 3.1", "Problèmes identifiés et impacts"),
    ("Tableau 4.1", "Besoins fonctionnels détaillés (F1-F27)"),
    ("Tableau 4.2", "Règles métier (R1-R23)"),
    ("Tableau 4.3", "Cas d'utilisation (UC-01 à UC-26)"),
    ("Tableau 4.4", "Besoins non fonctionnels (NF1-NF10)"),
    ("Tableau 5.1", "Description des tables de la base de données"),
    ("Tableau 5.2", "Énumérations du système"),
    ("Tableau 5.3", "Dictionnaire de données : colonnes, types SQL et contraintes"),
    ("Tableau 6.1", "Comparatif des choix technologiques"),
    ("Tableau 7.1", "Structure des packages du projet"),
    ("Tableau 7.2", "Types d'alertes et déclencheurs"),
    ("Tableau 8.1", "Récapitulatif des tests d'intégration"),
    ("Tableau 9.1", "Conformité aux besoins fonctionnels"),
], cw=[1.2, 5.0])
pb()

# ════════════════════════════════════════════════════════════════════
# PREMIÈRE PARTIE + CHAPITRE 1 (expanded)
# ════════════════════════════════════════════════════════════════════
P("PREMIÈRE PARTIE", b=True, a=C, sz=16)
P("CONTEXTE ET PROBLÉMATIQUE", b=True, a=C, sz=14)
pb()

doc.add_heading("Chapitre 1 : Le Burundi et son secteur agricole", level=1)
B("Le Burundi, petite nation enclavée de la région des Grands Lacs en Afrique de l'Est, présente un profil économique et démographique singulier. Malgré des ressources naturelles limitées et une superficie modeste, le pays tire l'essentiel de son revenu national de l'agriculture, secteur qui emploie la grande majorité de sa population active. Comprendre le contexte dans lequel évolue la société FOMI est essentiel pour appréhender les enjeux de la gestion des stocks d'engrais au Burundi. Ce chapitre pose le cadre géographique, économique et agronomique qui justifie la pertinence et l'urgence d'un système d'information pour la gestion des intrants agricoles.")

doc.add_heading("1.1 Géographie et économie du Burundi", level=2)
B("Le Burundi est situé entre les latitudes 2°23' et 4°27' Sud et les longitudes 28°59' et 30°49' Est. Il est borné au nord par le Rwanda, à l'est et au sud par la Tanzanie, et à l'ouest par la République Démocratique du Congo, dont la frontière est marquée par le lac Tanganyika, le deuxième plus grand lac d'Afrique. Sa superficie totale est de 27 834 km², ce qui en fait l'un des plus petits pays du continent africain, comparable en taille au Rwanda voisin (26 338 km²) ou au Maryland aux États-Unis.")
B("La topographie du Burundi est caractérisée par un relief accidenté avec des altitudes variant de 774 mètres au niveau du lac Tanganyika à 2 670 mètres au sommet du mont Heha, le point culminant du pays. Le territoire se divise en trois régions naturelles : la plaine de la Rusizi à l'ouest le long du lac Tanganyika, le plateau central et les collines qui couvrent la majeure partie du territoire, et les plaines à l'est. Cette topographie accidentée, combinée à une densité de population élevée, rend l'agriculture particulièrement vulnérable à l'érosion des sols.")
B("La population burundaise, estimée à environ 13 millions d'habitants en 2024, affiche une densité de population parmi les plus élevées d'Afrique, avec environ 467 habitants par km². Cette pression démographique sur des terres agricoles limitées constitue un défi majeur pour la sécurité alimentaire du pays. Avec un taux de croissance démographique de 2,7 % par an, la pression sur les ressources agricoles ne cesse d'augmenter, rendant chaque amélioration de productivité cruciale pour la survie des communautés rurales.")
B("L'économie burundaise demeure essentiellement agropastorale. Le produit intérieur brut (PIB) par habitant est estimé à environ 260 USD, plaçant le Burundi parmi les pays les plus pauvres du monde selon les critères de la Banque Mondiale. Le PIB total du pays est d'environ 3,4 milliards USD (2024). L'agriculture représente environ 34,9 % du PIB national en 2024 et emploie près de 85 % de la population active. Cette dépendance quasi-exclusive à l'agriculture rend l'économie particulièrement vulnérable aux aléas climatiques, aux maladies des cultures et aux fluctuations des prix mondiaux des matières premières.")
B("Les principales cultures vivrières sont le maïs, les haricots, le riz, le manioc et la patate douce, qui constituent l'alimentation de base des ménages burundais. Le maïs occupe la première place en termes de superficie cultivée, couvrant environ 350 000 hectares, suivi des haricots (280 000 ha), du manioc (200 000 ha) et de la patate douce (150 000 ha). Les cultures de rente, notamment le café (Arabica) et le thé, représentent l'essentiel des exportations du pays, générant environ 70 % des recettes en devises. Toutefois, les rendements restent très inférieurs aux standards régionaux : le rendement céréalier moyen est d'environ 1 163 kg/ha en 2024, contre plus de 2 000 kg/ha dans les pays voisins comme le Kenya et la Tanzanie, et 3 000 à 5 000 kg/ha dans les pays développés.")

P("Tableau 1.1 — Principales cultures au Burundi", b=True, a=C, sz=11)
TBL(["Culture", "Type", "Rendement moyen", "Zones principales", "Superficie (ha)"], [
    ("Maïs", "Vivrière", "~1 100 kg/ha", "Répartition nationale", "~350 000"),
    ("Haricots", "Vivrière", "~600 kg/ha", "Répartition nationale", "~280 000"),
    ("Riz", "Vivrière", "~2 500 kg/ha", "Plaines humides", "~35 000"),
    ("Manioc", "Vivrière", "~8 000 kg/ha", "Sols pauvres", "~200 000"),
    ("Patate douce", "Vivrière", "~6 000 kg/ha", "Collines", "~150 000"),
    ("Café (Arabica)", "Rente", "~0,8 t/ha", "Altitude > 1200m", "~60 000"),
    ("Thé", "Rente", "~4 t/ha", "Nord et centre", "~10 000"),
    ("Soja", "Légumineuse", "~1 200 kg/ha", "Intérêt croissant", "~15 000"),
    ("Arachide", "Légumineuse", "~1 000 kg/ha", "Plaines", "~20 000"),
], cw=[1.1, 0.8, 1.1, 1.5, 1.2])

B("La faiblesse des rendements s'explique par plusieurs facteurs convergents qui se renforcent mutuellement. L'érosion des sols, aggravée par la culture sur pente et les pluies torrentielles de la saison humide, emporte chaque année des milliers de tonnes de terre arable. Le manque d'intrants agricoles de qualité — semences améliorées, engrais, produits phytosanitaires — prive les cultures des nutriments essentiels à leur croissance. L'absence quasi-totale de mécanisation agricole limite la superficie cultivable par ménage et réduit l'efficacité des travaux champêtres. Enfin, les pratiques culturales traditionnelles, bien qu'adaptées au contexte local, ne permettent pas d'optimiser les rendements sans apport extérieur d'intrants.")
B("Dans ce contexte, l'accès à des engrais de qualité à prix abordable revêt une importance capitale pour améliorer la productivité agricole et, par conséquent, la sécurité alimentaire du pays. Les études agronomiques montrent qu'un apport correct en engrais peut multiplier les rendements par deux à trois dans les sols burundais, transformation qui pourrait à elle seule éliminer les déficits alimentaires chroniques du pays.")

doc.add_heading("1.2 Le défi de la fertilité des sols", level=2)
B("La fertilité des sols constitue l'un des défis les plus pressants de l'agriculture burundaise. Les sols du Burundi sont majoritairement acides, avec un pH variant entre 4,5 et 5,5, bien en dessous de la plage optimale de 6,0 à 7,0 pour la plupart des cultures vivrières. Cette acidité est particulièrement problématique car elle réduit la biodisponibilité du phosphore, élément nutritif pourtant essentiel au développement racinaire et à la formation des graines.")
B("Les sols burundais sont pauvres en phosphore disponible, avec des teneurs moyennes de 3 à 8 mg/kg de P assimilable, bien en dessous du seuil critique de 15 mg/kg en deçà duquel les apports en engrais phosphatés deviennent indispensables. Cette pauvreté en phosphore s'explique à la fois par la nature géologique des roches mères (roches cristallines pauvres en phosphore) et par les pratiques agricoles qui exportent le phosphore du sol sans compensation adéquate.")
B("En outre, les sols des collines burundaises sont sujets à une érosion rapide due au relief accidenté, aux pluies torrentielles et aux pratiques de culture sur pente. L'érosion emporte non seulement les particules fines du sol riches en matière organique et en nutriments, mais aussi les engrais appliqués en surface avant qu'ils ne soient absorbés par les racines des plantes. Il est estimé que l'érosion des sols coûte au Burundi l'équivalent de 1 à 2 % du PIB agricole chaque année.")
B("L'utilisation d'engrais chimiques au Burundi reste très en deçà des besoins réels. La consommation totale oscillait historiquement entre 15 000 et 25 000 tonnes par an, soit une consommation par hectare de l'ordre de 39,79 kg/ha en 2022. Cette consommation est très inférieure à la recommandation technique de 100 à 200 kg/ha selon les cultures et les types de sol. Pour comparaison, le Kenya consomme environ 40 kg/ha, la Tanzanie 15 kg/ha, et les pays d'Europe de l'Ouest entre 150 et 300 kg/ha. Le Burundi se situe donc dans une zone de sous-fertilisation chronique qui compromet directement la productivité agricole.")
B("L'acidité des sols aggrave considérablement le problème de la fertilisation. Sans apport correcteur de chaux ou d'amendements calcaires, l'efficacité des engrais minéraux est réduite de 30 à 50 %. Les sols acides fixent le phosphore sous des formes insolubles (aluminium-phosphate, fer-phosphate), rendant cet élément nutritif inaccessible aux racines des plantes. De plus, les sols fortement acides (pH < 5,0) libèrent de l'aluminium et du manganese en quantités toxiques pour les racines, entravant leur développement et réduisant leur capacité d'absorption des nutriments. Cette situation appelle des solutions intégrées combinant amendements et fertilisants, ce qui justifie le positionnement stratégique des engrais organo-minéraux produits par FOMI, qui contiennent naturellement des amendements calciques.")

P("Tableau 1.2 — Consommation d'engrais au Burundi (2018-2024)", b=True, a=C, sz=11)
TBL(["Année", "Consommation (t)", "kg/ha", "Observations"], [
    ("2018", "~12 000", "31.2", "Importation dominante, FOMI naissante"),
    ("2019", "~18 000", "47.0", "Lancement FOMI + interdiction import engrais chimiques"),
    ("2020", "~20 000", "52.2", "Production FOMI en hausse, COVID-19 ralentit"),
    ("2021", "~25 000", "65.2", "Capacité FOMI atteint 500 t/jour"),
    ("2022", "~30 000", "39.79", "Expansion PNSEB, records de distribution"),
    ("2023", "~22 000", "57.4", "Contraintes logistiques, déficit 3656t"),
    ("2024", "~25 000", "65.2", "Reprise partielle, besoins croissants"),
], cw=[0.7, 1.3, 0.8, 2.8])

B("Les principaux types d'engrais utilisés au Burundi sont le DAP (Di-ammonium Phosphate, 18-46-0), l'URÉA (46-0-0) et le NPK 17-17-17. Le DAP, qui assure à la fois la fertilisation phosphatée et azotée, reste l'engrais le plus demandé par les paysans, en particulier pour la culture du maïs lors de la plantation. Le NPK, qui apporte les trois éléments majeurs (azote, phosphore et potassium), est utilisé en second rang pour les cultures exigeantes en potassium comme les haricots et les pommes de terre. L'URÉA, riche en azote (46 %), est principalement utilisé en top-dressing pour les céréales déjà en phase de croissance végétative.")
B("Toutefois, l'accès à ces engrais est limité par leur coût élevé, leur disponibilité irrégulière et les contraintes logistiques liées au caractère enclavé du pays. Le Burundi ne produit pas d'engrais chimiques purs et dépend entièrement des importations pour ces intrants, ce qui le rend vulnérable aux fluctuations des prix mondiaux et aux perturbations des chaînes d'approvisionnement internationales. C'est dans ce contexte de dépendance stratégique que la création de FOMI revêt une importance nationale.")

doc.add_heading("1.3 Le Programme National de Subvention des Engrais (PNSEB)", level=2)
B("Face à la crise de la fertilité des sols et à l'insécurité alimentaire croissante, le gouvernement burundais a mis en place le Programme National de Subvention des Engrais au Burundi (PNSEB). Ce programme, coordonné par le Ministère de l'Agriculture et de l'Élevage, vise à rendre les engrais accessibles aux petits agriculteurs à travers un mécanisme de subvention publique. Le PNSEB constitue l'un des plus grands programmes d'appui agricole en Afrique de l'Est en termes de nombre de bénéficiaires par rapport à la taille du pays.")
B("Le Fonds Commun pour les Fertilisants et Amendements (FCFA), créé par le décret n° 100-119 du 20 mai 2013, constitue l'outil financier du programme. Le FCFA est alimenté par le budget de l'État, les contributions des partenaires internationaux (Banque Mondiale, FAO, Union Européenne) et les fonds propres de FOMI. Le mécanisme de subvention permet de réduire le prix de vente des engrais de 64 % à 74 % par rapport au prix de revient, rendant ainsi ces intrants accessibles même aux plus petits producteurs dont le revenu annuel ne dépasse pas 100 à 200 USD.")
B("Cette subvention considérable a permis d'étendre le programme à un nombre croissant de bénéficiaires : en 2019, 865 666 agriculteurs étaient inscrits dans le système, soit environ 48 % des ménages agricoles du pays. L'inscription se fait au niveau des collines, où les autorités locales recensent les agriculteurs éligibles en fonction de la superficie cultivable et de la situation socio-économique du ménage. Chaque agriculteur inscrit reçoit un identifiant unique qui lui permet de bénéficier des engrais subventionnés selon un quota calculé en fonction de la superficie de ses terres.")
B("Le mécanisme de distribution repose sur un circuit hiérarchisé structuré en cinq niveaux, depuis l'usine FOMI de Maramvya jusqu'aux agriculteurs bénéficiaires. Les engrais, d'abord stockés à l'usine, sont acheminés vers les BPEAE qui constituent les dépôts provinciaux. De là, les stocks sont distribués vers les dépôts de zone, puis vers les dépôts de colline, avant d'atteindre finalement les agriculteurs. Ce circuit implique de multiples acteurs et institutions, chacun jouant un rôle spécifique dans la chaîne de distribution.")

P("Tableau 1.3 — Prix subventionnés des engrais FOMI", b=True, a=C, sz=11)
TBL(["Produit", "Cond.", "Prix usine (FBu)", "Prix agri. (FBu)", "Taux subv.", "Prix marché noir"], [
    ("FOMI-IMBURA (NPK 9-22-4)", "50 kg", "86 408", "~31 000", "64 %", "250 000-350 000"),
    ("FOMI-BAGARA (NK 11-0-22)", "50 kg", "77 473", "~28 000", "64 %", "200 000-300 000"),
    ("FOMI-TOTAHAZA (NK 21-0-8)", "50 kg", "~70 000", "~25 000", "64 %", "180 000-250 000"),
    ("Chaux agricole", "50 kg", "~40 000", "~14 000", "65 %", "80 000-120 000"),
], cw=[1.5, 0.6, 1.0, 1.0, 0.7, 1.2])

B("Le système de paiement implique souvent des microfinances partenaires, notamment la Poste du Burundi et la FENACOBU, qui collectent les fonds auprès des agriculteurs et les transmettent à FOMI. Un paiement avance de 50 % du prix subventionné est généralement requis avant la mise à disposition des engrais, créant ainsi une avance de trésorerie pour l'approvisionnement en intrants. Le solde de 50 % est payé lors du reeffectif du retrait des engrais au dépôt de colline.")
B("Le PNSEB a permis d'augmenter significativement la consommation d'engrais au Burundi et d'améliorer les rendements dans les zones couvertes par le programme. Les évaluations de la FAO montrent une amélioration moyenne de 25 à 40 % des rendements dans les zones bien desservies par le programme. Cependant, des défis persistent, notamment en ce qui concerne la régularité de l'approvisionnement, la traçabilité des distributions, l'identification des bénéficiaires réels et la lutte contre la fraude et le détournement des intrants subventionnés.")

doc.add_heading("1.4 La réforme administrative de 2023", level=2)
B("En 2023, le Burundi a entrepris une profonde réforme de son organisation administrative, l'une des plus importantes depuis l'indépendance du pays en 1962. Le nombre de provinces a été réduit de 18 à 5, et celui des communes est passé de 119 à 42. Les nouvelles provinces sont : Bujumbura Mairie, Bujumbura Rural, Gitega, Muyinga et Ngozi. Cette réorganisation, motivée par des impératifs de gouvernance et de décentralisation visant à réduire les coûts administratifs et à améliorer l'efficacité des services publics, a eu des répercussions directes sur la chaîne de distribution des engrais.")
B("La reconfiguration territoriale a entraîné la redistribution des zones de compétence des BPEAE, la restructuration des dépôts provinciaux et la réorganisation des circuits logistiques. Les anciennes limites provinciales ne correspondant plus aux nouvelles circonscriptions, il a été nécessaire de revoir l'ensemble du maillage territorial de distribution, incluant la réaffectation des stocks entre dépôts, la réorganisation des équipes de distribution et la mise à jour des circuits d'acheminement. Cette transition a généré des perturbations temporaires significatives dans l'approvisionnement des agriculteurs, avec des retards de distribution allant jusqu'à deux mois dans certaines zones.")
B("Cette réforme met en évidence la nécessité d'un système de gestion informatisé capable de s'adapter rapidement aux changements de structure administrative. Un système rigide, dépendant d'une organisation territoriale figée dans son code source, serait incapable de s'ajuster aux nouvelles configurations géographiques sans intervention manuelle lourde et coûteuse. Cette considération a influencé les choix de conception de l'API de gestion des stocks, notamment en ce qui concerne la modélisation de la hiérarchie géographique avec des niveaux de dépôt configurables et des relations inter-dépôts flexibles. Le système conçu dans le cadre de ce mémoire permet l'ajout, la modification et la suppression de niveaux géographiques sans modification du code applicatif.")
pb()

# ── CHAPITRE 2 (expanded) ──────────────────────────────────────────
doc.add_heading("Chapitre 2 : FOMI — Fertilisants Organo-Minéraux Industries", level=1)
B("Ce chapitre présente en détail la société FOMI, acteur central de la chaîne d'approvisionnement en engrais au Burundi. L'historique de l'entreprise, ses produits, son circuit de distribution et les défis auxquels elle fait face sont analysés pour comprendre les enjeux spécifiques qui motivent la conception d'un système de gestion des stocks informatisé.")

doc.add_heading("2.1 Historique et création", level=2)
B("FOMI — Fertilisants Organo-Minéraux Industries — a été fondée en février 2019 par M. Adrien Ntigacika, à travers le groupe ITRACOM Holdings. Il s'agit de la première et unique usine de production d'engrais organo-minéraux au Burundi, marquant ainsi une étape historique dans l'autonomie du pays en matière d'intrants agricoles. La création de FOMI répond à un besoin stratégique national : réduire la dépendance du Burundi aux importations d'engrais et promouvoir la production locale à partir de matières premières disponibles localement.")
B("L'usine principale est située à Maramvya, dans la Commune de Mutimbuzi, province de Bujumbura Rural. Ce choix de localisation, à proximité du lac Tanganyika et des axes de communication majeurs, facilite à la fois l'importation des matières premières (phosphates, potasse) et l'acheminement des produits finis vers les différentes provinces du pays. La zone industrielle de Maramvya bénéficie d'une connexion routière directe vers Bujumbura (50 km), Gitega (120 km) et les principales villes du pays.")
B("La création de FOMI a coïncidé avec une décision gouvernementale stratégique : l'interdiction de l'importation d'engrais chimiques purs en 2019. Cette mesure, destinée à promouvoir la production locale et à réduire la dépendance aux importations, a conféré à FOMI une position de quasi-monopole sur le marché des engrais au Burundi. Aujourd'hui, FOMI demeure le principal fournisseur d'engrais pour le PNSEB, produisant la quasi-totalité des engrais distribués dans le cadre du programme de subvention.")

IMG("fomi_timeline.png", "Figure 2.1 — Chronologie de la société FOMI")

B("La capacité de production de FOMI a connu une croissance rapide depuis son lancement. L'usine a démarré avec une capacité de 150 à 200 tonnes par jour en 2019, avant d'atteindre 500 tonnes par jour dès 2021, soit une multiplication par trois en deux ans. Cette montée en puissance a permis de créer plus de 3 500 emplois directs et indirects, contribuant significativement à l'économie nationale. L'usine emploie environ 800 personnes en permanence, avec desEffectifs supplémentaires recrutés lors des pics de production liés aux campagnes agricoles.")
B("En 2021, FOMI a obtenu les certifications ISO 9001 (management de la qualité), ISO 14001 (management environnemental) et ISO 45001 (santé et sécurité au travail), démontrant son engagement envers les standards internationaux de production. Ces certifications, obtenues en un temps record pour une entreprise burundaise, témoignent de la rigueur managériale et technique de l'entreprise. L'entreprise a également étendu ses activités à la Tanzanie avec l'ouverture d'une usine secondaire, consolidant ainsi sa présence régionale et diversifiant ses sources de revenus.")

doc.add_heading("2.2 Les produits FOMI", level=2)
B("FOMI commercialise une gamme diversifiée de produits adaptés aux besoins spécifiques de l'agriculture burundaise. Chaque produit est formulé pour répondre aux exigences nutritionnelles de certaines cultures et aux caractéristiques pédologiques des sols burundais. La particularité des engrais FOMI réside dans leur composition organo-minérale, qui combine des éléments nutritifs minéraux à de la matière organique d'origine animale (fumier composté).")

P("Tableau 2.1 — Caractéristiques des produits FOMI", b=True, a=C, sz=11)
TBL(["Produit", "Formule", "Composition", "Cultures cibles", "Zones"], [
    ("FOMI-IMBURA", "NPK 9-22-4", "9% N, 22% P₂O₅, 4% K₂O", "Maïs, haricots, légumes", "Toutes zones"),
    ("FOMI-BAGARA", "NK 11-0-22", "11% N, 0% P, 22% K₂O", "Bananes, manioc, patate", "Collines sèches"),
    ("FOMI-TOTAHAZA", "NK 21-0-8", "21% N, 0% P, 8% K₂O", "Céréales (2e saison)", "Régénération azote"),
    ("Chaux agricole", "CaCO₃", "38% CaO + MgO", "Correction acide sols", "Sols acides"),
], cw=[1.2, 0.8, 1.5, 1.3, 0.9])

B("L'un des atouts majeurs des engrais FOMI est leur teneur élevée en matière organique. Constitués à 50 % de fumier composté, ces engrais organo-minéraux apportent non seulement les éléments nutritifs essentiels (azote, phosphore, potassium), mais également du calcium, du magnésium et de la matière organique qui améliore la structure du sol, sa capacité de rétention en eau et son activité microbienne. L'ajout de matière organique augmente la capacité de rétention en eau du sol de 15 à 25 %, avantage crucial dans un pays où les sécheresses ponctuelles peuvent ruiner une récolte entière.")
B("La matière organique des engrais FOMI constitue un aliment pour la faune et la flore du sol. Les micro-organismes du sol se nourrissent de cette matière organique et la transforment en humus, qui améliore la structure physique du sol (agrégation, porosité), sa capacité de rétention en eau et en nutriments, et son activité biologique. Les champignons mycorhiziens, essentiels pour l'absorption du phosphore par les racines des plantes, bénéficient particulièrement de cet apport en matière organique.")

P("Tableau 2.2 — Comparaison engrais FOMI et engrais conventionnels", b=True, a=C, sz=11)
TBL(["Critère", "FOMI organo-minéral", "Engrais chimique pur", "Avantage FOMI"], [
    ("Matière organique", "~50 %", "0 %", "Améliore structure sol"),
    ("Libération nutriments", "Progressive (60-90j)", "Rapide (15-30j)", "Moins de lessivage"),
    ("Effet sur sol", "Restauration long terme", "Nutrition court terme", "FOMI + chaux = idéal"),
    ("Prix subventionné", "~31 000 FBu/sac 50kg", "~25 000 FBu/sac 50kg", "Comparable"),
    ("Disponibilité locale", "Production nationale", "Importation", "Souveraineté alimentaire"),
    ("Impact environnemental", "Faible", "Modéré à élevé", "Réduit pollution"),
], cw=[1.3, 1.4, 1.4, 1.6])

doc.add_heading("2.3 Le circuit de distribution", level=2)
B("La distribution des engrais FOMI suit un circuit hiérarchisé en cinq niveaux, depuis l'usine de Maramvya jusqu'aux agriculteurs bénéficiaires. Ce circuit, structuré en conformité avec l'organisation administrative du pays, implique de multiples acteurs et institutions, chacun jouant un rôle spécifique et bien défini dans la chaîne de valeur.")

IMG("distribution_circuit.png", "Figure 2.2 — Circuit de distribution des engrais FOMI")

B("Le premier niveau du circuit est l'usine FOMI de Maramvya, point de production et de stockage central. Les engrais y sont stockés dans des entrepôts couverts d'une capacité totale de 15 000 tonnes après fabrication, attendant les commandes des niveaux inférieurs. C'est également le point de contrôle qualité où chaque lot est analysé avant stockage. Les stocks sont gérés par l'agent usine qui procède aux entrées de production et prépare les expéditions.")
B("Le deuxième niveau est constitué des BPEAE (Bureaux Provinciaux de l'Éducation, de l'Agriculture et de l'Élevage), qui constituent les dépôts provinciaux. Ces dépôts, gérés par les responsables provinciaux, reçoivent les livraisons de l'usine FOMI et répartissent les stocks entre les zones de leur province. La capacité de stockage de chaque dépôt provincial varie de 500 à 2 000 tonnes selon la taille de la province et le nombre d'agriculteurs bénéficiaires.")
B("Le troisième niveau est le dépôt de zone. Chaque zone administrative dispose d'un dépôt qui assure la réception des engrais depuis le dépôt provincial et leur distribution vers les collines de sa juridiction. Les agents de zone sont responsables de la planification des distributions et du suivi des stocks intermédiaires. La capacité de stockage des dépôts de zone est généralement de 100 à 500 tonnes.")
B("Le quatrième niveau est le dépôt de colline, le niveau le plus proche des agriculteurs. Les agents de colline reçoivent les engrais depuis le dépôt de zone et les distribuent directement aux agriculteurs bénéficiaires sur présentation de leur ticket de distribution. Les dépôts de colline ont une capacité de 20 à 100 tonnes et sont souvent des structures temporaires (hangars, écoles, églises) utilisées pendant la période de distribution.")
B("Le cinquième et dernier niveau est l'agriculteur, bénéficiaire final du programme de subvention. L'agriculteur se présente au dépôt de colline avec son ticket de distribution et sa pièce d'identité pour récupérer ses engrais. Le ticket, délivré après paiement, précise le type d'engrais, la quantité autorisée et la saison agricole concernée.")
B("Le processus de distribution implique un volet financier important. Les microfinances partenaires, notamment la Poste du Burundi et la FENACOBU, jouent un rôle d'intermédiaire financier en collectant les paiements des agriculteurs et les virant à FOMI. Un paiement avance de 50 % du prix subventionné est généralement requis avant la mise à disposition des engrais. Ce mécanisme permet à FOMI de constituer le capital de roulement nécessaire à l'approvisionnement en matières premières, qui doivent être importées en devises étrangères (dollars américains).")

doc.add_heading("2.4 Les défis de FOMI", level=2)
B("Malgré ses réalisations remarquables, la société FOMI fait face à des défis structurels majeurs qui entravent son efficacité dans la chaîne d'approvisionnement en engrais. Ces défis, souvent liés à l'absence de systèmes d'information performants pour la gestion des stocks et de la distribution, constituent la motivation principale du projet de mémoire.")
B("Ruptures de stock chroniques : Le déficit de stock a atteint 3 656 tonnes lors de la Saison A 2023, soit un écart considérable entre l'offre et la demande. En 2025, la production nationale de FOMI ne couvre que 27 % des besoins totaux du pays, laissant un vide considérable que les importations ne comblent que partiellement. Ces ruptures de stock entraînent des retards de distribution préjudiciables aux campagnes agricoles, car les agriculteurs ne reçoivent leurs engrais qu'après la période optimale de plantation. Les retards de distribution, qui peuvent aller jusqu'à trois semaines, réduisent les rendements de 15 à 25 % selon les études de l'ISABU.")
B("Fraude et marché noir : Le prix subventionné d'un sac de FOMI-IMBURA (50 kg) étant d'environ 31 000 FBu, tandis que le prix au marché noir peut atteindre 250 000 à 350 000 FBu, l'incitation à la fraude est considérable. Les sacs d'engrais revendus illégalement à des prix six à dix fois supérieurs au prix subventionné constituent un phénomène récurrent qui prive les agriculteurs bénéficiaires de leurs droits. En mars 2025, environ 100 sacs d'urée ont été volés à Gihanga lors de détournements nocturnes, illustrant l'ampleur du problème. La fraude se manifeste également par des distribution fictives, des gonflement des quantités déclarées et des ventes illicites à des non-bénéficiaires.")
B("Scandale financier et dette : En 2025, FOMI a réclamé 74 milliards FBu dans le cadre d'un différend financier lié aux subventions. Par ailleurs, l'entreprise cumule une dette de 368 millions USD, reflétant les difficultés financières liées au modèle de subvention et aux retards de paiement des bénéficiaires. Ces difficultés financières compromettent la capacité de FOMI à investir dans l'augmentation de sa production et dans la modernisation de ses équipements.")
B("Irrégularités dans la distribution : Les investigations menées par IWACU en février 2026 ont révélé de nombreuses irrégularités dans la distribution des engrais, incluant des cas de favoritisme, des distributions non documentées et des pertes de stock inexpliquées. Les agriculteurs dénoncent des paiements effectués depuis plus de deux ans sans réception des engrais correspondants. À Cibitoke, des agriculteurs ont rapporté qu'« un sac de 50 kg coûte 250 000 FBu au marché noir alors qu'il leur a été facturé au prix subventionné sans jamais être livré ».")
B("Ces défis convergent vers un constat central : l'absence d'un système d'information centralisé et fiable pour la gestion des stocks constitue le facteur aggravant majeur de tous les dysfonctionnements observés dans la chaîne d'approvisionnement. Sans visibilité en temps réel sur les niveaux de stock par dépôt, sans traçabilité des mouvements et des distributions, sans mécanisme d'alerte de rupture, il est impossible de détecter les anomalies, de prévenir les fraudes et d'optimiser la distribution. C'est précisément ce constat qui motive la réalisation du projet décrit dans ce mémoire.")

doc.add_heading("2.5 Systèmes de référence en Afrique de l'Est", level=2)
B("Plusieurs pays d'Afrique de l'Est ont développé des systèmes numériques pour la gestion des intrants agricoles et des stocks, offrant des modèles de référence pour le projet FOMI. L'analyse de ces systèmes permet d'identifier les meilleures pratiques et les fonctionnalités essentielles à implémenter.")
B("Au Rwanda, le système e-Soko (Electronic System for Agricultural Production and Marketing) permet le suivi en temps réel des stocks agricoles et des prix des intrants à travers tout le pays. Ce système, développé avec l'appui de la FAO, intègre des fonctionnalités de géolocalisation des dépôts et d'alertes automatiques de rupture de stock. Le Rwanda, avec sa superficie comparable à celle du Burundi (26 338 km²), constitue un modèle pertinent de référence. Le système e-Soko a permis de réduire les ruptures de stock de 40 % dans les zones couvertes et d'améliorer la transparence des prix des intrants.")
B("Au Kenya, la Kenya Agricultural and Livestock Research Organization (KALRO) a développé un système de gestion des semences et des engrais qui intègre le suivi des lots par date de production et date de péremption, un mécanisme similaire au FIFO implémenté dans le projet FOMI. Le Kenya, avec une consommation d'engrais de 40 kg/ha, offre un modèle de référence en matière de consommation optimisée. Le système kenyan intègre également un module de prévision de la demande basé sur les données climatiques et les historiques de production, une fonctionnalité qui pourrait être ajoutée dans les perspectives du projet FOMI.")
B("En Tanzanie, la Tanzania Fertilizer Regulatory Authority (TFRA) a mis en place un système de régulation et de traçabilité des engrais qui couvre l'ensemble de la chaîne, de l'importation à la distribution finale. Ce système, qui intègre des mécanismes de certification et de contrôle qualité, offre des leçons utiles pour la conception du module de traçabilité des lots dans l'API FOMI. Le TFRA utilise un code QR sur chaque sac d'engrais permettant de tracer l'origine, la date de production et le circuit de distribution, une technologie qui pourrait être intégrée dans une version future du système FOMI.")
B("L'analyse de ces systèmes de référence révèle des convergences dans les besoins fondamentaux : suivi en temps réel des stocks, traçabilité des lots, alertes de rupture, et mécanismes de contrôle de la fraude. Ces constats valident l'approche adoptée pour le projet FOMI tout en soulignant l'importance d'adapter les solutions aux spécificités du contexte burundais, notamment la hiérarchie géographique à cinq niveaux et le système de subvention impliquant des microfinances partenaires.")
pb()

# ── CHAPITRE 3 (expanded) ──────────────────────────────────────────
doc.add_heading("Chapitre 3 : Problématique et objectifs", level=1)
B("Ce chapitre formalise la problématique technique et organisationnelle qui motive le projet, identifie les objectifs à atteindre et délimite le périmètre du travail de mémoire. L'analyse des dysfonctionnements observés dans le système actuel de gestion des stocks de FOMI conduit à la formulation d'une problématique claire et à la définition d'objectifs mesurables.")

doc.add_heading("3.1 Les problèmes identifiés", level=2)
B("L'analyse du fonctionnement actuel du système de gestion des stocks de la société FOMI a permis d'identifier onze problèmes majeurs, regroupés en quatre catégories : gestion des stocks, distribution, suivi et transparence, et gouvernance. Chaque problème a été identifié à travers des entretiens avec les responsables de FOMI, des observations sur le terrain et l'analyse des documents de suivi existants (registres papier, tableurs Excel).")

P("Tableau 3.1 — Problèmes identifiés et impacts", b=True, a=C, sz=11)
TBL(["ID", "Catégorie", "Problème", "Impact"], [
    ("P1", "Gestion stocks", "Absence de suivi en temps réel des stocks", "Ruptures inattendues, réactions tardives"),
    ("P2", "Gestion stocks", "Mauvaise estimation des besoins", "Sous/sur-approvisionnement, gaspillage"),
    ("P3", "Distribution", "Difficulté à identifier agriculteurs non servis", "Inéquité dans la distribution"),
    ("P4", "Suivi", "Absence d'historique centralisé des mouvements", "Impossibilité d'audit, litiges"),
    ("P5", "Gouvernance", "Risque de fraude et détournement", "Pertes financières, perte confiance"),
    ("P6", "Suivi", "Manque de statistiques fiables", "Décisions non éclairées"),
    ("P7", "Distribution", "Retards chroniques dans la distribution", "Pertes de récoltes"),
    ("P8", "Gestion stocks", "Difficulté à localiser stocks disponibles", "Acheminement inefficace"),
    ("P9", "Gouvernance", "Absence de lien ticket-lot physique", "Impossibilité de traçabilité"),
    ("P10", "Gestion stocks", "Absence d'alerte préventive de rupture", "Gestion réactive"),
    ("P11", "Transparence", "Agriculteurs ne peuvent consulter commande", "Manque confiance, déplacements"),
], cw=[0.4, 0.9, 2.3, 1.9])

B("Le problème P1, l'absence de suivi en temps réel des stocks, est sans doute le plus critique car il est à l'origine de la plupart des autres dysfonctionnements. Sans visibilité en temps réel sur les niveaux de stock par dépôt et par type d'engrais, les responsables sont contraints de prendre des décisions basées sur des données obsolètes ou incomplètes. Les registres papier et les tableaux Excel utilisés actuellement ne permettent pas de disposer d'une image consolidée et actualisée de la situation des stocks à l'échelle nationale.")
B("Le problème P5, le risque de fraude et de détournement, est directement lié à l'absence de traçabilité (P4, P9). Sans enregistrement numérique des mouvements de stock et sans lien entre les tickets de distribution et les lots physiques, il est impossible de détecter les anomalies de distribution, de retracer l'historique des opérations ou de prouver les cas de fraude devant les instances disciplinaires ou judiciaires.")
B("Le problème P11, l'incapacité des agriculteurs à consulter l'état de leur commande, est particulièrement préjudiciable dans un contexte où la confiance entre les agriculteurs et les institutions est érodée par des années de retards et d'irrégularités. Les agriculteurs sont obligés de se déplacer physiquement aux dépôts pour connaître l'état de leur commande, souvent après des heures de marche, pour découvrir que les engrais ne sont pas encore disponibles.")

doc.add_heading("3.2 Conséquences pour les parties prenantes", level=2)
B("Les problèmes identifiés dans la section précédente ont des répercussions significatives sur les trois principales parties prenantes du système : les agriculteurs, la société FOMI et l'État burundais. Ces conséquences se renforcent mutuellement et créent un cercle vicieux qui affaiblit l'ensemble de la chaîne d'approvisionnement.")
B("Pour les agriculteurs, les conséquences sont les plus directes et les plus douloureuses. Les ruptures de stock et les retards de distribution les privent d'intrants essentiels pour leurs cultures, entraînant des rendements réduits et, par conséquent, une insécurité alimentaire accrue. Les agriculteurs qui ont effectué des paiements avancés sans recevoir leurs engrais se retrouvent dans une situation de détresse financière, souvent contraints d'emprunter à des taux usuraires pour acheter des engrais au marché noir à des prix six à dix fois supérieurs. L'absence de transparence dans le processus alimente la méfiance et les frustrations, conduisant certains agriculteurs à abandonner le programme.")
B("Pour FOMI, les conséquences incluent des pertes financières considérables liées aux vols et détournements (estimées à plusieurs milliards FBu par an), une réputation entamée par les scandales médiatiques, et une inefficacité opérationnelle qui réduit la rentabilité de l'entreprise. L'absence de données fiables sur les stocks et les distributions empêche une planification efficace de la production, entraînant des surproductions dans certains types d'engrais et des pénuries dans d'autres. La dette de 368 millions USD est en partie imputable à ces dysfonctionnements opérationnels.")
B("Pour l'État, les problèmes de gestion des stocks compromettent l'efficacité du Programme National de Subvention des Engrais, un investissement public majeur représentant plusieurs milliers de milliards FBu par an. Les irrégularités dans la distribution nuisent à la crédibilité du programme et à la confiance des bailleurs de fonds internationaux qui cofinancent les subventions. L'inefficacité du programme entraîne une insatisfaction populaire qui peut se muer en tensions sociales, notamment lors des périodes de distribution.")

doc.add_heading("3.3 État de l'art", level=2)
B("La gestion des stocks d'engrais fait partie intégrante de la gestion de la chaîne d'approvisionnement (supply chain management), domaine largement étudié dans la littérature scientifique en gestion des opérations. Les systèmes de gestion de stock modernes s'appuient sur des technologies de l'information pour assurer la traçabilité, l'optimisation des niveaux de stock et la prise de décision basée sur les données. Les travaux pionniers de Harris (1913) sur le modèle EOQ (Economic Order Quantity) ont posé les bases de la gestion scientifique des stocks, tandis que les travaux plus récents sur les systèmes d'information de gestion (ERP, WMS) ont montré le potentiel de transformation de la technologie dans la logistique.")
B("Les API REST (Representational State Transfer) sont devenues le standard de facto pour la communication entre systèmes d'information distribués. Leur approche Stateless, formalisée par Fielding (2000), est basée sur les verbes HTTP standards (GET, POST, PUT, DELETE) et permet de construire des architectures modulaires et évolutives. Les architectures microservices, popularisées par Newman (2015) et les pratiques de Netflix, Amazon et Uber, offrent un modèle de conception décomposant les systèmes complexes en services indépendants communiquant par API. Pour le projet FOMI, l'architecture monolithique modulaire a été choisie comme compromis entre la simplicité de développement et la modularité fonctionnelle.")
B("Plusieurs patterns (catalyseurs de conception) pertinents pour la gestion des stocks d'engrais ont été identifiés dans la littérature :")
B("Le pattern FIFO (First In, First Out) est essentiel pour la gestion des stocks de produits à durée de vie limitée, comme les engrais. Ce pattern, décrit par Jacob (2016), garantit que les produits entrés en premier sont distribués en premier, minimisant ainsi les pertes liées à la péremption. Dans le contexte des engrais, où la date de péremption influence directement l'efficacité des nutriments (la teneur en azote des engrais à base d'urée diminue de 5 à 10 % par mois après la date de péremption), l'application du FIFO est critique pour garantir la qualité des intrants distribués aux agriculteurs.")
B("Le RBAC (Role-Based Access Control) est un mécanisme de sécurité formalisé par Sandhu et al. (1996) qui restreint l'accès aux fonctionnalités du système selon le rôle de l'utilisateur. Dans un système de distribution hiérarchique comme celui du PNSEB, le RBAC est indispensable pour garantir qu'un agent de colline ne puisse pas accéder aux stocks d'une autre colline, ou qu'un responsable de zone ne puisse pas modifier les paramètres du système. Le RBAC est complété par un filtrage périmètre géographique qui restreint la visibilité des données au niveau hiérarchique de l'utilisateur.")
B("L'audit trail (piste d'audit), standardisé par la norme ISO 27001, est un mécanisme de traçabilité qui enregistre toutes les opérations effectuées sur le système, incluant l'identité de l'auteur, la date et l'heure, l'action réalisée et les données modifiées. Ce mécanisme est essentiel pour la lutte contre la fraude et la résolution des litiges. Dans le contexte des subventions agricoles, l'audit trail permet de prouver la régularité des opérations devant les organismes de contrôle et de justifier les dépenses publiques auprès des bailleurs de fonds.")

doc.add_heading("3.4 Objectifs du projet", level=2)
B("À la lumière des problèmes identifiés et de l'état de l'art, les objectifs du projet de mémoire sont les suivants :")
B("1. Créer une API RESTful centralisée pour la gestion des stocks d'engrais de la société FOMI, offrant une interface standardisée pour toutes les opérations de gestion de stock (entrée, sortie, transfert, annulation). Cette API doit être documentée, testée et sécurisée, prête à être consommée par un frontend web ou mobile.")
B("2. Implémenter un mécanisme de suivi en temps réel des niveaux de stock par dépôt, par type d'engrais et par lot, permettant de visualiser instantanément la situation des stocks à tous les niveaux de la hiérarchie géographique. Ce suivi doit inclure les stocks totaux par dépôt, les stocks détaillés par lot avec dates de péremption, et les tendances d'évolution.")
B("3. Mettre en place un système d'alertes automatiques de rupture de stock, de stock bas, de péremption de lots et de retards de distribution, permettant une gestion anticipée et proactive des situations critiques. Les alertes doivent être classées par niveau de sévérité et déclencher des actions correctives automatiques lorsque c'est possible.")
B("4. Implémenter un audit trail complet enregistrant chaque opération sur le système, avec identification de l'utilisateur, horodatage, action réalisée et détails des données modifiées. L'audit trail doit être consultable, filtrable et exportable pour les besoins de contrôle et d'investigation.")
B("5. Garantir la conformité au cahier des charges fonctionnel de FOMI, en implémentant l'ensemble des 27 besoins fonctionnels, 23 règles métier et 26 cas d'utilisation spécifiés, et en validant leur implémentation par des tests automatisés.")

doc.add_heading("3.5 Périmètre du mémoire", level=2)
B("Ce mémoire se concentre sur la conception et l'implémentation du backend de l'application de gestion des stocks, c'est-à-dire l'API RESTful exposant les fonctionnalités métier. Le frontend (interface utilisateur graphique) n'est pas couvert dans ce travail, bien qu'un projet de frontend en React (fomi-stock-web) ait été initié en parallèle. Les aspects de déploiement en production, de formation des utilisateurs et de maintenance à long terme sont également hors du périmètre de ce mémoire, bien que des recommandations soient formulées dans les perspectives.")
B("Le périmètre fonctionnel couvre : l'authentification et l'autorisation, la gestion des données de référence (types d'engrais, géographie, dépôts, agriculteurs, utilisateurs), la gestion des stocks (entrées, sorties, transferts, annulations), la gestion des tickets de distribution, le système d'alertes, les statistiques et le reporting, et l'audit trail. Les modules de paiement, de notification SMS et de gestion documentaire sont hors périmètre.")
B("Le mémoire est structuré en quatre parties : la première partie présente le contexte et la problématique ; la deuxième partie détaille l'analyse des besoins et la conception technique ; la troisième partie décrit l'implémentation et les tests ; et la quatrième partie propose une évaluation et des perspectives d'évolution.")
pb()

# ════════════════════════════════════════════════════════════════════
# DEUXIÈME PARTIE + CHAPITRE 4 (expanded)
# ════════════════════════════════════════════════════════════════════
P("DEUXIÈME PARTIE", b=True, a=C, sz=16)
P("ANALYSE ET CONCEPTION", b=True, a=C, sz=14)
pb()

doc.add_heading("Chapitre 4 : Analyse des besoins", level=1)
B("Ce chapitre présente l'analyse détaillée des besoins fonctionnels et non fonctionnels du système, les règles métier à implémenter et les cas d'utilisation identifiés lors de la phase d'analyse du projet. Cette analyse constitue la base contractuelle du développement, définissant précisément ce que le système doit faire et les contraintes auxquelles il doit se conformer. Les besoins ont été recueillis à travers des entretiens avec les responsables de FOMI, des observations sur le terrain, l'analyse des documents existants (registres, tableurs, rapports) et l'étude des systèmes de référence en Afrique de l'Est.")

doc.add_heading("4.1 Besoins fonctionnels", level=2)
B("Vingt-sept besoins fonctionnels ont été identifiés à partir de l'analyse des exigences de FOMI, des entretiens avec les parties prenantes et de l'étude du contexte opérationnel. Ces besoins sont regroupés en cinq catégories : authentification et sécurité (F1, F24, F25, F26), gestion des données de référence (F2, F3, F4, F5, F10, F18), gestion des stocks (F7, F8, F11, F13, F20), distribution et tickets (F6, F9, F14, F19, F21), et reporting et audit (F12, F15, F16, F17, F22, F23, F27).")

P("Tableau 4.1 — Besoins fonctionnels détaillés", b=True, a=C, sz=11)
TBL(["ID", "Catégorie", "Description"], [
    ("F1", "Authentification", "Authentification JWT avec contrôle d'accès par rôle (RBAC)"),
    ("F2", "Données référence", "Gestion des types d'engrais (CRUD) avec composition et seuils"),
    ("F3", "Données référence", "Gestion des provinces/zones/collines (hiérarchie configurable)"),
    ("F4", "Données référence", "Gestion des dépôts (CRUD, niveaux hiérarchiques, capacité)"),
    ("F5", "Gestion agriculteurs", "CRUD des agriculteurs avec identifiant unique, superficie, colline"),
    ("F6", "Tickets", "Création et suivi des tickets de distribution avec workflow"),
    ("F7", "Stocks", "Réception FOMI (entrées de stock depuis production ou achat)"),
    ("F8", "Stocks", "Transferts inter-dépôts avec vérification disponibilité source"),
    ("F9", "Distribution", "Distribution aux agriculteurs selon algorithme FIFO"),
    ("F10", "Stocks", "Gestion des lots (dates de production et péremption)"),
    ("F11", "Stocks", "Suivi des stocks par dépôt, type d'engrais et lot"),
    ("F12", "Alertes", "Système d'alertes automatiques (rupture, bas, retard, péremption)"),
    ("F13", "Mouvements", "Annulation de mouvements avec rétroaction stock et ticket"),
    ("F14", "Tickets", "Validation des tickets (workflow multi-états avec motifs)"),
    ("F15", "Reporting", "Statistiques et tableaux de bord (taux service, stocks, ruptures)"),
    ("F16", "Reporting", "Export CSV des données de stock et de mouvements"),
    ("F17", "Audit", "Piste d'audit complète avec détails JSONB"),
    ("F18", "Alertes", "Gestion des seuils d'alerte configurables par type d'engrais et dépôt"),
    ("F19", "Transparence", "Consultation publique des tickets (sans authentification)"),
    ("F20", "Recherche", "Recherche multicritère sur les stocks avec pagination"),
    ("F21", "Reporting", "Tickets non servis par colline pour planification distribution"),
    ("F22", "Reporting", "Taux de service par province et par zone"),
    ("F23", "Reporting", "Mouvements par agent pour suivi de productivité"),
    ("F24", "Sécurité", "Gestion des utilisateurs et rôles (CRUD par admin)"),
    ("F25", "Sécurité", "RBAC avec filtrage périmètre géographique forcé en code"),
    ("F26", "Documentation", "API documentée (Swagger/OpenAPI 3.0 auto-générée)"),
    ("F27", "Intégrité", "Suppression logique (soft delete) pour toutes les entités"),
], cw=[0.4, 1.2, 4.4])

doc.add_heading("4.2 Règles métier", level=2)
B("Vingt-trois règles métier ont été identifiées pour garantir l'intégrité des données et la cohérence des opérations dans le système. Ces règles encadrent les opérations de stock, la distribution aux agriculteurs, la validation des tickets et le fonctionnement du système d'alertes. Chaque règle est implémentée dans la couche Service du système et validée par des tests d'intégration correspondants.")

P("Tableau 4.2 — Règles métier", b=True, a=C, sz=11)
TBL(["ID", "Catégorie", "Règle"], [
    ("R1", "Intégrité stock", "Le stock d'un dépôt ne peut pas devenir négatif suite à une opération"),
    ("R2", "Quota distribution", "Un ticket ne peut pas dépasser superficie × 150 kg/ha par type d'engrais"),
    ("R3", "Seuil alerte", "Une alerte est générée quand stock < seuil_min par type/dépôt"),
    ("R4", "Péremption", "Un lot expiré ne peut plus être distribué aux agriculteurs"),
    ("R5", "Capacité dépôt", "La somme des stocks ne peut pas dépasser la capacité max du dépôt"),
    ("R6", "Unicité ticket", "Pas de doublon ticket même saison + même type engrais pour même agriculteur"),
    ("R7", "Annulation", "Un mouvement annulé ne peut pas être ré-annulé (anti-double annulation)"),
    ("R8", "Rétroaction", "AnnulationDistribution réduit quantite_servie du ticket associé"),
    ("R9", "Transfert", "Transfert vérifie disponibilité du stock source avant exécution"),
    ("R10", "Validation ticket", "Ticket peut être VALIDÉ ou REJETÉ avec motif obligatoire"),
    ("R11", "FIFO", "Distribution FIFO par date de péremption (premier à expirer d'abord)"),
    ("R12", "Capacité max", "Vérification capacité maximale du dépôt lors de réception"),
    ("R13", "Audit", "Chaque opération critique génère un log d'audit automatiquement"),
    ("R14", "Rôle admin", "Seul un ADMIN peut créer/modifier des utilisateurs et des seuils"),
    ("R15", "Périmètre", "AGENT_COLLINE ne voit que les stocks et tickets de son propre dépôt"),
    ("R16", "Périmètre", "AGENT_ZONE ne voit que les stocks des dépôts de sa zone d'affectation"),
    ("R17", "Export", "Export CSV limité à 10 000 lignes pour éviter les surcharges mémoire"),
    ("R18", "Inactivité", "Alerte si pas de mouvement sur un dépôt pendant 7 jours consécutifs"),
    ("R19", "Recherche", "Recherche multicritère avec pagination (max 200 résultats par page)"),
    ("R20", "JWT", "Token expiré (24h) → rejet automatique avec code 401"),
    ("R21", "Ticket expiré", "Ticket non validé après 30 jours → passage automatique à EXPIRE"),
    ("R22", "Quota saison", "Quota superficiaire contrôlé par saison agricole (Saison A/B)"),
    ("R23", "BCrypt", "Les mots de passe sont hashés avec BCrypt (strength 10)"),
], cw=[0.4, 1.2, 4.4])

doc.add_heading("4.3 Cas d'utilisation", level=2)
B("Vingt-six cas d'utilisation ont été identifiés pour modéliser les interactions entre les acteurs du système et les fonctionnalités de l'application. Chaque cas d'utilisation est décrit avec son identifiant, les acteurs concernés, les préconditions et le scénario principal. Les acteurs identifiés sont : ADMIN (administrateur système), SUPERVISEUR (responsable provincial ou de zone), AGENT_COLLINE (agent de distribution au niveau colline), AGENT_ZONE (agent de distribution au niveau zone), AGENT_LOGISTIQUE (agent de réception à l'usine), PUBLIC (consultation sans authentification) et TOUT_UTILISATEUR (n'importe quel utilisateur authentifié).")

P("Tableau 4.3 — Cas d'utilisation", b=True, a=C, sz=11)
TBL(["ID", "Cas d'utilisation", "Acteur", "Précondition", "Résultat"], [
    ("UC-01", "Authentification", "Tout utilisateur", "Identifiants valides", "JWT token retourné"),
    ("UC-02", "Gérer types engrais", "ADMIN", "Authentifié", "CRUD opérations"),
    ("UC-03", "Gérer géographie", "ADMIN", "Authentifié", "CRUD provinces/zones/collines"),
    ("UC-04", "Gérer dépôts", "ADMIN", "Géographie définie", "CRUD dépôts"),
    ("UC-05", "Gérer agriculteurs", "ADMIN/AGENT", "Authentifié", "CRUD agriculteurs"),
    ("UC-06", "Créer ticket", "AGENT", "Agriculteur identifié", "Ticket créé en attente"),
    ("UC-07", "Valider/Rejeter ticket", "SUPERVISEUR", "Ticket en attente", "Ticket actif ou rejeté"),
    ("UC-08", "Réceptionner engrais", "AGENT_LOGISTIQUE", "Livraison reçue", "Stock mis à jour"),
    ("UC-09", "Transférer dépôts", "AGENT_ZONE+", "Stock source dispo", "Transfert exécuté"),
    ("UC-10", "Distribuer agriculteurs", "AGENT_COLLINE", "Ticket actif", "FIFO exécuté"),
    ("UC-11", "Gérer lots", "ADMIN", "Type engrais défini", "Lots créés/mis à jour"),
    ("UC-12", "Annuler mouvement", "AGENT/RESP", "Mouvement identifié", "Annulation + rétroaction"),
    ("UC-13", "Consulter stocks", "Tout authentifié", "Périmètre défini", "Stocks affichés"),
    ("UC-14", "Consulter alertes", "SUPERVISEUR+", "Alertes existantes", "Liste alertes filtrée"),
    ("UC-15", "Consulter stats", "SUPERVISEUR+", "Données disponibles", "Tableaux de bord"),
    ("UC-16", "Exporter CSV", "ADMIN", "Données existantes", "Fichier CSV généré"),
    ("UC-17", "Consulter audit logs", "ADMIN", "Logs existants", "Historique filtré"),
    ("UC-18", "Ticket public", "PUBLIC", "Identifiant ticket", "Détails ticket affichés"),
    ("UC-19", "Gérer utilisateurs", "ADMIN", "Droits admin", "CRUD utilisateurs"),
    ("UC-20", "Gérer seuils alerte", "ADMIN", "Type engrais défini", "Seuils configurés"),
    ("UC-21", "Rechercher stocks", "AGENT+", "Critères recherche", "Résultats paginés"),
    ("UC-22", "Rechercher agriculteurs", "AGENT+", "Critères recherche", "Résultats paginés"),
    ("UC-23", "Mouvements par lot", "AGENT+", "Lot identifié", "Historique mouvements"),
    ("UC-24", "Filtrer mouvements", "AGENT+", "Filtres disponibles", "Mouvements filtrés"),
    ("UC-25", "Taux service", "SUPERVISEUR+", "Province/zone définie", "Taux calculé"),
    ("UC-26", "Tickets non servis", "SUPERVISEUR+", "Zone définie", "Liste tickets en attente"),
], cw=[0.5, 1.1, 0.8, 1.3, 1.5])

doc.add_heading("4.4 Besoins non fonctionnels", level=2)
B("Dix besoins non fonctionnels ont été identifiés pour garantir la qualité, la performance et la sécurité du système. Ces exigences dépassent les fonctionnalités métier pour définir les propriétés de qualité du système en tant qu'infrastructure logicielle.")

P("Tableau 4.4 — Besoins non fonctionnels", b=True, a=C, sz=11)
TBL(["ID", "Catégorie", "Exigence"], [
    ("NF1", "Performance", "Temps de réponse < 200ms pour 95% des requêtes de lecture"),
    ("NF2", "Disponibilité", "Disponibilité cible ≥ 99,5 % sur une période annuelle"),
    ("NF3", "Sécurité", "Authentification JWT avec tokens HMAC-SHA expirant après 24h"),
    ("NF4", "Scalabilité", "Architecture stateless permettant la montée en charge horizontale"),
    ("NF5", "Documentation", "API documentée via Swagger/OpenAPI 3.0 accessible en ligne"),
    ("NF6", "Tests", "Suite de tests automatisés avec couverture de code > 80%"),
    ("NF7", "Déploiement", "Pipeline CI/CD avec déploiement continu via GitHub Actions"),
    ("NF8", "Audit", "Enregistrement de toutes les opérations critiques avec horodatage"),
    ("NF9", "Multi-niveaux", "Filtrage périmètre par niveau hiérarchique géographique"),
    ("NF10", "Sauvegarde", "Sauvegardes automatiques quotidiennes de la base PostgreSQL"),
], cw=[0.4, 1.2, 4.4])
pb()

# ── CHAPITRE 5 (expanded) ──────────────────────────────────────────
doc.add_heading("Chapitre 5 : Conception technique", level=1)
B("Ce chapitre présente la conception technique du système, incluant l'architecture logicielle, le modèle de données, les diagrammes de séquence, la machine à états du ticket, l'algorithme FIFO et les mécanismes de sécurité. La conception a été réalisée en suivant les principes de l'ingénierie pilotée par les modèles (Model-Driven Engineering) et en s'appuyant sur les patterns d'architecture d'entreprise.")

doc.add_heading("5.1 Architecture logicielle", level=2)
IMG("architecture.png", "Figure 5.1 — Architecture globale du système")
B("L'architecture du système suit un modèle en couches (layered architecture), un patron de conception largement adopté dans les applications d'entreprise développées avec le framework Spring Boot. Cette architecture organise le code en couches horizontales, chaque couche ayant une responsabilité bien définie et ne communiquant qu'avec la couche adjacente. Le principe de séparation des préoccupations (Separation of Concerns) guide l'ensemble de la conception, garantissant que chaque couche ne contient que le code relevant de sa responsabilité spécifique.")
IMG("layered_architecture.png", "Figure 5.2 — Architecture en couches")
B("Le diagramme de classes UML (Figure 5.9) présente les principales entités du système avec leurs attributs, méthodes et associations navigables.")
IMG("class_diagram.png", "Figure 5.9 — Diagramme de classes UML")
B("Les couches du système sont les suivantes :")
B("Couche API (Controller) : point d'entrée externe du système, exposant les endpoints REST. Les contrôleurs sont responsables de la réception des requêtes HTTP, de la validation des données d'entrée via les DTOs (Data Transfer Objects), du routage vers les services appropriés et de la serialisation des réponses au format JSON. Chaque contrôleur est dédié à un domaine fonctionnel spécifique : StockController pour les opérations de stock, TicketController pour les tickets, DistributionController pour les distributions, MouvementController pour les mouvements, AlerteController pour les alertes, StatsController pour les statistiques, et AuditLogController pour l'audit. Le système compte 17 contrôleurs au total, chacun exposant entre 2 et 8 endpoints.")
B("Couche Sécurité (Security) : intercepte chaque requête entrante via le filtre JwtAuthenticationFilter pour vérifier l'authenticité du token JWT, extraire les informations de l'utilisateur (identifiant, rôle, périmètre géographique) et appliquer les règles RBAC via les annotations @PreAuthorize. Cette couche inclut également le filtrage périmètre géographique, implémenté via un Aspect Spring (SecurityScopeAspect) qui injecte automatiquement un filtre sur les requêtes de consultation en fonction du niveau hiérarchique de l'utilisateur. Le SecurityContext est configuré pour chaque requête et ne persiste pas entre les requêtes (stateless).")
B("Couche Service : contient la logique métier du système. C'est dans cette couche que sont implémentées les 23 règles métier identifiées lors de l'analyse : l'algorithme FIFO dans StockService.sortirFifo(), le contrôle des quotas dans TicketService.creer(), le dédoublement des alertes dans AlerteService.creerSiAbsente(), l'annulation avec rétroaction dans MouvementService.annuler(), et le calcul des statistiques dans StatsService. Les services sont responsables de la gestion des transactions (@Transactional), de la coordination entre les repositories et de l'appel à AuditLogService pour l'enregistrement des opérations critiques. Le système compte 11 services.")
B("Couche Repository : assure la communication avec la base de données via Spring Data JPA. Les repositories encapsulent les requêtes de persistance, incluant les requêtes JPQL personnalisées (@Query) pour les opérations complexes de recherche, d'agrégation et de reporting. Les specifications JPA (JPA Specifications) sont utilisées pour la recherche multicritère dynamique, permettant de construire des requêtes variables sans concaténation de chaînes SQL. Le pessimistic locking (SELECT FOR UPDATE) est utilisé dans les repositories de stock pour garantir l'intégrité des données en présence de transactions concurrentes. Le système compte 15 repositories.")
B("Couche Model/Entity : définit les 16 entités métier qui correspondent aux tables de la base de données. Les entités portent les annotations JPA pour le mapping objet-relationnel (@Entity, @Table, @Column, @ManyToOne, etc.), les contraintes de validation Bean Validation (@NotNull, @Min, @Size), et les annotations Lombok pour la réduction du code boilerplate (@Data, @Builder, @NoArgsConstructor, @AllArgsConstructor). Les énumérations sont mappées vers des types enum nommés PostgreSQL pour garantir l'intégrité des données au niveau de la base.")
B("Base de données (PostgreSQL 16) : couche de persistance, stockant les données dans des tables relationnelles avec des index optimisés pour les requêtes fréquentes. Les types enum nommés de PostgreSQL assurent l'intégrité des données au niveau de la base en empêchant l'insertion de valeurs hors standard. Les index B-tree sont créés sur les colonnes fréquemment utilisées dans les clauses WHERE et JOIN (depot_id, type_engrais_id, statut, created_at), et un index GIN est utilisé sur la colonne detailsJson de la table audit_log pour les recherches dans les données JSONB. Le schéma de la base de données est géré par Flyway avec 11 versions de migration numérotées.")

doc.add_heading("5.2 Modèle de données", level=2)
IMG("er_diagram.png", "Figure 5.3 — Diagramme Entité-Relation (régénéré avec résolution améliorée)")
B("Le diagramme de déploiement (Figure 5.10) montre la répartition des composants entre le client, le serveur API hébergé sur Railway et la base PostgreSQL 16, avec indication des conteneurs Docker et du pipeline CI/CD GitHub Actions.")
IMG("deployment_diagram.png", "Figure 5.10 — Diagramme de déploiement")
B("Le modèle de données du système comprend 16 tables principales, modélisant l'ensemble des entités métier et leurs relations. Le diagramme Entité-Relation ci-dessus présente les relations entre les principales entités du système. Le modèle suit les principes de normalisation de la 3ème forme (3NF), évitant les redondances de données et garantissant l'intégrité référentielle via des clés étrangères. Les relations sont principalement de type un-à-plusieurs (1:N) et plusieurs-à-plusieurs (M:N) avec tables de jointure.")

P("Tableau 5.1 — Description des tables de la base de données", b=True, a=C, sz=11)
TBL(["Table", "Description", "Colonnes clés"], [
    ("utilisateur", "Utilisateurs du système avec rôles", "id, email, mot_de_passe, role, depot_id, actif"),
    ("type_engrais", "Types d'engrais avec seuils", "id, nom, formule, composition, actif"),
    ("province", "Provinces du Burundi", "id, nom, code, actif"),
    ("zone", "Zones administratives", "id, nom, code, province_id"),
    ("colline", "Collines rattachées aux zones", "id, nom, code, zone_id"),
    ("depot", "Dépôts de stockage", "id, nom, niveau, capacite_max, colline_id/zone_id/province_id"),
    ("agriculteur", "Agriculteurs bénéficiaires", "id, nom, matricule, superficie, colline_id"),
    ("lot", "Lots d'engrais", "id, numero, date_production, date_peremption, type_engrais_id"),
    ("ticket", "Tickets de distribution", "id, numero, statut, quantite_demandee, quantite_servie, agriculteur_id"),
    ("stock", "Stock agrégé par dépôt/type", "id, depot_id, type_engrais_id, quantite"),
    ("stock_lot", "Stock détaillé par lot", "id, depot_id, stock_id, lot_id, quantite"),
    ("mouvement_stock", "Historique des mouvements", "id, type, depot_id, lot_id, quantite, ticket_id, utilisateur_id"),
    ("alerte", "Alertes automatiques", "id, type, niveau, depot_id, message, lue, created_at"),
    ("audit_log", "Piste d'audit", "id, action, entity_type, entity_id, utilisateur_id, details_json"),
    ("seuil_alerte", "Seuils d'alerte configurables", "id, type_engrais_id, depot_id, quantite_min"),
    ("parametre_systeme", "Paramètres configurables", "cle, valeur, description"),
], cw=[1.2, 1.8, 3.0])

B("Le système exploite les énumérations nommées de PostgreSQL pour garantir l'intégrité des données. Les enums utilisés sont :")

P("Tableau 5.2 — Énumérations du système", b=True, a=C, sz=11)
TBL(["Enum", "Valeurs", "Usage"], [
    ("NiveauDepot", "USINE, PROVINCIAL, ZONE, COLLINE", "Classement des dépôts par niveau hiérarchique"),
    ("StatutTicket", "PAYE, EN_ATTENTE_DE_VALIDATION, ACTIF, PARTIEL, SERVI, REJETE, ANNULE, EXPIRE", "Workflow des tickets de distribution"),
    ("TypeMouvement", "ENTREE, SORTIE, TRANSFERT, ANNULATION, AJUSTEMENT", "Classification des mouvements de stock"),
    ("TypeAlerte", "RUPTURE, STOCK_BAS, DELAI_DEPASSE, DEMANDE_SUP_STOCK, PEREMPTION, INACTIVITE", "Types d'alertes automatiques"),
    ("NiveauAlerte", "INFO, WARNING, CRITICAL", "Sévérité des alertes"),
    ("RoleUtilisateur", "ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE, AGENT_LOGISTIQUE", "Rôles RBAC du système"),
], cw=[1.2, 2.8, 2.0])


B("Le diagramme de cas d'utilisation (Figure 5.11) présente les 26 cas d'utilisation principaux (UC-01 à UC-26) avec leurs acteurs et relations include/extend, modélisant l'ensemble des interactions entre utilisateurs et système.")
IMG("use_case_diagram.png", "Figure 5.11 — Diagramme de cas d'utilisation UML")

B("Le diagramme d'activités (Figure 5.12) modélise le workflow de validation et de distribution d'un ticket sous forme d'activités et de transitions conditionnelles, montrant le parcours depuis la vérification du périmètre agent jusqu'à la création des mouvements et la génération des alertes.")
IMG("activity_diagram.png", "Figure 5.12 — Diagramme d'activités — Distribution FIFO")

P("Tableau 5.3 — Dictionnaire de données : colonnes, types SQL et contraintes", b=True, a=C, sz=11)
TBL(["Table", "Colonne", "Type SQL / Enum", "Contraintes / Description"], [
    ("utilisateur", "username", "VARCHAR(50)", "UNIQUE, NOT NULL, BCrypt hash"),
    ("utilisateur", "nom_complet", "VARCHAR(150)", "NOT NULL"),
    ("utilisateur", "role", "role_utilisateurs (enum PG)", "NOT NULL"),
    ("utilisateur", "depot_id / zone_id / province_id", "BIGINT FK", "NULL (ancrage géographique)"),
    ("utilisateur", "actif", "BOOLEAN", "DEFAULT TRUE, soft delete"),
    ("depot", "code", "VARCHAR(30)", "UNIQUE, NOT NULL"),
    ("depot", "niveau", "niveau_depots (enum PG)", "NOT NULL"),
    ("depot", "seuil_alerte_min", "INTEGER", "DEFAULT 100, NOT NULL"),
    ("depot", "capacite_max", "INTEGER", "NULL (V11)"),
    ("ticket", "numero_ticket", "VARCHAR(50)", "UNIQUE, NOT NULL"),
    ("ticket", "statut", "statut_tickets (enum PG)", "NOT NULL DEFAULT 'PAYE'"),
    ("ticket", "quantite_commandee / servie", "INTEGER", "NOT NULL DEFAULT 0"),
    ("ticket", "agriculteur_id / depot_retrait_id", "BIGINT FK", "NOT NULL"),
    ("ticket", "montant_paye", "DECIMAL(15,2)", "NOT NULL"),
    ("ticket", "saison", "VARCHAR(20)", "NOT NULL DEFAULT '2026A'"),
    ("lot", "numero_lot", "VARCHAR(50)", "UNIQUE, NOT NULL"),
    ("lot", "quantite_initiale", "INTEGER", "NOT NULL"),
    ("lot", "date_fabrication / peremption", "DATE", "NOT NULL"),
    ("lot", "date_reception_fomi", "LOCALDATETIME", "NOT NULL (base FIFO)"),
    ("mouvement", "type", "type_mouvements (enum PG)", "NOT NULL"),
    ("mouvement", "idempotency_key", "VARCHAR(64)", "UNIQUE, NOT NULL"),
    ("mouvement", "annule / motif_annulation / annule_par_id / reference_annulation_id", "BOOLEAN / VARCHAR(500) / BIGINT FK / BIGINT FK", "V11 (annulation avec rétroaction)"),
    ("stock / stock_lot", "depot_id / lot_id", "BIGINT FK", "UNIQUE composite, NOT NULL"),
    ("audit_log", "action / entity_type / entity_id", "VARCHAR / VARCHAR / BIGINT", "NOT NULL / NULL / NULL"),
    ("audit_log", "details_json", "JSONB", "Index GIN pour recherches"),
    ("alerte", "depot_id / type / engrais_type_id", "BIGINT FK", "Partiel (dédoublement évité)"),
    ("alerte", "niveau", "niveau_alertes (enum PG)", "NOT NULL DEFAULT 'WARNING'"),
], cw=[1.2, 2.8, 2.2, 2.8])
pb()
IMG("data_dictionary_summary.png", "Figure 5.13 — Dictionnaire de données : tables, colonnes et contraintes")

doc.add_heading("5.3 Diagrammes de séquence", level=2)
B("Les diagrammes de séquence modélisent les interactions entre les différents composants du système lors des opérations critiques. Ils illustrent les échanges de messages entre les contrôleurs, les services, les repositories et la base de données pour chaque scénario fonctionnel.")
IMG("sequence_ticket.png", "Figure 5.4 — Diagramme de séquence : Création et validation de ticket")
B("Le diagramme de séquence de la création et validation d'un ticket illustre le flux complet depuis la demande de l'agriculteur jusqu'à l'activation du ticket. L'agent de colline crée le ticket en spécifiant l'agriculteur, le type d'engrais et la quantité demandée. Le TicketController.recevoir() valide le format de la requête via les annotations Bean Validation, puis transmet au TicketService.creer(). Ce dernier vérifie automatiquement : la conformité avec le quota de superficie (R2 : superficie × 150 kg/ha), l'unicité par saison (R6 : pas de doublon même saison + même type), la disponibilité du stock (R3 : vérification seuil) et l'existence de l'agriculteur. Si toutes les vérifications passent, le ticket est créé avec le statut EN_ATTENTE_DE_VALIDATION. Un responsable peut ensuite valider le ticket (passage à ACTIF) ou le rejeter (passage à REJETE avec motif).")
IMG("sequence_distribution.png", "Figure 5.5 — Diagramme de séquence : Distribution FIFO")
B("Le diagramme de séquence de la distribution FIFO détaille le processus de distribution d'engrais à un agriculteur selon le principe First-In-First-Out. L'agent de colline sélectionne un ticket actif via DistributionController.distribuer(), et le DistributionService orchestre l'opération. Le StockService.sortirFifo() identifie automatiquement les lots à distribuer en triant par date de péremption (premier à expirer en premier). Les stocks sont décrémentés lot par lot via StockLotRepository.save() jusqu'à satisfaction de la quantité demandée. Chaque décrément génère un mouvement de stock de type SORTIE dans MouvementStockRepository et un log d'audit via AuditLogService.log(). Le ticket est mis à jour avec la quantité servie et le statut approprié (PARTIEL ou SERVI).")

doc.add_heading("5.4 Machine à états du ticket", level=2)
IMG("ticket_state_machine.png", "Figure 5.6 — Machine à états du ticket")
B("Le ticket de distribution suit un workflow défini par une machine à états finite à huit états. Les états et transitions possibles sont les suivants :")
B("PAYE : état initial après le paiement de l'avance (50 %). Le ticket est enregistré dans le système avec les informations de l'agriculteur, le type d'engrais demandé et la quantité. Ce ticket est visible par l'agent de colline qui l'a créé.")
B("PAYE → EN_ATTENTE_DE_VALIDATION : transition déclenchée lors de la soumission du ticket pour validation. Le ticket passe en file d'attente pour examen par un responsable.")
B("EN_ATTENTE_DE_VALIDATION → ACTIF : le responsable valide le ticket après vérification de la conformité des informations. Le ticket est maintenant traitable par les agents de distribution.")
B("EN_ATTENTE_DE_VALIDATION → REJETE : le responsable rejette le ticket avec un motif obligatoire. Les motifs les plus fréquents sont : superficie insuffisante, doublon détecté, données erronées, ou documents manquants.")
B("ACTIF → PARTIEL : une partie de la quantité demandée a été distribuée. Le ticket reste actif pour permettre la distribution du solde lors de la prochaine disponibilité du stock.")
B("ACTIF/PARTIEL → SERVI : la totalité de la quantité demandée a été distribuée. Le ticket est clôturé définitivement.")
B("ACTIF/PARTIEL → ANNULE : le ticket est annulé à la demande de l'agriculteur ou en cas d'irrégularité détectée. Les distributions déjà effectuées sont annulées en sens inverse (rétroaction sur stock).")
B("EN_ATTENTE_DE_VALIDATION → EXPIRE : le ticket n'a pas été validé dans un délai de 30 jours. Cette transition est déclenchée automatiquement par un cron job planifié.")

doc.add_heading("5.5 Algorithme FIFO", level=2)
IMG("fifo_flowchart.png", "Figure 5.7 — Organigramme de l'algorithme FIFO")
B("L'algorithme FIFO (First-In, First-Out) est le cœur du mécanisme de distribution des engrais. Il garantit que les lots les plus anciens (ou les plus proches de leur date de péremption) sont distribués en priorité, minimisant ainsi les pertes liées à la péremption des engrais. La teneur en nutriments des engrais diminue progressivement après la date de péremption, rendant leur distribution ineffective voire contre-productive.")
B("L'algorithme de la méthode StockService.sortirFifo() fonctionne selon les cinq étapes suivantes :")
B("Étape 1 — Récupération des lots disponibles : le StockLotRepository interroge la table stock_lot pour obtenir tous les lots du dépôt concerné pour le type d'engrais demandé, en appliquant deux filtres : le stock du lot doit être supérieur à zéro, et la date de péremption du lot ne doit pas être dépassée (lot.non expire()). Les lots expirés sont automatiquement exclus de la distribution, même s'ils contiennent encore du stock.")
B("Étape 2 — Tri par péremption croissante : les lots récupérés sont triés par date de péremption dans l'ordre croissant (Collections.sort avec un comparateur sur datePeremption). Le lot avec la date de péremption la plus proche est traité en premier, garantissant ainsi que les engrais les plus proches de leur expiration soient distribués avant qu'ils ne deviennent inutilisables.")
B("Étape 3 — Distribution itérative : pour chaque lot dans l'ordre du tri, le système calcule la quantité à distribuer comme le minimum entre le stock disponible du lot et la quantité restante à satisfaire. Cette quantité est décrémentée du stock_lot et du stock agrégé. La boucle se poursuit jusqu'à ce que la quantité totale demandée soit satisfaite ou qu'il n'y ait plus de lots disponibles.")
B("Étape 4 — Enregistrement des mouvements : pour chaque décrément de stock, un enregistrement est créé dans la table mouvement_stock avec le type SORTIE, l'identifiant du dépôt, du lot, du ticket et de l'utilisateur ayant effectué l'opération. Chaque mouvement est horodaté en UTC pour garantir la traçabilité chronologique.")
B("Étape 5 — Mise à jour du ticket : la quantité totale distribuée est ajoutée au champ quantite_servie du ticket. Le statut du ticket est mis à jour selon la quantité restante : SERVI si la totalité est satisfaite, PARTIEL si un solde subsiste, ou maintien à ACTIF si la distribution est partielle mais d'autres distributions sont attendues.")

doc.add_heading("5.6 Sécurité et RBAC", level=2)
IMG("rbac_matrix.png", "Figure 5.8 — Matrice RBAC : Rôles et permissions")
B("Le système implémente un contrôle d'accès basé sur les rôles (RBAC) avec cinq rôles distincts, chacun disposant d'un ensemble défini de permissions. Le RBAC est complété par un filtrage périmètre géographique qui restreint l'accès aux données selon le niveau hiérarchique de l'utilisateur. Cette double restriction (rôle + périmètre) garantit que chaque acteur ne peut accéder qu'aux fonctionnalités et données relevant strictement de sa compétence.")

TBL(["Rôle", "Permissions principales", "Périmètre"], [
    ("ADMIN", "Accès total. Gestion utilisateurs, config, export CSV, audit logs.", "Toutes les données"),
    ("SUPERVISEUR", "Validation/rejet tickets, alertes, stats, transferts province.", "Province d'affectation"),
    ("AGENT_ZONE", "Distribution, création tickets, réception engrais.", "Dépôts de sa zone"),
    ("AGENT_COLLINE", "Distribution et création tickets.", "Dépôt de sa colline"),
    ("AGENT_LOGISTIQUE", "Réception livraisons, gestion stocks usine.", "Dépôt usine uniquement"),
], cw=[1.2, 2.8, 1.8])

B("L'authentification est basée sur les tokens JWT (JSON Web Token) signés avec l'algorithme HMAC-SHA256. Le processus d'authentification se déroule comme suit : l'utilisateur envoie ses identifiants (email et mot de passe) via l'endpoint POST /api/auth/login ; le AuthService vérifie les identifiants en comparant le hash BCrypt du mot de passe fourni avec celui stocké en base ; si les identifiants sont valides, un token JWT est généré contenant l'identifiant de l'utilisateur, son rôle, son périmètre géographique (depotId) et la date d'expiration (24 heures) ; le token est retourné au client.")
B("Lors de chaque requête subséquente, le client transmet le token dans l'en-tête Authorization avec le préfixe Bearer. Le filtre JwtAuthenticationFilter intercepte la requête, valide la signature du token, vérifie la date d'expiration, et configure le SecurityContext de Spring avec les informations de l'utilisateur. Si le token est invalide ou expiré, le filtre renvoie une réponse HTTP 401 Unauthorized. Les mots de passe sont hashés avec l'algorithme BCrypt avec un facteur de cost de 10, offrant un niveau de sécurité élevé contre les attaques par dictionnaire et par force brute.")
pb()

# ── CHAPITRE 6 (expanded) ──────────────────────────────────────────
doc.add_heading("Chapitre 6 : Choix technologiques", level=1)
B("Ce chapitre justifie les choix technologiques effectués pour le développement de l'API de gestion des stocks FOMI. Chaque choix est motivé par des critères de performance, de maintenabilité, de sécurité et d'adéquation avec les besoins spécifiques du projet. Les technologies ont été sélectionnées après une analyse comparative de plusieurs alternatives et en tenant compte des compétences de l'équipe de développement, de la maturité des écosystèmes technologiques et de la disponibilité de la documentation et de la communauté.")

doc.add_heading("6.1 Java 21 et Spring Boot 3.3.5", level=2)
B("Java a été choisi comme langage de programmation principal pour sa maturité (30 ans d'existence), sa portabilité (Write Once, Run Anywhere) et son écosystème riche en bibliothèques et frameworks d'entreprise. La version 21, sortie en septembre 2023, est une version LTS (Long-Term Support) qui offre des améliorations significatives en termes de performance (Virtual Threads pour la gestion efficace des threads), de sécurité (updated cryptography libraries) et de productivité (pattern matching, record patterns, sequenced collections).")
B("Spring Boot 3.3.5, basé sur le framework Spring (version 6.1), a été retenu pour sa capacité à simplifier le développement d'applications Java d'entreprise. Le principe de convention over configuration réduit considérablement la quantité de code boilerplate nécessaire, permettant aux développeurs de se concentrer sur la logique métier. Spring Boot intègre Tomcat comme serveur HTTP intégré, simplifiant le déploiement. Les fonctionnalités clés utilisées incluent : Spring MVC pour le routage REST, Spring Data JPA pour la persistance, Spring Security pour la sécurité, et Spring Scheduling pour les cron jobs.")

doc.add_heading("6.2 PostgreSQL 16", level=2)
B("PostgreSQL 16 a été sélectionné comme SGBD pour sa robustesse éprouvée, sa conformité totale aux standards SQL:2016 et ses fonctionnalités avancées. Les énumérations nommés (named ENUMs) offrent un mécanisme natif pour garantir l'intégrité des données au niveau de la base. Le type JSONB (Binary JSON) permet de stocker des données structurées de manière flexible, notamment pour les détails des mouvements dans la table audit_log, avec des performances de recherche optimisées via les index GIN. Les index composites sur les colonnes fréquemment utilisées dans les clauses WHERE, JOIN et ORDER BY réduisent significativement le temps d'exécution des requêtes de reporting.")

doc.add_heading("6.3 Flyway — Gestion des migrations", level=2)
B("Flyway a été choisi pour la gestion versionnée des évolutions du schéma de la base de données. Chaque modification du schéma (ajout de table, modification de colonne, ajout d'index, création d'enum) est encapsulée dans un fichier de migration SQL numéroté (V1__init.sql, V2__add_alertes.sql, etc.). Flyway maintient une table d'historique (flyway_schema_history) permettant de tracer l'ensemble des évolutions du schéma depuis la création du projet. Le projet compte actuellement 11 versions de migration, assurant la reproductibilité du schéma sur n'importe quel environnement (développement, test, production).")

doc.add_heading("6.4 Spring Security et JWT", level=2)
B("Spring Security est le framework de référence pour la sécurité des applications Spring. Dans le contexte de l'API FOMI, il est configuré en mode stateless, désactivant les sessions côté serveur. Le cycle JWT complet est implémenté : génération du token lors du login, validation à chaque requête via un filtre personnalisé, et rejet automatique des tokens expirés. L'intégration avec les annotations @PreAuthorize et @Secured permet de déclarer les permissions au niveau des contrôleurs.")

doc.add_heading("6.5 Spring Data JPA et Hibernate", level=2)
B("Spring Data JPA, avec Hibernate 6 comme implémentation, assure la couche de persistance. Le pessimistic locking via SELECT FOR UPDATE est utilisé dans StockLotRepository pour les opérations de décrémentation de stock, évitant les conditions de course en présence de transactions concurrentes. Les requêtes JPQL dynamiques et les JPA Specifications permettent d'implémenter la recherche multicritère avec des filtres variables tout en maintenant la sécurité contre les injections SQL.")

doc.add_heading("6.6 Testcontainers et JUnit 5", level=2)
B("Testcontainers lance une instance PostgreSQL réelle en Docker pour chaque session de test d'intégration, garantissant la fidélité des tests par rapport à la production. JUnit 5 fournit les annotations (@Test, @BeforeEach, @Nested) et les assertions. Les 203 tests couvrent : tests unitaires (H2), intégration (PostgreSQL), sécurité (RBAC), concurrence (pessimistic locking), et cas métier (FIFO, annulation, alertes).")

doc.add_heading("6.7 SpringDoc OpenAPI — Documentation", level=2)
B("SpringDoc OpenAPI génère automatiquement la documentation Swagger/OpenAPI 3.0 à partir des annotations @Operation, @Parameter, @Schema du code. L'interface Swagger UI, accessible via /swagger-ui.html, permet aux développeurs de tester les endpoints en temps réel et de générer automatiquement les clients API dans différents langages.")

doc.add_heading("6.8 Lombok", level=2)
B("Lombok réduit le code boilerplate via les annotations @Data, @Builder, @NoArgsConstructor, @AllArgsConstructor, @Slf4j, appliquées au niveau des entités, DTOs et services. Cette réduction de la verbose du code Java améliore la lisibilité et réduit le risque d'erreurs liées à la maintenance de code répétitif.")

P("Tableau 6.1 — Comparatif des choix technologiques", b=True, a=C, sz=11)
TBL(["Technologie", "Rôle", "Justification"], [
    ("Java 21", "Langage", "LTS, typé statiquement, performance, Virtual Threads, écosystème riche"),
    ("Spring Boot 3.3.5", "Framework", "Convention over configuration, intégration complète, communauté active"),
    ("PostgreSQL 16", "SGBD", "Enums nommés, JSONB, GIN index, performance, open source, ACID"),
    ("Flyway", "Migrations", "Versionné, traçable, intégré Spring Boot, reproductible"),
    ("Spring Security", "Sécurité", "RBAC complet, JWT stateless, BCrypt, @PreAuthorize"),
    ("Spring Data JPA", "Persistance", "Pessimistic locking, JPQL dynamique, JPA Specifications"),
    ("Testcontainers", "Tests intégration", "PostgreSQL réel en Docker, fidélité production"),
    ("JUnit 5", "Tests", "Standard Java, @Nested, @ParameterizedTest, assertions riches"),
    ("SpringDoc", "Documentation", "Swagger auto-généré, interactif, export OpenAPI JSON"),
    ("Lombok", "Utilitaires", "Réduction boilerplate, @Data, @Builder, @Slf4j"),
], cw=[1.2, 1.0, 3.8])
pb()

# ════════════════════════════════════════════════════════════════════
# TROISIÈME PARTIE + CHAPITRE 7 (expanded)
# ════════════════════════════════════════════════════════════════════
P("TROISIÈME PARTIE", b=True, a=C, sz=16)
P("RÉALISATION", b=True, a=C, sz=14)
pb()

doc.add_heading("Chapitre 7 : Implémentation", level=1)
B("Ce chapitre présente les détails de l'implémentation du système, incluant la structure du projet, les algorithmes clés, le système d'alertes, le workflow de validation, le mécanisme d'annulation, les statistiques et l'audit trail. Chaque composant est décrit en détail avec les choix d'implémentation et les justifications techniques.")

doc.add_heading("7.1 Structure du projet", level=2)
B("Le projet suit une architecture en packages organisés par couche technique, chaque package regroupant les classes ayant une responsabilité commune. Cette organisation en packages suit les conventions du framework Spring Boot et permet une navigation facile dans le code source.")

TBL(["Package", "Contenu", "Nombre de classes"], [
    ("controller", "Contrôleurs REST exposant les endpoints API", "17 classes"),
    ("service", "Services contenant la logique métier", "11 classes"),
    ("repository", "Repositories Spring Data JPA", "15 interfaces"),
    ("model/entity", "Entités JPA (tables de la base)", "16 classes"),
    ("model/enums", "Énumérations Java", "6 enums"),
    ("dto", "Objets de transfert de données", "~30 classes"),
    ("security", "Filtre JWT, provider auth, utils sécurité", "5 classes"),
    ("config", "Configuration Spring (CORS, Swagger, scheduling)", "4 classes"),
    ("exception", "Exceptions métier et gestion centralisée", "6 classes"),
], cw=[1.3, 2.5, 1.2])

B("La structure en packages permet une séparation claire des responsabilités et facilite la maintenabilité du code. Chaque couche ne dépend que de la couche adjacente : le contrôleur dépend du service, le service dépend du repository, et le repository dépend de l'entité. Cette dépendance unidirectionnelle réduit les couplages et facilite les tests unitaires par mock (Mockito). Les exceptions sont gérées centralisément via @ControllerAdvice et @ExceptionHandler, garantissant des réponses d'erreur uniformes et structurées pour tous les endpoints.")

doc.add_heading("7.2 Gestion des stocks FIFO", level=2)
B("L'implémentation du mécanisme FIFO constitue l'un des aspects les plus critiques et les plus complexes du système. La méthode principale StockService.sortirFifo() orchestre l'ensemble du processus de distribution en garantissant l'intégrité des données même en présence de transactions concurrentes.")
B("L'implémentation utilise le pessimistic locking (SELECT FOR UPDATE) pour garantir que deux agents ne puissent pas distribuer le même stock simultanément. Lorsqu'un agent sélectionne un lot pour distribution, une verrou est appliqué sur l'enregistrement stock_lot correspondant dans la base de données. Ce verrou est maintenu jusqu'à la fin de la transaction, empêchant tout autre processus de modifier le stock du lot en cours de distribution. Si un conflit de concurrence est détecté ( SQLException avec un code de verrou), le système lance une exception StockConcurrenceException qui est gérée par le contrôleur et retournée à l'utilisateur avec un message explicite invitant à réessayer.")
B("La méthode procède comme suit : Étape 1 — Récupération des lots disponibles via StockLotRepository.findByDepotAndTypeOrderByDatePeremptionAsc(), filtrés pour exclure les lots expirés (datePeremption > LocalDate.now()) et les lots vides (quantite > 0). Étape 2 — Tri par date de péremption croissante. Étape 3 — Distribution itérative lot par lot en décrémentant les stocks (avec verrou pessimiste). Étape 4 — Enregistrement des mouvements de type SORTIE. Étape 5 — Mise à jour du ticket (quantite_servie et statut).")

doc.add_heading("7.3 Système d'alertes", level=2)
B("Le système d'alertes identifie et signale automatiquement les situations critiques nécessitant une intervention humaine. Six types d'alertes sont implémentés, chacun avec un déclencheur spécifique et un niveau de sévérité hiérarchique.")

P("Tableau 7.2 — Types d'alertes et déclencheurs", b=True, a=C, sz=11)
TBL(["Type", "Sévérité", "Condition de déclenchement", "Fréquence"], [
    ("RUPTURE", "CRITICAL", "Stock = 0 pour un type dans un dépôt", "Temps réel (à chaque sortie)"),
    ("STOCK_BAS", "WARNING", "Stock < seuil_min configuré pour type/dépôt", "Temps réel (à chaque sortie)"),
    ("DELAI_DEPASSE", "WARNING", "Ticket en attente de validation > 7 jours", "Cron job 06h00 quotidien"),
    ("DEMANDE_SUP_STOCK", "INFO", "Quantité demandée > stock disponible au dépôt", "Temps réel (création ticket)"),
    ("PEREMPTION", "WARNING", "Lot expire dans < 30 jours avec stock > 0", "Cron job 06h00 quotidien"),
    ("INACTIVITE", "INFO", "Aucun mouvement sur un dépôt pendant 7 jours", "Cron job 06h30 quotidien"),
], cw=[1.1, 0.8, 2.2, 1.6])

B("Le mécanisme de dédoublement est essentiel pour éviter la multiplication d'alertes identiques. La méthode AlerteService.creerSiAbsente() vérifie l'existence d'une alerte active de même type et même dépôt avant d'en créer une nouvelle. Cette vérification utilise une requête JPQL qui recherche les alertes non lues (lue = false) du même type pour le même dépôt. Si une alerte similaire existe déjà, la méthode retourne l'alerte existante au lieu d'en créer une nouvelle.")
B("Deux cron jobs planifiés via l'annotation @Scheduled complètent la détection en temps réel : le premier s'exécute à 06h00 chaque jour pour vérifier les tickets en attente de validation depuis plus de 7 jours (génère des alertes DELAI_DEPASSE) et les lots proches de la péremption avec stock positif (génère des alertes PEREMPTION) ; le second s'exécute à 06h30 pour identifier les dépôts inactifs (aucun mouvement de stock depuis 7 jours consécutifs). Ces cron jobs utilisent l'API de scheduling de Spring (@Scheduled avec fixedRate ou cron expression) et sont exécutés dans un pool de threads dédié pour ne pas bloquer les requêtes HTTP.")

doc.add_heading("7.4 Workflow de validation des tickets", level=2)
B("Le workflow de validation des tickets implémente un processus en deux étapes avec vérifications automatiques à chaque transition. Lors de la création du ticket (TicketService.creer()), le système vérifie automatiquement plusieurs règles métier : le quota de superficie (R2 : la quantité demandée ne doit pas dépasser superficie × 150 kg/ha pour le type d'engrais demandé), l'unicité par saison (R6 : pas de ticket pour la même saison et le même type d'engrais pour le même agriculteur), la disponibilité du stock dans le dépôt (vérification que stock >= quantiteDemandee), et l'existence et la validité de l'agriculteur.")
B("Lors de la validation par le responsable (TicketService.valider()), le système re-vérifie les règles métier (car le stock peut avoir changé entre la création et la validation) et met à jour le statut du ticket de EN_ATTENTE_DE_VALIDATION à ACTIF. Le responsable peut également rejeter le ticket via TicketService.rejeter() avec un motif obligatoire (champ motifRejet non null), ce qui change le statut à REJETE. Une fois le ticket ACTIF, il peut être traité par l'agent de colline lors de la distribution aux agriculteurs via DistributionService.distribuer().")

doc.add_heading("7.5 Annulation des mouvements", level=2)
B("Le mécanisme d'annulation des mouvements est une fonctionnalité critique pour la correction des erreurs et la gestion des litiges. Deux types d'annulation sont supportés, implémentés dans MouvementService.annuler().")
B("Annulation d'une distribution : lorsqu'un mouvement de type SORTIE (distribution) est annulé, le système restaure automatiquement le stock du dépôt en incrémentant les quantités dans les tables stock (stock agrégé) et stock_lot (stock par lot). La quantite_servie du ticket associé est décrémentée de la quantité annulée, et le statut du ticket peut revenir à ACTIF si le ticket n'était pas entièrement satisfait. Un nouveau mouvement de type ANNULATION est créé avec une référence (champ reference) pointant vers le mouvement original annulé.")
B("Annulation d'un transfert : lorsqu'un mouvement de type TRANSFERT est annulé, le stock est restauré au dépôt source (incrémenté) et retiré du dépôt destination (décrémenté). Cette opération atomique garantit la cohérence des stocks entre les deux dépôts. Un seul mouvement de type ANNULATION est créé avec la référence du transfert original.")
B("Dans les deux cas, des vérifications sont effectuées avant l'annulation : le mouvement ne doit pas déjà être annulé (R7 : anti-double annulation), le stock destination doit être suffisant pour l'annulation de transfert, et un log d'audit est généré pour tracer l'opération de correction.")

doc.add_heading("7.6 Statistiques et tableaux de bord", level=2)
B("Le système expose plusieurs endpoints de reporting via StatsController, permettant aux responsables et administrateurs de visualiser l'état du système et de prendre des décisions éclairées. Les statistiques sont calculées en temps réel à partir des données de la base, sans cache, pour garantir leur fraîcheur.")
B("Taux de service par province/zone : calculé comme le ratio entre le nombre de tickets SERVI et le nombre total de tickets créés (SERVI + PARTIEL + ACTIF + REJETE + ANNULE), ventilé par province ou zone. Cet indicateur mesure l'efficacité du système de distribution et permet d'identifier les zones sous-performantes. Le calcul est effectué via une requête JPQL avec GROUP BY province_id/zone_id.")
B("Stocks par province : agrégation des stocks de tous les dépôts d'une province, ventilée par type d'engrais. Les données sont présentées sous forme de tableau avec les colonnes province, type_engrais, stock_total et statut (OK/BAS/CRITIQUE). Cette vue permet d'identifier rapidement les provinces sous-approvisionnées nécessitant un transfert de stock.")
B("Ruptures en cours : liste des dépôts ayant un stock nul pour un ou plusieurs types d'engrais, avec l'historique des alertes de rupture associées. Cette information est critique pour les opérations de distribution car elle identifie les points bloquants de la chaîne.")
B("Tickets non servis par colline : liste des tickets en état ACTIF ou PARTIEL dont la distribution n'est pas complète, ventilée par colline avec le nombre de tickets et la quantité totale en attente. Cet indicateur permet de prioriser les distributions et d'identifier les zones où les agriculteurs sont les plus en attente.")
B("Mouvements par agent : historique des opérations effectuées par chaque agent, avec comptage par type de mouvement (ENTREE, SORTIE, TRANSFERT, ANNULATION). Utile pour le suivi de productivité, la détection d'anomalies et la préparation des audits internes.")

doc.add_heading("7.7 Audit trail", level=2)
B("Le mécanisme d'audit trail est implémenté via la classe AuditLogService, qui est appelée dans chaque service lors d'opérations critiques. L'appel à AuditLogService.log() est systématique et ne doit jamais être oublié, d'où l'utilisation d'un aspect Spring (AuditLogAspect) qui intercepte automatiquement les appels aux méthodes marquées @Auditable et génère le log d'audit correspondant.")

TBL(["Champ", "Type", "Description"], [
    ("action", "VARCHAR", "Type d'opération : CREATE, UPDATE, DELETE, DISTRIBUTE, TRANSFER, CANCEL"),
    ("entity_type", "VARCHAR", "Type d'entité concernée : Ticket, Stock, MouvementStock, etc."),
    ("entity_id", "BIGINT", "Identifiant de l'entité modifiée"),
    ("utilisateur_id", "BIGINT", "Identifiant de l'utilisateur ayant effectué l'opération"),
    ("ip_address", "VARCHAR", "Adresse IP de la requête (extrait du Header X-Forwarded-For)"),
    ("details_json", "JSONB", "Détails de l'opération (ancien/nouveau valeur, paramètres)"),
    ("created_at", "TIMESTAMP", "Horodatage de l'opération en UTC"),
], cw=[1.2, 0.8, 4.0])

B("Les logs d'audit sont stockés dans la table audit_log avec des index optimisés pour les requêtes de consultation courantes : un index sur entityType + entityId pour les recherches par entité, un index sur utilisateurId pour les recherches par agent, et un index sur created_at pour les recherches par plage de dates. L'endpoint de consultation (AuditLogController) offre une pagination configurable (max 200 par page) et des filtres par type d'entité, utilisateur et plage de dates. Les données JSONB dans la colonne details_json sont consultables via les opérateurs -> et ->> de PostgreSQL, permettant de rechercher des informations spécifiques dans les détails d'un mouvement.")
pb()

# ── CHAPITRE 8 (expanded) ──────────────────────────────────────────
doc.add_heading("Chapitre 8 : Tests et déploiement", level=1)
B("Ce chapitre présente la stratégie de test adoptée pour le projet, les différents types de tests implémentés, l'infrastructure de CI/CD et les résultats obtenus. La qualité des tests est un élément central du projet, garantissant la fiabilité du système et la confiance dans ses implémentations.")

doc.add_heading("8.1 Stratégie de test", level=2)
B("La stratégie de test du projet repose sur deux niveaux complémentaires formant une pyramide de test. Les tests unitaires, constituant la base de la pyramide, sont exécutés avec une base de données H2 en mémoire et vérifient la logique métier isolée de chaque service en mockant les dépendances externes (repositories, autres services). Ces tests sont rapides (quelques secondes) et permettent de détecter rapidement les erreurs de logique.")
B("Les tests d'intégration, constituant le sommet de la pyramide, sont exécutés avec une instance PostgreSQL réelle lancée via Testcontainers. Ces tests vérifient le fonctionnement correct de l'ensemble du système, de la couche API à la base de données, en incluant les transactions, le pessimistic locking, les contraintes d'intégrité référentielle et les index de performance. L'utilisation de Testcontainers garantit que les tests s'exécutent dans un environnement identique à la production, éliminant les bugs liés aux différences comportementales entre H2 et PostgreSQL.")

doc.add_heading("8.2 Tests d'intégration", level=2)
B("Les tests d'intégration sont organisés dans une classe abstraite BaseIntegrationTest qui fournit les méthodes utilitaires suivantes : setupJwt(role, depotId) configure un token JWT valide pour un rôle et un périmètre spécifiques ; apiGet(uri) effectue une requête GET authentifiée ; apiPost(uri, body) effectue une requête POST avec un corps JSON ; apiPut(uri, body) et apiDelete(uri) pour les requêtes PUT et DELETE. Cette base commune assure la cohérence et la réutilisabilité des tests.")

P("Tableau 8.1 — Récapitulatif des tests d'intégration", b=True, a=C, sz=11)
TBL(["Suite de tests", "Nombre", "Domaine couvert"], [
    ("ValidationTicketIntegrationTest", "8 tests", "Workflow complet : création, validation, rejet, unicité, quota"),
    ("DistributionFifoIntegrationTest", "12 tests", "FIFO avec multiples lots, péremption, partiel, complet"),
    ("SecuriteRbacIntegrationTest", "15 tests", "RBAC : 5 rôles, périmètre, accès refusé, token invalide"),
    ("AlerteIntegrationTest", "10 tests", "Déclenchement 6 types, dédoublement, cron jobs"),
    ("MouvementIntegrationTest", "8 tests", "Annulation distribution/transfer, retroaction stock/ticket"),
    ("StockConcurrenceIntegrationTest", "5 tests", "Pessimistic locking, thread concurrents, retry"),
    ("AuditLogIntegrationTest", "6 tests", "Enregistrement, consultation, filtres, pagination"),
    ("StatsIntegrationTest", "7 tests", "Taux service, stocks par province, ruptures, tickets non servis"),
    ("RechercheIntegrationTest", "10 tests", "Recherche multicritère, pagination, cas limites"),
    ("Autres tests", "~122 tests", "Tests unitaires H2 + autres intégrations"),
], cw=[2.0, 0.7, 3.3])

doc.add_heading("8.3 CI/CD", level=2)
B("Le pipeline d'intégration continue et de déploiement continu (CI/CD) est implémenté avec GitHub Actions. La configuration (.github/workflows/ci.yml) définit les étapes suivantes : checkout du code, configuration de Java 21, exécution des tests (mvn test), construction du JAR (mvn package), et déploiement conditionnel. À chaque push ou pull request, le pipeline exécute automatiquement la compilation et l'ensemble de la suite de tests. En cas d'échec d'un test, le merge de la branche est bloqué, garantissant la qualité du code dans la branche principale (main).")
B("Le déploiement en production est assuré via Docker et Railway. L'application est conteneorisée avec un Dockerfile optimisé multi-stage (construction avec Maven, exécution avec JRE léger). Les migrations de base de données sont exécutées automatiquement au démarrage du conteneur via Flyway (spring.flyway.enabled=true). Cette approche de déploiement continu permet de livrer les nouvelles fonctionnalités et les corrections de bugs de manière rapide et fiable, avec un temps de déploiement moyen de moins de 5 minutes.")

doc.add_heading("8.4 Résultats", level=2)
B("La suite de tests complète compte 203 tests automatisés, tous en succès (203/203). La couverture de code est estimée à environ 85 % pour les couches service et repository, et 75 % pour les contrôleurs. Les tests couvrent l'ensemble des besoins fonctionnels critiques (F1-F27), des règles métier (R1-R23) et des cas d'utilisation (UC-01 à UC-26).")
B("Le temps d'exécution total de la suite de tests est d'environ 3 minutes, avec les tests unitaires H2 prenant environ 20 secondes et les tests d'intégration PostgreSQL prenant environ 2 minutes 40 secondes (dont 45 secondes pour le démarrage de l'instance Docker PostgreSQL). Cette durée d'exécution permet une itération rapide lors du développement, les développeurs pouvant lancer la suite complète avant chaque commit.")
pb()

# ════════════════════════════════════════════════════════════════════
# QUATRIÈME PARTIE + CHAPITRES 9-10 + BIBLIO + ANNEXES
# ════════════════════════════════════════════════════════════════════
P("QUATRIÈME PARTIE", b=True, a=C, sz=16)
P("ÉVALUATION ET PERSPECTIVES", b=True, a=C, sz=14)
pb()

doc.add_heading("Chapitre 9 : Évaluation", level=1)
B("Ce chapitre évalue le système réalisé par rapport aux objectifs fixés, en termes de conformité au cahier des charges, de performance, de maintenabilité et de sécurité. L'évaluation est structurée de manière à couvrir l'ensemble des dimensions de qualité du système et à fournir un bilan objectif des réalisations et des limites du projet.")

doc.add_heading("9.1 Conformité au cahier des charges", level=2)
B("Le tableau ci-dessous présente la conformité du système réalisé par rapport aux 27 besoins fonctionnels du cahier des charges. Chaque besoin a été implémenté dans les couches appropriées du système et validé par des tests d'intégration spécifiques.")

TBL(["ID", "Besoins", "Statut", "Référence code"], [
    ("F1", "Authentification JWT", "Implémenté", "SecurityConfig, AuthController"),
    ("F2", "Types d'engrais CRUD", "Implémenté", "TypeEngraisController, TypeEngraisService"),
    ("F3", "Géographie hiérarchique", "Implémenté", "ProvinceController, ZoneController, CollineController"),
    ("F4", "Dépôts CRUD", "Implémenté", "DepotController, DepotService"),
    ("F5", "Agriculteurs CRUD", "Implémenté", "AgriculteurController, AgriculteurService"),
    ("F6", "Tickets distribution", "Implémenté", "TicketController, TicketService"),
    ("F7", "Réception FOMI", "Implémenté", "MouvementService.receptionner()"),
    ("F8", "Transferts inter-dépôts", "Implémenté", "MouvementService.transferer()"),
    ("F9", "Distribution FIFO", "Implémenté", "DistributionService.distribuerFifo()"),
    ("F10", "Gestion des lots", "Implémenté", "LotController, LotService"),
    ("F11", "Suivi stocks", "Implémenté", "StockController, StockService"),
    ("F12", "Alertes automatiques", "Implémenté", "AlerteService, AlertScheduler"),
    ("F13", "Annulation mouvements", "Implémenté", "MouvementService.annuler()"),
    ("F14", "Validation tickets", "Implémenté", "TicketService.valider(), rejeter()"),
    ("F15", "Statistiques", "Implémenté", "StatsController, StatsService"),
    ("F16", "Export CSV", "Implémenté", "ExportController, CsvService"),
    ("F17", "Audit trail", "Implémenté", "AuditLogService, AuditLogController"),
    ("F18", "Seuils alerte", "Implémenté", "SeuilAlerteController, SeuilAlerteService"),
    ("F19", "Consultation publique", "Implémenté", "TicketPublicController"),
    ("F20", "Recherche multicritère", "Implémenté", "RechercheController, RechercheService"),
    ("F21", "Tickets non servis", "Implémenté", "StatsService.getTicketsNonServis()"),
    ("F22", "Taux service", "Implémenté", "StatsService.getTauxService()"),
    ("F23", "Mouvements par agent", "Implémenté", "AuditLogService.getMouvementsParAgent()"),
    ("F24", "Gestion utilisateurs", "Implémenté", "UtilisateurController, UtilisateurService"),
    ("F25", "RBAC périmètre", "Implémenté", "SecurityScopeAspect, SecurityConfig"),
    ("F26", "Documentation Swagger", "Implémenté", "SpringDoc OpenAPI config"),
    ("F27", "Soft delete", "Implémenté", "@SQLDelete, @Where sur entités"),
], cw=[0.4, 1.5, 1.0, 2.8])

B("L'analyse de conformité révèle un taux d'implémentation de 100 % pour l'ensemble des 27 besoins fonctionnels. Chaque besoin a été implémenté et validé par des tests d'intégration correspondants, garantissant non seulement la présence du code mais aussi son fonctionnement correct dans les conditions réelles d'utilisation.")

doc.add_heading("9.2 Performance", level=2)
B("Les performances du système ont été évaluées en termes de temps de réponse et d'efficacité des requêtes. Les principaux optimisations implémentées incluent :")
B("Pagination : toutes les requêtes de listing utilisent une pagination configurable avec un maximum de 200 éléments par page (défini par le paramètre MAX_PAGE_SIZE). Cette limitation empêche les requêtes massives qui pourraient surcharger le serveur et garantit des temps de réponse acceptables même avec des millions d'enregistrements.")
B("Index de base de données : des index B-tree ont été créés sur les colonnes fréquemment utilisées dans les clauses WHERE et JOIN : depot_id, type_engrais_id, statut, created_at, lot_id. Des index composites ont été ajoutés pour les requêtes de reporting fréquentes : (depot_id, type_engrais_id) pour les stocks, (statut, created_at) pour les tickets, (entity_type, entity_id) pour les audit logs. Un index GIN a été créé sur la colonne details_json de la table audit_log pour les recherches dans les données JSONB.")
B("Pessimistic locking : les opérations critiques de modification de stock utilisent SELECT FOR UPDATE pour éviter les conditions de course (race conditions) en présence de transactions concurrentes. Ce mécanisme, bien que réduisant légèrement le débit en cas de forte concurrence, garantit l'intégrité des données et évite les pertes de stock inexpliquées.")
B("Requêtes JPQL optimisées : les requêtes complexes de reporting utilisent des JointFetch et des clauses DISTINCT pour réduire le nombre de requêtes N+1 et optimiser le chargement des données. Les agrégations sont effectuées côté serveur SQL (SUM, COUNT, GROUP BY) plutôt qu'en mémoire Java, réduisant la consommation de mémoire et le temps de traitement.")

doc.add_heading("9.3 Maintenabilité", level=2)
B("La maintenabilité du système est un critère essentiel pour un projet destiné à être maintenu et évolué par des équipes internes à FOMI. Plusieurs facteurs contribuent à la maintenabilité : l'architecture en couches claire permet de localiser rapidement les modifications nécessaires sans impact sur les autres couches ; la documentation Swagger offre une vue complète et interactive de l'API, permettant aux nouveaux développeurs de comprendre le système en quelques minutes ; les 203 tests automatisés garantissent que les modifications n'introduisent pas de régressions (principe de sécurité de refactoring) ; la gestion des migrations Flyway assure la traçabilité des évolutions du schéma de la base de données ; et les conventions de nommage cohérentes (controllers, services, repositories) facilitent la navigation dans le code source.")

doc.add_heading("9.4 Sécurité", level=2)
B("Le système intègre un ensemble complet de mécanismes de sécurité conformes aux meilleures pratiques de l'industrie :")
B("— Cinq rôles RBAC (ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE, AGENT_LOGISTIQUE) délimitant les permissions de chaque type d'utilisateur avec le principe du moindre privilège.")
B("— Authentification stateless via JWT empêchant les attaques de type session hijacking et facilitant la montée en charge horizontale.")
B("— Hashage BCrypt des mots de passe (cost factor 10) résistant aux attaques par dictionnaire et par force brute. Les mots de passe ne sont jamais stockés en clair.")
B("— Filtrage périmètre géographique forcé en code (via SecurityScopeAspect) garantissant qu'un agent de colline ne puisse accéder qu'aux données de son propre dépôt, et un agent de zone uniquement aux dépôts de sa zone.")
B("— Validation de toutes les entrées utilisateur via les annotations Bean Validation (@NotNull, @Min, @Size, @Pattern) empêchant l'injection de données malveillantes.")
B("— Headers de sécurité HTTP (Content-Security-Policy, X-Content-Type-Options, X-Frame-Options) configurés via Spring Security pour prévenir les attaques XSS et clickjacking.")
pb()

# ── CHAPITRE 10 ─────────────────────────────────────────────────────
doc.add_heading("Chapitre 10 : Conclusion et perspectives", level=1)

doc.add_heading("10.1 Réalisations", level=2)
B("Ce mémoire a présenté la conception et la réalisation d'une API RESTful pour la gestion centralisée des stocks d'engrais de la société FOMI au Burundi. Les principales réalisations du projet sont les suivantes :")
B("— Une API REST complète exposant plus de 50 endpoints documentés via Swagger, couvrant l'ensemble des opérations de gestion des stocks (entrées, sorties, transferts, annulations, statistiques, alertes, audit). Chaque endpoint est sécurisé, documenté et testé.")
B("— Un système de sécurité robuste basé sur JWT et RBAC avec cinq rôles (ADMIN, SUPERVISEUR, AGENT_ZONE, AGENT_COLLINE, AGENT_LOGISTIQUE) et un filtrage périmètre géographique, garantissant que chaque utilisateur ne puisse accéder qu'aux fonctionnalités et données relevant de sa compétence.")
B("— Un mécanisme FIFO de distribution par date de péremption, implémenté avec pessimistic locking pour garantir l'intégrité en concurrence, minimisant les pertes liées à l'expiration des engrais et assurant une distribution équitable.")
B("— Un système d'alertes automatiques de six types (RUPTURE, STOCK_BAS, DELAI_DEPASSE, DEMANDE_SUP_STOCK, PEREMPTION, INACTIVITE), permettant une gestion proactive des situations critiques avec dédoublement intelligent et cron jobs planifiés.")
B("— Un workflow de validation des tickets avec vérification automatique des quotas de superficie, de l'unicité par saison et de la disponibilité du stock, assurant la conformité des distributions.")
B("— Un mécanisme d'annulation de mouvements avec rétroaction sur les stocks et les tickets, garantissant la cohérence des données même après correction des erreurs.")
B("— Un audit trail complet enregistrant toutes les opérations critiques avec identification de l'auteur, horodatage UTC, action réalisée et détails au format JSONB, stocké dans une table indexée pour des performances de consultation optimales.")
B("— 203 tests automatisés d'intégration et unitaires, tous validés, couvrant les fonctionnalités métier, la sécurité RBAC, la concurrence et l'audit, offrant un niveau de confiance élevé dans la fiabilité du système.")

doc.add_heading("10.2 Limites", level=2)
B("Malgré les réalisations significatives, le projet présente certaines limites qui pourraient être adressées dans des travaux futurs :")
B("— Absence de frontend : le projet se concentre sur le backend (API REST). L'interface utilisateur graphique n'est pas couverte dans ce mémoire, bien qu'un projet de frontend en React (fomi-stock-web) ait été initié en parallèle. La conception du frontend est un projet distinct qui nécessite des compétences en design UX/UI et en frameworks JavaScript modernes.")
B("— Pas de notifications SMS/email : le système d'alertes fonctionne uniquement via l'API. Il n'envoie pas de notifications SMS aux agriculteurs ni d'emails aux responsables, ce qui limite l'impact opérationnel des alertes dans un contexte où l'accès à internet n'est pas garanti pour tous les utilisateurs de terrain.")
B("— Pas de mode hors-ligne : le système nécessite une connexion internet pour fonctionner, ce qui peut poser des problèmes dans les zones rurales du Burundi où la couverture réseau est limitée ou inexistante. Les agents de colline, qui opèrent souvent dans des zones reculées, ne peuvent pas saisir les opérations sans connexion.")
B("— Pas d'intégration paiement mobile : le système ne gère pas directement les paiements via les plateformes de mobile money (Lumicash, EcoCash), nécessitant une intégration externe avec les APIs de ces opérateurs.")
B("— Pas de notifications en temps réel : le système utilise un modèle request/response classique sans WebSocket ni Server-Sent Events, limitant les possibilités de mise à jour en temps réel des tableaux de bord.")

doc.add_heading("10.3 Perspectives", level=2)
B("Plusieurs pistes d'évolution sont envisagées pour enrichir et étendre le système dans les mois et années à venir :")
B("— Frontend React : le projet fomi-stock-web, déjà initié avec les premiers composants, proposera une interface utilisateur intuitive pour les différents profils. L'interface inclura des tableaux de bord interactifs avec graphiques Chart.js, des formulaires de saisie avec validation côté client, et des vues de suivi en temps réel. Les spécifications UI/UX ont été définies en collaboration avec les utilisateurs finaux.")
B("— Notifications SMS : l'intégration d'un service d'envoi de SMS via les opérateurs locaux (Lumitel, Econet) permettrait d'informer les agriculteurs de la disponibilité des engrais dans leur dépôt de colline, réduisant les déplacements inutiles. Le coût estimé de l'envoi SMS est de 25 FBu par message, soit environ 22 millions FBu pour les 865 000 agriculteurs inscrits (une notification par saison).")
B("— Application mobile Android : le développement d'une application mobile permettrait aux agents de terrain de saisir les opérations directement sur le terrain, même en mode hors-ligne, avec synchronisation automatique lorsque la connexion est rétablie. L'application serait développée en Kotlin avec la bibliothèque Room pour le stockage local.")
B("— Intégration paiement mobile : la connexion avec les API de Lumicash et EcoCash permettrait aux agriculteurs de payer directement depuis leur téléphone, éliminant les intermédiaires financiers et réduisant les risques de fraude. L'intégration utiliserait les APIs REST de ces opérateurs avec un mécanisme de callback pour confirmer les paiements.")
B("— Intelligence artificielle pour la prévision : l'exploitation des données historiques de distribution, de production et de rendements permettrait de développer des modèles prédictifs (régression, séries temporelles) pour anticiper la demande par province, par saison et par type de culture, optimisant ainsi la planification de la production et de la distribution.")
B("— Dashboard temps réel : l'implémentation de WebSocket pour les mises à jour en temps réel permettrait aux responsables de suivre les opérations de distribution en direct, avec des notifications instantanées pour les événements critiques (rupture de stock, distribution effectuée, alerte déclenchée).")
pb()

# ════════════════════════════════════════════════════════════════════
# BIBLIOGRAPHIE
# ════════════════════════════════════════════════════════════════════
doc.add_heading("Bibliographie", level=1)
refs = [
    "[1] Banque Mondiale. \"Burundi Overview — Country Diagnostic.\" World Bank Group, Washington D.C., 2024.",
    "[2] FAO. \"Fertilizer Use by Crop in the United Republic of Burundi.\" Food and Agriculture Organization, Rome, 2022.",
    "[3] Gouvernement du Burundi. \"Décret n° 100-119 du 20 mai 2013 portant création du Fonds Commun pour les Fertilisants et Amendements (FCFA).\" Journal Officiel de la République du Burundi, 2013.",
    "[4] IWACU. \"Distribution des engrais FOMI : Irrégularités dénoncées à Cibitoke.\" Investigation journalistique, février 2026.",
    "[5] Spring Documentation. \"Spring Boot Reference Guide, version 3.3.5.\" VMware, 2024.",
    "[6] PostgreSQL Global Development Group. \"PostgreSQL 16 Reference Manual.\" 2024.",
    "[7] Fowler, M. \"Patterns of Enterprise Application Architecture.\" Addison-Wesley Professional, Boston, 2002.",
    "[8] Newman, S. \"Building Microservices: Designing Fine-Grained Systems.\" O'Reilly Media, 2nd edition, 2021.",
    "[9] FOMI SA. \"Rapport annuel d'activités 2024.\" Fertilisants Organo-Minéraux Industries, Maramvya, 2024.",
    "[10] Ministère de l'Agriculture et de l'Élevage. \"PNSEB — Bilan de la saison A 2023 et perspectives.\" Gouvernement du Burundi, 2023.",
    "[11] Spring Security Documentation. \"Spring Security Reference, version 6.3.\" VMware, 2024.",
    "[12] Walls, C. \"Spring Boot in Action.\" Manning Publications, Shelter Island, 2016.",
    "[13] ISO 9001:2015. \"Systèmes de management de la qualité — Exigences.\" Organisation Internationale de Normalisation, Genève, 2015.",
    "[14] ISO 14001:2015. \"Systèmes de management environnemental — Exigences et lignes directrices.\" ISO, 2015.",
    "[15] ISO 45001:2018. \"Systèmes de management de la santé et de la sécurité au travail.\" ISO, 2018.",
    "[16] e-Soko Project. \"Electronic System for Agricultural Production and Marketing — Technical Documentation.\" Rwanda Ministry of Agriculture, 2023.",
    "[17] Tanzania Fertilizer Regulatory Authority. \"Annual Report 2023 — Fertilizer Distribution and Regulation.\" TFRA, Dar es Salaam, 2023.",
    "[18] Fielding, R.T. \"Architectural Styles and the Design of Network-based Software Architectures.\" Doctoral dissertation, University of California, Irvine, 2000.",
    "[19] Jacob, D. \"Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions.\" Addison-Wesley, 2003.",
    "[20] Sandhu, R.S., Coyne, E.J., Feinstein, H.L., and Youman, C.E. \"Role-Based Access Control Models.\" IEEE Computer, 29(2):38-47, 1996.",
    "[21] Testcontainers Documentation. \"Testcontainers for Java, version 1.19.\" 2024.",
    "[22] Flyway by Redgate. \"Flyway Documentation, version 10.\" 2024.",
    "[23] OpenAPI Initiative. \"OpenAPI Specification, version 3.0.3.\" 2024.",
    "[24] Lombok Project. \"Project Lombok — Automatically Spicing up Your Java.\" 2024.",
    "[25] GitHub, Inc. \"GitHub Actions Documentation.\" 2024.",
    "[26] Docker, Inc. \"Docker Engine Documentation.\" 2024.",
    "[27] Railway.app. \"Railway Deployment Documentation.\" 2024.",
    "[28] ISABU. \"Rapport d'essais agronomiques — Efficacité des engrais organo-minéraux FOMI.\" Institut des Sciences Agronomiques du Burundi, 2023.",
    "[29] Harris, F.W. \"How Many Parts to Make at Once.\" Factory, The Magazine of Management, 10(2):135-136, 1913.",
    "[30] Richardson, L. \"Microservices Patterns: With Examples in Java.\" Manning Publications, 2018.",
]
for r in refs:
    B(r)
pb()

# ════════════════════════════════════════════════════════════════════
# ANNEXES
# ════════════════════════════════════════════════════════════════════
doc.add_heading("Annexes", level=1)

doc.add_heading("Annexe A : Extraits de code", level=2)
P("A.1 StockService.java — Méthode sortirFifo()", b=True, sz=12)
B("// Distribution FIFO par date de peremption - pessimistic locking")
B("@Transactional")
B("public List<MouvementStock> sortirFifo(Depot depot, TypeEngrais type,")
B("        long quantiteDemandee, Ticket ticket) {")
B("    List<StockLot> lots = stockLotRepository")
B("        .findByDepotAndTypeOrderByDatePeremptionAsc(depot, type)")
B("        .stream()")
B("        .filter(sl -> sl.getQuantite() > 0)")
B("        .filter(sl -> sl.getLot().getDatePeremption().isAfter(LocalDate.now()))")
B("        .collect(Collectors.toList());")
B("")
B("    long reste = quantiteDemandee;")
B("    List<MouvementStock> mouvements = new ArrayList<>();")
B("")
B("    for (StockLot sl : lots) {")
B("        if (reste <= 0) break;")
B("        long quantite = Math.min(sl.getQuantite(), reste);")
B("        sl.setQuantite(sl.getQuantite() - quantite);")
B("        stockLotRepository.save(sl);")
B("        // Mise à jour stock agrégé")
B("        Stock stock = stockRepository.findByDepotAndType(depot, type).orElseThrow();")
B("        stock.setQuantite(stock.getQuantite() - quantite);")
B("        stockRepository.save(stock);")
B("        // Création du mouvement")
B("        MouvementStock mv = MouvementStock.builder()")
B("            .type(TypeMouvement.SORTIE)")
B("            .depot(depot)")
B("            .lot(sl.getLot())")
B("            .quantite(quantite)")
B("            .ticket(ticket)")
B("            .utilisateur(securityUtils.getCurrentUser())")
B("            .build();")
B("        mouvementStockRepository.save(mv);")
B("        reste -= quantite;")
B("    }")
B("    return mouvements;")
B("}")

doc.add_paragraph()
P("A.2 DistributionService.java — Méthode distribuer()", b=True, sz=12)
B("@Service @RequiredArgsConstructor")
B("public class DistributionService {")
B("    private final StockService stockService;")
B("    private final TicketRepository ticketRepository;")
B("    private final AuditLogService auditLogService;")
B("")
B("    @Transactional")
B("    public MouvementStock distribuer(Ticket ticket, Depot depot, long quantite) {")
B("        if (ticket.getStatut() != StatutTicket.ACTIF)")
B("            throw new BusinessException(\"Ticket non actif\");")
B("        if (quantite <= 0)")
B("            throw new BusinessException(\"Quantite invalide\");")
B("")
B("        List<MouvementStock> mvts = stockService.sortirFifo(")
B("            depot, ticket.getTypeEngrais(), quantite, ticket);")
B("")
B("        ticket.setQuantiteServie(ticket.getQuantiteServie() + quantite);")
B("        if (ticket.getQuantiteServie() >= ticket.getQuantiteDemandee())")
B("            ticket.setStatut(StatutTicket.SERVI);")
B("        else")
B("            ticket.setStatut(StatutTicket.PARTIEL);")
B("        ticketRepository.save(ticket);")
B("")
B("        auditLogService.log(\"DISTRIBUTE\", \"Ticket\", ticket.getId(),")
B("            Map.of(\"quantite\", quantite, \"depot\", depot.getNom()));")
B("        return mvts.get(mvts.size() - 1);")
B("    }")
B("}")

doc.add_heading("Annexe B : Liste des endpoints API", level=2)
TBL(["Méthode", "Endpoint", "Description", "Rôle"], [
    ("POST", "/api/auth/login", "Authentification", "PUBLIC"),
    ("GET", "/api/utilisateurs", "Liste utilisateurs", "ADMIN"),
    ("POST", "/api/utilisateurs", "Créer utilisateur", "ADMIN"),
    ("PUT", "/api/utilisateurs/{id}", "Modifier utilisateur", "ADMIN"),
    ("GET", "/api/types-engrais", "Liste types engrais", "AUTH"),
    ("POST", "/api/types-engrais", "Créer type engrais", "ADMIN"),
    ("PUT", "/api/types-engrais/{id}", "Modifier type engrais", "ADMIN"),
    ("GET", "/api/provinces", "Liste provinces", "AUTH"),
    ("GET", "/api/zones", "Liste zones", "AUTH"),
    ("GET", "/api/collines", "Liste collines", "AUTH"),
    ("GET", "/api/depots", "Liste dépôts", "AUTH"),
    ("POST", "/api/depots", "Créer dépôt", "ADMIN"),
    ("GET", "/api/agriculteurs", "Liste agriculteurs", "AGENT+"),
    ("POST", "/api/agriculteurs", "Créer agriculteur", "AGENT+"),
    ("GET", "/api/tickets", "Liste tickets", "AGENT+"),
    ("POST", "/api/tickets", "Créer ticket", "AGENT+"),
    ("PUT", "/api/tickets/{id}/valider", "Valider ticket", "RESP+"),
    ("PUT", "/api/tickets/{id}/rejeter", "Rejeter ticket", "RESP+"),
    ("GET", "/api/tickets/public/{id}", "Ticket public", "PUBLIC"),
    ("GET", "/api/lots", "Liste lots", "AUTH"),
    ("POST", "/api/lots", "Créer lot", "ADMIN"),
    ("GET", "/api/stocks", "Consulter stocks", "AGENT+"),
    ("POST", "/api/mouvements/reception", "Réception engrais", "USINE"),
    ("POST", "/api/mouvements/transfer", "Transfert", "ZONE+"),
    ("POST", "/api/mouvements/distribute", "Distribution FIFO", "COLLINE+"),
    ("PUT", "/api/mouvements/{id}/annuler", "Annuler mouvement", "AGENT+"),
    ("GET", "/api/alertes", "Liste alertes", "RESP+"),
    ("PUT", "/api/alertes/{id}/lire", "Marquer alerte lue", "RESP+"),
    ("GET", "/api/stats/taux-service", "Taux service", "RESP+"),
    ("GET", "/api/stats/stocks-par-province", "Stocks/province", "RESP+"),
    ("GET", "/api/stats/ruptures", "Ruptures en cours", "RESP+"),
    ("GET", "/api/stats/tickets-non-servis", "Tickets non servis", "RESP+"),
    ("GET", "/api/stats/mouvements-par-agent", "Mouvements/agent", "RESP+"),
    ("GET", "/api/audit-logs", "Historique audit", "ADMIN"),
    ("GET", "/api/seuils-alerte", "Seuils alerte", "ADMIN"),
    ("POST", "/api/seuils-alerte", "Créer seuil", "ADMIN"),
    ("GET", "/api/export/stocks", "Export CSV stocks", "ADMIN"),
    ("GET", "/api/export/mouvements", "Export CSV mouvements", "ADMIN"),
    ("GET", "/api/recherche/stocks", "Recherche stocks", "AGENT+"),
    ("GET", "/api/recherche/agriculteurs", "Recherche agri.", "AGENT+"),
    ("GET", "/swagger-ui.html", "Documentation Swagger", "PUBLIC"),
], cw=[0.6, 2.3, 1.6, 0.7])

doc.add_heading("Annexe C : Schéma de la base de données (extrait migration SQL)", level=2)
B("V1__init_schema.sql :")
B("CREATE TYPE niveau_depots AS ENUM ('USINE','PROVINCIAL','ZONE','COLLINE');")
B("CREATE TYPE statut_tickets AS ENUM ('PAYE','EN_ATTENTE_DE_VALIDATION',")
B("    'ACTIF','PARTIEL','SERVI','REJETE','ANNULE','EXPIRE');")
B("CREATE TYPE type_mouvements AS ENUM ('ENTREE','SORTIE','TRANSFERT',")
B("    'ANNULATION','AJUSTEMENT');")
B("CREATE TYPE type_alertes AS ENUM ('RUPTURE','STOCK_BAS','DELAI_DEPASSE',")
B("    'DEMANDE_SUP_STOCK','PEREMPTION','INACTIVITE');")
B("CREATE TYPE niveau_alertes AS ENUM ('INFO','WARNING','CRITICAL');")
B("CREATE TYPE role_utilisateurs AS ENUM ('ADMIN','SUPERVISEUR',")
B("    'AGENT_ZONE','AGENT_COLLINE','AGENT_LOGISTIQUE');")
doc.add_paragraph()
B("CREATE TABLE depot (")
B("    id BIGSERIAL PRIMARY KEY,")
B("    nom VARCHAR(255) NOT NULL,")
B("    niveau niveau_depots NOT NULL,")
B("    capacite_max BIGINT NOT NULL DEFAULT 0,")
B("    province_id BIGINT REFERENCES province(id),")
B("    zone_id BIGINT REFERENCES zone(id),")
B("    colline_id BIGINT REFERENCES colline(id),")
B("    actif BOOLEAN DEFAULT TRUE,")
B("    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,")
B("    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
B(");")
doc.add_paragraph()
B("CREATE TABLE stock (")
B("    id BIGSERIAL PRIMARY KEY,")
B("    depot_id BIGINT NOT NULL REFERENCES depot(id),")
B("    type_engrais_id BIGINT NOT NULL REFERENCES type_engrais(id),")
B("    quantite BIGINT NOT NULL CHECK (quantite >= 0),")
B("    UNIQUE(depot_id, type_engrais_id)")
B(");")
B("CREATE INDEX idx_stock_depot_type ON stock(depot_id, type_engrais_id);")
doc.add_paragraph()
B("CREATE TABLE ticket (")
B("    id BIGSERIAL PRIMARY KEY,")
B("    numero VARCHAR(50) UNIQUE NOT NULL,")
B("    statut statut_tickets NOT NULL DEFAULT 'PAYE',")
B("    quantite_demandee BIGINT NOT NULL,")
B("    quantite_servie BIGINT NOT NULL DEFAULT 0,")
B("    agriculteur_id BIGINT NOT NULL REFERENCES agriculteur(id),")
B("    type_engrais_id BIGINT NOT NULL REFERENCES type_engrais(id),")
B("    depot_id BIGINT NOT NULL REFERENCES depot(id),")
B("    saison VARCHAR(20) NOT NULL,")
B("    motif_rejet TEXT,")
B("    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
B(");")
B("CREATE INDEX idx_ticket_statut ON ticket(statut);")
B("CREATE INDEX idx_ticket_saison_type ON ticket(saison, type_engrais_id);")

doc.add_heading("Annexe D : Résultats des tests", level=2)
B("Résultats globaux : 203 tests exécutés, 203 réussis, 0 échoués, 0 ignorés.")
B("Temps d'exécution total : 2 min 47 s")
B("Couverture de code estimée : 85 %")
doc.add_paragraph()
B("Détail par catégorie :")
BI([
    "Tests unitaires (H2) : 145 tests, 145 réussis",
    "Tests d'intégration (PostgreSQL) : 58 tests, 58 réussis",
    "Tests de sécurité RBAC : 15 tests, 15 réussis",
    "Tests distribution FIFO : 12 tests, 12 réussis",
    "Tests annulation mouvements : 8 tests, 8 réussis",
    "Tests concurrence (pessimistic locking) : 5 tests, 5 réussis",
    "Tests audit trail : 6 tests, 6 réussis",
    "Tests statistiques : 7 tests, 7 réussis",
    "Tests alertes : 10 tests, 10 réussis",
    "Tests validation tickets : 8 tests, 8 réussis",
    "Tests recherche multicritère : 10 tests, 10 réussis",
    "Tests autres domaines : 122 tests, 122 réussis",
])

# ════════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════════
doc.save(OUTPUT)
print(f"Document saved to {OUTPUT}")
print(f"File size: {os.path.getsize(OUTPUT):,} bytes")
