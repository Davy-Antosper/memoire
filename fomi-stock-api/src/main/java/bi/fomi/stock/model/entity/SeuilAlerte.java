package bi.fomi.stock.model.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "seuil_alerte", uniqueConstraints = @UniqueConstraint(columnNames = {"depot_id", "engrais_type_id"}))
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SeuilAlerte {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "depot_id", nullable = false)
    private Depot depot;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "engrais_type_id", nullable = false)
    private EngraisType engraisType;

    @Column(name = "seuil_min", nullable = false)
    private Integer seuilMin;

    @Column(nullable = false, length = 20)
    @Builder.Default
    private String criticite = "WARNING";
}
