#!/usr/bin/env python3
"""
Script de génération du mémoire FOMI - Gestion des stocks d'engrais
Génère les diagrammes PNG puis le document DOCX (~100 pages)
"""

import os
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memoire_assets")
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# 1. DIAGRAMME D'ARCHITECTURE GÉNÉRALE (3-tiers)
# ============================================================
def draw_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Architecture logicielle du système FOMI-Stock', fontsize=16, fontweight='bold', pad=20)

    def box(x, y, w, h, text, color='#E3F2FD', ec='#1565C0', fontsize=10, bold=False):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor=ec, linewidth=2)
        ax.add_patch(rect)
        weight = 'bold' if bold else 'normal'
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fontsize, fontweight=weight, wrap=True)

    def arrow(x1, y1, x2, y2, label='', color='#1565C0'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx+0.1, my, label, fontsize=8, color=color, style='italic')

    # Client Layer
    box(0.5, 8.5, 3, 1, 'Navigateur Web\n(Frontend React)', '#FFF9C4', '#F9A825', 11, True)
    box(5, 8.5, 3.5, 1, 'Swagger UI\n(Test API)', '#FFF9C4', '#F9A825', 11, True)
    box(9.5, 8.5, 4, 1, 'Application Mobile\n(Futur)', '#FFF9C4', '#F9A825', 11, True)

    # API Layer
    box(1, 6.2, 12, 1.8, '', '#E8F5E9', '#2E7D32')
    ax.text(7, 7.8, 'Couche API REST - Spring Boot 3.3.5 (Java 21)', fontsize=13, fontweight='bold',
            ha='center', color='#1B5E20')

    api_items = ['AuthController\n(JWT)', 'TicketController\n(Gestion tickets)',
                 'MouvementController\n(Réception/Transfert)', 'DistributionController\n(FIFO)',
                 'StockController\n(Stocks)', 'AlerteController\n(Alertes)',
                 'StatsController\n(Statistiques)']
    for i, item in enumerate(api_items):
        x = 1.3 + i * 1.7
        box(x, 6.35, 1.5, 1.1, item, '#C8E6C9', '#388E3C', 7)

    # Security Layer
    box(4, 5.0, 6, 0.9, 'Sécurité : Spring Security + JWT + RBAC\n5 rôles : ADMIN | SUPERVISEUR | AGENT_ZONE | AGENT_COLLINE | AGENT_LOGISTIQUE',
        '#FFECB3', '#FF8F00', 7.5, True)

    # Service Layer
    box(0.5, 3.2, 13, 1.5, '', '#F3E5F5', '#7B1FA2')
    ax.text(7, 4.5, 'Couche Service (Logique métier)', fontsize=13, fontweight='bold',
            ha='center', color='#4A148C')
    svc_items = ['DistributionService\n(FIFO)', 'MouvementService\n(Annulation)',
                 'TicketService\n(Quotas/R6)', 'AlerteService\n(Cron 06h00)',
                 'StockService\n(Gestion FIFO)', 'StatsService\n(Requêtes JPQL)',
                 'AuditLogService\n(Traçabilité)', 'EmailNotification\n(SMTP)']
    for i, item in enumerate(svc_items):
        x = 0.6 + i * 1.6
        box(x, 3.35, 1.45, 1.0, item, '#E1BEE7', '#9C27B0', 6.5)

    # Repository Layer
    box(1, 2.0, 12, 0.9, 'Couche Repository - Spring Data JPA (16 repositories)\nPessimistic locking (SELECT FOR UPDATE) + Requêtes JPQL dynamiques',
        '#E0F7FA', '#00838F', 10, True)

    # Data Layer
    box(1, 0.3, 5.5, 1.4, 'PostgreSQL 16\n16 tables | Enums nommés\nFlyway (12 migrations)\nJSONB pour audit logs',
        '#FCE4EC', '#C62828', 10, True)
    box(7.5, 0.3, 5.5, 1.4, 'Tests automatisés\nTestcontainers + PostgreSQL\nJUnit 5 + Mockito\n218 tests (dont notifications)',
        '#E8EAF6', '#283593', 10, True)

    # Arrows
    arrow(7, 8.5, 7, 8.0, 'HTTPS/REST')
    arrow(7, 5.9, 7, 5.0, 'JWT Token')
    arrow(7, 4.0, 7, 3.2)
    arrow(7, 2.0, 7, 1.7, 'JPA/Hibernate')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/architecture.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ architecture.png")


