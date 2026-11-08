package bi.fomi.stock.model.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

/**
 * Réclamation liée à un ticket : entité séparée du ticket, avec ses propres
 * statuts. Un ticket payé mais non servi peut ainsi rester « PAYE » tandis que
 * la réclamation suit son propre circuit (OUVERTE → EN_INSTRUCTION → RESOLUE
 * ou REJETEE).
 */
@Entity
@Table(name = "reclamation")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Reclamation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ticket_id", nullable = false)
    private Ticket ticket;

    @Column(nullable = false, length = 200)
    private String motif;

    @Column(length = 1000)
    private String description;

    @Column(name = "quantite_manquante")
    private Integer quantiteManquante;

    @Column(nullable = false, length = 20)
    @Builder.Default
    private String statut = "OUVERTE";

    @Column(length = 1000)
    private String resolution;

    @Column(name = "date_creation", nullable = false)
    @Builder.Default
    private LocalDateTime dateCreation = LocalDateTime.now();

    @Column(name = "date_resolution")
    private LocalDateTime dateResolution;

    @Column(name = "est_demo", nullable = false)
    @Builder.Default
    private Boolean estDemo = false;
}
