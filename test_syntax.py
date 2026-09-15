#!/usr/bin/env python3
"""
Script de génération du mémoire FOMI - Gestion des stocks d'engrais
Génère les diagrammes PNG puis le document DOCX (~100 pages)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

OUT_DIR = "/home/antbeat/projects/memoire_assets"
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
        '#FFECB3', '#FF8F00', 9, True)

    # Service Layer
    box(0.5, 3.2, 13, 1.5, '', '#F3E5F5', '#7B1FA2')
    ax.text(7, 4.5, 'Couche Service (Logique métier)', fontsize=13, fontweight='bold',
            ha='center', color='#4A148C')
    svc_items = ['DistributionService\n(FIFO)', 'MouvementService\n(Annulation)',
                 'TicketService\n(Quotas/R6)', 'AlerteService\n(Cron 06h00)',
                 'StockService\n(Gestion FIFO)', 'StatsService\n(Requêtes JPQL)',
                 'AuditLogService\n(Traçabilité)']
    for i, item in enumerate(svc_items):
        x = 0.8 + i * 1.85
        box(x, 3.35, 1.6, 1.0, item, '#E1BEE7', '#9C27B0', 7)

    # Repository Layer
    box(1, 2.0, 12, 0.9, 'Couche Repository - Spring Data JPA (15 repositories)\nPessimistic locking (SELECT FOR UPDATE) + Requêtes JPQL dynamiques',
        '#E0F7FA', '#00838F', 10, True)

    # Data Layer
    box(1, 0.3, 5.5, 1.4, 'PostgreSQL 16\n16 tables | Enums nommés\nFlyway (11 migrations)\nJSONB pour audit logs',
        '#FCE4EC', '#C62828', 10, True)
    box(7.5, 0.3, 5.5, 1.4, 'Testcontainers\n(Tests d\'intégration)\nJUnit 5 + Mockito\n203 tests automatisés',
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
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 16)
    ax.axis('off')
    ax.set_title('Diagramme Entité-Relation du système FOMI-Stock', fontsize=16, fontweight='bold', pad=20)

    def entity_box(x, y, name, fields, color='#E3F2FD'):
        w = 3.2
        h = 0.35 * len(fields) + 0.6
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='#1565C0', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.2, name, ha='center', va='center',
                fontsize=9, fontweight='bold', color='#0D47A1')
        ax.plot([x, x+w], [y + h - 0.4, y + h - 0.4], color='#1565C0', linewidth=1)
        for i, f in enumerate(fields):
            ax.text(x + 0.1, y + h - 0.55 - i*0.35, f, fontsize=7, va='center', color='#333')
        return (x + w/2, y, x + w/2, y + h)

    def relation(x1, y1, x2, y2, label='', cardinality='', color='#666'):
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=1, linestyle='-', zorder=0)
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my+0.15, label, fontsize=6, ha='center', color=color, style='italic')
        if cardinality:
            ax.text(x2, y2+0.1, cardinality, fontsize=7, ha='center', color=color, fontweight='bold')

    # Géographie
    entity_box(0.3, 13, 'Province', ['id PK', 'code UNIQUE', 'nom'], '#E8EAF6')
    entity_box(5, 13, 'Zone', ['id PK', 'code UNIQUE', 'nom', 'province_id FK'], '#E8EAF6')
    entity_box(10, 13, 'Colline', ['id PK', 'code UNIQUE', 'nom', 'zone_id FK'], '#E8EAF6')

    # Dépôt
    entity_box(15, 13, 'Depot', ['id PK', 'code UNIQUE', 'nom', 'niveau (enum)', 'province_id FK', 'zone_id FK', 'colline_id FK', 'seuil_alerte_min', 'capacite_max', 'supprime', 'deleted_at'], '#FFF3E0')

    # Entités métier
    entity_box(0.3, 9.5, 'Agriculteur', ['id PK', 'numero_identite', 'nom', 'prenom', 'telephone', 'colline_id FK', 'est_cooperative', 'superficie_ha', 'supprime'], '#E8F5E9')
    entity_box(5, 9.5, 'EngraisType', ['id PK', 'code UNIQUE', 'nom', 'poids_sac_kg', 'prix_subventionne', 'actif'], '#FCE4EC')
    entity_box(10, 9.5, 'Lot', ['id PK', 'numero_lot UNIQUE', 'engrais_type_id FK', 'quantite_initiale', 'date_fabrication', 'date_peremption', 'date_reception_fomi'], '#FCE4EC')
    entity_box(15, 9.5, 'Ticket', ['id PK', 'numero_ticket UNIQUE', 'agriculteur_id FK', 'engrais_type_id FK', 'quantite_commandee', 'quantite_servie', 'montant_paye', 'date_paiement', 'depot_retrait_id FK', 'statut (enum)', 'saison', 'superficie_ha', 'supprime'], '#FFF3E0')

    # Stock
    entity_box(0.3, 6.5, 'Stock', ['id PK', 'depot_id FK', 'engrais_type_id FK', 'quantite_disponible', 'updated_at'], '#F1F8E9')
    entity_box(5, 6.5, 'StockLot', ['id PK', 'depot_id FK', 'lot_id FK', 'quantite', 'updated_at'], '#F1F8E9')

    # Mouvement
    entity_box(10, 5.5, 'Mouvement', ['id PK', 'type (enum)', 'lot_id FK', 'engrais_type_id FK', 'depot_source_id FK', 'depot_dest_id FK', 'quantite', 'agent_id FK', 'ticket_id FK', 'commentaire', 'date_mouvement', 'idempotency_key', 'annule', 'motif_annulation', 'annule_par_id FK', 'reference_annulation_id FK'], '#FFEBEE')

    # Distribution
    entity_box(0.3, 3.5, 'Distribution', ['id PK', 'ticket_id FK', 'lot_id FK', 'depot_id FK', 'quantite', 'agent_id FK', 'date_distribution', 'reference_mouvement_id FK UNIQUE'], '#FFEBEE')

    # Alertes & Seuils
    entity_box(15, 5.5, 'Alerte', ['id PK', 'depot_id FK', 'engrais_type_id FK', 'type (enum)', 'message', 'niveau (enum)', 'traitee', 'created_at'], '#FFF9C4')
    entity_box(15, 3.5, 'SeuilAlerte', ['id PK', 'depot_id FK', 'engrais_type_id FK', 'seuil_min', 'criticite'], '#FFF9C4')

    # Utilisateur & Audit
    entity_box(0.3, 0.5, 'Utilisateur', ['id PK', 'username UNIQUE', 'password_hash', 'nom_complet', 'role (enum)', 'depot_id FK', 'zone_id FK', 'province_id FK', 'actif', 'supprime'], '#F3E5F5')
    entity_box(10, 0.5, 'AuditLog', ['id PK', 'utilisateur_id FK', 'action', 'entity_type', 'entity_id', 'ip_address', 'details_json (JSONB)', 'created_at'], '#EFEBE9')

    # Relations
    relation(1.9, 13, 5, 13.5, '', '1:N')
    relation(6.6, 13, 10, 13.5, '', '1:N')
    relation(11.6, 13.5, 15, 13.5, '', '0..1:N')
    relation(1.9, 9.5, 10, 13, '', 'N:1')
    relation(6.6, 9.5, 10, 10, '', '1:N')
    relation(11.6, 10, 15, 10, '', '1:N')
    relation(1.9, 9.5, 10, 13.5, '', 'N:1')

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
        (2, 3, 'sortirFifo(depot, type, qty)', 9.5),
        (3, 4, 'SELECT lot ORDER BY date ASC\n(FIFO)', 9.0),
        (4, 3, 'List<LotSortie>', 8.5),
        (3, 2, 'Quantités décrémentées', 8.0),
        (2, 4, 'MouvementRepository.save(DISTRIBUTION)', 7.5),
        (2, 4, 'DistributionRepository.save()', 7.0),
        (2, 4, 'TicketRepository.save(statut=SERVI)', 6.5),
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
        (1, 0, 'TicketResponse {statut: EN_ATTENTE...}', 5.5),
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
        (0.5, 2.6, 13, 1.5, 'SERVICES', 'DistributionService (FIFO) │ TicketService (Quotas R6/R22) │ AlerteService (Cron)\nStockService │ MouvementService │ StatsService │ AuditLogService', '#F3E5F5', '#7B1FA2'),
        (0.5, 1.0, 6, 1.3, 'REPOSITORIES', 'Spring Data JPA │ 15 Repositories\nRequêtes JPQL │ Pessimistic Locking', '#FCE4EC', '#C62828'),
        (7.5, 1.0, 6, 1.3, 'MODÈLE DOMAINE', '16 Entités JPA │ 6 Enums PostgreSQL\n30+ DTOs (Records Java)', '#EFEBE9', '#5D4037'),
        (0.5, 0.0, 13, 0.7, 'INFRASTRUCTURE', 'PostgreSQL 16 │ Flyway (11 migrations) │ Docker │ GitHub Actions │ Railway CI/CD', '#263238', '#FFF'),
    ]

    for x, y, w, h, title, desc, bg, ec in layers:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=bg, edgecolor=ec, linewidth=2)
        ax.add_patch(rect)
        tc = ec if ec != '#FFF' else '#333'
        ax.text(x + 0.3, y + h - 0.3, title, fontsize=11, fontweight='bold', color=tc)
        ax.text(x + 0.3, y + h/2 - 0.2, desc, fontsize=8, color='#555')

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
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Diagramme d\'état - Cycle de vie du ticket', fontsize=14, fontweight='bold', pad=15)

    def state(x, y, text, color='#E3F2FD'):
        rect = FancyBboxPatch((x-0.9, y-0.3), 1.8, 0.6, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#1565C0', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')

    def trans(x1, y1, x2, y2, label):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.15, label, fontsize=7, ha='center',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFF9C4', edgecolor='#CCC'))

    # States
    state(2, 6.5, 'PAYE\n(Paiement reçu)', '#C8E6C9')
    state(5.5, 6.5, 'EN_ATTENTE\nDE_VALIDATION', '#BBDEFB')
    state(9.5, 6.5, 'ACTIF\n(Validé)', '#A5D6A7')
    state(13.5, 6.5, 'PARTIEL\n(Livré partiel)', '#FFCC80')
    state(13.5, 3.5, 'SERVI\n(Totalement livré)', '#81C784')
    state(5.5, 3.5, 'REJETÉ\n(Refusé)', '#EF9A9A')
    state(9, 1.5, 'ANNULE', '#E0E0E0')
    state(2, 3.5, 'EXPIRE\n(Annulé auto)', '#BDBDBD')

    # Transitions
    trans(2.9, 6.5, 4.6, 6.5, 'Soumettre')
    trans(6.4, 6.5, 8.6, 6.5, 'Activer\n(Superviseur)')
    trans(9.5, 6.2, 12.6, 6.2, 'Distribution\npartielle')
    trans(12.6, 5.5, 9.5, 3.5, 'quantite_servie\n== commandee')
    trans(6.4, 6.2, 6.4, 3.8, 'Rejeter\n(motif)')
    trans(13.5, 6.2, 13.5, 3.8, 'Dernière\ndistribution')

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
    process(4, 10.5, 6, 0.8, 'Début : Demande de distribution', '#C8E6C9')
    arrow(7, 10.5, 7, 10.0)

    diamond(4.5, 9.0, 5, 0.8, 'Ticket valide?\n(ACTIF ou PAYE)')
    arrow(7, 9.0, 7, 8.5, 'Oui')
    arrow(9.5, 9.4, 12, 9.4, 'Non → Erreur')
    ax.text(12, 9.6, '✗ Rejeté', fontsize=8, color='red')

    process(4, 7.5, 6, 0.8, 'Vérifier Périmètre Agent\n(Colline → Depot → Zone)')
    arrow(7, 7.5, 7, 7.0)

    diamond(4, 6.0, 6, 0.8, 'quantité restante > 0?')
    arrow(7, 6.0, 7, 5.5, 'Oui')
    arrow(10, 6.4, 12, 6.4, 'Non → SERVI')
    ax.text(12, 6.6, '✓ Ticket complet', fontsize=8, color='green')

    process(4, 4.5, 6, 0.8, 'Trier les lots par date\n(FIFO : premier entré = premier sorti)')
    arrow(7, 4.5, 7, 4.0)

    process(3, 2.8, 8, 0.8, 'Pour chaque lot :\n  min(quantité_lot, quantité_restante)\n  Décrémenter StockLot et Stock')
    arrow(7, 2.8, 7, 2.3)

    process(4, 1.2, 6, 0.8, 'Créer Mouvement(DISTRIBUTION)\n+ Distribution + MAJ Ticket\n+ AuditLog + Vérif Alertes', '#F3E5F5')
    arrow(7, 1.2, 7, 0.7)

    process(4.5, 0.0, 5, 0.5, 'Fin', '#EF9A9A')

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
# Générer tous les diagrammes
# ============================================================
if __name__ == '__main__':
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

# ============================================================
# DIAGRAMME DE CLASSES UML (Classes principales du système)
# ============================================================
def draw_class_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Diagramme de classes — Entités et relations', fontsize=14, fontweight='bold', pad=15)

    def cls_box(x, y, w, h, title, attrs, ops):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                              facecolor='#FCE4EC', edgecolor='#C62828', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.2, title, ha='center', fontsize=9, fontweight='bold', color='#C62828')
        # separator line
        ax.plot([x, x+w], [y + h - 0.4, y + h - 0.4], color='#C62828', lw=1)
        # attributes
        for i, a in enumerate(attrs):
            ax.text(x + 0.1, y + h - 0.55 - i*0.28, a, fontsize=6.5, va='center', color='#333')
        # methods separator
        y_start_ops = y + max(0.6, 0.28*len(attrs) + 0.1)
        ax.plot([x, x+w], [y_start_ops, y_start_ops], color='#C62828', lw=0.5)
        for i, o in enumerate(ops):
            ax.text(x + 0.1, y_start_ops - 0.35 - i*0.25, o, fontsize=6, va='center', color='#1565C0', style='italic')
        return (x + w/2, y + h/2)

    # Key entities with representative attributes/methods
    cls_box(0.3, 9.5, 2.5, 2.2, 'Ticket', ['id: Long', 'numeroTicket: String', 'statut: StatutTicket', 'quantiteServie: Integer', 'agriculteur: Agriculteur'], ['creer()', 'valider()', 'rejeter()', 'mettreAJourStatut()'])
    cls_box(3.5, 9.5, 2.5, 2.0, 'Agriculteur', ['id: Long', 'numeroIdentite: String', 'telephone: String', 'superficieHa: BigDecimal', 'colline: Colline'], ['creer()', 'rechercherParTelephone()'])
    cls_box(6.8, 9.5, 2.5, 2.2, 'Mouvement', ['id: Long', 'type: TypeMouvement', 'quantite: Integer', 'agent: Utilisateur', 'dateMouvement: LocalDateTime', 'idempotencyKey: String'], ['annuler()', 'restaurerStock()'])
    cls_box(10, 9.5, 2.5, 2.0, 'Distribution', ['id: Long', 'ticket: Ticket', 'lot: Lot', 'quantite: Integer', 'agent: Utilisateur', 'dateDistribution: LocalDateTime'], ['distribuerFifo()', 'annuler()'])
    cls_box(13.5, 9.5, 2.5, 2.4, 'Utilisateur', ['id: Long', 'username: String', 'passwordHash: String', 'role: RoleUtilisateur', 'depot: Depot', 'zone: Zone', 'province: Province'], ['getAuthorities()', 'isAccountNonExpired()'])

    # Second row
    cls_box(0.3, 5.8, 2.5, 2.0, 'Lot', ['id: Long', 'numeroLot: String', 'dateFabrication: LocalDate', 'datePeremption: LocalDate', 'dateReceptionFomi: LocalDateTime', 'quantiteInitiale: Integer'], ['estPerime()', 'verifierCapacite()'])
    cls_box(3.5, 5.8, 2.5, 2.0, 'Depot', ['id: Long', 'code: String', 'nom: String', 'niveau: NiveauDepot', 'province/zone/colline: FK'], ['verifierCapacite()', 'verifierPerimetre()'])
    cls_box(6.8, 5.8, 2.5, 2.4, 'Stock', ['id: Long', 'depot: Depot', 'engraisType: EngraisType', 'quantiteDisponible: Integer', 'updatedAt: LocalDateTime'], ['mettreAJourQuantite()', 'verifierSeuil()'])
    cls_box(10, 5.8, 2.5, 2.0, 'StockLot', ['id: Long', 'depot: Depot', 'lot: Lot', 'quantite: Integer', 'updatedAt: LocalDateTime'], ['verifierLotPerime()', 'decrementer()'])

    # Third row
    cls_box(3, 3.5, 2.5, 1.5, 'Alerte', ['id: Long', 'depot: Depot', 'type: TypeAlerte', 'niveau: NiveauAlerte', 'traitee: Boolean', 'message: String'], ['creerSiAbsente()', 'traiter()'])
    cls_box(6.8, 3.5, 2.5, 2.0, 'AuditLog', ['id: Long', 'utilisateur: Utilisateur', 'action: String', 'entityType: String', 'detailsJson: JSONB', 'ipAddress: String'], ['log()'])
    cls_box(10, 3.5, 2.5, 1.5, 'SeuilAlerte', ['id: Long', 'depot: Depot', 'engraisType: EngraisType', 'seuilMin: Integer', 'criticite: String'], ['verifierSeuil()'])

    # Relationships (simplified UML associations)
    def rel_line(x1, y1, x2, y2, label='', color='#1565C0', style='-'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my+0.15, label, fontsize=7, ha='center', va='bottom', color=color,
                    bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8))

    rel_line(2.8, 8.4, 4.7, 9.0, 'N:1')
    rel_line(6.0, 8.8, 8.0, 9.0, 'N:1 (Ticket)', '#7B1FA2')
    rel_line(9.5, 5.5, 9.5, 7.5, '1:1 (Distribution)', '#7B1FA2')
    rel_line(5.5, 7.7, 5.5, 6.7, '1:N', '#333')
    rel_line(8.0, 4.5, 8.0, 5.3, '1:N', '#333')

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
    node(3.5, 1.5, 5, 1.5, 'PostgreSQL 16', '16 tables + enums / JSONB audit / Index GIN / Migrations Flyway V1→V11', '#FCE4EC', '#C62828')
    node(9.5, 1.5, 3, 1.5, 'Testcontainers', 'PostgreSQL 16-alpine / JUnit 5 / 203 tests / Docker Java 1.44', '#E8EAF6', '#283593')

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
    conn(4, 4.5, 5.5, 3.2, 'JDBC / JPA')
    # DB -> Testcontainers
    conn(9.5, 1.5, 11, 1.5, 'Docker')
    # CI note
    ax.text(8, 0.2, 'Déploiement CI/CD : GitHub Actions (build + test 203) → Docker build → Railway (auto-deploy sur push main)', fontsize=7, ha='center', color='#555', style='italic', bbox=dict(boxstyle='round,pad=0.2', facecolor='#F5F5F5', edgecolor='#CCC'))

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/deployment_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ deployment_diagram.png")

# (use_case_diagram and activity_diagram temporarily removed for syntax isolation)