# ============================================================
# 2. DIAGRAMME ENTITÉ-RELATION (ER)
# ============================================================
def draw_er_diagram():
    """ER diagramme : colonnes empilées sans chevauchement, relations orthogonales.

    Les versions précédentes plaçaient les entités à des ordonnées fixes, ce qui
    faisait chevaucher les boîtes hautes (Depot/Ticket, Lot/Mouvement, etc.) et
    empêchait d'ajouter la colonne email de l'agriculteur.
    """
    fig, ax = plt.subplots(1, 1, figsize=(22, 16))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 19)
    ax.axis('off')
    ax.set_title('Diagramme Entité-Relation du système FOMI-Stock', fontsize=16, fontweight='bold', pad=20)

    W = 3.6
    COL_X = {1: 0.4, 2: 6.0, 3: 11.6, 4: 17.2}
    boxes = {}

    def entity_box(col, name, fields, color, top):
        x = COL_X[col]
        h = 0.35 * len(fields) + 0.6
        y = top - h
        rect = FancyBboxPatch((x, y), W, h, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='#1565C0', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + W/2, y + h - 0.2, name, ha='center', va='center',
                fontsize=9, fontweight='bold', color='#0D47A1')
        ax.plot([x, x+W], [y + h - 0.4, y + h - 0.4], color='#1565C0', linewidth=1)
        for i, f in enumerate(fields):
            ax.text(x + 0.12, y + h - 0.55 - i*0.35, f, fontsize=7, va='center', color='#333')
        boxes[name] = (x, y, W, h)
        return y

    def stack(col, entities, top=18.4, gap=0.55):
        y = top
        for name, fields, color in entities:
            y = entity_box(col, name, fields, color, y) - gap
        return y

    def anchor(name, side, frac=0.5):
        x, y, w, h = boxes[name]
        if side == 'left':
            return (x, y + h*frac)
        if side == 'right':
            return (x + w, y + h*frac)
        if side == 'top':
            return (x + w*frac, y + h)
        return (x + w*frac, y)

    def poly(points, card='', label='', color='#607D8B'):
        ax.plot([p[0] for p in points], [p[1] for p in points],
                color=color, linewidth=1.1, zorder=0)
        if label:
            (x1, y1), (x2, y2) = points[0], points[1]
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.12, label, fontsize=6,
                    ha='center', color=color, style='italic',
                    bbox=dict(boxstyle='round,pad=0.05', facecolor='white', alpha=0.7))
        if card:
            x2, y2 = points[-1]
            x1, y1 = points[-2]
            dx, dy = x2 - x1, y2 - y1
            off = (0.12 if abs(dx) > abs(dy) else 0.0, 0.12 if abs(dy) >= abs(dx) else 0.0)
            ax.text(x2 + off[0], y2 + off[1], card, fontsize=7, ha='center',
                    va='bottom', color=color, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.05', facecolor='white', alpha=0.8))

    def rel(a, sa, fa, b, sb, fb, card='', label='', route=None, color='#607D8B'):
        pts = [anchor(a, sa, fa)] + (route or []) + [anchor(b, sb, fb)]
        poly(pts, card=card, label=label, color=color)

    # Colonne 1 : géographie -> agriculteur -> stock -> distribution -> utilisateur
    stack(1, [
        ('Province', ['id PK', 'code UNIQUE', 'nom'], '#E8EAF6'),
        ('Agriculteur', ['id PK', 'numero_identite UNIQUE', 'nom', 'prenom', 'telephone UNIQUE',
                         'email UNIQUE', 'colline_id FK', 'est_cooperative', 'superficie_ha',
                         'supprime'], '#E8F5E9'),
        ('Stock', ['id PK', 'depot_id FK', 'engrais_type_id FK', 'quantite_disponible', 'updated_at'], '#F1F8E9'),
        ('Distribution', ['id PK', 'ticket_id FK', 'lot_id FK', 'depot_id FK', 'quantite',
                          'agent_id FK', 'date_distribution', 'reference_mouvement_id FK'], '#FFEBEE'),
        ('Utilisateur', ['id PK', 'username UNIQUE', 'password_hash', 'nom_complet', 'role (enum)',
                         'depot_id FK', 'zone_id FK', 'province_id FK', 'actif', 'supprime'], '#F3E5F5'),
    ])

    # Colonne 2 : zone -> engrais -> stock_lot
    stack(2, [
        ('Zone', ['id PK', 'code UNIQUE', 'nom', 'province_id FK'], '#E8EAF6'),
        ('EngraisType', ['id PK', 'code UNIQUE', 'nom', 'poids_sac_kg', 'prix_subventionne', 'actif'], '#FCE4EC'),
        ('StockLot', ['id PK', 'depot_id FK', 'lot_id FK', 'quantite', 'updated_at'], '#F1F8E9'),
    ])

    # Colonne 3 : colline -> lot -> mouvement -> audit
    stack(3, [
        ('Colline', ['id PK', 'code UNIQUE', 'nom', 'zone_id FK'], '#E8EAF6'),
        ('Lot', ['id PK', 'numero_lot UNIQUE', 'engrais_type_id FK', 'quantite_initiale',
                 'date_fabrication', 'date_peremption', 'date_reception_fomi'], '#FCE4EC'),
        ('Mouvement', ['id PK', 'type (enum)', 'lot_id FK', 'engrais_type_id FK', 'depot_source_id FK',
                       'depot_dest_id FK', 'quantite', 'agent_id FK', 'ticket_id FK', 'commentaire',
                       'date_mouvement', 'idempotency_key', 'annule', 'motif_annulation',
                       'annule_par_id FK', 'reference_annulation_id FK'], '#FFEBEE'),
        ('AuditLog', ['id PK', 'utilisateur_id FK', 'action', 'entity_type', 'entity_id',
                      'ip_address', 'details_json (JSONB)', 'created_at'], '#EFEBE9'),
    ])

    # Colonne 4 : dépôt -> ticket -> alerte -> seuil
    stack(4, [
        ('Depot', ['id PK', 'code UNIQUE', 'nom', 'niveau (enum)', 'province_id FK', 'zone_id FK',
                   'colline_id FK', 'seuil_alerte_min', 'capacite_max', 'supprime', 'deleted_at'], '#FFF3E0'),
        ('Ticket', ['id PK', 'numero_ticket UNIQUE', 'agriculteur_id FK', 'engrais_type_id FK',
                    'quantite_commandee', 'quantite_servie', 'montant_paye', 'date_paiement',
                    'depot_retrait_id FK', 'statut (enum)', 'saison', 'superficie_ha', 'supprime'], '#FFF3E0'),
        ('Alerte', ['id PK', 'depot_id FK', 'engrais_type_id FK', 'type (enum)', 'message',
                    'niveau (enum)', 'traitee', 'created_at'], '#FFF9C4'),
        ('SeuilAlerte', ['id PK', 'depot_id FK', 'engrais_type_id FK', 'seuil_min', 'criticite'], '#FFF9C4'),
    ])

    # Relations entre colonnes adjacentes
    rel('Province', 'right', 0.5, 'Zone', 'left', 0.5, '1:N')
    rel('Zone', 'right', 0.5, 'Colline', 'left', 0.5, '1:N')
    rel('Colline', 'right', 0.5, 'Depot', 'left', 0.8, '0..1:N')
    rel('EngraisType', 'right', 0.5, 'Lot', 'left', 0.35, '1:N',
        route=[(10.6, anchor('EngraisType', 'right', 0.5)[1])])
    rel('Lot', 'left', 0.5, 'StockLot', 'right', 0.5, '1:N',
        route=[(10.6, anchor('Lot', 'left', 0.5)[1])])

    # Relations dans la colonne 4 (dépôt -> ticket -> alerte)
    rel('Depot', 'right', 0.45, 'Ticket', 'right', 0.6, '1:N',
        route=[(21.2, anchor('Depot', 'right', 0.45)[1])])
    rel('Depot', 'left', 0.55, 'Mouvement', 'right', 0.75, '1:N',
        route=[(16.2, anchor('Depot', 'left', 0.55)[1])])
    rel('Depot', 'right', 0.15, 'Alerte', 'right', 0.5, '1:N',
        route=[(21.4, anchor('Depot', 'right', 0.15)[1])])

    # Relations longues routées par les marges (aucune traversée de boîte)
    rel('Agriculteur', 'right', 0.35, 'Ticket', 'right', 0.35, '1:N',
        route=[(5.0, anchor('Agriculteur', 'right', 0.35)[1]), (5.0, 18.8),
               (21.6, 18.8), (21.6, anchor('Ticket', 'right', 0.35)[1])])
    rel('Ticket', 'right', 0.1, 'Distribution', 'right', 0.5, '1:N',
        route=[(21.4, anchor('Ticket', 'right', 0.1)[1]), (21.4, 0.25),
               (5.0, 0.25), (5.0, anchor('Distribution', 'right', 0.5)[1])])
    rel('Utilisateur', 'left', 0.6, 'AuditLog', 'left', 0.5, '1:N',
        route=[(0.15, anchor('Utilisateur', 'left', 0.6)[1]), (0.15, 18.95),
               (10.6, 18.95), (10.6, anchor('AuditLog', 'left', 0.5)[1])])

    ax.text(0.4, 0.02, 'Les cardinalités sont indiquées à l’extrémité de chaque relation ; '
                       'la colonne email (V12) est unique et nullable.',
            fontsize=7, color='#666', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/er_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ er_diagram.png")


# ============================================================
# 3. DIAGRAMME DE SÉQUENCE - Distribution FIFO
# ============================================================
def draw_sequence_distribution():
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Diagramme de séquence - Distribution FIFO des engrais', fontsize=14, fontweight='bold', pad=15)

    actors = ['Agent', 'Controller', 'DistributionService', 'StockService', 'Repository', 'AlerteService']
    xs = [1, 3.5, 6.5, 9.5, 12, 14]
    colors = ['#FF8A65', '#4FC3F7', '#81C784', '#FFB74D', '#CE93D8', '#F06292']

    for i, (name, x) in enumerate(zip(actors, xs)):
        rect = FancyBboxPatch((x-0.6, 11), 1.2, 0.5, boxstyle="round,pad=0.05",
                              facecolor=colors[i], edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 11.25, name, ha='center', va='center', fontsize=8, fontweight='bold')
        ax.plot([x, x], [0.5, 11], color='#CCC', linewidth=1, linestyle='--')

    messages = [
        (0, 1, 'POST /api/distributions', 10.5),
        (1, 2, 'distribuer(req, agent)', 10.0),
        (2, 3, 'sortirFifo(depot, type, qty, lotIdForce)', 9.5),
        (3, 4, 'findByDepotId...OrderByLotDateReceptionFomiAsc\n+ filtre des lots non périmés', 9.0),
        (4, 3, 'List<LotSortie>', 8.5),
        (3, 2, 'Quantités décrémentées', 8.0),
        (2, 4, 'MouvementRepository.save(DISTRIBUTION)', 7.5),
        (2, 4, 'DistributionRepository.save()', 7.0),
        (2, 4, 'TicketRepository.save()\n(mettreAJourStatut : SERVI/PARTIEL)', 6.5),
        (2, 5, 'verifierDepot(depot, type)', 6.0),
        (5, 5, 'Vérif STOCK_BAS, RUPTURE\nPEREMPTION, INACTIVITÉ', 5.5),
        (2, 1, 'List<DistributionResponse>', 5.0),
    ]

    for src, dst, label, y in messages:
        x1, x2 = xs[src], xs[dst]
        ax.annotate('', xy=(x2, y-0.1), xytext=(x1, y-0.1),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
        mx = (x1 + x2) / 2
        ax.text(mx, y + 0.15, label, fontsize=7, ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.9))

    # Activation bars
    for i, x in enumerate(xs):
        if i in [1, 2, 3]:
            rect = plt.Rectangle((x-0.15, 5.0), 0.3, 5.5, facecolor=colors[i], alpha=0.3)
            ax.add_patch(rect)

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/sequence_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ sequence_distribution.png")


# ============================================================
# 4. DIAGRAMME DE SÉQUENCE - Création ticket
# ============================================================
def draw_sequence_ticket():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Diagramme de séquence - Création et validation d\'un ticket', fontsize=14, fontweight='bold', pad=15)

    actors = ['Agent', 'TicketController', 'TicketService', 'Superviseur']
    xs = [1.5, 4.5, 7.5, 11]
    colors = ['#FF8A65', '#4FC3F7', '#81C784', '#FFB74D']

    for i, (name, x) in enumerate(zip(actors, xs)):
        rect = FancyBboxPatch((x-0.7, 9.2), 1.4, 0.5, boxstyle="round,pad=0.05",
                              facecolor=colors[i], edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 9.45, name, ha='center', va='center', fontsize=9, fontweight='bold')
        ax.plot([x, x], [0.5, 9.2], color='#CCC', linewidth=1, linestyle='--')

    messages = [
        (0, 1, 'POST /api/tickets\n{saison, numero, agriculteurId, ...}', 8.7),
        (1, 2, 'creer(request)', 8.2),
        (2, 2, 'Vérifier unicité numero_ticket\n+ quota superficie × 150 kg/ha (R6, R22)\n+ pas de doublon même saison/type', 7.5),
        (2, 2, 'Sauvegarder ticket\nstatut = EN_ATTENTE_DE_VALIDATION', 6.5),
        (2, 2, 'AuditLog: TICKET_CREATE', 6.0),
        (1, 0, 'TicketResponse\n{statut: EN_ATTENTE_DE_VALIDATION}', 5.5),
        (3, 1, 'PATCH /api/tickets/{id}/activer', 4.7),
        (1, 2, 'activer(id)', 4.2),
        (2, 2, 'Vérifier statut == EN_ATTENTE_DE_VALIDATION\n→ statut = ACTIF', 3.5),
        (2, 2, 'AuditLog: TICKET_ACTIVATE', 3.0),
        (1, 3, 'TicketResponse {statut: ACTIF}', 2.5),
    ]

    for src, dst, label, y in messages:
        x1, x2 = xs[src], xs[dst]
        if src == dst:
            ax.plot([x1-0.3, x1+0.3, x1+0.3, x1-0.3, x1-0.3],
                    [y+0.1, y+0.1, y-0.3, y-0.3, y+0.1], color='#333', linewidth=1.5)
            ax.text(x1+0.5, y-0.1, label, fontsize=7, va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF9C4', alpha=0.9))
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
            mx = (x1 + x2) / 2
            ax.text(mx, y + 0.2, label, fontsize=7, ha='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/sequence_ticket.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ sequence_ticket.png")


# ============================================================
# 5. DIAGRAMME RBAC
# ============================================================
def draw_rbac():
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Matrice RBAC - Contrôle d\'accès basé sur les rôles', fontsize=14, fontweight='bold', pad=15)

    roles = ['ADMIN', 'SUPERVISEUR', 'AGENT_ZONE', 'AGENT_COLLINE', 'AGENT_LOGISTIQUE']
    perms = [
        'CRUD Utilisateurs',
        'CRUD Dépôts',
        'CRUD EngraisType',
        'Reception FOMI',
        'Transfert inter-dépôt',
        'Créer/Modifier Ticket',
        'Activer/Rejeter Ticket',
        'Distribuer (FIFO)',
        'Annuler Mouvement',
        'Voir Statistiques',
        'Export CSV',
        'Gérer Seuils Alerte',
    ]

    matrix = [
        [1,1,1,1,1,1,1,1,1,1,1,1],  # ADMIN
        [0,0,0,0,0,0,1,1,1,1,1,0],  # SUPERVISEUR
        [0,0,0,0,0,1,0,1,0,0,1,0],  # AGENT_ZONE
        [0,0,0,0,0,1,0,1,0,0,0,0],  # AGENT_COLLINE
        [0,0,0,1,0,0,0,0,0,0,1,0],  # AGENT_LOGISTIQUE
    ]

    cell_w = 1.1
    cell_h = 0.55
    x0 = 2.5
    y0 = 9

    # Headers
    for j, perm in enumerate(perms):
        ax.text(x0 + j*cell_w + cell_w/2, y0 + 0.1, perm, fontsize=6.5, ha='center', va='bottom',
                rotation=45, fontweight='bold', color='#333')

    for i, role in enumerate(roles):
        y = y0 - (i+1)*cell_h
        ax.text(x0 - 0.1, y + cell_h/2, role, fontsize=9, ha='right', va='center', fontweight='bold',
                color='#1565C0')
        for j in range(len(perms)):
            x = x0 + j*cell_w
            if matrix[i][j]:
                color = '#4CAF50'
                symbol = '✓'
            else:
                color = '#FFCDD2'
                symbol = '✗'
            rect = FancyBboxPatch((x, y), cell_w, cell_h, boxstyle="round,pad=0.02",
                                  facecolor=color, edgecolor='#DDD', linewidth=0.5, alpha=0.7)
            ax.add_patch(rect)
            ax.text(x + cell_w/2, y + cell_h/2, symbol, ha='center', va='center',
                    fontsize=10, color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/rbac_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ rbac_matrix.png")


# ============================================================
# 6. CIRCUIT DE DISTRIBUTION FOMI
# ============================================================
def draw_distribution_circuit():
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Circuit de distribution des engrais FOMI au Burundi', fontsize=14, fontweight='bold', pad=15)

    def box(x, y, w, h, text, color, fontsize=9, bold=False):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        weight = 'bold' if bold else 'normal'
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize, fontweight=weight)

    def arrow(x1, y1, x2, y2, label='', color='#1565C0'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.2, label, fontsize=8, ha='center', color=color, fontweight='bold')

    # Chain
    box(0.2, 5, 2.5, 1.5, 'Usine FOMI\nMaramvya\nProduction', '#FFCDD2', 10, True)
    box(3.5, 5, 2.5, 1.5, 'BPEAE\nDépôt Provincial\n(5 provinces)', '#C8E6C9', 9, True)
    box(6.8, 5, 2.5, 1.5, 'Chefs de Zone\nDépôt Zonal\n(~450 zones)', '#BBDEFB', 9, True)
    box(10.1, 5, 2.5, 1.5, 'Chefs de Colline\nDépôt Collinaire\n(3 041 collines)', '#D1C4E9', 9, True)
    box(13.4, 5, 2.4, 1.5, 'Agriculteurs\nBénéficiaires\n(~865 000)', '#FFE0B2', 9, True)

    arrow(2.7, 5.75, 3.5, 5.75, 'Réception FOMI')
    arrow(6, 5.75, 6.8, 5.75, 'Transfert')
    arrow(9.3, 5.75, 10.1, 5.75, 'Distribution')
    arrow(12.6, 5.75, 13.4, 5.75, 'Remise')

    # Bottom: paiement flow
    box(1, 2, 3, 1.2, 'Agriculteur\nPaiement avance\n(50% du prix)', '#FFF9C4', 9)
    box(5, 2, 3, 1.2, 'Microfinance\n(Poste / FENACOBU)\nEncaissement', '#E1F5FE', 9)
    box(9, 2, 3.5, 1.2, 'Système FOMI-Stock API\nGénération ticket\nSuivi en temps réel', '#F3E5F5', 9, True)
    box(13, 2, 2.8, 1.2, 'Superviseur\nValidation\nActivation ticket', '#E8F5E9', 9)

    arrow(4, 2.6, 5, 2.6, 'Paiement')
    arrow(8, 2.6, 9, 2.6, 'Ticket')
    arrow(12.5, 2.6, 13, 2.6, 'Validation')

    # PNSEB subsidy
    ax.text(8, 0.8, 'Programme PNSEB : Subvention gouvernementale 64-74% du prix │ FCFA : Fonds Commun pour les Fertilisants',
            fontsize=9, ha='center', color='#666', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F5F5', edgecolor='#CCC'))

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/distribution_circuit.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ distribution_circuit.png")


# ============================================================
# 7. ARCHITECTURE EN COUCHES (détaillée)
# ============================================================
def draw_layered_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Architecture en couches du système FOMI-Stock', fontsize=14, fontweight='bold', pad=15)

    layers = [
        (0.5, 8.0, 13, 1.5, 'PRÉSENTATION', 'Navigateur Web (React) │ Swagger UI │ Applications Mobiles', '#E3F2FD', '#1565C0'),
        (0.5, 6.2, 13, 1.5, 'API REST', '17 Controllers Spring MVC │ Endpoints HTTP │ Validation @Valid │ OpenAPI/Swagger', '#E8F5E9', '#2E7D32'),
        (0.5, 4.4, 13, 1.5, 'SÉCURITÉ', 'Spring Security │ JWT (HMAC-SHA) │ Filtre d\'authentification │ RBAC 5 rôles', '#FFF3E0', '#E65100'),
        (0.5, 2.6, 13, 1.5, 'SERVICES', 'DistributionService (FIFO) │ TicketService (Quotas R6/R22) │ AlerteService (Cron)\nStockService │ MouvementService │ StatsService │ AuditLogService │ EmailNotificationService (SMTP)', '#F3E5F5', '#7B1FA2'),
        (0.5, 1.0, 6, 1.3, 'REPOSITORIES', 'Spring Data JPA │ 16 Repositories\nRequêtes JPQL │ Pessimistic Locking', '#FCE4EC', '#C62828'),
        (7.5, 1.0, 6, 1.3, 'MODÈLE DOMAINE', '16 Entités JPA │ 6 Enums PostgreSQL\n30+ DTOs (Records Java) │ email agriculteur', '#EFEBE9', '#5D4037'),
        (0.5, 0.0, 13, 0.7, 'INFRASTRUCTURE', 'PostgreSQL 16 │ Flyway (12 migrations) │ SMTP (Mailpit/Mailjet) │ Docker │ GitHub Actions │ Railway CI/CD', '#263238', '#FFF'),
    ]

    for x, y, w, h, title, desc, bg, ec in layers:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=bg, edgecolor=ec, linewidth=2)
        ax.add_patch(rect)
        sombre = ec == '#FFF'
        tc = '#FFFFFF' if sombre else ec
        ax.text(x + 0.3, y + h - 0.3, title, fontsize=11, fontweight='bold', color=tc)
        ax.text(x + 0.3, y + h/2 - 0.2, desc, fontsize=8, color='#E0E0E0' if sombre else '#555')

    # Arrows between layers
    for y in [7.7, 5.9, 4.1, 2.3]:
        ax.annotate('', xy=(7, y), xytext=(7, y+0.3),
                    arrowprops=dict(arrowstyle='<->', color='#999', lw=1.5))

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/layered_architecture.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ layered_architecture.png")


# ============================================================
# 8. DIAGRAMME D'ÉTAT - Cycle de vie du ticket
# ============================================================
def draw_ticket_state_machine():
    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('Machine à états du ticket de distribution', fontsize=14, fontweight='bold', pad=15)

    def state(x, y, text, color='#E3F2FD', ec='#1565C0', w=2.0, h=0.9, fontsize=8):
        rect = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor=ec, linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold')

    def trans(p1, p2, label, rad=0.0, color='#333', ls='-', lx=None, ly=None, fontsize=7):
        ax.annotate('', xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5, linestyle=ls,
                                    connectionstyle=f"arc3,rad={rad}"))
        if label:
            mx = lx if lx is not None else (p1[0] + p2[0]) / 2
            my = ly if ly is not None else (p1[1] + p2[1]) / 2
            ax.text(mx, my, label, fontsize=fontsize, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF9C4', edgecolor='#CCC'))

    # État initial (pseudo-état)
    ax.add_patch(plt.Circle((0.6, 7.0), 0.12, facecolor='#333', edgecolor='#333', zorder=5))

    # États principaux
    state(3.0, 7.0, 'EN_ATTENTE_DE\nVALIDATION', '#BBDEFB', w=2.5)
    state(6.8, 7.0, 'ACTIF', '#A5D6A7', w=1.7)
    state(10.3, 7.0, 'PARTIEL', '#FFCC80', w=1.8)
    state(13.7, 7.0, 'SERVI', '#81C784', w=1.7)
    state(4.6, 4.5, 'REJETE', '#EF9A9A', w=1.8)
    state(8.6, 3.0, 'ANNULE', '#E0E0E0', w=1.8)
    state(2.5, 2.2, 'EXPIRE', '#BDBDBD', w=1.8)

    # Transitions
    trans((0.75, 7.0), (1.55, 7.0), '')
    trans((4.2, 7.0), (5.85, 7.0), 'activer()\n(SUPERVISEUR)')
    trans((7.7, 7.0), (9.3, 7.0), 'distribution\npartielle')
    trans((11.3, 7.0), (12.75, 7.0), 'solde\ndistribué')
    trans((6.8, 7.4), (13.7, 7.4),
          'distribution totale (quantité servie ≥ quantité commandée)',
          rad=-0.35, ly=8.35)
    trans((3.0, 6.55), (4.3, 4.95), 'rejeter(motif)', rad=0.15, lx=3.3, ly=5.4)
    trans((6.8, 6.55), (7.9, 3.5), 'annuler()\n(ACTIF/PARTIEL)', rad=-0.15, lx=6.9, ly=5.1)
    trans((10.3, 6.55), (9.2, 3.5), '', rad=0.15)
    trans((2.5, 6.55), (2.5, 2.65), 'expirerTickets(saison)\n(tickets non servis)',
          rad=-0.25, lx=1.35, ly=4.6)

    # États hérités de l'énumération StatutTicket
    legacy = FancyBboxPatch((11.9, 1.2), 3.8, 2.6, boxstyle="round,pad=0.1",
                            facecolor='#FAFAFA', edgecolor='#9E9E9E', linewidth=1.5, linestyle='--')
    ax.add_patch(legacy)
    ax.text(13.8, 3.55, 'États hérités', ha='center', fontsize=8, fontweight='bold', color='#616161')
    state(12.85, 2.85, 'PAYE', '#ECEFF1', ec='#9E9E9E', w=1.5, h=0.55, fontsize=7)
    state(14.85, 2.85, 'EN_ATTENTE', '#ECEFF1', ec='#9E9E9E', w=1.5, h=0.55, fontsize=6.5)
    state(13.85, 1.85, 'RECLAMATION', '#ECEFF1', ec='#9E9E9E', w=1.7, h=0.55, fontsize=6.5)
    ax.text(13.8, 1.35, 'acceptés à la distribution, non produits par creer()',
            ha='center', fontsize=6, color='#757575', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/ticket_state_machine.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ ticket_state_machine.png")


# ============================================================
# 9. FLOWCHART FIFO
# ============================================================
def draw_fifo_flowchart():
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Algorithme FIFO de distribution des engrais', fontsize=14, fontweight='bold', pad=15)

    def diamond(x, y, w, h, text, color='#FFF9C4'):
        pts = [(x, y+h/2), (x+w/2, y+h), (x+w, y+h/2), (x+w/2, y)]
        poly = plt.Polygon(pts, facecolor=color, edgecolor='#F57F17', linewidth=2)
        ax.add_patch(poly)
        ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=8, fontweight='bold')

    def process(x, y, w, h, text, color='#E3F2FD'):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#1565C0', linewidth=2)
        ax.add_patch(rect)
        ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=8)

    def arrow(x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx+0.1, my, label, fontsize=7, color='#333')

    # Flow
    process(4, 10.5, 6, 0.8, 'Début : demande de distribution', '#C8E6C9')
    arrow(7, 10.5, 7, 10.0)

    diamond(3.2, 9.0, 7.6, 0.9,
            'Ticket distribuable ?\n(ACTIF, PARTIEL, PAYE ou EN_ATTENTE)')
    arrow(7, 9.0, 7, 8.5, 'Oui')
    arrow(10.8, 9.45, 12, 9.45, 'Non')
    ax.text(12, 9.7, '✗ Statut incompatible', fontsize=8, color='red')

    process(4, 7.5, 6, 0.8, 'Vérifier le périmètre de l\'agent\n(Colline → Dépôt → Zone)')
    arrow(7, 7.5, 7, 7.0)

    process(3.6, 6.0, 6.8, 0.9,
            'Récupérer les lots du dépôt\n(quantité > 0 et lots non périmés)\nTrier par dateReceptionFomi croissante')
    arrow(7, 6.0, 7, 5.5)

    diamond(4, 4.6, 6, 0.8, 'quantité restante > 0?')
    arrow(7, 4.6, 7, 4.1, 'Oui')
    arrow(10, 5.0, 12, 5.0, 'Non → SERVI')
    ax.text(12, 5.3, '✓ Ticket complet', fontsize=8, color='green')

    process(3, 2.6, 8, 0.9,
            'Pour chaque lot : pris = min(stock du lot, restant)\nDécrémenter StockLot et Stock\nPasser au lot suivant')
    arrow(7, 2.6, 7, 2.1)

    process(4, 1.0, 6, 0.8,
            'Créer Mouvement(DISTRIBUTION)\n+ Distribution + MAJ Ticket\n+ AuditLog + Vérifier alertes', '#F3E5F5')
    arrow(7, 1.0, 7, 0.55)

    process(4.5, 0.0, 5, 0.45, 'Fin', '#EF9A9A')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/fifo_flowchart.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ fifo_flowchart.png")


# ============================================================
# 10. CHRONOLOGIE FOMI
# ============================================================
def draw_fomi_timeline():
    fig, ax = plt.subplots(1, 1, figsize=(16, 6))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('Chronologie historique de FOMI et du projet', fontsize=14, fontweight='bold', pad=15)

    events = [
        (1, 3, '2018', 'Étude de\nfaisabilité\nPAPAB', '#E3F2FD'),
        (3, 3, '2019', 'Création FOMI\nInterdiction\nimport engrais', '#C8E6C9'),
        (5, 3, '2021', 'ISO 9001/14001\n3 500 emplois\n500 t/jour', '#BBDEFB'),
        (7, 3, '2023', 'Scandale\nprix + pénurie\nRéforme admin', '#FFF9C4'),
        (9, 3, '2025', 'Crise financière\n368M$ dette\nScandale 74B FBu', '#FFCDD2'),
        (11, 3, '2026', 'Début projet\nFOMI-Stock API\nConformité CDC', '#F3E5F5'),
    ]

    ax.plot([0.5, 14.5], [3, 3], color='#1565C0', linewidth=3, zorder=1)

    for x, y, year, desc, color in events:
        ax.plot(x, 3, 'o', color='#1565C0', markersize=12, zorder=2)
        rect = FancyBboxPatch((x-0.8, 3.5), 1.6, 1.5, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#1565C0', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 4.7, year, ha='center', va='center', fontsize=10, fontweight='bold', color='#0D47A1')
        ax.text(x, 3.85, desc, ha='center', va='center', fontsize=7)

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/fomi_timeline.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ fomi_timeline.png")


# ============================================================
# DIAGRAMME DE CLASSES UML (Classes principales du système)
# ============================================================
def draw_class_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(18, 13))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 13.4)
    ax.axis('off')
    ax.set_title('Diagramme de classes — Entités et relations', fontsize=14, fontweight='bold', pad=15)

    def cls_box(x, y, w, h, title, attrs, ops):
        # Hauteur calculée pour que les attributs ET les méthodes tiennent dans
        # la boîte (l'ancienne formule faisait chevaucher les deux sections).
        h = max(h, 0.75 + 0.28*len(attrs) + 0.30*len(ops) + 0.15)
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                              facecolor='#FCE4EC', edgecolor='#C62828', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.2, title, ha='center', fontsize=9, fontweight='bold', color='#C62828')
        # separator line
        ax.plot([x, x+w], [y + h - 0.4, y + h - 0.4], color='#C62828', lw=1)
        # attributes
        for i, a in enumerate(attrs):
            ax.text(x + 0.1, y + h - 0.62 - i*0.28, a, fontsize=6.5, va='center', color='#333')
        # methods separator : juste sous le dernier attribut
        y_sep = y + h - 0.62 - 0.28*(len(attrs) - 1) - 0.17
        ax.plot([x, x+w], [y_sep, y_sep], color='#C62828', lw=0.5)
        for i, o in enumerate(ops):
            ax.text(x + 0.1, y_sep - 0.28 - i*0.26, o, fontsize=6, va='center', color='#1565C0', style='italic')
        return (x + w/2, y + h/2)

    # Key entities with representative attributes/methods
    cls_box(0.3, 9.5, 2.5, 2.2, 'Ticket', ['id: Long', 'numeroTicket: String', 'statut: StatutTicket', 'quantiteServie: Integer', 'agriculteur: Agriculteur'], ['getQuantiteRestante()', 'mettreAJourStatut()'])
    cls_box(3.5, 9.5, 2.5, 2.0, 'Agriculteur', ['id: Long', 'numeroIdentite: String', 'telephone: String', 'email: String', 'superficieHa: BigDecimal', 'colline: Colline'], ['creer()', 'rechercherParTelephone()'])
    cls_box(6.8, 9.5, 2.5, 2.2, 'Mouvement', ['id: Long', 'type: TypeMouvement', 'quantite: Integer', 'agent: Utilisateur', 'dateMouvement: LocalDateTime', 'idempotencyKey: String'], ['annuler()', 'restaurerStock()'])
    cls_box(10, 9.5, 2.5, 2.0, 'Distribution', ['id: Long', 'ticket: Ticket', 'lot: Lot', 'quantite: Integer', 'agent: Utilisateur', 'dateDistribution: LocalDateTime'], ['distribuer()', 'annuler()'])
    cls_box(13.5, 9.5, 2.5, 2.4, 'Utilisateur', ['id: Long', 'username: String', 'passwordHash: String', 'role: RoleUtilisateur', 'depot: Depot', 'zone: Zone', 'province: Province'], ['getAuthorities()', 'isAccountNonExpired()'])

    # Second row
    cls_box(0.3, 5.8, 2.5, 2.0, 'Lot', ['id: Long', 'numeroLot: String', 'dateFabrication: LocalDate', 'datePeremption: LocalDate', 'dateReceptionFomi: LocalDateTime', 'quantiteInitiale: Integer'], ['estPerime()', 'verifierCapacite()'])
    cls_box(3.5, 5.8, 2.5, 2.0, 'Depot', ['id: Long', 'code: String', 'nom: String', 'niveau: NiveauDepot', 'province/zone/colline: FK'], ['verifierCapacite()', 'verifierPerimetre()'])
    cls_box(6.8, 5.8, 2.5, 2.4, 'Stock', ['id: Long', 'depot: Depot', 'engraisType: EngraisType', 'quantiteDisponible: Integer', 'updatedAt: LocalDateTime'], ['mettreAJourQuantite()', 'verifierSeuil()'])
    cls_box(10, 5.8, 2.5, 2.0, 'StockLot', ['id: Long', 'depot: Depot', 'lot: Lot', 'quantite: Integer', 'updatedAt: LocalDateTime'], ['verifierLotPerime()', 'decrementer()'])

    # Third row
    cls_box(3, 1.6, 2.5, 1.5, 'Alerte', ['id: Long', 'depot: Depot', 'type: TypeAlerte', 'niveau: NiveauAlerte', 'traitee: Boolean', 'message: String'], ['creerSiAbsente()', 'traiter()'])
    cls_box(6.8, 1.6, 2.5, 2.0, 'AuditLog', ['id: Long', 'utilisateur: Utilisateur', 'action: String', 'entityType: String', 'detailsJson: JSONB', 'ipAddress: String'], ['log()'])
    cls_box(10, 1.6, 2.5, 1.5, 'SeuilAlerte', ['id: Long', 'depot: Depot', 'engraisType: EngraisType', 'seuilMin: Integer', 'criticite: String'], ['verifierSeuil()'])

    # Relationships (simplified UML associations)
    def rel_line(x1, y1, x2, y2, label='', color='#1565C0', style='-'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my+0.15, label, fontsize=7, ha='center', va='bottom', color=color,
                    bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8))

    rel_line(2.8, 10.9, 3.5, 10.9, 'N:1')
    rel_line(2.8, 7.0, 3.5, 7.0, '1:N', '#7B1FA2')
    rel_line(9.3, 7.0, 10.0, 7.0, '1:N', '#333')
    rel_line(4.4, 5.8, 4.4, 4.78, '1:N', '#333')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/class_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ class_diagram.png")

