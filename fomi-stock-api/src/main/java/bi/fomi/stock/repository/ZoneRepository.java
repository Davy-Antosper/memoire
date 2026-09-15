package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Zone;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface ZoneRepository extends JpaRepository<Zone, Long> {
    List<Zone> findByProvinceId(Long provinceId);

    Optional<Zone> findByCode(String code);
}
