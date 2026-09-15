package bi.fomi.stock.model.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "distribution")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Distribution {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ticket_id", nullable = false)
    private Ticket ticket;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "lot_id", nullable = false)
    private Lot lot;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "depot_id", nullable = false)
    private Depot depot;

    @Column(nullable = false)
    private Integer quantite;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "agent_id", nullable = false)
    private Utilisateur agent;

    @Column(name = "date_distribution", nullable = false)
    private LocalDateTime dateDistribution;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "reference_mouvement_id", nullable = false, unique = true)
    private Mouvement referenceMouvement;

    @PrePersist
    void prePersist() {
        if (dateDistribution == null) {
            dateDistribution = LocalDateTime.now();
        }
    }
}
