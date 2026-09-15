package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Distribution;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface DistributionRepository extends JpaRepository<Distribution, Long> {
    List<Distribution> findByTicketId(Long ticketId);

    List<Distribution> findByLotId(Long lotId);
}
