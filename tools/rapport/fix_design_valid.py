"""Corrections de design - version valide.

Difference cle avec la version precedente : les sectPr intermediaires sont
places DANS le pPr d'un paragraphe (position imposee par le schema OOXML),
et non au niveau du corps du document (ce qui etait invalide et faisait que
Word les supprimait).
"""
import copy
import re
import zipfile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

SRC = '_backup/Rapport_stage_FOMI_canevas.avant_design.docx'
DST = 'Rapport_stage_FOMI_canevas.docx'

d = Document(SRC)
body = d.element.body

# ------------------------------------------------------------------ 1. A4
for s in d.sections:
    s.page_width = Cm(21.0)
    s.page_height = Cm(29.7)
    s.left_margin = Cm(3.0)
    s.right_margin = Cm(2.5)
    s.top_margin = Cm(2.5)
    s.bottom_margin = Cm(2.5)
print('1. A4 + marges : OK')


def txt(el):
    return ''.join(t.text or '' for t in el.iter(qn('w:t'))).strip()


def find_par(pred, label):
    for p in d.paragraphs:
        if pred(p):
            return p
    raise SystemExit('introuvable : ' + label)


# ------------------------------------------- 2. nettoyer la TOC figee
old_toc = [p for p in d.paragraphs if p.style.name.lower().startswith('toc')]
for p in old_toc:
    p._p.getparent().remove(p._p)
print('2. anciens paragraphes TOC supprimes :', len(old_toc))

title_toc = find_par(lambda p: p.text.strip() == 'TABLE DES MATIÈRES', 'TABLE DES MATIÈRES')
intro = find_par(lambda p: p.text.strip() == 'INTRODUCTION GÉNÉRALE', 'INTRODUCTION')

# ------------------------------------------- 3. vrai champ TOC
toc_par = d.add_paragraph(style='toc 1')
tp = toc_par._p


def fld(kind):
    r = OxmlElement('w:r')
    fc = OxmlElement('w:fldChar')
    fc.set(qn('w:fldCharType'), kind)
    r.append(fc)
    return r


tp.append(fld('begin'))
r = OxmlElement('w:r')
it = OxmlElement('w:instrText')
it.set(qn('xml:space'), 'preserve')
it.text = ' TOC \\o "1-3" \\h \\z \\u '
r.append(it)
tp.append(r)
tp.append(fld('separate'))
r = OxmlElement('w:r')
t = OxmlElement('w:t')
t.text = 'Mettre à jour la table des matières (F9).'
r.append(t)
tp.append(r)
tp.append(fld('end'))
title_toc._p.addnext(tp)
print('3. nouveau champ TOC insere')


# ------------------------------------------- 4. sections valides (dans pPr)
def make_sectpr():
    new = copy.deepcopy(d.sections[0]._sectPr)
    for tag in ('w:headerReference', 'w:footerReference', 'w:type', 'w:pgNumType'):
        for el in new.findall(qn(tag)):
            new.remove(el)
    ty = OxmlElement('w:type')
    ty.set(qn('w:val'), 'nextPage')
    new.insert(0, ty)
    return new


def attach_sectpr(par, sectpr):
    """Place sectPr comme dernier enfant du pPr (ordre impose par le schema)."""
    pPr = par._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        par._p.insert(0, pPr)
    for old in pPr.findall(qn('w:sectPr')):
        pPr.remove(old)
    pPr.append(sectpr)


# la section des liminaires se termine au paragraphe qui precede la TOC
prev_before_toc = title_toc._p.getprevious()
while prev_before_toc is not None and prev_before_toc.tag != qn('w:p'):
    prev_before_toc = prev_before_toc.getprevious()
from docx.text.paragraph import Paragraph
attach_sectpr(Paragraph(prev_before_toc, title_toc._parent), make_sectpr())

# la section de la table des matieres se termine au paragraphe du champ TOC
attach_sectpr(toc_par, make_sectpr())

print('4. sections inserees ->', len(d.sections))


