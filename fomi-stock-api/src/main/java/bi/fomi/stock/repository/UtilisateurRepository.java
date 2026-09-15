package bi.fomi.stock.repository;

import bi.fomi.stock.model.entity.Utilisateur;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UtilisateurRepository extends JpaRepository<Utilisateur, Long> {
    Optional<Utilisateur> findByUsername(String username);

    boolean existsByUsername(String username);
}
