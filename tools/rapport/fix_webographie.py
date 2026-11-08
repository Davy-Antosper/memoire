# -*- coding: utf-8 -*-
"""Nettoie les URLs residuelles du corps, reconstruit la webographie,
et corrige la mention 'Architecture en couches' dans le tableau."""
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC = r"Rapport_stage_FOMI_canevas.docx"

URL_RE = re.compile(r'\s*https?://\S+')

# Libelles de webographie : (auteur/organisation, titre, url)
WEBO = [
    ("SOS Médias Burundi", "Fertilizer Scandal in Burundi: Billions Claimed, Unclear Responsibilities",
     "https://www.sosmediasburundi.org/en/2026/01/03/fertilizer-scandal-in-burundi-billions-claimed-unclear-responsibilities-and-farmers-held-hostage/"),
    ("SOS Médias Burundi", "Burunga : la crise des engrais tourne au cauchemar, les agriculteurs craignent une catastrophe alimentaire",
     "https://www.sosmediasburundi.org/en/2026/06/24/burunga-the-fertilizer-crisis-turns-into-a-nightmare-farmers-fear-a-food-catastrophe/"),
    ("Andika Magazine", "Tensions entre le ministre des Finances et la FOMI : 81,6 milliards en jeu dans le différend sur les engrais",
     "https://andikamagazine.net/tensions-between-burundis-finance-minister-and-fomi-bif-81-6-billion-at-stake-in-fertilizer-dispute/"),
    ("IWACU Burundi", "Engrais FOMI : des irrégularités dans la distribution persistent",
     "https://www.iwacu-burundi.org/engrais-fomi-des-irregularites-dans-la-distribution-persistent/"),
    ("CGIAR", "Rwanda's Digital Revolution in Agriculture: Challenges and Progress in Smart Fertilizer Management",
     "https://www.cgiar.org/news-events/news/rwandas-digital-revolution-in-agriculture-challenges-and-progress-in-smart-fertilizer-management"),
    ("CGIAR CGSpace", "Smart Nkunganire System — évaluation de la plateforme de subvention des intrants au Rwanda",
     "https://cgspace.cgiar.org/items/136fbcf4-94c8-4411-a9e2-803f794bd6e6"),
    ("CGIAR CGSpace", "Digital tools for fertilizer subsidy management in East Africa",
     "https://cgspace.cgiar.org/items/92ed3212-3eed-4b59-bb84-8ee93b3a4255"),
    ("Safaricom", "Ministry of Agriculture selects Safaricom to streamline the subsidy voucher programme",
     "https://www.safaricom.co.ke/media-center-landing/press-releases/ministry-of-agriculture-selects-safaricom-to-streamline-subsidy-voucher-program"),
    ("Ethics and Anti-Corruption Commission (Kenya)", "EACC to monitor compliance of the National Fertilizer Subsidy Programme",
     "https://eacc.go.ke/en/default/eacc-to-monitor-compliance-of-national-fertilizer-subsidy-program-in-the-ministry-of-agriculture/"),
    ("Institute of Economic Affairs (Kenya)", "The pros and cons of the KSh 3 500 fertilizer subsidy",
     "https://ieakenya.or.ke/blog/the-pros-and-cons-of-the-ksh-3500-fertilizer-subsidy/"),
    ("Tanzania Fertilizer Regulatory Authority", "TFRA — Portail officiel de régulation des engrais",
     "https://www.tfra.go.tz/"),
    ("ZATRA", "Register a fertilizer product in Tanzania",
     "https://www.zatra.co/post/register-fertilizer-product-tanzania"),
    ("Spring", "Spring Boot Reference Documentation (3.3.5)",
     "https://docs.spring.io/spring-boot/index.html"),
    ("PostgreSQL Global Development Group", "PostgreSQL 16 Documentation",
     "https://www.postgresql.org/docs/16/index.html"),
    ("Testcontainers", "Testcontainers for Java — Documentation",
     "https://java.testcontainers.org/"),
    ("Redgate", "Flyway Documentation",
     "https://documentation.red-gate.com/flyway"),
    ("OpenAPI Initiative", "OpenAPI Specification 3.0.3",
     "https://spec.openapis.org/oas/v3.0.3"),
    ("Project Lombok", "Project Lombok — Documentation",
     "https://projectlombok.org/"),
    ("GitHub", "GitHub Actions Documentation",
     "https://docs.github.com/en/actions"),
    ("Docker Inc.", "Docker Engine Documentation",
     "https://docs.docker.com/engine/"),
    ("Railway", "Railway — Documentation de déploiement",
     "https://docs.railway.com/"),
]