# ============================================================
# DIAGRAMME DE DÉPLOIEMENT (3 niveaux : Client / API / DB)
# ============================================================
def draw_deployment_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('Diagramme de déploiement — FOMI-Stock', fontsize=14, fontweight='bold', pad=15)

    def node(x, y, w, h, label, sublabel='', color='#E3F2FD', ec='#1565C0'):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor=ec, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.55, label, fontsize=11, fontweight='bold', ha='center', va='center', color=ec)
        ax.text(x + w/2, y + h*0.3, sublabel, fontsize=7, ha='center', va='center', color='#555')

    # Client tier
    node(0.5, 7.5, 2.5, 1.2, 'Client Web', 'React / Vite / PWA', '#FFF9C4', '#F9A825')
    node(4, 7.5, 2.5, 1.2, 'Client Mobile', 'Expo SDK 57 / RN', '#FFF9C4', '#F9A825')
    node(8, 7.5, 2.5, 1.2, 'Swagger UI', 'API doc / Test', '#FFF9C4', '#F9A825')

    # Middle tier: Railway / Docker
    node(0.5, 4.5, 14.5, 2.0, 'Serveur API (Railway Docker)', 'Java 21 / Spring Boot 3.3.5 / PostgreSQL 16 / JWT / RBAC / Flyway\nImage Docker multi-étapes (JRE 21) / Port 8080 / CI GitHub Actions', '#E8F5E9', '#2E7D32')

    # DB tier
    node(3.2, 1.5, 4.6, 1.5, 'PostgreSQL 16', '16 tables + enums / JSONB audit / Index B-tree et composites / Migrations Flyway V1→V12', '#FCE4EC', '#C62828')
    node(8.4, 1.5, 3.0, 1.5, 'Testcontainers', 'PostgreSQL 16-alpine / JUnit 5 / 218 tests / Docker Java 1.44', '#E8EAF6', '#283593')
    node(12.0, 1.5, 3.2, 1.5, 'Serveur SMTP', 'Notifications email / SMTP 1025 (Mailpit) / Mailjet en production', '#E0F2F1', '#00695C')

    # Connections
    def conn(x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my+0.1, label, fontsize=7, ha='center', bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8))

    # Client -> API
    conn(3.0, 7.0, 7.5, 5.7, 'HTTPS / REST')
    conn(6.5, 7.0, 7.5, 5.7, 'HTTPS / REST')
    conn(10.75, 7.0, 7.5, 5.7, 'HTTPS / REST')
    # API -> DB
    conn(4, 4.5, 5.0, 3.2, 'JDBC / JPA')
    # API -> SMTP
    conn(12.5, 4.5, 13.6, 3.2, 'SMTP / TLS')
    # DB -> Testcontainers
    conn(7.8, 1.5, 8.4, 1.5, 'Docker')
    # CI note
    ax.text(8, 0.2, 'Déploiement CI/CD : GitHub Actions (build + test 218) → Docker build → Railway (auto-deploy sur push main)', fontsize=7, ha='center', color='#555', style='italic', bbox=dict(boxstyle='round,pad=0.2', facecolor='#F5F5F5', edgecolor='#CCC'))

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/deployment_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ deployment_diagram.png")

