package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Colline;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface CollineRepository extends JpaRepository<Colline, Long> {
    List<Colline> findByZoneId(Long zoneId);

    Optional<Colline> findByCode(String code);
}