def set_text(par, text):
    runs = par.runs
    if not runs:
        par.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


doc = Document(DOC)

# 1. Retirer les URLs collées dans le corps
body_fixed = 0
for p in doc.paragraphs:
    if "http://" in p.text or "https://" in p.text:
        # ne pas toucher la webographie (reconstruite plus bas)
        new = URL_RE.sub("", p.text).strip()
        if not new.endswith(".") and not new.endswith(":"):
            new += "."
        new = re.sub(r'\s{2,}', ' ', new)
        new = new.replace("..", ".")
        if new != p.text:
            set_text(p, new)
            body_fixed += 1

# 2. Corriger la mention 'architecture en couches' dans le tableau
tbl_fixed = 0
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                if "Architecture en couches" in p.text:
                    set_text(p, p.text.replace("Architecture en couches",
                                               "Architecture trois tiers"))
                    tbl_fixed += 1

# 3. Supprimer la reference [9] (PNSEB) et renumeroter 1..N
refs_start = None
webo_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.style.name == "Heading 1" and p.text.strip().upper().startswith("RÉFÉRENCES"):
        refs_start = i
    if p.style.name == "Heading 1" and p.text.strip().upper() == "WEBOGRAPHIE":
        webo_idx = i
        break

if refs_start is None or webo_idx is None:
    raise SystemExit("Sections bibliographie/webographie introuvables")

ref_pars = [p for p in doc.paragraphs[refs_start + 1:webo_idx] if p.text.strip()]
kept = [p for p in ref_pars if "PNSEB" not in p.text]

# retirer les paragraphes supprimes
for p in ref_pars:
    if p not in kept:
        p._element.getparent().remove(p._element)

# renumeroter les references
for n, p in enumerate(kept, start=1):
    txt = re.sub(r'^\[\d+\]\s*', '', p.text).strip()
    set_text(p, f"[{n}] {txt}")

# 4. Reconstruire la webographie : supprimer les anciens paragraphes
#    et reinserer les nouvelles entrées
old_webo = []
idx = None
for i, p in enumerate(doc.paragraphs):
    if p.style.name == "Heading 1" and p.text.strip().upper() == "WEBOGRAPHIE":
        idx = i
        break
for p in doc.paragraphs[idx + 1:]:
    if p.style.name == "Heading 1":
        break
    old_webo.append(p)

heading = doc.paragraphs[idx]
model = old_webo[0] if old_webo else None
for p in old_webo:
    p._element.getparent().remove(p._element)

base = len(kept)
prev = heading._element
for n, (org, title, url) in enumerate(WEBO, start=base + 1):
    new_p = doc.add_paragraph()
    # deplacer juste apres le titre WEBOGRAPHIE
    prev.addnext(new_p._element)
    prev = new_p._element
    r = new_p.add_run(f"[{n}] {org}. « {title}. » [en ligne], {url}, consulté le 7 novembre 2026.")
    r.font.size = Pt(12)
    r.font.name = "Times New Roman"
    new_p.paragraph_format.space_after = Pt(6)
    new_p.paragraph_format.line_spacing = 1.5
    new_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

doc.save(DOC)
print("URLs retirees du corps :", body_fixed)
print("cellules tableau corrigees :", tbl_fixed)
print("references conservees :", len(kept), "| webographie :", len(WEBO))