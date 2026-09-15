package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class AlerteIntegrationTest extends BaseIntegrationTest {

    @Test
    void listerAlertes() throws Exception {
        MvcResult result = apiGet("/api/alertes", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).size()).isEqualTo(2);
    }

    @Test
    void listerAlertesNonTraitees() throws Exception {
        MvcResult result = apiGet("/api/alertes?nonTraitees=true", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(2);
        for (JsonNode a : array) {
            assertThat(a.get("traitee").asBoolean()).isFalse();
        }
    }

    @Test
    void alertesParDepot() throws Exception {
        MvcResult result = apiGet("/api/alertes/depot/3", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(1);
        JsonNode a = array.get(0);
        assertThat(a.get("depotCode").asText()).isEqualTo("DEP-NGO-P");
        assertThat(a.get("engraisTypeCode").asText()).isEqualTo("UREE");
        assertThat(a.get("type").asText()).isEqualTo("RUPTURE");
        assertThat(a.get("niveau").asText()).isEqualTo("CRITICAL");
        assertThat(a.get("traitee").asBoolean()).isFalse();
    }

    @Test
    void traiterAlerte() throws Exception {
        String token = tokenAdmin();
        JsonNode alertes = node(apiGet("/api/alertes?nonTraitees=true", token));
        long ruptureId = -1;
        for (JsonNode a : alertes) {
            if ("RUPTURE".equals(a.get("type").asText())) {
                ruptureId = a.get("id").asLong();
            }
        }
        assertThat(ruptureId).isGreaterThan(0);

        MvcResult result = apiPatch("/api/alertes/" + ruptureId + "/traiter", token);
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("traitee").asBoolean()).isTrue();

        JsonNode restantes = node(apiGet("/api/alertes?nonTraitees=true", token));
        assertThat(restantes.size()).isEqualTo(1);
    }

    @Test
    void traiterAlerteInexistante() throws Exception {
        MvcResult result = apiPatch("/api/alertes/999999/traiter", tokenAdmin());
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void nonAdminNePeutPasTraiter() throws Exception {
        MvcResult result = apiPatch("/api/alertes/1/traiter", token("agent.zone"));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void receptionDeclencheAlerteStockBas() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 8,
                "quantite", 5)))).isEqualTo(200);

        JsonNode alertes = node(apiGet("/api/alertes/depot/8", token));
        boolean stockBas = false;
        for (JsonNode a : alertes) {
            if ("STOCK_BAS".equals(a.get("type").asText())) {
                stockBas = true;
                assertThat(a.get("niveau").asText()).isEqualTo("WARNING");
            }
        }
        assertThat(stockBas).isTrue();
    }

    @Test
    void demandeNonServieSuperieureAuStockDeclencheAlerte() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/tickets", token, Map.of(
                "numeroTicket", "TKT-DEM-001",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 200,
                "montantPaye", 200 * 25000L,
                "datePaiement", "2026-04-01",
                "depotRetraitId", 8,
                "saison", "2026A")))).isEqualTo(200);

        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 8,
                "quantite", 5)))).isEqualTo(200);

        JsonNode alertes = node(apiGet("/api/alertes/depot/8", token));
        boolean demandeSup = false;
        for (JsonNode a : alertes) {
            if ("DEMANDE_SUP_STOCK".equals(a.get("type").asText())) {
                demandeSup = true;
                assertThat(a.get("niveau").asText()).isEqualTo("WARNING");
            }
        }
        assertThat(demandeSup).isTrue();
    }
}
