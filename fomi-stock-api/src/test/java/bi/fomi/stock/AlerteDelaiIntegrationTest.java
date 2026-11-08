package bi.fomi.stock;

import bi.fomi.stock.model.entity.Alerte;
import bi.fomi.stock.model.enums.TypeAlerte;
import bi.fomi.stock.repository.AlerteRepository;
import bi.fomi.stock.service.AlerteService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class AlerteDelaiIntegrationTest extends BaseIntegrationTest {

    @Autowired
    private AlerteService alerteService;

    @Autowired
    private AlerteRepository alerteRepository;

    @Test
    void verifierDelaisDepasseCreeAlertes() {
        alerteService.verifierDelaisDepasse();

        List<Alerte> depots = alerteRepository.findByDepotIdOrderByCreatedAtDesc(6L);
        boolean delaiTrouve = depots.stream()
                .anyMatch(a -> a.getType() == TypeAlerte.DELAI_DEPASSE);
        assertThat(delaiTrouve).as("Alerte DELAI_DEPASSE attendue pour DEP-MUT (tickets 1247/1248 en retard)")
                .isTrue();

        List<Alerte> delais = depots.stream()
                .filter(a -> a.getType() == TypeAlerte.DELAI_DEPASSE)
                .toList();
        assertThat(delais).hasSize(1);
        assertThat(delais.get(0).getMessage()).contains("tickets en retard");
    }

    @Test
    void verifierDelaisDepasseSurTicketRecouvrement() {
        alerteService.verifierDelaisDepasse();

        List<Alerte> musigati = alerteRepository.findByDepotIdOrderByCreatedAtDesc(8L);
        boolean delaiTrouve = musigati.stream()
                .anyMatch(a -> a.getType() == TypeAlerte.DELAI_DEPASSE);
        assertThat(delaiTrouve).as("Ticket 1250 (PAYE, 2025-11-01) doit déclencher DELAI_DEPASSE à DEP-MUS")
                .isTrue();
    }

    @Test
    void verifierDelaisDepasseSansTicketEnRetard() {
        alerteService.verifierDelaisDepasse();
        alerteService.verifierDelaisDepasse();

        List<Alerte> depots = alerteRepository.findByDepotIdOrderByCreatedAtDesc(6L);
        long delais = depots.stream()
                .filter(a -> a.getType() == TypeAlerte.DELAI_DEPASSE)
                .count();
        assertThat(delais).as("Pas de doublon : l'alerte existe déjà").isEqualTo(1);
    }
}
