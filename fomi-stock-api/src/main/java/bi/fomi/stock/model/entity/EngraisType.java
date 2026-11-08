package bi.fomi.stock.model.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Table(name = "engrais_type")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class EngraisType {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 20)
    private String code;

    @Column(nullable = false, length = 100)
    private String nom;

    @Column(name = "poids_sac_kg", nullable = false)
    @Builder.Default
    private BigDecimal poidsSacKg = new BigDecimal("50.00");

    @Column(name = "prix_subventionne", nullable = false)
    private BigDecimal prixSubventionne;

    /** Prix non encore publié par la FOMI : l'interface doit l'indiquer clairement. */
    @Column(name = "prix_a_confirmer", nullable = false)
    @Builder.Default
    private Boolean prixAConfirmer = false;

    @Column(nullable = false)
    @Builder.Default
    private Boolean actif = true;
}
