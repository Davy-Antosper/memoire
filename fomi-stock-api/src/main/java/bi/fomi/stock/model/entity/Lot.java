package bi.fomi.stock.model.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "lot")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Lot {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "numero_lot", nullable = false, unique = true, length = 50)
    private String numeroLot;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "engrais_type_id", nullable = false)
    private EngraisType engraisType;

    @Column(name = "quantite_initiale", nullable = false)
    private Integer quantiteInitiale;

    @Column(name = "date_fabrication")
    private LocalDate dateFabrication;

    @Column(name = "date_peremption")
    private LocalDate datePeremption;

    @Column(name = "date_reception_fomi", nullable = false)
    private LocalDateTime dateReceptionFomi;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @PrePersist
    void prePersist() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
        if (dateReceptionFomi == null) {
            dateReceptionFomi = LocalDateTime.now();
        }
    }
}
