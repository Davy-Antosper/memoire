package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class DistributionFifoIntegrationTest extends BaseIntegrationTest {

    private long creerTicket(String token, String numero, int quantite, long depotId) throws Exception {
        MvcResult result = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", numero,
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", quantite,
                "montantPaye", quantite * 25000L,
                "datePaiement", "2026-04-01",
                "depotRetraitId", depotId,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(200);
        long id = node(result).get("id").asLong();
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(200);
        return id;
    }

    @Test
    void distributionSertLeLotLePlusAncien() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 2,
                "depotDestId", 1,
                "quantite", 100)))).isEqualTo(200);

        long ticketId = creerTicket(token, "TKT-FIFO-001", 10, 1);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 1,
                "quantite", 10));
        assertThat(code(result)).isEqualTo(200);

        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(1);
        assertThat(array.get(0).get("lotNumero").asText())
                .as("Le lot LOT-IMBURA-2026-001 (reçu le premier) doit être consommé en FIFO")
                .isEqualTo("LOT-IMBURA-2026-001");
    }

    @Test
    void distributionLotForce() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 2,
                "depotDestId", 1,
                "quantite", 50)))).isEqualTo(200);

        long ticketId = creerTicket(token, "TKT-FIFO-002", 5, 1);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 1,
                "quantite", 5,
                "lotId", 2));
        assertThat(code(result)).isEqualTo(200);

        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(1);
        assertThat(array.get(0).get("lotNumero").asText()).isEqualTo("LOT-IMBURA-2026-002");
    }

    @Test
    void distributionLotAbsentDuDepotRefuse() throws Exception {
        String token = tokenAdmin();
        long ticketId = creerTicket(token, "TKT-FIFO-003", 2, 1);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 1,
                "quantite", 2,
                "lotId", 3));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionLotForceTypeDifferentRefuse() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 3,
                "depotDestId", 1,
                "quantite", 100)))).isEqualTo(200);

        long ticketId = creerTicket(token, "TKT-FIFO-004", 5, 1);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 1,
                "quantite", 5,
                "lotId", 3));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionLotForceQuantiteInsuffisanteRefuse() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 2,
                "depotDestId", 1,
                "quantite", 5)))).isEqualTo(200);

        long ticketId = creerTicket(token, "TKT-FIFO-005", 10, 1);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", ticketId,
                "depotId", 1,
                "quantite", 10,
                "lotId", 2));
        assertThat(code(result)).isEqualTo(400);
    }
}
