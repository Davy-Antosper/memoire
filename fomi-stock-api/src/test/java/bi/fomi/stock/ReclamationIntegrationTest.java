package bi.fomi.stock;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class ReclamationIntegrationTest extends BaseIntegrationTest {

    @Test
    void listerReclamationsSeed() throws Exception {
        MvcResult result = apiGet("/api/reclamations", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        JsonNode array = node(result);
        assertThat(array.size()).isEqualTo(1);
        JsonNode r = array.get(0);
        assertThat(r.get("ticketNumero").asText()).isEqualTo("TKT-2026-1250");
        assertThat(r.get("statut").asText()).isEqualTo("OUVERTE");
        assertThat(r.get("quantiteManquante").asInt()).isEqualTo(4);
        assertThat(r.get("estDemo").asBoolean()).isTrue();
    }

    @Test
    void creerReclamation() throws Exception {
        MvcResult result = apiPost("/api/reclamations", tokenAdmin(), Map.of(
                "ticketId", 5,
                "motif", "Engrais non retiré",
                "description", "Ticket payé mais aucune distribution enregistrée",
                "quantiteManquante", 2));
        assertThat(code(result)).isEqualTo(200);
        JsonNode r = node(result);
        assertThat(r.get("ticketId").asLong()).isEqualTo(5);
        assertThat(r.get("ticketNumero").asText()).isEqualTo("TKT-2026-1251");
        assertThat(r.get("statut").asText()).isEqualTo("OUVERTE");
        assertThat(r.get("quantiteManquante").asInt()).isEqualTo(2);
        assertThat(r.get("dateResolution").isNull()).isTrue();

        MvcResult liste = apiGet("/api/reclamations", tokenAdmin());
        assertThat(node(liste).size()).isEqualTo(2);
    }

    @Test
    void creerReclamationSansMotifRefuse() throws Exception {
        MvcResult result = apiPost("/api/reclamations", tokenAdmin(), Map.of(
                "ticketId", 5,
                "description", "Motif absent",
                "quantiteManquante", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void doublonReclamationOuverteRefuse() throws Exception {
        // Le ticket 4 possède déjà une réclamation OUVERTE dans le jeu de données.
        MvcResult result = apiPost("/api/reclamations", tokenAdmin(), Map.of(
                "ticketId", 4,
                "motif", "Deuxième réclamation",
                "quantiteManquante", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void quantiteManquanteSuperieureAuResteRefusee() throws Exception {
        // Ticket 1 : 5 sacs commandés, 3 servis, il reste 2 sacs.
        MvcResult result = apiPost("/api/reclamations", tokenAdmin(), Map.of(
                "ticketId", 1,
                "motif", "Quantité incohérente",
                "quantiteManquante", 5));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void clotureSansResolutionRefusee() throws Exception {
        MvcResult result = apiPatch("/api/reclamations/1/statut", tokenAdmin(),
                Map.of("statut", "RESOLUE"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void clotureAvecResolutionAcceptee() throws Exception {
        MvcResult result = apiPatch("/api/reclamations/1/statut", tokenAdmin(), Map.of(
                "statut", "RESOLUE",
                "resolution", "Engrais remis à l'agriculteur le 2026-11-08"));
        assertThat(code(result)).isEqualTo(200);
        JsonNode r = node(result);
        assertThat(r.get("statut").asText()).isEqualTo("RESOLUE");
        assertThat(r.get("resolution").asText()).contains("remis");
        assertThat(r.get("dateResolution").isNull()).isFalse();
    }

    @Test
    void statutInvalideRefuse() throws Exception {
        MvcResult result = apiPatch("/api/reclamations/1/statut", tokenAdmin(),
                Map.of("statut", "EN_COURS", "resolution", "Test"));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void listerFiltreParStatut() throws Exception {
        MvcResult result = apiGet("/api/reclamations?statut=RESOLUE", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).size()).isEqualTo(0);

        MvcResult ouvertes = apiGet("/api/reclamations?statut=OUVERTE", tokenAdmin());
        assertThat(code(ouvertes)).isEqualTo(200);
        assertThat(node(ouvertes).size()).isEqualTo(1);
    }

    @Test
    void agentCollinePeutCreerReclamation() throws Exception {
        MvcResult result = apiPost("/api/reclamations", token("agent.colline"), Map.of(
                "ticketId", 5,
                "motif", "Signalement terrain",
                "quantiteManquante", 1));
        assertThat(code(result)).isEqualTo(200);
    }

    @Test
    void superviseurNePeutPasCreerReclamation() throws Exception {
        MvcResult result = apiPost("/api/reclamations", token("superviseur"), Map.of(
                "ticketId", 5,
                "motif", "Tentative non autorisée",
                "quantiteManquante", 1));
        assertThat(code(result)).isEqualTo(403);
    }

    @Test
    void agentLogistiqueNePeutPasCloturerReclamation() throws Exception {
        MvcResult result = apiPatch("/api/reclamations/1/statut", token("agent.fomi"), Map.of(
                "statut", "RESOLUE",
                "resolution", "Tentative non autorisée"));
        assertThat(code(result)).isEqualTo(403);
    }
}
