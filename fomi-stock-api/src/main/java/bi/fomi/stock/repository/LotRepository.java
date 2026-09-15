package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Lot;
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface LotRepository extends JpaRepository<Lot, Long> {
    Optional<Lot> findByNumeroLot(String numeroLot);

    List<Lot> findByEngraisTypeIdOrderByDateReceptionFomiAsc(Long engraisTypeId);

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT l FROM Lot l WHERE l.id = :id")
    Optional<Lot> findByIdForUpdate(@Param("id") Long id);
}
