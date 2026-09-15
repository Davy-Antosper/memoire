package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.AuditLog;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {
    List<AuditLog> findByUtilisateurIdOrderByCreatedAtDesc(Long utilisateurId);

    List<AuditLog> findByEntityTypeAndEntityIdOrderByCreatedAtDesc(String entityType, Long entityId);

    @Query("""
            SELECT a FROM AuditLog a
            WHERE (:action IS NULL OR LOWER(a.action) LIKE LOWER(CONCAT('%', CAST(:action AS string), '%')))
              AND (:entityType IS NULL OR a.entityType = :entityType)
              AND (:entityId IS NULL OR a.entityId = :entityId)
              AND (:utilisateurId IS NULL OR a.utilisateur.id = :utilisateurId)
            ORDER BY a.createdAt DESC
            """)
    Page<AuditLog> search(@Param("action") String action,
                          @Param("entityType") String entityType,
                          @Param("entityId") Long entityId,
                          @Param("utilisateurId") Long utilisateurId,
                          Pageable pageable);
}