# ------------------------------------------- 5. pieds de page numerotes
def make_field(par, instr, size=10):
    def run():
        rr = par.add_run()
        rr.font.name = 'Times New Roman'
        rr.font.size = Pt(size)
        rpr = rr._r.get_or_add_rPr()
        rf = rpr.find(qn('w:rFonts'))
        if rf is None:
            rf = OxmlElement('w:rFonts')
            rpr.insert(0, rf)
        for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
            rf.set(qn(a), 'Times New Roman')
        return rr

    a = run()
    fc = OxmlElement('w:fldChar')
    fc.set(qn('w:fldCharType'), 'begin')
    a._r.append(fc)

    b = run()
    ii = OxmlElement('w:instrText')
    ii.set(qn('xml:space'), 'preserve')
    ii.text = instr
    b._r.append(ii)

    c = run()
    fc = OxmlElement('w:fldChar')
    fc.set(qn('w:fldCharType'), 'separate')
    c._r.append(fc)

    run().text = '1'

    e = run()
    fc = OxmlElement('w:fldChar')
    fc.set(qn('w:fldCharType'), 'end')
    e._r.append(fc)


def reset_footer(footer):
    pars = footer.paragraphs
    for p in pars[1:]:
        p._p.getparent().remove(p._p)
    target = footer.paragraphs[0]
    for r in list(target.runs):
        r._r.getparent().remove(r._r)
    target.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return target


PLAN = [(0, 'lowerRoman', 1), (1, 'lowerRoman', None), (2, 'decimal', 1)]
for idx, fmt, start in PLAN:
    sec = d.sections[idx]
    sec.footer.is_linked_to_previous = False
    par = reset_footer(sec.footer)
    make_field(par, ' PAGE ', 10)

    sectPr = sec._sectPr
    for old in sectPr.findall(qn('w:pgNumType')):
        sectPr.remove(old)
    el = OxmlElement('w:pgNumType')
    el.set(qn('w:fmt'), fmt)
    if start is not None:
        el.set(qn('w:start'), str(start))
    anchor = None
    for tag in ('w:pgMar', 'w:paperSrc', 'w:pgBorders', 'w:lnNumType'):
        f = sectPr.find(qn(tag))
        if f is not None:
            anchor = f
    if anchor is not None:
        anchor.addnext(el)
    else:
        cols = sectPr.find(qn('w:cols'))
        if cols is not None:
            cols.addprevious(el)
        else:
            sectPr.append(el)
    print('   section %d : %s start=%s + champ PAGE' % (idx, fmt, start))

# ------------------------------------------- 6. legendes de tableaux au-dessus
kids = list(body.iterchildren())
moved = 0
for i, el in enumerate(kids):
    if el.tag != qn('w:tbl'):
        continue
    nxt = kids[i + 1] if i + 1 < len(kids) else None
    if nxt is not None and nxt.tag == qn('w:p') and re.match(r'^Tableau\s', txt(nxt)):
        el.addprevious(nxt)
        moved += 1
print('6. legendes de tableaux remontees :', moved)

# ------------------------------------------- 7. image + legende solidaires
kids = list(body.iterchildren())
glued = kept = 0
for el in kids:
    if el.tag != qn('w:p'):
        continue
    pPr = el.find(qn('w:pPr'))
    is_img = el.findall('.//' + qn('w:drawing')) or el.findall('.//' + qn('w:pict'))
    is_cap = re.match(r'^(Figure|Tableau)\s', txt(el))
    if not (is_img or is_cap):
        continue
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        el.insert(0, pPr)
    if pPr.find(qn('w:keepNext')) is None:
        pPr.append(OxmlElement('w:keepNext'))
        if is_img:
            glued += 1
        else:
            kept += 1
print('7. images solidaires : %d | legendes solidaires : %d' % (glued, kept))

# ------------------------------------------- 8. enregistrer
d.save(DST)

with zipfile.ZipFile(DST) as z:
    names = z.namelist()
    data = {n: z.read(n) for n in names}
st = data['word/settings.xml'].decode('utf8')
st = st.replace('w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="14"',
                'w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"')
st = st.replace('<w:useFELayout/>', '')
if '<w:updateFields' not in st:
    i = st.index('>', st.index('<w:settings')) + 1
    st = st[:i] + '<w:updateFields w:val="true"/>' + st[i:]
data['word/settings.xml'] = st.encode('utf8')
with zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.writestr(n, data[n])

print('\nsave ->', DST)
print('sections finales :', len(d.sections))