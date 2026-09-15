package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.StockLot;
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;

import java.util.List;
import java.util.Optional;

public interface StockLotRepository extends JpaRepository<StockLot, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    Optional<StockLot> findByDepotIdAndLotId(Long depotId, Long lotId);

    List<StockLot> findByDepotIdAndLotEngraisTypeIdOrderByLotDateReceptionFomiAsc(
            Long depotId, Long engraisTypeId);

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    List<StockLot> findByDepotIdAndLotEngraisTypeIdAndQuantiteGreaterThanOrderByLotDateReceptionFomiAsc(
            Long depotId, Long engraisTypeId, Integer quantiteMin);

    @org.springframework.data.jpa.repository.Query(
            "SELECT COALESCE(SUM(sl.quantite), 0) FROM StockLot sl WHERE sl.lot.id = :lotId")
    int sumQuantiteByLot(@org.springframework.data.repository.query.Param("lotId") Long lotId);
}
