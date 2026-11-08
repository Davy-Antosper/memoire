package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Commune;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface CommuneRepository extends JpaRepository<Commune, Long> {
    List<Commune> findByProvinceId(Long provinceId);

    Optional<Commune> findByCode(String code);
}
