package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Stock;
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;

import java.util.List;
import java.util.Optional;

public interface StockRepository extends JpaRepository<Stock, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    Optional<Stock> findByDepotIdAndEngraisTypeId(Long depotId, Long engraisTypeId);

    List<Stock> findByDepotIdOrderByEngraisTypeCode(Long depotId);

    List<Stock> findByEngraisTypeIdAndQuantiteDisponibleGreaterThan(Long engraisTypeId, Integer min);
}
