package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import bi.fomi.stock.repository.AuditLogRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.MvcResult;

import java.time.LocalDate;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class SecuriteRbacIntegrationTest extends BaseIntegrationTest {

    @Autowired
    private AuditLogRepository auditLogRepository;

    // ---- RBAC : dépôts (création/modification réservées à ADMIN) ----

    @Test
    void agentZoneNePeutPasCreerUnDepot() throws Exception {
        MvcResult result = apiPost("/api/depots", token("agent.zone"), Map.of(
                "code", "DEP-RBAC-1",
                "nom", "Interdit",
                "niveau", "PROVINCE",
                "provinceId", 1));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void superviseurNePeutPasCreerUnDepot() throws Exception {
        MvcResult result = apiPost("/api/depots", token("superviseur"), Map.of(
                "code", "DEP-RBAC-2",
                "nom", "Interdit",
                "niveau", "PROVINCE",
                "provinceId", 1));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void agentZoneNePeutPasModifierUnSeuilDAlerte() throws Exception {
        MvcResult result = apiPut("/api/depots/9", token("agent.zone"), Map.of(
                "code", "DEP-MWE",
                "nom", "Dépôt Zone Mwendo",
                "niveau", "ZONE",
                "zoneId", 4,
                "seuilAlerteMin", 5));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void agentLogistiqueNePeutPasCreerUnDepot() throws Exception {
        MvcResult result = apiPost("/api/depots", token("agent.fomi"), Map.of(
                "code", "DEP-RBAC-3",
                "nom", "Interdit",
                "niveau", "PROVINCE",
                "provinceId", 1));
        assertThat(code(result)).isEqualTo(403);
    }

    // ---- RBAC : agriculteurs (agents de distribution autorisés, FOMI interdit) ----

    @Test
    void agentCollinePeutCreerUnAgriculteur() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", token("agent.colline"), Map.of(
                "numeroIdentite", "AGR-RBAC-01",
                "nom", "Zonze",
                "prenom", "Z",
                "telephone", "79660001",
                "collineId", 6));
        assertThat(code(result)).isEqualTo(200);
    }

    @Test
    void agentLogistiqueNePeutPasCreerUnAgriculteur() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", token("agent.fomi"), Map.of(
                "numeroIdentite", "AGR-RBAC-02",
                "nom", "Fomi",
                "prenom", "F",
                "collineId", 1));
        assertThat(code(result)).isEqualTo(403);
    }

    // ---- RBAC : tickets (agents de distribution autorisés, FOMI interdit) ----

    @Test
    void agentZonePeutCreerUnTicket() throws Exception {
        MvcResult result = apiPost("/api/tickets", token("agent.zone"), Map.of(
                "numeroTicket", "TKT-RBAC-001",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 2,
                "montantPaye", 50000,
                "datePaiement", "2026-03-15",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(200);
    }

    @Test
    void agentLogistiqueNePeutPasCreerUnTicket() throws Exception {
        MvcResult result = apiPost("/api/tickets", token("agent.fomi"), Map.of(
                "numeroTicket", "TKT-RBAC-002",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 2,
                "montantPaye", 50000,
                "datePaiement", "2026-03-15",
                "depotRetraitId", 6,
                "saison", "2026A"));
        assertThat(code(result)).isEqualTo(403);
    }

    // ---- RBAC : distributions (FOMI interdit) ----

    @Test
    void agentLogistiqueNePeutPasDistribuer() throws Exception {
        long ticketId = creerTicketActif(tokenAdmin(), "TKT-RBAC-003", 2, 1);
        MvcResult result = apiPost("/api/distributions", token("agent.fomi"), Map.of(
                "ticketId", ticketId,
                "depotId", 1,
                "quantite", 2));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void superviseurPeutDistribuer() throws Exception {
        long ticketId = creerTicketActif(tokenAdmin(), "TKT-RBAC-004", 2, 1);
        MvcResult result = apiPost("/api/distributions", token("superviseur"), Map.of(
                "ticketId", ticketId,
                "depotId", 1,
                "quantite", 2));
        assertThat(code(result)).isEqualTo(200);
    }

    // ---- Lots : validation des dates et numéro auto-généré ----

    @Test
    void lotPeremptionAvantFabricationRefuse() throws Exception {
        MvcResult result = apiPost("/api/lots", tokenAdmin(), Map.of(
                "numeroLot", "LOT-RBAC-001",
                "engraisTypeId", 2,
                "quantiteInitiale", 100,
                "dateFabrication", "2026-08-01",
                "datePeremption", "2026-07-01"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void lotDejaPerimeRefuse() throws Exception {
        MvcResult result = apiPost("/api/lots", tokenAdmin(), Map.of(
                "numeroLot", "LOT-RBAC-002",
                "engraisTypeId", 2,
                "quantiteInitiale", 100,
                "dateFabrication", "2020-01-01",
                "datePeremption", "2020-06-01"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void lotSansNumeroAutoGenere() throws Exception {
        MvcResult result = apiPost("/api/lots", tokenAdmin(), Map.of(
                "engraisTypeId", 2,
                "quantiteInitiale", 100,
                "dateFabrication", "2026-07-01",
                "datePeremption", "2027-07-01"));
        assertThat(code(result)).isEqualTo(200);
        JsonNode lot = node(result);
        assertThat(lot.get("numeroLot").asText())
                .startsWith("FOMI-" + LocalDate.now().getYear() + "-");
    }

    // ---- Agriculteurs : modification + doublon de téléphone ----

    @Test
    void modifierAgriculteur() throws Exception {
        MvcResult created = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-RBAC-03",
                "nom", "Avant",
                "prenom", "X",
                "telephone", "79660003",
                "collineId", 1));
        long id = node(created).get("id").asLong();

        MvcResult updated = apiPut("/api/agriculteurs/" + id, tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-RBAC-03",
                "nom", "Apres",
                "prenom", "X",
                "telephone", "79660004",
                "collineId", 1));
        assertThat(code(updated)).isEqualTo(200);
        JsonNode a = node(updated);
        assertThat(a.get("nom").asText()).isEqualTo("Apres");
        assertThat(a.get("telephone").asText()).isEqualTo("79660004");
    }

    @Test
    void modifierAgriculteurTelephoneDoublonRefuse() throws Exception {
        MvcResult premier = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-RBAC-04",
                "nom", "Un",
                "prenom", "A",
                "telephone", "79660005",
                "collineId", 1));
        MvcResult second = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-RBAC-05",
                "nom", "Deux",
                "prenom", "B",
                "telephone", "79660006",
                "collineId", 1));
        long id2 = node(second).get("id").asLong();

        MvcResult conflict = apiPut("/api/agriculteurs/" + id2, tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-RBAC-05",
                "nom", "Deux",
                "prenom", "B",
                "telephone", "79660005",
                "collineId", 1));
        assertThat(code(conflict)).isEqualTo(400);
        assertThat(node(premier).get("id").asLong()).isNotEqualTo(id2);
    }

    // ---- Audit des nouvelles actions ----

    @Test
    void creationDepotTracee() throws Exception {
        MvcResult result = apiPost("/api/depots", tokenAdmin(), Map.of(
                "code", "DEP-AUDIT-1",
                "nom", "Audit Depot",
                "niveau", "PROVINCE",
                "provinceId", 1));
        long depotId = node(result).get("id").asLong();
        assertThat(auditLogRepository.findByEntityTypeAndEntityIdOrderByCreatedAtDesc("Depot", depotId))
                .anyMatch(l -> "DEPOT_CREATE".equals(l.getAction()));
    }

    @Test
    void creationLotTracee() throws Exception {
        MvcResult result = apiPost("/api/lots", tokenAdmin(), Map.of(
                "numeroLot", "LOT-AUDIT-1",
                "engraisTypeId", 2,
                "quantiteInitiale", 100));
        long lotId = node(result).get("id").asLong();
        assertThat(auditLogRepository.findByEntityTypeAndEntityIdOrderByCreatedAtDesc("Lot", lotId))
                .anyMatch(l -> "LOT_CREATE".equals(l.getAction()));
    }

    @Test
    void creationAgriculteurTracee() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-AUDIT-01",
                "nom", "Audit",
                "prenom", "A",
                "telephone", "79660007",
                "collineId", 1));
        long id = node(result).get("id").asLong();
        assertThat(auditLogRepository.findByEntityTypeAndEntityIdOrderByCreatedAtDesc("Agriculteur", id))
                .anyMatch(l -> "AGRICULTEUR_CREATE".equals(l.getAction()));
    }
}
