package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class MouvementIntegrationTest extends BaseIntegrationTest {

    @Test
    void receptionAjouteAuStock() throws Exception {
        String token = tokenAdmin();
        long avant = stockDepot(token, 2, "UREE");
        assertThat(avant).isEqualTo(1200);

        MvcResult result = apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 10,
                "commentaire", "Réception test"));
        assertThat(code(result)).isEqualTo(200);
        JsonNode m = node(result);
        assertThat(m.get("type").asText()).isEqualTo("RECEPTION_FOMI");
        assertThat(m.get("quantite").asInt()).isEqualTo(10);
        assertThat(m.get("depotDestCode").asText()).isEqualTo("DEP-BUB-P");
        assertThat(m.get("lotNumero").asText()).isEqualTo("LOT-UREE-2026-001");
        assertThat(m.get("agentUsername").asText()).isEqualTo("admin");

        assertThat(stockDepot(token, 2, "UREE")).isEqualTo(1210);
    }

    @Test
    void receptionRespecteIdempotence() throws Exception {
        String token = tokenAdmin();
        Map<String, Object> body = Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 5,
                "idempotencyKey", "reception-uniq-01");
        assertThat(code(apiPost("/api/mouvements/reception", token, body))).isEqualTo(200);
        MvcResult second = apiPost("/api/mouvements/reception", token, body);
        assertThat(code(second)).isEqualTo(400);
    }

    @Test
    void receptionQuantiteDepasseLotRefusee() throws Exception {
        MvcResult result = apiPost("/api/mouvements/reception", tokenAdmin(), Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 99999));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void receptionLotInexistant() throws Exception {
        MvcResult result = apiPost("/api/mouvements/reception", tokenAdmin(), Map.of(
                "lotId", 999999,
                "depotDestId", 2,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void receptionDepotInexistant() throws Exception {
        MvcResult result = apiPost("/api/mouvements/reception", tokenAdmin(), Map.of(
                "lotId", 1,
                "depotDestId", 999999,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void receptionSansLotRefusee() throws Exception {
        MvcResult result = apiPost("/api/mouvements/reception", tokenAdmin(), Map.of(
                "depotDestId", 2,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void superviseurInterditReception() throws Exception {
        MvcResult result = apiPost("/api/mouvements/reception", token("superviseur"), Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void nonAdminInterditTransfert() throws Exception {
        MvcResult result = apiPost("/api/mouvements/transfert", token("agent.zone"), Map.of(
                "lotId", 1,
                "depotSourceId", 1,
                "depotDestId", 2,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void transfertMetAJourSourceEtDest() throws Exception {
        String token = tokenAdmin();
        assertThat(stockDepot(token, 1, "UREE")).isEqualTo(1500);
        assertThat(stockDepot(token, 4, "UREE")).isEqualTo(400);

        MvcResult result = apiPost("/api/mouvements/transfert", token, Map.of(
                "lotId", 1,
                "depotSourceId", 1,
                "depotDestId", 4,
                "quantite", 100,
                "commentaire", "Transfert test"));
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(1);
        assertThat(array.get(0).get("type").asText()).isEqualTo("TRANSFERT");
        assertThat(array.get(0).get("depotSourceCode").asText()).isEqualTo("DEP-GIT-P");
        assertThat(array.get(0).get("depotDestCode").asText()).isEqualTo("DEP-GIT-Z");

        assertThat(stockDepot(token, 1, "UREE")).isEqualTo(1400);
        assertThat(stockDepot(token, 4, "UREE")).isEqualTo(500);
    }

    @Test
    void transfertSourceEgaleDestRefuse() throws Exception {
        MvcResult result = apiPost("/api/mouvements/transfert", tokenAdmin(), Map.of(
                "lotId", 1,
                "depotSourceId", 1,
                "depotDestId", 1,
                "quantite", 10));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void transfertStockInsuffisantRefuse() throws Exception {
        MvcResult result = apiPost("/api/mouvements/transfert", tokenAdmin(), Map.of(
                "lotId", 1,
                "depotSourceId", 1,
                "depotDestId", 4,
                "quantite", 99999));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void transfertLotAbsentDuDepotRefuse() throws Exception {
        MvcResult result = apiPost("/api/mouvements/transfert", tokenAdmin(), Map.of(
                "lotId", 1,
                "depotSourceId", 4,
                "depotDestId", 2,
                "quantite", 10));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void listerMouvements() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 3)))).isEqualTo(200);

        MvcResult result = apiGet("/api/mouvements", token);
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("content").size()).isGreaterThanOrEqualTo(1);
    }

    @Test
    void listerMouvementsParLot() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 7)))).isEqualTo(200);

        MvcResult result = apiGet("/api/mouvements/lot/1", token);
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isGreaterThanOrEqualTo(1);
        assertThat(array.get(0).get("type").asText()).isEqualTo("RECEPTION_FOMI");
    }
}
