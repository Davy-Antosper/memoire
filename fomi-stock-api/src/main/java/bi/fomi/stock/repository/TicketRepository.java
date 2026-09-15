package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Ticket;
import bi.fomi.stock.model.enums.StatutTicket;
import jakarta.persistence.LockModeType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface TicketRepository extends JpaRepository<Ticket, Long> {
    Optional<Ticket> findByNumeroTicket(String numeroTicket);

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT t FROM Ticket t WHERE t.id = :id")
    Optional<Ticket> findByIdForUpdate(@Param("id") Long id);

    Page<Ticket> findByStatut(StatutTicket statut, Pageable pageable);

    List<Ticket> findByAgriculteurId(Long agriculteurId);

    Page<Ticket> findByDepotRetraitId(Long depotId, Pageable pageable);

    Page<Ticket> findByDepotRetraitIdAndStatut(Long depotId, StatutTicket statut, Pageable pageable);

    @Query("""
            SELECT t FROM Ticket t
            WHERE t.depotRetrait.id = :depotId
              AND t.statut IN :statuts
              AND t.quantiteServie < t.quantiteCommandee
            """)
    List<Ticket> findNonServisByDepot(@Param("depotId") Long depotId,
                                      @Param("statuts") List<StatutTicket> statuts);

    List<Ticket> findBySaisonAndStatutNotIn(String saison, List<StatutTicket> statuts);
}
