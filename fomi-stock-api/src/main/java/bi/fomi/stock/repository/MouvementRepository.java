package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Mouvement;
import bi.fomi.stock.model.enums.TypeMouvement;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface MouvementRepository extends JpaRepository<Mouvement, Long> {
    List<Mouvement> findByLotIdOrderByDateMouvementAsc(Long lotId);

    List<Mouvement> findByDepotSourceIdOrDepotDestIdOrderByDateMouvementAsc(Long sourceId, Long destId);

    List<Mouvement> findByTypeAndDateMouvementBetween(TypeMouvement type, LocalDateTime from, LocalDateTime to);

    Optional<Mouvement> findByIdempotencyKey(String idempotencyKey);

    @Query(value = """
            SELECT m.* FROM mouvement m
            WHERE (:type IS NULL OR m.type = CAST(:type AS type_mouvement))
              AND (:agentId IS NULL OR m.agent_id = :agentId)
              AND (:depotId IS NULL OR m.depot_source_id = :depotId OR m.depot_dest_id = :depotId)
              AND (:from IS NULL OR m.date_mouvement >= :from)
              AND (:to IS NULL OR m.date_mouvement <= :to)
            """,
            countQuery = """
            SELECT COUNT(*) FROM mouvement m
            WHERE (:type IS NULL OR m.type = CAST(:type AS type_mouvement))
              AND (:agentId IS NULL OR m.agent_id = :agentId)
              AND (:depotId IS NULL OR m.depot_source_id = :depotId OR m.depot_dest_id = :depotId)
              AND (:from IS NULL OR m.date_mouvement >= :from)
              AND (:to IS NULL OR m.date_mouvement <= :to)
            """,
            nativeQuery = true)
    Page<Mouvement> findAllFiltered(@Param("type") String type,
                                    @Param("agentId") Long agentId,
                                    @Param("depotId") Long depotId,
                                    @Param("from") LocalDateTime from,
                                    @Param("to") LocalDateTime to,
                                    Pageable pageable);
}
