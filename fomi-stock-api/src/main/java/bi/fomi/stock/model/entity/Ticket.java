package bi.fomi.stock.model.entity;

import bi.fomi.stock.model.enums.StatutTicket;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "ticket")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Ticket {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "numero_ticket", nullable = false, unique = true, length = 50)
    private String numeroTicket;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "agriculteur_id", nullable = false)
    private Agriculteur agriculteur;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "engrais_type_id", nullable = false)
    private EngraisType engraisType;

    @Column(name = "quantite_commandee", nullable = false)
    private Integer quantiteCommandee;

    @Column(name = "quantite_servie", nullable = false)
    @Builder.Default
    private Integer quantiteServie = 0;

    @Column(name = "montant_paye", nullable = false)
    private BigDecimal montantPaye;

    @Column(name = "date_paiement", nullable = false)
    private LocalDate datePaiement;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "depot_retrait_id", nullable = false)
    private Depot depotRetrait;

    @Enumerated(EnumType.STRING)
    @JdbcTypeCode(SqlTypes.NAMED_ENUM)
    @Column(nullable = false, columnDefinition = "statut_ticket")
    @Builder.Default
    private StatutTicket statut = StatutTicket.PAYE;

    @Column(nullable = false, length = 10)
    @Builder.Default
    private String saison = "2027A";

    @Column(name = "superficie_ha")
    private java.math.BigDecimal superficieHa;

    @Column(name = "motif_rejet", length = 500)
    private String motifRejet;

    @Column(name = "est_demo", nullable = false)
    @Builder.Default
    private Boolean estDemo = false;

    @Column(name = "date_creation", nullable = false)
    private LocalDateTime dateCreation;

    @Column(nullable = false)
    @Builder.Default
    private Boolean supprime = false;

    @Column(name = "deleted_at")
    private LocalDateTime deletedAt;

    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    void prePersist() {
        LocalDateTime now = LocalDateTime.now();
        if (dateCreation == null) {
            dateCreation = now;
        }
        updatedAt = now;
    }

    @PreUpdate
    void preUpdate() {
        updatedAt = LocalDateTime.now();
    }

    public int getQuantiteRestante() {
        return (quantiteCommandee != null ? quantiteCommandee : 0) - (quantiteServie != null ? quantiteServie : 0);
    }

    public void mettreAJourStatut() {
        if (statut == StatutTicket.ANNULE || statut == StatutTicket.REJETE
                || statut == StatutTicket.EXPIRE) {
            return;
        }
        if (quantiteServie == 0) {
            return;
        }
        if (quantiteServie >= quantiteCommandee) {
            statut = StatutTicket.SERVI;
        } else {
            statut = StatutTicket.PARTIEL;
        }
    }
}
