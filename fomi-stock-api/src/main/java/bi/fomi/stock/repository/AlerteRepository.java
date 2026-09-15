package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Alerte;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AlerteRepository extends JpaRepository<Alerte, Long> {
    List<Alerte> findByTraiteeFalseOrderByCreatedAtDesc();

    List<Alerte> findByDepotIdOrderByCreatedAtDesc(Long depotId);

    List<Alerte> findByDepotIdAndEngraisTypeIdAndTypeAndTraiteeFalse(Long depotId, Long engraisTypeId,
                                                                     bi.fomi.stock.model.enums.TypeAlerte type);
}
