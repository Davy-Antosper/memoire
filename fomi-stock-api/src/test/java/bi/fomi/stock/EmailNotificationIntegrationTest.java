package bi.fomi.stock;

import bi.fomi.stock.service.MailSenderPort;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MvcResult;

import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.contains;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;

@TestPropertySource(properties = "fomi.mail.enabled=true")
class EmailNotificationIntegrationTest extends BaseIntegrationTest {

    @MockBean
    private MailSenderPort mailSenderPort;

    @Test
    void agriculteurExposeSonEmail() throws Exception {
        MvcResult result = apiGet("/api/agriculteurs/1", tokenAdmin());
        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("email").asText()).isEqualTo("jean.ndayisaba@example.bi");
    }

    @Test
    void notifierAgriculteurParEndpoint() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiPost("/api/agriculteurs/1/notifier", token, Map.of(
                "sujet", "Engrais disponible",
                "message", "Votre engrais UREE est disponible au dépôt de Mutaho."));

        assertThat(code(result)).isEqualTo(200);
        assertThat(node(result).get("envoye").asBoolean()).isTrue();
        assertThat(node(result).get("destinataire").asText()).isEqualTo("jean.ndayisaba@example.bi");
        verify(mailSenderPort).envoyer(eq("jean.ndayisaba@example.bi"),
                contains("Engrais disponible"), contains("dépôt de Mutaho"));
    }

    @Test
    void creationTicketNotifieAgriculteur() throws Exception {
        String token = tokenAdmin();
        MvcResult result = apiPost("/api/tickets", token, Map.of(
                "numeroTicket", "TKT-EMAIL-001",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 1,
                "montantPaye", 25000,
                "datePaiement", "2026-04-01",
                "depotRetraitId", 1,
                "saison", "2026E1"));

        assertThat(code(result)).isEqualTo(200);
        verify(mailSenderPort).envoyer(eq("jean.ndayisaba@example.bi"),
                contains("TKT-EMAIL-001"), contains("EN_ATTENTE_DE_VALIDATION"));
    }

    @Test
    void activationEtRejetNotifientAgriculteur() throws Exception {
        String token = tokenAdmin();

        long idActif = node(apiPost("/api/tickets", token, Map.of(
                "numeroTicket", "TKT-EMAIL-002",
                "agriculteurId", 1,
                "engraisTypeId", 1,
                "quantiteCommandee", 1,
                "montantPaye", 25000,
                "datePaiement", "2026-04-02",
                "depotRetraitId", 1,
                "saison", "2026E2"))).get("id").asLong();
        assertThat(code(apiPatch("/api/tickets/" + idActif + "/activer", token))).isEqualTo(200);

        long idRejete = node(apiPost("/api/tickets", token, Map.of(
                "numeroTicket", "TKT-EMAIL-003",
                "agriculteurId", 1,
                "engraisTypeId", 2,
                "quantiteCommandee", 1,
                "montantPaye", 25000,
                "datePaiement", "2026-04-03",
                "depotRetraitId", 1,
                "saison", "2026E3"))).get("id").asLong();
        assertThat(code(apiPatch("/api/tickets/" + idRejete + "/rejeter", token,
                Map.of("motif", "Superficie insuffisante")))).isEqualTo(200);

        verify(mailSenderPort).envoyer(eq("jean.ndayisaba@example.bi"),
                contains("TKT-EMAIL-002"), contains("ACTIF"));
        verify(mailSenderPort).envoyer(eq("jean.ndayisaba@example.bi"),
                contains("TKT-EMAIL-003"), contains("REJETE"));
    }

    @Test
    void emailInvalideRefuse() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-EMAIL-INVALIDE",
                "nom", "Test",
                "prenom", "Email",
                "email", "pas-un-email",
                "collineId", 1));
        assertThat(code(result)).isEqualTo(400);
        verify(mailSenderPort, never()).envoyer(eq("pas-un-email"), contains(""), contains(""));
    }

    @Test
    void emailDejaUtiliseRefuse() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs", tokenAdmin(), Map.of(
                "numeroIdentite", "AGR-EMAIL-DOUBLON",
                "nom", "Test",
                "prenom", "Doublon",
                "email", "jean.ndayisaba@example.bi",
                "collineId", 1));
        assertThat(code(result)).isEqualTo(400);
    }

    @Test
    void agriculteurSansEmailNePeutPasEtreNotifie() throws Exception {
        String token = tokenAdmin();
        long id = node(apiPost("/api/agriculteurs", token, Map.of(
                "numeroIdentite", "AGR-EMAIL-ABSENT",
                "nom", "Sans",
                "prenom", "Email",
                "collineId", 1))).get("id").asLong();

        MvcResult result = apiPost("/api/agriculteurs/" + id + "/notifier", token, Map.of(
                "sujet", "Test",
                "message", "Ce message ne doit pas partir"));
        assertThat(code(result)).isEqualTo(400);
        verify(mailSenderPort, never()).envoyer(eq(""), contains("Test"), contains("message"));
    }

    @Test
    void notificationInterditeAgentLogistique() throws Exception {
        MvcResult result = apiPost("/api/agriculteurs/1/notifier", token("agent.fomi"), Map.of(
                "sujet", "Test",
                "message", "Interdit"));
        assertThat(code(result)).isEqualTo(403);
        verify(mailSenderPort, never()).envoyer(eq("jean.ndayisaba@example.bi"),
                contains("Test"), contains("Interdit"));
    }
}
