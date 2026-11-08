# -*- coding: utf-8 -*-
"""Exporte le rapport DOCX en PDF via Word (Windows).

LibreOffice n'est pas installé sur ce poste ; Word l'est, et son moteur
d'export PDF conserve la pagination, les styles et la table des matières.
Le script échoue proprement si Word est absent.

Usage :
    python to_pdf.py [chemin.docx] [chemin.pdf]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

DOCX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "Rapport_stage_FOMI_canevas.docx")
PDF = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "Rapport_stage_FOMI_canevas.pdf")

WD_FORMAT_PDF = 17  # wdFormatPDF


def main():
    try:
        import win32com.client as win32
    except ImportError:
        print("pywin32 est requis : python -m pip install pywin32")
        return 1

    if not os.path.exists(DOCX):
        print(f"Document introuvable : {DOCX}")
        return 1

    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = None
    try:
        doc = word.Documents.Open(os.path.abspath(DOCX), ReadOnly=True, AddToRecentFiles=False)
        # Met à jour la table des matières et les renvois avant l'export.
        for ref in doc.TablesOfContents:
            ref.Update()
        doc.Fields.Update()
        doc.SaveAs(os.path.abspath(PDF), FileFormat=WD_FORMAT_PDF)
        pages = doc.ComputeStatistics(2)  # wdStatisticPages
        print(f"PDF : {PDF}")
        print(f"Pages : {pages}")
        return 0
    finally:
        if doc is not None:
            doc.Close(SaveChanges=0)
        word.Quit()


if __name__ == "__main__":
    sys.exit(main())