package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class DistributionIntegrationTest extends BaseIntegrationTest {

    private long creerTicket(String token, String numero, int quantite) throws Exception {
        MvcResult result = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", numero,
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", quantite,
                "montantPaye", quantite * 25000L,
                "datePaiement", "2026-03-15",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(200);
        long id = node(result).get("id").asLong();
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(200);
        return id;
    }

    @Test
    void distributionPartielleMetAJourLeTicket() throws Exception {
        String token = tokenAdmin();
        long ticketId = creerTicket(token, "TKT-DIST-001", 5);

        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 6,
                "quantite", 2));
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(1);
        assertThat(array.get(0).get("ticketNumero").asText()).isEqualTo("TKT-DIST-001");
        assertThat(array.get(0).get("depotCode").asText()).isEqualTo("DEP-MUT");
        assertThat(array.get(0).get("agentUsername").asText()).isEqualTo("admin");

        JsonNode ticket = node(apiGet("/api/tickets/" + ticketId, token));
        assertThat(ticket.get("statut").asText()).isEqualTo("PARTIEL");
        assertThat(ticket.get("quantiteServie").asInt()).isEqualTo(2);
        assertThat(ticket.get("quantiteRestante").asInt()).isEqualTo(3);
    }

    @Test
    void distributionCompleteSertLeTicket() throws Exception {
        String token = tokenAdmin();
        long ticketId = creerTicket(token, "TKT-DIST-002", 2);

        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 6,
                "quantite", 2));
        assertThat(code(result)).isEqualTo(200);

        JsonNode ticket = node(apiGet("/api/tickets/" + ticketId, token));
        assertThat(ticket.get("statut").asText()).isEqualTo("SERVI");
        assertThat(ticket.get("quantiteRestante").asInt()).isEqualTo(0);
    }

    @Test
    void distributionTicketDejaServiRefusee() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "ticketId", 3,
                "depotId", 7,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionQuantiteSupRestantRefusee() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "ticketId", 2,
                "depotId", 6,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void agentCollineHorsPerimetreRefuse() throws Exception {
        MvcResult result = apiPost("/api/distributions", token("agent.colline"), Map.of(
                "ticketId", 2,
                "depotId", 7,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void agentCollineSurSonDepotAutorise() throws Exception {
        String token = token("agent.colline");
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", 2,
                "depotId", 6,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get(0).get("agentUsername").asText()).isEqualTo("agent.colline");
    }

    @Test
    void agentZoneHorsPerimetreRefuse() throws Exception {
        MvcResult result = apiPost("/api/distributions", token("agent.zone"), Map.of(
                "ticketId", 2,
                "depotId", 1,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void agentZoneDansSaZoneAutorise() throws Exception {
        MvcResult result = apiPost("/api/distributions", token("agent.zone"), Map.of(
                "ticketId", 2,
                "depotId", 4,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get(0).get("agentUsername").asText()).isEqualTo("agent.zone");
    }

    @Test
    void distributionTicketInexistant() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "ticketId", 999999,
                "depotId", 6,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void distributionDepotInexistant() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "ticketId", 2,
                "depotId", 999999,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void distributionQuantiteZeroRefusee() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "ticketId", 2,
                "depotId", 6,
                "quantite", 0));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionStockDepotInsuffisant() throws Exception {
        String token = tokenAdmin();
        long ticketId = creerTicket(token, "TKT-DIST-003", 100);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 6,
                "quantite", 100));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionTicketReclamationRefusee() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "ticketId", 4,
                "depotId", 8,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionSansQuantiteRefusee() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "ticketId", 2,
                "depotId", 6));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionSansTicketRefusee() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "depotId", 6,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionSansDepotRefusee() throws Exception {
        MvcResult result = apiPost("/api/distributions", tokenAdmin(), Map.of(
                "ticketId", 2,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void listerDistributionsDunTicket() throws Exception {
        String token = tokenAdmin();
        long ticketId = creerTicket(token, "TKT-DIST-004", 3);
        assertThat(code(apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 6,
                "quantite", 3)))).isEqualTo(200);

        MvcResult result = apiGet("/api/distributions/ticket/" + ticketId, token);
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(1);
        assertThat(array.get(0).get("ticketNumero").asText()).isEqualTo("TKT-DIST-004");
        assertThat(array.get(0).get("quantite").asInt()).isEqualTo(3);
    }
}
