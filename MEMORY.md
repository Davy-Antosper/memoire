# Mémoire de session

Dernière mise à jour : 13 août 2026

## Contexte
- Projet : création d'un mémoire PDF (~100 pages) sur le système de gestion et de traçabilité des stocks d'engrais FOMI au Burundi.
- Source : /home/antbeat/fomi.txt (2612 lignes) — cahier des charges : analyse des besoins, acteurs, besoins fonctionnels/non fonctionnels, règles métier (F1-F27, NF1-NF10, R1-R23), 26 cas d'utilisation (UC-01 à UC-26), question de recherche, hypothèses (H1-H6), roadmap en 6 phases.
- Utilisateur : français. Auteur du mémoire : Davy-Antosper.
- Repos GitHub : https://github.com/Davy-Antosper/fomi-stock-api et fomi-stock-web.
- SÉCURITÉ : un token GitHub a été exposé dans fomi.txt — conseiller à l'utilisateur de le révoquer.

## Environnement / outils installés
- Système : Ubuntu 26.04 LTS, utilisateur `antbeat`.
- `sudo` fonctionne avec le mot de passe de l'utilisateur.
- Outils de génération PDF disponibles :
  - pandoc
  - pdflatex (texlive-latex-recommended, texlive-fonts-recommended, texlive-latex-extra)
  - libreoffice-writer
  - reportlab (Python)
  - weasyprint 69.0 (installé via `uv tool install weasyprint`)
- `wkhtmltopdf` : indisponible dans les dépôts Ubuntu 26.04 (pas nécessaire).
- `uv` installé dans ~/.local/bin (chemin à ajouter : `export PATH="$HOME/.local/bin:$PATH"`).

## Analyse du cahier des charges (13/08/2026)
Incohérences à corriger :
- Rôles contradictoires : AGENT_PROVINCIAL (F2) vs AGENT_COLLINE (UC-01).
- UC-08 dupliqué (FOMI historique + Provincial transfert) ; UC-15/UC-17 manquants.
- R14 dupliqué ; F24 manquant ; problème "k" manquant (j→l).
- Références de règles erronées dans UC (R9/R10/R31 = R13/R6/R19-20).
- Cible pages : Phase 6 dit 60-80 pages, objectif utilisateur : 100.
Manquants : diagrammes UML, modèle de données, Swagger, état de l'art, bibliographie.
SÉCURITÉ : token GitHub exposé dans fomi.txt — utilisateur doit le révoquer. Format ticket TKT prédictible → risque scraping.

## À faire
- Corriger les incohérences du cahier des charges.
- Rédiger le mémoire complet (~100 pages).
- Générer le PDF (pandoc/LaTeX ou weasyprint).
