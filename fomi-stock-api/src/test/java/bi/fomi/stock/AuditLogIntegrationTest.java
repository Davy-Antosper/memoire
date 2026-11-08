package bi.fomi.stock;

import bi.fomi.stock.model.entity.AuditLog;
import bi.fomi.stock.repository.AuditLogRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.MvcResult;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class AuditLogIntegrationTest extends BaseIntegrationTest {

    @Autowired
    private AuditLogRepository auditLogRepository;

    @Test
    void creationTicketTracee() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", "TKT-AUDIT-001",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 3,
                "montantPaye", 75000,
                "datePaiement", "2026-03-20",
                "depotRetraitId", 6,
                "saison", "2027A"));
        long ticketId = node(result).get("id").asLong();

        List<AuditLog> logs = auditLogRepository.findByEntityTypeAndEntityIdOrderByCreatedAtDesc("Ticket", ticketId);
        assertThat(logs).hasSize(1);
        assertThat(logs.get(0).getAction()).isEqualTo("TICKET_CREATE");
        assertThat(logs.get(0).getUtilisateur().getUsername()).isEqualTo("admin");
        assertThat(logs.get(0).getDetailsJson()).contains("TKT-AUDIT-001");
    }

    @Test
    void distributionTracee() throws Exception {
        String token = tokenAdmin();
        MvcResult ticketResult = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", "TKT-AUDIT-002",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 2,
                "montantPaye", 50000,
                "datePaiement", "2026-03-20",
                "depotRetraitId", 6,
                "saison", "2027A"));
        long ticketId = node(ticketResult).get("id").asLong();
        assertThat(code(apiPatch("/api/tickets/" + ticketId + "/activer", token))).isEqualTo(200);

        assertThat(code(apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 6,
                "quantite", 2)))).isEqualTo(200);

        List<AuditLog> logs = auditLogRepository.findByEntityTypeAndEntityIdOrderByCreatedAtDesc("Ticket", ticketId);
        assertThat(logs).hasSize(3);
        assertThat(logs.get(0).getAction()).isEqualTo("DISTRIBUTION_CREATE");
    }

    @Test
    void receptionTracee() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 6)))).isEqualTo(200);

        List<AuditLog> logs = auditLogRepository.findAll().stream()
                .filter(l -> "MOUVEMENT_RECEPTION".equals(l.getAction()))
                .toList();
        assertThat(logs).isNotEmpty();
        assertThat(logs.get(0).getDetailsJson()).contains("\"depot\":\"DEP-BUJ-P\"");
    }

    @Test
    void transfertTracee() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/transfert", token, Map.of(
                "lotId", 1,
                "depotSourceId", 1,
                "depotDestId", 4,
                "quantite", 20)))).isEqualTo(200);

        List<AuditLog> logs = auditLogRepository.findAll().stream()
                .filter(l -> "MOUVEMENT_TRANSFERT".equals(l.getAction()))
                .toList();
        assertThat(logs).isNotEmpty();
        assertThat(logs.get(0).getDetailsJson()).contains("\"source\":\"DEP-GIT-P\"");
    }
}
