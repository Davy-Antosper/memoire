package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class TicketIntegrationTest extends BaseIntegrationTest {

    @Test
    void listerTous() throws Exception {
        MvcResult result = apiGet("/api/tickets", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("content").size()).isEqualTo(5);
    }

    @Test
    void listerParDepot() throws Exception {
        MvcResult result = apiGet("/api/tickets?depotId=6", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result).get("content");
        assertThat(array.size()).isEqualTo(2);
        for (JsonNode t : array) {
            assertThat(t.get("depotRetraitCode").asText()).isEqualTo("DEP-MUT");
        }
    }

    @Test
    void listerParStatut() throws Exception {
        MvcResult result = apiGet("/api/tickets?statut=PAYE", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result).get("content");
        assertThat(array.size()).isEqualTo(1);
        assertThat(array.get(0).get("numeroTicket").asText()).isEqualTo("TKT-2026-1251");
    }

    @Test
    void listerParDepotEtStatut() throws Exception {
        MvcResult aucunStatut = apiGet("/api/tickets?depotId=6", tokenAdmin());
        assertThat(node(aucunStatut).get("content").size()).isEqualTo(2);

        MvcResult paye = apiGet("/api/tickets?depotId=6&statut=PAYE", tokenAdmin());
        assertThat(code(paye)).isEqualTo(200);
        assertThat(node(paye).get("content").size()).isZero();

        MvcResult partiel = apiGet("/api/tickets?depotId=6&statut=PARTIEL", tokenAdmin());
        JsonNode array = node(partiel).get("content");
        assertThat(array.size()).isEqualTo(1);
        assertThat(array.get(0).get("numeroTicket").asText()).isEqualTo("TKT-2026-1247");
        assertThat(array.get(0).get("depotRetraitCode").asText()).isEqualTo("DEP-MUT");
    }

    @Test
    void getById() throws Exception {
        MvcResult result = apiGet("/api/tickets/1", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode t = node(result);
        assertThat(t.get("numeroTicket").asText()).isEqualTo("TKT-2026-1247");
        assertThat(t.get("statut").asText()).isEqualTo("PARTIEL");
        assertThat(t.get("quantiteCommandee").asInt()).isEqualTo(5);
        assertThat(t.get("quantiteServie").asInt()).isEqualTo(3);
        assertThat(t.get("quantiteRestante").asInt()).isEqualTo(2);
        assertThat(t.get("engraisTypeCode").asText()).isEqualTo("UREE");
        assertThat(t.get("depotRetraitCode").asText()).isEqualTo("DEP-MUT");
        assertThat(t.get("agriculteurNomComplet").asText()).isEqualTo("Ndayisaba Jean");
    }

    @Test
    void getByIdInexistant() throws Exception {
        MvcResult result = apiGet("/api/tickets/999999", tokenAdmin());
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void creerTicket() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", "TKT-NEW-0001",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 4,
                "montantPaye", 100000,
                "datePaiement", "2026-03-01",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(200);
        JsonNode created = node(result);
        long id = created.get("id").asLong();
        assertThat(created.get("numeroTicket").asText()).isEqualTo("TKT-NEW-0001");
        assertThat(created.get("statut").asText()).isEqualTo("EN_ATTENTE_DE_VALIDATION");
        assertThat(created.get("quantiteRestante").asInt()).isEqualTo(4);

        JsonNode fetched = node(apiGet("/api/tickets/" + id, token));
        assertThat(fetched.get("numeroTicket").asText()).isEqualTo("TKT-NEW-0001");
    }

    @Test
    void creerNumeroDoublonRefuse() throws Exception {
        MvcResult result = apiPost("/api/tickets", tokenAdmin(), Map.of(
                "numeroTicket", "TKT-2026-1247",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 2,
                "montantPaye", 50000,
                "datePaiement", "2026-03-01",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void creerAgriculteurInexistant() throws Exception {
        MvcResult result = apiPost("/api/tickets", tokenAdmin(), Map.of(
                "numeroTicket", "TKT-NEW-0002",
                "agriculteurId", 999999,
                "engraisTypeId", 1,
                "quantiteCommandee", 2,
                "montantPaye", 50000,
                "datePaiement", "2026-03-01",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void creerDepotInexistant() throws Exception {
        MvcResult result = apiPost("/api/tickets", tokenAdmin(), Map.of(
                "numeroTicket", "TKT-NEW-0003",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 2,
                "montantPaye", 50000,
                "datePaiement", "2026-03-01",
                "depotRetraitId", 999999,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void creerQuantiteZeroRefuse() throws Exception {
        MvcResult result = apiPost("/api/tickets", tokenAdmin(), Map.of(
                "numeroTicket", "TKT-NEW-0004",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 0,
                "montantPaye", 0,
                "datePaiement", "2026-03-01",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void modifierTicketNonServi() throws Exception {
        String token = tokenAdmin();
        MvcResult create = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", "TKT-EDIT-0001",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 4,
                "montantPaye", 100000,
                "datePaiement", "2026-03-01",
                "depotRetraitId", 6,
                "saison", "2026A"));
        long id = node(create).get("id").asLong();

        MvcResult update = apiPut("/api/tickets/" + id, token, Map.of(
                "numeroTicket", "TKT-EDIT-0001",
                "agriculteurId", 1,
                "engraisTypeId", 2,
                "quantiteCommandee", 7,
                "montantPaye", 175000,
                "datePaiement", "2026-03-10",
                "depotRetraitId", 4,
                "saison", "2026A"));
        assertThat(code(update)).isEqualTo(200);
        JsonNode updated = node(update);
        assertThat(updated.get("quantiteCommandee").asInt()).isEqualTo(7);
        assertThat(updated.get("engraisTypeCode").asText()).isEqualTo("NPK");
        assertThat(updated.get("depotRetraitCode").asText()).isEqualTo("DEP-GIT-Z");
    }

    @Test
    void modifierTicketDejaServiRefuse() throws Exception {
        MvcResult result = apiPut("/api/tickets/1", tokenAdmin(), Map.of(
                "numeroTicket", "TKT-2026-1247",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 10,
                "montantPaye", 200000,
                "datePaiement", "2026-03-01",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void agentCollineNePeutPasModifierUnTicket() throws Exception {
        MvcResult result = apiPut("/api/tickets/5", token("agent.colline"), Map.of(
                "numeroTicket", "TKT-2026-1251",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 2,
                "montantPaye", 50000,
                "datePaiement", "2026-03-01",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(403);
    }
}
