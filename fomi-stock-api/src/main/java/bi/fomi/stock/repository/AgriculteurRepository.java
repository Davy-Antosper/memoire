package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Agriculteur;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface AgriculteurRepository extends JpaRepository<Agriculteur, Long> {
    Optional<Agriculteur> findByNumeroIdentite(String numeroIdentite);

    List<Agriculteur> findByTelephone(String telephone);

    boolean existsByTelephone(String telephone);
}
