package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Depot;
import bi.fomi.stock.model.enums.NiveauDepot;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface DepotRepository extends JpaRepository<Depot, Long> {
    Optional<Depot> findByCode(String code);

    List<Depot> findByNiveau(NiveauDepot niveau);

    List<Depot> findByProvinceId(Long provinceId);

    List<Depot> findByZoneId(Long zoneId);
}
