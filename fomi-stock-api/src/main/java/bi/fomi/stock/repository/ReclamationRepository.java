package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Reclamation;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ReclamationRepository extends JpaRepository<Reclamation, Long> {

    List<Reclamation> findAllByOrderByDateCreationDesc();

    List<Reclamation> findByStatutOrderByDateCreationDesc(String statut);

    List<Reclamation> findByTicketIdOrderByDateCreationDesc(Long ticketId);

    boolean existsByTicketIdAndStatutIn(Long ticketId, List<String> statuts);
}
