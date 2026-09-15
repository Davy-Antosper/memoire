package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.EngraisType;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface EngraisTypeRepository extends JpaRepository<EngraisType, Long> {
    Optional<EngraisType> findByCode(String code);
}
