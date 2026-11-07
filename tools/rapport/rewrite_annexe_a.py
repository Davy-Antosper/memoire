# -*- coding: utf-8 -*-
"""Remplace l'annexe A par des extraits de code non-FIFO
(activation de ticket, systeme d'alertes) et corrige les dernieres
mentions FIFO du resume et de la strategie de test."""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

DOC = r"Rapport_stage_FOMI_canevas.docx"


def set_text(par, text):
    runs = par.runs
    if not runs:
        par.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


doc = Document(DOC)

# ---------------------------------------------------------------------------
# 1. Dernieres mentions FIFO dans le corps
# ---------------------------------------------------------------------------
REPL = [
    ("la gestion FIFO des lots par date",
     "la gestion des lots par date de réception"),
    ("les cas métier (FIFO, annulation, alertes)",
     "les cas métier (distribution, annulation, alertes)"),
]
fixed = 0
for p in doc.paragraphs:
    for old, new in REPL:
        if old in p.text:
            set_text(p, p.text.replace(old, new))
            fixed += 1
            break

# ---------------------------------------------------------------------------
# 2. Remplacer le contenu de l'annexe A
# ---------------------------------------------------------------------------
pars = doc.paragraphs
start = end = None
for i, p in enumerate(pars):
    if p.style.name == "Heading 2" and p.text.strip().startswith("Annexe A"):
        start = i
    if p.style.name == "Heading 2" and p.text.strip().startswith("Annexe B") and start:
        end = i
        break

if start is None or end is None:
    raise SystemExit("Annexe A introuvable")

# modele de paragraphe de code (Consolas 8,5 pt)
code_model = None
for p in pars[start:end]:
    if p.runs and p.runs[0].font.name == "Consolas":
        code_model = p
        break

# supprimer l'ancien contenu (garder le titre)
for p in pars[start + 1:end]:
    p._element.getparent().remove(p._element)

CODE = [
    ("A.1 TicketService.java — Activation et rejet d’un ticket", True),
    ("@Transactional", False),
    ("public TicketResponse activer(Long id) {", False),
    ("    Ticket ticket = ticketRepository.findById(id)", False),
    ("            .orElseThrow(() -> new ResourceNotFoundException(", False),
    ('                    "Ticket introuvable : " + id));', False),
    ("    if (ticket.getStatut() != StatutTicket.EN_ATTENTE_DE_VALIDATION) {", False),
    ('        throw new BusinessException("Seul un ticket en attente de validation "', False),
    ('                + "peut être activé (statut actuel : " + ticket.getStatut() + ")");', False),
    ("    }", False),
    ("    ticket.setStatut(StatutTicket.ACTIF);", False),
    ('    auditLogService.log("TICKET_ACTIVATE", "Ticket", ticket.getId(),', False),
    ('            "{\\"numero\\":\\"" + ticket.getNumeroTicket() + "\\",\\"statut\\":\\""', False),
    ('                    + StatutTicket.ACTIF + "\\"}");', False),
    ("    ticket = ticketRepository.save(ticket);", False),
    ('    emailNotificationService.notifierTicket(ticket, "TICKET_VALIDE",', False),
    ('            "Votre ticket est désormais actif : vous pouvez retirer votre "', False),
    ('                    + "engrais au dépôt indiqué.");', False),
    ("    return toResponse(ticket);", False),
    ("}", False),
    ("", False),
    ("A.2 AlerteService.java — Détection d’une rupture de stock", True),
    ("@Transactional", False),
    ("public void verifierDepot(Depot depot, EngraisType engraisType) {", False),
    ("    int stock = stockRepository.findByDepotIdAndEngraisTypeId(", False),
    ("                    depot.getId(), engraisType.getId())", False),
    ("            .map(Stock::getQuantiteDisponible)", False),
    ("            .orElse(0);", False),
    ("", False),
    ("    SeuilAlerte seuil = seuilAlerteRepository", False),
    ("            .findByDepotIdAndEngraisTypeId(depot.getId(), engraisType.getId())", False),
    ("            .orElse(null);", False),
    ("    int seuilMin = seuil != null ? seuil.getSeuilMin()", False),
    ("                                  : depot.getSeuilAlerteMin();", False),
    ("", False),
    ("    if (stock == 0) {", False),
    ("        creerSiAbsente(depot, engraisType, TypeAlerte.RUPTURE,", False),
    ("                NiveauAlerte.CRITICAL,", False),
    ('                "Stock " + engraisType.getNom() + " épuisé au dépôt "', False),
    ("                        + depot.getNom());", False),
    ("    } else if (stock < seuilMin) {", False),
    ("        creerSiAbsente(depot, engraisType, TypeAlerte.STOCK_BAS,", False),
    ("                NiveauAlerte.WARNING,", False),
    ('                "Stock " + engraisType.getNom() + " (" + stock + " sacs) "', False),
    ('                        + "sous le seuil de " + seuilMin);', False),
    ("    }", False),
    ("}", False),
    ("", False),
    ("A.3 AlerteService.java — Création sans doublon", True),
    ("private void creerSiAbsente(Depot depot, EngraisType engraisType,", False),
    ("                            TypeAlerte type, NiveauAlerte niveau,", False),
    ("                            String message) {", False),
    ("    Long depotId = depot.getId();", False),
    ("    Long engraisTypeId = engraisType != null ? engraisType.getId() : null;", False),
    ("    boolean existe = engraisTypeId != null", False),
    ("            && !alerteRepository", False),
    ("                    .findByDepotIdAndEngraisTypeIdAndTypeAndTraiteeFalse(", False),
    ("                            depotId, engraisTypeId, type)", False),
    ("                    .isEmpty();", False),
    ("    if (!existe) {", False),
    ("        alerteRepository.save(Alerte.builder()", False),
    ("                .depot(depot)", False),
    ("                .engraisType(engraisType)", False),
    ("                .type(type)", False),
    ("                .niveau(niveau)", False),
    ("                .message(message)", False),
    ("                .traitee(false)", False),
    ("                .build());", False),
    ("    }", False),
    ("}", False),
]

anchor = doc.paragraphs[start]
for text, is_title in CODE:
    new_p = doc.add_paragraph()
    anchor._p.addnext(new_p._p)
    anchor = new_p
    run = new_p.add_run(text)
    if is_title:
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.bold = True
        new_p.paragraph_format.space_before = Pt(10)
        new_p.paragraph_format.space_after = Pt(4)
        new_p.paragraph_format.line_spacing = 1.15
    else:
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        new_p.paragraph_format.space_before = Pt(0)
        new_p.paragraph_format.space_after = Pt(0)
        new_p.paragraph_format.line_spacing = 1.0
        new_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        # police complexe aussi
        rPr = run._element.get_or_add_rPr()
        rf = rPr.find(qn("w:rFonts"))
        if rf is None:
            rf = rPr.makeelement(qn("w:rFonts"), {})
            rPr.insert(0, rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs"):
            rf.set(qn(a), "Consolas")

doc.save(DOC)
print("mentions FIFO corrigees :", fixed, "| annexe A remplacee :", len(CODE), "lignes")