# ============================================================
# DIAGRAMME DE CAS D'UTILISATION (UML Use Case)
# ============================================================
def draw_use_case_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Diagramme de cas d\'utilisation - Acteurs et fonctionnalites principales', fontsize=14, fontweight='bold', pad=15)

    # Actor positions
    actors = [
        (1.5, 8.5, 'ADMIN\n(Système)', '#FCE4EC'),
        (3.5, 8.5, 'RESPONSABLE\n(Prov/Zone)', '#E8F5E9'),
        (5.5, 8.5, 'AGENT_ZONE\n(Zone)', '#BBDEFB'),
        (7.5, 8.5, 'AGENT_COLLINE\n(Colline)', '#D1C4E9'),
        (9.5, 8.5, 'AGENT_LOGISTIQUE\n(Usine)', '#FFF9C4'),
        (11.5, 8.5, 'PUBLIC\n(Suivi public)', '#FFE0B2'),
    ]

    for x, y, label, color in actors:
        circle = plt.Circle((x, y), 0.55, facecolor=color, edgecolor='#333', linewidth=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y-0.1, label, fontsize=7, fontweight='bold', ha='center', va='center', color='#333')
        ax.annotate('', xy=(x, y-0.55), xytext=(x, y-0.55-0.4),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
        ax.plot([x, x], [y-0.55, y-0.55-0.7], color='#333', lw=1.5)

    # System boundary box
    rect = FancyBboxPatch((2.2, 2.2), 10.5, 5.5, boxstyle="round,pad=0.05",
                          facecolor='#F5F5F5', edgecolor='#333', linewidth=2)
    ax.add_patch(rect)
    ax.text(7.5, 7.5, 'Système FOMI-Stock', fontsize=11, fontweight='bold', color='#333', ha='center')
    ax.text(7.5, 7.2, 'Cas d\'utilisation principaux (UC-1 a UC-26)', fontsize=7, color='#666', ha='center')

    # Use cases inside boundary
    use_cases = [
        (3.5, 6.5, 'UC-01\nAuthentification', '#C8E6C9'),
        (6.0, 6.5, 'UC-06~UC-07\nTickets (Création/Validation)', '#BBDEFB'),
        (8.5, 6.5, 'UC-10\nDistribution FIFO', '#D1C4E9'),
        (3.5, 5.0, 'UC-07~UC-08\nRéception / Transfert', '#FFE0B2'),
        (6.0, 5.0, 'UC-12\nAnnulation Mouvements', '#FCE4EC'),
        (8.5, 5.0, 'UC-13~UC-21\nConsultation / Recherche', '#C8E6C9'),
        (3.5, 3.5, 'UC-14~UC-20\nAlertes / Seuils / Stats', '#FFF9C4'),
        (6.0, 3.5, 'UC-15\nAudit Trail', '#BBDEFB'),
        (8.5, 3.5, 'UC-18~UC-19\nPublic / Utilisateurs', '#D1C4E9'),
    ]

    for x, y, label, color in use_cases:
        oval = Ellipse((x, y), 2.0, 0.7, facecolor=color, edgecolor='#333', linewidth=1.5, zorder=4)
        ax.add_patch(oval)
        ax.text(x, y, label, fontsize=7, ha='center', va='center', fontweight='bold', color='#333')

    # Actor associations
    associations = [
        (1.5, 8.0, 3.5, 7.2, 'auth'),
        (3.5, 7.8, 5.3, 7.2, 'créer'),
        (5.5, 7.8, 7.2, 7.2, 'valider'),
        (7.5, 7.8, 9.2, 7.2, 'distribuer'),
        (11.5, 7.8, 8.5, 5.7, 'consulter'),
        (9.5, 7.8, 4.2, 5.7, 'recevoir'),
    ]
    for x1, y1, x2, y2, lbl in associations:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color='#333', lw=1))

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/use_case_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ use_case_diagram.png")

