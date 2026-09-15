package bi.fomi.stock.model.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "agriculteur")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Agriculteur {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "numero_identite", nullable = false, unique = true, length = 30)
    private String numeroIdentite;

    @Column(nullable = false, length = 100)
    private String nom;

    @Column(nullable = false, length = 100)
    private String prenom;

    @Column(length = 20)
    private String telephone;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "colline_id", nullable = false)
    private Colline colline;

    @Column(name = "est_cooperative", nullable = false)
    @Builder.Default
    private Boolean estCooperative = false;

    @Column(name = "superficie_ha")
    private java.math.BigDecimal superficieHa;

    @Column(nullable = false)
    @Builder.Default
    private Boolean supprime = false;

    @Column(name = "deleted_at")
    private LocalDateTime deletedAt;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @PrePersist
    void prePersist() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }
}
