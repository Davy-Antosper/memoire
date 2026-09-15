package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class ValidationTicketIntegrationTest extends BaseIntegrationTest {

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
        return node(result).get("id").asLong();
    }

    @Test
    void creationTicketStatutEnAttenteDeValidation() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-000", 2);
        JsonNode ticket = node(apiGet("/api/tickets/" + id, token));
        assertThat(ticket.get("statut").asText()).isEqualTo("EN_ATTENTE_DE_VALIDATION");
    }

    @Test
    void superviseurPeutActiverUnTicket() throws Exception {
        String token = token("superviseur");
        long id = creerTicket(token("admin"), "TKT-VAL-001", 3);
        MvcResult result = apiPatch("/api/tickets/" + id + "/activer", token);
        assertThat(code(result)).isEqualTo(200);
        JsonNode ticket = node(apiGet("/api/tickets/" + id, token("admin")));
        assertThat(ticket.get("statut").asText()).isEqualTo("ACTIF");
    }

    @Test
    void adminPeutActiverUnTicket() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-002", 3);
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(200);
    }

    @Test
    void agentZoneNePeutPasActiverUnTicket() throws Exception {
        long id = creerTicket(tokenAdmin(), "TKT-VAL-003", 3);
        MvcResult result = apiPatch("/api/tickets/" + id + "/activer", token("agent.zone"));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void activerDeuxFoisRefuse() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-004", 3);
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(200);
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(400);
    }

    @Test
    void rejeterUnTicketAvecMotif() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-005", 3);
        MvcResult result = apiPatch("/api/tickets/" + id + "/rejeter", token, Map.of("motif", "Paiement non confirmé"));
        assertThat(code(result)).isEqualTo(200);
        JsonNode ticket = node(apiGet("/api/tickets/" + id, token));
        assertThat(ticket.get("statut").asText()).isEqualTo("REJETE");
    }

    @Test
    void rejeterSansMotifAccepte() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-006", 3);
        assertThat(code(apiPatch("/api/tickets/" + id + "/rejeter", token))).isEqualTo(200);
    }

    @Test
    void activerTicketRejeteRefuse() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-007", 3);
        assertThat(code(apiPatch("/api/tickets/" + id + "/rejeter", token))).isEqualTo(200);
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(400);
    }

    @Test
    void distributionTicketEnAttenteRefusee() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-008", 2);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", id,
                "depotId", 6,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionTicketRejeteRefusee() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-009", 2);
        assertThat(code(apiPatch("/api/tickets/" + id + "/rejeter", token))).isEqualTo(200);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", id,
                "depotId", 6,
                "quantite", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void distributionTicketActifAutorisee() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-010", 2);
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(200);
        MvcResult result = apiPost("/api/distributions", token, Map.of(
                "ticketId", id,
                "depotId", 6,
                "quantite", 2));
        assertThat(code(result)).isEqualTo(200);
        JsonNode ticket = node(apiGet("/api/tickets/" + id, token));
        assertThat(ticket.get("statut").asText()).isEqualTo("SERVI");
    }

    @Test
    void modifierTicketEnAttenteReactiveValidation() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-VAL-011", 2);
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(200);

        MvcResult update = apiPut("/api/tickets/" + id, token, Map.of(
                "numeroTicket", "TKT-VAL-011",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 4,
                "montantPaye", 100000,
                "datePaiement", "2026-03-20",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(update)).isEqualTo(200);
        JsonNode updated = node(update);
        assertThat(updated.get("statut").asText()).isEqualTo("EN_ATTENTE_DE_VALIDATION");
    }

    @Test
    void consulterTicketPublic() throws Exception {
        String token = tokenAdmin();
        long id = creerTicket(token, "TKT-PUB-001", 2);
        assertThat(code(apiPatch("/api/tickets/" + id + "/activer", token))).isEqualTo(200);

        MvcResult result = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .get("/api/public/tickets/TKT-PUB-001"))
                .andReturn();
        assertThat(code(result)).isEqualTo(200);
        JsonNode t = node(result);
        assertThat(t.get("numeroTicket").asText()).isEqualTo("TKT-PUB-001");
        assertThat(t.get("statut").asText()).isEqualTo("ACTIF");
        assertThat(t.get("quantiteRestante").asInt()).isEqualTo(2);
        assertThat(t.has("agriculteurId")).isFalse();
    }

    @Test
    void consulterTicketPublicInexistant() throws Exception {
        MvcResult result = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .get("/api/public/tickets/INEXISTANT"))
                .andReturn();
        assertThat(code(result)).isEqualTo(404);
    }

    @Test
    void exportTicketsCsv() throws Exception {
        String token = tokenAdmin();
        MvcResult result = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .get("/api/export/tickets.csv")
                        .header(org.springframework.http.HttpHeaders.AUTHORIZATION, "Bearer " + token))
                .andReturn();
        assertThat(code(result)).isEqualTo(200);
        String csv = content(result);
        assertThat(csv).startsWith("Numéro;Agriculteur");
        assertThat(csv).contains("TKT-2026-1247");
    }

    @Test
    void exportTicketsCsvFiltreParDepot() throws Exception {
        String token = tokenAdmin();
        MvcResult result = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .get("/api/export/tickets.csv?depotId=6")
                        .header(org.springframework.http.HttpHeaders.AUTHORIZATION, "Bearer " + token))
                .andReturn();
        assertThat(code(result)).isEqualTo(200);
        String csv = content(result);
        assertThat(csv).contains("TKT-2026-1247");
        assertThat(csv).doesNotContain("TKT-2026-1251");
    }

    @Test
    @org.springframework.transaction.annotation.Transactional(
            propagation = org.springframework.transaction.annotation.Propagation.NOT_SUPPORTED)
    void exportTicketsCsvHorsTransaction() throws Exception {
        String token = tokenAdmin();
        MvcResult result = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .get("/api/export/tickets.csv")
                        .header(org.springframework.http.HttpHeaders.AUTHORIZATION, "Bearer " + token))
                .andReturn();
        assertThat(code(result)).isEqualTo(200);
        String csv = content(result);
        assertThat(csv).contains("TKT-2026-1247");
    }

    @Test
    void exportMouvementsCsv() throws Exception {
        String token = tokenAdmin();
        assertThat(code(apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 5)))).isEqualTo(200);

        MvcResult result = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .get("/api/export/mouvements.csv")
                        .header(org.springframework.http.HttpHeaders.AUTHORIZATION, "Bearer " + token))
                .andReturn();
        assertThat(code(result)).isEqualTo(200);
        assertThat(content(result)).startsWith("Type;Lot");
    }

    @Test
    void exportSansAuthRefuse() throws Exception {
        MvcResult result = mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                        .get("/api/export/tickets.csv"))
                .andReturn();
        assertThat(code(result)).isIn(401, 403);
    }

    @Test
    void auditLogsListesParAdmin() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiGet("/api/audit-logs", token);
        assertThat(code(result)).isEqualTo(200);
        JsonNode page = node(result);
        assertThat(page.has("content")).isTrue();
    }

    @Test
    void auditLogsFiltreParAction() throws Exception {
        String token = tokenAdmin();
        creerTicket(token, "TKT-AUDIT-100", 2);
        MvcResult result = apiGet("/api/audit-logs?action=TICKET", token);
        assertThat(code(result)).isEqualTo(200);
        JsonNode page = node(result);
        assertThat(page.get("content").size()).isGreaterThan(0);
        for (JsonNode l : page.get("content")) {
            assertThat(l.get("action").asText()).contains("TICKET");
        }
    }

    @Test
    void auditLogsRefusesPourAgentZone() throws Exception {
        MvcResult result = apiGet("/api/audit-logs", token("agent.zone"));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    @org.springframework.transaction.annotation.Transactional(
            propagation = org.springframework.transaction.annotation.Propagation.NOT_SUPPORTED)
    void auditLogsListesHorsTransaction() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiGet("/api/audit-logs", token);
        assertThat(code(result)).isEqualTo(200);
        JsonNode page = node(result);
        assertThat(page.has("content")).isTrue();
    }

    @Test
    void agentLogistiquePeutCreerUnLot() throws Exception {
        String token = token("agent.fomi");
        MvcResult result = apiPost("/api/lots", token, Map.of(
                "numeroLot", "LOT-FOMI-001",
                "engraisTypeId", 1,
                "quantiteInitiale", 500,
                "dateFabrication", "2026-05-01",
                "datePeremption", "2027-05-01"));
        assertThat(code(result)).isEqualTo(200);
    }

    @Test
    void agentLogistiquePeutFaireUneReception() throws Exception {
        String token = token("agent.fomi");
        MvcResult result = apiPost("/api/mouvements/reception", token, Map.of(
                "lotId", 1,
                "depotDestId", 2,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(200);
    }

    @Test
    void agentLogistiquePeutPasTransfeter() throws Exception {
        MvcResult result = apiPost("/api/mouvements/transfert", token("agent.fomi"), Map.of(
                "lotId", 1,
                "depotSourceId", 1,
                "depotDestId", 4,
                "quantite", 5));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void agentLogistiqueNePeutPasActiverUnTicket() throws Exception {
        long id = creerTicket(tokenAdmin(), "TKT-VAL-012", 2);
        MvcResult result = apiPatch("/api/tickets/" + id + "/activer", token("agent.fomi"));
        assertThat(code(result)).isEqualTo(403);
    }
}
