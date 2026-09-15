package bi.fomi.stock.model.entity;

import bi.fomi.stock.model.enums.TypeMouvement;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;

@Entity
@Table(name = "mouvement")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Mouvement {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @JdbcTypeCode(SqlTypes.NAMED_ENUM)
    @Column(nullable = false, columnDefinition = "type_mouvement")
    private TypeMouvement type;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "lot_id", nullable = false)
    private Lot lot;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "engrais_type_id", nullable = false)
    private EngraisType engraisType;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "depot_source_id")
    private Depot depotSource;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "depot_dest_id")
    private Depot depotDest;

    @Column(nullable = false)
    private Integer quantite;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "agent_id", nullable = false)
    private Utilisateur agent;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ticket_id")
    private Ticket ticket;

    @Column(length = 500)
    private String commentaire;

    @Column(name = "date_mouvement", nullable = false)
    private LocalDateTime dateMouvement;

    @Column(name = "idempotency_key", unique = true, length = 64)
    private String idempotencyKey;

    @Column(nullable = false)
    @Builder.Default
    private Boolean annule = false;

    @Column(name = "motif_annulation", length = 500)
    private String motifAnnulation;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "annule_par_id")
    private Utilisateur annulePar;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "reference_annulation_id")
    private Mouvement referenceAnnulation;

    @PrePersist
    void prePersist() {
        if (dateMouvement == null) {
            dateMouvement = LocalDateTime.now();
        }
    }
}