# ============================================================
# DIAGRAMME D'ACTIVITÉS (UML Activity) - Distribution FIFO
# ============================================================
def draw_activity_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Diagramme d\'activites - Distribution FIFO d\'un ticket', fontsize=14, fontweight='bold', pad=15)

    # Start/End
    oval_start = plt.Circle((2, 11), 0.35, facecolor='#81C784', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(oval_start)
    ax.text(2, 11, 'Début', fontsize=8, ha='center', va='center', fontweight='bold')
    ax.annotate('', xy=(2, 10.65), xytext=(2, 10.65), arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    # Activity nodes (rounded rectangles)
    def act(x, y, w, h, text, color='#E3F2FD'):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", facecolor=color, edgecolor='#1565C0', linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, fontsize=9, fontweight='bold', ha='center', va='center')

    act(0.5, 9.5, 3, 0.9, 'Vérifier périmètre agent', '#FFF9C4')
    # Decision diamond
    diamond = plt.Polygon([(5.5, 8.5), (6.5, 9.2), (5.5, 9.9), (4.5, 9.2)], facecolor='#FFE0B2', edgecolor='#EF6C00', linewidth=2)
    ax.add_patch(diamond)
    ax.text(5.5, 9.2, 'Périmètre OK ?', fontsize=7, ha='center', va='center')

    # Yes path
    act(8, 9.5, 3, 0.9, 'Vérifier statut ticket (ACTIF/PAYE)', '#C8E6C9')
    diamond2 = plt.Polygon([(11.5, 8.5), (12.5, 9.2), (11.5, 9.9), (10.5, 9.2)], facecolor='#FFE0B2', edgecolor='#EF6C00', linewidth=2)
    ax.add_patch(diamond2)
    ax.text(11.5, 9.2, 'Quantité restante > 0 ?', fontsize=7, ha='center', va='center')

    # Loop: distribute lots FIFO
    act(7, 6.5, 4.5, 1.2, 'Pour chaque lot : min(lot.qté, reste) décrémenter StockLot', '#BBDEFB')
    # Arrow from loop back
    ax.annotate('', xy=(9.75, 6.5+1.2), xytext=(11.5, 8.5), arrowprops=dict(arrowstyle='->', color='#333', lw=1, connectionstyle="arc3,rad=0.3"))
    # Arrow from decision to loop
    ax.annotate('', xy=(7, 7.15), xytext=(11.5, 8.5-0.4), arrowprops=dict(arrowstyle='->', color='#333', lw=1))

    # No path from decision
    act(12.5, 6.5, 4, 1.0, 'Distribuer quantité finale', '#C8E6C9')

    # Final
    act(9, 3.5, 5, 1.0, 'Créer Mouvements + Distribution + Audit + Vérifier Alertes', '#F3E5F5')

    # End oval
    oval_end = plt.Circle((7, 1.5), 0.35, facecolor='#81C784', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(oval_end)
    ax.text(7, 1.5, 'FIN', fontsize=8, fontweight='bold', ha='center', va='center')

    ax.annotate('', xy=(6.5, 2.5), xytext=(7, 2.5), arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    # Connector: start -> first act
    ax.annotate('', xy=(2, 9.85), xytext=(2, 10.0-0.35), arrowprops=dict(arrowstyle='-', color='#333', lw=1.5))
    ax.annotate('', xy=(1.25, 9.5), xytext=(2.0, 9.5), arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    # Labels on arrows
    ax.annotate('', xy=(7.0, 9.5+0.9), xytext=(5.5, 9.5+0.45), arrowprops=dict(arrowstyle='->', color='#333', lw=1))
    ax.annotate('', xy=(12.0, 7.7), xytext=(11.5, 7.7+0.8), arrowprops=dict(arrowstyle='->', color='#333', lw=1))
    ax.annotate('', xy=(7.0, 6.5+1.2), xytext=(9.75, 6.5+1.2), arrowprops=dict(arrowstyle='->', color='#333', lw=1))

    # Legend / note
    ax.text(7, 0.3, 'Boucle : continue tant que reste > 0 │ Sortie : fin si reste = 0', fontsize=7, ha='center', color='#555', style='italic', bbox=dict(boxstyle='round,pad=0.2', facecolor='#F5F5F5', edgecolor='#CCC'))

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/activity_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ activity_diagram.png")

# ============================================================
# DICTIONNAIRE DE DONNÉES (Visual summary — image + table reference)
# ============================================================
def draw_data_dictionary():
    """Dictionnaire visuel : colonnes fixes + retour a la ligne explicite.

    Les libelles longs etaient auparavant dessines sur une seule ligne et
    debordaient des cadres (voire de la figure) ; ils sont maintenant replies
    avec textwrap et chaque bloc a une largeur reservee.
    """
    fig, ax = plt.subplots(1, 1, figsize=(16, 13))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 13)
    ax.axis('off')
    ax.set_title('Dictionnaire de données — Tables principales du système FOMI-Stock', fontsize=14, fontweight='bold', pad=15)
    ax.text(8, 12.55, '16 tables | 30+ DTOs | 6 énumérations PostgreSQL | 12 migrations Flyway',
            fontsize=10, ha='center', color='#555', style='italic')

    def ligne(y, h, table, desc, pk, details, rel, bg, ec):
        rect = FancyBboxPatch((0.5, y), 15, h, boxstyle="round,pad=0.05",
                              facecolor=bg, edgecolor=ec, linewidth=1)
        ax.add_patch(rect)
        ax.text(0.75, y + h/2, table, fontsize=8.5, fontweight='bold', color=ec, va='center')
        ax.text(2.55, y + h/2, desc, fontsize=7.2, color='#333', va='center')
        ax.text(6.2, y + h/2, textwrap.fill(f"PK: {pk}", 20), fontsize=5.9,
                color='#555', va='center', linespacing=1.15)
        if details:
            ax.text(8.3, y + h/2, textwrap.fill(details, 44), fontsize=5.6,
                    color='#555', va='center', linespacing=1.15)
        ax.text(13.6, y + h/2, textwrap.fill(rel, 17), fontsize=5.6,
                color=ec, style='italic', va='center', linespacing=1.15)

    def section(y, titre, bg, ec):
        ax.text(0.5, y, titre, fontsize=10, fontweight='bold', color=ec,
                bbox=dict(boxstyle='round,pad=0.15', facecolor=bg, edgecolor=ec))

    # Géographie
    section(11.85, 'GÉOGRAPHIE', '#E8EAF6', '#283593')
    geo = [
        ('province', 'Province', 'code UNIQUE', '', '1:N zone'),
        ('zone', 'Zone', 'code UNIQUE', 'nom, province_id FK', '1:N colline'),
        ('colline', 'Colline', 'code UNIQUE', 'nom, zone_id FK', '0..1:N agriculteur'),
    ]
    y = 11.25
    for table, desc, pk, details, rel in geo:
        ligne(y, 0.48, table, desc, pk, details, rel, '#E8EAF6', '#283593')
        y -= 0.55

    # Référentiel
    section(9.35, 'RÉFÉRENTIEL MÉTIER', '#E8F5E9', '#2E7D32')
    ref = [
        ('engrais_type', 'EngraisType', 'code UNIQUE', 'nom, poids_sac_kg (50.00), prix_subventionne, actif', '1:N lot, 1:N stock'),
        ('agriculteur', 'Agriculteur', 'numero_identite UNIQUE, telephone UNIQUE, email UNIQUE', 'nom, prenom, superficie_ha, colline_id FK, est_cooperative, email (V12)', '1:N ticket'),
        ('depot', 'Depot', 'code UNIQUE', 'nom, niveau (enum PG), colline/zone/province_id, seuil_alerte_min, capacite_max', '1:N ticket, 1:N stock'),
        ('lot', 'Lot', 'numero_lot UNIQUE', 'quantite_initiale, date_fabrication, date_peremption, engrais_type_id FK, date_reception_fomi', '1:N mouvement, 1:N stock_lot'),
    ]
    y = 8.75
    for table, desc, pk, details, rel in ref:
        ligne(y, 0.62, table, desc, pk, details, rel, '#E8F5E9', '#2E7D32')
        y -= 0.65

    # Opérations
    section(6.15, 'OPÉRATIONS & MOUVEMENTS', '#FFF3E0', '#E65100')
    op = [
        ('ticket', 'Ticket', 'numero_ticket UNIQUE', 'agriculteur_id, depot_retrait_id, statut (enum PG), saison, quantite_commandee/servie, montant_paye', '1:N distribution'),
        ('distribution', 'Distribution', 'ticket_id FK UNIQUE', 'quantite, depot_id FK, agent_id FK, date_distribution (1:1 mouvement)', '1:1 mouvement'),
        ('mouvement', 'Mouvement', 'idempotency_key UNIQUE (64 car)', 'type (enum PG), lot_id FK, quantite, agent_id FK, depot_source/dest_id FK, annule, reference_annulation_id FK', '1:N audit_log'),
        ('stock', 'Stock (agrégat)', '(depot_id, engrais_type_id) UNIQUE', 'quantite_disponible, updated_at (@PreUpdate)', '1:N mouvement'),
        ('stock_lot', 'StockLot', '(depot_id, lot_id) UNIQUE', 'quantite, updated_at', '1:1 lot, 1:N mouvement'),
    ]
    y = 5.55
    for table, desc, pk, details, rel in op:
        ligne(y, 0.56, table, desc, pk, details, rel, '#FFF3E0', '#E65100')
        y -= 0.62

    # Sécurité et audit
    section(2.45, 'SÉCURITÉ, ALERTES & AUDIT', '#FFEBEE', '#C62828')
    sec = [
        ('utilisateur', 'Utilisateur', 'username UNIQUE', 'password_hash (BCrypt), nom_complet, role (enum PG), depot/zone/province_id, actif, soft_delete', '1:N audit_log'),
        ('alerte', 'Alerte', 'depot_id + type + engrais_type_id', 'message, niveau (enum PG), traitee', 'N:1 audit_log'),
        ('seuil_alerte', 'SeuilAlerte', '(depot_id, engrais_type_id) UNIQUE', 'seuil_min, criticite', '1:N alerte (indirect)'),
        ('audit_log', 'AuditLog', 'utilisateur_id FK (nullable)', 'action, entity_type, entity_id, ip_address, details_json (JSONB)', 'N:1 utilisateur'),
    ]
    y = 1.85
    for table, desc, pk, details, rel in sec:
        ligne(y, 0.48, table, desc, pk, details, rel, '#FFEBEE', '#C62828')
        y -= 0.55

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/data_dictionary_summary.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ data_dictionary_summary.png")

# ============================================================
# Générer tous les diagrammes
# ============================================================
if __name__ == "__main__":
    print("Génération des diagrammes...")
    draw_architecture()
    draw_er_diagram()
    draw_sequence_distribution()
    draw_sequence_ticket()
    draw_rbac()
    draw_distribution_circuit()
    draw_layered_architecture()
    draw_ticket_state_machine()
    draw_fifo_flowchart()
    draw_fomi_timeline()
    draw_class_diagram()
    draw_deployment_diagram()
    draw_use_case_diagram()
    draw_activity_diagram()
    draw_data_dictionary()
    print(f"\n✓ Tous les diagrammes générés dans {OUT_DIR}/")

