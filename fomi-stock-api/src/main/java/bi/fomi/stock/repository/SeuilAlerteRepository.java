package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.SeuilAlerte;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface SeuilAlerteRepository extends JpaRepository<SeuilAlerte, Long> {
    Optional<SeuilAlerte> findByDepotIdAndEngraisTypeId(Long depotId, Long engraisTypeId);
    List<SeuilAlerte> findByDepotId(Long depotId);
}
